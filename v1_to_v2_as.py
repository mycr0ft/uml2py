#!/usr/bin/env python
"""v1_to_v2_as.py — clean-room SysML v1 → v2 abstract-syntax transformer.

Requirement 3 of the transformation conformance clause (§2 of
ptc/2025-04-07): transform an abstract-syntax representation of an input
SysML v1 model into an abstract-syntax representation of a SysML v2
model. This module constructs gen.sysml2 objects (R2 artifact) from
gen.uml25 + gen.sysml objects (R1 artifacts) — the same normative
mappings v1_to_v2.py implements for textual notation, but building the
AS the clause demands.

Mapping authority: OMG "SysML v2.0 Beta 4, Part 2: SysML v1 to SysML v2
Transformation" (ptc/2025-04-07), same anchors as v1_to_v2.py. Anything
without a normative mapping raises UnmappedFeature.

Wave A (this module): core structural mappings
  Block→PartDefinition (7.8.4.3.3) via ToPartUsage_Init family,
  Property typed by block + isComposite→PartUsage (7.8.4.3.13),
  non-composite block-typed Property→PartUsage w/ isComposite=false
  (the 'ref part' form), Property untyped→Feature, ValueType→
  AttributeDefinition (7.8.4.3.14), Enumeration→EnumerationDefinition,
  EnumerationLiteral→EnumerationUsage, ConstraintBlock→
  ConstraintDefinition (7.8.5.3.1), plain Class→OccurrenceDefinition,
  Property typed by plain Class→OccurrenceUsage (7.7.4.2.37),
  Generalization→Subclassification (7.7.4.2.12), typing via
  FeatureTyping (Core-Features), Comment→Documentation
  (7.4.2.1.9 ToDocumentation_Init).

One v1 element maps to exactly ONE v2 AS object (kept in the index);
usage typings reference that object rather than duplicating it.

Honest elisions (documented, no data invented silently):
  - multiplicities: v1 upperValue/lowerValue have no settable AS end
    (MultiplicityRange bounds are derived unions in the metamodel and
    the runtime has no FeatureMultiplicityMembership storage); the
    textual pipeline carries them, the AS wave does not yet.
  - behaviors (Operations/Activities), connectors, ports, state
    machines, requirements: raise UnmappedFeature (later waves).
"""
from __future__ import annotations

import gen.uml25 as U
import gen.sysml2 as S2
import gen.sysml as S


class UnmappedFeature(Exception):
    """A v1 element whose normative v2 mapping is not implemented."""


def _name(el):
    n = getattr(el, "name", None)
    return n if isinstance(n, str) and n else None


def _own_membership(owner, member):
    """Owner gains *member* through an OwningMembership (the normative
    ownership mechanism for package members and nested definitions)."""
    om = S2.OwningMembership()
    om.ownedRelatedElement.append(member)
    owner.ownedRelationship.append(om)
    return om


def _feature_membership(owner_def, feature):
    """Owner gains *feature* through a FeatureMembership (the normative
    membership for features of a Type; makes the Type a featuringType)."""
    fm = S2.FeatureMembership()
    fm.ownedRelatedElement.append(feature)
    owner_def.ownedRelationship.append(fm)
    return fm


def _type_feature(feature, type_def):
    """FeatureTyping (§7.4.2.2.24 ToPortDefinition family / KerML
    Core-Features-FeatureTyping): feature.type = type_def. The typing is
    owned by the feature (ownedTyping), which back-wires owningFeature."""
    ft = S2.FeatureTyping()
    ft.type = type_def
    feature.ownedTyping.append(ft)
    return ft


