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
    (Path("/mnt/TBFox/surfacebackup_512GB/uml_xmi/StandardProfile.xmi"), None),
    (Path("/mnt/TBFox/surfacebackup_512GB/uml_xmi/sysml.xmi"), None),
    (Path("/mnt/TBFox/uml_xmi/UAF.xmi"), None),        # OMG UAF 1.2 UAFML profile
    # OMG UAF 1.3 (formal/25-10-03 era; dtc/24-11-06 machine-readable).  Same
    # profile name "UAF" as 1.2, so the module name is overridden to uaf13;
    # the profile URI (http://www.omg.org/spec/UAF/20241101/UAF) carries the
    # version identity in the emitted module.
    (Path("/mnt/TBFox/uml_xmi/UAF13.xml"), "uaf13"),
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
        self.bases = []          # stereotype names (same profile)
        self.bases_meta = []     # metaclass names from base_* ends (ordered)
        self.bases_ext = []      # (profile, stereotype) href generalizations
        self.gen_refs = []       # raw generalization refs (ids or name paths)
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


def resolve_prop_type(el, idmap):
    """(tname, kind) for a stereotype attribute, dialect-aware.

    kind: 'prim' | 'enum' | 'stereo' (same-profile stereotype) |
    'extstereo' (SysML stereotype via href) | None (name-dispatch fallback
    with the type_of() semantics).  Extends type_of() with the xmi:id /
    href dialects the UAF 1.2 UAFML serialization uses: type attributes
    carrying xmi:id refs into the same document, hrefs into SysML.xmi, and
    UUID-referenced EnumerationLiteral defaults.
    """
    t = el.get("type")
    if t:
        if t in PRIMITIVES:
            return t, "prim"
        target = idmap.get(t)
        if target is not None:
            tx = xt(target) or etree.QName(target).localname
            if tx == "uml:Enumeration":
                return target.get("name"), "enum"
            if tx == "uml:Stereotype":
                return target.get("name"), "stereo"
        if "." in t:                       # dotted name-path (sysml dialect)
            return t.split(".")[-1], None
        return t, None
    ty = el.find("{*}type")
    if ty is not None and ty.get("href"):
        href = ty.get("href")
        base = href.split("#")[0].rsplit("/", 1)[-1]
        frag = href.split("#")[-1]
        if "PrimitiveTypes" in base:
            return frag, "prim"
        if "UML" in base:
            return frag, "meta"
        if "SysML" in base:
            if "Libraries" in frag:       # SysML library primitive, e.g. String
                mm = re.search(r"-([A-Za-z]+)_PackageableElement$", frag)
                return (mm.group(1) if mm else frag), "prim"
            dt = re.match(r"SysML_dataType\.(\w+)$", frag)   # UAF 1.3: tagged values
            if dt and dt.group(1) in PRIMITIVES:             # typed-by SysML library
                return dt.group(1), "prim"                   # datatypes (not stereotypes)
            if "." in frag:               # e.g. #SysML.Block
                return frag.split(".", 1)[1], "extstereo"
            return frag, "extstereo"
        return frag, "meta"
    dv = el.find("{*}defaultValue")
    if dv is not None:
        iv = dv.find("{*}instance")
        if iv is not None:
            ref = idref(iv) or ""
            if "." in ref:                # dotted name-path default
                return ref.split(".")[-2], "enum"
            lit = idmap.get(ref)          # UUID-referenced literal (UAF)
            if lit is not None:
                owner = lit.getparent()
                if owner is not None and etree.QName(owner).localname == "Enumeration":
                    return owner.get("name"), "enum"
    return None, None


def lower_of(el):
    lv = el.find("{*}lowerValue")
    return int(lv.get("value", 0)) if lv is not None else 0


