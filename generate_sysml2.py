#!/usr/bin/env python
"""generate_sysml2.py — generate gen/sysml2.py from the OMG SysML v2 XMI.

Clean-room: the OMG-published SysML.xmi (MOF XMI for the SysML v2 Abstract
Syntax, https://www.omg.org/spec/SysML/20250201/SysML.xmi, ptc/25-02-15) is
the normative machine-readable artifact for requirement 2 of the
transformation conformance clause (§2 of ptc/2025-04-07).

The SysML v2 AS package specializes the KerML metamodel via cross-file
hrefs (KerML.xmi). This generator parses BOTH files in one pass:
  - classes defined in SysML.xmi (89 + the ones nested in packages)
  - KerML classes referenced by href (78) — resolved from kerml.xmi so
    that gen/sysml2.py is self-contained (KerML bases inlined)
  - generalizations across the file boundary (href="#Kernel-...-Class")
    resolve to the KerML class's *name*
  - attributes carried by href'd KerML ends resolve via kerml.xmi ids

Writes gen/sysml2.py + gen/kerml.py + sysml2_stats.json.

Usage: <venv-with-lxml>/bin/python generate_sysml2.py [sysml.xmi] [kerml.xmi]
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

from lxml import etree

XMI2016 = "{http://www.omg.org/spec/XMI/20161101}"
XMI2013 = "{http://www.omg.org/spec/XMI/20131001}"
HERE = Path(__file__).resolve().parent

PRIMITIVES = {"Boolean": "bool", "Integer": "int", "Real": "float",
              "String": "str", "UnlimitedNatural": "UnlimitedNatural"}

KEYWORDS = {
    "False", "None", "True", "and", "as", "assert", "async", "await", "break",
    "class", "continue", "def", "del", "elif", "else", "except", "finally",
    "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal",
    "not", "or", "pass", "return", "try", "while", "with", "yield",
}


def safe_name(n):
    return n + "_" if n in KEYWORDS else n


def dq(text):
    return text.replace("\\", "\\\\").replace('"', '\\"')


def tdoc(text):
    return text.replace('"""', '" "').replace("\\", "\\\\")


def lower_of(el):
    for lv in el.findall("{*}lowerValue"):
        v = lv.get("value")
        if v is not None:
            try:
                return int(v)
            except ValueError:
                return 0
        return 0
    return None


def upper_of(el):
    for uv in el.findall("{*}upperValue"):
        v = uv.get("value")
        if v == "-1":
            return "*"
        if v is not None:
            try:
                return int(v)
            except ValueError:
                return 1
        return 1
    return 1


def spec_body_of(el):
    for spec in el.findall("{*}specification"):
        body = spec.find("{*}body")
        if body is not None and body.text:
            return body.text.strip()
        return (spec.get("body") or "").strip()
    return ""


def first_comment(el):
    c = el.find("{*}ownedComment")
    if c is not None:
        return c.get("body") or ""
    return ""


class MAttr:
    def __init__(self, aid, owner, name):
        self.id, self.owner, self.name = aid, owner, name
        self.type = None          # emitted type expr or None
        self.type_name = None     # resolved source-level name
        self.via_href = False
        self.lower = None
        self.upper = None
        self.multi = False
        self.derived = False
        self.union = False
        self.composite = False
        self.readonly = False
        self.assoc = None
        self.subsets = []         # attr ids
        self.redefines = []       # attr ids
        self.comment = ""
        self.hidden = False


class MOp:
    def __init__(self, owner, name):
        self.owner, self.name = owner, name
        self.params = []
        self.ret = None
        self.is_query = False
        self.comment = ""


class MClass:
    def __init__(self, cid, name, pkg, src):
        self.id, self.name, self.pkg, self.src = cid, name, pkg, src
        self.abstract = False
        self.bases = []           # class names (resolved)
        self.bases_raw = []       # idrefs / href fragments
        self.attrs = []
        self.ops = []
        self.constraints = []
        self.comment = ""


class MEnum:
    def __init__(self, eid, name, pkg, src):
        self.id, self.name, self.pkg, self.src = eid, name, pkg, src
        self.literals = []
        self.comment = ""


