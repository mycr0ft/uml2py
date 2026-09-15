#!/usr/bin/env python
"""Generate a Python package from the OMG UML 2.5.1 metamodel XMI.

Clean-room exploration: the OMG-published UML.xmi (XMI 2.5 serialization of
the UML 2.5.1 metamodel) is parsed and re-emitted as pure-stdlib Python:
metaclasses with inheritance, property descriptors carrying UML property
semantics (multiplicity, derived, derived-union, composite, read-only,
subsets, redefines, association opposites), enumerations, operation stubs,
and normative OCL constraints / spec comments as metadata.

Usage:  <venv-with-lxml>/bin/python generate.py [path/to/UML.xmi]
Writes: gen/uml25.py and stats.json next to this file.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

from lxml import etree

XMI = "{http://www.omg.org/spec/XMI/20131001}"
HERE = Path(__file__).resolve().parent

PRIMITIVES = {"Boolean": "bool", "Integer": "int", "Real": "float",
              "String": "str", "UnlimitedNatural": "UnlimitedNatural"}

KEYWORDS = {
    "False", "None", "True", "and", "as", "assert", "async", "await", "break",
    "class", "continue", "def", "del", "elif", "else", "except", "finally",
    "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal",
    "not", "or", "pass", "raise", "return", "try", "while", "with", "yield",
}


def safe_name(n):
    return n + "_" if n in KEYWORDS else n


def dq(text):
    """Make text safe inside a "..." or triple-quoted literal."""
    return text.replace("\\", "\\\\").replace('"', '\\"')


def tdoc(text):
    """Make text safe inside a triple-quoted docstring."""
    return text.replace('"""', '" "').replace("\\", "\\\\")


class MAttr:
    def __init__(self, aid, owner, name):
        self.id, self.owner, self.name = aid, owner, name
        self.hidden = False     # association-owned end (not a class attribute)
        self.type = None        # python type expression (str) or None
        self.type_name = None   # metaclass / primitive / enum name
        self.via_href = False
        self.lower, self.upper = 0, 1
        self.multi = False
        self.derived = False
        self.union = False
        self.composite = False
        self.readonly = False
        self.subsets = []       # attr ids
        self.redefines = []     # attr ids
        self.assoc = None
        self.comment = None


class MOp:
    def __init__(self, owner, name):
        self.owner, self.name = owner, name
        self.params = []        # (name, type_expr)
        self.ret = None
        self.is_query = False
        self.comment = None


class MClass:
    def __init__(self, cid, name, pkg):
        self.id, self.name, self.pkg = cid, name, pkg
        self.abstract = False
        self.bases = []
        self.attrs = []
        self.ops = []
        self.constraints = []   # (name, ocl)
        self.comment = None


class MEnum:
    def __init__(self, eid, name, pkg):
        self.id, self.name, self.pkg = eid, name, pkg
        self.literals = []      # (safe_name, original)
        self.comment = None


def lower_of(el):
    lv = el.find("{*}lowerValue")
    return int(lv.get("value", 0)) if lv is not None else 0


def upper_of(el):
    uv = el.find("{*}upperValue")
    return uv.get("value", 1) if uv is not None else 1


def body_of(el):
    spec = el.find("{*}specification")
    if spec is None:
        return None
    b = spec.find("{*}body")
    if b is not None and b.text:
        return " ".join(b.text.split())
    return spec.get("value")


def first_comment(el):
    c = el.find("{*}ownedComment")
    if c is None:
        return None
    return (c.get("body") or "").strip() or None


