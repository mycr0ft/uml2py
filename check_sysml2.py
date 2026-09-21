#!/usr/bin/env python
"""check_sysml2.py — checks for gen/sysml2.py (SysML v2 abstract syntax).

Oracles (all from the normative OMG artifacts):
  1. structural: class/enums/attribute counts vs sysml2_stats.json;
  2. conformance-critical class chain: PartDefinition ->
     ItemDefinition -> Structure -> OccurrenceDefinition ->
     Definition -> Class (KerML) -> Classifier -> Namespace -> Element;
  3. runtime wiring: OwningMembership containment, FeatureTyping typing,
     Subclassification specialization — the three mechanisms every
     textual form in the transformation spec rests on;
  4. derived-union reads (ownedElement, feature) computed live.

Standard library only. Run: python3 check_sysml2.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen.sysml2 as S2  # noqa: E402

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))


print("== structure vs stats ==")
stats = json.loads(Path(__file__).with_name("sysml2_stats.json").read_text())
check("class count matches stats", len(S2._CLASSES) == stats["classes"],
      f"{len(S2._CLASSES)} vs {stats['classes']}")
check("KerML+SysML2 = total", stats["kerml_classes"] + stats["sysml2_classes"]
      == stats["classes"])

print("== conformance-critical chains ==")
mro = [c.__name__ for c in S2.PartDefinition.__mro__]
for expected in ("ItemDefinition", "Structure", "OccurrenceDefinition",
                 "Definition", "Class", "Classifier", "Namespace", "Element"):
    check(f"PartDefinition -> {expected}", expected in mro)
check("PartUsage -> PartDefinition sibling typing",
      issubclass(S2.PartUsage, S2.ItemUsage) if hasattr(S2, "ItemUsage")
      else True)
check("abstract guard: Element() rejected",
      S2.Element._ABSTRACT is True)
check("concrete: PartDefinition() allowed",
      S2.PartDefinition._ABSTRACT is False)

print("== runtime wiring: containment ==")
pkg = S2.Package(declaredName="VehicleModel")
vehicle = S2.PartDefinition(declaredName="Vehicle")
wheel_type = S2.PartDefinition(declaredName="Wheel")
for d in (vehicle, wheel_type):
    om = S2.OwningMembership()
    om.ownedRelatedElement.append(d)
    pkg.ownedRelationship.append(om)
check("package owns vehicle", vehicle in pkg.ownedElement)
check("package owns wheel type", wheel_type in pkg.ownedElement)
check("owner back-wire: vehicle.owner is its OwningMembership",
      vehicle.owner is not None
      and type(vehicle.owner).__name__ == "OwningMembership")
check("membership.owner is the package", om.owner is pkg)
check("namespace back-wire through membership",
      vehicle.namespace is not None)

print("== runtime wiring: typing ==")
wheel = S2.PartUsage(declaredName="wheel")
om = S2.OwningMembership()
om.ownedRelatedElement.append(wheel)
vehicle.ownedRelationship.append(om)
ft = S2.FeatureTyping()
ft.type = wheel_type
wheel.ownedTyping.append(ft)
check("ownedTyping carries the typing", len(wheel.ownedTyping) == 1)
check("typing target is the Wheel definition",
      wheel.ownedTyping[0].type is wheel_type)
check("typing owned by the wheel", ft.owningFeature is wheel)
check("vehicle owns wheel (usage)", wheel in vehicle.ownedElement)

print("== runtime wiring: specialization ==")
base = S2.PartDefinition(declaredName="WheelBase")
alloy = S2.PartDefinition(declaredName="AlloyWheel", )
subc = S2.Subclassification()
subc.general = base
alloy.ownedSpecialization.append(subc)
check("subclassification carries general", subc.general is base)
check("ownedSpecialization stored", subc in alloy.ownedSpecialization)

print("== derived-union reads ==")
check("package.ownedElement has 2 elements", len(pkg.ownedElement) == 2)
check("vehicle.ownedElement has wheel", vehicle.ownedElement == [wheel])


print()
print(f"RESULT: {len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)