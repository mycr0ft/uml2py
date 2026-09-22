#!/usr/bin/env python
"""check_v1_to_v2_as.py — checks for v1_to_v2_as.py, the R3 leg of the
SysML v1 -> v2 transformation conformance chain:

  R1  xmi21.py / mdzip_import.py read SysML v1 XMI into gen.uml25 +
      gen.sysml objects (abstract-syntax representation of the input);
  R3  v1_to_v2_as.py transforms those objects into gen.sysml2 objects
      (abstract-syntax representation of the output) per ptc/2025-04-07;
  R2  gen/sysml2.py IS the normative SysML v2 abstract syntax (from the
      OMG CMOF XMI) and provides the runtime the transformed graph
      lives in (check_sysml2.py covers it).

Oracles here:
  1. R1 leg: a hand-written v1 XMI 2.1 file (UML-20090901 dialect, the
     DoDAFLibrary.xmi spelling) is read with xmi21 and transformed —
     file -> R1 objects -> R3 -> R2 AS graph, end to end.
  2. R3 mappings: each wave-A normative mapping checked against the
     transformation spec (ptc/2025-04-07) anchors, including the
     identity rule (one v1 element = one AS object; usages type-
     reference the SAME definition object, never a copy).
  3. Parity: the AS graph re-renders to the same textual notation the
     independently-validated textual pipeline (v1_to_v2.py, checked by
     check_v1_to_v2.py with sysmlpy) emits for the same model.
  4. Honesty: UnmappedFeature for everything without a normative
     mapping — never a guess.

Needs lxml (the R1 reader); everything else stdlib.
Run: python3 check_v1_to_v2_as.py
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen.uml25 as U  # noqa: E402
import gen.sysml as S  # noqa: E402
import gen.sysml2 as S2  # noqa: E402
import v1_to_v2 as MT  # noqa: E402  (textual pipeline, parity oracle)
import v1_to_v2_as as A  # noqa: E402

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))


def find(root, name, cls=None):
    """All AS objects with declaredName == name (optionally of a class)."""
    hits = []

    def walk(el):
        if getattr(el, "declaredName", None) == name and (
                cls is None or isinstance(el, cls)):
            hits.append(el)
        for r in getattr(el, "ownedRelationship", []):
            for e in r.ownedRelatedElement:
                walk(e)
    walk(root)
    return hits


def typing_of(feature):
    return feature.ownedTyping[0].type if feature.ownedTyping else None


# == 1. R1 leg: v1 XMI file -> gen.uml25 -> transform -> gen.sysml2 ========
print("== R1 leg: v1 XMI -> AS ==")
XMI = """<?xml version="1.0" encoding="UTF-8"?>
<xmi:XMI xmi:version="2.1" xmlns:uml="http://schema.omg.org/spec/UML/2.0"
         xmlns:xmi="http://schema.omg.org/spec/XMI/2.1">
  <uml:Package xmi:id="p1" xmi:type="uml:Package">
    <name>FromXMI</name>
    <packagedElement xmi:type="uml:Class" xmi:id="c_engine">
      <name>Engine</name>
      <ownedAttribute xmi:type="uml:Property" xmi:id="a_rpm">
        <name>rpm</name>
        <type xmi:idref="dt_rpm"/>
      </ownedAttribute>
      <ownedAttribute xmi:type="uml:Property" xmi:id="a_piston">
        <name>piston</name>
        <type xmi:idref="c_piston"/>
        <aggregation>composite</aggregation>
      </ownedAttribute>
    </packagedElement>
    <packagedElement xmi:type="uml:Class" xmi:id="c_piston">
      <name>Piston</name>
      <generalization xmi:type="uml:Generalization" xmi:id="g1">
        <general xmi:idref="c_part"/>
      </generalization>
    </packagedElement>
    <packagedElement xmi:type="uml:Class" xmi:id="c_part">
      <name>Part</name>
    </packagedElement>
    <packagedElement xmi:type="uml:DataType" xmi:id="dt_rpm">
      <name>RPM</name>
    </packagedElement>
    <packagedElement xmi:type="uml:Enumeration" xmi:id="e_state">
      <name>EngineState</name>
      <ownedLiteral xmi:type="uml:EnumerationLiteral" xmi:id="l_off"><name>off</name></ownedLiteral>
      <ownedLiteral xmi:type="uml:EnumerationLiteral" xmi:id="l_on"><name>on</name></ownedLiteral>
    </packagedElement>
  </uml:Package>
