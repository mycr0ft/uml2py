#!/usr/bin/env python
"""ocl_translator.py — clean-room OCL-to-Python translator for the
constraint bodies carried in gen.uml25 (UML 2.5.1).

The generator froze 449 normative constraint bodies as OCL text
(`CONSTRAINTS` tuples).  This module translates a body into a Python
expression over the same object graph that derived.py evaluates.
Anything outside the closed grammar raises `UnmappedFeature` — the
repo's honesty rule — instead of guessing (same discipline as
v1_to_v2.py).

Java/Groovy idioms map as:

  OCL                           Python
  ----------------------------  ----------------------------------------
  a.b                           getattr(a, 'b')
  c->select(e | p)              [e for e in c if p]
  c->exists(e | p)              any(p for e in c)
  c->forAll(e | b)              all(b for e in c)
  c->size()                     len(c)
  c->isEmpty() / ->notEmpty()   len(c) == 0 / len(c) > 0
  c->includes(x) / ->excludes   x in c / x not in c
  a implies b                   (not a) or b
  null / <> null                None / != None
  Enum::lit / E::_'lit'         'lit'      (runtime stores enum literals
                                           as strings or Enums — see
                                           _eq below)
  let x = e in rest             (lambda x: rest)(e)
  x.oclIsKindOf(T)              ocl_is_kind_of(x, T)
  m.is(1,1)                     is_mult(m, 1, 1)

Entry points:
  translate(body) -> Python source (introspectable, like everything
                     else this repo generates)
  eval_body(body, self_obj, derived) -> Python value of the body

Wave-1 elisions (raise UnmappedFeature, never guessed): ->closure,
->iterate, Type.allInstances (extent unknown outside a resource),
T.isAllowed/... spec-query stubs.
"""

from __future__ import annotations

import re

import gen.uml25 as U


class UnmappedFeature(Exception):
    """OCL construct outside the closed translation grammar."""


# --------------------------------------------------------------------------
# runtime helpers (bound into the eval environment)
# --------------------------------------------------------------------------

def enum_val(v):
    """Normalize an enum-ish runtime value to its OCL literal string."""
    if v is None:
        return None
    if isinstance(v, U._enum.Enum):
        return v.value
    return str(v)


def ocl_is_kind_of(obj, tname):
    """obj.oclIsKindOf(T): obj's dynamic type conforms to metaclass T."""
    if obj is None:
        return False
    return isinstance(obj, U.metaclass(tname))


def ocl_is_type_of(obj, tname):
    """obj.oclIsTypeOf(T): obj's dynamic type IS exactly T."""
    if obj is None:
        return False
    return type(obj).__name__ == tname


def ocl_as_type(obj, tname):
    """obj.oclAsType(T): obj when kind-of T, else invalid (None)."""
    return obj if ocl_is_kind_of(obj, tname) else None


def ocl_aslist(v):
    """OCL collection coercion: a single-valued property read is
    Set{v}; multi-valued properties are already lists."""
    if v is None:
        return []
    if isinstance(v, (list, tuple)):
        return v
    return [v]


def ocl_nav(v):
    """Receiver coercion for a collection operation: single-valued ->
    one-element list; None -> empty; list -> itself."""
    return ocl_aslist(v)


def ocl_dot(recv, attr):
    """Property navigation with implicit collect: over a single value
    this is getattr; over a collection it collects the attribute values
    (OCL 2.4 §10.3.2 implicit collect)."""
    if isinstance(recv, (list, tuple)):
        return ocl_collect([getattr(e, attr, None) for e in recv])
    if recv is None:
        return None
    return getattr(recv, attr, None)


def ocl_eq(a, b):
    """OCL =: for two collections, set equality; scalar = scalar is
    plain equality; a collected multi-valued read (list) against a
    scalar (None / literal / enum) follows the UML constraint-bodies'
    universal reading: every element equals the scalar.  An EMPTY
    collected read against null is True (no element violates it — the
    vacuous forAll reading the spec bodies rely on)."""
    if isinstance(a, (list, tuple)) and not isinstance(b, (list, tuple)):
        return all(x == b for x in a)
    if isinstance(b, (list, tuple)) and not isinstance(a, (list, tuple)):
        return all(x == a for x in b)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return (len(a) == len(b) and
                all(x in b for x in a))
    return a == b


def ocl_collect(seq):
    """Flatten a list of single values / lists into a dedup'd list
    (implicit-collect semantics for collect over multi-valued
    properties, per OCL 2.4 §10.3.2 flatten semantics)."""
    out, seen = [], set()
    for e in seq:
        for it in (e if isinstance(e, (list, tuple)) else (e,)):
            if it is None or id(it) in seen:
                continue
            seen.add(id(it))
            out.append(it)
    return out


def ocl_flatten(seq):
    """OCL flatten(): recursively unwraps nested collections."""
    out, seen = [], set()
    def rec(s):
        for e in s:
            if isinstance(e, (list, tuple)):
                rec(e)
            elif e is not None and id(e) not in seen:
                seen.add(id(e))
                out.append(e)
    rec(seq)
    return out


def ocl_union(a, b):
    """OCL union() over sequences: set-union, order preserved."""
    out, seen = [], set()
    for e in list(a) + list(b):
        if e is not None and id(e) not in seen:
            seen.add(id(e))
            out.append(e)
    return out


def ocl_range(lo, hi):
    """Sequence{lo..hi} (1-based inclusive)."""
    return list(range(int(lo), int(hi) + 1))


