#!/usr/bin/env python
"""Clean-room SysML v1 -> SysML v2 textual-notation emitter.

Mapping authority: OMG "Systems Modeling Language (SysML) v2.0 Beta 4,
Part 2: SysML v1 to SysML v2 Transformation" (ptc/2025-04-07), normative
statements extracted from the published document, e.g.:

  - "A SysML::Blocks::Block is mapped to a SysML v2 PartDefinition."
  - "A SysML::Blocks::ValueType is mapped to a SysML v2 AttributeDefinition."
  - "A SysML::ConstraintBlocks::ConstraintBlock is mapped to a SysML v2
     ConstraintDefinition."
  - "A SysML::Requirement is mapped to a SysML v2 RequirementUsage."
  - "A SysML::Requirements::Satisfy relationship is mapped to a SysML v2
     SatisfyRequirementUsage."
  - "A SysML::Blocks::BindingConnector is mapped to a SysML v2
     BindingConnectorAsUsage."                     (not yet emitted here)
  - "A UML4SysML::Enumeration is mapped to a SysML v2 EnumerationDefinition."
  - "A UML4SysML::EnumerationLiteral is mapped to a SysML v2 EnumerationUsage."
  - "A UML4SysML::Generalization relationship is mapped to a SysML v2
     Subclassification."
  - "A UML4SysML::Comment is mapped to a SysML v2 Comment."
  - "A UML4SysML::Property which is typed by a block is mapped to a PartUsage.
     The derived property Property::isComposite is directly mapped to
     PartUsage::isComposite."
  - "A UML4SysML::Property is mapped to a SysML v2 AttributeUsage" (typed by
    DataType / ValueType), and "a UML4SysML::Property ... without a type" to
    a Feature.

Honesty rule: elements with no normative mapping handled here raise
UnmappedFeature naming the v1 metaclass, rather than guessing.

Operates on models built with the generated metaclasses (gen.uml25) and
stereotypes (gen.sysml); stereotype application is the fold-in itself
(a Block IS a Class carrying Block's tagged values).
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import gen.uml25 as U
import gen.sysml as S


class UnmappedFeature(Exception):
    """A v1 element whose normative v2 mapping is not implemented here."""


def _name(el):
    n = getattr(el, "name", None)
    return n if isinstance(n, str) and n else None


def _mult(prop) -> str:
    """Multiplicity text from lowerValue/upperValue literal values."""
    lo = hi = None
    lv = prop._vals.get("lowerValue")
    uv = prop._vals.get("upperValue")
    if isinstance(lv, U._Element) and lv._vals.get("value") is not None:
        lo = lv._vals.get("value")
    if isinstance(uv, U._Element):
        v = uv._vals.get("value")
        if isinstance(v, U.UnlimitedNatural):
            hi = "*" if v.unbounded else v.n
        elif v is not None:
            hi = v
    lo = 1 if lo is None else int(lo)
    if hi is None:
        return "" if lo == 1 else f"[{lo}..1]"
    if hi == "*":
        return "[*]" if lo == 0 else f"[{lo}..*]"
    hi = int(hi)
    if lo == hi == 1:
        return ""
    if lo == 0 and hi == 1:
        return "[0..1]"
    return f"[{lo}..{hi}]" if lo != hi else f"[{hi}]"


def _doc_lines(el):
    comments = el._vals.get("ownedComment") or []
    return [" ".join(c._vals.get("body", "").split()) for c in comments
            if c._vals.get("body")]


def _is_block(t):
    return isinstance(t, S.Block)


def emit_v2(pkg, indent=0) -> str:
    """Emit SysML v2 textual notation for a v1 Package (and contents)."""
    pad = "  " * indent
    name = _name(pkg) or "Package"
    lines = [f"{pad}package {name} {{"]
    for el in list(pkg.ownedMember):
        lines += emit_element(el, indent + 1)
    lines.append(pad + "}")
    return "\n".join(lines)


def emit_element(el, indent) -> list[str]:
    pad = "  " * indent
    out = []

    # ---- requirements come first so satisfy can reference them -------------
    if isinstance(el, S.Requirement):
        nm = _name(el) or "?"
        docs = []
        txt = el._vals.get("text")
        if isinstance(txt, str) and txt:
            docs.append(txt)          # normative: Requirement.text -> doc
        docs += [d for d in _doc_lines(el)]
        rid = el._vals.get("id")
        out.append(f"{pad}requirement {nm} {{")
        for d in docs:
            out.append(f"{pad}  doc /* {d} */")
        if rid:
            out.append(f"{pad}  /* v1 id: {rid} */")
        out.append(pad + "}")
        return out

    if isinstance(el, U.Package):
        return [emit_v2(el, indent)]

    if isinstance(el, U.Enumeration):
        nm = _name(el) or "?"
        lits = [l for l in el.ownedLiteral]
        out.append(f"{pad}enum def {nm} {{")
        for l in lits:
            out.append(f"{pad}  {(_name(l) or 'lit')};")
        out.append(pad + "}")
        return out

    if isinstance(el, U.Comment):
        for d in _doc_lines(el):
            out.append(f"{pad}doc /* {d} */")
        return out

    if isinstance(el, S.Satisfy):
        return emit_satisfy(el, pad)

    if isinstance(el, U.Class):
        return emit_class_like(el, indent)

    if isinstance(el, U.DataType):
        nm = _name(el) or "?"
        if isinstance(el, S.ValueType):
            out.append(f"{pad}attribute def {nm};")
        elif isinstance(el, S.ConstraintBlock):
            out.append(f"{pad}constraint def {nm};")
        else:
            raise UnmappedFeature(f"DataType {_name(el)!r} (no stereotype)")
        return out

    raise UnmappedFeature(f"{type(el).__name__} {_name(el)!r}")


def emit_class_like(cls, indent) -> list[str]:
    pad = "  " * indent
    nm = _name(cls) or "?"
    if isinstance(cls, S.Block):
        head = f"{pad}part def {nm}"
    elif isinstance(cls, S.Requirement):
        head = f"{pad}requirement {nm}"
    elif isinstance(cls, S.ConstraintBlock):
        head = f"{pad}constraint def {nm}"
    elif isinstance(cls, U.Class):
        raise UnmappedFeature(f"Class {nm!r} without SysML v1 stereotype")
    else:
        raise UnmappedFeature(type(cls).__name__)

    supers = []
    for g in list(cls.generalization):
        t = g._vals.get("general")
        tn = _name(t)
        if tn is None:
            raise UnmappedFeature(f"generalization to unnamed {type(t).__name__}")
        supers.append(tn)

    docs = _doc_lines(cls)
    has_body = bool(list(cls.ownedAttribute)) or bool(list(cls.nestedClassifier)) \
        or docs
    suffix = f" :> {', '.join(supers)}" if supers else ""
    if not has_body:
        return [f"{head}{suffix};"]
    body = [f"{head}{suffix} {{"]
    for d in docs:
        body.append(f"{pad}  doc /* {d} */")
    for attr in list(cls.ownedAttribute):
        body += emit_property(attr, indent + 1)
    for nested in list(cls.nestedClassifier):
        body += emit_element(nested, indent + 1)
    body.append(pad + "}")
    return body


def emit_property(prop, indent) -> list[str]:
    pad = "  " * indent
    nm = _name(prop) or "?"
    t = prop._vals.get("type")
    composite = prop._vals.get("aggregation") is U.AggregationKind.composite
    mult = _mult(prop)

    if isinstance(prop, S.FlowProperty):
        raise UnmappedFeature("FlowProperty (flow attributes not yet emitted)")
    if t is None:
        # normative: "maps properties without a type" -> Feature
        return [f"{pad}feature {nm};"]
    tn = _name(t)
    if tn is None:
        raise UnmappedFeature(f"Property {nm!r} typed by unnamed element")
    if _is_block(t):
        # normative: Property typed by block -> PartUsage; isComposite direct
        kind = "part" if composite else "ref part"
        return [f"{pad}{kind} {nm}{mult} : {tn};"]
    if isinstance(t, U.DataType):  # ValueType / DataType -> AttributeUsage
        return [f"{pad}attribute {nm}{mult} : {tn};"]
    if isinstance(t, U.Enumeration):
        return [f"{pad}attribute {nm}{mult} : {tn};"]
    raise UnmappedFeature(f"Property {nm!r} typed by {type(t).__name__} {tn!r}")


def emit_satisfy(sat, pad) -> list[str]:
    client = [_name(c) for c in list(sat.client)]
    supplier = [_name(s) for s in list(sat.supplier)]
    if not supplier or not client:
        raise UnmappedFeature("Satisfy without client/supplier names")
    # normative: Satisfy -> SatisfyRequirementUsage; v1 client satisfies
    # v1 supplier requirement -> v2 'satisfy <name> : <req> by <part>'
    return [f"{pad}satisfy {(_name(sat) or 'satisfy')} : "
            f"{', '.join(supplier)} by {', '.join(client)};"]


def validate_with_sysmlpy(text: str) -> dict:
    """Parse emitted v2 text with sysmlpy (authoritative v2 reader)."""
    import sys
    from io import StringIO

    sys.path.insert(0, str(Path.home() / "sysmlpy" / "src"))
    from sysmlpy import load  # noqa: E402

    with tempfile.NamedTemporaryFile("w", suffix=".sysml", delete=False) as fp:
        fp.write(text)
        path = fp.name
    try:
        with open(path) as fh:
            return load(fh).count()
    finally:
        Path(path).unlink(missing_ok=True)