def parse_profile(path):
    r = etree.parse(str(path)).getroot()
    prof = next(e for e in r.iter() if ln(e) == "Profile")
    profile = prof.get("name")
    uri = next((e.text.strip() for e in prof
                if ln(e) == "URI" and e.text and e.text.strip()), None)
    xid_key = "{http://www.omg.org/spec/XMI/20131001}id"
    idmap = {el.get(xid_key): el for el in r.iter() if el.get(xid_key)}
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
                                if b is None and gel.get("href"):
                                    frag = gel.get("href").split("#")[-1]
                                    if "." in frag:      # e.g. SysML.Block
                                        s.bases_ext.append(tuple(frag.split(".", 1)))
                                        continue
                        if b:
                            s.gen_refs.append(b)
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
                            if meta not in s.bases_meta:   # UAF.xmi repeats base_Element
                                s.bases_meta.append(meta)
                        else:
                            lo = lower_of(a)
                            upv = a.find("{*}upperValue")
                            up = upv.get("value", 1) if upv is not None else 1
                            multi = up == "*" or (isinstance(up, str) and up.isdigit() and int(up) > 1)
                            derived = a.get("isDerived") == "true"
                            union = a.get("isDerivedUnion") == "true"
                            cmt = first_comment(a)
                            tname, tk = resolve_prop_type(a, idmap)
                            s.tags.append((safe_name(aname), tname, multi,
                                           lo, up, derived, union, cmt, tk))
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
                        # nameless extensions (UAF 1.2): metaclass from the
                        # memberEnd property whose name carries base_<Meta>;
                        # ExtensionEnd::lower defaults to 1 per UML 2.5.1,
                        # so a bare (value-attr-less) lowerValue means a
                        # REQUIRED extension (ordinary EMF properties
                        # default lower to 0 -- DoDAF dialect lesson)
                        ee_id = xid(ee)
                        meta_id = next((idref(x) for x in kid.findall("{*}memberEnd")
                                        if idref(x) != ee_id), None)
                        prop = idmap.get(meta_id) if meta_id else None
                        pname = prop.get("name") if prop is not None else None
                        meta = (pname[len("base_"):] if pname and pname.startswith("base_")
                                else None)
                        lv = ee.find("{*}lowerValue")
                        req = int(lv.get("value", "1")) == 1 if lv is not None else True
                        if prop is not None:
                            par = prop.getparent()
                            if par is not None and xt(par) == "uml:Stereotype":
                                st_name = par.get("name")
                    if meta is None:
                        warns.append(f"extension {name}: no metaclass in name")
                        continue
                    exts.setdefault(st_name, [])
                    if (meta, req) not in exts[st_name]:   # UAF.xmi repeats extensions
                        exts[st_name].append((meta, req))
                elif kxt == "uml:Enumeration":
                    lits = [(safe_name(l.get("name")), l.get("name"))
                            for l in kid.findall("{*}ownedLiteral")]
                    enums[kid.get("name")] = lits

    walk(prof, profile)

    # resolve raw generalization refs: sysml.xmi uses dotted name paths,
    # UAF.xmi uses xmi:id refs into the same document (256 unique names)
    for s in stereotypes.values():
        for ref in s.gen_refs:
            if "." in ref:
                s.bases.append(ref.split(".")[-1])
                continue
            gel = idmap.get(ref)
            if gel is not None and xt(gel) == "uml:Stereotype":
                if gel.get("name") not in s.bases:   # UAF.xmi repeats generalizations
                    s.bases.append(gel.get("name"))
            else:
                warns.append(f"{s.name}: generalization target {ref!r} unresolved")

    # stereotype generalization validation
    for s in stereotypes.values():
        for b in s.bases:
            if b not in stereotypes:
                warns.append(f"{s.name}: stereotype base {b!r} unresolved")

    return dict(profile=profile, uri=uri, stereotypes=stereotypes, enums=enums,
                extensions=exts, warns=warns)