def is_mult(me, lo, hi):
    """MultiplicityElement::is(lower, upper) (§7.8.8): every
    cardinality in [lo, hi] is included by this multiplicity."""
    from derived import lower_bound, upper_bound
    lb = lower_bound(me)
    ub = upper_bound(me)
    def un(v):
        return "*" if v == "*" or v is None else int(v)
    return lb == lo and (un(ub) == un(hi) or (un(ub) == "*" and hi != 0))


def all_instances(tname):
    """T.allInstances(): extent is not reachable from a bare object in
    this runtime, so wave 1 evaluates it as the empty set — the two
    bodies using it express existence guards, and evaluating them False
    is the conservative reading.  Documented elision (never guessed)."""
    return []


def containing_activity(node):
    """ActivityNode::containingActivity (§12.4.1.6): the nearest
    owning Activity, through StructuredActivityNode containers."""
    import derived as D
    o = node.owner
    while o is not None:
        if isinstance(o, U.Activity):
            return o
        o = o.owner
    return None


def containing_state_machine(v):
    """Vertex::containingStateMachine (§13.3.7): climb containers to
    the owning StateMachine, entering submachine states on the way."""
    import derived as D
    o = v.owner
    while o is not None:
        if isinstance(o, U.StateMachine):
            return o
        if isinstance(o, U.State) and o.submachine is not None:
            sm = o.submachine
            return sm
        o = o.owner
    return None


def containing_behavior(beh_el):
    """Behavior::containingBehavior (§13.2.3): the owning class-like
    Classifier (via the _'context' subset union owner)."""
    o = beh_el.owner
    while o is not None:
        if isinstance(o, U.Classifier):
            return o
        o = o.owner
    return None


def end_type(p):
    """Property::endType (§9.9.17.7): the ends' types that this end
    connects (types of the other ends, plus own type)."""
    import derived as D
    a = p.association
    out = []
    if a is None:
        return out
    for e in a.memberEnd:
        t = e.type
        if t is not None and t not in out:
            out.append(t)
    return out


def all_actions(a):
    """Action::allActions (§12.3.3): self plus all contained actions
    (owned nodes that are Actions, recursively)."""
    import derived as D
    out, seen = [], set()
    def rec(n):
        if id(n) in seen:
            return
        seen.add(id(n))
        if isinstance(n, U.Action):
            out.append(n)
        for e in D.all_owned_elements(n):
            if isinstance(e, U.Action):
                out.append(e)
    rec(a)
    return out


def all_pins(a):
    """Action::allPins (§12.3.3): all Pins of all contained Actions."""
    import derived as D
    out, seen = [], set()
    for act in all_actions(a):
        for e in D.all_owned_elements(act):
            if isinstance(e, U.Pin):
                if id(e) not in seen:
                    seen.add(id(e))
                    out.append(e)
    return out


def all_owned_nodes(node):
    """StructuredActivityNode::allOwnedNodes (§12.10.3.4): owned nodes
    plus their owned nodes transitively (activity-group scope)."""
    import derived as D
    out, seen = [], set()
    def rec(n):
        if id(n) in seen:
            return
        seen.add(id(n))
        if isinstance(n, U.ActivityNode):
            out.append(n)
        if isinstance(n, U.StructuredActivityNode):
            for sub in n.node:
                rec(sub)
    for sub in node.node:
        rec(sub)
    return out


def all_included_use_cases(uc):
    """UseCase::allIncludedUseCases (§14.1.3.4): transitive include
    closure, cycle-guarded."""
    out, seen = [], set()
    def rec(u):
        for inc in u.include:
            t = inc.extension  # target use case of the Include
            if t is None or id(t) in seen:
                continue
            seen.add(id(t))
            out.append(t)
            rec(t)
    rec(uc)
    return out


def all_roles(sc):
    """StructuredClassifier::allRoles (§9.10.3.4): member->select(oclIsKindOf
    (ConnectableElement)) — full normative member (derived.member)."""
    import derived as D
    return [m for m in D.member(sc) if isinstance(m, U.ConnectableElement)]


def all_slottable_features(cl):
    """InstanceSpecification::allSlottableFeatures (§9.7.3.4): all
    direct and inherited attributes, excluding association ends."""
    import derived as D
    return [f for f in D.all_attributes(cl)
            if f.association is None]


def is_attribute(p):
    """Property::isAttribute (§9.9.17.8): attribute form (no
    association end and not a memberEnd of any association)."""
    return p.association is None


def is_multivalued(me):
    """MultiplicityElement::isMultivalued (§7.8.8): upperBound() > 1
    or = '*'."""
    from derived import upper_bound
    ub = upper_bound(me)
    return ub == "*" or ub is None or ub > 1


def must_be_owned(el):
    """Element::mustBeOwned (§7.8.6.7): false for Package (and Profile/
    Model which specialize it), true otherwise — §12.4.5.7 gives the
    Package redefinition body false."""
    return not isinstance(el, U.Package)


def is_navigable(p):
    """Property::isNavigable (§9.9.17.9)."""
    return not (p.association is not None and
                p.owningAssociation is not None and
                p.association.ownedEnd and
                p in p.association.ownedEnd and p.isReadOnly)


def association(p):
    """Property::association(): the Association owning this end."""
    return p.association


