#!/usr/bin/env python
"""UML 2.5.1 normative derived properties over gen.uml25 objects.

Clean-room implementations of the spec's derivation bodies (OCL quoted
per clause from formal/2017-12-05, chapter 7/9/12). The generated
modules stay byte-frozen: derivations are free functions. Everything is
standard library only.

Union evaluation (`union`) follows UML 2.5.1 §7.6.3: "the collection of
values denoted by the Property in some context is derived by being the
strict union of all of the values denoted, in the same context, by
Properties defined to subset it". Two consequences beyond the runtime's
generation-time flattening (`_Ref._union`):

  - a contributing property that is itself a derived union is expanded
    recursively (cycle-guarded) - its own value is the union of its
    subsetters, so those values belong to the outer union;
  - a property that REDEFINES a property that subsets a union also
    contributes: redefinition makes any reference to the redefined
    member resolve to the redefining member (§9.2.3.3), so its values
    are values of the subsetted property. The generated _UNIONS tables
    record subsettedProperty only; nine generated metaclasses depend on
    this closure (e.g. LoopNode.result redefines structuredNodeOutput,
    which subsets /output; RedefinableTemplateSignature.classifier
    redefines template, which subsets /owner).

Documented elisions (UnmappedFeature honesty rule): operations needing a
full OCL engine (arbitrary iterate/let/intersections over instance
models) are not attempted; e.g. Namespace.membersAreDistinguishable,
Classifier.inherit over all members, ActivityNode logic constraints.
"""
from __future__ import annotations

import gen.uml25 as uml

_SEPARATOR = "::"


# ---------------------------------------------------------------------------
# derived-union evaluation
# ---------------------------------------------------------------------------

def union_contributors(el, name):
    """Property names that contribute to union `name` on el's class:
    subsettedProperty contributors from the generated _UNIONS tables,
    plus the redefinition-aware closure."""
    names = []
    seen = set()
    for cls in type(el).__mro__:
        for c in getattr(cls, "_UNIONS", {}).get(name, ()):
            if c not in seen:
                seen.add(c)
                names.append(c)
    for pname, d in list(el._props.items()):
        if pname in seen:
            continue
        for r in d.redefines:
            if r == pname:
                continue  # self-redefinition marker, no semantics
            q = el._props.get(r)
            if q is not None and name in q.subsets:
                names.append(pname)
                seen.add(pname)
    return names


def union(el, name):
    """Value of derived union `name` (recursive, redefinition-aware,
    cycle-guarded; order: declaration order per MRO, deterministic)."""
    out, seen = [], set()
    _ucollect(el, name, out, seen, set())
    return out


def _ucollect(el, name, out, seen, progress):
    key = (id(el), name)
    if key in progress:
        return
    progress.add(key)
    try:
        for c in union_contributors(el, name):
            d = el._props.get(c)
            if d is None:
                continue
            if d.union:
                _ucollect(el, c, out, seen, progress)
                continue
            v = d.__get__(el)
            items = v if d.multi else ((v,) if v is not None else ())
            for it in items:
                if it is not None and id(it) not in seen:
                    seen.add(id(it))
                    out.append(it)
    finally:
        progress.discard(key)


def union_names(el):
    """All derived-union property names of el's class (for checks)."""
    out = []
    for cls in type(el).__mro__:
        for n in getattr(cls, "_UNIONS", {}):
            if n not in out:
                out.append(n)
    return out


# ---------------------------------------------------------------------------
# Element (UML 2.5.1 §7.8.6)
# ---------------------------------------------------------------------------

def owner(el):
    """Element::owner (§7.8.6.4, /owner {union}): the Element that owns
    this Element. The runtime maintains the containment inverse."""
    return el.owner


def all_owned_elements(el):
    """Element::allOwnedElements (§7.8.6.5):
    ownedElement->union(ownedElement->collect(e | e.allOwnedElements())).
    The traversal carries a global seen-set: the OCL is set-valued, so
    revisits (ill-formed ownership cycles) are dropped, not re-walked."""
    out, seen = [], set()
    _aoe(el, out, seen)
    return out


