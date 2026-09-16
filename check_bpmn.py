#!/usr/bin/env python
"""Checks for the generated BPMN 2.0.2 metamodel (gen/bpmn.py, from CMOF)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen.bpmn as B  # noqa: E402
import gen.uml25 as U  # noqa: E402

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))


print("== counts ==")
check("137 BPMN classes", len(B._CLASSES) == 137, f"{len(B._CLASSES)}")
check("9 enumerations",
      sum(1 for n in dir(B) if isinstance(getattr(B, n), type)
          and issubclass(getattr(B, n), __import__("enum").Enum)
          and getattr(B, n).__module__ == "gen.bpmn") == 9)
check("193 associations in _ASSOCIATIONS", len(B._ASSOCIATIONS) == 193)
check("class_of lookup", B.class_of("ExclusiveGateway").__name__ == "ExclusiveGateway")

print("== hierarchy (superClass attributes, multi-inheritance) ==")
check("Task <: Activity <: FlowNode <: FlowElement <: BaseElement",
      issubclass(B.Task, B.Activity) and issubclass(B.Activity, B.FlowNode)
      and issubclass(B.FlowNode, B.FlowElement)
      and issubclass(B.FlowElement, B.BaseElement))
check("Task folds Activity + InteractionNode (two superClasses)",
      any(k.__name__ == "InteractionNode" for k in B.Task.__mro__))
check("BPMN classes are NOT UML Elements",
      not isinstance(B.Task(), U.Element) and not issubclass(B.BaseElement, U.Element))
check("mixin base is _MOFBase", issubclass(B.BaseElement, B._MOFBase))

print("== instantiation / properties ==")
p = B.Process(name="P1", isExecutable=True, processType=B.ProcessType.Public)
check("Process kw construction", p.name == "P1" and p.isExecutable is True
      and p.processType is B.ProcessType.Public)
p.add("flowElements", B.Task(name="T1"), B.SequenceFlow(name="SF"))
check("multi ref add/list", [e.name for e in p.flowElements] == ["T1", "SF"])
check("flowElements is multi/composite on FlowElementsContainer",
      "flowElements" in B.Process._props
      and B.Process._props["flowElements"].multi
      and B.Process._props["flowElements"].composite)
t = B.Task(name="T2")
check("concrete Task instantiable with inherited _props",
      t.name == "T2" and t.incoming == [] and t.outgoing == [])
guarded = False
try:
    B.BaseElement()
except TypeError:
    guarded = True
check("abstract BaseElement raises TypeError", guarded)
guarded = False
try:
    B.CatchEvent()
except TypeError:
    guarded = True
check("abstract CatchEvent guarded", guarded)

print("== enumerations ==")
check("GatewayDirection literals",
      [l.value for l in B.GatewayDirection]
      == ["Unspecified", "Converging", "Diverging", "Mixed"])
check("'None' literal keyword-guarded (ProcessType.None_)",
      B.ProcessType.None_.value == "None")

print("== descriptors / opposites ==")
check("opposite wiring both directions",
      B.CatchEvent._DECL["dataOutputAssociation"].opp == "catchEvent"
      and B.DataOutputAssociation._DECL["catchEvent"].opp
      == "dataOutputAssociation")
check("multi flags (dataOutputAssociations 0..*, parallelMultiple 1..1)",
      B.Activity._DECL["dataOutputAssociations"].multi
      and not B.CatchEvent._DECL["parallelMultiple"].multi)
check("composite flags carried",
      B.Process._props["flowElements"].composite
      and B.CatchEvent._DECL["dataOutputAssociation"].composite)
check("derived properties marked read-only",
      sum(1 for c in B._CLASSES for d in c.__dict__.get("_DECL", {}).values()
          if d.derived) == 10)
check("MOF DOM Element types late-bound as strings",
      sum(1 for c in B._CLASSES for d in c.__dict__.get("_DECL", {}).values()
          if d.t == "xml.dom.Element") == 8)
check("external BPMNDI ref package-qualified",
      B.Definitions._DECL["diagrams"].t == "BPMNDI.BPMNDiagram"
      and B.Definitions._DECL["diagrams"].multi)
check("primitive types map to Python builtins",
      B.BaseElement._DECL["id"].t is str
      and B.CatchEvent._DECL["parallelMultiple"].t is bool)

print("== separation from UML machinery ==")
check("gen.bpmn does not collide with gen.uml25 class objects",
      B.Event is not U.Event and B.Association is not U.Association)
check("_finish assembled _props across MRO",
      B.Task._props["documentation"].name == "documentation")

print()
print(f"RESULT: {len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)