#!/usr/bin/env python
"""mdzip.py - scrape and forensically inspect MagicDraw/Cameo .mdzip project files.

A .mdzip is a ZIP of XML members.  Nothing in it is actually binary in the
files examined so far (2015-era MagicDraw through 2024x-era Cameo): the
"BINARY-<uuid>" members are diagram *presentation* XML (mdOwnedViews /
mdElement), and the model itself lives in one or more
"proxy.local__PROJECT$..._resource_com$dnomagic$dmagicdraw$duml_umodel$...
dsnapshot" members -- XMI 2.0 with standard UML property names, but under the
Nomagic namespace (http://www.nomagic.com/magicdraw/UML/2.5[.1.1]) and split
across members that reference each other by xmi:id / href.

This module is the extraction/forensics layer of a clean-room importer:
  - inventory:      what is in the archive, by kind
  - version_clues:  MagicDraw/Cameo era fingerprints (ID prefixes + option text)
  - usages:         project-usages / referenced projects (Proxy evidence)
  - proxies:        the proxy snapshot members and their resource URIs
  - images:         hex- or base64-encoded payloads (GT-corpus feature: SVGs
                    encoded as hex digits inside XMI attributes) decoded and
                    sniffed (SVG/PNG/JPEG/GIF/ZIP/GZIP)
  - model members:  the umodel snapshot XMLs, aliased Nomagic->UML for
                    downstream XMI processing (xmi21.py / gen.uml25)

Usage:
    python mdzip.py <file.mdzip> members|info|usages|versions|images <outdir>

std-lib only.  No MagicDraw/Cameo code or documentation was consulted; every
fact here is pinned by check_mdzip.py against downloaded public corpus files.
"""
import base64
import binascii
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

NOMAGIC_NS = re.compile(r"http://www\.nomagic\.com/magicdraw/UML/(2\.5(\.1\.1)?)")
XMI_TYPE_KEYS = ("{http://www.omg.org/XMI}type",
                 "{http://www.w3.org/2001/XMLSchema-instance}type")

UMODEL_SNAPSHOT = re.compile(
    r"_resource_com\$dnomagic\$dmagicdraw\$duml_umodel\$d.*dsnapshot$")
UMODEL_MODEL = re.compile(r"^com\.nomagic\.magicdraw\.uml_model\.(model|shared_model)$")
PROXY_MEMBER = re.compile(r"proxy\.local__PROJECT\$")
PROJECT_MEMBER = re.compile(r"^PROJECT-[0-9a-f]{8}-[0-9a-f]{4}-")
DEPENDENCY_LIST = re.compile(r"privatedependencylist$")
PROJECT_META = re.compile(r"com\.nomagic\.ci\.metamodel\.project$")
OPTIONS_MEMBER = re.compile(r"project\.options|commonprojectoptions|"
                            r"personalprojectoptions")

# _2021x_2_1b400495_1713...  /  _12_0_8f90291_1163...  /  _16_8beta_2104... /
# _9_0_2_91a0295_1110...  -- era, optional counters, hex tag, timestamp
ID_PREFIX = re.compile(r"_(\d{1,4}(?:x|beta)?(?:_\d+)*)_[0-9a-f]{6,8}_\d{10,}")
ERA_NAMES = {
    "9_0": "MagicDraw 9.0 (2005-era)",
    "12_0": "MagicDraw 12.0 (2006/2007-era)",
    "12_1": "MagicDraw 12.1",
    "16_0": "MagicDraw 16.0",
    "16_8": "MagicDraw 16.8",
    "16_8beta": "MagicDraw 16.8 beta",
    "17_0": "MagicDraw 17.0",
    "18_0": "MagicDraw 18.0",
    "18_0beta": "MagicDraw 18.0 beta",
    "18_5": "MagicDraw 18.5",
    "19_0": "MagicDraw 19.0 LTR",
    "2021x": "Cameo/MagicDraw 2021x",
    "2022x": "Cameo/MagicDraw 2022x",
    "2024x": "Cameo/MagicDraw 2024x",
}

HEX_RUN = re.compile(r"[0-9a-fA-F]{256,}")
B64_RUN = re.compile(r"[A-Za-z0-9+/]{800,}={0,2}")


def _local(tag):
    return tag.split("}")[-1] if "}" in tag else tag


def _xmi_type(el):
    for k, v in el.attrib.items():
        if _local(k) == "type":
            return v
    return None


def _xmi_id(el):
    for k, v in el.attrib.items():
        if _local(k) in ("id", "ID"):
            return v
    return None


