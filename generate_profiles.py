#!/usr/bin/env python
"""Generate Python stereotype classes from OMG profile XMI files.

Extends the UML 2.5.1 spike: parses the OMG StandardProfile.xmi and the
SysML v1 profile XMI (sysml.xmi) and emits gen/profiles.py, where each
stereotype becomes a Python class folding its base metaclasses (via the
base_* extension ends) together with stereotype generalizations, and
tagged values become _Ref descriptors reusing the uml25 machinery.

Extension metadata (required vs optional, per metaclass) is carried as
tables; base_* ends are consumed, not emitted as attributes.

Usage: <venv-with-lxml>/bin/python generate_profiles.py
Writes: gen/profiles.py and profile_stats.json
"""
import json
import re
from collections import defaultdict
from pathlib import Path

from lxml import etree

HERE = Path(__file__).resolve().parent
UML = HERE / "gen" / "uml25.py"

import sys
sys.path.insert(0, str(HERE))
from gen import uml25 as U  # noqa: E402

PROFILES = [
    Path("/mnt/TBFox/surfacebackup_512GB/uml_xmi/StandardProfile.xmi"),
    Path("/mnt/TBFox/surfacebackup_512GB/uml_xmi/sysml.xmi"),
]

PRIMITIVES = {"Boolean": "bool", "Integer": "int", "Real": "float",
              "String": "str", "UnlimitedNatural": "UnlimitedNatural"}

KEYWORDS = {
    "False", "None", "True", "and", "as", "assert", "async", "await", "break",
    "class", "continue", "def", "del", "elif", "else", "except", "finally",
    "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal",
    "not", "or", "pass", "raise", "return", "try", "while", "with", "yield",
}


def safe_name(n):
    n = re.sub(r"\W", "_", n)          # '~InterfaceBlock' etc.
    if n[0].isdigit():
        n = "_" + n
    return n + "_" if n in KEYWORDS else n


def dq(t):
    return t.replace("\\", "\\\\").replace('"', '\\"')


def tdoc(t):
    return t.replace('"""', '" "').replace("\\", "\\\\")


def xt(el):
    """xmi:type regardless of namespace spelling (http/https)."""
    for k, v in el.attrib.items():
        if k.split("}")[-1] == "type":
            return v
    return None


def xid(el):
    for k, v in el.attrib.items():
        if k.split("}")[-1] == "id":
            return v
    return None


def idref(el):
    for k, v in el.attrib.items():
        if k.split("}")[-1] == "idref":
            return v
    return None


def ln(el):
    return el.tag.split("}")[-1]


class MStereo:
    def __init__(self, name, profile, pkg):
        self.name, self.profile, self.pkg = name, profile, pkg
        self.abstract = False
        self.bases = []          # stereotype names
        self.bases_meta = []     # metaclass names from base_* ends (ordered)
        self.tags = []           # (name, type_expr, flags...)
        self.constraints = []
        self.comment = None
        self.extensions = []     # (metaclass, required)


def first_comment(el):
    c = el.find("{*}ownedComment")
    return (c.get("body") or "").strip() or None if c is not None else None


def type_of(el):
    tp = el.get("type")
    if tp:
        return PRIMITIVES.get(tp, tp), tp.split(".")[-1]
    ty = el.find("{*}type")
    if ty is not None and ty.get("href"):
        frag = ty.get("href").split("#")[-1]
        return PRIMITIVES.get(frag.split(".")[-1], frag), frag.split(".")[-1]
    # type implied by default InstanceValue: SysML_dataType.<Enum>.<literal>
    dv = el.find("{*}defaultValue")
    if dv is not None:
        iv = dv.find("{*}instance")
        if iv is not None:
            ref = idref(iv) or ""
            parts = ref.split(".")
            if len(parts) >= 3:
                return parts[-2], parts[-2]
    return None, None


