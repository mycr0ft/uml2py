#!/usr/bin/env python
"""Generate Python BPMN 2.0.2 metamodel classes from the OMG CMOF XMI.

OMG does not publish BPMN as a UML-profile XMI; the machine-readable
metamodel ships as CMOF (MOF 2.0 XMI):
https://www.omg.org/spec/BPMN/20100501/BPMN20.cmof

CMOF dialect handled here (distinct from the UML 2.5.1 EMF dialect):
- generalization via space-separated `superClass` attributes, not
  <generalization> elements;
- class-side properties as <ownedAttribute> carrying the full
  multiplicity (216 attrs default to 1..1, 99 carry upper='*', 96 are
  composite, 10 derived, 27 carry literal defaults). CMOF defaults:
  absent upper -> 1; absent lower -> 0 when upper='*' (all such
  attributes are 0..* in the normative BPMN prose), else 1;
- associations as memberEnd name-pairs: one end is class-owned
  ("Class-endName"), the opposite may also be class-owned (wired as
  an opposite) or association-owned ("AssocId-endName"), in which
  case it is synthesized onto the partner class (mirroring
  gen/uml25.py's hidden-end closure);
- primitive types by href into the CMOF namespace (String/Boolean/
  Integer), MOF DOM Element by href, and one external BPMNDI.cmof
  href kept as a late-bound string.

The emitted gen/bpmn.py reuses gen.uml25's _Ref/_RefList descriptors
(their wiring hooks are UML-scoped and no-op for BPMN instances) on a
local _MOFBase base - BPMN classes are deliberately NOT UML Elements.

Usage: <venv-with-lxml>/bin/python generate_bpmn.py
Writes: gen/bpmn.py and bpmn_stats.json
"""
import json
import re
from pathlib import Path

from lxml import etree

HERE = Path(__file__).resolve().parent
CMOF = Path("/mnt/TBFox/uml_xmi/BPMN20.cmof")

X_TYPE = "{http://schema.omg.org/spec/XMI/2.1}type"
X_ID = "{http://schema.omg.org/spec/XMI/2.1}id"
CMOF_PRIMS = {"String": "str", "Boolean": "bool", "Integer": "int"}


def safe_name(n):
    n = re.sub(r"\W", "_", n)
    if n[0].isdigit():
        n = "_" + n
    return n + "_" if n in KEYWORDS else n


KEYWORDS = {
    "False", "None", "True", "and", "as", "assert", "async", "await", "break",
    "class", "continue", "def", "del", "elif", "else", "except", "finally",
    "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal",
    "not", "or", "pass", "raise", "return", "try", "while", "with", "yield",
}


def dq(t):
    return t.replace("\\", "\\\\").replace('"', '\\"')


def prop_type(a):
    """(tkind, tname) for a cmof property."""
    t = a.get("type")
    if t:
        return "cls", t
    ty = a.find("*")
    if ty is not None and ty.get("href"):
        frag = ty.get("href").split("#")[-1]
        if frag in CMOF_PRIMS:
            return "prim", frag
        if frag == "Element":
            return "dom", "xml.dom.Element"   # MOF Element (DOM), late-bound
        pkg = ty.get("href").split("#")[0].rsplit("/", 1)[-1].replace(".cmof", "")
        return "ext", f"{pkg}.{frag}"         # e.g. BPMNDI.BPMNDiagram
    return "untyped", None


