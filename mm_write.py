#!/usr/bin/env python
"""CMOF writer (MOF 2.0 XMI) - the metamodel-writing half of the exporter.

Reconstructs the OMG BPMN20.cmof dialect from the generated module
(gen/bpmn.py) plus its `_SYNTH` serialization table (see generate_bpmn.py
and REPORT.md Part 11). Dialect conventions (probes P5/P8, BPMN20.cmof):

  - root <xmi:XMI> with the cmof namespace
    (http://schema.omg.org/spec/MOF/2.0/cmof.xml); one cmof:Package
    (xmi:id "_0", name/uri attributes) plus cmof:Tag elements;
  - all members flattened as ownedMember children (cmof:Class /
    cmof:Enumeration / cmof:Association); member order is not semantic
    (MOF ownedMember is a set) and is writer-determined;
  - classes: name attribute (= xmi:id), space-separated superClass
    attribute (the C3-verified base order equals the file's), isAbstract
    when true; per-class ownedAttribute children in declaration order;
  - properties: primitive/DOM/external types as <type> children carrying
    the verbatim href; class/enum types as `type="<id>"` attributes;
    `association` attribute exactly on the class-owned memberEnd ends;
    lower/upper/visibility/isOrdered/default mirrored from _SYNTH
    (absence of lower with upper='*' is meaningful: two spellings of
    0..* occur in the file and are preserved);
  - enumerations: ownedLiteral children with classifier/enumeration
    attributes naming the owning enumeration;
  - associations: visibility="private" always, memberEnd attribute
    verbatim from _ASSOCIATIONS, ownedEnd children for association-owned
    ends (xmi:id "<assoc>-<end name>", owningAssociation/association
    attributes) - including the ends whose class-side property was
    synthesized by the generator (those class attributes are absent from
    the file and are skipped);
  - ids follow the file's conventions (class/enum/association id ==
    name, property id "<owner>-<name>"); canon ignores them, but
    memberEnd/type/element attribute values are compared verbatim.

Standard library except lxml (writers use lxml).
"""
from __future__ import annotations

import enum as _enum

from lxml import etree

XMI = "http://schema.omg.org/spec/XMI/2.1"
CMOF = "http://schema.omg.org/spec/MOF/2.0/cmof.xml"


class _Prims:
    """Runtime types -> (href frag, cmof xmi:type) for CMOF primitives."""

    @staticmethod
    def of(t):
        return {
            str: ("String", "cmof:PrimitiveType"),
            bool: ("Boolean", "cmof:PrimitiveType"),
            int: ("Integer", "cmof:PrimitiveType"),
        }.get(t)


def _enums(module):
    """(name, EnumClass) for the module's CMOF enumerations, in
    definition order (the generator emits them sorted)."""
    import sys
    return [(name, obj) for name, obj in vars(module).items()
            if isinstance(obj, type) and issubclass(obj, _enum.Enum)
            and obj.__module__ == module.__name__]


def _class_name(module, b):
    return b.__name__


