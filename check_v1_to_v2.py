#!/usr/bin/env python
"""End-to-end v1 -> v2 check (wave 2): builds a SysML v1 model exercising
the structural core + the wave-2 mappings (connections, bindings, ports,
items, actors, occurrences, behaviors/operations, state machines,
verification test cases, requirement relationships, allocations,
use cases), emits SysML v2 textual notation, and validates the output
with sysmlpy (the authoritative v2 reader).

Run under ~/sysmlpy/.venv (needs sysmlpy + pint)."""
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
axle = S.Block(name="Axle")

mass = S.ValueType(name="Kilogram")
color = U.Enumeration(name="VehicleColor")
for lit in ("red", "green", "blue"):
    color.ownedLiteral.append(U.EnumerationLiteral(name=lit))

# parts / attributes on Vehicle
wheels = U.Property(name="wheels")
wheels.type = wheel
wheels.aggregation = U.AggregationKind.composite
uv = U.LiteralUnlimitedNatural()
uv.value = U.UnlimitedNatural("4")
wheels.upperValue = uv
vehicle.add("ownedAttribute", wheels)

mass_attr = U.Property(name="mass")
mass_attr.type = mass
vehicle.add("ownedAttribute", mass_attr)

paint = U.Property(name="paint")
paint.type = color
vehicle.add("ownedAttribute", paint)

# ports: InterfaceBlock + typed/untyped Ports
power_if = S.InterfaceBlock(name="PowerIf")
pwr = U.Port(name="pwr")
pwr.type = power_if
vehicle.add("ownedAttribute", pwr)
free_port = U.Port(name="aux")
vehicle.add("ownedAttribute", free_port)

# connector between parts (normative: Connector -> ConnectionUsage)
p1 = U.Property(name="frontAxle")
p1.type = axle
p1.aggregation = U.AggregationKind.composite
p2 = U.Property(name="rearAxle")
p2.type = axle
p2.aggregation = U.AggregationKind.composite
vehicle.add("ownedAttribute", p1)
vehicle.add("ownedAttribute", p2)
conn = U.Connector(name="axleLink")
cend1 = U.ConnectorEnd(); cend1.role = p1
cend2 = U.ConnectorEnd(); cend2.role = p2
conn.add("end", cend1)
conn.add("end", cend2)
vehicle.add("ownedConnector", conn)

# binding connector
raw_a = U.Property(name="rawA")
raw_a.type = mass
raw_b = U.Property(name="rawB")
raw_b.type = mass
vehicle.add("ownedAttribute", raw_a)
vehicle.add("ownedAttribute", raw_b)
binding = S.BindingConnector(name="massBind")
bend1 = U.ConnectorEnd(); bend1.role = raw_a
bend2 = U.ConnectorEnd(); bend2.role = raw_b
binding.add("end", bend1)
binding.add("end", bend2)
vehicle.add("ownedConnector", binding)

# operation with parameters (normative: Operation -> PerformActionUsage)
op = U.Operation(name="totalMass")
par_in = U.Parameter(name="extra"); par_in.direction = U.ParameterDirectionKind.in_
par_in.type = mass
par_out = U.Parameter(name="result"); par_out.direction = U.ParameterDirectionKind.return_
op.add("ownedParameter", par_in)
op.add("ownedParameter", par_out)
vehicle.add("ownedOperation", op)

# association (normative: -> ConnectionDefinition with ends)
assoc = U.Association(name="WheelToAxle")
e1 = U.Property(name="wheelEnd"); e1.type = wheel
e2 = U.Property(name="axleEnd"); e2.type = axle
assoc.add("ownedEnd", e1)
assoc.add("ownedEnd", e2)
assoc.memberEnd = [e1, e2]

# actor (normative: Actor -> PartDefinition)
actor = U.Actor(name="Operator")

# signal + item-typed property (normative: Signal -> ItemDefinition)
cmd = U.Signal(name="MoveCommand")

# plain class + occurrence-typed property (OccurrenceDefinition/Usage)
legacy = U.Class(name="LegacyPart")
occ_ref = U.Property(name="legacy")
occ_ref.type = legacy
vehicle.add("ownedAttribute", occ_ref)

