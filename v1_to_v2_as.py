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


def transform_v1_element(el):
    """Dispatch on v1 metaclass: build the v2 AS object per the
    normative mapping. Returns the v2 element (not yet owned)."""
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
        # mappings (behaviors, state machines, use cases, signals,
        # ports/requirements machinery) are later waves — not guesses.
        if isinstance(el, (U.Behavior, U.UseCase, U.Signal,
                           U.InformationItem, U.Interface,
                           S.TestCase, S.Requirement, S.InterfaceBlock)):
            raise UnmappedFeature(
                f"{type(el).__name__} (own mapping, later wave)")
        return S2.OccurrenceDefinition(declaredName=_name(el))
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
    # conformance-critical identity: every reference resolves to it)
    for el in list(pkg.ownedMember):
        v2 = transform_v1_element(el)
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
        if isinstance(el, U.Class):
            _populate_class(el, v2, index, pending_generalizations)

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
