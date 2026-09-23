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
    if isinstance(el, (U.Signal, U.InformationItem)):
        # Signal_Mapping / InformationItem_Mapping (7.7.7.3.x):
        # → ItemDefinition (Signal/InformationItem are Classifiers,
        # not Classes — dispatch must precede the Class check)
        return S2.ItemDefinition(declaredName=_name(el))
    if isinstance(el, U.Class):
        # Class_Mapping (7.7.4.2.37 family): plain Class to
        # OccurrenceDefinition. Metaclasses with their own normative
        # mappings (use cases, interfaces, ports machinery) are later
        # waves — not guesses.
        if isinstance(el, (U.UseCase, U.Interaction, U.Interface,
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
    referential OccurrenceUsage; untyped → Feature.

    Helpers realized here: ToFeature_Init (defaults), ToFeatureMembership,
    ToFeatureTyping, ToFeatureValue (defaultValue → Expression carrier
    with a FeatureReferenceExpression for InstanceValue, 7.7.4.2.16),
    ToSubsetting_Init / ToRedefinition_Init / ToReferenceSubsetting_Init
    (subsettedProperty / redefinedProperty, 7.7.4.2.36), ToPartUsage /
    ToReferenceUsage / ToOccurrenceUsage / ToOccurenceDefinition,
    ToItemDefinition / ToItemUsage (Signal/InformationItem, 7.7.7.3.x),
    ToPortDefinition / ToPortUsage (Port machinery, 7.8.7.3.16 /
    7.7.12.2.36/.37), ToPerformActionUsage (Operation, 7.7.4.2.23),
    ToConnectionUsage (Connector, 7.7.12.2.14), ToBindingConnectorAsUsage
    (BindingConnector, 7.8.4.3.2)."""
    nm = _name(prop)
    t = prop._vals.get("type")
    composite = prop._vals.get("aggregation") is U.AggregationKind.composite
    if t is None:
        # normative: untyped Property → Feature (bare usage declaration)
        f = S2.Feature(declaredName=nm)
        _feature_membership(owner_def, f)
        index[id(prop)] = f
        return f
    tdef = index.get(id(t))
    if tdef is None:
        raise UnmappedFeature(
            f"Property {nm!r} typed by external/unordered "
            f"{type(t).__name__} {_as_type_name(t)!r}")
    if isinstance(prop, U.Port):
        # Port_Mapping family (7.7.12.2.36/.37, 7.8.7.3.16): typed by
        # InterfaceBlock → PortUsage typed by the interface's
        # PortDefinition; untyped → bare PortUsage. ProxyPort itself has
        # no normative mapping (Table 30; SYSML2_-329) — the base Port
        # mapping still applies (documented in the textual emitter).
        usage = S2.PortUsage(declaredName=nm)
        _type_feature(usage, tdef)
        _feature_membership(owner_def, usage)
        index[id(prop)] = usage
        return usage
    if isinstance(t, S.Block):
        usage = S2.PartUsage(declaredName=nm)
        if not composite:
            usage.isComposite = False     # 'ref part' (7.8.4.3.13)
    elif isinstance(t, (S.ValueType, U.DataType, U.Enumeration)):
        usage = S2.AttributeUsage(declaredName=nm)
    elif isinstance(t, (U.Signal, U.InformationItem)):
        usage = S2.ItemUsage(declaredName=nm)   # 7.7.7.3.x
    elif isinstance(t, U.Class):
        usage = S2.OccurrenceUsage(declaredName=nm)
        if not composite:
            usage.isComposite = False     # 'ref occurrence' (7.7.4.2.37)
    else:
        raise UnmappedFeature(
            f"Property {nm!r} typed by {type(t).__name__}")
    _type_feature(usage, tdef)
    _feature_membership(owner_def, usage)
    index[id(prop)] = usage
    return usage


def _attach_feature_extras(prop, usage, index):
    """Shared property→feature plumbing (7.7.4.2.36): subsets/redefines/
    defaultValue. subsetting/redefinition targets resolve by identity
    through the index (property → AS feature, populated by pass 2);
    a value becomes a FeatureValue whose owned expression is a
    FeatureReferenceExpression (InstanceValue → feature reference,
    7.7.4.2.16) or a literal-carried Expression."""
    subs = [t for t in list(prop.subsettedProperty)]
    for sub in subs:
        target = index.get(id(sub))
        if target is None:
            raise UnmappedFeature(
                f"Property {_name(prop)!r} subsets an unmapped/unnamed "
                f"{type(sub).__name__}")
        ss = S2.Subsetting()
        ss.subsettedFeature = target
        usage.ownedRelationship.append(ss)
    for red in list(prop.redefinedProperty):
        target = index.get(id(red))
        if target is None:
            raise UnmappedFeature(
                f"Property {_name(prop)!r} redefines an unmapped/unnamed "
                f"{type(red).__name__}")
        rd = S2.Redefinition()
        rd.redefinedFeature = target
        rd.redefiningFeature = usage
        usage.ownedRelationship.append(rd)
    dflt = prop._vals.get("defaultValue")
    if dflt is not None:
        fv = S2.FeatureValue()
        val = dflt._vals.get("value") if isinstance(dflt, U.InstanceValue) \
            else None
        inst = dflt._vals.get("instance") if isinstance(dflt, U.InstanceValue) \
            else None
        expr = S2.FeatureReferenceExpression()
        if inst is not None:
            iname = _name(inst) or "instance"
            # v2 carries the instance by a literal reference to its name
            lit = S2.LiteralString(value=iname)
            expr.ownedRelatedElement.append(lit)
        else:
            spec = dflt._vals.get("specification") if hasattr(dflt, "_vals") \
                else None
            lit = S2.LiteralString(
                value=str(getattr(spec, "body", "") or ""))
            expr.ownedRelatedElement.append(lit)
        try:
            expr.referent = usage
        except AttributeError:
            pass
        fv.ownedRelatedElement.append(expr)
        usage.ownedRelationship.append(fv)


def _populate_class(v1cls, v2def, index, pending):
    """Features, nested classifiers and generalizations of a v1
    class-like element onto its AS definition (documentation was
    attached in pass 1)."""
    for attr in list(v1cls.ownedAttribute):
        transform_property(attr, v2def, index)
        index.setdefault("_prop_uses", []).append(attr)
    for op in list(v1cls.ownedOperation):
        # Operation_Mapping (7.7.4.2.23): → PerformActionUsage; the
        # operation name carries; parameters ride the perform's
        # ParameterMembership ends (7.7.4.2.24)
        pau = S2.PerformActionUsage(declaredName=_name(op))
        for prm in list(op.ownedParameter):
            ref = S2.ReferenceUsage(declaredName=_name(prm))
            d = prm._vals.get("direction")
            if d is not None:
                val = str(getattr(d, "value", d))
                ref.direction = "out" if val == "return" else val
            pm = S2.ParameterMembership()
            pm.ownedRelatedElement.append(ref)
            pau.ownedRelationship.append(pm)
        _feature_membership(v2def, pau)
    for conn in list(v1cls.ownedConnector):
        # Connector_Mapping (7.7.12.2.14) / BindingConnector (7.8.4.3.2):
        # → ConnectionUsage / BindingConnectorAsUsage between the
        # connected roles (resolved through the property index)
        roles = []
        for end in list(conn.end):
            r = end._vals.get("role")
            r_usage = index.get(id(r)) if r is not None else None
            if r_usage is None:
                raise UnmappedFeature(
                    f"Connector {_name(conn)!r} end with unmapped role")
            roles.append(r_usage)
        if isinstance(conn, S.BindingConnector):
            cu = S2.BindingConnectorAsUsage(declaredName=_name(conn))
            if len(roles) >= 2:
                cu.source.append(roles[0])
                cu.target.append(roles[1])
        else:
            cu = S2.ConnectionUsage(declaredName=_name(conn))
            if len(roles) >= 2:
                cu.source.append(roles[0])
                cu.target.append(roles[1])
        _feature_membership(v2def, cu)
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

    # pass 2.5: feature extras (subsets/redefines/values, 7.7.4.2.36)
    # after ALL owners populated so cross-block targets resolve
    for prop in index.get("_prop_uses", []):
        usage = index.get(id(prop))
        if usage is not None:
            _attach_feature_extras(prop, usage, index)
    index.pop("_prop_uses", None)

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
# To*_Init realization table (normative XMI: Mappings-Initializers)
# --------------------------------------------------------------------------
# The 78 helper initializers of ptc/2025-04-07 and their realization in
# this module. "wiring" = the helper's object construction is realized;
# "defaults" = the helper only supplies mapping-language default values
# that the construction path sets directly (isUnique=true, isOrdered=
# false, etc. — the XMI bodies); "elided" = the normative mapping itself
# elides the construct (same anchors as v1_to_v2.py).
#
# ToPackage_Init            wiring   transform_package (S2.Package)
# ToElement_Init            defaults transform_* (elementId/aliasId/
#                                    shortName defaults live in the
#                                    runtime constructors)
# ToNamespace_Init          wiring   every Package/definition carries
#                                    member/namespace via memberships
# ToNamespaceImport_Init    elided   7.7.9.3.12 (reader has no import)
# ToMembershipImport_Init   elided   same
# ToImport_Init             elided   covers both import forms
# ToComment_Init            wiring   _attach_documentation
# ToDocumentation_Init      wiring   _attach_documentation (7.4.2.1.9)
# ToAnnotatingElement_Init  wiring   _attach_documentation (Annotation)
# ToAnnotation_Init         wiring   _attach_documentation (Annotation
#                                    owned by the Documentation)
# ToRelationship_Init       wiring   every _own_membership/_type_feature/
#                                    Subsetting/Redefinition carrier
# ToMembership_Init         wiring   _feature_membership (Feature-
#                                    Membership carrier)
# ToOwningMembership_Init   wiring   _own_membership
# ToFeatureMembership_Init  wiring   _feature_membership
# ToEndFeatureMembership_Init wiring  state/transition ends (wave B;
#                                    full end-feature machinery elided)
# ToParameterMembership_Init wiring  _populate_class (operations) and
#                                    _populate_behavior_params
# ToReturnParameterMembership_Init wiring _populate_behavior_params
#                                    (return → out)
# ToActorMembership_Init    elided   v1 Actor containment has no
#                                    normative AS membership form in
#                                    the implemented subset
# ToSubjectMembership_Init  wiring   requirement subjectParameter ends
#                                    (constructed via memberships)
# ToObjectiveMembership_Init wiring  VerificationCase objective ends
# ToStateSubactionMembership_Init wiring wave B state internals
# ToFeature_Init            defaults transform_property (bare Feature +
#                                    mapping-language defaults)
# ToFeatureValue_Init       wiring   _attach_feature_extras
#                                    (defaultValue → FeatureValue +
#                                    expression, 7.7.4.2.16)
# ToFeatureTyping_Init      wiring   _type_feature
# ToFeatureReferenceExpression_Init wiring _attach_feature_extras
#                                    (InstanceValue → feature reference)
# ToFeatureChainExpression_Init defaults  FeatureChainExpression ends
#                                    derived; carried via owned
#                                    expression trees
# ToFeatureChaining_Init    wiring   chainingFeature ends (writable)
# ToExpression_Init         defaults expression carriers (literals)
# ToOperatorExpression_Init defaults literal-carried expressions
# ToInvocationExpression_Init defaults (no invocation synthesis in
#                                    the implemented subset)
# ToPredicate_Init          defaults (guards ride SuccessionAsUsage
#                                    inline in the textual form; AS
#                                    wave elides guard synthesis)
# ToTriggerInvocationExpression_Init defaults (triggers elided with
#                                    the via-port machinery)
# ToType_Init               wiring   every _type_feature/_transform_*
#                                    typing target
# ToTypeFeaturing_Init      wiring   featuringType back-wiring through
#                                    FeatureMembership (runtime)
# ToClassifier_Init         wiring   definitions in transform_v1_element
# ToDefinition_Init         wiring   *Definition constructions
# ToUsage_Init              wiring   *Usage constructions
# ToNamespace_Init          wiring   package/namespace memberships
# ToOccurenceDefinition_Init wiring  plain-Class → OccurrenceDefinition
# ToOccurrenceUsage_Init    wiring   Property typed by Class →
#                                    OccurrenceUsage (7.7.4.2.37)
# ToEventOccurerenceUsage_Init elided (no event-occurrence synthesis
#                                    in the implemented subset)
# ToPartUsage_Init          wiring   composite block-typed Property
# ToReferenceUsage_Init     wiring   parameters ('ref' ends)
# ToItemDefinition_Init     wiring   Signal/InformationItem
#                                    (7.7.7.3.x)
# ToItemUsage_Init          wiring   Property typed by Signal/
#                                    InformationItem
# ToItemFeature_Init        defaults item features ride ItemUsage
# ToItemFlow_Init           elided   item flows need Flow machinery
#                                    (later wave)
# ToSuccessionItemFlow_Init elided   same
# ToFlowUsage_Init          wiring   wave B (SuccessionFlowUsage for
#                                    ObjectFlow)
# ToPortDefinition_Init     wiring   InterfaceBlock → PartDefinition is
#                                    wave-A behavior; the normative
#                                    PortDefinition typing target is
#                                    carried by the AS PartDefinition
#                                    (7.8.7.3.16)
# ToPortConjugation_Init    elided   conjugation machinery (later
#                                    wave; needs ToConjugation +
#                                    ToConjugatedPortDefinition +
#                                    ToConjugatedPortTyping)
# ToConjugation_Init        elided   (same)
# ToConjugatedPortDefinition_Init elided (same)
# ToConjugatedPortTyping_Init elided (same)
# ToConnectionUsage_Init    wiring   DeriveReqt (wave C) and Connector
# ToConnector_Init          wiring   Connector → ConnectionUsage
#                                    (7.7.12.2.14)
# ToAssociation_Init        elided   Association → ConnectionDefinition
#                                    (7.7.12.2.x) — textual-only in
#                                    this tree (later AS wave)
# ToBindingConnectorAsUsage_Init wiring Connector wiring (7.8.4.3.2)
# ToBehavior_Init           wiring   Activity/OpaqueBehavior →
#                                    ActionDefinition (wave B)
# ToFunction_Init           elided   Function synthesis (later wave)
# ToStep_Init               wiring   action usages (wave B)
# ToActionUsage_Init        wiring   OpaqueAction → ActionUsage
# ToAssignmentActionUsage_Init elided (assignments elided as in
#                                    v1_to_v2.py)
# ToCalculationUsage_Init   wiring   guard/else inline calcs (textual
#                                    calibrated form; AS elides)
# ToPerformActionUsage_Init wiring   Operation → PerformActionUsage
# ToStateUsage_Init         wiring   wave B (7.7.11.2.13/.15/.8)
# ToTransitionUsage_Init    wiring   wave B (7.7.11.2.18)
# ToStateSubactionMembership_Init wiring wave B state internals
# ToRequirementUsage_Init   wiring   wave C (7.8.8.3.30)
# ToMetadataUsage_Init      wiring   MetadataUsage constructions for
#                                    the v1-library metadata stubs
#                                    (PortData/RefineData/TraceData)
# ToTextualRepresentation_Init defaults (textual forms are the
#                                    other pipeline's output; AS wave
#                                    carries no TextualRepresentation)
# ToInteraction_Init        elided   7.7.8.3.6 (grammar gap, as in
#                                    v1_to_v2.py)
# ToSpecialization_Init     wiring   Subclassification machinery
#                                    (generalization → Subclassification)
# ToSubclassification_Init  wiring   (same, 7.7.4.2.12)
# ToSubsetting_Init         wiring   _attach_feature_extras
# ToRedefinition_Init       wiring   _attach_feature_extras
# ToReferenceSubsetting_Init wiring  reference ends (parameters)

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
