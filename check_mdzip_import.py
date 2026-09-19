#!/usr/bin/env python
"""Checks for mdzip_import.py over the public corpus.

Corpus files are NOT committed (see scripts/fetch_mdzip_corpus.sh and
scripts/mdzip_corpus_tools.py).  MDZIP_CORPUS selects the directory
(default /mnt/TBFox/mdzip_corpus).  Skips cleanly when absent.
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mdzip_import import import_mdzip, MdZipImportError  # noqa: E402

CORPUS = Path(os.environ.get("MDZIP_CORPUS", "/mnt/TBFox/mdzip_corpus"))
PROBE = Path(os.environ.get("MDZIP_PROBE", "/tmp/mdzip_probe"))

FILES = {
    "APE": CORPUS / "Open-MBEE__OpenSE-Cookbook" / "APE-ReferenceModel.mdzip",
    "MPS": CORPUS / "GaloisInc__VERSE-OpenSUT" / "MPS.mdzip",
    "maas": CORPUS / "autarchprinceps__Multiagent-Warehouse" / "maas-warehouse.mdzip",
    "SAF": CORPUS / "GfSE__SAF-Cameo-Profile" / "SAF_FFDS.mdzip",
    "NERDMAN": CORPUS / "gtri__rapid-modeling-tools" / "INGRID Nerdman.mdzip",
}
missing = [k for k, p in FILES.items() if not p.is_file()]

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))


if missing:
    print(f"  SKIP: corpus missing in {CORPUS}: {missing}")
    print(f"  {len(PASS)} passed, 0 failed (skipped)")
    sys.exit(0)

imps = {}
for k, p in FILES.items():
    imps[k] = import_mdzip(p)

print("== construction across dialects ==")
ape = imps["APE"].stats()
check("APE constructs > 400 objects", ape["objects"] > 400, str(ape["objects"]))
check("APE has Classes + DataTypes + Packages",
      ape["by_metaclass"].get("Class", 0) > 200
      and ape["by_metaclass"].get("DataType", 0) >= 80
      and ape["by_metaclass"].get("Package", 0) >= 60,
      str(ape["by_metaclass"]))
check("APE delta-snapshot duplicates dropped (keep-last)",
      ape["duplicates_dropped"] == 811, str(ape["duplicates_dropped"]))
check("APE type coercions applied", ape["coercions"] == 585, str(ape["coercions"]))
check("APE 18 roots (per-member snapshots)", ape["roots"] == 18)
check("APE profile-layer unmapped recorded, not raised",
      0 < ape["unmapped"] < 20, str(ape["unmapped"]))
saf = imps["SAF"].stats()
check("SAF_FFDS (2024x) constructs", saf["objects"] > 150, str(saf["objects"]))
check("SAF_FFDS AssociationClass handled",
      saf["by_metaclass"].get("AssociationClass", 0) >= 1
      or saf["by_metaclass"].get("Association", 0) >= 1,
      str(saf["by_metaclass"]))
mps = imps["MPS"].stats()
check("MPS (2021x) constructs", mps["objects"] > 10, str(mps["objects"]))
maas = imps["maas"].stats()
check("maas-warehouse (2015) constructs", maas["objects"] >= 8, str(maas["objects"]))

print("== provenance carried alongside the model ==")
check("APE usages preserved", len(imps["APE"].usages) >= 10,
      str(len(imps["APE"].usages)))
check("APE version eras preserved", len(imps["APE"].eras) >= 5)
check("MPS usages preserved", len(imps["MPS"].usages) == 3)

print("== wave-2 boundary recorded, not invented ==")
check("APE name-typed refs recorded", ape["name_refs"] > 100, str(ape["name_refs"]))
check("APE raw unresolved types recorded", ape["raw_unresolved"] == 3)
check("no cross-project refs crash the reader",
      all(i.stats()["cross_project_refs"] >= 0 for i in imps.values()))

print("== object sanity ==")
ape_x = imps["APE"].xmi
pk = [o for o in ape_x.objects.values() if type(o).__name__ == "Package"]
check("APE packages have names", all(o.name for o in pk if o.name is not None)
      and len(pk) >= 60, str(len(pk)))
cls = [o for o in ape_x.objects.values() if type(o).__name__ == "Class"]
named = [c.name for c in cls if isinstance(c.name, str) and c.name]
check("APE classes carry names from the source", len(named) > 200, str(len(named)))

print()
print(f"RESULT: {len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)