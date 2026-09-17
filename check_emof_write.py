#!/usr/bin/env python
"""E6 checks: EMOF writer (mm_write.write_emof) over a trimmed BPMN 2.0.2
metamodel subset.

Oracles (verification-grade, clearly labeled - see REPORT Part 14):
  1. spec-rule conformance: MOF 2.0/XMI Mapping v2.1 section 6.5.2 -
     derived information not serialized, default values not serialized,
     no Association serialization (EMOF has none), composite opposites
     not serialized;
  2. determinism;
  3. semantic round-trip: a minimal EMOF reader reconstructs the
     subset's classes/supers/attributes/multiplicities from the file;
  4. dialect parallelism with the CMOF writer for the same subset.
Standard library except lxml. Run under ~/ams-gra-sim/.venv."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen.bpmn as B  # noqa: E402
import mm_write  # noqa: E402

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))


NAMES = ["FlowNode", "SequenceFlow", "Gateway", "ExclusiveGateway",
         "Task", "Process", "DataInput", "FormalExpression"]
SEL = [getattr(B, n) for n in NAMES]

data = mm_write.write_emof(B, SEL)
data2 = mm_write.write_emof(B, SEL)
open("/tmp/bpmn_subset.emof", "wb").write(data)

print("== writer / determinism ==")
check("write_emof is deterministic (byte-identical)", data == data2)

print("== namespace and element pins ==")
check("root xmi:XMI with XMI 2.1 + emof namespaces",
      data.startswith(b"<?xml version='1.0' encoding='UTF-8'?>\n<xmi:XMI")
      and 'xmlns:xmi="http://schema.omg.org/spec/XMI/2.1"' in data.decode()
      and 'xmlns:emof="http://schema.omg.org/spec/MOF/2.0/emof.xml"'
      in data.decode())
from lxml import etree  # noqa: E402
root = etree.parse("/tmp/bpmn_subset.emof").getroot()
E = "{http://schema.omg.org/spec/MOF/2.0/emof.xml}"
X = "{http://schema.omg.org/spec/XMI/2.1}"
pkg = root.find(f"{E}Package")
oms = pkg.findall("ownedMember")
kinds = [om.get(X + "type") for om in oms]
check("Package with 10 members: 8 classes + 2 enums",
      pkg.get("name") == "BPMN20" and pkg.get(X + "id") == "_0"
      and kinds.count("emof:Class") == 8
      and kinds.count("emof:Enumeration") == 2
      and len(oms) == 10)
check("tags serialize as emof:Tag (nsPrefix/nsURI), ids _1/_2",
      [t.get(X + "id") for t in root.findall(f"{E}Tag")] == ["_1", "_2"]
      and [t.get("name") for t in root.findall(f"{E}Tag")]
      == ["org.omg.xmi.nsPrefix", "org.omg.xmi.nsURI"])

print("== EMOF 6.5.2 suppression rules ==")
check("no Association serialization anywhere (EMOF has none)",
      not any("memberEnd" in d or "ownedEnd" in d
              for d in data.decode().split("<")),
      "memberEnd/ownedEnd absent")
check("association/derived-union properties absent "
      "(association is derived; synthesized back-refs skipped)",
      not any(a.get("association") for a in root.iter("ownedAttribute"))
      and not any(a.get("name") == "inputSetRefs"
                  for a in root.iter("ownedAttribute")))
fn0 = next(om for om in oms if om.get("name") == "FlowNode")
outg = next(a for a in fn0.findall("ownedAttribute")
            if a.get("name") == "outgoing")
check("isOrdered=true survives, false defaults suppressed",
      outg.get("isOrdered") == "true"
      and not any(a.get("isOrdered") == "false"
                  for a in root.iter("ownedAttribute"))
      and not any(a.get("isComposite") == "false"
                  for a in root.iter("ownedAttribute"))
      and not any(a.get("isDerived") for a in root.iter("ownedAttribute")))
check("visibility public suppressed (MOF default)",
      not any(a.get("visibility") == "public"
              for a in root.iter("ownedAttribute")))
proc = next(om for om in oms if om.get("name") == "Process")
check("superClass preserved verbatim",
      proc.get("superClass") == "FlowElementsContainer CallableElement")
fn = next(om for om in oms if om.get("name") == "FlowNode")
gw = next(om for om in oms if om.get("name") == "Gateway")
task = next(om for om in oms if om.get("name") == "Task")
check("isAbstract=true serialized; false omitted (Task)",
      fn.get("isAbstract") == "true" and gw.get("isAbstract") == "true"
      and "isAbstract" not in task.attrib)

print("== property forms ==")
check("primitive types by emof.xml href",
      any(t.get("href") == "http://schema.omg.org/spec/MOF/2.0/emof.xml#String"
          for t in root.iter("type"))
      and any(t.get("href") == "http://schema.omg.org/spec/MOF/2.0/emof.xml#Boolean"
              for t in root.iter("type")))
check("class/enum types by name attribute",
      outg.get("type") == "SequenceFlow"
      and next(a for a in root.iter("ownedAttribute")
               if a.get("name") == "gatewayDirection").get("type")
      == "GatewayDirection")
check("external MOF Element href verbatim (cmof.xml#Element)",
      any(t.get("href") == "http://schema.omg.org/spec/MOF/2.0/cmof.xml#Element"
          for t in root.iter("type")))
lits = [l for om in oms for l in om.findall("ownedLiteral")]
check("literals with ids/names only (composite opposites suppressed)",
      len(lits) == 7
      and all(l.get("name") and l.get(X + "id") for l in lits)
      and not any(l.get("enumeration") for l in lits))

print("== semantic round-trip (minimal EMOF reader) ==")
readback = {}
for om in oms:
    if om.get(X + "type") == "emof:Class":
        attrs = {}
        for a in om.findall("ownedAttribute"):
            t = a.find("type")
            tv = (t.get("href").split("#")[-1] if t is not None
                  else a.get("type"))
            attrs[a.get("name")] = (a.get("lower"), a.get("upper"),
                                    a.get("isComposite"), a.get("default"), tv)
        readback[om.get("name")] = (om.get("superClass"), attrs)
src = {}
for cls in SEL:
    attrs = {}
    for aname, d in cls.__dict__.get("_DECL", {}).items():
        if f"{cls.__name__}.{aname}" in B._SYNTH["synth_attrs"]:
            continue
        if d.derived or d.union:
            continue
        lraw, uraw, vis, ordered, default = \
            B._SYNTH["props"][f"{cls.__name__}.{aname}"]
        tname = ({"str": "String", "bool": "Boolean",
                  "int": "Integer"}[d.t.__name__]
                 if isinstance(d.t, type)
                 else "Element" if d.t == "xml.dom.Element" else d.t)
        attrs[aname] = (lraw, uraw, "true" if d.composite else None,
                        default, tname)
    supers = " ".join(b.__name__ for b in cls.__bases__
                      if b.__name__ != "_MOFBase")
    src[cls.__name__] = (supers, attrs)
norm = lambda v: v if v not in (None, "1") else None  # noqa: E731
match, diff = True, ""
for n, (supers, attrs) in src.items():
    r_supers, r_attrs = readback[n]
    if (supers or None) != (r_supers or None):
        match, diff = False, f"superClass {n}"
        break
    for an, (lo, hi, comp, dflt, tn) in attrs.items():
        rlo, rhi, rcomp, rdflt, rtn = r_attrs[an]
        if (norm(lo), norm(hi), norm(dflt)) != (norm(rlo), norm(rhi),
                                                norm(rdflt)):
            match, diff = False, f"{n}.{an} {lo}..{hi} vs {rlo}..{rhi}"
            break
        if tn != rtn or norm(comp) != norm(rcomp):
            match, diff = False, f"{n}.{an} type {tn} vs {rtn}"
            break
    if not match:
        break
check("round-trip: classes/supers/attrs/multiplicities reconstructed equal",
      match, diff)

print("== dialect parallelism with the CMOF writer ==")
cmof = mm_write.write_cmof(B)
croot = etree.fromstring(cmof)
c_oms = [om for om in croot[0].findall("*")
         if om.get("name") in {n for n in NAMES}]
check("same subset names in both dialects",
      {om.get("name") for om in oms if om.get(X + "type") == "emof:Class"}
      == {om.get("name") for om in c_oms
          if om.get(X + "type") == "cmof:Class"})
c_proc = next(om for om in c_oms if om.get("name") == "Process")
check("multi-superClass identical across dialects",
      c_proc.get("superClass") == proc.get("superClass")
      == "FlowElementsContainer CallableElement")
c_outg = next(a for a in next(om for om in c_oms
                              if om.get("name") == "FlowNode")
              .findall("{*}ownedAttribute") if a.get("name") == "outgoing")
check("the one isOrdered property agrees (FlowNode.outgoing)",
      c_outg.get("isOrdered") == outg.get("isOrdered") == "true")

print()
print(f"RESULT: {len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)