</xmi:XMI>
"""
with tempfile.NamedTemporaryFile("w", suffix=".xmi", delete=False) as fp:
    fp.write(XMI)
    xmi_path = fp.name
try:
    pkgs = A.transform_xmi(xmi_path)
    check("transform_xmi returns one AS package", len(pkgs) == 1
          and isinstance(pkgs[0], S2.Package))
    as_pkg = pkgs[0]
    check("AS package carries the v1 name", as_pkg.declaredName == "FromXMI")
    eng = find(as_pkg, "Engine", S2.OccurrenceDefinition)
    check("v1 Class -> OccurrenceDefinition (7.7.4.2.37 family)",
          len(eng) == 1)
    piston = find(as_pkg, "Piston", S2.OccurrenceDefinition)[0]
    part = find(as_pkg, "Part", S2.OccurrenceDefinition)[0]
    check("XMI generalization -> Subclassification to the indexed object",
          len(piston.ownedSpecialization) == 1
          and piston.ownedSpecialization[0].general is part)
    rpm = find(as_pkg, "rpm", S2.AttributeUsage)[0]
    check("XMI property typed by DataType -> AttributeUsage typed",
          typing_of(rpm) is find(as_pkg, "RPM", S2.AttributeDefinition)[0])
    pist = find(as_pkg, "piston", S2.OccurrenceUsage)[0]
    check("XMI property typed by Class -> OccurrenceUsage typed",
          typing_of(pist) is piston)
    # R1 dialect honesty: the UML-20090901 reader does not carry the
    # <aggregation> child (XMI 2.1 records it as an unmapped feature),
    # so the AS usage is referential rather than silently composite
    import xmi21  # noqa: E402
    reader = xmi21.read_xmi21(xmi_path)
    check("R1 reader records <aggregation> as unmapped (no silent loss)",
          ("a_piston", "aggregation") in reader.unmapped_features
          and pist._vals.get("isComposite") is False)
    est = find(as_pkg, "EngineState", S2.EnumerationDefinition)[0]
    check("XMI enumeration literals -> EnumerationUsage features",
          [f.declaredName for f in est.feature] == ["off", "on"])
finally:
    Path(xmi_path).unlink()


# == 2. R3 wave-A mappings over a stereotype-carrying v1 model =============
print("== R3 wave-A mappings ==")
V = U.Package(name="Vehicle")
engine = S.Block(name="Engine"); V.add("packagedElement", engine)
piston = S.Block(name="Piston"); V.add("packagedElement", piston)
g = U.Generalization(); g.general = engine
piston.add("generalization", g)
kg = S.ValueType(name="Kilogram"); V.add("packagedElement", kg)
color = U.Enumeration(name="Color")
for lit in ("red", "green"):
    color.ownedLiteral.append(U.EnumerationLiteral(name=lit))
V.add("packagedElement", color)
cb = S.ConstraintBlock(name="Adder"); V.add("packagedElement", cb)
legacy = U.Class(name="Legacy"); V.add("packagedElement", legacy)
actor = U.Actor(name="Operator"); V.add("packagedElement", actor)

pist = U.Property(name="piston"); pist.type = piston
pist.aggregation = U.AggregationKind.composite
engine.add("ownedAttribute", pist)
ref_part = U.Property(name="sibling"); ref_part.type = piston
engine.add("ownedAttribute", ref_part)
mass = U.Property(name="mass"); mass.type = kg
engine.add("ownedAttribute", mass)
paint = U.Property(name="paint"); paint.type = color
engine.add("ownedAttribute", paint)
loose = U.Property(name="loose")
engine.add("ownedAttribute", loose)
leg = U.Property(name="leg"); leg.type = legacy
leg.aggregation = U.AggregationKind.composite
engine.add("ownedAttribute", leg)
leg_ref = U.Property(name="legRef"); leg_ref.type = legacy
engine.add("ownedAttribute", leg_ref)
cm = U.Comment(); cm.body = "the engine block"
engine.add("ownedComment", cm)

as_pkg = A.transform_package(V)

eng_defs = find(as_pkg, "Engine", S2.PartDefinition)
check("Block -> PartDefinition (7.8.4.3.3)", len(eng_defs) == 1)
engine_as = eng_defs[0]
check("one AS definition per v1 Block (index identity)",
      len(find(as_pkg, "Piston", S2.PartDefinition)) == 1)
piston_as = find(as_pkg, "Piston", S2.PartDefinition)[0]

pist_as = find(as_pkg, "piston", S2.PartUsage)[0]
check("composite block-typed Property -> PartUsage (7.8.4.3.13)",
      pist_as._vals.get("isComposite", True) is True)
check("PartUsage types reference the indexed PartDefinition object",
      typing_of(pist_as) is piston_as)
sib_as = find(as_pkg, "sibling", S2.PartUsage)[0]
check("non-composite block-typed Property -> PartUsage isComposite=false"
      " (the 'ref part' form)", sib_as._vals.get("isComposite") is False)
mass_as = find(as_pkg, "mass", S2.AttributeUsage)[0]
check("ValueType -> AttributeDefinition (7.8.4.3.14), usage typed by it",
      typing_of(mass_as) is find(as_pkg, "Kilogram", S2.AttributeDefinition)[0])
paint_as = find(as_pkg, "paint", S2.AttributeUsage)[0]
check("Enumeration -> EnumerationDefinition; typed AttributeUsage",
      typing_of(paint_as) is find(as_pkg, "Color", S2.EnumerationDefinition)[0])
loose_as = find(as_pkg, "loose", S2.Feature)[0]
check("untyped Property -> Feature, no typing", loose_as is not None
      and loose_as.ownedTyping == [])
leg_as = find(as_pkg, "leg", S2.OccurrenceUsage)[0]
check("Class-typed composite Property -> composite OccurrenceUsage"
      " (7.7.4.2.37)", leg_as._vals.get("isComposite", True) is True
      and typing_of(leg_as) is find(as_pkg, "Legacy", S2.OccurrenceDefinition)[0])
legr_as = find(as_pkg, "legRef", S2.OccurrenceUsage)[0]
check("Class-typed referential Property -> OccurrenceUsage"
      " isComposite=false", legr_as._vals.get("isComposite") is False)
cb_as = find(as_pkg, "Adder", S2.ConstraintDefinition)
check("ConstraintBlock -> ConstraintDefinition (7.8.5.3.1)",
      len(cb_as) == 1)
actor_as = find(as_pkg, "Operator", S2.PartDefinition)
check("Actor -> PartDefinition (7.7.13.3.1)", len(actor_as) == 1)
piston_sub = piston_as.ownedSpecialization
check("Generalization -> Subclassification, general = indexed object",
      len(piston_sub) == 1 and piston_sub[0].general is engine_as)
doc = find(as_pkg, None)  # documentation has no name
docs = [e for e in engine_as.ownedElement if isinstance(e, S2.Documentation)]
check("Comment -> Documentation owned by the documented element"
      " (7.4.2.1.9)", len(docs) == 1 and docs[0].body == "the engine block"
      and docs[0] in engine_as.ownedElement)
check("Documentation annotates the engine via an Annotation relationship"
      " (runtime-elided back-ends documented)",
      len(docs) == 1
      and any(isinstance(r, S2.Annotation)
              and r.annotatedElement is engine_as
              for r in docs[0].ownedRelationship))
color_as = find(as_pkg, "Color", S2.EnumerationDefinition)[0]
check("EnumerationLiteral -> EnumerationUsage via FeatureMembership",
      [f.declaredName for f in color_as.feature] == ["red", "green"])

print()
print("== R2 runtime wiring over the transformed graph ==")
check("FeatureMembership makes the definition the featuringType"
      " (owner back-wire)", pist_as.owner is not None
      and type(pist_as.owner).__name__ == "FeatureMembership"
      and pist_as.owner.owner is engine_as)
check("membership chain: pistons reachable via ownedElement",
      pist_as in engine_as.ownedElement)
check("Type.feature (computed runtime): Engine features complete",
      [f.declaredName for f in engine_as.feature]
      == ["piston", "sibling", "mass", "paint", "loose", "leg", "legRef"])
check("FeatureTyping back-wire: typedFeature is the usage",
      pist_as.ownedTyping[0].typedFeature is pist_as
      or pist_as.ownedTyping[0].owningFeature is pist_as)
check("Subclassification owned by the specific definition",
      piston_sub[0].owner is piston_as)

print()
print("== parity with the validated textual pipeline ==")
textual = MT.emit_v2(V)

AS_KW = {"Package": "package", "PartDefinition": "part def",
         "AttributeDefinition": "attribute def",
         "EnumerationDefinition": "enum def",
         "ConstraintDefinition": "constraint def",
         "OccurrenceDefinition": "occurrence def"}


def render_as(el, ind=0):
    pad = "  " * ind
    n = el.declaredName
    if isinstance(el, S2.Documentation):
        body = " ".join((el.body or "").split())
        return ([f"{pad}doc /* {body} */"] if body else [])
    if isinstance(el, S2.EnumerationUsage):
        return [f"{pad}{n};"]          # literal: bare-name form
    if isinstance(el, (S2.PartUsage, S2.AttributeUsage, S2.ReferenceUsage)):
        t = typing_of(el)
        kw = ("part" if isinstance(el, S2.PartUsage) else "attribute")
        if not el._vals.get("isComposite", True):
            kw = "ref " + kw
        line = f"{pad}{kw} {n}" + (f" : {t.declaredName};" if t else ";")
        return [line]
    if isinstance(el, S2.OccurrenceUsage):
        t = typing_of(el)
        kw = "occurrence" if el._vals.get("isComposite", True) \
            else "ref occurrence"
        return [f"{pad}{kw} {n}" + (f" : {t.declaredName};" if t else ";")]
    if isinstance(el, S2.Feature):
        return [f"{pad}{n};"]          # untyped: bare-name feature form
    kw = AS_KW.get(type(el).__name__)
    if kw is None:
        return []                      # runtime-elided: not rendered
    kids = []
    for r in el.ownedRelationship:
        for e in r.ownedRelatedElement:
            kids.append(e)
    supers = [r.general.declaredName
              for r in getattr(el, "ownedSpecialization", ())]
    line = f"{pad}{kw} {n}"
    if supers:
        line += f" :> {', '.join(supers)}"
    if not kids:
        return [line + ";"]
    lines = [line + " {"]
    for k in kids:
        lines += render_as(k, ind + 1)
    lines.append(pad + "}")
    return lines


as_textual = "\n".join(render_as(as_pkg))
print("---- textual pipeline (v1_to_v2.py) ----")
print(textual)
print("---- AS graph rendered ----")
print(as_textual)
print("----------------------------------------")
check("AS graph renders to the same notation the textual pipeline emits",
      as_textual == textual,
      "differences above" if as_textual != textual else "identical")

print()
print("== honesty: unmapped features refuse to guess ==")
orphan = U.Package(name="Orphan")
orphan.add("packagedElement", U.StateMachine(name="SM"))
try:
    A.transform_package(orphan)
    check("UnmappedFeature raised for StateMachine", False)
except A.UnmappedFeature as e:
    check("UnmappedFeature raised for StateMachine", "StateMachine" in str(e),
          str(e))
ext = U.Package(name="Ext")
blk = S.Block(name="B"); ext.add("packagedElement", blk)
other = S.Block(name="Elsewhere")
p2 = U.Property(name="x"); p2.type = other
blk.add("ownedAttribute", p2)
try:
    A.transform_package(ext)
    check("UnmappedFeature raised for external type", False)
except A.UnmappedFeature as e:
    check("UnmappedFeature raised for external type",
          "external" in str(e), str(e))
gen_unnamed = U.Package(name="GU")
b1 = S.Block(name="B1"); gen_unnamed.add("packagedElement", b1)
anon = U.Class()
g2 = U.Generalization(); g2.general = anon
b1.add("generalization", g2)
try:
    A.transform_package(gen_unnamed)
    check("UnmappedFeature raised for unnamed general", False)
except A.UnmappedFeature as e:
    check("UnmappedFeature raised for unnamed general",
          "external/unnamed" in str(e), str(e))

print()
print(f"RESULT: {len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)