def parse_one(xmi_path, src_label):
    """Parse one CMOF XMI file; returns (classes, enums, attr_by_id,
    assoc_members). Class ids are globally unique per file; the src tag
    distinguishes kerml/ sysml attributes when the same id appears."""
    t = etree.parse(str(xmi_path))
    root = t.getroot()
    classes, enums = {}, {}
    attr_by_id = {}
    assoc_members = {}

    def type_ref(el):
        tp = el.get("type")
        if tp:
            return tp, tp, False
        href = el.find("{*}type")
        if href is not None:
            # inline idref: <type xmi:idref="SomeClass"/>
            idref = href.get(XMI2016 + "idref")
            if idref:
                return None, idref, False
            if href.get("href"):
                frag = href.get("href").split("#")[-1]
                return None, frag, True
        return None, None, False

    def parse_attr(kid, owner, hidden=False):
        a = MAttr(kid.get(XMI2016 + "id") or kid.get("xmi:id"),
                  owner, kid.get("name"))
        a.hidden = hidden
        a.type, a.type_name, a.via_href = type_ref(kid)
        a.lower, a.upper = lower_of(kid), upper_of(kid)
        a.multi = a.upper == "*" or (
            isinstance(a.upper, str) and a.upper.isdigit()
            and int(a.upper) > 1)
        a.derived = kid.get("isDerived") == "true"
        a.union = kid.get("isDerivedUnion") == "true"
        a.composite = kid.get("aggregation") == "composite"
        a.readonly = kid.get("isReadOnly") == "true"
        a.assoc = kid.get("association")
        if a.assoc is None:
            assoc_el = kid.find("{*}association")
            if assoc_el is not None:
                a.assoc = assoc_el.get(XMI2016 + "idref")
        oc = kid.find("{*}ownedComment")
        a.comment = oc.get("body") or "" if oc is not None else ""
        for sp in kid.findall("{*}subsettedProperty"):
            a.subsets.append(sp.get(XMI2016 + "idref"))
        for rp in kid.findall("{*}redefinedProperty"):
            a.redefines.append(rp.get(XMI2016 + "idref"))
        attr_by_id[a.id] = a
        return a

    def collect_ops(el, c):
        for kid in el:
            tag = kid.tag.split("}")[-1]
            if tag == "ownedOperation":
                o = MOp(c.name, kid.get("name"))
                o.is_query = kid.get("isQuery") == "true"
                o.comment = first_comment(kid)
                for p in kid.findall("{*}ownedParameter"):
                    pname = p.get("name")
                    ptype, _, _ = type_ref(p)
                    if p.get("direction") == "return":
                        o.ret = ptype
                    else:
                        o.params.append((safe_name(pname or "arg"), ptype))
                c.ops.append(o)

    def walk_package(el, pkg_name, src):
        for kid in el:
            tag = kid.tag.split("}")[-1]
            xt = kid.get(XMI2016 + "type") or kid.get("xsi:type")
            if tag not in ("packagedElement", "ownedType"):
                continue
            if xt == "uml:Package":
                walk_package(kid, kid.get("name"), src)
            elif xt == "uml:Association":
                members = [m.get(XMI2016 + "idref")
                           for m in kid.findall("{*}memberEnd")]
                assoc_members[kid.get(XMI2016 + "id")] = members
            elif xt == "uml:Class":
                c = MClass(kid.get(XMI2016 + "id"), kid.get("name"),
                           pkg_name, src)
                c.abstract = kid.get("isAbstract") == "true"
                c.comment = first_comment(kid)
                for g in kid.findall("{*}generalization"):
                    gref = g.get("general")
                    if gref is None:
                        gen = g.find("{*}general")
                        if gen is not None:
                            gref = gen.get(XMI2016 + "idref")
                            if gref is None and gen.get("href"):
                                gref = gen.get("href").split("#")[-1]
                            gref = gref or gen.get(XMI2016 + "idref")
                            gref = gref or gen.get("idref")
                            gref = gref or gen.get("ref")
                            gref = gref or (
                                gen.get("{http://www.w3.org/1999/xlink}href")
                                or "").split("#")[-1]
                            gref = gref or gen.get("href", "")
                            gref = gref.split("#")[-1] if gref else None
                        else:
                            gref = None
                    else:
                        gref = gref_from_id(gref := g.get("general"))
                    if gref:
                        c.bases.append(gref)
                for cr in kid.findall("{*}ownedRule"):
                    c.constraints.append(
                        (cr.get("name") or cr.get(XMI2016 + "id"),
                         spec_body_of(cr)))
                for k2 in kid.findall("{*}ownedAttribute"):
                    c.attrs.append(parse_attr(k2, c.name))
                collect_ops(kid, c)
                classes[c.name] = c
            elif xt == "uml:Enumeration":
                e = MEnum(kid.get(XMI2016 + "id"), kid.get("name"),
                          pkg_name, src)
                e.comment = first_comment(kid)
                for lit in kid.findall("{*}ownedLiteral"):
                    raw = lit.get("name")
                    e.literals.append((safe_name(raw), raw))
                enums[e.name] = e

    def gref_from_id(gid):
        return gid

    root_pkg = None
    for e in root:
        if e.get("name") in ("KerML", "SysML"):
            root_pkg = e
            break
    if root_pkg is None:
        raise ValueError(f"root KerML/SysML package not found in {xmi_path}")
    walk_package(root_pkg, root_pkg.get("name"), src_label)
    return classes, enums, attr_by_id, assoc_members


