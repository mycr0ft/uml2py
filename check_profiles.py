#!/usr/bin/env python
"""Checks for the generated profile modules (StandardProfile + SysML v1)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen.uml25 as U  # noqa: E402
import gen.standard_profile as SP  # noqa: E402
import gen.sysml as S  # noqa: E402

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))


def raises(fn, exc):
    try:
        fn()
        return False
    except exc:
        return True


print("== counts / separation ==")
check("33 StandardProfile stereotypes", len(SP._STEREOTYPES) == 33)
check("56 SysML v1 stereotypes", len(S._STEREOTYPES) == 56)
check("no cross-profile shadowing (Trace distinct)",
      SP.Trace is not S.Trace and SP.Trace._STEREO.startswith("StandardProfile")
      and S.Trace._STEREO.startswith("SysML"))

print("== stereotype folding (Block extends Class) ==")
b = S.Block(name="B")
check("Block is a UML Class", isinstance(b, U.Class))
check("Block extension metadata", S._EXTENSIONS["Block"] == (("Class", False),))
b.isEncapsulated = True
check("tagged value isEncapsulated settable", b.isEncapsulated is True)
check("tagged type metadata is bool", S.Block._DECL["isEncapsulated"].t is bool)
check("metaclass unions still work on stereotype instance",
      isinstance(b, U.Class) and b.ownedAttribute == [])

print("== SysML v1 hierarchy ==")
r = S.Requirement(name="req1")
check("Requirement folds Class + AbstractRequirement",
      isinstance(r, U.Class)
      and any(k.__name__ == "AbstractRequirement" for k in type(r).__mro__))
check("text/id inherited from AbstractRequirement",
      "text" in S.AbstractRequirement._DECL and "id" in S.AbstractRequirement._DECL)
r.text = "shall track targets"
r.id = "R-1"
check("requirement text/id settable", r.text == "shall track targets" and r.id == "R-1")
fp = S.FullPort()
check("FullPort extends U.Port (per 20240101 serialization)",
      isinstance(fp, U.Port) and S.FullPort._BASE_METACLASSES == ("Port",))
check("ValueType extends U.DataType (not Class in UML 2.5)",
      isinstance(S.ValueType(), U.DataType)
      and not isinstance(S.ValueType(), U.Class))
check("ConstraintBlock extends Class with spec text",
      isinstance(S.ConstraintBlock(), U.Class)
      and "Cannot be expressed in OCL" in S.ConstraintBlock.CONSTRAINTS[0][1])
check("FlowProperty direction uses FlowDirectionKind enum",
      S.FlowProperty._DECL["direction"].t is S.FlowDirectionKind)
check("abstract stereotype guarded",
      raises(S.DirectedRelationshipPropertyPath, TypeError))
check("abstract stereotypes flagged",
      sum(1 for c in S._STEREOTYPES if c._ABSTRACT) >= 1)

print("== StandardProfile ==")
check("Derive extends Abstraction", issubclass(SP.Derive, U.Abstraction))
check("Document specializes File", issubclass(SP.Document, SP.File))
check("Metaclass extends Class", issubclass(SP.Metaclass, U.Class))

print("== profile constraints carried ==")
n_cons = sum(len(c.CONSTRAINTS) for c in S._STEREOTYPES
             if "CONSTRAINTS" in c.__dict__)
check("SysML profile constraints carried as metadata", n_cons >= 100, f"{n_cons}")

print()
print(f"RESULT: {len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)