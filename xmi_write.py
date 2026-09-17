#!/usr/bin/env python
"""EMF-dialect XMI 2.1 instance writer - the write half of xmi21.py.

Serialization conventions (mirrored from the OMG-published UPDM example
DoDAFLibrary.xmi, the E1 oracle corpus; see PLAN.md probes P1-P3):

  - root <xmi:XMI> (xmi ns http://schema.omg.org/spec/XMI/2.1); UML roots
    in a UML namespace (default the corpus's 20090901 ns); stereotype
    applications as root-level children in profile namespaces;
  - composite features: feature-named nested child elements carrying
    xmi:type="uml:<Metaclass>" and xmi:id;
  - non-containment references: repeated feature-named child elements with
    xmi:idref (single-valued: one child); cross-file references: child
    element with href (the referenced object carries _external_href);
  - primitive- and enum-valued features: feature-named child elements with
    text (the corpus writes name/body/visibility/value this way; no
    boolean-valued feature occurs in the corpus - emitted the same way,
    'true'/'false', as a documented convention);
  - LiteralUnlimitedNatural 'value' == 0 is omitted (EMF writes the
    feature default as no child; the reader's inverse rule maps an empty
    <lowerValue/> to 0), '*' for unbounded;
  - derived/union/readonly properties are never emitted (they are not
    settable, so they are never stored);
  - profile applications: <profileApplication><appliedProfile href=.../>
    as a child of the first root;
  - deterministic ids: stored _xmi_id is reused (round-trip stable);
    otherwise '_<n>' in traversal order.

Usage (round-trip of a reader result):
    m = xmi21.read_xmi21(path)
    data = xmi_write.write_xmi(m.roots,
                               apps=xmi_write.apps_from_model(m),
                               nsmap=m.nsmap,
                               profile_applications=m.profiles)
"""
from __future__ import annotations

import enum as _enum

from lxml import etree

import gen.uml25 as U

XMI_NS = "http://schema.omg.org/spec/XMI/2.1"
UML_NS_DEFAULT = "http://www.omg.org/spec/UML/20090901"


class WriteError(Exception):
    """A reference target outside the containment graph (dangling)."""


def _text(v):
    """Text form of a primitive / enum / UnlimitedNatural value."""
    if isinstance(v, U.UnlimitedNatural):
        return "*" if v.unbounded else str(v.n)
    if isinstance(v, _enum.Enum):
        return str(v.value)
    if isinstance(v, bool):
        return "true" if v else "false"
    return str(v)


def _iter_graph(roots):
    """Deterministic DFS over composite containment from the roots."""
    seen, order = set(), []

    def visit(el):
        if id(el) in seen:
            return
        seen.add(id(el))
        order.append(el)
        for name, d in type(el)._props.items():
            if not d.composite:
                continue
            v = el._vals.get(name)
            if v is None:
                continue
            for it in (v if isinstance(v, (list, tuple)) else (v,)):
                if isinstance(it, U.Element) \
                        and not getattr(it, "_external_href", None):
                    visit(it)

    for r in roots:
        visit(r)
    return order


class _Ids:
    """Identity map: reuse stored _xmi_id, else deterministic '_<n>'."""

    def __init__(self):
        self.by_object = {}
        self.next = 1

    def ident(self, el):
        i = getattr(el, "_xmi_id", None)
        if i:
            return i
        if id(el) not in self.by_object:
            self.by_object[id(el)] = f"_{self.next}"
            self.next += 1
        return self.by_object[id(el)]


def _feat_kind(d):
    """('composite' | 'text' | 'ref') emission form for a property."""
    t = d.t
    if d.composite:
        return "composite"
    if t is str or t is int or t is bool:
        return "text"
    if isinstance(t, type) and (issubclass(t, _enum.Enum)
                                or issubclass(t, U.UnlimitedNatural)):
        return "text"
    return "ref"


def _app_uri(profile, nsmap, profiles):
    """Namespace URI for an application's profile: nsmap prefix first,
    then the profile module's _URI (only carried by UAF.xmi; the
    StandardProfile / SysML XMI have no <URI> child)."""
    if profile in nsmap:
        return nsmap[profile]
    mod = (profiles or {}).get(profile)
    if mod is not None and getattr(mod, "_URI", None):
        return mod._URI
    raise WriteError(
        f"application profile {profile!r} has no namespace URI (missing "
        f"from nsmap and no _URI on the provided profile module)")


def _ext_base(profiles, profile, stereo):
    """base_<Metaclass> feature for a stereotype from the profile module's
    _EXTENSIONS table (most-general extended metaclass = first entry)."""
    mod = (profiles or {}).get(profile)
    ext = getattr(mod, "_EXTENSIONS", None) if mod is not None else None
    if ext and ext.get(stereo):
        return "base_" + ext[stereo][0][0]
    return None


def _apps_key(app):
    return (app[0], app[1], app[3] if len(app) > 3 else "",
            app[2] if isinstance(app[2], str) else id(app[2]),
            app[4] if len(app) > 4 else "")


def apps_from_model(m):
    """Application tuples (profile, stereo, base_id, app_id, base_feat)
    from a reader XMI21Model (base metas from app_metas, with a
    base_<Metaclass of the base element> fallback)."""
    out = []
    for base_id, lst in m.apps.items():
        base = m.objects.get(base_id)
        for profile, stereo, app_id in lst:
            meta = m.app_metas.get(app_id) \
                or (f"base_{type(base).__name__}" if base is not None
                    else None)
            out.append((profile, stereo, base_id, app_id, meta,
                        dict(m.app_tags.get(app_id) or {})))
    out.sort(key=_apps_key)
    return out