def main(argv):
    sysml_path = Path(argv[1]) if len(argv) > 1 else Path("/tmp/SysML2.xmi")
    kerml_path = Path(argv[2]) if len(argv) > 2 else Path("/tmp/kerml.xmi")
    k_classes, k_enums, k_attrs, k_assocs = parse_one(kerml_path, "kerml")
    s_classes, s_enums, s_attrs, s_assocs = parse_one(sysml_path, "sysml2")
    # ---- id→name resolution + emit -----------------------------------------
    id2name = {}
    for m in (k_classes, s_classes):
        for n, c in m.items():
            id2name[c.id] = n
    # attribute ids also resolve: attr ids look like
    # 'Root-Elements-Relationship-ownedRelatedElement' — the last dash
    # segment is the attribute name; keep id→(owner-class, attr-name)
    attr_by_id_raw = dict(k_attrs)
    attr_by_id_raw.update(s_attrs)

    def gen_attr_block(a, attr_by_id):
        lines = []
        if a.comment:
            cmt = " ".join(a.comment.split())
            for i in range(0, len(cmt), 96):
                lines.append(f"    # {cmt[i:i + 96]}")
        flags = []
        if a.derived:
            flags.append("derived=True")
        if a.union:
            flags.append("union=True")
        if a.composite:
            flags.append("composite=True")
        elif a.name.startswith("owned") and a.name != "ownedAnnotation":
            # KerML ownership convention: properties named owned* carry
            # containment (KerML §7.3.2.5) even though the CMOF XMI does
            # not set aggregation="composite". Wire them as composite so
            # the runtime's owner/namespace machinery engages, matching
            # gen/uml25.py behavior. (ownedAnnotation excluded: it is a
            # reference-style annotation end.)
            flags.append("composite=True")
        if a.readonly:
            flags.append("readonly=True")
        if a.multi:
            flags.append(f"multi=True, lo={a.lower}, hi={a.upper!r}")
        if a.subsets:
            flags.append("subsets=("
                         + ", ".join(f'"{s}"' for s in a.subsets) + ",)")
        if a.redefines:
            flags.append("redefines=("
                         + ", ".join(f'"{s}"' for s in a.redefines) + ",)")
        if a.assoc:
            flags.append(f'assoc="{a.assoc}"')
        tail = (", " + ", ".join(flags)) if flags else ""
        lines.append(f"    {safe_name(a.name)!r}: "
                     f"_Ref('{a.name}', {a.type or 'None'}{tail}),")
        return "\n".join(lines)

    def gen_op(o):
        seen = set()
        ps = []
        for n, t in o.params:
            while n in seen or n == "self":
                n += "_"
            seen.add(n)
            ps.append(f"{n}: {t or 'None'} = None")
        sig = f"def {safe_name(o.name)}(self"
        if ps:
            sig += ", " + ", ".join(ps)
        sig += f") -> {o.ret or 'None'}:"
        pdesc = (", ".join(f"{n}: {t or '?'}" for n, t in o.params)
                 or "none")
        meta = (f"[{o.owner} operation{' (query)' if o.is_query else ''}; "
                f"params: {pdesc}; returns: {o.ret or 'nothing'}; "
                f"stub - metamodel metadata only]")
        doc_lines = []
        if o.comment:
            txt = " ".join(o.comment.split())
            doc_lines += [txt[i:i + 94] for i in range(0, len(txt), 94)]
        doc_lines += [meta[i:i + 94] for i in range(0, len(meta), 94)]
        lines = [f"    {sig}", '        """']
        lines += ["        " + dl for dl in doc_lines]
        lines += ['        """', "        raise NotImplementedError"]
        return "\n".join(lines)
    # KerML ids like 'Kernel-Classes-Class' or 'Systems-Parts-PartDefinition'
    # carry the class name as the last dash-segment (verified 175/175)
    def name_of(ref):
        if ref is None:
            return None
        if ref in id2name:
            return id2name[ref]
        tail = ref.split("-")[-1]
        return tail if tail in classes else None

    # merge class sets; SysML redefinitions win, keep KerML bases
    classes = dict(k_classes)
    enums = dict(k_enums)
    enums.update(s_enums)
    for name, c in s_classes.items():
        if name in classes:
            c.bases = c.bases or classes[name].bases
        classes[name] = c
    attr_by_id = dict(k_attrs)
    attr_by_id.update(s_attrs)
    assoc_members = dict(k_assocs)
    assoc_members.update(s_assocs)

    # resolve bases to names
    for c in classes.values():
        resolved = []
        for b in c.bases:
            n = name_of(b)
            if n is not None and n != c.name:
                resolved.append(n)
        c.bases = resolved

    # resolve attribute types to emitted names (via the id-suffix rule)
    for a in attr_by_id.values():
        if a.type_name is None:
            continue
        n = name_of(a.type_name)
        if n is not None and n in classes:
            a.type = f'"{n}"'
        elif a.type_name in PRIMITIVES:
            a.type = PRIMITIVES[a.type_name]

    # The KerML AS marks ownedTyping/ownedSpecialization/ownedFeature
    # derived (they are computed views over the specialization graph),
    # but they are the ONLY programmatic write path for typing/
    # subclassification in a stdlib runtime without a full KerML
    # interpreter. Emit them writable so _hook_add wiring engages and
    # the derived-union read reflects stored values (documented wave-1
    # deviation; matches how the v2 textual examples attach typings).
    WRITABLE_DERIVED = {"ownedTyping", "ownedSpecialization", "ownedFeature",
                        "owningFeature", "owningType",
                        "owningClassifier", "subclassifier",
                        "superclassifier"}
    for a in attr_by_id.values():
        if a.name in WRITABLE_DERIVED:
            a.derived = False

    n_attrs = sum(len(c.attrs) for c in classes.values())
    n_ops = sum(len(c.ops) for c in classes.values())
    n_cons = sum(len(c.constraints) for c in classes.values())

    # subsets/redefines across files: resolve idrefs to attribute NAMES
    # (attr idrefs resolve via the raw id map, falling back to the
    # last-dash-segment name which matches the attribute name)
    for a in attr_by_id.values():
        resolved_subs = []
        for s in a.subsets:
            if s in attr_by_id_raw:
                resolved_subs.append(attr_by_id_raw[s].name)
            else:
                tail = name_of(s)
                if tail:
                    resolved_subs.append(tail)
        a.subsets = resolved_subs
        resolved_reds = []
        for s in a.redefines:
            if s in attr_by_id_raw:
                resolved_reds.append(attr_by_id_raw[s].name)
            else:
                tail = name_of(s)
                if tail:
                    resolved_reds.append(tail)
        a.redefines = resolved_reds

    # association opposites (both ends must be class-owned attrs)
    opposites = {}
    for members in assoc_members.values():
        if len(members) != 2:
            continue
        x = attr_by_id.get(members[0])
        y = attr_by_id.get(members[1])
        if x is None or y is None or x.owner is None or y.owner is None:
            continue
        opposites[(x.owner, x.name)] = y
        opposites[(y.owner, y.name)] = x

    # subset/redefine closure for derived-union contribution
    memo = {}

    def closure(aid):
        if aid in memo:
            return memo[aid]
        memo[aid] = set()
        a = attr_by_id.get(aid)
        out = set()
        if a is not None:
            for s in a.subsets:
                # resolved names: find the attr id via owner class scan
                for other_id, other in attr_by_id.items():
                    if other.name == s:
                        out.add(other.id)
                        out |= closure(other.id)
                        break
        memo[aid] = out
        return out

    union_contribs = defaultdict(lambda: defaultdict(list))
    for c in classes.values():
        for a in c.attrs:
            if a.union:
                continue
            for tid in closure(a.id):
                tu = attr_by_id.get(tid)
                if tu is not None and tu.union:
                    union_contribs[c.name][tu.name].append(a.name)

    # topological order: bases emitted before subclasses
    order = []
    _seen = set()

    def visit(c):
        if c.name in _seen:
            return
        _seen.add(c.name)
        for b in c.bases:
            if b in classes:
                visit(classes[b])
        order.append(c)

    for c in sorted(classes.values(), key=lambda c: c.name):
        visit(c)

    depth = {}

    def dep(name):
        if name not in classes:
            return 0
        if name in depth:
            return depth[name]
        d = 0
        for b in classes[name].bases:
            if b in classes:
                d = max(d, dep(b) + 1)
        depth[name] = d
        return d

    for c in classes.values():
        dep(c.name)

    o = []
    w = o.append
    w('"""SysML v2 abstract syntax + KerML base, generated from the OMG XMIs.')
    w("")
    w(f"Sources: {sysml_path.name} (SysML v2 AS, ptc/25-02-15) + "
      f"{kerml_path.name} (KerML).")
    w("Pure-stdlib Python. Do not edit by hand; regenerate with")
    w("generate_sysml2.py.")
    w("")
    w(f"Contents: {len(classes)} metaclasses ({len(k_classes)} KerML + "
      f"{len(s_classes)} SysML v2), {n_attrs} properties,")
    w(f"{n_ops} operations, {len(enums)} enumerations, "
      f"{n_cons} normative constraints (metadata).")
    w('"""')
    w("import enum as _enum")
    w("")
    w("class UnlimitedNatural:")
    w('    """UML UnlimitedNatural: a natural number or unbounded ("*")."""')
    w("    __slots__ = ('n',)")
    w("    def __init__(self, value):")
    w("        if value == '*': self.n = None")
    w("        else:")
    w("            n = int(value)")
    w("            if n < 0: raise ValueError('UnlimitedNatural must be >= 0')")
    w("            self.n = n")
    w("    @property")
    w("    def unbounded(self): return self.n is None")
    w("    def __eq__(self, other):")
    w("        return isinstance(other, UnlimitedNatural) and other.n == self.n")
    w("    def __hash__(self): return hash(self.n)")
    w("    def __repr__(self): return '*' if self.n is None else str(self.n)")
    for e in sorted(enums.values(), key=lambda e: e.name):
        w("")
        w(f"class {e.name}(_enum.Enum):")
        if e.comment:
            w('    """' + tdoc(" ".join(e.comment.split()))[:400] + '"""')
        for safe, raw in e.literals:
            w(f'    {safe} = "{raw}"')
    w("")
    w("class _Ref:")
    w('    """Descriptor carrying one metamodel property and its semantics."""')
    w("    __slots__ = ('name', 't', 'multi', 'lo', 'hi', 'derived', 'union',")
    w("               'composite', 'readonly', 'subsets', 'redefines', 'assoc',")
    w("               'opp', 'owner_cls')")
    w("    def __init__(self, name, t, multi=False, lo=0, hi=1, derived=False,")
    w("                 union=False, composite=False, readonly=False,")
    w("                 subsets=(), redefines=(), assoc=None):")
    w("        self.name, self.t, self.multi, self.lo, self.hi = name, t, multi, lo, hi")
    w("        self.derived, self.union, self.composite = derived, union, composite")
    w("        self.readonly = readonly")
    w("        self.subsets, self.redefines, self.assoc = subsets, redefines, assoc")
    w("        self.opp = None")
    w("        self.owner_cls = None")
    w("    def __get__(self, inst, cls=None):")
    w("        if inst is None: return self")
    w("        if self.union: return inst._union(self.name)")
    w("        v = inst._vals.get(self.name)")
    w("        if v is None and self.multi:")
    w("            v = inst._vals[self.name] = _RefList(inst, self)")
    w("        return v")
    w("    def _check_set(self, inst):")
    w("        if self.union or self.derived or self.readonly:")
    w("            raise AttributeError(")
    w("                f'{type(inst).__name__}.{self.name} is derived/read-only')")
    w("    def __set__(self, inst, value):")
    w("        self._check_set(inst)")
    w("        old = inst._vals.get(self.name)")
    w("        if self.multi:")
    w("            lst = _RefList(inst, self)")
    w("            if value is not None:")
    w("                for v in value:")
    w("                    lst._raw_append(v)")
    w("                    _hook_add(inst, self, v)")
    w("            inst._vals[self.name] = lst")
    w("        else:")
    w("            if old is not None and old is not value:")
    w("                _hook_remove(inst, self, old)")
    w("            inst._vals[self.name] = value")
    w("            if value is not None:")
    w("                _hook_add(inst, self, value)")
    w("    def __delete__(self, inst):")
    w("        self._check_set(inst)")
    w("        old = inst._vals.pop(self.name, None)")
    w("        if old is None: return")
    w("        if self.multi:")
    w("            for v in list(old): _hook_remove(inst, self, v)")
    w("        else:")
    w("            _hook_remove(inst, self, old)")
    w("    def _raw_set(self, inst, value): inst._vals[self.name] = value")
    w("    def _raw_clear(self, inst): inst._vals.pop(self.name, None)")
    w("")
    w("class _RefList(list):")
    w('    """List-valued property; every mutation fires the wiring hooks."""')
    w("    def __init__(self, inst, ref):")
    w("        super().__init__()")
    w("        self._inst, self._ref = inst, ref")
    w("    def _check(self): self._ref._check_set(self._inst)")
    w("    def append(self, v):")
    w("        self._check()")
    w("        super().append(v)")
    w("        _hook_add(self._inst, self._ref, v)")
    w("    def insert(self, i, v):")
    w("        self._check()")
    w("        super().insert(i, v)")
    w("        _hook_add(self._inst, self._ref, v)")
    w("    def extend(self, vs):")
    w("        self._check()")
    w("        for v in vs: self.append(v)")
    w("    def remove(self, v):")
    w("        self._check()")
    w("        super().remove(v)")
    w("        _hook_remove(self._inst, self._ref, v)")
    w("    def pop(self, i=-1):")
    w("        self._check()")
    w("        v = super().pop(i)")
    w("        _hook_remove(self._inst, self._ref, v)")
    w("        return v")
    w("    def __setitem__(self, i, v):")
    w("        self._check()")
    w("        old = self[i] if isinstance(i, int) else None")
    w("        super().__setitem__(i, v)")
    w("        if old is not None: _hook_remove(self._inst, self._ref, old)")
    w("        if isinstance(i, int): _hook_add(self._inst, self._ref, v)")
    w("    def _raw_append(self, v): super().append(v)")
    w("    def _raw_remove(self, v): super().remove(v)")
    w("")
    w("def _hook_add(container, ref, child):")
    w('    """Composite ownership + association-opposite wiring (idempotent)."""')
    w("    if not isinstance(child, _Element):")
    w("        return")
    w("    if ref.composite:")
    w("        child._owner = container")
    w("        child._namespace = container")
    w("    oname = ref.opp")
    w("    if not oname or child._wiring: return")
    w("    od = child._props.get(oname)")
    w("    if od is None or od.derived or od.readonly or od.union: return")
    w("    child._wiring = True")
    w("    try:")
    w("        if od.multi:")
    w("            lst = od.__get__(child)")
    w("            if container not in lst:")
    w("                lst._raw_append(container)")
    w("                _hook_add(child, od, container)")
    w("        else:")
    w("            if od.__get__(child) is not container:")
    w("                od._raw_set(child, container)")
    w("                _hook_add(child, od, container)")
    w("    finally:")
    w("        child._wiring = False")
    w("")
    w("def _hook_remove(container, ref, child):")
    w("    if not isinstance(child, _Element):")
    w("        return")
    w("    if ref.composite:")
    w("        if child._owner is container: child._owner = None")
    w("        if child._namespace is container: child._namespace = None")
    w("    oname = ref.opp")
    w("    if not oname or child._wiring: return")
    w("    od = child._props.get(oname)")
    w("    if od is None or od.derived or od.readonly or od.union: return")
    w("    child._wiring = True")
    w("    try:")
    w("        if od.multi:")
    w("            lst = od.__get__(child)")
    w("            if container in lst: lst._raw_remove(container)")
    w("        elif od.__get__(child) is container:")
    w("            od._raw_clear(child)")
    w("    finally:")
    w("        child._wiring = False")
    w("")
    w("class _Element:")
    w('    """Common base of all KerML/SysML v2 metaclasses (KerML Element)."""')
    w("    _DECL: dict = {}")
    w("    _UNIONS: dict = {}")
    w("    _ABSTRACT = False")
    w("    def __init__(self, **kw):")
    w("        if type(self)._ABSTRACT:")
    w("            raise TypeError(")
    w("                f'{type(self).__name__} is abstract in the SysML v2'")
    w("                f' metamodel; instantiate a concrete subclass.')")
    w("        self._vals = {}")
    w("        self._owner = None")
    w("        self._namespace = None")
    w("        self._wiring = False")
    w("        for k, v in kw.items():")
    w("            if k not in self._props:")
    w("                raise TypeError(f'{type(self).__name__} has no property {k!r}')")
    w("            setattr(self, k, v)")
    w("    def _union(self, name):")
    w('        """Derived-union read: collect values of properties that subset."""')
    w("        out, seen = [], set()")
    w("        for cls in type(self).__mro__:")
    w("            for contrib in getattr(cls, '_UNIONS', {}).get(name, ()):")
    w("                d = self._props.get(contrib)")
    w("                if d is None or d.union: continue")
    w("                v = d.__get__(self)")
    w("                items = v if d.multi else ((v,) if v is not None else ())")
    w("                for it in items:")
    w("                    if id(it) not in seen:")
    w("                        seen.add(id(it))")
    w("                        out.append(it)")
    w("        return out")
    w("    def add(self, name, *values):")
    w('        """Append value(s) to a multi-valued property."""')
    w("        lst = getattr(self, name)")
    w("        for v in values: lst.append(v)")
    w("    def remove(self, name, *values):")
    w("        lst = getattr(self, name)")
    w("        for v in values: lst.remove(v)")
    w("    @property")
    w("    def owner(self):")
    w('        """Element.owner: derived as the inverse of composite containment."""')
    w("        return self._owner")
    w("    @property")
    w("    def namespace(self):")
    w('        """Namespace.namespace: derived from composite ownership."""')
    w("        return self._namespace")
    w("    @property")
    w("    def ownedElement(self):")
    w('        """KerML §7.3.2: ownedElement = the ownedRelatedElements of the')
    w('        Relationships this Element owns. Computed from the owner')
    w('        back-wiring maintained by _hook_add (the CMOF XMI leaves')
    w('        ownedElement a derived union with no subsetters)."""')
    w("        out, seen = [], set()")
    w("        for r in self.ownedRelationship:")
    w("            for e in r.ownedRelatedElement:")
    w("                if e is not None and id(e) not in seen:")
    w("                    seen.add(id(e))")
    w("                    out.append(e)")
    w("        return out")
    w("    def __repr__(self):")
    w("        n = self._vals.get('declaredName') or self._vals.get('name')")
    w("        if isinstance(n, str) and n:")
    w("            return f'<{type(self).__name__} {n!r}>'")
    w("        return f'<{type(self).__name__} #{id(self):x}>'")
    w("")
    # ---- metaclasses ----
    for c in order:
        bases = sorted((b for b in c.bases if b in classes),
                       key=lambda b: -depth[b]) or ["_Element"]
        w("")
        w(f"class {c.name}(" + ", ".join(bases) + "):")
        doc = " ".join(c.comment.split()) if c.comment else ""
        if doc:
            guard = tdoc(doc)
            w('    """' + guard[:900]
              + ('...[truncated]' if len(guard) > 900 else '') + '"""')
        w(f'    _PKG = "{c.pkg}"')
        skip = {a for a in c.attrs
                if a.name in ("owner", "namespace", "ownedElement")
                and a.derived}
        if skip:
            w("    # (owner / namespace properties are hardcoded on _Element)")
        decls = [gen_attr_block(a, attr_by_id)
                 for a in sorted(c.attrs, key=lambda x: x.name)
                 if a not in skip]
        if decls:
            w("    _DECL = {")
            w("\n".join(decls))
            w("    }")
        contribs = union_contribs.get(c.name)
        if contribs:
            w("    _UNIONS = {")
            for u in sorted(contribs):
                names = ", ".join(f'"{safe_name(n)}"'
                                  for n in sorted(set(contribs[u])))
                w(f'        "{u}": ({names},),')
            w("    }")
        if c.constraints:
            w("    CONSTRAINTS = (")
            for cn, body in c.constraints:
                w(f'        ("{dq(cn)}",')
                b = dq(body or "(no specification serialized)")
                for i in range(0, len(b), 88):
                    w(f'         "{b[i:i + 88]}"')
                w("        ),")
            w("    )")
        for op in c.ops:
            w(gen_op(op))
    # ---- assembly ----
    w("")
    w("_CLASSES = [" + ", ".join(c.name for c in order) + "]")
    w("_OPPOSITES = {")
    for (owner, aname), other in sorted(opposites.items()):
        w(f'    ("{owner}", "{aname}"): ("{other.owner}", '
          f'"{safe_name(other.name)}"),')
    w("}")
    w("_ABSTRACT_NAMES = {"
      + ", ".join(f'"{c.name}"' for c in order if c.abstract) + "}")
    w("")
    w("def _finish():")
    w("    for c in _CLASSES:")
    w("        props = {}")
    w("        for k in reversed(c.__mro__):")
    w("            for n, d in getattr(k, '_DECL', {}).items():")
    w("                    props[n] = d")
    w("        c._props = props")
    w("        c._ABSTRACT = c.__name__ in _ABSTRACT_NAMES")
    w("    for c in _CLASSES:")
    w("        decl = c.__dict__.get('_DECL')")
    w("        if not decl:")
    w("            continue")
    w("        for d in decl.values():")
    w("            d.owner_cls = c.__name__")
    w("            opp = _OPPOSITES.get((c.__name__, d.name))")
    w("            d.opp = opp[1] if opp else None")
    w("        for n, d in decl.items():")
    w("            setattr(c, n, d)")
    w("_finish()")
    w("")
    w("def metaclass(name):")
    w('    """Look up a generated metaclass by metamodel name."""')
    w("    for c in _CLASSES:")
    w("        if c.__name__ == name: return c")
    w("    raise KeyError(name)")
    w("")
    w("_ENUMS = {" + ", ".join(
        f'"{e.name}": {e.name}'
        for e in sorted(enums.values(), key=lambda e: e.name)) + "}")
    w("")
    code = "\n".join(o) + "\n"
    dest = HERE / "gen"
    dest.mkdir(exist_ok=True)
    (dest / "__init__.py").write_text("")
    (dest / "sysml2.py").write_text(code)
    stats = {
        "source_sysml": str(sysml_path),
        "source_kerml": str(kerml_path),
        "classes": len(classes),
        "attributes": n_attrs,
        "operations": n_ops,
        "enums": len(enums),
        "constraints": n_cons,
        "associations": len(set(k_assocs) | set(s_assocs)),
        "kerml_classes": len(k_classes),
        "sysml2_classes": len(s_classes),
        "generated_lines": code.count("\n"),
    }
    (HERE / "sysml2_stats.json").write_text(json.dumps(stats, indent=1))
    print(json.dumps(stats, indent=1))
    return 0




if __name__ == "__main__":
    sys.exit(main(sys.argv))