def _aoe(el, out, seen):
    for e in union(el, "ownedElement"):
        if id(e) in seen:
            continue
        seen.add(id(e))
        out.append(e)
        _aoe(e, out, seen)


def must_be_owned(el):
    """Element::mustBeOwned (§7.8.6.5 body true; §12.4.5.7 redefines
    body false for Package)."""
    return not isinstance(el, uml.Package)


# ---------------------------------------------------------------------------
# NamedElement / Namespace (UML 2.5.1 §7.8.9, §7.8.10)
# ---------------------------------------------------------------------------

def all_namespaces(el):
    """Namespace::allNamespaces (§7.8.9.6, ordered innermost-first,
    including the element's own innermost namespace):

    body: if owner.oclIsKindOf(TemplateParameter) and
      owner.signature.template.oclIsKindOf(Namespace) then
        enclosingNamespace.allNamespaces()->prepend(enclosingNamespace)
      else if namespace->isEmpty() then OrderedSet{}
      else namespace.allNamespaces()->prepend(namespace) endif endif
    """
    o = el.owner
    if isinstance(o, uml.TemplateParameter):
        sig = o.signature
        if sig is not None:
            tmpl = sig.template
            if isinstance(tmpl, uml.Namespace):
                return [tmpl] + all_namespaces(tmpl)
    ns = el.namespace
    if ns is None:
        return []
    return [ns] + all_namespaces(ns)


def qualified_name(el):
    """NamedElement::qualifiedName (§7.8.9.6): null unless the element
    and every namespace in allNamespaces() has a name; otherwise the
    '::'-joined names from the outermost namespace to the element."""
    if el.name is None:
        return None
    nss = all_namespaces(el)
    if any(ns.name is None for ns in nss):
        return None
    return _SEPARATOR.join([ns.name for ns in reversed(nss)] + [el.name])


def separator():
    """NamedElement::separator (§7.8.9.6): '::'."""
    return _SEPARATOR


def _import_name(ei):
    """ElementImport::getName (§7.8.7.6): alias if given, else the
    imported element's name."""
    if ei.alias:
        return ei.alias
    ie = ei.importedElement
    return ie.name if ie is not None else None


def get_names_of_member(ns, element):
    """Namespace::getNamesOfMember (§7.8.10.6), taking imports into
    account (ownedMember, ElementImport aliases, PackageImport
    recursion)."""
    if element in union(ns, "ownedMember"):
        return {element.name} if element.name is not None else set()
    eis = [ei for ei in (ns.elementImport or [])
           if ei.importedElement is element]
    if eis:
        return {_import_name(ei) for ei in eis} - {None}
    names = set()
    for pi in (ns.packageImport or []):
        pkg = pi.importedPackage
        if not isinstance(pkg, uml.Package):
            continue  # external (href) import: elision, see module notes
        if element in visible_members(pkg):
            names |= get_names_of_member(pkg, element)
    return names


def visible_members(pkg):
    """Package::visibleMembers (§12.4.5.6):
    member->select(m | m.oclIsKindOf(PackageableElement)
                     and self.makesVisible(m))."""
    out = []
    for m in union(pkg, "member"):
        if isinstance(m, uml.PackageableElement) and makes_visible(pkg, m):
            out.append(m)
    return out


def makes_visible(pkg, el):
    """Package::makesVisible (§12.4.5.6): ownedMember includes el, or a
    public ElementImport imports it, or a public PackageImport imports
    a Package whose member includes el."""
    if el in union(pkg, "ownedMember"):
        return True
    for ei in pkg.elementImport or []:
        if (ei.visibility == "public" and ei.importedElement is el):
            return True
    for pi in pkg.packageImport or []:
        ip = pi.importedPackage
        if (pi.visibility == "public" and isinstance(ip, uml.Package)
                and el in union(ip, "member")):
            return True
    return False


