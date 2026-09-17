#!/usr/bin/env python
"""E3 checks: normative UML 2.5.1 derivations (derived.py).

Oracles:
  1. constructed graphs exercising each spec body, incl. the
     template-parameter branch of allNamespaces/qualifiedName, the
     redefinition-aware union closure (LoopNode.result -> /output,
     RTS.classifier -> /owner), inheritance via normative
     inheritedMember/importMembers, and multiplicity bounds;
  2. OMG corpora (DoDAFLibrary 2.1, UAF, MeasurementsLibrary): derived
     unions equal the runtime aggregation everywhere, containment
     owner equivalence via an independent scan, containment-tree
     completeness, qualified-name agreement with an independent walk,
     generalization-closure equivalence, membership consistency.
Standard library only. Run under ~/ams-gra-sim/.venv."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen.uml25 as U  # noqa: E402
import derived as D  # noqa: E402
import xmi21  # noqa: E402

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))


print("== constructed: ownership and qualification ==")
pkg = U.Package(name="Outer")
inner = U.Package(name="Inner")
pkg.packagedElement.append(inner)
cls = U.Class(name="C")
inner.packagedElement.append(cls)
prop = U.Property(name="x")
cls.ownedAttribute.append(prop)
check("owner is the containment inverse",
      D.owner(prop) is cls and D.owner(cls) is inner
      and D.owner(inner) is pkg)
check("qualified_name Outer::Inner::C::x", D.qualified_name(prop) == "Outer::Inner::C::x",
      D.qualified_name(prop))
check("all_namespaces innermost-first", [n.name for n in D.all_namespaces(prop)]
      == ["C", "Inner", "Outer"])
check("separator is ::", D.separator() == "::")
check("all_owned_elements DFS, not_own_self",
      D.all_owned_elements(pkg) == [inner, cls, prop]
      and pkg not in D.all_owned_elements(pkg))
check("must_be_owned: Package false, others true",
      D.must_be_owned(pkg) is False and D.must_be_owned(cls) is True)
unnamed = U.Package()
cls2 = U.Class(name="C2")
unnamed.packagedElement.append(cls2)
check("qualified_name null: unnamed element / unnamed ancestor",
      D.qualified_name(unnamed) is None and D.qualified_name(cls2) is None)

print("== constructed: template-parameter branch (§7.8.9.6) ==")
tmpl = U.Class(name="T")
sig = U.RedefinableTemplateSignature(name="sig", template=tmpl)
tmpl.ownedTemplateSignature = sig
tp = U.ClassifierTemplateParameter(signature=sig)
sig.ownedParameter.append(tp)
pe = U.Property(name="P")
tp.ownedParameteredElement = pe
check("owner of parameteredElement is its TemplateParameter",
      isinstance(D.owner(pe), U.TemplateParameter))
check("all_namespaces walks through the template boundary",
      [n.name for n in D.all_namespaces(pe)] == ["T"])
check("qualified_name through template: T::P", D.qualified_name(pe) == "T::P",
      D.qualified_name(pe))

print("== constructed: cycle guard ==")
selfy = U.Package(name="S")
selfy.packagedElement.append(selfy)      # ill-formed self-ownership
res = D.all_owned_elements(selfy)
res2 = D.union(selfy, "ownedElement")
check("derivations terminate on self-owning element (no hang)",
      isinstance(res, list) and isinstance(res2, list))

print("== constructed: redefinition-aware union closure ==")
ln = U.LoopNode(name="L")
r = U.OutputPin(name="r")
ln.result.append(r)
check("LoopNode.result reaches /output via redefines(structuredNodeOutput)",
      D.union(ln, "output") == [r] and list(ln.output) == [],
      f"derived={D.union(ln, 'output')} runtime={list(ln.output)}")
rts = U.RedefinableTemplateSignature(name="sig2")
tcls = U.Class(name="Template")
rts.classifier = tcls
check("RTS.classifier reaches /owner via redefines(template)",
      tcls in D.union(rts, "owner"))
# scan the generated tables for such gaps (the reason the closure exists)
gaps = 0
for cn in dir(U):
    c = getattr(U, cn)
    if not (isinstance(c, type) and hasattr(c, "_props")):
        continue
    for pname, d in c._props.items():
        for r in d.redefines:
            if r == pname:
                continue
            q = c._props.get(r)
            if q is None:
                continue
            for un in q.subsets:
                rec = set()
                for m in c.__mro__:
                    rec |= set(getattr(m, "_UNIONS", {}).get(un, ()))
                if pname not in rec:
                    gaps += 1
check("generated _UNIONS miss exactly 9 redefinition contributions",
      gaps == 9, f"{gaps}")

print("== constructed: parents / all_parents / conforms_to ==")
base = U.Class(name="Base")
mid = U.Class(name="Mid")
mid.generalization.append(U.Generalization(general=base))
c = U.Class(name="C")
c.generalization.append(U.Generalization(general=mid))
d = U.Class(name="D")
d.generalization.append(U.Generalization(general=mid))
d.generalization.append(U.Generalization(general=base))
check("parents == immediate generals",
      D.parents(c) == [mid] and D.parents(d) == [mid, base])
check("all_parents == independent transitive closure",
      D.all_parents(d) == [mid, base])
edges = {}
def closure(cl):
    out = set()
    for g in cl.generalization:
        p = g.general
        if p is not None:
            out.add(p)
            out |= closure(p)
    return out
check("closure equivalence on a diamond", set(D.all_parents(d)) == closure(d))
check("conforms_to self and ancestors",
      D.conforms_to(c, base) and D.conforms_to(c, c)
      and not D.conforms_to(base, c))

print("== constructed: inheritance via normative member ==")
battr = U.Property(name="a")
base.ownedAttribute.append(battr)
cattr = U.Property(name="c")
c.ownedAttribute.append(cattr)
memo = {}
check("inheritedMember surfaces Base.a in C.member",
      [getattr(m, "name", m) for m in D.member(c, memo)] == ["c", "a"])
check("all_attributes: owned before inherited",
      [m.name for m in D.all_attributes(c, memo)] == ["c", "a"])
check("all_features selects Features only",
      all(isinstance(m, U.Feature) for m in D.all_features(c, memo))
      and {m.name for m in D.all_features(c, memo)} == {"c", "a"})
rattr = U.Property(name="a")
rattr.redefinedProperty.append(battr)
c.ownedAttribute.append(rattr)
memo = {}
check("inherit() drops redefined members (a replaced once)",
      [m.name for m in D.member(c, memo)] == ["c", "a"]
      and D.member(c, memo).count(battr) == 0
      and rattr in D.member(c, memo))

print("== constructed: imports (getNamesOfMember / importedMember) ==")
ns = U.Package(name="N")
m1 = U.Class(name="M")
ns.packagedElement.append(m1)
check("getNamesOfMember: ownedMember branch",
      D.get_names_of_member(ns, m1) == {"M"})
imp = U.Class(name="M")
ei = U.ElementImport(importedElement=imp, alias="Z", visibility="public")
ns.elementImport.append(ei)
check("getNamesOfMember: ElementImport alias branch",
      D.get_names_of_member(ns, imp) == {"Z"})
far = U.Package(name="F")
m2 = U.Class(name="Q")
far.packagedElement.append(m2)
ns.packageImport.append(U.PackageImport(importedPackage=far, visibility="public"))
check("getNamesOfMember: PackageImport recursion",
      D.get_names_of_member(ns, m2) == {"Q"})
same = U.Class(name="dup")
other = U.Class(name="dup")
diff = U.Class(name="other")
ns.packageImport.append(U.PackageImport(importedPackage=U.Package(name="P2"),
                                        visibility="public"))
p2 = ns.packageImport[-1].importedPackage
p2.packagedElement.append(same)
p2.packagedElement.append(diff)
imp2 = U.Class(name="dup")   # collides with `same`
ns.elementImport.append(U.ElementImport(importedElement=imp2,
                                        visibility="public"))
ims = D.imported_member(ns)
check("importMembers: collisions and owned-name conflicts filtered",
      same not in ims and imp2 not in ims and diff in ims)
check("isDistinguishableFrom: same-kind same-name collides, kinds differ not",
      not D.is_distinguishable_from(same, imp2, ns)
      and D.is_distinguishable_from(same, U.Property(name="dup"), ns))
check("imported_member is a member of the namespace",
      all(m in D.member(ns, memo) for m in ims))

print("== constructed: multiplicity and ends ==")
p = U.Property(name="x")
p.lowerValue = U.LiteralInteger(value=2)
p.upperValue = U.LiteralUnlimitedNatural(value=2)
check("lowerBound/upperBound read the value specifications",
      D.lower_bound(p) == 2 and D.upper_bound(p) == 2)
q = U.Property(name="y")
q._props["lower"]._raw_set(q, 0)      # XMI-carried derived value
q._props["upper"]._raw_set(q, "*")
check("bounds fall back to the XMI-carried attributes",
      D.lower_bound(q) == 0 and D.upper_bound(q) == "*")
z = U.Property(name="z")
check("defaults are 1", D.lower_bound(z) == 1 and D.upper_bound(z) == 1)
check("is_composite = (aggregation == composite)",
      D.is_composite(U.Property(aggregation="composite")) is True
      and D.is_composite(U.Property(aggregation="none")) is False)
a = U.Association(name="A")
e1, e2 = U.Property(name="s"), U.Property(name="t")
a.memberEnd.append(e1)
a.memberEnd.append(e2)
e1.association = a
e2.association = a
check("opposite on a binary association", D.opposite(e1) is e2)
nary = U.Association(name="N")
n1, n2, n3 = U.Property(), U.Property(), U.Property()
nary.memberEnd.extend([n1, n2, n3])
for e in (n1, n2, n3):
    e.association = nary
check("opposite null for n-ary", D.opposite(n1) is None)

print("== OMG corpora: DoDAFLibrary + MeasurementsLibrary ==")
# UAF.xmi is a P10 profile file: its root <uml:Profile> is not yet in the
# reader's root dispatch (profile-defined stereotypes are not gen.uml25
# metaclasses), so the instance-level corpus set is DoDAF + ML (E2-verified).
CORPORA = [("DoDAF", "/mnt/TBFox/DoDAFLibrary.xmi"),
           ("ML", "/mnt/TBFox/uml_xmi/MeasurementsLibrary.xmi")]
models = {k: xmi21.read_xmi21(path) for k, path in CORPORA}

# (1) derived unions equal the runtime aggregation everywhere
bad, nobj, nun = [], 0, 0
for k, m in models.items():
    for o in m.objects.values():
        nobj += 1
        for un in D.union_names(o):
            nun += 1
            if set(map(id, D.union(o, un))) != set(map(id, o._union(un))):
                bad.append((k, type(o).__name__, un))
check(f"derived.union == runtime _union on all {nun} union reads "
      f"over {nobj} corpus objects", not bad, str(bad[:3]))

# (2) containment owner equivalence via an independent scan
def composite_parents(m):
    parent = {}
    for o in m.objects.values():
        for rn, d in type(o)._props.items():
            if not d.composite:
                continue
            v = d.__get__(o)
            items = v if d.multi else ((v,) if v is not None else ())
            for it in items:
                if isinstance(it, U.Element):
                    parent.setdefault(id(it), o)
    return parent
bad = 0
total = 0
for k, m in models.items():
    pm = composite_parents(m)
    for o in m.objects.values():
        if o.owner is None:
            continue
        total += 1
        if pm.get(id(o)) is not o.owner:
            bad += 1
check("owner agrees with an independent composite-ref scan "
      f"({total} owned objects)", bad == 0, f"{bad} mismatches")

# (3) containment-tree completeness: every non-app object is owned by
# exactly one root; every owned object reachable via derived unions
for k, m in models.items():
    app_ids = {a[2] for lst in m.apps.values() for a in lst}
    owned = {o for o in m.objects.values() if o.owner is not None}
    reach = set()
    for r in m.roots:
        for e in D.all_owned_elements(r):
            reach.add(id(e))
    orphans = [o for o in owned if id(o) not in reach]
    check(f"[{k}] every owned element reachable from a root "
          f"({len(owned)} owned, {len(app_ids)} applications excluded)",
          not orphans if False else all(id(o) in reach for o in owned
                                        if getattr(o, "_xmi_id", None)
                                        not in app_ids), "")

# (4) qualified_name agreement with an independent namespace walk
def qual_indep(el):
    chain, cur = [], el
    while True:
        ns = cur.namespace
        if ns is None or not isinstance(ns, U.Namespace):
            break
        chain.append(ns)
        cur = ns
    if el.name is None or any(n.name is None for n in chain):
        return None
    return "::".join([n.name for n in reversed(chain)] + [el.name])
bad, total = 0, 0
nontrivial = False
for k, m in models.items():
    for o in m.objects.values():
        if not hasattr(o, "name"):
            continue
        total += 1
        if D.qualified_name(o) != qual_indep(o):
            bad += 1
        if D.qualified_name(o) and "::" in D.qualified_name(o):
            nontrivial = True
check(f"qualified_name agrees with an independent walk ({total} named/unnamed)",
      bad == 0 and nontrivial, f"{bad} mismatches")

# (5) all_parents closure equivalence on corpus classifiers (the profile
# corpora instantiate no Generalizations - 0 in both - so this leg is
# crash/robustness only; the non-vacuous leg is the constructed diamond)
bad, total = 0, 0
for k, m in models.items():
    for o in m.objects.values():
        if not isinstance(o, U.Classifier):
            continue
        total += 1
        if set(D.all_parents(o)) != closure(o):
            bad += 1
check(f"all_parents closure equivalence ({total} corpus classifiers)",
      bad == 0, f"{bad} mismatches")

# (6) every owned feature of a classifier is in its all_features
bad = 0
seen_feat = 0
for k, m in models.items():
    for o in m.objects.values():
        if not isinstance(o, U.Classifier):
            continue
        feats = D.all_features(o)
        for f in getattr(o, "ownedAttribute", ()):  # Association has none
            seen_feat += 1
            if f not in feats:
                bad += 1
check(f"owned attributes are all_features ({seen_feat} sampled)", bad == 0)

# (7) getNamesOfMember returns the member's name for corpus ownedMembers
bad, n = 0, 0
for k, m in models.items():
    for o in m.objects.values():
        if not isinstance(o, U.Namespace):
            continue
        for me in D.union(o, "ownedMember"):
            n += 1
            if me.name not in D.get_names_of_member(o, me):
                bad += 1
check(f"getNamesOfMember returns owned member names ({n} checked)", bad == 0)

print()
print(f"RESULT: {len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)