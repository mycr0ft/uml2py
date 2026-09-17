#!/usr/bin/env python
"""E5 checks: CMOF writer (mm_write.py) over the BPMN 2.0.2 metamodel.

Oracles:
  1. canonical structural parity: write(gen.bpmn) vs the OMG-published
     BPMN20.cmof, with Package.ownedMember order normalized as a multiset
     (MOF ownedMember is a set; the file's member order is hand-edited);
  2. structural round-trip: re-parsing the written file with the
     generator's parse must reproduce the same classes, associations and
     serialization metadata as parsing the original.
Run under ~/ams-gra-sim/.venv (lxml)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import canon  # noqa: E402
import generate_bpmn as G  # noqa: E402
import gen.bpmn as B  # noqa: E402
import mm_write  # noqa: E402

SRC = "/mnt/TBFox/uml_xmi/BPMN20.cmof"
RT = "/tmp/bpmn20_roundtrip.cmof"

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))


print("== generated-module serialization table (_SYNTH) ==")
synth = B._SYNTH
check("gen.bpmn carries the _SYNTH table",
      isinstance(synth, dict)
      and {"package", "tags", "hrefs", "ends", "props", "synth_attrs"}
      <= set(synth))
check("package metadata", synth["package"]
      == {"name": "BPMN20",
          "uri": "http://www.omg.org/spec/BPMN/20100524/MODEL-XMI"})
check("two tags (nsPrefix bpmn, nsURI MODEL-XMI)",
      synth["tags"] == (("org.omg.xmi.nsPrefix", "bpmn", "_0"),
                        ("org.omg.xmi.nsURI",
                         "http://www.omg.org/spec/BPMN/20100524/MODEL-XMI",
                         "_0")))
check("href table has the five verbatim forms",
      synth["hrefs"]["String"] == "http://schema.omg.org/spec/MOF/2.0/cmof.xml#String"
      and synth["hrefs"]["BPMNDI.BPMNDiagram"] == "BPMNDI.cmof#BPMNDiagram"
      and len(synth["hrefs"]) == 5)
check("177 association-owned ends recorded",
      len(synth["ends"]) == 177
      and all(len(v) == 6 for v in synth["ends"].values()))
check("316 class-side properties serialized (155 synthesized excluded)",
      len(synth["props"]) == 316 and len(synth["synth_attrs"]) == 155)

print("== write / determinism ==")
data = mm_write.write_cmof(B)
data2 = mm_write.write_cmof(B)
check("writer is deterministic (byte-identical)", data == data2)
open(RT, "wb").write(data)

print("== canonical parity vs the OMG original ==")
diffs = canon.compare(SRC, RT, multiset_features={"ownedMember"})
check("canon(BPMN20.cmof, written) empty", not diffs, str(diffs[:1]))

print("== structural counts (both files) ==")
from lxml import etree  # noqa: E402
X = "{http://schema.omg.org/spec/XMI/2.1}"
tr = etree.parse(RT)
oms = tr.getroot()[0].findall("*")
kinds = [om.get(X + "type") for om in oms]
check("339 ownedMembers: 137 Class + 9 Enumeration + 193 Association",
      len(oms) == 339
      and kinds.count("cmof:Class") == 137
      and kinds.count("cmof:Enumeration") == 9
      and kinds.count("cmof:Association") == 193)
props = [a for om in oms for a in om.findall("{*}ownedAttribute")]
ends_ = [e for om in oms for e in om.findall("{*}ownedEnd")]
lits = [l for om in oms for l in om.findall("{*}ownedLiteral")]
check("493 properties (316 class-side + 177 ends), 28 literals, 2 tags",
      len(props) == 316 and len(ends_) == 177 and len(lits) == 28
      and len(tr.getroot().findall("{http://schema.omg.org/spec/MOF/2.0/cmof.xml}Tag")) == 2)
# no synthesized class attribute reaches the file
skipped = {k.replace(".", "-") for k in synth["synth_attrs"]}
written_attr_ids = {a.get(X + "id") for a in props}
check("synthesized ids absent from written ownedAttributes",
      not (skipped & written_attr_ids), f"{len(skipped)} skipped")
ends_ids = {e.get(X + "id") for e in ends_}
check("every synthesized back-ref's association has its ownedEnd",
      all(a in synth["ends"] for a in synth["synth_attrs"].values()))
check("association attribute on exactly the 209 memberEnd class props",
      sum(1 for a in props if a.get("association")) == 209
      and all(a.get("association") for a in props
              if a.get(X + "id") in
              {r for pair in B._ASSOCIATIONS.values() for r in pair
               if not r.startswith("A_")}))
check("memberEnd strings verbatim (193)",
      all(" ".join(B._ASSOCIATIONS[a.get("name")]) == a.get("memberEnd")
          for a in [om for om in oms
                    if om.get(X + "type") == "cmof:Association"]))
check("hrefs verbatim",
      sorted(e.get("href") for e in tr.getroot().iter() if e.get("href"))
      == sorted(e.get("href") for e in etree.parse(SRC).getroot().iter()
                if e.get("href")))
check("multi-superClass preserved (Process = FlowElementsContainer CallableElement)",
      next(om for om in oms if om.get("name") == "Process")
      .get("superClass") == "FlowElementsContainer CallableElement")

print("== structural round-trip through the generator's parse ==")
c1, a1, w1, m1 = G.parse_cmof(SRC)
c2, a2, w2, m2 = G.parse_cmof(RT)
check("re-parsed classes identical", c1 == c2)
check("re-parsed associations identical", a1 == a2)
check("re-parsed package/tags/hrefs/ends identical", m1 == m2)
check("no warnings from either parse", not w1 and not w2)

print()
print(f"RESULT: {len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)