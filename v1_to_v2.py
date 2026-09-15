#!/usr/bin/env python
"""Clean-room SysML v1 -> SysML v2 textual-notation emitter.

Mapping authority: OMG "SysML v2.0 Beta 4, Part 2: SysML v1 to SysML v2
Transformation" (ptc/2025-04-07). Normative statements implemented here,
each anchored to the published document:

  Block->PartDefinition (7.8.4.3.3), Property typed by block->PartUsage
  w/ isComposite direct (7.8.4.3.13), Property untyped->Feature,
  ValueType->AttributeDefinition (7.8.4.3.14), Enumeration->Enumeration-
  Definition, EnumerationLiteral->EnumerationUsage, ConstraintBlock->
  ConstraintDefinition (7.8.5.3.1), Association/AssociationBlock->
  ConnectionDefinition (7.7.12.2.x / 7.8.4.3.x), Connector->ConnectionUsage
  (7.7.12.2.14), BindingConnector->BindingConnectorAsUsage (7.8.4.3.2),
  InterfaceBlock->PortDefinition (7.8.7.3.16), Port typed by InterfaceBlock->
  PortUsage (7.7.12.2.36), untyped Port->PortUsage (7.7.12.2.37),
  Property typed by Class/Interface->OccurrenceUsage (7.7.4.2.37),
  plain Class->OccurrenceDefinition, Actor->PartDefinition (7.7.13.3.1),
  Signal->ItemDefinition, InformationItem->ItemDefinition (7.7.7.3.x),
  Activity->ActionDefinition (7.7.3.3.1), OpaqueBehavior->ActionDefinition,
  Operation->PerformActionUsage (7.7.4.2.23), Parameter->ReferenceUsage
  w/ direction (7.7.4.2.24; return -> out per the Activity textual example),
  StateMachine->StateDefinition (7.7.11.2.16), State->StateUsage
  (7.7.11.2.15), Pseudostate->StateUsage (7.7.11.2.13), FinalState->
  StateUsage (7.7.11.2.8), InitialState elided per SYSML2_-203
  (7.7.11.2.10), Transition->TransitionUsage (7.7.11.2.18), Region
  inlined (7.7.11.2.12), Requirement->RequirementUsage (7.8.8.3.30)
  with id per the DeriveReqt textual example, Satisfy->
  SatisfyRequirementUsage (7.8.8.3.44), Verify->RequirementVerification-
  Membership (7.8.8.3.49, emitted inside the TestCase objective),
  TestCase->VerificationCaseDefinition (7.8.8.3.26) with
  'return verdict : VerificationCases::VerdictKind' (VerdictKind rule),
  DeriveReqt->DerivationConnections::Derivation connection (7.8.8.3.15),
  Refine/Trace->Dependency annotated with v1-library metadata
  (7.8.8.3.35 / 7.8.8.3.51; local RefineData/TraceData metadata stubs
  stand in for SysMLv1Library), Allocate->AllocationDefinition /
  AllocationUsage (7.8.3.3.9 / 7.8.3.3.10), PackageImport->
  NamespaceImport (7.7.9.3.12; elided because the target grammar reader
  has no import), ElementImport->MembershipImport (elided, same reason),
  Dependency/Realization/Abstraction->Dependency (7.7.6.2.9 / 7.7.14.x),
  UseCase->UseCaseDefinition (7.7.13.3.3), Include->IncludeUseCaseUsage
  (7.7.13.3.2), Comment->Comment,
  FullPort->PartUsage annotated with PortData metadata (7.8.7.3.7
  / 7.8.7.3.15; local SysMLv1Library::PortData metadata stub),
  ProxyPort -> base Port mapping + explicit not-mapped comment
  (Table 30 lists no target; SYSML2_-329), FlowProperty -> directed
  Attribute/Occurrence/ReferenceUsage (7.8.7.3.4-.6, flagged SYSML2_-76
  but specified), ConstraintBlock internals: parameters as
  'in attribute' + ownedRule Constraint as a nested ConstraintUsage
  w/ language/body (7.8.5.2.1), Property defaultValue ->
  FeatureValue '= <expr>' incl. InstanceValue -> feature reference
  (7.7.4.2.16), InstanceSpecification -> PartUsage / link
  ConnectionUsage with slots as 'redefines p = v;' (7.7.4.2.14/.13),
  InterfaceBlock-typed Property -> OccurrenceUsage
  (7.7.4.2.37 PropertyTypedByClassInterface), Interaction ->
  Interaction (7.7.8.3.6) elided (the target grammar reader has no
  interaction element; Lifeline -> PartUsage 7.7.8.3.13, Message ->
  Flow 7.7.8.3.15 noted in the elision), CombinedFragment ->
  Interaction (7.7.8.3.3), InteractionOperand -> Interaction
  (7.7.8.3.7), InteractionUse -> Step (7.7.8.3.9), StateInvariant ->
  Invariant (7.7.8.3.17) elided for the same grammar gap,
  ActionExecutionSpecification -> ActionUsage (7.7.8.3.1),
  Table-11 not-mapped interaction elements as explicit comments
  (7.7.8.2),

Honesty rule: elements with no normative mapping handled here raise
UnmappedFeature naming the v1 metaclass, rather than guessing.

Operates on models built with the generated metaclasses (gen.uml25) and
stereotypes (gen.sysml); stereotype application is the fold-in itself
(a Block IS a Class carrying Block's tagged values).

Textual forms are calibrated against sysmlpy (the authoritative v2
reader) - see calibrate_v2.py; the emitter only produces text that
sysmlpy parses.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import gen.uml25 as U
import gen.sysml as S


class UnmappedFeature(Exception):
    """A v1 element whose normative v2 mapping is not implemented here."""


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _name(el):
    n = getattr(el, "name", None)
    return n if isinstance(n, str) and n else None


def _mult(prop) -> str:
    """Multiplicity text from lowerValue/upperValue literal values."""
    lo = hi = None
    lv = prop._vals.get("lowerValue")
    uv = prop._vals.get("upperValue")
    if isinstance(lv, U._Element) and lv._vals.get("value") is not None:
        v = lv._vals.get("value")
        lo = v.n if isinstance(v, U.UnlimitedNatural) else v
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


def _is_stereo_class(t) -> bool:
    """True if t carries a SysML v1 stereotype (a gen.sysml subclass)."""
    return isinstance(t, (S.Block, S.ValueType, S.ConstraintBlock,
                          S.Requirement, S.TestCase, S.InterfaceBlock))


def _params(params, pad) -> list[str]:
    """UML Parameters -> v2 in/out/inout parameter lines (return -> out,
    per the Activity_Mapping textual example 'out parReturn')."""
    out = []
    for p in params:
        d = p._vals.get("direction")
        kw = "in"
        if d is U.ParameterDirectionKind.out:
            kw = "out"
        elif d is U.ParameterDirectionKind.inout:
            kw = "inout"
        elif d is U.ParameterDirectionKind.return_:
            kw = "out"
        t = p._vals.get("type")
        tn = _name(t)
        line = f"{pad}  {kw} {_name(p) or 'p'}" + (f" : {tn}" if tn else "") + ";"
        out.append(line)
    return out


def _docs_as(pad, el) -> list[str]:
    return [f"{pad}doc /* {d} */" for d in _doc_lines(el)]


def _flow_dir(fp) -> str:
    """FlowProperty direction tag -> 'in '/'out '/'inout ' prefix (or '').
    The tag value is a FlowDirectionKind member (Python Enum, name 'in_'
    for 'in') or an EnumerationLiteral or a raw string."""
    d = fp._vals.get("direction")
    nm = getattr(d, "name", None)
    if isinstance(nm, str):
        nm = nm.rstrip("_")
    if nm in ("in", "out", "inout"):
        return nm + " "
    return ""


def _value_text(v):
    """Format a ValueSpecification as an inline v2 expression; None when
    it has no inline textual form (caller elides honestly)."""
    if isinstance(v, U.LiteralString):
        b = v._vals.get("value") or v._vals.get("body") or ""
        return '"' + str(b).replace('"', '\\"') + '"'
    if isinstance(v, (U.LiteralInteger, U.LiteralUnlimitedNatural,
                      U.LiteralReal, U.LiteralBoolean)):
        x = v._vals.get("value")
        if isinstance(v, U.LiteralBoolean):
            return "true" if x in (True, "true", "1") else "false"
        if x is None:
            return None
        return str(x.n) if isinstance(x, U.UnlimitedNatural) else str(x)
    if isinstance(v, U.InstanceValue):      # 7.7.4.2.16 -> feature ref
        ins = v._vals.get("instance")
        return _name(ins)
    return None


def _default_suffix(prop) -> str:
    """Property::defaultValue -> ' = <expr>' (FeatureValue; gold example:
    'part p : T = sysMLv1InstanceSpecification;', 7.7.4.2.16)."""
    d = prop._vals.get("defaultValue")
    if d is None:
        return ""
    v = _value_text(d)
    if v is None:
        raise UnmappedFeature(
            f"Property {_name(prop)!r} default of {type(d).__name__}")
    return f" = {v}"


def _constraint_expr(r, pad) -> list[str]:
    """v1 Constraint owned by a ConstraintBlock -> nested ConstraintUsage
    with language + body comment (7.8.5.2.1 gold: 'constraint
    constraintExpression { language "OCL2.0" /* c == a + b */ }')."""
    nm = _v2name(_name(r) or "constraintExpression")
    spec = r._vals.get("specification")
    inner = []
    if isinstance(spec, U.OpaqueExpression):
        langs = [l for l in list(spec._vals.get("language") or [])
                 if isinstance(l, str) and l]
        if langs:
            inner.append(f'language "{langs[0]}"')
        body = spec._vals.get("body")
        body = body if isinstance(body, (list, tuple)) else [body]
        for b in body:
            if isinstance(b, str) and b.strip():
                inner.append("/* " + " ".join(b.split()) + " */")
    else:
        b = getattr(spec, "body", None)
        if isinstance(b, str) and b.strip():
            inner.append("/* " + " ".join(b.split()) + " */")
    if not inner:
        raise UnmappedFeature(
            f"Constraint {nm!r} without an OpaqueExpression specification")
    out = [f"{pad}constraint {nm} {{"] + [f"{pad}  {x}" for x in inner]
    out.append(pad + "}")
    return out


def _scan_fullports(pkg) -> bool:
    """True if any Port under pkg carries the FullPort stereotype (the
    package then needs the local SysMLv1Library::PortData stub)."""
    for el in list(pkg.ownedMember):
        if isinstance(el, (U.Class, U.DataType, U.Interface)):
            for attr in list(getattr(el, "ownedAttribute", ())):
                if isinstance(attr, U.Port) and isinstance(attr, S.FullPort):
                    return True
        if isinstance(el, U.Package) and _scan_fullports(el):
            return True
    return False


# --------------------------------------------------------------------------
# package / element dispatch
# --------------------------------------------------------------------------

def emit_v2(pkg, indent=0) -> str:
    """Emit SysML v2 textual notation for a v1 Package (and contents)."""
    pad = "  " * indent
    name = _v2name(_name(pkg) or "Package")
    lines = [f"{pad}package {name} {{"]
    for profile, stereo, _ in getattr(pkg, "_applied_stereotypes", None) or []:
        lines.append(f"{pad}  /* v1 stereotype applied: {profile}::{stereo} */")
    if _scan_fullports(pkg):                 # SysMLv1Library::PortData stub
        lines.append(f"{pad}  metadata def PortData {{ attribute isFullPort : Boolean; }}")
    # v1 imports -> target grammar reader has none: honest elision comments
    for pi in list(pkg.packageImport):
        ip = pi._vals.get("importedPackage")
        lines.append(f"{pad}  /* v1 packageImport of {_name(ip)!r} elided: "
                     "target grammar reader has no import */")
    # Verify relationships are consumed by their TestCase's emission
    verify_rels = _collect_verifies(pkg)
    for el in list(pkg.ownedMember):
        if isinstance(el, S.Verify):
            continue  # emitted inside the TestCase's objective
        lines += emit_element(el, indent + 1, verify_rels)
    if len(lines) == 1:
        return f"{pad}package {name};"
    lines.append(pad + "}")
    return "\n".join(lines)


def _collect_verifies(pkg) -> list:
    return [el for el in list(pkg.ownedMember) if isinstance(el, S.Verify)]


def emit_interaction(ix, pad) -> list[str]:
    """Interaction -> Interaction (normative 7.7.8.3.6) - but the target
    grammar reader has no interaction element, so the normative result is
    elided with a member inventory (Lifeline -> PartUsage 7.7.8.3.13,
    Message -> Flow 7.7.8.3.15)."""
    ls = [m for m in list(ix.ownedMember) if isinstance(m, U.Lifeline)]
    ms = [m for m in list(ix.ownedMember) if isinstance(m, U.Message)]
    nm = _name(ix) or "?"
    return [f"{pad}/* v1 Interaction {nm!r} elided: Interaction -> Interaction "
            f"(7.7.8.3.6; {len(ls)} Lifeline -> PartUsage, {len(ms)} Message -> "
            "Flow) but the target grammar reader has no interaction element */"]


def emit_instancespec(ins, pad) -> list[str]:
    """InstanceSpecification -> PartUsage (7.7.4.2.14; gold 'part inst :
    B { redefines p = "Hello"; }') or, when a classifier is an
    Association (a link), ConnectionUsage (7.7.4.2.13; gold 'connection
    l : Assoc connect a to b;')."""
    classifiers = list(ins.classifier)
    assocs = [c for c in classifiers if isinstance(c, U.Association)]
    nm = _v2name(_name(ins) or "?")
    slots = list(ins.slot)
    if assocs:
        roles = []
        for sl in slots:
            for v in list(sl._vals.get("value") or []):
                if isinstance(v, U.InstanceValue):
                    rn = _name(v._vals.get("instance"))
                else:
                    rn = _value_text(v)
                if not rn:
                    raise UnmappedFeature(
                        f"link InstanceSpecification {nm!r} slot value without "
                        "a referenceable name")
                roles.append(rn)
        if len(roles) != 2:
            raise UnmappedFeature(
                f"link InstanceSpecification {nm!r} with {len(roles)} roles")
        an = _name(assocs[0])
        head = f"{pad}connection {nm}"
        if an:
            head += f" : {an}"
        return [head + f" connect {roles[0]} to {roles[1]};"]
    # not a link -> PartUsage, typed by the classifier(s)
    tns = [_name(c) for c in classifiers if _name(c)]
    typing = f" : {', '.join(tns)}" if tns else ""
    if not slots:
        return [f"{pad}part {nm}{typing};"]
    out = [f"{pad}part {nm}{typing} {{"]
    out += _slot_lines(slots, pad + "  ")
    out.append(pad + "}")
    return out


def _slot_lines(slots, pad) -> list[str]:
    """Slots -> 'redefines <definingFeature> = <value>;' (7.7.4.2.14
    gold: 'redefines sysMLv1ValueProperty = "Hello InstanceSpecification";')."""
    out = []
    for sl in slots:
        feat = sl._vals.get("definingFeature")
        fn = _name(feat)
        if fn is None:
            raise UnmappedFeature("Slot without a named definingFeature")
        values = [v for v in list(sl._vals.get("value") or [])]
        if not values:
            out.append(f"{pad}redefines {_v2name(fn)};")
            continue
        for v in values:
            if isinstance(v, U.InstanceValue):
                txt = _name(v._vals.get("instance"))
            else:
                txt = _value_text(v)
            if txt is None:
                raise UnmappedFeature(
                    f"Slot {fn!r} value of {type(v).__name__}")
            out.append(f"{pad}redefines {_v2name(fn)} = {txt};")
    return out


def emit_element(el, indent, verify_rels=()) -> list[str]:
    pad = "  " * indent
    out = []

    # ---- relationships -----------------------------------------------------
    if isinstance(el, S.Satisfy):
        return emit_satisfy(el, pad)
    if isinstance(el, S.DeriveReqt):
        return emit_derive_reqt(el, pad)
    if isinstance(el, S.Verify):
        return [f"{pad}/* v1 Verify relationship emitted inside its "
                "TestCase objective */"]
    if isinstance(el, (S.Refine, S.Trace)):
        return emit_dependency(el, pad, annotated=True)
    if isinstance(el, S.Allocate):
        return emit_allocate(el, pad)
    if isinstance(el, (U.Abstraction, U.Dependency)):  # incl. Realization
        return emit_dependency(el, pad, annotated=False)
    if isinstance(el, (U.PackageImport, U.ElementImport)):
        return []  # handled at package level

    # ---- classifiers -------------------------------------------------------
    if isinstance(el, S.Requirement):
        return emit_requirement(el, pad)
    if isinstance(el, U.Package):
        return [emit_v2(el, indent)]
    if isinstance(el, U.Enumeration):
        return emit_enumeration(el, pad)
    if isinstance(el, U.Association):        # includes AssociationClass
        return emit_association(el, pad)
    if isinstance(el, S.InterfaceBlock):
        return [f"{pad}port def {_name(el) or '?'};"] + _docs_as(pad + "  ", el)
    if isinstance(el, (U.Signal, U.InformationItem)):
        return [f"{pad}item def {_name(el) or '?'};"] + _docs_as(pad + "  ", el)
    if isinstance(el, U.Actor):
        return [f"{pad}part def {_name(el) or '?'};"] + _docs_as(pad + "  ", el)
    if isinstance(el, S.TestCase):
        return emit_testcase(el, pad, verify_rels)
    if isinstance(el, U.StateMachine):
        return emit_statemachine(el, indent)
    if isinstance(el, (U.Activity, U.OpaqueBehavior)):
        return emit_action_def(el, indent)
    if isinstance(el, U.UseCase):
        return emit_usecase(el, indent)
    if isinstance(el, U.Comment):
        return _docs_as(pad, el)
    if isinstance(el, U.InstanceSpecification):
        return emit_instancespec(el, pad)
    if isinstance(el, U.Interaction):
        return emit_interaction(el, pad)
    if isinstance(el, (U.CombinedFragment, U.InteractionOperand)):
        anchor = "7.7.8.3.3" if isinstance(el, U.CombinedFragment) else "7.7.8.3.7"
        return [f"{pad}/* v1 {type(el).__name__} {_name(el)!r} elided: "
                f"mapped to v2 Interaction ({anchor}) but the target grammar "
                "reader has no interaction element */"]
    if isinstance(el, U.InteractionUse):
        return [f"{pad}/* v1 InteractionUse {_name(el)!r} elided: mapped to "
                "v2 Step (7.7.8.3.9) but the target grammar reader has no "
                "step element */"]
    if isinstance(el, U.StateInvariant):
        return [f"{pad}/* v1 StateInvariant {_name(el)!r} elided: mapped to "
                "v2 Invariant (7.7.8.3.17) but the target grammar reader has "
                "no invariant element */"]
    if isinstance(el, (U.ActionExecutionSpecification,
                       U.BehaviorExecutionSpecification)):
        # normative: -> ActionUsage (7.7.8.3.1 / 7.7.8.3.2)
        nm = _name(el)
        if nm is None:
            return [f"{pad}/* v1 {type(el).__name__} elided: mapped to "
                    "v2 ActionUsage (7.7.8.3.1/.2) but the execution "
                    "specification is unnamed */"]
        return [f"{pad}action {_v2name(nm)};"]
    if isinstance(el, (U.MessageOccurrenceSpecification,
                       U.ExecutionOccurrenceSpecification,
                       U.DestructionOccurrenceSpecification, U.OccurrenceSpecification,
                       U.Gate, U.GeneralOrdering, U.Continuation)):
        # Table 11 (7.7.8.2): not mapped in ptc/2025-04-07
        return [f"{pad}/* v1 {type(el).__name__} {_name(el)!r} not mapped "
                "in ptc/2025-04-07 (7.7.8.2 Table 11) */"]
    if isinstance(el, U.DataType):
        return emit_datatype(el, pad)
    if isinstance(el, U.Class):
        return emit_class_like(el, indent)

    raise UnmappedFeature(f"{type(el).__name__} {_name(el)!r}")


# --------------------------------------------------------------------------
# classifier bodies
# --------------------------------------------------------------------------

def emit_class_like(cls, indent) -> list[str]:
    """Blocks (part def), plain Classes (occurrence def), etc."""
    pad = "  " * indent
    nm = _v2name(_name(cls) or "?")
    if isinstance(cls, S.ConstraintBlock):
        head = f"{pad}constraint def {nm}"   # ConstraintBlock before Block
    elif isinstance(cls, S.Block):
        head = f"{pad}part def {nm}"
    elif isinstance(cls, U.Class):           # plain class -> occurrence def
        head = f"{pad}occurrence def {nm}"
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
        or bool(list(cls.ownedOperation)) or bool(list(cls.ownedConnector)) \
        or docs
    suffix = f" :> {', '.join(supers)}" if supers else ""
    if not has_body:
        return [f"{head}{suffix};"]

    body = [f"{head}{suffix} {{"]
    body += _docs_as(pad + "  ", cls)
    for attr in list(cls.ownedAttribute):
        body += emit_property(attr, indent + 1)
    if isinstance(cls, S.ConstraintBlock):   # normative: ownedRule ->
        for r in list(cls.ownedRule):        # nested ConstraintUsage
            body += _constraint_expr(r, pad + "  ")
    for op in list(cls.ownedOperation):      # normative: Operation ->
        body += emit_perform_action(op, indent + 1)   # PerformActionUsage
    for conn in list(cls.ownedConnector):    # Connector -> ConnectionUsage
        body += _connector_body(conn, pad + "  ")
    for nested in list(cls.nestedClassifier):
        body += emit_element(nested, indent + 1)
    body.append(pad + "}")
    return body


def emit_usecase(uc, indent) -> list[str]:
    pad = "  " * indent
    nm = _name(uc) or "?"
    includes = list(uc._vals.get("include") or []) \
        + [m for m in list(uc.ownedMember) if isinstance(m, U.Include)]
    includes = list(dict.fromkeys(includes))
    if not includes and not _doc_lines(uc):
        return [f"{pad}use case def {nm};"]
    body = [f"{pad}use case def {nm} {{"]
    body += _docs_as(pad + "  ", uc)
    for inc in includes:                     # normative: Include ->
        addition = inc._vals.get("addition")          # IncludeUseCaseUsage
        an = _name(addition)
        if an is None:
            raise UnmappedFeature("Include with unnamed addition")
        body.append(f"{pad}  include use case : {an};")
    body.append(pad + "}")
    return body


def _v2name(n: str) -> str:
    """Quote names that are not valid v2 identifiers (id-derived names
    like 'packagedElement-7' or enumeration literals like 'CTS-B')."""
    import re
    if n and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", n):
        return n
    return f"<'{n}'>"


def _indent_of(pad: str) -> int:
    return len(pad) // 2 if pad else 0


def emit_datatype(el, pad) -> list[str]:
    nm = _v2name(_name(el) or "?")
    docs = _doc_lines(el)
    apps = getattr(el, "_applied_stereotypes", None)
    if isinstance(el, S.ValueType):
        head = f"{pad}attribute def {nm}"
    elif isinstance(el, S.ConstraintBlock):
        head = f"{pad}constraint def {nm}"
    elif isinstance(el, U.DataType):
        head = f"{pad}attribute def {nm}"
    else:
        raise UnmappedFeature(f"DataType {nm!r} (no stereotype)")
    apps = apps or []
    if not docs and not apps and not list(el.ownedAttribute):
        return [head + ";"]
    out = [head + " {"]
    for d in docs:
        out.append(f"{pad}  doc /* {d} */")
    for profile, stereo, _ in apps:
        out.append(f"{pad}  /* v1 stereotype applied: {profile}::{stereo} */")
    for attr in list(el.ownedAttribute):
        out += emit_property(attr, _indent_of(pad) + 1)
    out.append(pad + "}")
    return out


def emit_enumeration(el, pad) -> list[str]:
    nm = _v2name(_name(el) or "?")
    out = [f"{pad}enum def {nm} {{"]
    for l in list(el.ownedLiteral):
        out.append(f"{pad}  {_v2name(_name(l) or 'lit')};")
    out.append(pad + "}")
    return out


def emit_association(assoc, pad) -> list[str]:
    """Association/AssociationBlock -> ConnectionDefinition (normative);
    member ends become connection ends."""
    nm = _v2name(_name(assoc) or "?")
    ends = []
    for e in list(assoc.memberEnd):
        tn = _name(e._vals.get("type"))
        mult = _mult(e)
        en = _name(e)
        end = "end" + (f" {_v2name(en)}" if en else "")
        end += (f" : {tn}" if tn else "") + mult + ";"
        ends.append(end)
    if isinstance(assoc, U.AssociationClass):
        nm += "  /* v1 AssociationClass */"
    if not ends:
        return [f"{pad}connection def {nm};"]
    out = [f"{pad}connection def {nm} {{"]
    for e in ends:
        out.append(f"{pad}  {e}")
    out.append(pad + "}")
    return out


def _connector_body(conn, pad) -> list[str]:
    """Connector -> ConnectionUsage; BindingConnector ->
    BindingConnectorAsUsage. Ends' roles are the connected part names."""
    nm = _name(conn) or "connection"
    roles = []
    for e in list(conn.end):
        r = e._vals.get("role")
        rn = _name(r)
        if rn is None:
            raise UnmappedFeature(f"Connector {_name(conn)!r} end without role")
        roles.append(rn)
    if isinstance(conn, S.BindingConnector):
        return [f"{pad}binding {nm} bind {roles[0]} = {roles[1]};"]
    return [f"{pad}connection {nm} connect {roles[0]} to {roles[1]};"]


def emit_perform_action(op, indent) -> list[str]:
    """Operation -> PerformActionUsage (normative 7.7.4.2.23)."""
    pad = "  " * indent
    nm = _name(op) or "op"
    params = _params(list(op.ownedParameter), pad)
    if not params:
        return [f"{pad}perform action {nm};"]
    out = [f"{pad}perform action {nm} {{"]
    out += params
    out.append(pad + "}")
    return out


def emit_action_def(act, indent) -> list[str]:
    """Activity / OpaqueBehavior -> ActionDefinition."""
    pad = "  " * indent
    nm = _name(act) or "?"
    params = _params(list(act.ownedParameter), pad)
    if not params and not _doc_lines(act):
        return [f"{pad}action def {nm};"]
    out = [f"{pad}action def {nm} {{"]
    out += _docs_as(pad + "  ", act)
    out += params
    out.append(pad + "}")
    return out


# --------------------------------------------------------------------------
# state machines
# --------------------------------------------------------------------------

def emit_statemachine(sm, indent) -> list[str]:
    """StateMachine -> StateDefinition; Region inlined; State/Pseudostate/
    FinalState -> StateUsage; InitialState elided (SYSML2_-203);
    Transition -> TransitionUsage ('first <src> then <tgt>')."""
    pad = "  " * indent
    nm = _name(sm) or "?"
    regions = [m for m in list(sm.ownedMember) if isinstance(m, U.Region)]
    if not regions:
        return [f"{pad}state def {nm};"]
    multi = len(regions) > 1
    out = [f"{pad}state def {nm} {{"]
    if multi:
        out.append(f"{pad}  /* v1 has {len(regions)} regions; "
                   "StateDefinition::isParallel = true */")
    for r in regions:
        if multi:
            out.append(f"{pad}  /* region {_name(r)!r} */")
        for st in list(r.ownedMember):
            if isinstance(st, U.Transition):
                continue
            out += _emit_state_like(st, indent + 1)
        for tr in list(r.ownedMember):
            if isinstance(tr, U.Transition):
                out += _emit_transition(tr, indent + 1)
    out.append(pad + "}")
    return out


def _emit_state_like(st, indent) -> list[str]:
    pad = "  " * indent
    if isinstance(st, U.Pseudostate) and st._vals.get("kind") is U.PseudostateKind.initial:
        # normative: InitialState -> StateUsage, flagged SYSML2_-203
        return [f"{pad}/* v1 initial state elided (SYSML2_-203) */"]
    nm = _name(st) or "state"
    docs = _doc_lines(st)
    inner = [m for m in list(st.ownedMember) if isinstance(m, U.State)]
    if not inner and not docs:
        return [f"{pad}state {nm};"]
    out = [f"{pad}state {nm} {{"]
    out += _docs_as(pad + "  ", st)
    for s in inner:
        out += _emit_state_like(s, indent + 1)
    out.append(pad + "}")
    return out


def _emit_transition(tr, indent) -> list[str]:
    pad = "  " * indent
    nm = _name(tr) or "transition"
    src, tgt = tr._vals.get("source"), tr._vals.get("target")
    sn, tn = _name(src), _name(tgt)
    if sn is None and isinstance(src, U.Pseudostate) \
            and src._vals.get("kind") is U.PseudostateKind.initial:
        return [f"{pad}/* v1 transition from initial state elided "
                "(SYSML2_-203) */"]
    if sn is None or tn is None:
        raise UnmappedFeature(f"Transition {nm!r} without named source/target")
    return [f"{pad}transition {nm} first {sn} then {tn};"]


# --------------------------------------------------------------------------
# requirements & relationships
# --------------------------------------------------------------------------

def emit_requirement(req, pad) -> list[str]:
    nm = _name(req) or "?"
    rid = req._vals.get("id")
    head = f"{pad}requirement " + (f"<'{rid}'> " if rid else "") + nm
    docs = []
    txt = req._vals.get("text")
    if isinstance(txt, str) and txt:
        docs.append(txt)                     # normative: text -> doc
    docs += _doc_lines(req)
    if not docs:
        return [head + ";"]
    out = [head + " {"]
    for d in docs:
        out.append(f"{pad}  doc /* {d} */")
    out.append(pad + "}")
    return out


def emit_satisfy(sat, pad) -> list[str]:
    client = [_name(c) for c in list(sat.client)]
    supplier = [_name(s) for s in list(sat.supplier)]
    if not supplier or not client:
        raise UnmappedFeature("Satisfy without client/supplier names")
    # normative: Satisfy -> SatisfyRequirementUsage; v1 client satisfies
    # v1 supplier requirement -> v2 'satisfy <name> : <req> by <part>'
    return [f"{pad}satisfy {(_name(sat) or 'satisfy')} : "
            f"{', '.join(supplier)} by {', '.join(client)};"]


def emit_derive_reqt(dr, pad) -> list[str]:
    """DeriveReqt -> DerivationConnections::Derivation connection
    (normative: 'connection : DerivationConnections::Derivation
    connect <derived> to <source>;')"""
    client = [_name(c) for c in list(dr.client)]
    supplier = [_name(s) for s in list(dr.supplier)]
    if not supplier or not client:
        raise UnmappedFeature("DeriveReqt without client/supplier names")
    return [f"{pad}connection : DerivationConnections::Derivation "
            f"connect {', '.join(client)} to {', '.join(supplier)};"]


def emit_dependency(dep, pad, annotated=False) -> list[str]:
    """Dependency/Realization/Abstraction -> Dependency. Refine/Trace are
    annotated with v1-library metadata per the normative examples; the
    metadata definition (SysMLv1Library::RefineData/TraceData) is emitted
    locally so the result parses standalone."""
    client = [_name(c) for c in list(dep.client)]
    supplier = [_name(s) for s in list(dep.supplier)]
    if not supplier or not client:
        raise UnmappedFeature("dependency without client/supplier names")
    nm = _name(dep)
    head = f"{pad}dependency " + (f"{nm} " if nm else "") \
        + f"from {', '.join(client)} to {', '.join(supplier)}"
    if not annotated:
        return [head + ";"]
    tag = "RefineData" if isinstance(dep, S.Refine) else "TraceData"
    attr = "isRefine" if tag == "RefineData" else "isTrace"
    out = [f"{pad}metadata def {tag} {{ attribute {attr} : Boolean; }}",
           head + " {"]
    out.append(f"{pad}  @{tag} {{ {attr} = true; }}")
    out.append(pad + "}")
    return out


def emit_allocate(al, pad) -> list[str]:
    """Allocate -> AllocationDefinition (definition ends) or
    AllocationUsage inside an anonymous allocation def (usage ends)."""
    src, tgt = list(al.client)[0], list(al.supplier)[0]
    src_t, tgt_t = _name(src._vals.get("type")), _name(tgt._vals.get("type"))
    src_n, tgt_n = _name(src), _name(tgt)
    usage = isinstance(src, U.Property) or isinstance(tgt, U.Property)
    out = [f"{pad}allocation def" +
           (f" {_name(al)}" if not usage and _name(al) else "") + " {"]
    out.append(f"{pad}  end :>> source" + (f" : {src_t}" if src_t else "") + ";")
    out.append(f"{pad}  end :>> target" + (f" : {tgt_t}" if tgt_t else "") + ";")
    if usage:
        out.append(f"{pad}  allocate source.{src_n} to target.{tgt_n};")
    out.append(pad + "}")
    return out


def emit_testcase(tc, pad, verify_rels) -> list[str]:
    """TestCase (applied to an activity) -> VerificationCaseDefinition with
    'return verdict : VerificationCases::VerdictKind' (normative); each
    Verify relationship whose client is this test case becomes a
    RequirementVerificationMembership inside an objective."""
    nm = _name(tc) or "?"
    mine = [v for v in verify_rels if any(c is tc for c in list(v.client))]
    out = [f"{pad}verification def {nm} {{"]
    for v in mine:
        reqs = [_name(s) for s in list(v.supplier)]
        if not reqs:
            raise UnmappedFeature("Verify without named supplier requirement")
        out.append(f"{pad}  objective obj_{nm} {{")
        for r in reqs:
            out.append(f"{pad}    verify {r};")
        out.append(f"{pad}  }}")
    out.append(f"{pad}  return verdict : VerificationCases::VerdictKind;")
    out.append(pad + "}")
    return out


# --------------------------------------------------------------------------
# properties (attributes / parts / ports / items / occurrences)
# --------------------------------------------------------------------------

def emit_property(prop, indent) -> list[str]:
    pad = "  " * indent
    nm = _name(prop) or "?"
    t = prop._vals.get("type")
    composite = prop._vals.get("aggregation") is U.AggregationKind.composite
    mult = _mult(prop)
    dflt = _default_suffix(prop)
    owner = getattr(prop, "owner", None)

    if isinstance(prop, U.Port):
        if isinstance(prop, S.FullPort):
            # normative: FullPort_Mapping (7.8.7.3.7, typed) /
            # FullPortUntyped_Mapping (7.8.7.3.15) -> PartUsage with
            # SysMLv1Library::PortData {isFullPort = true;} metadata;
            # the stub is emitted at package level by emit_v2
            tn = _name(t)
            return [f"{pad}part {nm}" + (f" : {tn}" if tn else "")
                    + " {@PortData {isFullPort = true;}}"]
        if isinstance(prop, S.ProxyPort):
            # base Port mapping still applies; the ProxyPort stereotype
            # itself has no normative mapping in ptc/2025-04-07 (Table 30
            # lists no target; SYSML2_-329)
            if t is None:
                return [f"{pad}port {nm};",
                        f"{pad}/* v1 ProxyPort has no normative mapping "
                        "(7.8.7 Table 30; SYSML2_-329) */"]
            tn = _name(t)
            return [f"{pad}port {nm}{mult} : {tn};",
                    f"{pad}/* v1 ProxyPort has no normative mapping "
                    "(Table 30; SYSML2_-329) */"]
        if t is None:                        # normative: untyped Port ->
            return [f"{pad}port {nm};"]      # PortUsage
        tn = _name(t)
        if isinstance(t, S.InterfaceBlock):  # normative: typed PortUsage
            return [f"{pad}port {nm}{mult} : {tn};"]
        raise UnmappedFeature(f"Port {nm!r} typed by {type(t).__name__} {tn!r}")

    if isinstance(prop, S.FlowProperty):
        # normative 7.8.7.3.4-.6 (flagged SYSML2_-76 but specified):
        # directed usages; the target feature is always referential
        d = _flow_dir(prop)
        if t is None:                        # -> ReferenceUsage, referential
            return [f"{pad}{d}{nm};"]
        tn = _name(t)
        if tn is None:
            raise UnmappedFeature(f"FlowProperty {nm!r} typed by unnamed "
                                  f"{type(t).__name__}")
        if isinstance(t, U.DataType):        # -> AttributeUsage + direction
            return [f"{pad}{d}attribute {nm}{mult} : {tn};"]
        if isinstance(t, (U.Class, U.Interface)):
            # -> OccurrenceUsage, referential
            return [f"{pad}{d}ref occurrence {nm}{mult} : {tn};"]
        raise UnmappedFeature(f"FlowProperty {nm!r} typed by "
                              f"{type(t).__name__} {tn!r}")

    if t is None:
        # normative: "maps properties without a type" -> Feature
        return [f"{pad}feature {nm}{dflt};"]
    tn = _name(t)
    if tn is None:
        raise UnmappedFeature(f"Property {nm!r} typed by unnamed element")
    if isinstance(t, U.Port):
        raise UnmappedFeature(f"Property {nm!r} typed by a Port")

    if isinstance(t, S.ConstraintBlock):     # constraint property usage
        return [f"{pad}constraint {nm}{mult} : {tn}{dflt};"]
    if isinstance(t, (U.Signal, U.InformationItem)):
        return [f"{pad}item {nm}{mult} : {tn}{dflt};"]
    if _is_stereo_class(t):
        if isinstance(t, S.Block):
            # normative: Property typed by block -> PartUsage; isComposite
            kind = "part" if composite else "ref part"
            return [f"{pad}{kind} {nm}{mult} : {tn}{dflt};"]
        if isinstance(t, (S.ValueType, S.Requirement)):
            kw = "in " if isinstance(owner, S.ConstraintBlock) else ""
            # constraint parameters are 'in attribute' (7.8.5.2.1 gold)
            return [f"{pad}{kw}attribute {nm}{mult} : {tn}{dflt};"]
        if isinstance(t, S.InterfaceBlock):
            # PropertyTypedByClassInterface: InterfaceBlock is a Class
            return [f"{pad}occurrence {nm}{mult} : {tn}{dflt};"]
        if isinstance(t, S.TestCase):
            raise UnmappedFeature(f"Property {nm!r} typed by TestCase")
        raise UnmappedFeature(f"Property {nm!r} typed by {type(t).__name__} {tn!r}")
    if isinstance(t, U.DataType):
        kw = "in " if isinstance(owner, S.ConstraintBlock) else ""
        return [f"{pad}{kw}attribute {nm}{mult} : {tn}{dflt};"]
    if isinstance(t, U.Enumeration):
        kw = "in " if isinstance(owner, S.ConstraintBlock) else ""
        return [f"{pad}{kw}attribute {nm}{mult} : {tn}{dflt};"]
    if isinstance(t, U.Class):               # plain class -> OccurrenceUsage
        # normative: 'occurrence p [0..1] : C;' / 'ref occurrence ...'
        kind = "occurrence" if composite else "ref occurrence"
        return [f"{pad}{kind} {nm}{mult} : {tn}{dflt};"]
    raise UnmappedFeature(f"Property {nm!r} typed by {type(t).__name__} {tn!r}")


# --------------------------------------------------------------------------
# validation with sysmlpy
# --------------------------------------------------------------------------

def validate_with_sysmlpy(text: str) -> dict:
    """Parse emitted v2 text with sysmlpy (authoritative v2 reader)."""
    import sys

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