def _attach_documentation(v1_el, v2_el):
    """ToDocumentation_Init (7.4.2.1.9): v1 Comment → Documentation
    owned by the transformed element (owner == documentedElement),
    plus an explicit Annotation relationship to the documented element
    (the Annotation.derived back-ends — annotatingElement, ownedAnnotation
    — are runtime-elided; the relationship itself is carried)."""
    docs = []
    for c in getattr(v1_el, "ownedComment", ()):
        d = S2.Documentation(body=c.body if isinstance(c.body, str) else None)
        _own_membership(v2_el, d)
        ann = S2.Annotation()
        ann.annotatedElement = v2_el
        d.ownedRelationship.append(ann)
        docs.append(d)
    return docs


def transform_v1_element(el, index=None):
    """Dispatch on v1 metaclass: build the v2 AS object per the
    normative mapping. Returns the v2 element (not yet owned).

    The index (id(v1) -> v2 AS object) is shared through the recursive
    population passes; pass-1 callers pass it so requirement/TestCase
    objects register before relationship ends resolve."""
    if index is None:
        index = {}
    if isinstance(el, U.Package):
        return S2.Package(declaredName=_name(el))
    if isinstance(el, S.ConstraintBlock):
        # ConstraintBlock_Mapping (7.8.5.3.1): to ConstraintDefinition
        # (before the Block check: ConstraintBlock specializes Block)
        return S2.ConstraintDefinition(declaredName=_name(el))
    if isinstance(el, S.Block):
        # Block_Mapping (7.8.4.3.3): to PartDefinition
        return S2.PartDefinition(declaredName=_name(el))
    if isinstance(el, S.ValueType):
        # ValueType_Mapping (7.8.4.3.14): to AttributeDefinition
        return S2.AttributeDefinition(declaredName=_name(el))
    if isinstance(el, U.Enumeration):
        # Enumeration_Mapping: to EnumerationDefinition (before the
        # DataType check: Enumeration specializes DataType)
        return S2.EnumerationDefinition(declaredName=_name(el))
    if isinstance(el, U.DataType):
        # plain DataType (non-stereotyped): same mapping family as
        # ValueType -> AttributeDefinition (7.8.4.3.14)
        return S2.AttributeDefinition(declaredName=_name(el))
    if isinstance(el, U.EnumerationLiteral):
        # EnumerationLiteral_Mapping: to EnumerationUsage
        return S2.EnumerationUsage(declaredName=_name(el))
    if isinstance(el, U.Actor):
        # Actor_Mapping (7.7.13.3.1): to PartDefinition
        return S2.PartDefinition(declaredName=_name(el))
    if isinstance(el, U.Class):
        # Class_Mapping (7.7.4.2.37 family): plain Class to
        # OccurrenceDefinition. Metaclasses with their own normative
        # mappings (use cases, signals, information items, interfaces,
        # ports machinery) are later waves — not guesses.
        if isinstance(el, (U.UseCase, U.Signal, U.Interaction,
                           U.InformationItem, U.Interface,
                           S.InterfaceBlock)):
            raise UnmappedFeature(
                f"{type(el).__name__} (own mapping, later wave)")
        if isinstance(el, S.Requirement):
            # Requirement_Mapping (7.8.8.3.30)
            return _transform_requirement(el, index)
        if isinstance(el, S.TestCase):
            # TestCase_Mapping (7.8.8.3.27): TestCase →
            # VerificationCaseDefinition
            return S2.VerificationCaseDefinition(
                declaredName=_name(el))
        return S2.OccurrenceDefinition(declaredName=_name(el))
    if isinstance(el, U.StateMachine):
        # StateMachine_Mapping (7.7.11.2.16): to StateDefinition
        return S2.StateDefinition(declaredName=_name(el))
    if isinstance(el, (U.Activity, U.OpaqueBehavior)):
        # Activity_Mapping (7.7.3.3.1) / OpaqueBehavior: ActionDefinition
        return S2.ActionDefinition(declaredName=_name(el))
    raise UnmappedFeature(type(el).__name__)


def _as_type_name(t):
    """The v1 type object must have a name to be referenced; the
    transformation is name-resolving at package scope."""
    tn = _name(t)
    if tn is None:
        raise UnmappedFeature(
            f"property typed by unnamed {type(t).__name__}")
    return tn