def write_cmof(module) -> bytes:
    """Serialize the generated BPMN metamodel as CMOF XMI bytes.

    `module` is gen.bpmn (or an equivalent generated CMOF module) carrying
    _CLASSES, _ASSOCIATIONS and the _SYNTH table."""
    synth = getattr(module, "_SYNTH", None)
    if synth is None:
        raise ValueError(f"{module.__name__} carries no _SYNTH table")
    ends = synth["ends"]
    props = synth["props"]
    hrefs = synth["hrefs"]
    synth_attrs = synth.get("synth_attrs", {})
    member_refs = {ref for pair in module._ASSOCIATIONS.values()
                   for ref in pair}
    x = f"{{{XMI}}}"

    root = etree.Element(f"{x}XMI", nsmap={"xmi": XMI, "cmof": CMOF})
    pkg = etree.SubElement(root, f"{{{CMOF}}}Package")
    pkg.set(f"{x}id", "_0")
    pkg.set("name", synth["package"]["name"])
    pkg.set("uri", synth["package"]["uri"])

    # ---- enumerations and classes ----------------------------------------
    def _emit_type(parent, t, hrefs, x):
        """Type serialization: href child for primitives/DOM/external,
        type="<metaclass id>" attribute for class- and enum-typed."""
        if t is None:
            return
        if isinstance(t, type):          # prim kinds (str/bool/int)
            frag, kind = _Prims.of(t)
            ty = etree.SubElement(parent, "type")
            ty.set(f"{x}type", kind)
            ty.set("href", hrefs[frag])
        elif t == "xml.dom.Element":     # MOF Element (DOM) by href
            ty = etree.SubElement(parent, "type")
            ty.set(f"{x}type", "cmof:Class")
            ty.set("href", hrefs["Element"])
        elif t in hrefs:                 # external package-qualified type
            ty = etree.SubElement(parent, "type")
            ty.set(f"{x}type", "cmof:Class")
            ty.set("href", hrefs[t])
        else:                            # internal class / enumeration id
            parent.set("type", t)

    for name, en in _enums(module):
        om = etree.SubElement(pkg, "ownedMember")
        om.set(f"{x}type", "cmof:Enumeration")
        om.set(f"{x}id", name)
        om.set("name", name)
        for m in en:                     # definition order
            lit = etree.SubElement(om, "ownedLiteral")
            lit.set(f"{x}type", "cmof:EnumerationLiteral")
            lit.set(f"{x}id", f"{name}-{m.value}")
            lit.set("name", m.value)
            lit.set("classifier", name)
            lit.set("enumeration", name)

    for cls in module._CLASSES:
        cname = cls.__name__
        om = etree.SubElement(pkg, "ownedMember")
        om.set(f"{x}type", "cmof:Class")
        om.set(f"{x}id", cname)
        om.set("name", cname)
        supers = [b.__name__ for b in cls.__bases__
                  if b.__name__ != "_MOFBase"]
        if supers:
            om.set("superClass", " ".join(supers))
        if cls._ABSTRACT:
            om.set("isAbstract", "true")
        for aname, d in cls.__dict__.get("_DECL", {}).items():
            pid = f"{cname}-{aname}"          # xmi:id convention
            dotkey = f"{cname}.{aname}"       # _SYNTH key convention
            if dotkey in synth_attrs:
                continue  # generator-synthesized back-ref; the file
                          # serializes this end as association-owned
            a = etree.SubElement(om, "ownedAttribute")
            a.set(f"{x}type", "cmof:Property")
            a.set(f"{x}id", pid)
            a.set("name", aname)
            lraw, uraw, vis, ordered, default = props[dotkey]
            if vis:
                a.set("visibility", vis)
            if lraw is not None:
                a.set("lower", lraw)
            if uraw is not None:
                a.set("upper", uraw)
            if d.composite:
                a.set("isComposite", "true")
            if d.derived:
                a.set("isDerived", "true")
            if ordered:
                a.set("isOrdered", ordered)
            if pid in member_refs:
                a.set("association", d.assoc)
            if default is not None:
                a.set("default", default)
            _emit_type(a, d.t, hrefs, x)

    # ---- associations ------------------------------------------------------
    for an, refs in module._ASSOCIATIONS.items():
        om = etree.SubElement(pkg, "ownedMember")
        om.set(f"{x}type", "cmof:Association")
        om.set(f"{x}id", an)
        om.set("name", an)
        om.set("visibility", "private")
        om.set("memberEnd", " ".join(refs))
        e = ends.get(an)
        if e is not None:
            ename, etype, lraw, uraw, evis, ederived = e
            end = etree.SubElement(om, "ownedEnd")
            end.set(f"{x}type", "cmof:Property")
            end.set(f"{x}id", f"{an}-{ename}")
            end.set("name", ename)
            end.set("type", etype)
            if lraw is not None:
                end.set("lower", lraw)
            if uraw is not None:
                end.set("upper", uraw)
            if evis:
                end.set("visibility", evis)
            if ederived:
                end.set("isDerived", "true")
            end.set("owningAssociation", an)
            end.set("association", an)

    # ---- tags ---------------------------------------------------------------
    for i, (tname, tvalue, telement) in enumerate(synth["tags"], 1):
        tg = etree.SubElement(root, f"{{{CMOF}}}Tag")
        tg.set(f"{x}id", f"_{i}")
        tg.set("name", tname)
        tg.set("value", tvalue)
        tg.set("element", telement)

    return etree.tostring(root, xml_declaration=True, encoding="UTF-8",
                          pretty_print=True)