def parse(xmi_path):
    t = etree.parse(str(xmi_path))
    r = t.getroot()
    classes, enums, warns = {}, {}, []
    attr_by_id = {}
    assoc_members = {}

    def type_expr(el):
        tp = el.get("type")
        if tp:
            return tp, tp, False
        href = el.find("{*}type")
        if href is not None and href.get("href"):
            frag = href.get("href").split("#")[-1]
            return PRIMITIVES.get(frag, None), frag, True
        return None, None, False

    def parse_attr(kid, owner, hidden=False):
        a = MAttr(kid.get(XMI + "id"), owner, kid.get("name"))
        a.hidden = hidden
        a.type, a.type_name, a.via_href = type_expr(kid)
        a.lower, a.upper = lower_of(kid), upper_of(kid)
        a.multi = a.upper == "*" or (
            isinstance(a.upper, str) and a.upper.isdigit() and int(a.upper) > 1)
        a.derived = kid.get("isDerived") == "true"
        a.union = kid.get("isDerivedUnion") == "true"
        a.composite = kid.get("aggregation") == "composite"
        a.readonly = kid.get("isReadOnly") == "true"
        a.assoc = kid.get("association")
        a.comment = first_comment(kid)
        for sp in kid.findall("{*}subsettedProperty"):
            a.subsets.append(sp.get(XMI + "idref"))
        for rp in kid.findall("{*}redefinedProperty"):
            a.redefines.append(rp.get(XMI + "idref"))
        attr_by_id[a.id] = a
        return a

    def walk_package(el, pkg_name):
        for kid in el:
            tag = kid.tag.split("}")[-1]
            xt = kid.get(XMI + "type")
            if tag not in ("packagedElement", "ownedType"):
                continue
            if xt == "uml:Package":
                walk_package(kid, kid.get("name"))
            elif xt == "uml:Association":
                ends = []
                for e2 in kid.findall("{*}ownedEnd"):
                    ends.append(parse_attr(e2, None, hidden=True))
                members = [m.get(XMI + "idref")
                           for m in kid.findall("{*}memberEnd")]
                assoc_members[kid.get(XMI + "id")] = members
            elif xt == "uml:Class":
                c = MClass(kid.get(XMI + "id"), kid.get("name"), pkg_name)
                c.abstract = kid.get("isAbstract") == "true"
                c.comment = first_comment(kid)
                for g in kid.findall("{*}generalization"):
                    c.bases.append(g.get("general"))
                for cr in kid.findall("{*}ownedRule"):
                    c.constraints.append(
                        (cr.get("name") or cr.get(XMI + "id"), body_of(cr)))
                for kid2 in kid.findall("{*}ownedAttribute"):
                    c.attrs.append(parse_attr(kid2, c.name))
                collect_members(kid, c)
                if c.name in classes:
                    warns.append(f"duplicate class name {c.name}")
                classes[c.name] = c
            elif xt == "uml:Enumeration":
                e = MEnum(kid.get(XMI + "id"), kid.get("name"), pkg_name)
                e.comment = first_comment(kid)
                for lit in kid.findall("{*}ownedLiteral"):
                    raw = lit.get("name")
                    e.literals.append((safe_name(raw), raw))
                enums[e.name] = e

    def collect_members(el, c):
        for kid in el:
            tag = kid.tag.split("}")[-1]
            if tag == "ownedOperation":
                o = MOp(c.name, kid.get("name"))
                o.is_query = kid.get("isQuery") == "true"
                o.comment = first_comment(kid)
                for p in kid.findall("{*}ownedParameter"):
                    ptype, _, _ = type_expr(p)
                    pname = p.get("name")
                    if p.get("direction") == "return":
                        o.ret = ptype
                    else:
                        o.params.append((safe_name(pname or "arg"), ptype))
                c.ops.append(o)

    root_pkg = next(e for e in r if e.get("name") == "UML")
    walk_package(root_pkg, "UML")

    # ---- resolve type idrefs (id == class/enum name in this serialization) --
    known = {c.name for c in classes.values()} | set(enums)
    for a in attr_by_id.values():
        if a.via_href:
            continue
        if a.type_name is None:
            continue
        if a.type_name in known:
            a.type = f'"{a.type_name}"' if a.type_name not in enums else a.type_name
        else:
            warns.append(f"attr {a.owner}.{a.name}: unresolved type {a.type_name!r}")
            a.type = None
    for c in classes.values():
        for o in c.ops:
            o.params = [(n, (f'"{t}"' if t in known and t not in enums else t))
                        for n, t in o.params]
            if o.ret is not None:
                o.ret = f'"{o.ret}"' if o.ret in known and o.ret not in enums else o.ret

    # ---- validate references -------------------------------------------------
    for a in attr_by_id.values():
        for ref in a.subsets + a.redefines:
            if ref not in attr_by_id:
                warns.append(f"attr {a.owner}.{a.name}: unresolved ref {ref!r}")
    for c in classes.values():
        c.bases = [b for b in c.bases if b in known]
        dropped = len(c.attrs) and None
        for b in c.bases:
            if b not in classes:
                warns.append(f"class {c.name}: base {b!r} is not a class")

    # ---- subset/redefine closure --------------------------------------------
    memo = {}

    def closure(aid):
        if aid in memo:
            return memo[aid]
        memo[aid] = set()      # cycle guard
        a = attr_by_id[aid]
        out = set()
        for s in a.subsets:
            if s in attr_by_id:
                out.add(s)
                out |= closure(s)
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

    opposites = {}
    for members in assoc_members.values():
        if len(members) != 2:
            warns.append(f"association with {len(members)} memberEnds, skipped")
            continue
        if not all(mv in attr_by_id for mv in members):
            warns.append(f"association with unresolved memberEnds: {members}")
            continue
        x, y = (attr_by_id[mv] for mv in members)
        opposites[(x.owner, x.name)] = y
        opposites[(y.owner, y.name)] = x

    return dict(classes=classes, enums=enums, attr_by_id=attr_by_id,
                union_contribs=union_contribs, opposites=opposites,
                associations=len(assoc_members),
                hidden_ends=sum(1 for a in attr_by_id.values() if a.hidden),
                warns=warns)