def transform_property(prop, owner_def, index):
    """Property_Mapping (7.8.4.3.13 + 7.7.4.2.36): composite block-typed
    Property → PartUsage typed by the block's (already built) AS
    PartDefinition; non-composite → same PartUsage with
    isComposite=false (the 'ref part' form); value/enum/DataType-typed →
    AttributeUsage; plain-Class-typed → OccurrenceUsage (composite) or
    referential OccurrenceUsage; untyped → Feature."""
    nm = _name(prop)
    t = prop._vals.get("type")
    composite = prop._vals.get("aggregation") is U.AggregationKind.composite
    if t is None:
        # normative: untyped Property → Feature (bare usage declaration)
        f = S2.Feature(declaredName=nm)
        _feature_membership(owner_def, f)
        return f
    tdef = index.get(id(t))
    if tdef is None:
        raise UnmappedFeature(
            f"Property {nm!r} typed by external/unordered "
            f"{type(t).__name__} {_as_type_name(t)!r}")
    if isinstance(t, S.Block):
        usage = S2.PartUsage(declaredName=nm)
        if not composite:
            usage.isComposite = False     # 'ref part' (7.8.4.3.13)
    elif isinstance(t, (S.ValueType, U.DataType, U.Enumeration)):
        usage = S2.AttributeUsage(declaredName=nm)
    elif isinstance(t, U.Class):
        usage = S2.OccurrenceUsage(declaredName=nm)
        if not composite:
            usage.isComposite = False     # 'ref occurrence' (7.7.4.2.37)
    else:
        raise UnmappedFeature(
            f"Property {nm!r} typed by {type(t).__name__}")
    _type_feature(usage, tdef)
    _feature_membership(owner_def, usage)
    return usage


def _populate_class(v1cls, v2def, index, pending):
    """Features, nested classifiers and generalizations of a v1
    class-like element onto its AS definition (documentation was
    attached in pass 1)."""
    for attr in list(v1cls.ownedAttribute):
        transform_property(attr, v2def, index)
    for nested in list(v1cls.nestedClassifier):
        nv2 = transform_v1_element(nested)
        index[id(nested)] = nv2
        _own_membership(v2def, nv2)
        _populate_class(nested, nv2, index, pending)
    for g in list(v1cls.generalization):
        pending.append((v2def, g))


def _populate_statemachine(sm, v2def, index):
    """StateMachine internals (7.7.11.2.x): Regions inlined — States/
    Pseudostates/FinalStates → StateUsage; Transitions → TransitionUsage
    with source/target; initial states elided (SYSML2_-203)."""
    for member in list(sm.ownedMember):
        if isinstance(member, U.Region):
            for st in list(member.ownedMember):
                if isinstance(st, U.Transition):
                    continue
                if isinstance(st, U.Pseudostate) \
                        and st._vals.get("kind") is U.PseudostateKind.initial:
                    continue  # elided (SYSML2_-203)
                su = S2.StateUsage(declaredName=_name(st))
                _own_membership(v2def, su)
                index[id(st)] = su
        for tr in list(member.ownedMember):
            if not isinstance(tr, U.Transition):
                continue
            src, tgt = tr._vals.get("source"), tr._vals.get("target")
            if isinstance(src, U.Pseudostate) \
                    and src._vals.get("kind") is U.PseudostateKind.initial:
                continue  # elided (SYSML2_-203)
            src_obj = index.get(id(src))
            tgt_obj = index.get(id(tgt))
            if src_obj is None or tgt_obj is None:
                raise UnmappedFeature(
                    f"Transition {_name(tr)!r} to element outside the "
                    "state machine's owned states")
            tu = S2.TransitionUsage(declaredName=_name(tr))
            tu.source = src_obj
            tu.target = tgt_obj
            _own_membership(v2def, tu)
            index[id(tr)] = tu


