#!/usr/bin/env python
"""Checks for mdzip.py against the public MagicDraw/Cameo corpus.

Corpus files are NOT committed (they are third-party sample models; see
scripts/fetch_mdzip_corpus.sh for provenance and re-download).  Point
MDZIP_CORPUS_DIR at a directory containing:

    APE.mdzip            Open-MBEE/OpenSE-Cookbook master Models/APE-ReferenceModel.mdzip
    MPS.mdzip            GaloisInc/VERSE-OpenSUT main models/SysMLv1/MPS.mdzip
    maas-warehouse.mdzip autarchprinceps/Multiagent-Warehouse master Documentation/maas-warehouse.mdzip

Checks skip (exit 0, with a note) when the corpus is absent.
"""
import base64
import json
import os
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mdzip import MdZip, sniff_bytes  # noqa: E402

CORPUS = Path(os.environ.get("MDZIP_CORPUS", "/tmp/mdzip_probe"))
FILES = {n: CORPUS / f"{n}.mdzip" for n in ("APE", "MPS", "maas-warehouse")}

def snap_text_maas_model(md):
    return "\n".join(md.zf.read(i.filename).decode("utf-8", "replace")
                      for i in md.members_of("umodel-model"))

missing = [n for n, p in FILES.items() if not p.is_file()]
PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))


print("== corpus present ==")
if missing:
    print(f"  SKIP: corpus files missing in {CORPUS}: {missing}")
    print(f"  (set MDZIP_CORPUS or run scripts/fetch_mdzip_corpus.sh)")
    print(f"  {len(PASS)} passed, 0 failed (skipped)")
    sys.exit(0)

with MdZip(FILES["MPS"]) as mps, MdZip(FILES["APE"]) as ape, \
        MdZip(FILES["maas-warehouse"]) as maas:

    print("== inventory ==")
    inv = mps.inventory()
    check("MPS has umodel snapshots", inv.get("umodel-snapshot", 0) >= 5, str(inv))
    check("MPS has diagram-view (BINARY) members", inv.get("diagram-view", 0) > 10)
    check("MPS has project metadata + options + dependencies",
          {"project-metadata", "project-options", "proxy-dependencies"} <= set(inv))
    check("every MPS member is XML text or properties",
          all(sniff_bytes(mps.zf.read(i.filename)[:16]) in ("svg", "zip", "gz", None)
              or i.filename.endswith(".properties") or i.file_size == 0
              for i in mps.members),
          "no opaque Java-serialized blobs")

    print("== namespaces / aliasing ==")
    def snap_text(md):
        return "\n".join(md.zf.read(i.filename).decode("utf-8", "replace")
                          for i in md.members_of("umodel-snapshot"))
    ns_25 = "nomagic.com/magicdraw/UML/2.5\"" in snap_text(maas)
    ns_2511 = "nomagic.com/magicdraw/UML/2.5.1.1" in snap_text(mps)
    check("maas-warehouse (2015) snapshots use UML/2.5 ns", ns_25)
    check("MPS (2024-era) snapshots use UML/2.5.1.1 ns", ns_2511)
    check("model-style members use OMG 20131001 ns (both files)",
          "www.omg.org/spec/UML/20131001" in snap_text_maas_model(maas)
          and "www.omg.org/spec/UML/20131001" in snap_text_maas_model(mps))
    aliased = MdZip.alias_nomagic(snap_text(mps))
    check("alias_nomagic rewrites ns to OMG 20161101",
          "http://www.omg.org/spec/UML/20161101" in aliased
          and "nomagic.com/magicdraw" not in
          [s for s in aliased.split() if s.startswith("xmlns:uml")][0])
    import xml.etree.ElementTree as ET

    def parses(text):
        try:
            ET.fromstring(MdZip.alias_nomagic(text))
            return True
        except ET.ParseError:
            return False

    check("aliased umodel members parse as XML",
          all(parses(t) for _, t in mps.model_members()))

    print("== model element extraction (APE) ==")
    from collections import Counter
    types = Counter(t for _, t, _ in ape.iter_model_elements())
    check("APE full-store element count pinned (48225)",
          sum(types.values()) == 48225, str(sum(types.values())))
    check("APE ElementTaggedValue encoding present (208)",
          types.get("uml:ElementTaggedValue") == 208,
          str(types.get("uml:ElementTaggedValue")))

    print("== proxies and usages ==")
    deps = mps.members_of("proxy-dependencies")
    check("MPS proxy-dependencies member present", len(deps) == 1)
    uris = [p["resource_uris"] for p in mps.proxies()]
    flat = [u for us in uris for u in us]
    check("proxy dependency URIs are local:/PROJECT-... form",
          all(u.startswith("local:/PROJECT-") for u in flat), str(flat[:2]))
    used = mps.usages()
    check("MPS uses 3 referenced projects", len(used) == 3, str(len(used)))
    import re as _re
    check("usage entries are PROJECT-<hex/dashed-uuid>",
          all(_re.fullmatch(r"PROJECT-[0-9a-f][0-9a-f-]{29,}", u) and not u.endswith("-")
              for u in used), str(used))
    check("maas usages include its own PROJECT marker",
          any(u.startswith("PROJECT-a7827124") for u in maas.usages()))

    print("== version forensics ==")
    eras, detail = mps.version_clues()
    check("MPS IDs fingerprint 2021x era",
          any("2021x" in e for e in eras), str(eras))
    eras_a, _ = ape.version_clues()
    check("APE IDs fingerprint 9_0 era", any("9.0" in e for e in eras_a), str(eras_a))
    eras_m, _ = maas.version_clues()
    check("maas (2015) yields at least one era", len(eras_m) >= 1, str(eras_m))

    print("== image extraction ==")
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        man = mps.extract_images(td)
        check("MPS yields base64 ZIP payloads (project options)",
              sum(1 for e in man if e["type"] == "zip" and e["encoding"] == "base64") >= 3,
              str(len(man)))
        check("MPS yields no hex-encoded images (corpus fact)",
              not any(e["encoding"] == "hex" for e in man))
        z = [e for e in man if e["type"] == "zip"][0]
        raw = (Path(td) / z["file"]).read_bytes()
        check("decoded payload re-sniffs as zip", sniff_bytes(raw[:4]) == "zip")
        with zipfile.ZipFile(Path(td) / z["file"]) as zz:
            check("decoded payload opens as a real zip", len(zz.infolist()) >= 1)
        man_a = ape.extract_images(td)
        check("APE yields no hex-encoded images (corpus fact)",
              not any(e["encoding"] == "hex" for e in man_a))
        check("manifest rows carry member/offset/encoding/type",
              all({"member", "offset", "encoding", "type", "file"} <= set(e)
                  for e in man + man_a))
        check("manifest.json written", (Path(td) / "manifest.json").is_file())

print()
print(f"RESULT: {len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)