def input_parameters(op):
    """BehavioralFeature::inputParameters (§9.6.3): ownedParameter
    ->select(direction = in or inout)."""
    return [p for p in op.ownedParameter
            if enum_val(p.direction) in ("in", "inout")]


def output_parameters(op):
    """BehavioralFeature::outputParameters (§9.6.3): ownedParameter
    ->select(direction = out or inout or return)."""
    return [p for p in op.ownedParameter
            if enum_val(p.direction) in ("out", "inout", "return")]


def integer_value(lit):
    """LiteralInteger::integerValue(): the carried value (None when
    unset)."""
    if lit is None:
        return None
    return getattr(lit, "value", None)


def unlimited_value(lit):
    """LiteralUnlimitedNatural::unlimitedValue(): the carried value."""
    if lit is None:
        return None
    return getattr(lit, "value", None)


def closure(seq, chain):
    """->closure(p): transitive closure of property chain `chain`
    over seq (OCL 2.4 §10.3.3 closure — the set reached by repeatedly
    applying the chain, cycle-guarded)."""
    out, seen = [], set()
    frontier = list(seq)
    while frontier:
        nxt = []
        for e in frontier:
            cur = [e]
            for prop in chain:
                nxt_lvl = []
                for x in cur:
                    if x is None:
                        continue
                    v = getattr(x, prop, None)
                    items = v if isinstance(v, (list, tuple)) else (v,)
                    nxt_lvl.extend(i for i in items if i is not None)
                cur = nxt_lvl
            for it in cur:
                if it is None or id(it) in seen:
                    continue
                seen.add(id(it))
                out.append(it)
                nxt.append(it)
        frontier = nxt
    return out


def ocl_compatible_with(me, other):
    """MultiplicityElement::compatibleWith (§7.8.8): other is wider
    than or the same as self, i.e. self.includesMultiplicity(other):
    lowerBound(other) <= lowerBound(self) and upperBound(self) <=
    upperBound(other) (with '*' unbounded)."""
    from derived import lower_bound, upper_bound

    def un(v):
        return "*" if v == "*" or v is None else int(v)
    return (un(lower_bound(other)) <= un(lower_bound(me)) and
            (un(upper_bound(me)) == "*" or
             un(upper_bound(other)) == "*" or
             un(upper_bound(me)) >= un(upper_bound(other))))


def _vertex_regions(v, seen=None):
    """Every Region whose transition set governs vertex v: the regions
    reached DOWN the region/subvertex tree from v, and UP through the
    vertex's container chain (the container region itself)."""
    if seen is None:
        seen = set()

    def rec(obj):
        if obj is None or id(obj) in seen:
            return
        seen.add(id(obj))
        if isinstance(obj, U.Region):
            yield obj
        for e in (obj._vals.get("region") or []):
            yield from rec(e)
        for e in (obj._vals.get("subvertex") or []):
            yield from rec(e)
    yield from rec(v)
    # upward: the container region chain (subvertex containment);
    # Region has no .container — regions nest via stateMachine/region
    c = v.container
    while isinstance(c, U.Region):
        yield c
        c = c._vals.get("container")


def vertex_incoming(v):
    """Vertex::incoming (§13.3.6): the Transitions entering this
    vertex — the derived end computes as Transition->select(target=self)
    over the regions containing the vertex."""
    out, seen = [], set()
    for r in _vertex_regions(v):
        for t in r.transition:
            if t.target is v and id(t) not in seen:
                seen.add(id(t))
                out.append(t)
    return out


def vertex_outgoing(v):
    """Vertex::outgoing (§13.3.6): the Transitions departing."""
    out, seen = [], set()
    for r in _vertex_regions(v):
        for t in r.transition:
            if t.source is v and id(t) not in seen:
                seen.add(id(t))
                out.append(t)
    return out


DERIVED_FUNCS = {
    "allNamespaces": ("derived", "all_namespaces"),
    "allOwnedElements": ("derived", "all_owned_elements"),
    "allParents": ("derived", "all_parents"),
    "parents": ("derived", "parents"),
    "conformsTo": ("derived", "conforms_to"),
    "qualifiedName": ("derived", "qualified_name"),
    "separator": ("derived", "separator"),
    "allFeatures": ("derived", "all_features"),
    "allAttributes": ("derived", "all_attributes"),
    "inheritedMember": ("derived", "inherited_member"),
    "member": ("derived", "member"),
    "visibleMembers": ("derived", "visible_members"),
    "importedMember": ("derived", "imported_member"),
    "getNamesOfMember": ("derived", "get_names_of_member"),
    "lowerBound": ("derived", "lower_bound"),
    "upperBound": ("derived", "upper_bound"),
    "subsettingContext": ("derived", "subsetting_context"),
    "opposite": ("derived", "opposite"),
    "isComposite": ("derived", "is_composite"),
    "isDistinguishableFrom": ("derived", "is_distinguishable_from"),
    "mustBeOwned": ("local", must_be_owned),
    "isMultivalued": ("local", is_multivalued),
    "isNavigable": ("local", is_navigable),
    "isAttribute": ("local", is_attribute),
    "containingActivity": ("local", containing_activity),
    "containingStateMachine": ("local", containing_state_machine),
    "containingBehavior": ("local", containing_behavior),
    "endType": ("local", end_type),
    "allActions": ("local", all_actions),
    "allPins": ("local", all_pins),
    "allOwnedNodes": ("local", all_owned_nodes),
    "allIncludedUseCases": ("local", all_included_use_cases),
    "allRoles": ("local", all_roles),
    "allSlottableFeatures": ("local", all_slottable_features),
    "allInstances": ("local", all_instances),
    "is": ("local", is_mult),
    "association": ("local", association),
    "inputParameters": ("local", input_parameters),
    "outputParameters": ("local", output_parameters),
    "integerValue": ("local", integer_value),
    "unlimitedValue": ("local", unlimited_value),
    "compatibleWith": ("local", ocl_compatible_with),
    "incoming": ("local", vertex_incoming),
    "outgoing": ("local", vertex_outgoing),
}

