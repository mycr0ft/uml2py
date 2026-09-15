#!/usr/bin/env python
"""End-to-end check: read the OMG-published UPDM example model
DoDAFLibrary.xmi (XMI 2.1 / EMF dialect) with the clean-room instance
reader, verify the resulting gen.uml25 objects, then emit SysML v2
textual notation and validate it with sysmlpy.

Corpus eligibility: OMG-published model (see REPORT.md; commercial
book models are excluded).

Run under ~/sysmlpy/.venv (needs sysmlpy + pint)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen.uml25 as U  # noqa: E402
import v1_to_v2 as M  # noqa: E402
import xmi21  # noqa: E402

DODAF = "/mnt/TBFox/DoDAFLibrary.xmi"

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))


# ---- read -------------------------------------------------------------------
m = xmi21.read_xmi21(DODAF)

print(f"objects: {len(m.objects)}, roots: {len(m.roots)}, "
      f"apps: {sum(len(v) for v in m.apps.values())}, "
      f"hrefs: {len(m.hrefs)}, profiles: {len(m.profiles)}, "
      f"derived: {len(m.derived_names)}")

root = m.roots[0]
check("root is a UML Model", isinstance(root, U.Model), type(root).__name__)
check("model named from <name> child", root.name == "DoDAF Class Library",
      repr(root.name))
check("9 packagedElements", len(list(root.ownedMember)) == 9,
      str(len(list(root.ownedMember))))

enums = [e for e in root.ownedMember if isinstance(e, U.Enumeration)]
dts = [e for e in root.ownedMember
       if isinstance(e, U.DataType) and not isinstance(e, U.Enumeration)]
assocs = [e for e in root.ownedMember if isinstance(e, U.Association)]
check("7 DataTypes", len(dts) == 7, str(len(dts)))
check("1 Enumeration", len(enums) == 1, str(len(enums)))
check("1 Association", len(assocs) == 1, str(len(assocs)))
check("Enumeration has 17 literals", len(list(enums[0].ownedLiteral)) == 17,
      str(len(list(enums[0].ownedLiteral))))

props = [p for d in dts for p in d.ownedAttribute]
end_props = [e for a in assocs for e in a.ownedEnd]
check("53 classifier-owned properties", len(props) == 53, str(len(props)))
check("1 association-owned end", len(end_props) == 1, str(len(end_props)))

# typing: 52 external String hrefs + 2 internal idrefs
ext_props = [p for p in props
             if isinstance(p._vals.get("type"), U.DataType)
             and getattr(p._vals.get("type"), "_external_href", None)]
check("52 properties typed by external String", len(ext_props) == 52,
      str(len(ext_props)))
cls_prop = next(p for p in props if p.name == "classification"
                and p._vals.get("type") is enums[0])
check("SecurityAttributes-classification typed by ClassificationType",
      cls_prop is not None)
check("assoc end typed by SecurityAttributes",
      end_props[0]._vals.get("type") is dts[0])
check("52 external hrefs recorded, all UML.xmi#String",
      len(m.hrefs) == 52
      and all(h.endswith("UML.xmi#String") for _, _, h in m.hrefs),
      str(len(m.hrefs)))
ext = m.synthetic_types.get("String")
check("external String resolved to synthetic marker (never emitted)",
      ext is not None and ext._external_href.endswith("UML.xmi#String"))

# comments carried recursively with bodies
all_comments = [o for o in m.objects.values() if isinstance(o, U.Comment)]
check("30 comments carried with bodies",
      len(all_comments) == 30
      and all(isinstance(c._vals.get("body"), str) and c._vals.get("body")
              for c in all_comments), str(len(all_comments)))

# multiplicity: empty <lowerValue/> = EMF default 0; upper '*' = unbounded
star = [p for p in props if M._mult(p) == "[*]"]
check("26 properties serialized [0..*] (-> [*])", len(star) == 26,
      str(len(star)))
plain = [p for p in props if M._mult(p) == ""]
check("27 properties default [1..1]", len(plain) == 27, str(len(plain)))

# association wiring (memberEnd = [unnamed ownedEnd, classification])
assoc = assocs[0]
ends = list(assoc.memberEnd)
check("memberEnd = [ownedEnd, SecurityAttributes-classification]",
      len(ends) == 2 and ends[0] is end_props[0]
      and ends[1] is cls_prop)
check("properties' association back-refs resolve",
      sum(1 for o in m.objects.values()
          if isinstance(o, U.Property) and o._vals.get("association") is assoc) == 2)

# names: file names + recorded id-derived names
check("association name derived from xmi:id (recorded)",
      ("DoDAF_Class_Library-packagedElement-7", "packagedElement-7")
      in m.derived_names, repr(assoc.name))
check("unnamed ownedEnd name derived from xmi:id (recorded)",
      any(t == "ownedEnd" for _, t in m.derived_names),
      str(m.derived_names))

# stereotype applications: 53 Measurement + 7 MeasurementSet + 1 ModelLibrary
total_apps = sum(len(v) for v in m.apps.values())
kinds = {}
for lst in m.apps.values():
    for prof, st, _ in lst:
        kinds[st] = kinds.get(st, 0) + 1
check("61 applications (53 Measurement, 7 MeasurementSet, 1 ModelLibrary)",
      total_apps == 61 and kinds == {"Measurement": 53, "MeasurementSet": 7,
                                     "ModelLibrary": 1}, str(kinds))
check("ModelLibrary app attached to the model",
      getattr(root, "_applied_stereotypes", None)
      and root._applied_stereotypes[0][1] == "ModelLibrary")
check("MeasurementSet attached to DataTypes",
      all(getattr(d, "_applied_stereotypes", None)
          and d._applied_stereotypes[0][1] == "MeasurementSet" for d in dts),
      "7/7")
check("Measurement apps attached to properties",
      sum(1 for p in props if getattr(p, "_applied_stereotypes", None)) == 53)
check("appliedProfile href recorded (UPDM)",
      len(m.profiles) == 1 and "UPDM" in m.profiles[0], str(m.profiles))

check("no unmapped metaclass tags", not m.unmapped, str(m.unmapped[:3]))
check("no unmapped features", not m.unmapped_features, str(m.unmapped_features[:3]))

# ---- emit v2 and validate ---------------------------------------------------
text = M.emit_v2(root)
print("---- emitted SysML v2 (excerpt) ----")
lines_ = text.splitlines()
print("\n".join(lines_[:20]))
print("...")
counts = M.validate_with_sysmlpy(text)
print("sysmlpy counts:", counts)

check("sysmlpy parses emitted v2", isinstance(counts, dict))
check("7 attribute defs (external String not redefined)",
      counts.get("attribute", 0) == 7, str(counts.get("attribute")))
check("1 enum def", counts.get("enumeration", 0) == 1)
check("1 connection def", counts.get("connection", 0) == 1)

print()
print(f"RESULT: {len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)

out = Path(__file__).resolve().parent / "dodaf_library_v2.sysml"
out.write_text(text + "\n")
print(f"(wrote {out.name})")