def is_distinguishable_from(a, b, ns):
    """NamedElement::isDistinguishableFrom (§7.8.9.6): kind-compatible
    names must be disjoint."""
    if not (isinstance(a, type(b)) or isinstance(b, type(a))):
        return True
    return not (get_names_of_member(ns, a)
                & get_names_of_member(ns, b))


def exclude_collisions(ns, imps):
    """Namespace::excludeCollisions (§7.8.10.6):
    imps->reject(imp1 | imps->exists(imp2 |
        not imp1.isDistinguishableFrom(imp2, self))). The exists
    quantifier is read over elements other than imp1 (the literal OCL
    would compare imp1 with itself and reject everything)."""
    out = []
    for imp1 in imps:
        if not any(imp2 is not imp1
                   and not is_distinguishable_from(imp1, imp2, ns)
                   for imp2 in imps):
            out.append(imp1)
    return out


def import_members(ns, imps):
    """Namespace::importMembers (§7.8.10.6): exclude collisions, then
    exclude names that conflict with ownedMembers."""
    out = []
    for imp in exclude_collisions(ns, imps):
        if all(is_distinguishable_from(imp, mem, ns)
               for mem in union(ns, "ownedMember")):
            out.append(imp)
    return out


def imported_member(ns):
    """Namespace::importedMember (§7.8.10.6):
    importMembers(elementImport.importedElement
                   union packageImport.importedPackage.visibleMembers()).
    Imports whose target is an external (href) marker are elided."""
    imps = [ei.importedElement for ei in (ns.elementImport or [])
            if ei.importedElement is not None]
    for pi in ns.packageImport or []:
        ip = pi.importedPackage
        if isinstance(ip, uml.Package):
            imps.extend(visible_members(ip))
    return import_members(ns, imps)


# ---------------------------------------------------------------------------
# Classifier (UML 2.5.1 §9.9.5)
# ---------------------------------------------------------------------------

def parents(cl):
    """Classifier::parents (§9.2.4.6 body generalization.general)."""
    out, seen = [], set()
    for g in cl.generalization or []:
        p = g.general
        if p is not None and id(p) not in seen:
            seen.add(id(p))
            out.append(p)
    return out


def all_parents(cl, _seen=None):
    """Classifier::allParents (§9.2.4.6):
    parents()->union(parents()->collect(allParents())). The traversal
    carries a seen-set: the OCL is set-valued, so revisits (ill-formed
    generalization cycles) are dropped, not re-walked."""
    if _seen is None:
        _seen = set()
    out = []
    for p in parents(cl):
        if id(p) in _seen:
            continue
        _seen.add(id(p))
        out.append(p)
        out.extend(all_parents(p, _seen))
    return out


def all_features(cl, _memo=None):
    """Classifier::allFeatures (§9.2.4.6):
    member->select(oclIsKindOf(Feature))."""
    if _memo is None:
        _memo = {}
    return [m for m in member(cl, _memo) if isinstance(m, uml.Feature)]


def all_attributes(cl, _memo=None):
    """Classifier::allAttributes (§9.2.4.6, ordered: owned attributes
    before inherited; relative order across multiple parents follows the
    parents() order - the spec leaves it undefined):

    attribute->union(parents().allAttributes())->select(member->includes)."""
    if _memo is None:
        _memo = {}
    mem = member(cl, _memo)
    out, seen = [], set()
    for p in (list(union(cl, "attribute"))
              + [x for par in parents(cl)
                 for x in all_attributes(par, _memo)]):
        if id(p) in seen:
            continue
        if p in mem:
            seen.add(id(p))
            out.append(p)
    return out


def has_visibility_of(cl, n):
    """Classifier::hasVisibilityOf (§9.2.4.6): non-private members are
    visible."""
    return n.visibility != "private"


