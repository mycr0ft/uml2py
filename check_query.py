#!/usr/bin/env python
"""E4 checks: query helpers (query.py).

Oracles: programmatic graphs (built like the wave-2 v1 models) plus the
DoDAF and MeasurementsLibrary OMG corpora. Standard library only; run
under ~/ams-gra-sim/.venv."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen.uml25 as U  # noqa: E402
import derived as D  # noqa: E402
import query as Q  # noqa: E402
import xmi21  # noqa: E402

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))


# ---- programmatic graph -----------------------------------------------------
import gen.sysml as S  # noqa: E402

V = U.Package(name="VehicleExample")
sub = U.Package(name="Structure")
V.packagedElement.append(sub)
vehicle = S.Block(name="Vehicle")
wheel = S.Block(name="Wheel")
sub.packagedElement.append(vehicle)
sub.packagedElement.append(wheel)
part = U.Property(name="wheel", type=wheel)
vehicle.ownedAttribute.append(part)
mass = U.Property(name="mass")
vehicle.ownedAttribute.append(mass)
doc = U.Comment(body="vehicle model")
vehicle.ownedComment.append(doc)

print("== walk ==")
els = Q.walk(V)
check("walk is DFS: root, subpackages, classes, properties, comments",
      els[0] is V and els[1] is sub and els[2] is vehicle
      and els[3] is part and els[4] is mass and els[5] is doc
      and els[-2:] and wheel in els, f"{[type(e).__name__ for e in els]}")
check("walk covers exactly the derived containment tree",
      set(map(id, els)) == {id(V)} | set(map(id, D.all_owned_elements(V)))
      and len(els) == len(set(map(id, els))))

print("== find by metaclass ==")
props_cls = Q.find(V, metaclass=U.Property)

check("metaclass by class object and by name agree",
      props_cls == Q.find(V, metaclass="Property"))
check("metaclass filter count", len(props_cls) == 2
      and all(isinstance(e, U.Property) for e in props_cls))
feats = Q.find(V, metaclass=U.Feature)
check("abstract metaclass + subclass matching (Feature ⊇ Property)",
      set(map(id, props_cls)) <= set(map(id, feats))
      and all(isinstance(e, U.Feature) for e in feats))
coms = Q.find(V, metaclass="Comment")
check("find by metaclass name string", len(coms) == 1 and coms[0] is doc)

print("== find by name / qualified / pred ==")
check("name filter", Q.find(V, name="Vehicle") == [vehicle]
      and Q.find(V, name="wheel") == [part])
check("qualified filter (E3 integration)",
      Q.find(V, qualified="VehicleExample::Structure::Vehicle") == [vehicle]
      and Q.find(V, qualified="VehicleExample::Structure::Vehicle::wheel")
      == [part])
check("pred filter",
      Q.find(V, pred=lambda e: isinstance(getattr(e, "name", None), str)
             and e.name.startswith("m")) == [mass])
check("combined metaclass + name",
      Q.find(V, metaclass=U.Property, name="wheel") == [part]
      and Q.find(V, metaclass=U.Property, name="wheel") != [])

print("== deep / of_type / exists / count ==")
direct = Q.find(V, deep=False)
check("deep=False yields only direct children",
      all(D.owner(e) is V for e in direct)
      and set(map(id, direct)) == {id(sub)}
      and vehicle not in direct)
check("of_type == find(metaclass=...)", Q.of_type(V, U.Comment) == coms)
check("exists / count", Q.exists(V, name="wheel")
      and not Q.exists(V, name="nope")
      and Q.count(V, metaclass=U.Package) == 2)

print("== stereotypes (MeasurementsLibrary corpus) ==")
ml = xmi21.read_xmi21("/mnt/TBFox/uml_xmi/MeasurementsLibrary.xmi")
root = ml.roots[0]
taxonomy = next(o for o in ml.objects.values()
                if isinstance(o, U.Property) and o._vals.get("name") == "taxonomy")
check("stereotypes() resolves full labels",
      Q.stereotypes(taxonomy) == ["UAF::Parameters::Measurement"],
      Q.stereotypes(taxonomy))
by_label = Q.find(root, stereotype="Measurement")
by_pair = Q.find(root, stereotype=("UAF", "Measurement"))
check("stereotype filter: label form == (profile, name) form",
      by_label == by_pair and len(by_label) > 0, f"{len(by_label)} found")
app_count = sum(1 for o in ml.objects.values()
                for a in getattr(o, "_applied_stereotypes", ())
                if a[1] == "Measurement")
check("count matches the reader's application records",
      len(by_label) == app_count, f"{len(by_label)} == {app_count}")
ms = [o for o in ml.objects.values()
      if any(a[1] == "MeasurementSet"
             for a in getattr(o, "_applied_stereotypes", ()))]
n_ms = sum(1 for o in ml.objects.values()
           for a in getattr(o, "_applied_stereotypes", ())
           if a[1] == "MeasurementSet")
check("full-label form targets the right stereotype",
      Q.find(root, stereotype="UAF::Parameters::MeasurementSet") == ms
      and len(ms) == n_ms, f"{len(ms)} == {n_ms}")

print("== DoDAF corpus ==")
dodaf = xmi21.read_xmi21("/mnt/TBFox/DoDAFLibrary.xmi")
droot = dodaf.roots[0]
reach = Q.walk(droot)
rootless = {id(o) for o in dodaf.objects.values() if o.owner is None}
owned_ids = set(map(id, dodaf.objects.values())) - rootless
walked = set(map(id, reach))
check("walk: owned xmi:id objects all reached; every walked element is "
      "the root, reader-synthesized (owner unwired), or owned by a "
      "walked element",
      owned_ids <= walked
      and all(o is droot or o.owner is None or id(o.owner) in walked
              for o in reach)
      and all(isinstance(o, U.LiteralUnlimitedNatural)
              for o in reach
              if o is not droot and o.owner is None))
check("DoDAF comments and datatypes by metaclass",
      Q.count(droot, metaclass=U.Comment)
      == sum(1 for o in dodaf.objects.values() if isinstance(o, U.Comment))
      and Q.count(droot, metaclass=U.DataType)
      == sum(1 for o in dodaf.objects.values() if isinstance(o, U.DataType)))

print()
print(f"RESULT: {len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)