def sniff_bytes(b):
    if b[:5] in (b"<?xml", b"<svg ") or b[:4] == b"<svg":
        return "svg"
    if b[:4] == b"\x89PNG":
        return "png"
    if b[:2] == b"\xff\xd8":
        return "jpg"
    if b[:4] == b"GIF8":
        return "gif"
    if b[:2] == b"\x1f\x8b":
        return "gz"
    if b[:4] == b"PK\x03\x04":
        return "zip"
    return None


class MdZip:
    """Forensic view over one .mdzip archive."""

    def __init__(self, path):
        self.path = str(path)
        self.zf = zipfile.ZipFile(self.path)
        self.members = self.zf.infolist()

    def close(self):
        self.zf.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    # -- inventory ----------------------------------------------------------
    def kind_of(self, name):
        if UMODEL_SNAPSHOT.search(name):
            return "umodel-snapshot"
        if UMODEL_MODEL.search(name):
            return "umodel-model"
        if DEPENDENCY_LIST.search(name):
            return "proxy-dependencies"
        if PROXY_MEMBER.search(name):
            return "proxy"
        if name.startswith("BINARY-"):
            return "diagram-view"
        if PROJECT_MEMBER.match(name):
            return "used-project-marker"
        if PROJECT_META.search(name):
            return "project-metadata"
        if OPTIONS_MEMBER.search(name):
            return "project-options"
        if name.endswith(".properties"):
            return "properties"
        return "other"

    def inventory(self):
        inv = Counter(self.kind_of(i.filename) for i in self.members)
        return dict(sorted(inv.items()))

    def members_of(self, kind):
        return [i for i in self.members if self.kind_of(i.filename) == kind]

    # -- model members ------------------------------------------------------
    def model_members(self):
        """(name, root) for the model-bearing members.

        Two persistence layouts coexist and SOME FILES NEED BOTH:
          - snapshot style: proxy.local__PROJECT$...umodel...dsnapshot
            members (XMI 2.0 spellings) -- may carry the project's own
            model content (APE: 18 snapshot members, 2250 ids);
          - model style: com.nomagic.magicdraw.uml_model.model (primary
            model, can be a small stub pointing at used shared projects)
            and ...shared_model (profile libraries, can be the bulk:
            APE shared_model = 9.5 MB, 18k ids).
        The id spaces are near-disjoint (overlap ~14 ids on APE), so
        merging BOTH styles is correct; keep-last dedup in the importer
        collapses the tiny overlap.  Order: snapshots first, model-style
        last (later wins on dedup, and the model-style store is newer).
        """
        out = []
        for i in self.members:
            if self.kind_of(i.filename) == "umodel-snapshot":
                out.append((i.filename,
                            self.zf.read(i.filename).decode("utf-8", "replace")))
        for i in self.members:
            if self.kind_of(i.filename) == "umodel-model":
                out.append((i.filename,
                            self.zf.read(i.filename).decode("utf-8", "replace")))
        return out

    @staticmethod
    def alias_nomagic(text):
        """Namespace-alias Nomagic UML to the OMG 2.5.1 namespace, so standard
        UML XMI processing (xmi21.py) can consume the member.  Returns the
        text with only the xmlns:uml declaration rewritten."""
        return NOMAGIC_NS.sub("http://www.omg.org/spec/UML/20161101", text)

    def iter_model_elements(self):
        """Yield (xmi_id, xmi_type, element) across all umodel members."""
        for name, text in self.model_members():
            try:
                root = ET.fromstring(self.alias_nomagic(text))
            except ET.ParseError:
                continue
            for el in root.iter():
                yield _xmi_id(el), _xmi_type(el), el

    # -- proxies and usages -------------------------------------------------
    def proxies(self):
        """Proxy snapshot members and the resource URIs they reference."""
        out = []
        for i in self.members:
            if PROXY_MEMBER.search(i.filename) or DEPENDENCY_LIST.search(i.filename):
                try:
                    root = ET.fromstring(self.zf.read(i.filename))
                except ET.ParseError:
                    continue
                uris = [e.get("originalResourceURI") for e in root.iter()
                        if e.get("originalResourceURI")]
                out.append({"member": i.filename, "kind": self.kind_of(i.filename),
                            "size": i.file_size, "resource_uris": uris})
        return out

    def usages(self):
        """Referenced (USED) projects: PROJECT-* markers + dependency URIs."""
        used = set()
        for i in self.members:
            if PROJECT_MEMBER.match(i.filename):
                used.add(i.filename)
        for p in self.proxies():
            for uri in p["resource_uris"]:
                m = re.match(r"local:/?(PROJECT-[0-9a-f-]+)", uri)
                if m and m.group(1) not in {i.filename for i in self.members}:
                    used.add(m.group(1))
                elif m:
                    # self-reference; skip
                    pass
        return sorted(used)

    def project_description(self):
        for i in self.members_of("project-metadata"):
            try:
                root = ET.fromstring(self.zf.read(i.filename))
            except ET.ParseError:
                continue
            if _local(root.tag) == "Project":
                return root.get("description"), root.get("id")
        return None, None

    # -- version forensics --------------------------------------------------
    def version_clues(self):
        """(eras, detail) -- ID-prefix fingerprints + option-text hints."""
        eras = Counter()
        extra = set()
        for i in self.members:
            text = self.zf.read(i.filename).decode("utf-8", "replace")
            for m in ID_PREFIX.finditer(text):
                era = m.group(1)
                eras[era] += 1
            if self.kind_of(i.filename) == "project-options":
                for m in re.finditer(
                        r"(?:MagicDraw|Cameo(?:\s+Enterprise\s+Architecture)?|"
                        r"CATIA\s+NoMagic)[^\n]{0,80}?\b(1[89]\.\d|202\d x?)\b",
                        text):
                    extra.add(m.group(0).strip()[:100])
        named = set()
        for e in eras:
            key = e
            m2 = re.match(r"(\d{4}x)_\d+$", key)          # 2021x_2 -> 2021x
            if m2:
                key = m2.group(1)
            elif key.count("_") > 1 and not key.endswith("beta"):
                key = re.sub(r"_\d+$", "", key)           # 12_0_2 -> 12_0
            named.add(ERA_NAMES.get(key, f"ID-era {key}"))
        detail = [{"era": e, "count": n} for e, n in eras.most_common(12)]
        return sorted(named), {"prefixes": detail, "option_text": sorted(extra)}

    # -- image extraction ---------------------------------------------------
    def extract_images(self, outdir, min_hex=256):
        """Decode hex/base64 payloads found in any member; write to outdir.

        GT-corpus feature: diagrams/assets encoded as hex digits inside XMI
        attribute values.  Scan is generic (attribute or text).  Returns the
        manifest (also written as manifest.json).
        """
        outdir = Path(outdir)
        outdir.mkdir(parents=True, exist_ok=True)
        manifest = []
        seen = set()
        for idx, i in enumerate(self.members):
            text = self.zf.read(i.filename).decode("utf-8", "replace")
            for enc, rx in (("hex", HEX_RUN), ("base64", B64_RUN)):
                for m in rx.finditer(text):
                    blob = m.group(0)
                    if enc == "hex":
                        if len(blob) % 2:
                            blob = blob[:-1]
                        try:
                            raw = bytes.fromhex(blob)
                        except ValueError:
                            continue
                    else:
                        try:
                            raw = base64.b64decode(blob + "=" * (-len(blob) % 4))
                        except binascii.Error:
                            continue
                    kind = sniff_bytes(raw)
                    if not kind:
                        continue
                    key = (idx, kind, len(raw))
                    if key in seen:
                        continue
                    seen.add(key)
                    fn = outdir / f"m{idx:03d}_{m.start():09d}_{kind}.{kind}"
                    fn.write_bytes(raw)
                    manifest.append({
                        "member": i.filename, "offset": m.start(),
                        "encoding": enc, "type": kind,
                        "decoded_bytes": len(raw), "file": fn.name,
                    })
        (outdir / "manifest.json").write_text(
            json.dumps(manifest, indent=2))
        return manifest

    # -- summary ------------------------------------------------------------
    def info(self):
        desc, pid = self.project_description()
        eras, detail = self.version_clues()
        return {
            "file": self.path,
            "size": Path(self.path).stat().st_size,
            "members": len(self.members),
            "inventory": self.inventory(),
            "project_description": desc,
            "project_id": pid,
            "usages": self.usages(),
            "version_eras": eras,
            "version_detail": detail,
        }


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    path, cmd = argv[1], argv[2]
    with MdZip(path) as md:
        if cmd == "members":
            for i in md.members:
                print(f"{md.kind_of(i.filename):22s} {i.file_size:>10d}  {i.filename[:80]}")
        elif cmd == "info":
            print(json.dumps(md.info(), indent=2))
        elif cmd == "usages":
            print(json.dumps(md.usages(), indent=2))
        elif cmd == "versions":
            eras, detail = md.version_clues()
            print(json.dumps({"eras": eras, "detail": detail}, indent=2))
        elif cmd == "images":
            outdir = argv[3] if len(argv) > 3 else "./mdzip_images"
            man = md.extract_images(outdir)
            print(json.dumps(man, indent=2))
        else:
            print(f"unknown command {cmd!r}")
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))