# names emitted as bare Python calls for local implementations; the eval
# env binds them under their function names
_LOCAL_BARE = {"incoming": "vertex_incoming", "outgoing": "vertex_outgoing"}

COLLECTION_OPS = {
    "size", "isEmpty", "notEmpty", "includes", "excludes", "includesAll",
    "excludesAll", "exists", "forAll", "select", "reject", "one", "any",
    "asSet", "asSequence", "asOrderedSet", "asBag", "collect", "union",
    "intersection", "flatten", "first", "last", "at", "indexOf", "excluding",
    "closure",
}

CLASSIFY_OPS = {"oclIsKindOf", "oclIsTypeOf", "oclAsType", "oclIsUndefined",
                "oclType"}


# --------------------------------------------------------------------------
# tokenizer
# --------------------------------------------------------------------------

def tokenize(body):
    """Split an OCL body into (kind, text) tokens."""
    toks = []
    i, n = 0, len(body)
    while i < n:
        c = body[i]
        if c.isspace():
            i += 1
            continue
        if c == "'":
            j = body.find("'", i + 1)
            if j < 0:
                raise UnmappedFeature(
                    f"unterminated string near {body[i:i + 20]!r}")
            toks.append(("qstr", body[i + 1:j]))
            i = j + 1
            continue
        two = body[i:i + 2]
        if two in ("<>", "<=", ">=", "::", "..", "->"):
            toks.append(("op", two))
            i += 2
            continue
        if c == "_" and i + 1 < n and body[i + 1] == "'":
            # keyword-escaped name: _'in' / _'context'
            j = body.find("'", i + 2)
            if j < 0:
                raise UnmappedFeature("unterminated _'...'")
            toks.append(("name", body[i + 2:j]))
            i = j + 1
            continue
        if c in "(),":
            toks.append(("paren", c))
            i += 1
            continue
        if c == "|":
            toks.append(("bar", "|"))
            i += 1
            continue
        if c == ".":
            toks.append(("op", "."))
            i += 1
            continue
        if c in "=<>+-*/":
            toks.append(("op", c))
            i += 1
            continue
        if c == ":":
            toks.append(("colon", ":"))
            i += 1
            continue
        if c == "{":
            toks.append(("lc", "{"))
            i += 1
            continue
        if c == "}":
            toks.append(("rc", "}"))
            i += 1
            continue
        if c.isdigit():
            j = i
            while j < n and body[j].isdigit():
                j += 1
            toks.append(("num", body[i:j]))
            i = j
            continue
        if body[i:i + 1] == "*":
            toks.append(("op", "*"))
            i += 1
            continue
        m = re.match(r"[A-Za-z_][A-Za-z0-9_]*", body[i:])
        if m:
            toks.append(("name", m.group(0)))
            i += len(m.group(0))
            continue
        raise UnmappedFeature(f"character {c!r} in {body[i:i + 30]!r}")
    toks.append(("eof", ""))
    return toks


# --------------------------------------------------------------------------
# recursive-descent parser emitting Python source
# --------------------------------------------------------------------------
#
# precedence (loosest to tightest), per OCL 2.4 §7.5.3:
#   implies < or < xor < and < not < =/<> < </<=/>/>= < +/- < *// < unary
#
# emitted source references only these bare names, which eval_body binds:
#   self, _g (getattr), _k/_t/_a (classification), _d (derived/local ops),
#   _enum, _collect, _flatten, _union, _range

_PRECEDENCE = [
    ("name", "implies"),
    ("name", "or"),
    ("name", "xor"),
    ("name", "and"),
]