# state machine w/ initial state, 2 states, transition
sm = U.StateMachine(name="OpMode")
reg = U.Region(name="r1")
st_on = U.State(name="on")
st_off = U.State(name="off")
trans = U.Transition(name="t1")
reg.add("subvertex", st_on)
reg.add("subvertex", st_off)
trans.source = st_on
trans.target = st_off
reg.add("transition", trans)
sm.add("region", reg)

# activity (normative: Activity -> ActionDefinition w/ parameters)
act = U.Activity(name="Generate")
ap = U.Parameter(name="demand")
ap.direction = U.ParameterDirectionKind.in_
act.add("ownedParameter", ap)

# test case + verify (normative: TestCase -> verification def, Verify ->
# RequirementVerificationMembership inside its objective)
tc = S.TestCase(name="CheckMass")
req = S.Requirement(name="CarIsVehicle")
req.text = "A car shall be a specialization of vehicle."
req.id = "R-1"
ver = S.Verify(name="verifyCar")
ver.client = [tc]
ver.supplier = [req]

# derived requirement (normative: DeriveReqt -> Derivation connection)
derived_req = S.Requirement(name="DerivedReq")
dr = S.DeriveReqt(name="derives")
dr.client = [derived_req]
dr.supplier = [req]

# refine (normative: Refine -> annotated Dependency)
refined = U.Dependency(name="refinesVeh")
refined.client = [vehicle]
refined.supplier = [req]
refine = S.Refine(name="refineTag")
refine.client = [vehicle]
refine.supplier = [req]

# plain dependency
dep = U.Dependency(name="usesLegacy")
dep.client = [vehicle]
dep.supplier = [legacy]

# allocation between part usages (normative: AllocationUsage)
alloc_target = U.Property(name="spareWheel")
alloc_target.type = wheel
car.add("ownedAttribute", alloc_target)
alloc = S.Allocate(name="allocWheel")
alloc.client = [wheels]
alloc.supplier = [alloc_target]

# use case with include
uc_main = U.UseCase(name="OperateVehicle")
uc_sub = U.UseCase(name="StartEngine")
inc = U.Include()
inc.addition = uc_sub
uc_main.add("include", inc)

# package import (elided: target grammar has no import)
P_q = U.Package(name="Common")
pimport = U.PackageImport()
pimport.importedPackage = P_q
V.add("packageImport", pimport)

for el in (P_q, wheel, vehicle, axle, mass, color, power_if, legacy, cmd,
           actor, sm, act, uc_main, uc_sub, car, req, derived_req,
           assoc, tc, ver, dr, refine, refined, dep, alloc, pimport):
    V.add("packagedElement", el)

# ---- emit and validate ------------------------------------------------------
text = M.emit_v2(V)
print("---- emitted SysML v2 ----")
print(text)
print("--------------------------")

counts = M.validate_with_sysmlpy(text)
print("sysmlpy counts:", counts)

check("sysmlpy parses emitted v2", isinstance(counts, dict) and len(counts) >= 5)
for label, key, minimum in (
        ("part definitions", "part", 3),          # Wheel, Vehicle, Axle, Car, Operator
        ("attributes", "attribute", 1),           # mass
        ("requirement", "requirement", 1),
        ("connection defs", "connection", 1),     # WheelToAxle + connection usage
        ("typed port", "port", 1),                # pwr (untyped aux counts as part)
        ("items", "item", 1),                     # MoveCommand
        ("verification def", "verification", 1),  # CheckMass
        ("allocation", "allocation", 1),
        ("state", "state", 1),                    # state def OpMode
        ("action def", "action", 1),              # Generate
        ("use case", "use_case", 1),
        ("dependency", "dependency", 2),          # refinesVeh + usesLegacy
        ("metadata", "metadata", 1),              # RefineData stub
        ("occurrence", "part", 3)):               # occurrence def LegacyPart
    check(label, counts.get(key, 0) >= minimum, str(counts))

# ---- honesty: unmapped features refuse to guess -----------------------------
orphan = U.Package(name="Orphan")
orphan.add("packagedElement", U.Message(name="SomeMessage"))
try:
    M.emit_v2(orphan)
    check("UnmappedFeature raised for unmapped Message", False)
except M.UnmappedFeature as e:
    check("UnmappedFeature raised for unmapped Message", "Message" in str(e), str(e))

print()
print(f"RESULT: {len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)

out = Path(__file__).resolve().parent / "vehicle_example_v2.sysml"
out.write_text(text + "\n")
print(f"(wrote {out.name})")