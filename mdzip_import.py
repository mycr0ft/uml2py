#!/usr/bin/env python
"""mdzip_import.py - MagicDraw/Cameo .mdzip -> gen.uml25 objects.

Increment 2 of the mdzip pipeline (mdzip.py is the scrape/forensics layer).
Strategy: mdzip model members are XMI 2.0 snapshots of ONE model, split so
that references resolve globally by xmi:id.  So the importer

  1. merges every umodel-snapshot member under a synthetic
     <uml:Model xmi:id="_md_import_root"> root (plain idrefs then resolve
     in-document for read_xmi21);
  2. coerces element types that MagicDraw serializes as raw metamodel IDs
     (xmi:type="_9_0_2_91a0295_...") -- first from the parent feature's
     declared metaclass in gen.uml25 (the metamodel itself is the map),
     then from a small structural signature table;
  3. rewrites cross-project references (local:/PROJECT-<id>?resource=...,
     the proxy/usage mechanism) into http-synthetic hrefs so read_xmi21
     records them as external markers instead of raising;
  4. drops duplicate xmi:id subtrees (delta snapshots) with a record;
  5. delegates to xmi21.read_xmi21 unchanged and reports provenance
     (usages, version eras) alongside construction stats.

Profile *definition* elements (MD's built-in stereotypes/extensions and
their tag definitions) are intentionally recorded, not constructed: they
are the wave-2 layer.  Encrypted projects raise MdZipImportError.

Usage:  python mdzip_import.py <file.mdzip> [--stats]
    (mainly a library: from mdzip_import import import_mdzip)
"""
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mdzip import MdZip  # noqa: E402
from xmi21 import read_xmi21, CONSTRUCTIBLE  # noqa: E402
from gen import uml25 as U  # noqa: E402

OMG_XMI = "http://www.omg.org/XMI"              # XMI 2.0 (Nomagic spells attrs here)
OMG_XMI_25 = "http://www.omg.org/spec/XMI/20131001"   # what read_xmi21 accepts
OMG_UML_251 = "http://www.omg.org/spec/UML/20161101"
SYNTH_BASE = "http://mdzip.import.invalid"

XMI20_PREFIX = "{http://www.omg.org/XMI}"
XMI25_PREFIX = "{" + OMG_XMI_25 + "}"

# project-reference href forms: local:/PROJECT-x?resource=... (dependency
# list), PROJECT-x?resource=... (owningPackage etc.), plain PROJECT-x
PROJECT_HREF = re.compile(
    r"^(?:local:)?/?(PROJECT-[0-9a-zA-Z_+-]+)(?:\?resource=([^#]*))?(#.*)?$")

RAW_TYPE = re.compile(r"^_[0-9a-zA-Z_]+$")


def _local(tag):
    return tag.split("}")[-1] if "}" in tag else tag


def _xmi_attr(el, name):
    for k, v in el.attrib.items():
        if _local(k) == name:
            return v
    return None


class MdZipImportError(Exception):
    """The archive cannot be imported (encrypted, no model members, ...)."""


class MdZipImport:
    """Result of importing one .mdzip."""

    def __init__(self):
        self.xmi = None          # xmi21.XMI21Model
        self.usages = []         # referenced PROJECT ids (mdzip-level)
        self.eras = []           # version fingerprints (mdzip-level)
        self.description = None
        self.members_used = 0
        self.coercions = []      # (xmi:id, raw_type, metaclass, rule)
        self.duplicates = []     # xmi:id values dropped (delta snapshots)
        self.cross_project = []  # rewritten hrefs
        self.dangling_internal = []  # '#id' refs to nothing, made synthetic
        self.name_refs = []          # name-typed refs (type="uml:Property")
        self.raw_unresolved = []     # (xmi:id, raw_type) left for wave-2
        self.skipped_stray = 0

    def stats(self):
        by_class = Counter(type(o).__name__ for o in self.xmi.objects.values())
        return {
            "objects": len(self.xmi.objects),
            "by_metaclass": dict(by_class.most_common()),
            "apps": sum(len(v) for v in self.xmi.apps.values()),
            "hrefs": len(self.xmi.hrefs),
            "unmapped": len(self.xmi.unmapped),
            "unmapped_features": len(self.xmi.unmapped_features),
            "roots": len(self.xmi.roots),
            "members_used": self.members_used,
            "coercions": len(self.coercions),
            "duplicates_dropped": len(self.duplicates),
            "cross_project_refs": len(self.cross_project),
            "dangling_internal_refs": len(self.dangling_internal),
            "name_refs": len(self.name_refs),
            "raw_unresolved": len(self.raw_unresolved),
            "skipped_stray": self.skipped_stray,
        }


