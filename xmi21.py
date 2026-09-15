#!/usr/bin/env python
"""Generic reader for XMI 2.1 / EMF-style UML instance models.

Built against the OMG-published UPDM example `DoDAFLibrary.xmi`
(UML 20090901 namespace, XMI 2.1). Corpus eligibility: OMG-published
models only (see REPORT.md; commercial book models excluded).

Dialect features handled (all distinct from the UML 2.5 metamodel XMI):

  - xmi:id / xmi:uuid / xmi:type are plain XML attributes (XMI 2.1
    namespace declared in the document); references use xmi:idref.
  - Metaclass instances: the root UML-Namespace element is in a UML
    namespace, but its containment features (packagedElement,
    ownedAttribute, ownedComment, memberEnd, type, name, body, ...)
    are UNPREFIXED child tags.
  - String-valued features are child elements (`<name>`,
    `<body>`, `<visibility>`), not XML attributes.
  - Multiplicity literals: `<lowerValue xmi:type="uml:LiteralUnlimited-
    Natural"/>` (no value child = EMF attribute default 1) and
    `<upperValue ...><value>*</value></upperValue>` ('*' = unbounded).
  - Cross-file type references: `<type href="...UML.xmi#String"/>` --
    resolved to a synthetic external marker (the referenced file is
    OMG-published; the reference itself is recorded verbatim).
  - Stereotype applications: top-level elements in profile namespaces
    (e.g. `updm:Measurement`, `StandardProfileL2:ModelLibrary`) holding
    `base_<Metaclass xmi:idref="...">` extension ends -- UML 2.1-style
    profile application, collected as an application map (not folded).

Objects are instances of the generated gen.uml25 metaclasses, so the
v1->v2 emitter works on the result unchanged.
"""
from __future__ import annotations

from lxml import etree

import gen.uml25 as U

XMI_NS = "{http://schema.omg.org/spec/XMI/2.1}"

# containment features (composite; child elements own sub-objects)
COMPOSITE = {"packagedElement", "nestedClassifier", "ownedAttribute",
             "ownedLiteral", "ownedEnd", "ownedComment", "ownedConnector",
             "ownedParameter", "ownedOperation", "ownedMember", "region",
             "subvertex", "transition"}
# single-value string features
STRING = {"name", "body", "visibility", "language"}
# single reference features
REF_SINGLE = {"type", "association", "general", "classifier", "specification"}
# multi reference features (may arrive before their targets)
REF_MULTI = {"memberEnd", "annotatedElement", "client", "supplier"}
# multiplicity literal features
LITERAL = {"lowerValue", "upperValue", "defaultValue"}

# metaclass names constructible in gen.uml25 (instances, not abstract)
CONSTRUCTIBLE = {"Model", "Package", "Class", "DataType", "Enumeration",
                 "Association", "Property", "Port", "Comment",
                 "EnumerationLiteral", "LiteralInteger",
                 "LiteralUnlimitedNatural", "LiteralString", "Operation",
                 "OpaqueExpression", "Connector", "ConnectorEnd",
                 "Generalization", "InstanceSpecification", "Slot",
                 "InstanceValue", "Dependency", "Interface"}

# metaclasses for which a missing name is derived from the xmi:id tail
# (recorded in derived_names, never silently invented)
NAME_DERIVABLE = {"Model", "Package", "Class", "DataType", "Enumeration",
                  "Association", "Property", "Port", "EnumerationLiteral",
                  "Operation"}


class UnresolvedReference(Exception):
    """A dangling reference in the instance model."""


class XMI21Model:
    """Result of reading an XMI 2.1 instance file."""

    def __init__(self):
        self.objects = {}        # xmi:id -> gen.uml25 element (metamodel only)
        self.apps = {}           # base xmi:id -> [(profile, stereo, app_id)]
        self.hrefs = []          # (xmi:id, feature, href) external refs
        self.synthetic_types = {}  # href -> synthetic U.DataType
        self.unmapped = []       # (xmi:id, tag) not constructible
        self.unmapped_features = []  # (xmi:id, feature) not in the tables
        self.profiles = []       # appliedProfile hrefs
        self.roots = []          # top-level UML Namespace objects
        self.derived_names = []  # (xmi:id, derived name) provenance record
        self.pending = []        # (obj, feature, idref|href, single)