# --------------------------------------------------------------------------
# code generation
# --------------------------------------------------------------------------

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
    if a.readonly:
        flags.append("readonly=True")
    if a.multi:
        flags.append(f"multi=True, lo={a.lower}, hi={a.upper!r}")
    subs = ", ".join(f'"{attr_by_id[s].name}"' for s in a.subsets if s in attr_by_id)
    if subs:
        flags.append(f"subsets=({subs},)")
    reds = ", ".join(f'"{attr_by_id[s].name}"' for s in a.redefines if s in attr_by_id)
    if reds:
        flags.append(f"redefines=({reds},)")
    if a.assoc:
        flags.append(f'assoc="{a.assoc}"')
    tail = (", " + ", ".join(flags)) if flags else ""
    lines.append(f"    {safe_name(a.name)!r}: _Ref('{a.name}', {a.type or 'None'}{tail}),")
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
    pdesc = ", ".join(f"{n}: {t or '?'}" for n, t in o.params) or "none"
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


def gen():
    src = Path(sys.argv[1] if len(sys.argv) > 1 else
               "/mnt/TBFox/surfacebackup_512GB/uml_xmi/UML.xmi")
    m = parse(src)
    attr_by_id = m["attr_by_id"]
    classes, enums = m["classes"], m["enums"]
    warns = m["warns"]
    uc, opps_raw = m["union_contribs"], m["opposites"]
    # emit only opposite pairs where both ends are class-owned attributes
    opps = {k: v for k, v in opps_raw.items() if k[0] and v.owner}

    for c in classes.values():
        for a in c.attrs:
            if a.name != safe_name(a.name):
                warns.append(f"attr renamed {c.name}.{a.name} -> {safe_name(a.name)}")

    # topological order: bases always emitted before their subclasses
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

    # inheritance depth (for Python-compatible base ordering in emission)
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
    n_attrs = sum(len(c.attrs) for c in classes.values())
    n_ops = sum(len(c.ops) for c in classes.values())
    n_cons = sum(len(c.constraints) for c in classes.values())

    o = []
    w = o.append
    w('"""UML 2.5.1 metaclass hierarchy generated from the OMG-published XMI.')
    w("")
    w(f"Source: {src.name} (metamodel URI http://www.omg.org/spec/UML/20161101).")
    w("Pure-stdlib Python, no dependencies. Do not edit by hand; regenerate.")
    w("")
    w(f"Contents: {len(classes)} metaclasses, {n_attrs} properties, {n_ops} operations,")
    w(f"{len(enums)} enumerations, {n_cons} normative OCL constraints (metadata).")
    w("Derived unions / subsets / composite ownership / association opposites wired.")
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
    # ---- enumerations (needed before metaclasses reference them) ------------
    for e in sorted(enums.values(), key=lambda e: e.name):
        w("")
        w(f"class {e.name}(_enum.Enum):")
        if e.comment:
            w('    """' + tdoc(" ".join(e.comment.split()))[:400] + '"""')
        for safe, raw in e.literals:
            w(f'    {safe} = "{raw}"')
    w("")
    w("class _Ref:")
    w('    """Descriptor carrying one UML property and its metamodel semantics."""')
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
    w("                f'{type(inst).__name__}.{self.name} is derived/read-only in'")
    w("                f' the UML 2.5.1 metamodel; it is computed, not assigned.')")
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
    w('    """List-valued UML property; every mutation fires the wiring hooks."""')
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
    w('    """Common base of all UML metaclasses (UML 2.5.1 Element)."""')
    w("    _DECL: dict = {}")
    w("    _UNIONS: dict = {}")
    w("    _ABSTRACT = False")
    w("    def __init__(self, **kw):")
    w("        if type(self)._ABSTRACT:")
    w("            raise TypeError(")
    w("                f'{type(self).__name__} is abstract in the UML 2.5.1'")
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
    w('        """Derived-union read: collect all values of properties that subset."""')
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
    w('        """NamedElement.namespace: derived from composite ownership."""')
    w("        return self._namespace")
    w("    def __repr__(self):")
    w("        n = self._vals.get('name')")
    w("        if isinstance(n, str) and n:")
    w("            return f'<{type(self).__name__} {n!r}>'")
    w("        return f'<{type(self).__name__} #{id(self):x}>'")

    # ---- metaclasses ---------------------------------------------------------
    for c in order:
        bases = sorted((b for b in c.bases if b in classes),
                       key=lambda b: -depth[b]) or ["_Element"]
        w("")
        w(f"class {c.name}(" + ", ".join(bases) + "):")
        doc = " ".join(c.comment.split()) if c.comment else ""
        if doc:
            guard = tdoc(doc)
            w('    """' + guard[:900] + ('...[truncated]' if len(guard) > 900 else '') + '"""')
        w(f'    _PKG = "{c.pkg}"')
        skip = {a for a in c.attrs if a.name in ("owner", "namespace") and a.derived}
        if skip:
            w("    # (owner / namespace properties are hardcoded on _Element)")
        decls = [gen_attr_block(a, attr_by_id)
                 for a in sorted(c.attrs, key=lambda x: x.name) if a not in skip]
        if decls:
            w("    _DECL = {")
            w("\n".join(decls))
            w("    }")
        contribs = uc.get(c.name)
        if contribs:
            w("    _UNIONS = {")
            for u in sorted(contribs):
                names = ", ".join(f'"{safe_name(n)}"' for n in sorted(set(contribs[u])))
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
        if not c.attrs and not c.ops and not c.constraints:
            pass  # _PKG line guarantees a non-empty body
    # ---- enumerations were emitted above (classes reference them eagerly) ---
    # ---- assembly ------------------------------------------------------------
    w("")
    w("# ---------------------------------------------------------------------------")
    w("# post-import assembly")
    w("# ---------------------------------------------------------------------------")
    w("_CLASSES = [" + ", ".join(c.name for c in order) + "]")
    w("_OPPOSITES = {")
    for (owner, aname), other in sorted(opps.items()):
        w(f'    ("{owner}", "{aname}"): ("{other.owner}", "{safe_name(other.name)}"),')
    w("}")
    w("_ABSTRACT_NAMES = {" + ", ".join(f'"{c.name}"' for c in order if c.abstract) + "}")
    w("")
    w("def _finish():")
    w("    for c in _CLASSES:")
    w("        props = {}")
    w("        for k in reversed(c.__mro__):")
    w("            for n, d in getattr(k, '_DECL', {}).items():")
    w("                props[n] = d")
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
    (dest / "uml25.py").write_text(code)

    stats = dict(
        source=str(src), classes=len(classes), attributes=n_attrs,
        operations=n_ops, enums=len(enums), constraints=n_cons,
        abstract=sum(1 for c in classes.values() if c.abstract),
        multi_inheritance=sum(1 for c in classes.values() if len(c.bases) > 1),
        union_attrs=sum(1 for c in classes.values() for a in c.attrs if a.union),
        derived_attrs=sum(1 for c in classes.values() for a in c.attrs if a.derived),
        composite=sum(1 for c in classes.values() for a in c.attrs if a.composite),
        subset_refs=sum(len(a.subsets) for c in classes.values() for a in c.attrs),
        redefine_refs=sum(len(a.redefines) for c in classes.values() for a in c.attrs),
        assoc_pairs=len(opps),
        associations=m["associations"], hidden_ends=m["hidden_ends"],
        generated_lines=code.count("\n"),
        warnings=sorted(set(warns)),
    )
    (HERE / "stats.json").write_text(json.dumps(stats, indent=2))
    print(json.dumps({k: v for k, v in stats.items() if k != "warnings"}, indent=2))
    print(f"\n{len(stats['warnings'])} unique warnings; sample:")
    for warn in stats["warnings"][:10]:
        print("  -", warn)


if __name__ == "__main__":
    gen()