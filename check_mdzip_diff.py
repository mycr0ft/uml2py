#!/usr/bin/env python
"""check_mdzip_diff.py - semantic diff checks over the revision pairs.

Pairs live in $MDZIP_REVISIONS (default /mnt/TBFox/mdzip_corpus/_revisions);
they are third-party model snapshots, NOT committed (see
scripts/fetch_mdzip_revisions.sh).  Skips cleanly when absent.

Pins the three guarantees that make semantic diffing mdzips viable:
  noise immunity (re-save only => zero delta),
  change detection (real edits => exact reported deltas),
  identity repair (renames/moves matched despite new qualified paths).
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mdzip_diff import import_records, diff_records  # noqa: E402

REV = Path(os.environ.get("MDZIP_REVISIONS",
                          "/mnt/TBFox/mdzip_corpus/_revisions"))
missing = [d.name for d in REV.iterdir()
           if d.is_dir() and not (d / "old.mdzip").is_file()] \
    if REV.is_dir() else ["(no revisions dir)"]
have = sorted({d.name.split("_")[0] for d in REV.iterdir() if d.is_dir()}) \
    if REV.is_dir() else []

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))


def pair(tag):
    for d in REV.iterdir():
        if d.name.startswith(tag) and (d / "old.mdzip").is_file():
            return d
    return None


if not REV.is_dir() or not any(REV.iterdir()):
    print(f"  SKIP: no revision pairs under {REV}")
    print(f"  (run scripts/fetch_mdzip_revisions.sh)")
    print(f"  {len(PASS)} passed, 0 failed (skipped)")
    sys.exit(0)

print("== noise immunity (re-saves must read as zero delta) ==")
p = pair("GfSE__SAF-Cameo-Profile_SAF_SCM_Profile.mdzip_fc25ce-fdb39c")
if p:
    ra, _ = import_records(p / "old.mdzip")
    rb, _ = import_records(p / "new.mdzip")
    rep = diff_records(ra, rb)
    c = rep["counts"]
    check("SAF profile re-save => zero semantic delta",
          c["added"] == 0 and c["removed"] == 0 and c["changed"] == 0
          and c["moved_or_renamed"] == 0, json.dumps(c))
    check("SAF pair: matched == old == new",
          c["matched"] == c["old"] == c["new"], json.dumps(c))
p = pair("openEHR__specifications-AM_openEHR_UML-AM-14.mdzip_9f99cc-b830e8")
if p:
    ra, _ = import_records(p / "old.mdzip")
    rb, _ = import_records(p / "new.mdzip")
    rep = diff_records(ra, rb)
    c = rep["counts"]
    # commit claims "non-semantic changes": identity repair must hold even
    # through large id churn (49 add + 48 remove would be WRONG here)
    check("openEHR regen: no net element churn (added ~ removed)",
          abs(c["added"] - c["removed"]) <= 2,
          f"add={c['added']} rem={c['removed']} mv={c['moved_or_renamed']}")
    check("openEHR regen: identity repaired across id churn",
          c["matched"] >= c["old"] - 10, json.dumps(c))

print("== change detection (real edits reported exactly) ==")
p = pair("DLR-FT__ModelBasedSTPA_STPAStandaloneProfileWithExample_v19SP3._d0810a-5bc92e")
if p:
    ra, _ = import_records(p / "old.mdzip")
    rb, _ = import_records(p / "new.mdzip")
    rep = diff_records(ra, rb)
    c = rep["counts"]
    added_names = {r["name"] for r in rep["added"]}
    check("DLR: ControlledProcessSTPA stereotype detected as added",
          "ControlledProcessSTPA" in added_names, str(added_names))
    check("DLR: base_Class/base_Property extension properties detected",
          any(r["name"] in ("base_Class", "base_Property")
              for r in rep["added"]))
    check("DLR: nothing removed", c["removed"] == 0, json.dumps(c))
p = pair("stuartfowler__CEMT_Cyber_Profile.mdzip_4afd60-a7aba7")
if p:
    ra, _ = import_records(p / "old.mdzip")
    rb, _ = import_records(p / "new.mdzip")
    rep = diff_records(ra, rb)
    c = rep["counts"]
    check("CEMT RC10->2022xR2: 8 stereotypes added, 1 removed",
          c["added"] == 8 and c["removed"] == 1, json.dumps(c))

print("== identity repair (renames/moves) ==")
p = pair("usnistgov__DiscreteEventLogist_CentralFillPharmacy.mdzip_ade53f-035274")
if p:
    ra, _ = import_records(p / "old.mdzip")
    rb, _ = import_records(p / "new.mdzip")
    rep = diff_records(ra, rb)
    c = rep["counts"]
    check("NIST rename commit: no false adds (added == 0)", c["added"] == 0,
          json.dumps(c))
    check("NIST: >= 10 moved/renamed matched", c["moved_or_renamed"] >= 10,
          str(c["moved_or_renamed"]))
    mvs = [p2 for p2 in rep["pairs"] if p2.get("moved_or_renamed")]
    check("NIST: DELS -> Data rename repaired at Model level",
          any("DELS" in p2["old"] and "Data" in p2["new"] for p2 in mvs))

print("== id-independence (the TWC guarantee) ==")
p = pair("DLR-FT__ModelBasedSTPA_STPAStandaloneProfileWithExample_v19SP3._d0810a-5bc92e")
if p:
    ra, _ = import_records(p / "old.mdzip")
    rb, _ = import_records(p / "new.mdzip")
    # the two files share almost NO ids for the added content; prove the
    # matcher never sees ids: every added record's qualpath carries the
    # element NAME, and matching works purely on metaclass+path+features
    check("records carry no xmi ids",
          all("_xmi_id" not in r and "id" not in r["feats"]
              for r in ra + rb))

print()
print(f"RESULT: {len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)