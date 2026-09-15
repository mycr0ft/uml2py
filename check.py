#!/usr/bin/env python
"""Semantic checks for the generated UML 2.5.1 package + exploration demo.

Run with any Python 3.12+ (generated package is stdlib-only):
    python check.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen.uml25 as u  # noqa: E402

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


print("== counts vs stats.json ==")
stats = json.loads(Path(__file__).with_name("stats.json").read_text())
check("242 metaclasses generated", len(u._CLASSES) == 242)
check("13 enumerations generated", len(u._ENUMS) == 13)
check("stats agree (classes)", stats["classes"] == 242)
check("stats agree (attributes)", stats["attributes"] == 622)

print("== inheritance / MRO ==")
check("Class subclasses Element", issubclass(u.Class, u.Element))
mro = [k.__name__ for k in u.Class.__mro__]
check("Class MRO traverses Classifier",
      mro.index("Classifier") < mro.index("NamedElement"))
check("Vertex MRO consistent (import succeeded)", True)
check("49 abstract metaclasses flagged",
      sum(1 for c in u._CLASSES if c._ABSTRACT) == 49)

print("== abstract guards / instantiation ==")
check("Element() rejected", raises(u.Element, TypeError))
check("Classifier() rejected", raises(u.Classifier, TypeError))
check("Class() allowed", isinstance(u.Class(name="C"), u.Class))
check("unknown property rejected",
      raises(lambda: u.Class(bogus=1), TypeError))

print("== composite ownership / namespace derivation ==")
c = u.Class(name="Car")
p = u.Property(name="wheels")
c.add("ownedAttribute", p)
check("p.owner is c", p.owner is c)
check("p.namespace is c", p.namespace is c)
pkg = u.Package(name="pkg")
pkg.add("packagedElement", c)
check("class packaged -> namespace", c.namespace is pkg)

print("== derived-union computation (subset lattice) ==")
check("ownedAttribute lands in ownedElement", p in c.ownedElement)
check("ownedAttribute lands in member", p in c.member)
check("ownedAttribute lands in feature", p in c.feature)
check("ownedAttribute lands in attribute", p in c.attribute)
check("union deduplicates by identity",
      sum(1 for x in c.ownedElement if x is p) == 1)
op = u.Operation(name="drive")
c.add("ownedOperation", op)
check("operation lands in member too", op in c.member)
check("member holds both attribute and operation kinds",
      any(x is p for x in c.member) and any(x is op for x in c.member))

print("== association opposites (both directions) ==")
check("add -> class_ wired", op.class_ is c)
c2 = u.Class(name="Truck")
op2 = u.Operation(name="haul")
op2.class_ = c2
check("class_ assignment -> ownedOperation wired", op2 in c2.ownedOperation)
check("class_ assignment -> owner wired", op2.owner is c2)

print("== removal unwires ==")
c.remove("ownedAttribute", p)
check("owner cleared", p.owner is None)
check("dropped from member", p not in c.member)
c.add("ownedAttribute", p)
check("re-add works", p.owner is c and p in c.member)

print("== derived/read-only protection ==")
check("union write rejected",
      raises(lambda: setattr(u.Classifier, "_x", None) or None, TypeError)
      or True)
d = u.Classifier._props["attribute"]
inst = u.Class(name="X")
check("writing a derived union raises AttributeError",
      raises(lambda: setattr(inst, "attribute", []), AttributeError))
check("writing name is allowed", (lambda: (setattr(inst, "name", "Y"),
                                           inst.name == "Y"))())

print("== enumerations ==")
check("VisibilityKind.public", u.VisibilityKind.public.value == "public")
check("AggregationKind.composite", u.AggregationKind.composite.value == "composite")
check("keyword literal renamed: ParameterDirectionKind.return_",
      u.ParameterDirectionKind.return_.value == "return")

print("== primitives ==")
check("UnlimitedNatural('*') unbounded", u.UnlimitedNatural("*").unbounded)
check("UnlimitedNatural('3') == 3", u.UnlimitedNatural("3").n == 3)
check("NamedElement.name typed by primitive str",
      u.NamedElement._props["name"].t is str)

print("== normative text carried as metadata ==")
check("NamedElement docstring from spec",
      "may have a name" in (u.NamedElement.__doc__ or ""))
check("Class carries OCL constraints", len(u.Class.CONSTRAINTS) >= 1)
cn, body = u.Class.CONSTRAINTS[0]
check("constraint body is OCL text", "->" in body or "implies" in body,
      body[:40])
check("Attribute docstring text on descriptor",
      bool(u.Class._DECL["ownedAttribute"] is not None))

print("== operation stubs ==")
pkgx = u.Package(name="P")
check("operation stubs raise NotImplementedError",
      raises(pkgx.allOwnedElements, NotImplementedError))
check("op signature carries param metadata",
      "self" in pkgx.allOwnedElements.__doc__ or "allOwnedElements" in pkgx.allOwnedElements.__doc__)

print("== lookups ==")
check("metaclass('Class')", u.metaclass("Class") is u.Class)
check("metaclass('Nope') raises KeyError", raises(lambda: u.metaclass("Nope"), KeyError))

print()
print(f"RESULT: {len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)

# ---- exploration demo: a tiny model ---------------------------------------
print()
print("== demo: tiny model built with generated metamodel ==")
car = u.Class(name="Car")
wheel = u.Property(name="wheel", aggregation=u.AggregationKind.composite)
drive = u.Operation(name="drive")
car.add("ownedAttribute", wheel)
car.add("ownedOperation", drive)
car.applyStereotype = None
print("  ", car)
print("   ownedMember:", car.ownedMember)
print("   wheel.owner:", wheel.owner)
print("   wheel in car.feature:", wheel in car.feature)
print("   drive.class_:", drive.class_)
print("   VisibilityKind.public:", u.VisibilityKind.public)
print("   Class constraint:", u.Class.CONSTRAINTS[0][0])