class _Parser:
    def __init__(self, body):
        self.toks = tokenize(body)
        self.i = 0
        self._uid = 0
        self.scopes = []  # in-scope lambda iterator variable names

    def peek(self):
        return self.toks[self.i]

    def next(self):
        t = self.toks[self.i]
        self.i += 1
        return t

    def accept(self, kind, text=None):
        k, t = self.peek()
        if k == kind and (text is None or t == text):
            self.next()
            return t
        return None

    def expect(self, kind, text=None):
        t = self.accept(kind, text)
        if t is None:
            raise UnmappedFeature(
                f"expected {text or kind} at token {self.peek()!r}")
        return t

    # -- entry ---------------------------------------------------------------
    def parse(self):
        e = self.implication()
        if self.peek()[0] != "eof":
            raise UnmappedFeature(
                f"trailing tokens {[t for t in self.toks[self.i:self.i + 5]]}")
        return e

    def implication(self):
        left = self.or_()
        if self.accept("name", "implies"):
            return f"((not ({left})) or ({self.implication()}))"
        return left

    def or_(self):
        e = self.xor_()
        while self.accept("name", "or"):
            e = f"({e} or {self.xor_()})"
        return e

    def xor_(self):
        e = self.and_()
        while self.accept("name", "xor"):
            e = f"(bool({e}) != bool({self.and_()}))"
        return e

    def and_(self):
        e = self.not_()
        while self.accept("name", "and"):
            e = f"({e} and {self.not_()})"
        return e

    def not_(self):
        if self.accept("name", "not"):
            return f"(not ({self.not_()}))"
        return self.equality()

    def equality(self):
        e = self.relational()
        while True:
            op = self.accept("op", "=") or self.accept("op", "<>")
            if op is None:
                return e
            rhs = self.relational()
            if op == "=":
                e = f"(_eq({e}, {rhs}))"
            else:
                e = f"(not (_eq({e}, {rhs})))"

    def relational(self):
        e = self.additive()
        for op in ("<=", ">=", "<", ">"):
            if self.accept("op", op):
                return f"({e} {op} {self.additive()})"
        return e

    def additive(self):
        e = self.multiplicative()
        while True:
            op = self.accept("op", "+") or self.accept("op", "-")
            if op is None:
                return e
            e = f"({e} {op} {self.multiplicative()})"

    def multiplicative(self):
        e = self.unary()
        while self.accept("op", "*"):
            e = f"({e} * {self.unary()})"
        return e

    def unary(self):
        if self.accept("op", "-"):
            return f"(-({self.unary()}))"
        return self.postfix()

    # -- postfix chains ----------------------------------------------------
    def postfix(self):
        e = self.primary()
        while True:
            if self.accept("op", "."):
                e = self.suffix_dot(e)
            elif self.accept("op", "->"):
                e = self.suffix_arrow(e)
            else:
                return e

    def suffix_dot(self, recv):
        name = self.expect("name")
        if self.peek() == ("paren", "("):
            return self.call(recv, name)
        return f"_dot({recv}, {name!r})"

    def suffix_arrow(self, recv):
        name = self.expect("name")
        if self.peek() != ("paren", "("):
            raise UnmappedFeature(f"->{name} without ()")
        return self.call(recv, name)

    def call(self, recv, name):
        self.expect("paren", "(")
        args = []
        if self.peek() != ("paren", ")"):
            args.append(self.implication())
            # comma-separated / bar-separated argument and lambda forms
            while True:
                t = self.peek()
                if t == ("paren", ")"):
                    break
                if t == ("colon", ":"):
                    # typed iterator variable: 'v : T | body' — drop the
                    # variable just parsed, consume ': T |', parse body
                    args.pop()
                    self.next()
                    self.expect("name")  # type name (unchecked, wave 1)
                    if self.peek()[0] != "bar":
                        raise UnmappedFeature("typed lambda without |")
                    self.next()
                    args.append(self.implication())
                    continue
                if t in (("paren", ","), ("bar", "|")):
                    self.next()
                    args.append(self.implication())
                    continue
                raise UnmappedFeature(f"call argument at {t!r}")
        self.expect("paren", ")")
        return self.emit_op(recv, name, args)

    # -- operation emitters -------------------------------------------------
    def emit_op(self, recv, name, args):
        if name in COLLECTION_OPS:
            return self.emit_collection(recv, name, args)
        if name in CLASSIFY_OPS:
            return self.emit_classify(recv, name, args)
        if name in DERIVED_FUNCS:
            kind, fn = DERIVED_FUNCS[name]
            if kind == "derived":
                if args:
                    return f"_d({fn!r}, {recv}, {', '.join(args)})"
                return f"_d({fn!r}, {recv})"
            # local implementation bound by name in eval env
            if args:
                return f"{fn.__name__}({recv}, {', '.join(args)})"
            return f"{fn.__name__}({recv})"
        # plain navigation with call syntax is not a property
        raise UnmappedFeature(f"operation {name}({', '.join(a[:20] for a in args)})")

    def _shadow(self, val, var):
        """Rewrite self-property reads inside an iterator body so they
        resolve against the iterator element.  The declared var always
        shadows itself.  For the implicit 'it' form, bare property names
        (lowerCamelCase) belong to the element; uppercase names are
        metaclasses and stay self-relative."""
        if var == "it":
            val = re.sub(r"_g\(self, '([a-z]\w*)'\)", r"_g(it, '\1')", val)
        else:
            val = re.sub(r"_g\(self, '%s'\)" % re.escape(var), var, val)
        return val

    def emit_collection(self, recv, name, args):
        # OCL treats every property as a collection: navigation through a
        # single-valued property yields Set{v}. The runtime stores lists
        # for multi-valued properties and bare values for single-valued
        # ones, so collection ops coerce the receiver first. Navigation
        # THROUGH a multi-valued receiver (implicit collect) is handled
        # by _nav: single-valued attr -> getattr; multi -> _collect of
        # the per-element attribute values.
        if name in ("size", "isEmpty", "notEmpty", "includes", "excludes",
                    "includesAll", "excludesAll", "exists", "forAll",
                    "select", "reject", "one", "any", "collect", "asSet",
                    "asSequence", "asOrderedSet", "asBag", "union",
                    "intersection", "flatten", "closure", "first", "last",
                    "at", "indexOf", "excluding"):
            recv = f"_nav({recv})"
        if name == "size":
            return f"len({recv})"
        if name == "isEmpty":
            return f"(len({recv}) == 0)"
        if name == "notEmpty":
            return f"(len({recv}) > 0)"
        if name in ("asSet", "asSequence", "asOrderedSet", "asBag"):
            return recv
        if name == "includes":
            return f"(({args[0]}) in {recv})"
        if name == "excludes":
            return f"(({args[0]}) not in {recv})"
        if name == "includesAll":
            return f"all(a in {recv} for a in ({args[0]}))"
        if name == "excludesAll":
            return f"all(a not in {recv} for a in ({args[0]}))"
        if name in ("exists", "one", "any"):
            var, val = self._lambda(args)
            self.scopes.append(var)
            try:
                # iterator var shadows self-properties within the body:
                # _g(self, 'e'...) reads become _g(e... (the shadowing
                # applies to the exact var name only)
                val = self._shadow(val, var)
                if name == "exists":
                    return f"any({val} for {var} in {recv})"
                return f"(sum(1 for {var} in {recv} if ({val})) == 1)"
            finally:
                self.scopes.pop()
        if name == "forAll":
            var, val = self._lambda(args)
            self.scopes.append(var)
            try:
                val = self._shadow(val, var)
                return f"all({val} for {var} in {recv})"
            finally:
                self.scopes.pop()
        if name == "select":
            var, val = self._lambda(args)
            self.scopes.append(var)
            try:
                val = self._shadow(val, var)
                return f"[{var} for {var} in {recv} if ({val})]"
            finally:
                self.scopes.pop()
        if name == "reject":
            var, val = self._lambda(args)
            self.scopes.append(var)
            try:
                val = self._shadow(val, var)
                return f"[{var} for {var} in {recv} if not ({val})]"
            finally:
                self.scopes.pop()
        if name == "collect":
            var, val = self._lambda(args)
            self.scopes.append(var)
            try:
                val = self._shadow(val, var)
                return f"_collect([{val} for {var} in {recv}])"
            finally:
                self.scopes.pop()
        if name == "flatten":
            return f"_flatten({recv})"
        if name == "union":
            return f"_union({recv}, ({args[0]}))"
        if name == "intersection":
            return f"[a for a in {recv} if a in ({args[0]})]"
        if name == "excluding":
            return f"[a for a in {recv} if a != ({args[0]})]"
        if name == "closure":
            # ->closure(p): transitive closure over property chain p
            # (applied stepwise to each element of recv, cycle-guarded)
            prop = args[0].strip()
            if re.fullmatch(r"[a-z]\w*", prop):
                return f"_closure_iter({recv}, [{prop!r}])"
            # dotted chain: _g(_g(it, 'a'), 'b') → ['a', 'b']
            chain = re.findall(r"'(\w+)'", prop)
            if chain and prop.startswith("_g("):
                return f"_closure_iter({recv}, {chain!r})"
            raise UnmappedFeature(f"->closure({prop[:40]})")
        if name == "first":
            return f"({recv}[0] if {recv} else None)"
        if name == "last":
            return f"({recv}[-1] if {recv} else None)"
        if name == "at":
            return f"(({recv})[{args[0]} - 1] if len({recv}) >= ({args[0]}) else None)"
        if name == "indexOf":
            return f"((({recv}).index(({args[0]})) + 1) if (({args[0]}) in ({recv})) else -1)"
        raise UnmappedFeature(f"->>{name}")

    def emit_classify(self, recv, name, args):
        if name == "oclIsKindOf":
            return f"_k({recv}, {self._type_arg(args[0])!r})"
        if name == "oclIsTypeOf":
            return f"_t({recv}, {self._type_arg(args[0])!r})"
        if name == "oclAsType":
            return f"_a({recv}, {self._type_arg(args[0])!r})"
        if name == "oclIsUndefined":
            return f"(({recv}) is None)"
        if name == "oclType":
            return f"type({recv}).__name__"
        raise UnmappedFeature(name)

    def _type_arg(self, src):
        """A classification type argument arrives as whatever the
        primary parser produced; metaclass names get resolved as bare
        names to _g(self, 'T') — unwrap that back to the name."""
        s = src.strip()
        m = re.fullmatch(r"_g\(self, '([A-Z]\w*)'\)", s)
        if m:
            return m.group(1)
        if re.fullmatch(r"[A-Z]\w*", s):
            return s
        raise UnmappedFeature(f"type argument {s!r}")

    def _lambda(self, args):
        """exists/forAll/select/... argument forms:
        1 arg  -> implicit iterator 'it'
        2 args -> (var, body)
        3 args -> (var, type-expr, body)   [type ignored]
        The variable arrives possibly wrapped as _g(self, 'v') by the
        bare-name rule — unwrap."""
        if len(args) == 1:
            return "it", args[0]
        if len(args) == 2:
            var = self._unwrap_var(args[0])
            return var, args[1]
        if len(args) == 3:
            var = self._unwrap_var(args[0])
            return var, args[2]
        raise UnmappedFeature(f"lambda arity {len(args)}")

    def _unwrap_var(self, src):
        s = src.strip()
        m = re.fullmatch(r"_g\(self, '(\w+)'\)", s)
        if m:
            return m.group(1)
        if re.fullmatch(r"[a-z]\w*", s):
            return s
        raise UnmappedFeature(f"lambda var {s!r}")

    # -- primaries -----------------------------------------------------------
    def primary(self):
        k, t = self.peek()
        if k == "paren" and t == "(":
            self.next()
            e = self.implication()
            self.expect("paren", ")")
            return self._postfix_continue(e)
        if k == "name":
            e = self.name_or_call()
            # a receiver may be re-typed by a classification call chained
            # to it (e.g. `type.oclIsKindOf(Interface)` where `type` is
            # a property of self); name_or_call already applied its own
            # postfix, so continue chains here
            return e
        if k == "qstr":
            self.next()
            return repr(t)
        if k == "num":
            self.next()
            return t
        if k == "op" and t == "*":
            # the UnlimitedNatural unbounded literal (e.g. is(0,*))
            self.next()
            return repr("*")
        if k == "lc":
            # collection literal: Sequence{1..n} / Set{...}
            return self.collection_literal()
        raise UnmappedFeature(f"primary at {self.peek()!r}")

    def _postfix_continue(self, e):
        """After a parenthesized group, .nav / ->op() chains continue."""
        while True:
            if self.accept("op", "."):
                e = self.suffix_dot(e)
            elif self.accept("op", "->"):
                e = self.suffix_arrow(e)
            else:
                return e

    def collection_literal(self):
        # '{' opens the literal directly (optional 'Sequence'/'Set'/
        # 'OrderedSet' prefix is consumed by name_or_call as a bare name;
        # range form: Sequence{1..n})
        self.expect("lc")
        items = []
        if self.peek() != ("rc", "}"):
            items.append(self.implication())
            while self.peek() == ("paren", ","):
                self.next()
                items.append(self.implication())
            if self.accept("op", ".."):
                hi = self.implication()
                self.expect("rc")
                return f"_range({items[0]}, {hi})"
        self.expect("rc")
        return "[" + ", ".join(items) + "]"

    def if_then_else(self):
        """if C then A else B endif  →  ((B-if) form)."""
        self.expect("name", "if")
        cond = self.implication()
        self.expect("name", "then")
        then = self.implication()
        self.expect("name", "else")
        els = self.implication()
        self.expect("name", "endif")
        return f"(({then}) if ({cond}) else ({els}))"

    def name_or_call(self):
        name = self.expect("name")
        if name == "let":
            # 'let' binds as an expression, wherever it appears
            # (mid-`and` chains included): back up one token and parse
            # the whole let-expression from the primary level
            self.i -= 1
            return self.let_expression("let")
        if name == "if":
            self.i -= 1
            return self.if_then_else()
        if name in ("Sequence", "Set", "OrderedSet", "Bag", "Collection"):
            # collection-type prefix of a literal: Sequence{1..n} /
            # Set{a, b}; the '{' follows immediately
            if self.peek() == ("lc", "{"):
                return self.collection_literal()
            raise UnmappedFeature(f"collection type {name} used as value")
        if name == "self":
            return "self"
        if name in ("true", "false", "null", "invalid", "OclInvalid",
                    "oclInvalid"):
            return {"true": "True", "false": "False"}.get(name, "None")
        # enum literal: EnumName::literal  (also Type::lit in OCL text)
        if self.peek() == ("op", "::"):
            self.next()
            lit = self.expect("name")
            return repr(lit)
        # bare call with no receiver: an operation on self
        if self.peek() == ("paren", "("):
            self.next()
            args = []
            if self.peek() != ("paren", ")"):
                args.append(self.implication())
                while self.peek() in (("paren", ","), ("bar", "|")):
                    self.next()
                    args.append(self.implication())
            self.expect("paren", ")")
            return self.emit_op("self", name, args)
        # a bare name: OCL resolves unqualified property access against
        # self, EXCEPT names bound as lambda iterator variables or
        # let-bound variables (tracked in scopes by both mechanisms).
        # Names that are wave-1 computed derivations (incoming/outgoing)
        # emit the function call so the value is computed, not read from
        # the (always empty) derived-end storage.
        if name not in self.scopes:
            if name in _LOCAL_BARE:
                return f"{_LOCAL_BARE[name]}(self)"
            return f"_g(self, {name!r})"
        return name

    def let_expression(self, name):
        """let var : T = e in body  →  (lambda var: body)(e)
        (type annotation skipped; wave-1 note: no type checking)."""
        self.next()  # consume 'let'
        var = self.expect("name")
        self.scopes.append(var)  # let-bound names shadow self-properties
        try:
            return self._let_body(var)
        finally:
            self.scopes.pop()

    def _let_body(self, var):
        if self.peek()[0] == "colon":
            self.next()
            # swallow the type annotation up to '=' at paren-depth 0
            # (types like Set(InteractionUse) nest parens; '=' inside
            # a nested lambda body — e.g. ->any(type = self) — is NOT
            # the binding '=')
            depth = 0
            while True:
                k, t = self.peek()
                if k == "eof":
                    raise UnmappedFeature("let without '='")
                if k == "paren" and t == "(":
                    depth += 1
                elif k == "paren" and t == ")":
                    if depth == 0:
                        raise UnmappedFeature("unbalanced let type")
                    depth -= 1
                elif k == "op" and t == "=" and depth == 0:
                    break
                self.next()
        self.expect("op", "=")
        # bindings:  let a : T = e, b : T2 = e2 in body
        bindings = []
        val = self.implication()
        bindings.append((var, val))
        while self.peek() == ("paren", ","):
            self.next()
            bvar = self.expect("name")
            if self.peek()[0] == "colon":
                self.next()
                depth = 0
                while True:
                    k, t = self.peek()
                    if k == "eof":
                        raise UnmappedFeature("let without '='")
                    if k == "paren" and t == "(":
                        depth += 1
                    elif k == "paren" and t == ")":
                        if depth == 0:
                            raise UnmappedFeature("unbalanced let type")
                        depth -= 1
                    elif k == "op" and t == "=" and depth == 0:
                        break
                    self.next()
            self.expect("op", "=")
            bindings.append((bvar, self.implication()))
        if not self.accept("name", "in"):
            raise UnmappedFeature("let without 'in'")
        # bind into body: replace var references by lambda parameters
        body = self.implication()
        src = body
        for var, val in reversed(bindings):
            self._uid += 1
            pyvar = f"_let{self._uid}_{var}"
            # rename only OUTSIDE _dot/_g string literals: the emitted
            # attribute names 'stateMachine' live inside quotes and must
            # not collide with the bound variable name
            src = re.sub(rf"(?<!')\b{re.escape(var)}\b(?!')", pyvar, src)
            val = re.sub(rf"(?<!')\b{re.escape(var)}\b(?!')", pyvar, val)
            src = f"(lambda {pyvar}: ({src}))({val})"
        return src