def inheritable_members(cl, parent, _memo=None):
    """Classifier::inheritableMembers (§9.2.4.6): members of parent
    that may be inherited by cl (visibility-filtered)."""
    return [m for m in member(parent, _memo) if has_visibility_of(cl, m)]


def inherit(cl, inhs):
    """Classifier::inherit (§9.2.4.6): exclude members redefined by
    cl's own RedefinableElement ownedMembers."""
    redefiners = [m for m in union(cl, "ownedMember")
                  if isinstance(m, uml.RedefinableElement)]
    out = []
    for inh in inhs:
        if isinstance(inh, uml.RedefinableElement) and any(
                inh in union(rd, "redefinedElement") for rd in redefiners):
            continue
        out.append(inh)
    return out


def inherited_member(cl, _memo=None):
    """Classifier::inheritedMember (§9.2.4.6):
    inherit(parents()->collect(inheritableMembers(self)))."""
    if _memo is None:
        _memo = {}
    if id(cl) in _memo:
        return _memo[id(cl)]
    _memo[id(cl)] = []  # cycle guard
    inhs = []
    for p in parents(cl):
        inhs.extend(inheritable_members(cl, p, _memo))
    res = inherit(cl, inhs)
    _memo[id(cl)] = res
    return res


def member(cl, _memo=None):
    """Full normative Namespace::member: the stored member union plus
    the two derived contributors with normative bodies
    (inheritedMember - Classifier only - and importedMember); on
    instance models those are stored as null and must be computed."""
    vals = union(cl, "member")
    if isinstance(cl, uml.Classifier):
        vals = vals + inherited_member(cl, _memo)
    out, seen = [], set()
    for m in vals:
        if id(m) not in seen:
            seen.add(id(m))
            out.append(m)
    for m in imported_member(cl):
        if id(m) not in seen:
            seen.add(id(m))
            out.append(m)
    return out


def conforms_to(cl, other):
    """Classifier::conformsTo (§9.2.4.6): self or allParents includes."""
    return cl is other or other in all_parents(cl)


# ---------------------------------------------------------------------------
# MultiplicityElement (UML 2.5.1 §9.9.11)
# ---------------------------------------------------------------------------

def lower_bound(me):
    """MultiplicityElement::lowerBound (§7.8.8): the integerValue of
    lowerValue if given; otherwise 1. On instance models the XMI
    carries the derived `lower` attribute directly (no lowerValue
    element), so the carried value is used as the fall-back."""
    lv = me.lowerValue
    if lv is not None:
        return lv.value
    return 1 if me.lower is None else me.lower


def upper_bound(me):
    """MultiplicityElement::upperBound (§7.8.8): the
    unlimitedNaturalValue of upperValue if given; otherwise 1. Same
    XMI-carried fall-back as lower_bound."""
    uv = me.upperValue
    if uv is not None:
        return uv.value
    return 1 if me.upper is None else me.upper


# ---------------------------------------------------------------------------
# Property (UML 2.5.1 §9.9.17)
# ---------------------------------------------------------------------------

def is_composite(p):
    """Property::isComposite (§9.9.17.4, derived): aggregation is
    composite."""
    return p.aggregation == "composite"


def opposite(p):
    """Property::opposite (§9.9.17.6): the other end of a binary
    association, else null."""
    a = p.association
    if a is not None and len(a.memberEnd) == 2:
        return a.memberEnd[1] if a.memberEnd[0] is p else a.memberEnd[0]
    return None


def subsetting_context(p):
    """Property::subsettingContext (§9.9.17.6): the Classifiers at the
    other ends for an association end, else the attribute's Classifier."""
    a = p.association
    if a is not None:
        out, seen = [], set()
        for e in a.memberEnd:
            if e is p:
                continue
            t = e.type
            if t is not None and id(t) not in seen:
                seen.add(id(t))
                out.append(t)
        return out
    return [p.classifier] if p.classifier is not None else []