#!/usr/bin/env python
"""Calibrate SysML v2 textual forms against sysmlpy (authoritative reader).

Each snippet is written to a temp file and parsed with sysmlpy.load.
Prints accept/reject per form so the emitter only produces parseable text.
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path.home() / "sysmlpy" / "src"))
from sysmlpy import load  # noqa: E402

SNIPPETS = {
    # connections
    "connection def": "package P { connection def C1; }",
    "connection def ends": "package P { part def B2; connection def C1 { end e1 : B2; end e2 : B2; } }",
    "connection usage": "package P { part def B2; part def B1 { part p1 : B2; part p2 : B2; connection c1 connect p1 to p2; } }",
    "connect bare": "package P { part def B2; part def B1 { part p1 : B2; part p2 : B2; connect p1 to p2; } }",
    "binding": "package P { part def B1 { part p1; part p2; binding b1 bind p1 = p2; } }",
    "bind bare": "package P { part def B1 { part p1; part p2; bind p1 = p2; } }",
    # ports / items
    "port def": "package P { port def IB1; }",
    "port typed": "package P { port def IB1; part def B1 { port p1 : IB1; } }",
    "port untyped": "package P { part def B1 { port p2; } }",
    "item def": "package P { item def Sig1; }",
    "item usage": "package P { item def Sig1; part def B1 { item s1 : Sig1; } }",
    # requirements
    "requirement id angle": "package P { requirement <'R-1'> Req1 { doc /* x */ } }",
    "verification def return": "package P { verification def TC1 { return verdict : VerificationCases::VerdictKind; } }",
    "verification def objective": "package P { requirement Req1; verification def TC1 { objective o1 { verify Req1; } return verdict : VerificationCases::VerdictKind; } }",
    "verify bare": "package P { requirement Req1; verification def TC1 { verify Req1; } }",
    # derive / dependency
    "derive connection": "package P { requirement R1; requirement R2; connection : DerivationConnections::Derivation connect R2 to R1; }",
    "dependency from to": "package P { part def A; requirement R1; dependency from A to R1; }",
    "dependency named": "package P { part def A; requirement R1; dependency d1 from A to R1; }",
    # behaviors
    "action def params": "package P { action def A1 { in p : Integer; out q; } }",
    "perform action": "package P { part def B1 { perform action op1 { in p : Integer; out result : Integer; } } }",
    "action def return": "package P { action def A1 { return r : Integer; } }",
    "action usage bare": "package P { action def A1; part def B1 { action a1 : A1; } }",
    # state machines
    "state def": "package P { state def SM1 { state s1; state s2; } }",
    "transition first to": "package P { state def SM1 { state s1; state s2; transition t1 first s1 to s2; } }",
    "transition named source target": "package P { state def SM1 { state s1; state s2; transition t1 from s1 to s2; } }",
    "transition entry do": "package P { state def SM1 { state s1; transition t1 first s1; } }",
    # packages / imports
    "import members": "package P { package Q; import Q::*; }",
    "import single": "package P { package Q; import Q::C; }",
    # occurrences (plain classes)
    "occurrence def": "package P { occurrence def C1; }",
    "occurrence usage": "package P { occurrence def C1; part def B1 { occurrence o1 : C1; ref occurrence ro1 : C1; } }",
    # metadata annotation
    "metadata def": "package P { metadata def RefineData { attribute isRefine : Boolean; } }",
    "dependency annotated": "package P { metadata def RefineData { attribute isRefine : Boolean; } part def A; requirement R1; dependency from A to R1 { @RefineData { isRefine = true; } } }",
}


def main():
    ok, bad = [], []
    for label, text in SNIPPETS.items():
        with tempfile.NamedTemporaryFile("w", suffix=".sysml", delete=False) as fp:
            fp.write(text)
            path = fp.name
        try:
            with open(path) as fh:
                counts = load(fh).count()
            ok.append(label)
            print(f"  ACCEPT  {label:34s} {counts}")
        except Exception as e:  # noqa: BLE001
            bad.append(label)
            print(f"  REJECT  {label:34s} {type(e).__name__}: {str(e)[:110]}")
        finally:
            Path(path).unlink(missing_ok=True)
    print(f"\naccepted {len(ok)}, rejected {len(bad)}")


if __name__ == "__main__":
    main()