class _PropsCache:
    """gen.uml25 feature descriptors without re-instantiating constantly."""

    def __init__(self):
        self._d = {}

    def descriptor(self, cls, feat):
        key = (cls.__name__, feat)
        if key not in self._d:
            try:
                inst = cls() if not cls.__dict__.get("_ABSTRACT", False) else None
            except TypeError:
                inst = None
            if inst is None:
                self._d[key] = None
            else:
                self._d[key] = inst._props.get(feat)
        return self._d[key]


_PROPS = _PropsCache()

# structural Property signature (MagicDraw tag/attribute definitions that
# lost their metaclass to raw-ID typing)
PROPERTY_SIG_CHILDREN = {"taggedValue", "lowerValue", "upperValue",
                         "defaultValue", "ownedComment", "specification"}
PROPERTY_SIG_ATTRS = {"name", "visibility", "aggregation", "isUnique",
                      "isOrdered", "isReadOnly", "isDerived", "association"}


def _looks_like_property(el):
    kids = {_local(c.tag) for c in el}
    if not kids <= PROPERTY_SIG_CHILDREN:
        return False
    attrs = {_local(k) for k in el.attrib} - {"type", "id", "ID", "href"}
    return "name" in attrs and "visibility" in attrs \
        and attrs <= PROPERTY_SIG_ATTRS | {"appliedStereotype"}


def _cls_of(name):
    """U.metaclass that tolerates Nomagic's non-standard uml:X names."""
    return U.metaclass(name) if U.metaclass(name) is not None else None


def _metaclass_safe(name):
    try:
        return U.metaclass(name)
    except KeyError:
        return None


# feature -> constructible metaclass when the child omits xmi:type
# (composite/reference features whose type is fixed by UML 2.5.1)
FEATURE_TYPE = {"ownedAttribute": "Property", "ownedEnd": "Property",
                "generalization": "Generalization",
                "ownedLiteral": "EnumerationLiteral", "slot": "Slot",
                "ownedOperation": "Operation", "ownedConnector": "Connector",
                "ownedComment": "Comment", "ownedRule": "Constraint",
                "ownedParameter": "Parameter",
                "_extensionEndOfType": "ExtensionEnd"}


def _inject_types_from_tags(root, imp):
    """xmi:type where it is absent: (a) from the element tag for
    OMG-uml-namespaced top-level elements; (b) from the parent feature
    for composite children whose metaclass the feature fixes."""
    n = 0
    for el in root.iter():
        tag = el.tag
        if isinstance(tag, str) and tag.startswith(f"{{{OMG_UML_251}}}") \
                and _local(el.tag).startswith("uml:") is False \
                and _metaclass_safe(_local(el.tag)) is not None \
                and _xmi_attr(el, "type") is None:
            el.set(XMI25_PREFIX + "type", "uml:" + _local(el.tag))
            n += 1
        for c in el:
            if c.get(XMI25_PREFIX + "type") is not None:
                continue
            feat = _local(c.tag) if isinstance(c.tag, str) else None
            mt = FEATURE_TYPE.get(feat) if feat else None
            if mt and _metaclass_safe(mt) is not None:
                # only inject when the feature descriptor agrees and the
                # child is inline content (not a bare idref reference)
                ptype = _xmi_attr(el, "type") or ""
                pcls = _metaclass_safe(ptype.split(":")[-1]) \
                    if ptype.startswith("uml:") else None
                if pcls is not None:
                    d = _PROPS.descriptor(pcls, feat)
                    if d is not None and isinstance(d.t, str) \
                            and d.t.split(":")[-1] == mt:
                        has_ref = any(_local(k) in ("idref", "href")
                                      for k in c.attrib)
                        if not has_ref:
                            c.set(XMI25_PREFIX + "type", "uml:" + mt)
                            n += 1
    imp.tag_type_injections = n
    return n