def parse_cmof(path):
    """(classes, associations, warns, meta) from the CMOF package.

    classes: name -> dict(name, supers=[...], abstract=bool, attrs=[...],
    byname={}); an attr dict carries name/tkind/tname/multi/lo/hi/
    derived/composite/assocname/default/opps/synthesized plus the raw
    serialization forms (lraw/uraw/vis/ordered/href) mirrored into _SYNTH.
    Enumerations are stored as dict(name, enum=[literals], ...).
    associations: name -> (end1, end2) raw memberEnd strings.
    meta: package attrs, tags, hrefs (frag -> verbatim href), ends
    (assoc-owned ownedEnd records), synth_attrs (class-side attrs the
    generator created; absent from the file).
    """
    r = etree.parse(str(path)).getroot()
    pkg = r[0]
    classes, assocs, warns = {}, {}, []
    hrefs = {}
    ends_by_assoc = {}
    tags = [(t.get("name"), t.get("value"), t.get("element"))
            for t in r.findall("{http://schema.omg.org/spec/MOF/2.0/cmof.xml}Tag")]

    for om in pkg.findall("*"):
        if om.get(X_TYPE) == "cmof:Class":
            c = dict(name=om.get("name"),
                     supers=(om.get("superClass") or "").split(),
                     abstract=om.get("isAbstract") == "true",
                     attrs=[], byname={})
            for a in om.findall("{*}ownedAttribute"):
                tkind, tname = prop_type(a)
                ty = a.find("*")
                thref = ty.get("href") if ty is not None else None
                if thref:
                    frag = thref.split("#")[-1]
                    hrefs[tname if tkind == "ext" else frag] = thref
                up = a.get("upper")
                lo = a.get("lower")
                multi = up == "*" or (up and up.isdigit() and int(up) > 1)
                lo_i = int(lo) if lo is not None else (0 if up == "*" else 1)
                hi = up if up is not None else "1"
                c["attrs"].append(dict(
                    name=a.get("name"), tkind=tkind, tname=tname,
                    multi=multi, lo=lo_i, hi=hi,
                    derived=a.get("isDerived") == "true",
                    composite=a.get("isComposite") == "true",
                    assocname=a.get("association"),
                    default=a.get("default"),
                    lraw=lo, uraw=up, vis=a.get("visibility"),
                    ordered=a.get("isOrdered"), href=thref))
                c["byname"][a.get("name")] = c["attrs"][-1]
            classes[om.get("name")] = c
        elif om.get(X_TYPE) == "cmof:Enumeration":
            lits = [l.get("name") for l in om.findall("{*}ownedLiteral")]
            classes[om.get("name")] = dict(name=om.get("name"), enum=lits,
                                           supers=[], abstract=False, attrs=[])

    for om in pkg.findall("*"):
        if om.get(X_TYPE) != "cmof:Association":
            continue
        aname = om.get("name")
        refs = (om.get("memberEnd") or "").split()
        owned = {e.get(X_ID): e for e in om.findall("{*}ownedEnd")}
        class_ends, assoc_ends = [], []
        for ref in refs:
            e = owned.get(ref)
            if e is not None:
                assoc_ends.append(dict(
                    name=e.get("name"), type=e.get("type"),
                    lo=int(e.get("lower", 1)) if e.get("lower")
                    else (0 if e.get("upper") == "*" else 1),
                    hi=e.get("upper") or "1",
                    lraw=e.get("lower"), uraw=e.get("upper"),
                    vis=e.get("visibility"),
                    derived=e.get("isDerived") == "true"))
            elif "-" in ref:
                cls, pname = ref.split("-", 1)
                if cls not in classes:
                    warns.append(f"{aname}: class-owned end {ref!r} unresolved")
                    continue
                class_ends.append((cls, pname))
            else:
                warns.append(f"{aname}: memberEnd {ref!r} unresolved")
        for cls, pname in class_ends:
            a = classes[cls]["byname"].get(pname)
            if a is not None and not a.get("assocname"):
                a["assocname"] = aname
        if len(class_ends) == 2:
            (c1, p1), (c2, p2) = class_ends
            for (ca, pa), (cb, pb) in (((c1, p1), (c2, p2)), ((c2, p2), (c1, p1))):
                a = classes[ca]["byname"].get(pa)
                if a is not None:
                    a.setdefault("opps", []).append(pb)
        elif len(class_ends) == 1 and len(assoc_ends) == 1:
            c1, p1 = class_ends[0]
            e2 = assoc_ends[0]
            a = classes[c1]["byname"].get(p1)
            if a is not None:
                a.setdefault("opps", []).append(e2["name"])
                a["assocname"] = a.get("assocname") or aname
                partner = a["tname"]
                pc = classes.get(partner)
                if partner and partner in classes and "enum" not in pc \
                        and not (partner == c1 and e2["name"] == p1):
                    back = pc["byname"].get(e2["name"])
                    if back is not None:
                        # both ends serialized as class attributes:
                        # wire the opposite side
                        if p1 not in back.get("opps", []):
                            back.setdefault("opps", []).append(p1)
                        if not back.get("assocname"):
                            back["assocname"] = aname
                    else:
                        back = dict(name=e2["name"], tkind="cls", tname=c1,
                                    multi=e2["hi"] == "*"
                                    or (e2["hi"].isdigit() and int(e2["hi"]) > 1),
                                    lo=e2["lo"], hi=e2["hi"], derived=False,
                                    composite=False, assocname=aname,
                                    opps=[p1], default=None,
                                    synthesized=f"association end of {aname} "
                                                f"(opposite of {c1}.{p1})")
                        pc["attrs"].append(back)
                        pc["byname"][back["name"]] = back
            elif a is None:
                warns.append(f"{aname}: class-owned end {c1}.{p1} not found")
        elif len(class_ends) == 0 and len(assoc_ends) == 2:
            pass   # both ends association-owned; carried in _ASSOCIATIONS only
        if assoc_ends:
            ends_by_assoc[aname] = assoc_ends
    for om in pkg.findall("*"):
        if om.get(X_TYPE) == "cmof:Association":
            assocs[om.get("name")] = tuple((om.get("memberEnd") or "").split())
    ends = {an: tuple(ends_by_assoc[an]) for an in ends_by_assoc}
    meta = dict(package=dict(name=pkg.get("name"), uri=pkg.get("uri")),
                tags=tuple(tags), hrefs=hrefs, ends=ends)
    return classes, assocs, warns, meta


