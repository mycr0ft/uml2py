#!/usr/bin/env python
"""End-to-end v1 -> v2 check: build a SysML v1 model with the generated
metaclasses + stereotypes, emit SysML v2 textual notation with the
clean-room mapper, and validate the output with sysmlpy (the
authoritative v2 reader)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen.uml25 as U  # noqa: E402
import gen.sysml as S  # noqa: E402
import v1_to_v2 as M  # noqa: E402

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))


# ---- build a v1 model -------------------------------------------------------
V = U.Package(name="VehicleExample")

wheel = S.Block(name="Wheel")
vehicle = S.Block(name="Vehicle")
car = S.Block(name="Car")

mass = S.ValueType(name="Kilogram")
color = U.Enumeration(name="VehicleColor")
for lit in ("red", "green", "blue"):
    color.ownedLiteral.append(U.EnumerationLiteral(name=lit))

wheels = U.Property(name="wheels")
wheels.type = wheel
wheels.aggregation = U.AggregationKind.composite
uv = U.LiteralUnlimitedNatural()
uv.value = U.UnlimitedNatural("4")
wheels.upperValue = uv

mass_attr = U.Property(name="mass")
mass_attr.type = mass

paint = U.Property(name="paint")
paint.type = color

vehicle.add("ownedAttribute", wheels)
vehicle.add("ownedAttribute", mass_attr)
vehicle.add("ownedAttribute", paint)

gen = U.Generalization()
gen.general = vehicle
car.add("generalization", gen)

req = S.Requirement(name="CarIsVehicle")
req.text = "A car shall be a specialization of vehicle."
req.id = "R-1"
rc = U.Comment(body="derived from R-1")
req.add("ownedComment", rc)

sat = S.Satisfy(name="CarSatisfiesR1")
sat.client = [car]
sat.supplier = [req]

for el in (wheel, vehicle, mass, color, car, req, sat):
    V.add("packagedElement", el)

# ---- emit and validate ------------------------------------------------------
text = M.emit_v2(V)
print("---- emitted SysML v2 ----")
print(text)
print("--------------------------")

counts = M.validate_with_sysmlpy(text)
print("sysmlpy counts:", counts)

check("sysmlpy parses emitted v2", isinstance(counts, dict) and len(counts) >= 3)
check("two part definitions (Vehicle, Wheel, Car -> >=2)",
      counts.get("part", 0) >= 2, str(counts.get("part")))
check("requirement carried", counts.get("requirement", 0) >= 1)
check("enumeration carried", counts.get("enumeration", 0) >= 1)
check("attribute carried", counts.get("attribute", 0) >= 1)

# ---- honesty: unmapped features refuse to guess -----------------------------
orphan = U.Package(name="Orphan")
orphan.add("packagedElement", U.Activity(name="AnActivity"))
try:
    M.emit_v2(orphan)
    check("UnmappedFeature raised for unmapped Activity", False)
except M.UnmappedFeature as e:
    check("UnmappedFeature raised for unmapped Activity", "Activity" in str(e), str(e))

print()
print(f"RESULT: {len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)

# keep the emitted v2 for inspection
out = Path(__file__).resolve().parent / "vehicle_example_v2.sysml"
out.write_text(text + "\n")
print(f"(wrote {out.name})")