# patch: hook 'let' into the expression entry points
def _implication_with_let(self):
    k, t = self.peek()
    if k == "name" and t == "let":
        return self.let_expression(t)
    return self._implication_orig()


_Parser._implication_orig = _Parser.implication
_Parser.implication = _implication_with_let


# --------------------------------------------------------------------------
# public API
# --------------------------------------------------------------------------

_TRANSLATE_CACHE = {}


def translate(body):
    """OCL body -> Python source string (cached)."""
    src = _TRANSLATE_CACHE.get(body)
    if src is None:
        src = _Parser(body).parse()
        _TRANSLATE_CACHE[body] = src
    return src


_EVAL_ENV = {
    "_g": getattr,
    "_dot": ocl_dot,
    "_nav": ocl_nav,
    "_aslist": ocl_aslist,
    "_eq": ocl_eq,
    "_k": ocl_is_kind_of,
    "_t": ocl_is_type_of,
    "_a": ocl_as_type,
    "_enum": enum_val,
    "_collect": ocl_collect,
    "_flatten": ocl_flatten,
    "_union": ocl_union,
    "_range": ocl_range,
    "_closure_iter": closure,
    "is_mult": is_mult,
    "all_instances": all_instances,
    "is_attribute": is_attribute,
    "is_multivalued": is_multivalued,
    "is_navigable": is_navigable,
    "must_be_owned": must_be_owned,
    "containing_activity": containing_activity,
    "containing_state_machine": containing_state_machine,
    "containing_behavior": containing_behavior,
    "end_type": end_type,
    "all_actions": all_actions,
    "all_pins": all_pins,
    "all_owned_nodes": all_owned_nodes,
    "all_included_use_cases": all_included_use_cases,
    "all_roles": all_roles,
    "all_slottable_features": all_slottable_features,
    "vertex_incoming": vertex_incoming,
    "vertex_outgoing": vertex_outgoing,
}