def emit_module(classes, assocs, warns, meta):
    """Emit gen/bpmn.py: enums, topological C3-verified classes, tables."""
    enums = {n: c for n, c in classes.items() if "enum" in c}
    real = {n: c for n, c in classes.items() if "enum" not in c}
    for n, c in real.items():
        c["cls"] = None

    depth = {}
    for n, c in real.items():
        depth[n] = 0 if not c["supers"] else 1 + max(
            (depth.get(s, -1) for s in c["supers"] if s in real), default=-1)

    order, seen = [], set()

    def visit(n):
        if n in seen:
            return
        seen.add(n)
        for s in real[n]["supers"]:
            if s in real:
                visit(s)
        order.append(n)

    for n in sorted(real):
        visit(n)

    o = []
    w = o.append
    n_attrs = sum(len(c["attrs"]) for c in real.values())
    n_lits = sum(len(c["enum"]) for c in classes.values() if "enum" in c)
    w('"""BPMN 2.0.2 metamodel classes generated from the OMG CMOF XMI.')
    w("")
    w(f"{len(real)} classes, {n_attrs} attributes (including synthesized")
    w(f"association back-refs), {len(assocs)} associations, "
      f"{len(enums)} enumerations, {n_lits} literals (metadata).")
    w("Source: https://www.omg.org/spec/BPMN/20100501/BPMN20.cmof")
    w("(OMG BPMN 2.0.2). CMOF dialect: superClass attributes, memberEnd")
    w("name-pairs, href-typed primitives. The CMOF carries no OCL - BPMN")
    w("constraints are normative prose in the spec. Reuses gen.uml25's")
    w("_Ref/_RefList descriptors (their wiring hooks are UML-scoped and")
    w("no-op here); BPMN classes are deliberately NOT UML Elements.")
    w('"""')
    w("from __future__ import annotations")
    w("")
    w("import enum as _enum")
    w("")
    w("from gen.uml25 import _Ref  # noqa: F401  (descriptor machinery)")
    w("")
    w("")
    w("class _MOFBase:")
    w('    """Common base of all BPMN classes (mirrors gen.uml25._Element')
    w('    mechanics: _vals storage, _union reads, add() helper - without')
    w('    UML composite-ownership wiring)."""')
    w("    _DECL: dict = {}")
    w("    _UNIONS: dict = {}")
    w("    _ABSTRACT = False")
    w("")
    w("    def __init__(self, **kw):")
    w("        if type(self)._ABSTRACT:")
    w("            raise TypeError(")
    w("                f'{type(self).__name__} is abstract in the BPMN 2.0.2'")
    w("                f' metamodel; instantiate a concrete subclass.')")
    w("        self._vals = {}")
    w("        self._owner = None")
    w("        self._namespace = None")
    w("        self._wiring = False")
    w("        for k, v in kw.items():")
    w("            if k not in self._props:")
    w("                raise TypeError(")
    w("                f'{type(self).__name__} has no property {k!r}')")
    w("            setattr(self, k, v)")
    w("")
    w("    def _union(self, name):")
    w('        """Derived-union read: values of properties that subset it."""')
    w("        out, seen = [], set()")
    w("        for cls in type(self).__mro__:")
    w("            for contrib in getattr(cls, '_UNIONS', {}).get(name, ()):")
    w("                d = self._props.get(contrib)")
    w("                if d is None or d.union:")
    w("                    continue")
    w("                v = d.__get__(self)")
    w("                items = v if d.multi else ((v,) if v is not None else ())")
    w("                for it in items:")
    w("                    if id(it) not in seen:")
    w("                        seen.add(id(it))")
    w("                        out.append(it)")
    w("        return out")
    w("")
    w("    def add(self, name, *values):")
    w('        """Append value(s) to a multi-valued property."""')
    w("        lst = getattr(self, name)")
    w("        for v in values:")
    w("            lst.append(v)")
    w("")
    w("    def __repr__(self):")
    w("        n = self._vals.get('name')")
    w("        if isinstance(n, str) and n:")
    w("            return f'<{type(self).__name__} {n!r}>'")
    w("        return f'<{type(self).__name__} #{id(self):x}>'")
    w("")

    for ename in sorted(n for n, c in classes.items() if "enum" in c):
        lits = classes[ename]["enum"]
        if not lits:
            continue
        w(f"class {safe_name(ename)}(_enum.Enum):")
        for raw in lits:
            w(f'    {safe_name(raw)} = "{dq(raw)}"')
        w("")

    for n in order:
        c = real[n]
        base_names = [s for s in c["supers"] if s in real]
        bases = None
        if base_names:
            orders = [base_names]
            if len(base_names) <= 6:
                from itertools import permutations
                orders += [list(p) for p in permutations(base_names)
                           if list(p) != base_names]
            for od in orders:
                try:
                    type(safe_name(n),
                         tuple(real[b]["cls"] for b in od), {})
                except (TypeError, KeyError):
                    continue
                bases = od
                break
            if bases is None:
                kept, kept_cls = [], []
                for b in base_names:
                    trial = kept_cls + [real[b]["cls"]]
                    try:
                        type(safe_name(n), tuple(trial), {})
                    except (TypeError, KeyError):
                        warns.append(f"{n}: base {b} is C3-incompatible; "
                                     f"folded subset keeps {kept!r}")
                        continue
                    kept.append(b)
                    kept_cls = trial
                bases = kept
        if bases is None and base_names:
            warns.append(f"{n}: no C3-compatible base; falling back to _MOFBase")
        base_exprs = [safe_name(b) for b in (bases or [])] or ["_MOFBase"]
        # runtime class: build eagerly so later C3 verification sees it;
        # _MOFBase itself only exists in the emitted module, so runtime
        # bases are just the (already-created) superclass classes
        c["cls"] = type(safe_name(n),
                        tuple(real[b]["cls"] for b in (bases or [])), {})
        w("")
        w(f"class {safe_name(n)}(" + ", ".join(base_exprs) + "):")
        w(f"    _ABSTRACT = {str(bool(c['abstract']))}")
        opps = {}
        decl = []
        for a in c["attrs"]:
            tk, tn = a["tkind"], a["tname"]
            if tk == "prim":
                expr = CMOF_PRIMS[tn]
            elif tk == "cls":
                expr = f'"{tn}"'
            elif tk == "dom":
                expr = "'xml.dom.Element'"
            elif tk == "ext":
                expr = f"'{tn}'"
            else:
                expr = "None"
            flags = []
            if a["multi"]:
                flags.append(f"multi=True, lo={a['lo']}, hi='{a['hi']}'")
            if a["derived"]:
                flags.append("derived=True")
            if a["composite"]:
                flags.append("composite=True")
            if a.get("assocname"):
                flags.append(f'assoc="{a["assocname"]}"')
            tail = (", " + ", ".join(flags)) if flags else ""
            if a.get("synthesized"):
                w(f"    # {a['synthesized']}")
            elif a.get("default") is not None:
                w(f"    # default: {a['default']!r}")
            decl.append((a["name"], expr, tail))
            if a.get("opps"):
                opps[a["name"]] = tuple(a["opps"])
        if decl:
            w("    _DECL = {")
            for name, expr, tail in decl:
                w(f"    '{name}': _Ref('{name}', {expr}{tail}),")
            w("    }")
        if opps:
            w("    _OPPS = {")
            for k, v in opps.items():
                w(f"        '{k}': {v!r},")
            w("    }")
    w("")
    # -------------------------------------------------------------------
    # CMOF-side serialization metadata for the writer (mm_write.py):
    # the file's raw forms that the runtime _Ref tables do not carry
    # (lower/upper presence, visibility, isOrdered, defaults, tags,
    # hrefs, association-owned ends). See REPORT.md Part 11.
    # -------------------------------------------------------------------
    props = {}
    synth_attrs = {}
    for n, c in real.items():
        for a in c["attrs"]:
            key = f"{n}.{a['name']}"
            if a.get("synthesized"):
                synth_attrs[key] = a.get("assocname")
                continue
            props[key] = (a.get("lraw"), a.get("uraw"), a.get("vis"),
                          a.get("ordered"), a.get("default"))
    w("_SYNTH = {")
    w(f'    "package": {{"name": {meta["package"]["name"]!r}, '
      f'"uri": {meta["package"]["uri"]!r}}},')
    w('    "tags": (')
    for tn, tv, te in meta["tags"]:
        w(f'        ({tn!r}, {tv!r}, {te!r}),')
    w("    ),")
    w('    "hrefs": {')
    for frag, href in sorted(meta["hrefs"].items()):
        w(f'        "{dq(frag)}": "{dq(href)}",')
    w("    },")
    w('    "ends": {')
    for an in sorted(meta["ends"]):
        for e in meta["ends"][an]:
            w(f'        "{dq(an)}": ({e["name"]!r}, {e["type"]!r}, '
              f'{e["lraw"]!r}, {e["uraw"]!r}, {e["vis"]!r}, '
              f'{str(e["derived"])}),')
    w("    },")
    w('    "props": {')
    for key in sorted(props):
        t = props[key]
        w(f'        "{dq(key)}": ({t[0]!r}, {t[1]!r}, {t[2]!r}, '
          f'{t[3]!r}, {t[4]!r}),')
    w("    },")
    w('    "synth_attrs": {')
    for key in sorted(synth_attrs):
        w(f'        "{dq(key)}": {synth_attrs[key]!r},')
    w("    },")
    w("}")
    w("")
    w("# ---------------------------------------------------------------------------")
    w("# association table (raw CMOF memberEnd name-pairs per A_* association);")
    w("# file order - the writer emits members in this order")
    w("# ---------------------------------------------------------------------------")
    w("_ASSOCIATIONS = {")
    for an, (e1, e2) in assocs.items():
        w(f'    "{dq(an)}": ("{dq(e1)}", "{dq(e2)}"),')
    w("}")
    w("")
    w("_CLASSES = [" + ", ".join(safe_name(n) for n in order) + "]")
    w("")
    w("def _finish():")
    w("    for c in _CLASSES:")
    w("        props = {}")
    w("        for k in reversed(c.__mro__):")
    w("            for n, d in getattr(k, '_DECL', {}).items():")
    w("                props[n] = d")
    w("        c._props = props")
    w("    for c in _CLASSES:")
    w("        decl = c.__dict__.get('_DECL')")
    w("        if not decl:")
    w("            continue")
    w("        for d in decl.values():")
    w("            d.owner_cls = c.__name__")
    w("            for o in c.__dict__.get('_OPPS', {}).get(d.name, ()):")
    w("                if d.opp is None:")
    w("                    d.opp = o")
    w("        for n, d in decl.items():")
    w("            setattr(c, n, d)")
    w("_finish()")
    w("")
    w("")
    w("def class_of(name):")
    w('    """Look up a generated BPMN class by metamodel name."""')
    w("    for c in _CLASSES:")
    w("        if c.__name__ == name:")
    w("            return c")
    w("    raise KeyError(name)")
    w("")

    code = "\n".join(o) + "\n"
    dest = HERE / "gen"
    dest.mkdir(exist_ok=True)
    (dest / "bpmn.py").write_text(code)
    return warns


def gen():
    classes, assocs, warns, meta = parse_cmof(CMOF)
    warns = emit_module(classes, assocs, warns, meta)
    stats = dict(source="OMG BPMN 2.0.2 CMOF (BPMN20.cmof)",
                 classes=len([c for c in classes.values() if "enum" not in c]),
                 enums=len([c for c in classes.values() if "enum" in c]),
                 associations=len(assocs), warnings=sorted(set(warns)))
    (HERE / "bpmn_stats.json").write_text(json.dumps(stats, indent=2))
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    gen()