def gen_tag(t, metaclasses, local_enums):
    name, tname, multi, lo, up, derived, union, cmt, tk = t
    if tk in ("stereo", "extstereo"):
        # stereotype-typed tagged values are late-bound by name: the target
        # stereotype may be defined later in the module (topological order
        # only covers inheritance) or in gen.sysml; _Ref stores its type as
        # opaque metadata, so a string reference is safe
        expr = f"'sysml.{tname}'" if tk == "extstereo" else f"'{tname}'"
    elif tname == "UnlimitedNatural":
        expr = "U.UnlimitedNatural"
    elif tk == "prim" or (tk is None and tname in PRIMITIVES):
        expr = PRIMITIVES[tname]
    elif tk == "enum" or (tk is None and tname in local_enums):
        expr = tname
    elif tk == "meta" or (tk is None and tname in metaclasses):
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
    mod_name = {"StandardProfile": "standard_profile", "SysML": "sysml",
                "UAF": "uaf"}[d["profile"]]
    if d.get("_mod_override"):
        mod_name = d["_mod_override"]
    import gen.sysml as _sysml
    from itertools import permutations
    created = {}

    def verify_mro(name, base_names, base_objs):
        if not base_names:
            return None
        orders = [base_names]
        if len(base_names) <= 6:   # cap factorial blowup (UAF folds up to 10+ bases)
            orders += [list(p) for p in permutations(base_names)
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
        for p, b in s.bases_ext:
            cls = getattr(_sysml, b, None)
            if cls is not None:
                best = max(best, len(cls.__mro__))
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
    uses_sysml = any(s.bases_ext for s in st.values()) or any(
        t[8] == "extstereo" for s in st.values() for t in s.tags)
    if uses_sysml:
        w("import gen.sysml as sysml")
    w("from gen.uml25 import _Ref  # noqa: F401")
    w("")
    # profile URI, as carried by the OMG profile XMI (UAF.xmi has one;
    # StandardProfile.xmi / sysml.xmi do not - the applied URI is then
    # dialect-dependent, e.g. 20090901-era vs 20161101-era files)
    if d.get("uri"):
        w(f'_URI = {d["uri"]!r}')
    else:
        w("_URI = None  # profile XMI carries no <URI>; applied URI is dialect-dependent")
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
        for p, b in s.bases_ext:
            cls = getattr(_sysml, b, None)
            if cls is None:
                warns.append(f"{s.name}: cross-profile base {p}.{b} unresolved")
                continue
            cand.append((len(cls.__mro__), f"sysml.{b}", cls))
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
                   else getattr(_sysml, b.split(".")[-1]) if b.startswith("sysml.")
                   else (created[b] if b in created else getattr(U, b)))
                  for b in bases),
            {})
        doc = " ".join(s.comment.split()) if s.comment else ""
        if doc:
            w('    """' + tdoc(doc)[:700] + ('...[truncated]' if len(doc) > 700 else '') + '"""')
        w(f'    _STEREO = "{d["profile"]}::{s.pkg}::{s.name}"')
        bm = ", ".join(f'"{b}"' for b in s.bases_meta)
        w("    _BASE_METACLASSES = (" + bm + ("," if bm else "") + ")")
        # always explicit: concrete stereotypes must not inherit the
        # abstract guard of a folded abstract metaclass (e.g. TestCase ->
        # U.Behavior is abstract in UML but the stereotype is concrete)
        w(f"    _ABSTRACT = {str(bool(s.abstract))}")
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
    all_data = []
    for p, mod_override in PROFILES:
        d = parse_profile(p)
        d["_mod_override"] = mod_override
        all_data.append(d)
    uml_src = UML.read_text()
    metaclasses = set(re.findall(r"^class (\w+)\(", uml_src, re.M))
    warns = [wm for d in all_data for wm in d["warns"]]

    mods = [emit_module(d, metaclasses, warns) for d in all_data]
    stats = dict(modules=mods, warnings=sorted(set(warns)))
    (HERE / "profile_stats.json").write_text(json.dumps(stats, indent=2))
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    gen()