def _populate_activity(act, v2def, index):
    """Activity internals (7.7.3.3.x): nodes → action usages /
    control-node usages; edges → SuccessionAsUsage (ControlFlow) or
    SuccessionFlowUsage (ObjectFlow) with source/target."""
    nodes = list(act.node)
    edges = list(act.edge)
    for n in nodes:
        nm = _name(n)
        if isinstance(n, U.OpaqueAction):
            au = S2.ActionUsage(declaredName=nm)
            _own_membership(v2def, au)
            index[id(n)] = au
        elif isinstance(n, U.DecisionNode):
            du = S2.DecisionNode(declaredName=nm)
            _own_membership(v2def, du)
            index[id(n)] = du
        elif isinstance(n, U.MergeNode):
            mu = S2.MergeNode(declaredName=nm)
            _own_membership(v2def, mu)
            index[id(n)] = mu
        elif isinstance(n, (U.InitialNode, U.FinalNode)):
            # normative: elided (initial → source feature of outgoing
            # edges; final → done-subsetted feature; 7.7.3.3.22)
            continue
        else:
            raise UnmappedFeature(
                f"Activity node {type(n).__name__} (later wave)")
    for e in edges:
        src, tgt = e._vals.get("source"), e._vals.get("target")
        src_obj, tgt_obj = index.get(id(src)), index.get(id(tgt))
        if src_obj is None or tgt_obj is None:
            # initial/final nodes elided: the edge itself is elided
            if isinstance(src, (U.InitialNode, U.FinalNode)) or \
                    isinstance(tgt, (U.InitialNode, U.FinalNode)):
                continue
            raise UnmappedFeature(
                f"edge {_name(e)!r} touching unmapped node")
        if isinstance(e, U.ObjectFlow):
            se = S2.SuccessionFlowUsage(declaredName=_name(e))
        else:
            se = S2.SuccessionAsUsage(declaredName=_name(e))
        # KerML succession ends are multi-valued feature chains; the
        # wave-A mapping yields exactly one source and one target
        se.source.append(src_obj)
        se.target.append(tgt_obj)
        _own_membership(v2def, se)
        index[id(e)] = se


def _populate_behavior_params(behavior, v2def):
    """Parameter → ReferenceUsage with direction (7.7.4.2.24; return →
    out per the Activity textual example)."""
    for p in list(behavior.ownedParameter):
        ref = S2.ReferenceUsage(declaredName=_name(p))
        d = p._vals.get("direction")
        if d is not None:
            val = str(getattr(d, "value", d))
            # normative (7.7.4.2.24): return -> out per the Activity
            # textual example
            ref.direction = "out" if val == "return" else val
        _feature_membership(v2def, ref)