def read_xmi21(path) -> XMI21Model:
    root = etree.parse(str(path)).getroot()
    xmi = XMI21Model()

    def xid(e):
        return e.get(XMI_NS + "id")

    def xtype(e):
        return e.get(XMI_NS + "type")

    def is_uml_ns(e):
        ns = etree.QName(e).namespace or ""
        return "omg.org/spec/UML" in ns or "schema.omg.org/spec/UML" in ns

    def construct(e):
        mname = (xtype(e) or "").split(":")[-1]
        if not mname:
            return None
        cls = U.metaclass(mname)
        if cls is None or cls.__name__ not in CONSTRUCTIBLE:
            xmi.unmapped.append((xid(e), mname))
            return None
        try:
            obj = cls()
        except TypeError:
            xmi.unmapped.append((xid(e), mname))
            return None
        i = xid(e)
        if i:
            xmi.objects[i] = obj
            try:
                obj._xmi_id = i
            except Exception:
                pass
        return obj

    def walk(el, obj):
        for c in el:
            feat = etree.QName(c).localname
            if feat in STRING:
                if c.text is not None and c.text.strip():
                    obj._vals[feat] = c.text.strip()
                continue
            if feat in LITERAL:
                lit = construct(c)
                if lit is None:
                    continue
                obj._vals[feat] = lit
                v = next((g for g in c
                          if etree.QName(g).localname == "value"), None)
                text = v.text.strip() if v is not None and v.text \
                    and v.text.strip() else None
                if isinstance(lit, U.LiteralString):
                    if text is not None:
                        lit._vals["value"] = text
                elif isinstance(lit, U.LiteralInteger):
                    if text is not None:
                        lit._vals["value"] = int(text)
                elif isinstance(lit, U.LiteralUnlimitedNatural):
                    if text == "*":
                        lit._vals["value"] = U.UnlimitedNatural("*")
                    elif text is not None:
                        lit._vals["value"] = U.UnlimitedNatural(int(text))
                    else:
                        # EMF serialization omits <value> when it equals the
                        # feature default: 0 for UnlimitedNatural (so an
                        # empty <lowerValue/> = 0, i.e. [0..*] with '*').
                        lit._vals["value"] = U.UnlimitedNatural(0)
                continue
            idref = c.get(XMI_NS + "idref")
            href = c.get("href")
            if feat in REF_SINGLE:
                if idref is not None or href is not None:
                    xmi.pending.append((obj, feat, idref or href, True))
                else:
                    xmi.unmapped_features.append((xid(el), feat))
                continue
            if feat in REF_MULTI:
                if idref is not None:
                    xmi.pending.append((obj, feat, idref, False))
                else:
                    xmi.unmapped_features.append((xid(el), feat))
                continue
            if feat in COMPOSITE:
                child = construct(c)
                if child is None:
                    continue
                try:
                    obj.add(feat, child)
                except (AttributeError, TypeError) as ex:
                    xmi.unmapped_features.append((xid(el), feat + "=" + str(ex)[:60]))
                walk(c, child)
                continue
            if feat == "profileApplication":
                xmi.profiles.extend(h for g in c
                                    if etree.QName(g).localname == "appliedProfile"
                                    for h in [g.get("href")] if h)
                continue
            xmi.unmapped_features.append((xid(el), feat))

    # ---- top-level UML elements --------------------------------------------
    for e in root:
        ns = etree.QName(e).namespace or ""
        if not ns or "schema.omg.org/spec/XMI" in ns:
            continue
        if "omg.org/spec/UML" in ns and \
                etree.QName(e).localname in ("Model", "Package"):
            obj = construct(e)
            if obj is not None:
                xmi.roots.append(obj)
                walk(e, obj)

    # ---- resolve pending references -----------------------------------------
    for obj, feat, ref, single in xmi.pending:
        if ref.startswith("http"):
            xmi.hrefs.append((obj._xmi_id if hasattr(obj, "_xmi_id") else "?",
                              feat, ref))
            if feat == "type":
                # synthetic stand-in for an OMG-published external type
                frag = ref.split("#")[-1]
                st = xmi.synthetic_types.get(frag)
                if st is None:
                    st = U.DataType(name=frag)
                    st._external_href = ref
                    xmi.synthetic_types[frag] = st
                setattr(obj, feat, st)
            continue
        target = xmi.objects.get(ref)
        if target is None:
            raise UnresolvedReference(
                f"{type(obj).__name__}.{feat} -> xmi:idref {ref!r} unresolved")
        if single:
            obj._vals[feat] = target
        else:
            obj._vals[feat] = (obj._vals.get(feat) or []) + [target]

    # ---- stereotype applications (top-level, non-metamodel elements) -------
    for e in root:
        ns = etree.QName(e).namespace or ""
        if "schema.omg.org/spec/XMI" in ns:
            continue
        if "omg.org/spec/UML" in ns and \
                etree.QName(e).localname in ("Model", "Package"):
            continue  # UML metamodel root(s), already walked
        app_id = xid(e)
        stereo = etree.QName(e).localname
        profile = e.prefix or ns.rsplit("/", 1)[-1]
        for c in e:
            if etree.QName(c).localname.startswith("base_"):
                ref = c.get(XMI_NS + "idref")
                base = xmi.objects.get(ref)
                if base is not None:
                    xmi.apps.setdefault(ref, []).append((profile, stereo, app_id))
    for base_id, lst in xmi.apps.items():
        base = xmi.objects.get(base_id)
        if base is not None:
            base._applied_stereotypes = lst

    # ---- derived names for unnamed elements (provenance recorded) ----------
    for i, obj in xmi.objects.items():
        if type(obj).__name__ in NAME_DERIVABLE \
                and not (isinstance(obj.name, str) and obj.name):
            tail = i.rsplit("-", 1)[-1]
            if tail.isdigit() and "-" in i:
                # RSA numbering: '<pkg>-<feature>-<n>' -> '<feature>-<n>'
                tail = i.rsplit("-", 2)[-2] + "-" + tail
            obj._vals["name"] = tail
            xmi.derived_names.append((i, tail))
    return xmi