def write_xmi(roots, apps=None, nsmap=None, profile_applications=(),
              uml_ns=UML_NS_DEFAULT, profiles=None):
    """Serialize an object graph (and optional profile applications) as
    EMF-dialect XMI. Returns bytes.

    The XMI dialect is taken from nsmap['xmi'] when present: the 2003-era
    2.1 URI (DoDAFLibrary.xmi) writes applications with base_<Meta> idref
    children; any later URI (MeasurementsLibrary.xmi, P10) writes the
    2.5.1-era EMF form - prefixed application elements with base_<Meta>
    (and tag) attributes. nsmap['uml'] likewise overrides uml_ns.
    `profiles` maps a profile name to its generated module (with _URI /
    _EXTENSIONS) for applications whose URI is not in nsmap."""
    apps = sorted(apps or [], key=_apps_key)
    nsmap = dict(nsmap or {"xmi": XMI_NS, "uml": uml_ns})
    xmi_uri = nsmap.get("xmi", XMI_NS)
    if "xmi" not in nsmap:
        nsmap = {"xmi": xmi_uri, **nsmap}
    uml_ns = nsmap.get("uml", uml_ns)
    p10 = xmi_uri != XMI_NS
    ids = _Ids()
    graph = _iter_graph(roots)
    in_graph = {id(el) for el in graph}

    root = etree.Element(f"{{{xmi_uri}}}XMI", nsmap=nsmap)

    def ref_child(parent, name, target):
        href = getattr(target, "_external_href", None)
        c = etree.SubElement(parent, name)
        if href:
            c.set("href", href)
            return c
        if id(target) not in in_graph:
            raise WriteError(
                f"{name}: reference target {type(target).__name__!r} is "
                f"outside the written graph (dangling)")
        c.set(f"{{{xmi_uri}}}idref", ids.ident(target))
        return c

    # ---- stereotype applications first (corpus document order) -----------
    for app in apps:
        profile, stereo, base, app_id, base_feat = app[:5]
        tags = app[5] if len(app) > 5 else None
        uri = _app_uri(profile, nsmap, profiles)
        a = etree.SubElement(root, f"{{{uri}}}{stereo}")
        if app_id:
            a.set(f"{{{xmi_uri}}}id", app_id)
        if isinstance(base, str):
            base_id = base
            if not base_feat:
                base_feat = _ext_base(profiles, profile, stereo)
                if base_feat is None:
                    raise WriteError(
                        f"application {profile}::{stereo}: base element "
                        f"given as id without base_<Meta> feature and no "
                        f"profiles module to resolve it")
        else:
            base_id = ids.ident(base)
        bf = base_feat or "base_" + type(base).__name__
        if p10:
            a.set(bf, base_id)
            for tk, tv in sorted((tags or {}).items()):
                a.set(tk, tv)
        else:
            etree.SubElement(a, bf).set(f"{{{xmi_uri}}}idref", base_id)
            if tags:
                for tk, tv in sorted(tags.items()):
                    tc = etree.SubElement(a, tk)
                    tc.text = tv

    # ---- UML elements ------------------------------------------------------
    def build(el, parent, tag, owner=None, opp_name=None):
        e = etree.SubElement(parent, tag)
        e.set(f"{{{xmi_uri}}}type", f"uml:{type(el).__name__}")
        e.set(f"{{{xmi_uri}}}id", ids.ident(el))
        for name, d in type(el)._props.items():
            v = el._vals.get(name)
            if v is None:
                continue
            if d.derived or d.union or d.readonly:
                continue
            items = v if isinstance(v, (list, tuple)) else (v,)
            if not items:
                continue
            kind = _feat_kind(d)
            if kind == "composite":
                for it in items:
                    if isinstance(it, U.Element) \
                            and getattr(it, "_external_href", None):
                        c = etree.SubElement(e, name)
                        c.set("href", it._external_href)
                        continue
                    # pass the containment opposite down: EMF never
                    # serializes it on the child (Property.datatype,
                    # EnumerationLiteral.enumeration, ...) - it is wired
                    # into _vals by _hook_add but derivable from the tree
                    build(it, e, name, owner=el, opp_name=d.opp)
            elif kind == "text":
                omit_default = (name == "value"
                                and isinstance(el, U.LiteralUnlimitedNatural))
                # P10: name/visibility/body and literal values as attributes
                use_attr = p10 and (
                    name in ("name", "visibility", "body")
                    or (name == "value" and isinstance(
                        el, (U.LiteralInteger, U.LiteralUnlimitedNatural,
                             U.LiteralString))))
                for it in items:
                    txt = _text(it)
                    if omit_default and txt == "0":
                        continue  # EMF default: no child
                    if use_attr:
                        e.set(name, txt)
                    else:
                        c = etree.SubElement(e, name)
                        c.text = txt
            else:
                if name == opp_name and any(it is owner for it in items):
                    continue  # containment opposite: derivable, not emitted
                for it in items:
                    # P10: single-valued references as attributes (the
                    # cross-file href form stays a child element)
                    if p10 and not d.multi \
                            and not getattr(it, "_external_href", None):
                        e.set(name, ids.ident(it))
                    else:
                        ref_child(e, name, it)
        return e

    built_roots = [build(r, root, f"{{{uml_ns}}}{type(r).__name__}")
                   for r in roots]

    # profile applications recorded on the first root (one per applied
    # profile href; the reader flattens the corpus form)
    if profile_applications and built_roots:
        for h in profile_applications:
            pa = etree.SubElement(built_roots[0], "profileApplication")
            pa.set(f"{{{xmi_uri}}}type", "uml:ProfileApplication")
            ap = etree.SubElement(pa, "appliedProfile")
            ap.set("href", h)

    return etree.tostring(root, xml_declaration=True, encoding="UTF-8",
                          pretty_print=True)