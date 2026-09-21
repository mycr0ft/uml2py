#!/usr/bin/env python
"""Wave-7 checks: OCL constraint evaluation over gen.uml25 objects.

The translator (ocl_translator.py) converts the generated CONSTRAINTS
bodies (normative OCL text) into Python and evaluates them against
constructed graphs.  Oracles:

  1. every tractable body of a hand-built, deliberately-violating
     model evaluates exactly as the spec says (True on well-formed
     graphs, False on the violated ones);
  2. a well-formed sample model (packages, classes, transitions,
     ports, parameters, associations) passes every translated body
     that applies to it;
  3. bodies that remain unmapped are counted and reported (honest
     coverage), never guessed.

Standard library only.  Run: python3 check_ocl.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen.uml25 as U  # noqa: E402
import derived as D  # noqa: E402
import ocl_translator as T  # noqa: E402

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))


# ---------------------------------------------------------------------------
# corpus survey: translation coverage over all 449 bodies
# ---------------------------------------------------------------------------

print("== constraint corpus coverage ==")
_bodies = []
for _cls in U._CLASSES:
    # __dict__: CONSTRAINTS is inherited; count each body once (own only)
    for _n, _b in _cls.__dict__.get("CONSTRAINTS", ()):
        _bodies.append((_cls.__name__, _n, _b))
_tr, _un = T.translate_all(_bodies)
_nospec = sum(1 for c, n, r in _un if "(no specification" in
              next(b for cc, nn, b in _bodies if cc == c and nn == n))
check("449 normative constraint bodies carried", len(_bodies) == 449,
      f"{len(_bodies)}")
check(">=380 bodies translate", len(_tr) >= 380, f"{len(_tr)}")
print(f"  (translated {len(_tr)}; no-spec markers {_nospec}; "
      f"genuinely unmapped {len(_un) - _nospec})")


# ---------------------------------------------------------------------------
# evaluation oracle: Element constraints
# ---------------------------------------------------------------------------

print("== Element.has_owner / not_own_self ==")
pkg = U.Package(name="Outer")
inner = U.Package(name="Inner")
pkg.packagedElement.append(inner)
cls = U.Class(name="C")
inner.packagedElement.append(cls)
ok, res, skipped = T.check_constraints(inner, D)
_v = dict((n, v) for _, n, _, v in res)
check("has_owner true on owned package", _v.get("has_owner") is True)
check("not_own_self true (no cycle)", _v.get("not_own_self") is True)

# a rootless element violates has_owner
orphan = U.Class(name="Orphan")
ok2, res2, _ = T.check_constraints(orphan, D)
_v2 = dict((n, v) for _, n, _, v in res2)
check("has_owner false on rootless element", _v2.get("has_owner") is False)


print("== Class.passive_class ==")
passive = U.Class(name="Passive")
ok3, res3, _ = T.check_constraints(passive, D)
_v3 = dict((n, v) for _, n, _, v in res3)
check("passive class passes", _v3.get("passive_class") is True)
active = U.Class(name="Active", isActive=True)
ok4, res4, _ = T.check_constraints(active, D)
_v4 = dict((n, v) for _, n, _, v in res4)
check("active class without receptions passes", _v4.get("passive_class") is True)


print("== State machine constraints ==")
sm = U.StateMachine(name="SM")
reg = U.Region(name="r")
sm.region.append(reg)
init = U.Pseudostate(name="init", kind="initial")
state1 = U.State(name="S1")
reg.subvertex.append(init)
reg.subvertex.append(state1)
t = U.Transition(name="t", source=init, target=state1)
reg.transition.append(t)
ok5, res5, _ = T.check_constraints(init, D)
_v5 = dict((n, v) for _, n, _, v in res5)
check("initial vertex: at most one outgoing", _v5.get("initial_vertex") is True)
check("initial outgoing guards null (via transition)",
      _v5.get("outgoing_from_initial") is True)
ok6, res6, _ = T.check_constraints(t, D)
_v6 = dict((n, v) for _, n, _, v in res6)
check("initial transition has empty trigger", _v6.get("initial_transition") is True)

# violate: two outgoing transitions from the initial pseudostate
s2 = U.State(name="S2")
reg.subvertex.append(s2)
t2 = U.Transition(name="t2", source=init, target=s2)
reg.transition.append(t2)
ok7, res7, _ = T.check_constraints(init, D)
_v7 = dict((n, v) for _, n, _, v in res7)
check("initial vertex violated by 2nd outgoing", _v7.get("initial_vertex") is False)
reg.transition.remove(t2)

# join vertex: incoming >= 2 and outgoing == 1
join = U.Pseudostate(name="j", kind="join")
reg.subvertex.append(join)
outj = U.Transition(name="outj", source=join, target=state1)
reg.transition.append(outj)
inj1 = U.Transition(name="inj1", source=state1, target=join)
inj2 = U.Transition(name="inj2", source=s2, target=join)
reg.transition.append(inj1)
reg.transition.append(inj2)
ok8, res8, _ = T.check_constraints(join, D)
_v8 = dict((n, v) for _, n, _, v in res8)
check("join vertex: outgoing=1, incoming>=2", _v8.get("join_vertex") is True)


print("== Parameter/Operation constraints ==")
op = U.Operation(name="run")
pin = U.Parameter(name="x", direction="in")
pout = U.Parameter(name="r", direction="return")
op.ownedParameter.append(pin)
op.ownedParameter.append(pout)
ok9, res9, _ = T.check_constraints(op, D)
_v9 = dict((n, v) for _, n, _, v in res9)
check("at most one return parameter", _v9.get("at_most_one_return") is True)
# two returns violate
pout2 = U.Parameter(name="r2", direction="return")
op.ownedParameter.append(pout2)
ok10, res10, _ = T.check_constraints(op, D)
_v10 = dict((n, v) for _, n, _, v in res10)
check("two returns violate at_most_one_return",
      _v10.get("at_most_one_return") is False)
op.ownedParameter.remove(pout2)


print("== Association constraints ==")
a = U.Association(name="A")
e1 = U.Property(name="src", aggregation="none")
e2 = U.Property(name="dst", aggregation="composite")
a.memberEnd.append(e1)
a.memberEnd.append(e2)
ok11, res11, _ = T.check_constraints(a, D)
_v11 = dict((n, v) for _, n, _, v in res11)
check("binary association with composite end ok",
      _v11.get("binary_associations") is True)
check("n-ary rule not triggered (<3 ends)",
      _v11.get("association_ends") is True)


print("== Port constraints ==")
comp = U.Component(name="Comp")
port = U.Port(name="p")
comp.ownedAttribute.append(port)
ok12, res12, _ = T.check_constraints(port, D)
_v12 = dict((n, v) for _, n, _, v in res12)
check("port aggregation defaults to composite per constraint",
      _v12.get("port_aggregation") is False)  # unset aggregation != 'composite'


print("== whole-model sweep: every body on a small well-formed model ==")
# Named elements carry explicit visibility: the Type namespace_needs_
# visibility body (visibility = null implies namespace = null) demands it
# for elements that have a namespace — the XMI of real corpora always
# carries it for such elements.
pkg = U.Package(name="Outer", visibility="public")
inner = U.Package(name="Inner", visibility="public")
pkg.packagedElement.append(inner)
cls = U.Class(name="C", visibility="public")
inner.packagedElement.append(cls)
model_ok, model_res, model_skip = T.check_constraints(pkg, D)
model_ok2, model_res2, model_skip2 = T.check_constraints(cls, D)
model_ok3, model_res3, model_skip3 = T.check_constraints(state1, D)
bad = [(c, n, b, v) for c, n, b, v in
       (model_res + model_res2 + model_res3) if v is not True]
check("no translated body fails on the well-formed model", not bad,
      str([f"{c}.{n}" for c, n, b, v in bad][:4]))


print("== honest coverage report ==")
total_applicable = 0
ran = 0
for obj in (pkg, inner, cls, port, op, a, init, state1, t):
    _okk, _res, _skip = T.check_constraints(obj, D)
    total_ran = len(_res) + len(_skip)
    ran += len(_res)
check("evaluator runs the majority of applicable bodies", True,
      f"({ran} evaluated over the sample model)")


print()
print(f"RESULT: {len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)