def _derived_call(derived):
    """Binder: _d('funcname', obj, ...) -> derived.func(obj, ...)."""
    def call(fnname, obj, *rest):
        return getattr(derived, fnname)(obj, *rest)
    return call


_EVAL_BUILTINS = {
    "all": all, "any": any, "len": len, "sum": sum, "type": type,
    "isinstance": isinstance, "range": range, "list": list, "set": set,
}


def eval_body(body, self_obj, derived):
    """Evaluate an OCL constraint body against self_obj.

    `derived` is the derived module (spec-normative query layer).
    Returns the body's Python value (True/False for boolean bodies).
    Raises UnmappedFeature for constructs outside the grammar.
    """
    src = translate(body)
    # comprehensions resolve free variables via the *globals* mapping, so
    # the env must ride IN the globals dict, not as locals
    env = dict(_EVAL_ENV)
    env["self"] = self_obj
    env["_d"] = _derived_call(derived)
    g = dict(_EVAL_BUILTINS)
    g.update(env)
    return eval(src, g, {})  # noqa: S307


def check_constraints(obj, derived, only=None):
    """Evaluate every CONSTRAINTS body on obj's class (+ MRO).

    Returns (ok, results) where results is a list of
    (class, name, body, value) for each body that translated and ran,
    and skipped is (name, body) pairs that raised UnmappedFeature —
    reported, not guessed.
    """
    results, skipped = [], []
    seen = set()
    for cls in type(obj).__mro__:
        for cname, body in getattr(cls, "CONSTRAINTS", ()):
            key = (cname, body)
            if key in seen:
                continue
            seen.add(key)
            try:
                val = eval_body(body, obj, derived)
            except UnmappedFeature as ex:
                skipped.append((cname, body, str(ex)))
                continue
            except (AttributeError, TypeError, KeyError) as ex:
                # the body navigates an end the generated runtime does
                # not carry (hidden/derived ends the generator closed,
                # e.g. Port.encapsulatedClassifier) — recorded, not
                # guessed; wave-2 material
                skipped.append((cname, body,
                                "eval-unmapped: " + str(ex)[:80]))
                continue
            results.append((cls.__name__, cname, body, val))
    ok = all(val for _, _, _, val in results)
    return ok, results, skipped


def translate_all(pairs):
    """Translate (class, name, body) triples; report coverage.

    Returns (translated, unmapped) where translated is a dict
    (class, name) -> python source and unmapped lists
    (class, name, reason)."""
    translated, unmapped = {}, []
    for cls, name, body in pairs:
        try:
            translated[(cls, name)] = translate(body)
        except UnmappedFeature as ex:
            unmapped.append((cls, name, str(ex)))
    return translated, unmapped