def _coerce_types(root, imp, report):
    """Rewrite raw-ID xmi:type values where the target metaclass is certain.

    rule 'parent-feature': the parent feature descriptor names one
    constructible metaclass -- the metamodel itself is the ID map.
    rule 'property-signature': structural fingerprint of MD tag
    definitions.  Everything else is left verbatim and reported.
    """
    for parent in root.iter():
        ptype = _xmi_attr(parent, "type") or ""
        pcls = _metaclass_safe(ptype.split(":")[-1]) if ptype.startswith("uml:") \
            else None
        for el in parent:
            t = _xmi_attr(el, "type")
            if not t or t.startswith("uml:"):
                continue
            eid = _xmi_attr(el, "id")
            feat = _local(parent.tag) if parent is not root else None
            if pcls is not None and feat:
                d = _PROPS.descriptor(pcls, feat)
                if d is not None and not d.multi and isinstance(d.t, str):
                    cls = _metaclass_safe(d.t)
                    if cls is not None and cls.__name__ != "Element":
                        k = [k for k in el.attrib if _local(k) == "type"][0]
                        el.set(k, "uml:" + cls.__name__)
                        imp.coercions.append((eid, t, cls.__name__,
                                              "parent-feature"))
                        continue
            if _looks_like_property(el):
                k = [k for k in el.attrib if _local(k) == "type"][0]
                el.set(k, "uml:Property")
                imp.coercions.append((eid, t, "Property", "property-signature"))
                continue
            imp.raw_unresolved.append((eid, t))


def _scrub_refs(root, imp):
    """Cross-project refs, dangling refs, name-typed refs -> synthetic hrefs.

    References to non-constructible profile-layer elements (Profile,
    Stereotype, Extension, tagged-value metaclasses) also become synthetic
    external markers: read_xmi21 records them verbatim instead of raising
    on the wave-2 boundary.
    """
    ids = set()
    ids_bad = set()
    for el in root.iter():
        i = _xmi_attr(el, "id")
        if i:
            ids.add(i)
            t = _xmi_attr(el, "type") or ""
            name = t.split(":")[-1]
            if not t.startswith("uml:") or name not in CONSTRUCTIBLE:
                ids_bad.add(i)
    n_cross = n_dangle = n_name = 0
    for el in root.iter():
        for k, v in list(el.attrib.items()):
            auri, _, ln = k.rpartition("}")
            if not v:
                continue
            if ln not in ("href", "idref", "type") or auri:
                continue    # xmi:type (metaclass decl) and other ns attrs pass
            if ln == "idref" and v in ids:
                continue    # real idref, reader handles it
            m = PROJECT_HREF.match(v)
            if m and (v.startswith("local:") or "?resource=" in v
                      or not v.startswith("#")):
                rest = v
                if rest.startswith("local:"):
                    rest = rest[len("local:"):]
                new = f"{SYNTH_BASE}/{rest.lstrip('/')}"
                el.set(k, new)
                imp.cross_project.append((_xmi_attr(el, "id"), ln, v))
                n_cross += 1
                continue
            if v.startswith("#"):
                if v[1:] in ids:
                    # in-document fragment href == xmi:idref semantics
                    if v[1:] in ids_bad:
                        el.set(k, f"{SYNTH_BASE}/profile-layer#{v[1:]}")
                    else:
                        del el.attrib[k]
                        el.set(XMI25_PREFIX + "idref", v[1:])
                else:
                    new = f"{SYNTH_BASE}/dangling#{v[1:]}"
                    el.set(k, new)
                    imp.dangling_internal.append((_xmi_attr(el, "id"), ln, v))
                    n_dangle += 1
                continue
            if ln == "idref":
                if v in ids_bad:
                    # idref to a non-constructible profile-layer element:
                    # convert to an external-style href so the reader
                    # records it rather than raising
                    del el.attrib[k]
                    el.set("href", f"{SYNTH_BASE}/profile-layer#{v}")
                    n_name += 1
                continue    # real idref to a constructible object
            # Nomagic dialect: name-typed references on reference features
            # (type="uml:Property") instead of idrefs; only for features the
            # reader treats as single refs, and only when the value is not
            # an id (Nomagic ids start with _ or are dashed/undashed hex)
            if v not in ids and \
                    re.fullmatch(r"[A-Za-z_][\w.]*(:[A-Za-z_][\w.]*)+", v):
                new = f"{SYNTH_BASE}/names#{v}"
                el.set(k, new)
                imp.name_refs.append((_xmi_attr(el, "id"), ln, v))
                n_name += 1
    return n_cross, n_dangle, n_name


def _drop_duplicates(root, imp):
    """Delta snapshots repeat xmi:ids across members; keep the LAST
    occurrence (later snapshots are the more-current form) and drop the
    earlier ones."""
    seen_last = {}
    for el in root.iter():
        i = _xmi_attr(el, "id")
        if i:
            seen_last.setdefault(i, []).append(el)
    dup_ids = {i for i, els in seen_last.items() if len(els) > 1}
    dropped = []
    # remove earlier duplicates: walk parents, drop any element whose id
    # is duplicated and that is NOT the last occurrence in document order
    order = {}
    for n, el in enumerate(root.iter()):
        i = _xmi_attr(el, "id")
        if i in dup_ids:
            order.setdefault(i, []).append((n, el))
    parents = {id(el): parent for parent in root.iter() for el in parent}
    for i, occ in order.items():
        for _, el in occ[:-1]:          # keep the last occurrence only
            parent = parents.get(id(el))
            if parent is not None:
                parent.remove(el)
                dropped.append(i)
    imp.duplicates = dropped
    return dropped