def lower_of(el):
    lv = el.find("{*}lowerValue")
    return int(lv.get("value", 0)) if lv is not None else 0


def parse_profile(path):
    r = etree.parse(str(path)).getroot()
    prof = next(e for e in r.iter() if ln(e) == "Profile")
    profile = prof.get("name")
    warns = []
    stereotypes, exts, enums = {}, {}, {}

    def walk(el, pkg):
        for kid in el:
            ktag, kxt = ln(kid), xt(kid)
            if ktag in ("packagedElement", "ownedType"):
                if kxt == "uml:Package":
                    walk(kid, kid.get("name"))
                elif kxt == "uml:Stereotype":
                    s = MStereo(kid.get("name"), profile, pkg)
                    s.abstract = kid.get("isAbstract") == "true"
                    s.comment = first_comment(kid)
                    for g in kid.findall("{*}generalization"):
                        b = g.get("general")
                        if not b:
                            gel = g.find("{*}general")
                            if gel is not None:
                                b = idref(gel)
                        if b:
                            s.bases.append(b.split(".")[-1])   # strip 'SysML.' prefix
                    for cr in kid.findall("{*}ownedRule"):
                        spec = cr.find("{*}specification")
                        body = None
                        if spec is not None:
                            b = spec.find("{*}body")
                            if b is not None and b.text:
                                body = " ".join(b.text.split())
                            else:
                                body = spec.get("body") or spec.get("value")
                        s.constraints.append((cr.get("name") or "constraint", body))
                    for a in kid.findall("{*}ownedAttribute"):
                        aname = a.get("name")
                        if aname and aname.startswith("base_"):
                            meta = aname[len("base_"):]
                            s.bases_meta.append(meta)
                        else:
                            lo = lower_of(a)
                            upv = a.find("{*}upperValue")
                            up = upv.get("value", 1) if upv is not None else 1
                            multi = up == "*" or (isinstance(up, str) and up.isdigit() and int(up) > 1)
                            derived = a.get("isDerived") == "true"
                            union = a.get("isDerivedUnion") == "true"
                            cmt = first_comment(a)
                            _, tname = type_of(a)
                            s.tags.append((safe_name(aname), tname, multi,
                                           lo, up, derived, union, cmt))
                    stereotypes[s.name] = s
                elif kxt == "uml:Extension":
                    owned = kid.findall("{*}ownedEnd")
                    if not owned:
                        warns.append(f"extension {kid.get('name')} without ownedEnd")
                        continue
                    ee = owned[0]
                    st_name = (ee.get("name") or "").replace("extension_", "")
                    req = lower_of(ee) == 1
                    name = kid.get("name") or ""
                    if "_base_" in name:
                        m = re.search(r"_base_(\w+)$", name)
                        meta = m.group(1) if m else None
                    else:
                        meta = name.rsplit("_", 1)[0] if "_" in name else None
                    if meta is None:
                        warns.append(f"extension {name}: no metaclass in name")
                        continue
                    exts.setdefault(st_name, []).append((meta, req))
                elif kxt == "uml:Enumeration":
                    lits = [(safe_name(l.get("name")), l.get("name"))
                            for l in kid.findall("{*}ownedLiteral")]
                    enums[kid.get("name")] = lits

    walk(prof, "SysML" if profile == "SysML" else "StandardProfile")

    # resolve base metaclasses: prefer extension table, fall back to base_ names
    for s in stereotypes.values():
        pass

    # stereotype generalization validation
    for s in stereotypes.values():
        for b in s.bases:
            if b not in stereotypes:
                warns.append(f"{s.name}: stereotype base {b!r} unresolved")

    return dict(profile=profile, stereotypes=stereotypes, enums=enums,
                extensions=exts, warns=warns)