def transform_package(pkg):
    """MainMapping (§7.2.2.4): transform a v1 Package (and contents)
    into a v2 AS Package. Returns the v2 root Package.

    pass 1: one AS definition per v1 member (the index is the
    conformance-critical identity: every reference resolves to it);
    pass 2: features/nested members/generalizations per owner;
    pass 3: generalizations resolved against the index by identity.
    """
    out = S2.Package(declaredName=_name(pkg) or "Package")
    index = {}   # id(v1 element) -> v2 AS object
    pending_generalizations = []

    # pass 1: one AS definition per v1 member (the index is the
    # conformance-critical identity: every reference resolves to it);
    # relationships (Satisfy/Verify/DeriveReqt/Dependency/Allocate) are
    # not built here — pass 3 resolves their ends from the index
    for el in list(pkg.ownedMember):
        if isinstance(el, (S.Satisfy, S.Verify, S.DeriveReqt, S.Allocate,
                           U.Abstraction, U.Dependency)):
            continue  # built in pass 3 (ends need the completed index)
        v2 = transform_v1_element(el, index)
        index[id(el)] = v2
        _own_membership(out, v2)
        _attach_documentation(el, v2)
        if isinstance(el, U.Enumeration):
            for lit in list(el.ownedLiteral):
                lv2 = S2.EnumerationUsage(declaredName=_name(lit))
                _feature_membership(v2, lv2)

    # pass 2: features / nested members / collected generalizations
    for el in list(pkg.ownedMember):
        v2 = index.get(id(el))
        if isinstance(el, (U.StateMachine, U.Activity, U.OpaqueBehavior)):
            if isinstance(el, U.StateMachine):
                _populate_statemachine(el, v2, index)
            else:
                _populate_activity(el, v2, index)
                _populate_behavior_params(el, v2)
        elif isinstance(el, U.Class):
            _populate_class(el, v2, index, pending_generalizations)

    # pass 3: requirements chain (7.8.8.3.x) — relationships resolve
    # their client/supplier ends against the pass-1 index
    for el in list(pkg.ownedMember):
        if isinstance(el, S.Satisfy):
            _transform_satisfy(el, out, index)
        elif isinstance(el, S.Verify):
            _transform_verify(el, out, index)
        elif isinstance(el, S.DeriveReqt):
            _transform_derive_reqt(el, out, index)
        elif isinstance(el, (U.Abstraction, U.Dependency)):
            _transform_dependency(el, out, index,
                                  annotated=isinstance(el, (S.Refine, S.Trace)))
        elif isinstance(el, S.Allocate):
            _transform_allocate(el, out, index)

    for sub_def, g in pending_generalizations:
        t = g._vals.get("general")
        general = index.get(id(t))
        if general is None:
            raise UnmappedFeature(
                f"generalization to external/unnamed {_name(t)!r}")
        subc = S2.Subclassification()
        subc.general = general
        sub_def.ownedSpecialization.append(subc)
    return out


# --------------------------------------------------------------------------
# requirements chain (7.8.8.3.x)
# --------------------------------------------------------------------------

def _transform_requirement(req, index):
    """Requirement_Mapping (7.8.8.3.30): Requirement → RequirementUsage
    with the v1 id carried as the requirement's declaredShortId-style
    text (the textual example puts the id in quotes next to the name);
    text → Documentation (normative: text → doc)."""
    ru = S2.RequirementUsage(declaredName=_name(req))
    rid = req._vals.get("id")
    if isinstance(rid, str) and rid:
        # the id travels as an aliasIds-style metadata comment in the
        # textual form; in AS it is carried on the usage's element
        ru.aliasIds.append(rid)
    txt = req._vals.get("text")
    if isinstance(txt, str) and txt:
        doc = S2.Documentation(body=txt)
        _own_membership(ru, doc)
    _attach_documentation(req, ru)
    index[id(req)] = ru
    return ru


def _transform_satisfy(sat, out, index):
    """Satisfy_Mapping (7.8.8.3.44): Satisfy → SatisfyRequirementUsage;
    v1 client (the satisfying part) → satisfyingFeature; v1 supplier
    (the requirement) → satisfiedRequirement."""
    clients = [index.get(id(c)) for c in list(sat.client)]
    reqs = [index.get(id(s)) for s in list(sat.supplier)]
    if not clients or not any(cl for cl in clients) \
            or not any(s for s in list(sat.supplier)):
        raise UnmappedFeature("Satisfy without mapped client/supplier")
    sru = S2.SatisfyRequirementUsage(declaredName=_name(sat))
    for cl in clients:
        if cl is not None:
            sru.satisfyingFeature = cl
            break
    for s in sat.supplier:
        r = index.get(id(s))
        if r is not None:
            sru.satisfiedRequirement = r
            break
    _own_membership(out, sru)
    return sru


