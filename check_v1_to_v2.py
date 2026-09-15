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

# ---- wave 3: FullPort/ProxyPort, FlowProperty, constraints, instances -------
W3 = U.Package(name="Wave3")

ctrl = S.Block(name="Controller")
motor_if = S.InterfaceBlock(name="MotorIf")
full = S.FullPort(name="fullPort")
full.type = motor_if
ctrl.add("ownedAttribute", full)
proxy = S.ProxyPort(name="proxyPort")
ctrl.add("ownedAttribute", proxy)
W3.add("packagedElement", ctrl)

# FlowProperty: typed by DataType / untyped / typed by Class
fp_out = S.FlowProperty(name="torque")
fp_out.type = mass
fp_out.direction = S.FlowDirectionKind.out
ctrl.add("ownedAttribute", fp_out)
fp_in = S.FlowProperty(name="flowIn")
fp_in.direction = S.FlowDirectionKind.in_
ctrl.add("ownedAttribute", fp_in)
fp_ref = S.FlowProperty(name="flowRef")
fp_ref.type = axle
fp_ref.direction = S.FlowDirectionKind.inout
ctrl.add("ownedAttribute", fp_ref)

# ConstraintBlock internals: 'in attribute' params + ownedRule constraint
adder = S.ConstraintBlock(name="Adder")
for pname in ("a", "b", "c"):
    pp_ = U.Property(name=pname)
    pp_.type = mass
    adder.add("ownedAttribute", pp_)
sumc = U.Constraint(name="sumCheck")
oe = U.OpaqueExpression()
oe._vals["language"] = ["OCL2.0"]
oe._vals["body"] = ["c == a + b"]
sumc.specification = oe
adder.add("ownedRule", sumc)
W3.add("packagedElement", adder)

# InstanceSpecification: part usage w/ slot values (gold example)
b1 = S.Block(name="Block1")
bval = U.Property(name="massValue")
bval.type = mass
b1.add("ownedAttribute", bval)
inst1 = U.InstanceSpecification(name="inst1")
inst1.classifier.append(b1)
sl = U.Slot()
sl.definingFeature = bval
ls_ = U.LiteralString()
ls_._vals["value"] = "Hello InstanceSpecification"
sl.value.append(ls_)
inst1.add("slot", sl)
W3.add("packagedElement", b1)
W3.add("packagedElement", inst1)

# InstanceValue default -> feature reference (gold 'part pv : B1 = inst1;')
holder = S.Block(name="Holder")
pv = U.Property(name="pv")
pv.type = b1
iv = U.InstanceValue()
iv.instance = inst1
pv.defaultValue = iv
holder.add("ownedAttribute", pv)
W3.add("packagedElement", holder)

# link InstanceSpecification -> ConnectionUsage 'connect a to b'
b2 = S.Block(name="Block2")
assoc_d = U.Association(name="AssocD")
end1 = U.Property(name="e1"); end1.type = b1
end2 = U.Property(name="e2"); end2.type = b2
assoc_d.add("ownedEnd", end1)
assoc_d.add("ownedEnd", end2)
assoc_d.memberEnd = [end1, end2]
inst2 = U.InstanceSpecification(name="inst2")
inst2.classifier.append(b2)
link1 = U.InstanceSpecification(name="link1")
link1.classifier.append(assoc_d)
sl1 = U.Slot(); sl1.definingFeature = end1
iv1 = U.InstanceValue(); iv1.instance = inst1
sl1.value.append(iv1)
sl2 = U.Slot(); sl2.definingFeature = end2
iv2 = U.InstanceValue(); iv2.instance = inst2
sl2.value.append(iv2)
link1.add("slot", sl1)
link1.add("slot", sl2)
W3.add("packagedElement", b2)
W3.add("packagedElement", assoc_d)
W3.add("packagedElement", inst2)
W3.add("packagedElement", link1)

# Interaction -> elision with inventory; standalone unmapped elements
ix = U.Interaction(name="Comm")
ll1 = U.Lifeline(name="carL")
ll2 = U.Lifeline(name="opL")
ix.add("lifeline", ll1)
ix.add("lifeline", ll2)
msg = U.Message(name="m1")
mos1 = U.MessageOccurrenceSpecification(name="s1")
mos1.covered = ll1
mos2 = U.MessageOccurrenceSpecification(name="s2")
mos2.covered = ll2
msg.sendEvent = mos1
msg.receiveEvent = mos2
ix.add("message", msg)
W3.add("packagedElement", ix)
W3.add("packagedElement", U.StateInvariant(name="inv1"))
W3.add("packagedElement", U.InteractionUse(name="useBase"))
aes = U.ActionExecutionSpecification(name="exec1")
W3.add("packagedElement", aes)

text3 = M.emit_v2(W3)
print("---- emitted SysML v2 (wave 3) ----")
print(text3)
print("----------------------------------")
counts3 = M.validate_with_sysmlpy(text3)
print("sysmlpy counts (wave 3):", counts3)

check("sysmlpy parses wave 3", isinstance(counts3, dict) and len(counts3) >= 2)
for label, needle in (
        ("FullPort -> part usage with PortData metadata",
         "part fullPort : MotorIf {@PortData {isFullPort = true;}}"),
        ("PortData metadata stub emitted", "metadata def PortData"),
        ("ProxyPort emitted with not-mapped comment",
         "/* v1 ProxyPort has no normative mapping"),
        ("FlowProperty out -> directed attribute",
         "out attribute torque : Kilogram;"),
        ("untyped FlowProperty in -> directed reference", "in flowIn;"),
        ("FlowProperty inout -> directed ref occurrence",
         "inout ref occurrence flowRef : Axle;"),
        ("constraint params as 'in attribute'", "in attribute a : Kilogram;"),
        ("ownedRule -> nested constraint w/ language",
         'language "OCL2.0"'),
        ("ownedRule constraint body comment", "/* c == a + b */"),
        ("instance spec -> part usage", "part inst1 : Block1 {"),
        ("slot -> redefines with literal",
         'redefines massValue = "Hello InstanceSpecification";'),
        ("InstanceValue default -> feature reference",
         "part pv : Block1 = inst1;"),
        ("link instance -> connection usage",
         "connection link1 : AssocD connect inst1 to inst2;"),
        ("Interaction elision comment", "/* v1 Interaction 'Comm' elided"),
        ("StateInvariant elision comment", "/* v1 StateInvariant 'inv1' elided"),
        ("ActionExecutionSpecification -> action usage", "action exec1;")):
    check(label, needle in text3, needle)

print()

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
out3 = Path(__file__).resolve().parent / "wave3_example_v2.sysml"
out3.write_text(text3 + "\n")
print(f"(wrote {out3.name})")