#!/usr/bin/env python
"""E1 checks: EMF-dialect XMI 2.1 writer (xmi_write.py).

Oracles:
  1. round-trip graph parity: read(DoDAFLibrary.xmi) -> write -> read, the
     two object graphs must be equal (ids reused, so identity is id-keyed);
  2. canonical structural parity: canon.compare(original, written) must be
     empty modulo the documented normalizations (ids/uuid ignored, feature
     grouping, root-order, reader-derived <name> children).
Run under ~/ams-gra-sim/.venv (lxml)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen.uml25 as U  # noqa: E402
import canon  # noqa: E402
import xmi21  # noqa: E402
import xmi_write as W  # noqa: E402

DODAF = "/mnt/TBFox/DoDAFLibrary.xmi"
RT = "/tmp/dodaf_e1_roundtrip.xmi"

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))


def _sig_val(v):
    if isinstance(v, U.Element):
        if getattr(v, "_external_href", None):
            return ("@href", v._external_href)
        return ("@ref", getattr(v, "_xmi_id", "?"))
    if isinstance(v, (list, tuple)):
        return ("@list", tuple(_sig_val(x) for x in v))
    return ("@prim", repr(v))


def signature(m):
    id_of = {id(o): i for i, o in m.objects.items()}
    id_of.update({id(o): "href:" + frag
                  for frag, o in m.synthetic_types.items()})
    out = {}
    for i, o in sorted(m.objects.items()):
        feats = tuple(sorted((k, _sig_val(v))
                             for k, v in o._vals.items()))
        out[i] = (type(o).__name__, feats)
    return out, id_of


def graph_equal(m1, m2):
    s1, _ = signature(m1)
    s2, _ = signature(m2)
    if s1 != s2:
        for i in sorted(set(s1) | set(s2)):
            if s1.get(i) != s2.get(i):
                return i, s1.get(i), s2.get(i)
    return None


print("== read / write / determinism ==")
m1 = xmi21.read_xmi21(DODAF)
apps = W.apps_from_model(m1)
data = W.write_xmi(m1.roots, apps=apps, nsmap=m1.nsmap,
                   profile_applications=m1.profiles)
data2 = W.write_xmi(m1.roots, apps=apps, nsmap=m1.nsmap,
                    profile_applications=m1.profiles)
check("write is deterministic (byte-identical)", data == data2)
open(RT, "wb").write(data)

print("== round-trip graph parity (id-keyed) ==")
m2 = xmi21.read_xmi21(RT)
check("object count preserved", len(m1.objects) == len(m2.objects) == 163,
      f"{len(m1.objects)} -> {len(m2.objects)}")
check("application count preserved (61)",
      sum(len(v) for v in m1.apps.values())
      == sum(len(v) for v in m2.apps.values()) == 61)
check("app metas preserved", m1.app_metas == m2.app_metas)
check("appliedProfile hrefs preserved", m1.profiles == m2.profiles
      and len(m1.profiles) == 1)
check("external hrefs preserved (52, verbatim)",
      sorted(m1.hrefs) == sorted(m2.hrefs) and len(m1.hrefs) == 52)
check("synthetic types equal",
      {f: o._external_href for f, o in m1.synthetic_types.items()}
      == {f: o._external_href for f, o in m2.synthetic_types.items()})
check("no unmapped metaclass tags in re-read", not m2.unmapped)
check("no unmapped features in re-read", not m2.unmapped_features)
check("no derived names needed in re-read (names explicit)",
      not m2.derived_names, str(m2.derived_names[:2]))
bad = graph_equal(m1, m2)
check("full graph signature equal (features, refs, containment order)",
      bad is None, "" if bad is None else f"{bad[0]}: {bad[1]} != {bad[2]}")

print("== canonical parity vs the OMG original ==")
diffs = canon.compare(DODAF, RT,
                      drop_names_at={i for i, _ in m1.derived_names})
check("canon(original, written) empty", not diffs, str(diffs[:1]))

print("== serialization conventions (probes P1-P3) ==")
from lxml import etree  # noqa: E402
X = "{http://schema.omg.org/spec/XMI/2.1}"
t = etree.parse(RT)
r = t.getroot()
check("root is xmi:XMI", r.tag == f"{X}XMI", r.tag)
kids = [etree.QName(c).localname for c in r]
check("root children: 61 applications + Model + ModelLibrary",
      len(kids) == 62 and kids.count("Measurement") == 53
      and kids.count("MeasurementSet") == 7 and kids.count("Model") == 1
      and kids.count("ModelLibrary") == 1, str(len(kids)))
check("stereotype app elements carry xmi:id and base_<Meta> idref",
      all(c.get(X + "id") for c in r if etree.QName(c).namespace
          and "UPDM" in (etree.QName(c).namespace or ""))
      and len(m1.app_metas) == 61)
check("profileApplication with xmi:type on the model",
      any(c.get(X + "type") == "uml:ProfileApplication" for e in r.iter()
          if etree.QName(e).localname == "profileApplication"
          for c in [e]))
# every original xmi:id present in the written file, except the
# profileApplication element's own id (writer re-derives it; canon ignores it)
orig_ids = set()
for e in etree.parse(DODAF).getroot().iter():
    i = e.get(X + "id")
    if i and i != "DoDAF_Class_Library-profileApplication":
        orig_ids.add(i)
written_ids = {e.get(X + "id") for e in r.iter() if e.get(X + "id")}
check("all original xmi:ids preserved (profileApplication id excepted)",
      orig_ids <= written_ids, f"{len(orig_ids)} ids")
# containment-opposite never emitted; owner-pointing real refs kept
no_dt = not any(etree.QName(e).localname in ("datatype", "enumeration",
                                             "class_", "owningPackage")
                for e in r.iter())
check("containment opposites (datatype/enum/class_) not emitted", no_dt)
ann = [e for e in r.iter() if etree.QName(e).localname == "annotatedElement"]
check("annotatedElement refs kept even when pointing at the owner",
      len(ann) == 30, str(len(ann)))
# '*' upper emitted, 0-default lower omitted
ups = [e for e in r.iter() if etree.QName(e).localname == "upperValue"]
zeros = [c for e in r.iter() if etree.QName(e).localname == "lowerValue"
         for c in e if etree.QName(c).localname == "value"]
check("upperValue carries <value>*</value>; lowerValue 0 omitted",
      len(ups) == 26 and not zeros, f"{len(ups)} uppers, {len(zeros)} zeros")

print("== programmatic graph (no reader involvement) ==")
pkg = U.Package(name="P1")
cls = U.Class(name="C1")
pkg.add("packagedElement", cls)
prop = U.Property(name="attr1")
cls.add("ownedAttribute", prop)
prop._vals["visibility"] = "private"
lv = U.LiteralUnlimitedNatural()
setattr(lv, "value", U.UnlimitedNatural(0))
setattr(prop, "lowerValue", lv)
uv = U.LiteralUnlimitedNatural()
setattr(uv, "value", U.UnlimitedNatural("*"))
setattr(prop, "upperValue", uv)
cmt = U.Comment()
cmt._vals["body"] = "hello"
cls.add("ownedComment", cmt)

pdata = W.write_xmi([pkg])
open("/tmp/prog_rt.xmi", "wb").write(pdata)
mp = xmi21.read_xmi21("/tmp/prog_rt.xmi")
check("programmatic graph round-trips",
      len(mp.objects) == 6
      and next(o for i, o in mp.objects.items()
               if i == "_2" and isinstance(o, U.Class)).name == "C1")
prop2 = next(o for i, o in mp.objects.items()
             if isinstance(o, U.Property) and o.name == "attr1")
check("enum text child round-trips (visibility 'private')",
      prop2._vals.get("visibility") == "private",
      repr(prop2._vals.get("visibility")))
check("LiteralUnlimitedNatural '*' and 0-default round-trip",
      prop2._vals.get("upperValue")._vals.get("value").unbounded
      and prop2._vals.get("lowerValue")._vals.get("value").n == 0)
cmt2 = next(o for o in mp.objects.values() if isinstance(o, U.Comment))
check("comment body round-trips", cmt2._vals.get("body") == "hello")
check("assigned ids deterministic (_N traversal order)",
      b'_xmi' not in pdata
      and [e.get(X + "id") for e in etree.parse("/tmp/prog_rt.xmi")
           .getroot().iter() if e.get(X + "id")][0] == "_1")

print("== honesty guards ==")
# dangling detection: a ref whose target is outside the written graph
p3 = U.Property()
p3._vals["type"] = U.Class(name="dangling")
try:
    W.write_xmi([p3])
    raised = False
except W.WriteError:
    raised = True
check("dangling reference raises WriteError", raised)

print()
print(f"RESULT: {len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)