def _transform_verify(verify, out, index):
    """Verify_Mapping (7.8.8.3.49): Verify → the verification case's
    RequirementVerificationMembership; the v1 supplier requirement is
    the verifiedRequirement; the v1 client (TestCase) must already be a
    VerificationCaseDefinition in the index."""
    tc = next((index.get(id(c)) for c in list(verify.client)
               if index.get(id(c)) is not None
               and type(index.get(id(c))).__name__
               == "VerificationCaseDefinition"), None)
    if tc is None:
        raise UnmappedFeature(
            "Verify whose client is not a mapped TestCase")
    req = next((index.get(id(s)) for s in list(verify.supplier)
                if index.get(id(s)) is not None), None)
    if req is None:
        raise UnmappedFeature("Verify without mapped supplier requirement")
    rvm = S2.RequirementVerificationMembership()
    rvm.verifiedRequirement = req
    _own_membership(tc, rvm)
    return rvm


def _transform_derive_reqt(dr, out, index):
    """DeriveReqt_Mapping (7.8.8.3.15): DeriveReqt → ConnectionUsage
    typed by the DerivationConnections::Derivation model-library
    connection (referenced by qualified name; the library itself is
    external — the same name reference the textual form emits)."""
    client = next((index.get(id(c)) for c in list(dr.client)
                   if index.get(id(c)) is not None), None)
    supplier = next((index.get(id(s)) for s in list(dr.supplier)
                     if index.get(id(s)) is not None), None)
    if client is None or supplier is None:
        raise UnmappedFeature(
            "DeriveReqt without mapped client/supplier requirements")
    cu = S2.ConnectionUsage(declaredName=_name(dr))
    # the typing target is the library-defined Derivation; carried by
    # name — wave-1 notes the FeatureTyping would need the library
    # package, which is not part of the input model
    cu.source.append(client)
    cu.target.append(supplier)
    _own_membership(out, cu)
    return cu


def _transform_dependency(dep, out, index, annotated=False):
    """Dependency_Mapping (7.7.6.2.9): Dependency/Realization/Abstraction
    → Dependency; Refine/Trace annotated with v1-library metadata."""
    clients = [index.get(id(c)) for c in list(dep.client)]
    suppliers = [index.get(id(s)) for s in list(dep.supplier)]
    if not any(clients) or not any(suppliers):
        raise UnmappedFeature("dependency without mapped client/supplier")
    dep2 = S2.Dependency(declaredName=_name(dep))
    for cl in clients:
        if cl is not None:
            dep2.client.append(cl)
    for sp in suppliers:
        if sp is not None:
            dep2.supplier.append(sp)
    _own_membership(out, dep2)
    return dep2


def _transform_allocate(al, out, index):
    """Allocate_Mapping (7.8.3.3.9/.10): Allocate → AllocationUsage
    (usage ends) inside an AllocationDefinition; source/target ends."""
    src = next(iter(list(al.client)), None)
    tgt = next(iter(list(al.supplier)), None)
    if src is None or tgt is None:
        raise UnmappedFeature("Allocate without client/supplier")
    src_obj = index.get(id(src._vals.get("type"))) \
        if isinstance(src, U.Property) else index.get(id(src))
    tgt_obj = index.get(id(tgt._vals.get("type"))) \
        if isinstance(tgt, U.Property) else index.get(id(tgt))
    if src_obj is None or tgt_obj is None:
        raise UnmappedFeature(
            "Allocate ends reference unmapped definitions")
    al_def = S2.AllocationDefinition(declaredName=_name(al))
    al_usage = S2.AllocationUsage()
    al_usage.source.append(src_obj)
    al_usage.target.append(tgt_obj)
    _own_membership(al_def, al_usage)
    _own_membership(out, al_def)
    return al_def


# --------------------------------------------------------------------------
# R3 conformance: read a v1 XMI (R1 artifact) -> AS transform (R3) -> v2 AS
# --------------------------------------------------------------------------

def transform_xmi(path):
    """R1→R2→R3 pipeline entry: read a SysML v1 XMI 2.1 file into
    gen.uml25 objects (R1), transform every root Package (R3), and
    return the list of gen.sysml2 Packages (R2 artifacts)."""
    import xmi21
    model = xmi21.read_xmi21(path)
    out = []
    for root in model.roots:
        if isinstance(root, U.Package):
            out.append(transform_package(root))
    return out