def gen_tag(t, metaclasses, local_enums):
    name, tname, multi, lo, up, derived, union, cmt = t
    if tname == "UnlimitedNatural":
        expr = "U.UnlimitedNatural"
    elif tname in PRIMITIVES:
        expr = PRIMITIVES[tname]
    elif tname in local_enums:
        expr = tname
    elif tname in metaclasses:
        expr = f"U.{tname}"
    else:
        expr = "None"
    flags = []
    if multi:
        flags.append(f"multi=True, lo={lo}, hi={up!r}")
    if derived:
        flags.append("derived=True")
    if union:
        flags.append("union=True")
    tail = (", " + ", ".join(flags)) if flags else ""
    lines = []
    if cmt:
        cmt = " ".join(cmt.split())
        for i in range(0, len(cmt), 96):
            lines.append(f"    # {cmt[i:i + 96]}")
    lines.append(f"    {name!r}: _Ref('{name}', {expr}{tail}),")
    return "\n".join(lines)


def emit_module(d, metaclasses, warns):
    """Emit one profile as its own module (avoids cross-profile shadowing)."""
    st = d["stereotypes"]
    mod_name = {"StandardProfile": "standard_profile", "SysML": "sysml"}[d["profile"]]
    from itertools import permutations
    created = {}

    def verify_mro(name, base_names, base_objs):
        if not base_names:
            return None
        orders = [base_names] + [list(p) for p in permutations(base_names)
                                 if list(p) != base_names]
        obj_by_name = dict(zip(base_names, base_objs))
        for order in orders:
            try:
                type(name, tuple(obj_by_name[b] for b in order), {})
            except TypeError:
                continue
            return order
        kept_n, kept_o = [], []
        for b in base_names:
            trial = kept_o + [obj_by_name[b]]
            try:
                type(name, tuple(trial), {})
            except TypeError:
                warns.append(
                    f"{name}: base {b} is C3-incompatible; folded subset is "
                    f"{kept_n + [b]!r}, keeping {kept_n!r}")
                continue
            kept_n.append(b)
            kept_o = trial
        return kept_n or None

    meta_depth = {n: len(getattr(U, n).__mro__) for n in metaclasses}
    depth = {}

    def sdepth(s):
        if s.name in depth:
            return depth[s.name]
        depth[s.name] = 0
        best = 0
        for b in s.bases:
            if b in st:
                best = max(best, sdepth(st[b]) + 1)
        for b in s.bases_meta:
            best = max(best, meta_depth.get(b, 0))
        depth[s.name] = best
        return best

    for s in st.values():
        sdepth(s)

    order, seen = [], set()

    def visit(s):
        if s.name in seen:
            return
        seen.add(s.name)
        for b in s.bases:
            if b in st:
                visit(st[b])
        order.append(s)

    for s in sorted(st.values(), key=lambda s: s.name):
        visit(s)

    n_tags = sum(len(s.tags) for s in st.values())
    n_cons = sum(len(s.constraints) for s in st.values())
    o = []
    w = o.append
    w(f'"""{d["profile"]} stereotype classes generated from the OMG profile XMI.')
    w("")
    w(f"{len(st)} stereotypes, {n_tags} tagged values, {n_cons} constraints")
    w("(metadata). Stereotypes fold their base metaclasses (Python inheritance)")
    w("with stereotype generalizations; base_* extension ends are consumed;")
    w("extension required/optional data is in _EXTENSIONS.")
    w('"""')
    w("from __future__ import annotations")
    w("")
    w("import enum as _enum")
    w("")
    w("from gen import uml25 as U")
    w("from gen.uml25 import _Ref  # noqa: F401")
    w("")
    for ename, lits in sorted(d["enums"].items()):
        w(f"class {ename}(_enum.Enum):")
        for sname, raw in lits:
            w(f'    {sname} = "{raw}"')
        w("")

    for s in order:
        cand = []
        for b in s.bases_meta:
            if b in metaclasses:
                cand.append((meta_depth.get(b, 0), f"U.{b}", getattr(U, b)))
            else:
                warns.append(f"{s.name}: base metaclass {b!r} not in uml25")
        for b in s.bases:
            if b in st:
                cand.append((depth[b] + 1, b, created[b]))
            elif b not in s.bases_meta:
                warns.append(f"{s.name}: base {b!r} unresolved, dropped")
        cand.sort(key=lambda x: -x[0])
        names = [n for _, n, _ in cand]
        objs = [c for _, _, c in cand]
        bases = verify_mro(safe_name(s.name), names, objs)
        if bases is None:
            bases = ["U.Element"]
            warns.append(f"{s.name}: no compatible base; falling back to Element")
        w("")
        w(f"class {safe_name(s.name)}(" + ", ".join(bases) + "):")
        created[s.name] = type(
            safe_name(s.name),
            tuple((getattr(U, b[2:]) if b.startswith("U.")
                   else (created[b] if b in created else getattr(U, b)))
                  for b in bases),
            {})
        doc = " ".join(s.comment.split()) if s.comment else ""
        if doc:
            w('    """' + tdoc(doc)[:700] + ('...[truncated]' if len(doc) > 700 else '') + '"""')
        w(f'    _STEREO = "{d["profile"]}::{s.pkg}::{s.name}"')
        bm = ", ".join(f'"{b}"' for b in s.bases_meta)
        w("    _BASE_METACLASSES = (" + bm + ("," if bm else "") + ")")
        if s.abstract:
            w("    _ABSTRACT = True")
        decls = [gen_tag(t, metaclasses, set(d["enums"]))
                 for t in sorted(s.tags)]
        if decls:
            w("    _DECL = {")
            w("\n".join(decls))
            w("    }")
        if s.constraints:
            w("    CONSTRAINTS = (")
            for cn, body in s.constraints:
                w(f'        ("{dq(cn)}",')
                b = dq(body or "(no specification serialized)")
                for i in range(0, len(b), 88):
                    w(f'         "{b[i:i + 88]}"')
                w("        ),")
            w("    )")
    w("")
    w("# ---------------------------------------------------------------------------")
    w("# post-import assembly (mirror of uml25._finish for stereotype classes)")
    w("# ---------------------------------------------------------------------------")
    w("_STEREOTYPES = [" + ", ".join(safe_name(s.name) for s in order) + "]")
    w("_EXTENSIONS = {")
    for st_name, metas in sorted(d["extensions"].items()):
        if st_name not in st:
            warns.append(f"extension names unknown stereotype {st_name!r}")
            continue
        pairs = ", ".join(f'("{m}", {req!r})' for m, req in metas)
        w(f'    "{safe_name(st_name)}": ({pairs},),')
    w("}")
    w("")
    w("def _finish():")
    w("    for c in _STEREOTYPES:")
    w("        decl = c.__dict__.get('_DECL')")
    w("        if not decl:")
    w("            continue")
    w("        for d in decl.values():")
    w("            d.owner_cls = c.__name__")
    w("        for n, d in decl.items():")
    w("            setattr(c, n, d)")
    w("_finish()")
    w("")

    code = "\n".join(o) + "\n"
    dest = HERE / "gen"
    dest.mkdir(exist_ok=True)
    (dest / f"{mod_name}.py").write_text(code)
    return dict(profile=d["profile"], module=f"gen/{mod_name}.py",
                stereotypes=len(st), enums=sorted(d["enums"]),
                lines=code.count("\n"))


def gen():
    all_data = [parse_profile(p) for p in PROFILES]
    uml_src = UML.read_text()
    metaclasses = set(re.findall(r"^class (\w+)\(", uml_src, re.M))
    warns = [wm for d in all_data for wm in d["warns"]]

    mods = [emit_module(d, metaclasses, warns) for d in all_data]
    stats = dict(modules=mods, warnings=sorted(set(warns)))
    (HERE / "profile_stats.json").write_text(json.dumps(stats, indent=2))
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    gen()