def _retag_xmi_namespace(el):
    """Rewrite Nomagic's attribute spellings to what read_xmi21 accepts.

    Two dialect traits, one namespace generation apart:
      - xmi:id / xmi:idref / xmi:uuid / xmi:version are serialized under
        http://www.omg.org/XMI (XMI 2.0); read_xmi21 accepts the 2.1-era
        schema.omg.org URI and the 20131001 omg.org URI.
      - element typing is xsi:type (XML-Schema spelling, XMI 2.0 style);
        read_xmi21 reads xmi:type.
    """
    for k in list(el.attrib):
        if k.startswith(XMI20_PREFIX):
            v = el.attrib.pop(k)
            el.attrib[XMI25_PREFIX + k[len(XMI20_PREFIX):]] = v
        elif k == "{http://www.w3.org/2001/XMLSchema-instance}type" \
                and (XMI25_PREFIX + "type") not in el.attrib:
            v = el.attrib.pop(k)
            el.attrib[XMI25_PREFIX + "type"] = v
    for c in el:
        _retag_xmi_namespace(c)


def _merged_document(mdzip):
    """All umodel members merged into one xmi:XMI document.

    mdzip snapshots follow XMI 2.0 style: top-level elements are tagged by
    TYPE (<uml:Package xmi:id=.../> under xmi:XMI) while nested containment
    children are tagged by FEATURE (<packagedElement>, <ownedAttribute>,
    ...).  read_xmi21 dispatches top-level Model/Package elements by
    xmi:type and walks their feature-tagged children, so member roots go
    directly under the merged XMI root; any other top-level UML element
    (uml:Profile, stray classes) is re-parented under a synthetic
    'holding_bin' package so it is constructed too, and its idrefs still
    resolve in-document.
    """
    ET.register_namespace("uml", OMG_UML_251)
    ET.register_namespace("xmi", OMG_XMI_25)
    root = ET.Element(f"{{{OMG_XMI_25}}}XMI")
    root.set(XMI25_PREFIX + "version", "2.0")
    holding = ET.Element(f"{{{OMG_UML_251}}}Package")
    holding.set(XMI25_PREFIX + "id", "_md_import_holding_bin")
    holding.set(XMI25_PREFIX + "type", "uml:Package")
    holding.set("name", "holding_bin")
    used = 0
    have_holding = False
    for name, text in mdzip.model_members():
        try:
            mroot = ET.fromstring(MdZip.alias_nomagic(text))
        except ET.ParseError:
            continue
        used += 1
        for child in list(mroot):
            ln = _local(child.tag)
            if isinstance(child.tag, str) \
                    and child.tag.startswith(f"{{{OMG_UML_251}}}") \
                    and ln in ("Model", "Package"):
                root.append(child)   # re-parent (splices the subtree)
            else:
                holding.append(child)
                have_holding = True
    if have_holding:
        root.append(holding)
    return root, used


def import_mdzip(path) -> MdZipImport:
    with MdZip(path) as md:
        inv = md.inventory()
        if not inv.get("umodel-snapshot"):
            raise MdZipImportError(f"{path}: no umodel snapshot members")
        imp = MdZipImport()
        imp.usages = md.usages()
        eras, _ = md.version_clues()
        imp.eras = eras
        desc, _ = md.project_description()
        imp.description = desc
        root, used = _merged_document(md)
        imp.members_used = used
        if not used:
            raise MdZipImportError(f"{path}: umodel members failed to parse")
        _retag_xmi_namespace(root)
        _inject_types_from_tags(root, imp)
        _coerce_types(root, imp, root)
        _drop_duplicates(root, imp)
        _scrub_refs(root, imp)
        with tempfile.NamedTemporaryFile("w", suffix=".xmi", delete=False,
                                         encoding="utf-8") as tf:
            ET.register_namespace("xmi", OMG_XMI)
            tree = ET.ElementTree(root)
            tree.write(tf, encoding="unicode", xml_declaration=True)
            tmppath = tf.name
        imp.xmi = read_xmi21(tmppath)
        return imp


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    imp = import_mdzip(argv[1])
    import json
    out = {"description": imp.description, "usages": imp.usages,
           "eras": imp.eras[:10], "stats": imp.stats(),
           "coercions_sample": imp.coercions[:10],
           "raw_unresolved_sample": imp.raw_unresolved[:10]}
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))