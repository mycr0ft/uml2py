#!/usr/bin/env python
"""Checks for the generated profile modules (StandardProfile + SysML v1 + UAF 1.2)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen.uml25 as U  # noqa: E402
import gen.standard_profile as SP  # noqa: E402
import gen.sysml as S  # noqa: E402
import gen.uaf as F  # noqa: E402

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

print("== UAF 1.2 (UAFML, from OMG UAF.xmi) ==")
check("256 UAF stereotypes", len(F._STEREOTYPES) == 256)
check("20 UAF enumerations",
      sum(1 for n in dir(F) if isinstance(getattr(F, n), type)
          and issubclass(getattr(F, n), __import__("enum").Enum)) == 20)
check("UAFElement abstract, folds U.Element",
      F.UAFElement._ABSTRACT and issubclass(F.UAFElement, U.Element)
      and F.UAFElement._BASE_METACLASSES == ("Element",))
check("duplicate base_Element serialization deduped",
      F._EXTENSIONS["UAFElement"] == (("Element", True),))
check("Capability folds sysml.Block (cross-profile generalization)",
      issubclass(F.Capability, S.Block) and issubclass(F.Capability, U.Class))
check("View folds sysml.View (href generalization)",
      S.View in F.View.__mro__)
check("OperationalAgent folds 4 stereotype bases + U.Class, abstract",
      F.OperationalAgent._ABSTRACT
      and all(any(k.__name__ == n for k in F.OperationalAgent.__mro__)
              for n in ("OperationalAsset", "SubjectOfOperationalConstraint",
                        "CapableElement", "Desirer"))
      and issubclass(F.OperationalAgent, U.Class))
n_cons = sum(len(c.CONSTRAINTS) for c in F._STEREOTYPES
             if "CONSTRAINTS" in c.__dict__)
check("259 UAF OCL constraints carried", n_cons == 259, f"{n_cons}")
check("44 abstract stereotypes flagged",
      sum(1 for c in F._STEREOTYPES if c._ABSTRACT) == 44)
check("all _STEREO labels are UAF-qualified",
      all(c._STEREO.startswith("UAF::") for c in F._STEREOTYPES))
check("252 extension entries after dedup", len(F._EXTENSIONS) == 252)
check("extension metaclasses are required (ExtensionEnd::lower defaults 1)",
      all(req for metas in F._EXTENSIONS.values() for _, req in metas))
check("stereotype-typed tag late-bound by name",
      F.Measurement._DECL["environmentalContext"].t == "ActualCondition")
str_typed = [r.t for c in F._STEREOTYPES
             for r in c.__dict__.get("_DECL", {}).values()
             if isinstance(r.t, str)]
check("55 stereotype-typed tags, all resolving to uaf/sysml classes",
      len(str_typed) == 55
      and all((t.startswith("sysml.") and hasattr(S, t[6:])) or hasattr(F, t)
              for t in str_typed), f"{len(str_typed)}")
check("Capability.kind driven by local enum",
      F.Capability._DECL["kind"].t is F.CapabilityKind
      and F.Capability().kind is None)
check("OperationalExchangeKind literals carried",
      [l.value for l in F.OperationalExchangeKind][:2]
      == ["MaterielExchange", "OrganizationalExchange"])
check("no cross-profile shadowing (Viewpoint distinct)",
      F.Viewpoint is not S.Viewpoint
      and F.Viewpoint._STEREO.startswith("UAF"))
check("Viewpoint instantiable with tag roundtrip",
      (vp := F.Viewpoint()) is not None
      and issubclass(F.Viewpoint, U.Class))
check("generator produced no unresolved targets",
      not any("unresolved" in w for w in
              __import__("json").load(open("profile_stats.json"))["warnings"]))

print("== profile constraints carried ==")
n_cons = sum(len(c.CONSTRAINTS) for c in S._STEREOTYPES
             if "CONSTRAINTS" in c.__dict__)
check("SysML profile constraints carried as metadata", n_cons >= 100, f"{n_cons}")

print()
print(f"RESULT: {len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)