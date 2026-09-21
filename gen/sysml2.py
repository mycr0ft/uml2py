"""SysML v2 abstract syntax + KerML base, generated from the OMG XMIs.

Sources: SysML2.xmi (SysML v2 AS, ptc/25-02-15) + kerml.xmi (KerML).
Pure-stdlib Python. Do not edit by hand; regenerate with
generate_sysml2.py.

Contents: 175 metaclasses (82 KerML + 93 SysML v2), 428 properties,
103 operations, 7 enumerations, 623 normative constraints (metadata).
"""
import enum as _enum

class UnlimitedNatural:
    """UML UnlimitedNatural: a natural number or unbounded ("*")."""
    __slots__ = ('n',)
    def __init__(self, value):
        if value == '*': self.n = None
        else:
            n = int(value)
            if n < 0: raise ValueError('UnlimitedNatural must be >= 0')
            self.n = n
    @property
    def unbounded(self): return self.n is None
    def __eq__(self, other):
        return isinstance(other, UnlimitedNatural) and other.n == self.n
    def __hash__(self): return hash(self.n)
    def __repr__(self): return '*' if self.n is None else str(self.n)

class FeatureDirectionKind(_enum.Enum):
    """<p><code>FeatureDirectionKind</code> enumerates the possible kinds of <code>direction</code> that a <code>Feature</code> may be given as a member of a <code>Type</code>.</p>"""
    in_ = "in"
    inout = "inout"
    out = "out"

class PortionKind(_enum.Enum):
    """<p><code>PortionKind</code> is an enumeration of the specific kinds of <code><em>Occurrence</em></code> portions that can be represented by an <code>OccurrenceUsage</code>.</p>"""
    timeslice = "timeslice"
    snapshot = "snapshot"

class RequirementConstraintKind(_enum.Enum):
    """<p>A <code>RequirementConstraintKind</code> indicates whether a <code>ConstraintUsage</code> is an assumption or a requirement in a <code>RequirementDefinition</code> or <code>RequirementUsage</code>.</p>"""
    assumption = "assumption"
    requirement = "requirement"

class StateSubactionKind(_enum.Enum):
    """<p>A <code>StateSubactionKind</code> indicates whether the <code>action</code> of a StateSubactionMembership is an entry, do or exit action.</p>"""
    entry = "entry"
    do = "do"
    exit = "exit"

class TransitionFeatureKind(_enum.Enum):
    """<p>A <code>TransitionActionKind</code> indicates whether the <code>transitionFeature</code> of a <code>TransitionFeatureMembership</code> is a trigger, guard or effect.</p>"""
    trigger = "trigger"
    guard = "guard"
    effect = "effect"

class TriggerKind(_enum.Enum):
    """<p><code>TriggerKind</code> enumerates the kinds of triggers that can be represented by a <code>TriggerInvocationExpression</code>.</p>"""
    when = "when"
    at = "at"
    after = "after"

class VisibilityKind(_enum.Enum):
    """<p><code>VisibilityKind</code> is an enumeration whose literals specify the visibility of a <code>Membership</code> of an <code>Element</code> in a <code>Namespace</code> outside of that <code>Namespace</code>. Note that &quot;visibility&quot; specifically restricts whether an <code>Element</code> in a <code>Namespace</code> may be referenced by name from outside the <code>Namespace</code> and onl"""
    private = "private"
    protected = "protected"
    public = "public"

class _Ref:
    """Descriptor carrying one metamodel property and its semantics."""
    __slots__ = ('name', 't', 'multi', 'lo', 'hi', 'derived', 'union',
               'composite', 'readonly', 'subsets', 'redefines', 'assoc',
               'opp', 'owner_cls')
    def __init__(self, name, t, multi=False, lo=0, hi=1, derived=False,
                 union=False, composite=False, readonly=False,
                 subsets=(), redefines=(), assoc=None):
        self.name, self.t, self.multi, self.lo, self.hi = name, t, multi, lo, hi
        self.derived, self.union, self.composite = derived, union, composite
        self.readonly = readonly
        self.subsets, self.redefines, self.assoc = subsets, redefines, assoc
        self.opp = None
        self.owner_cls = None
    def __get__(self, inst, cls=None):
        if inst is None: return self
        if self.union: return inst._union(self.name)
        v = inst._vals.get(self.name)
        if v is None and self.multi:
            v = inst._vals[self.name] = _RefList(inst, self)
        return v
    def _check_set(self, inst):
        if self.union or self.derived or self.readonly:
            raise AttributeError(
                f'{type(inst).__name__}.{self.name} is derived/read-only')
    def __set__(self, inst, value):
        self._check_set(inst)
        old = inst._vals.get(self.name)
        if self.multi:
            lst = _RefList(inst, self)
            if value is not None:
                for v in value:
                    lst._raw_append(v)
                    _hook_add(inst, self, v)
            inst._vals[self.name] = lst
        else:
            if old is not None and old is not value:
                _hook_remove(inst, self, old)
            inst._vals[self.name] = value
            if value is not None:
                _hook_add(inst, self, value)
    def __delete__(self, inst):
        self._check_set(inst)
        old = inst._vals.pop(self.name, None)
        if old is None: return
        if self.multi:
            for v in list(old): _hook_remove(inst, self, v)
        else:
            _hook_remove(inst, self, old)
    def _raw_set(self, inst, value): inst._vals[self.name] = value
    def _raw_clear(self, inst): inst._vals.pop(self.name, None)

class _RefList(list):
    """List-valued property; every mutation fires the wiring hooks."""
    def __init__(self, inst, ref):
        super().__init__()
        self._inst, self._ref = inst, ref
    def _check(self): self._ref._check_set(self._inst)
    def append(self, v):
        self._check()
        super().append(v)
        _hook_add(self._inst, self._ref, v)
    def insert(self, i, v):
        self._check()
        super().insert(i, v)
        _hook_add(self._inst, self._ref, v)
    def extend(self, vs):
        self._check()
        for v in vs: self.append(v)
    def remove(self, v):
        self._check()
        super().remove(v)
        _hook_remove(self._inst, self._ref, v)
    def pop(self, i=-1):
        self._check()
        v = super().pop(i)
        _hook_remove(self._inst, self._ref, v)
        return v
    def __setitem__(self, i, v):
        self._check()
        old = self[i] if isinstance(i, int) else None
        super().__setitem__(i, v)
        if old is not None: _hook_remove(self._inst, self._ref, old)
        if isinstance(i, int): _hook_add(self._inst, self._ref, v)
    def _raw_append(self, v): super().append(v)
    def _raw_remove(self, v): super().remove(v)

def _hook_add(container, ref, child):
    """Composite ownership + association-opposite wiring (idempotent)."""
    if not isinstance(child, _Element):
        return
    if ref.composite:
        child._owner = container
        child._namespace = container
    oname = ref.opp
    if not oname or child._wiring: return
    od = child._props.get(oname)
    if od is None or od.derived or od.readonly or od.union: return
    child._wiring = True
    try:
        if od.multi:
            lst = od.__get__(child)
            if container not in lst:
                lst._raw_append(container)
                _hook_add(child, od, container)
        else:
            if od.__get__(child) is not container:
                od._raw_set(child, container)
                _hook_add(child, od, container)
    finally:
        child._wiring = False

def _hook_remove(container, ref, child):
    if not isinstance(child, _Element):
        return
    if ref.composite:
        if child._owner is container: child._owner = None
        if child._namespace is container: child._namespace = None
    oname = ref.opp
    if not oname or child._wiring: return
    od = child._props.get(oname)
    if od is None or od.derived or od.readonly or od.union: return
    child._wiring = True
    try:
        if od.multi:
            lst = od.__get__(child)
            if container in lst: lst._raw_remove(container)
        elif od.__get__(child) is container:
            od._raw_clear(child)
    finally:
        child._wiring = False

class _Element:
    """Common base of all KerML/SysML v2 metaclasses (KerML Element)."""
    _DECL: dict = {}
    _UNIONS: dict = {}
    _ABSTRACT = False
    def __init__(self, **kw):
        if type(self)._ABSTRACT:
            raise TypeError(
                f'{type(self).__name__} is abstract in the SysML v2'
                f' metamodel; instantiate a concrete subclass.')
        self._vals = {}
        self._owner = None
        self._namespace = None
        self._wiring = False
        for k, v in kw.items():
            if k not in self._props:
                raise TypeError(f'{type(self).__name__} has no property {k!r}')
            setattr(self, k, v)
    def _union(self, name):
        """Derived-union read: collect values of properties that subset."""
        out, seen = [], set()
        for cls in type(self).__mro__:
            for contrib in getattr(cls, '_UNIONS', {}).get(name, ()):
                d = self._props.get(contrib)
                if d is None or d.union: continue
                v = d.__get__(self)
                items = v if d.multi else ((v,) if v is not None else ())
                for it in items:
                    if id(it) not in seen:
                        seen.add(id(it))
                        out.append(it)
        return out
    def add(self, name, *values):
        """Append value(s) to a multi-valued property."""
        lst = getattr(self, name)
        for v in values: lst.append(v)
    def remove(self, name, *values):
        lst = getattr(self, name)
        for v in values: lst.remove(v)
    @property
    def owner(self):
        """Element.owner: derived as the inverse of composite containment."""
        return self._owner
    @property
    def namespace(self):
        """Namespace.namespace: derived from composite ownership."""
        return self._namespace
    @property
    def ownedElement(self):
        """KerML §7.3.2: ownedElement = the ownedRelatedElements of the
        Relationships this Element owns. Computed from the owner
        back-wiring maintained by _hook_add (the CMOF XMI leaves
        ownedElement a derived union with no subsetters)."""
        out, seen = [], set()
        for r in self.ownedRelationship:
            for e in r.ownedRelatedElement:
                if e is not None and id(e) not in seen:
                    seen.add(id(e))
                    out.append(e)
        return out
    def __repr__(self):
        n = self._vals.get('declaredName') or self._vals.get('name')
        if isinstance(n, str) and n:
            return f'<{type(self).__name__} {n!r}>'
        return f'<{type(self).__name__} #{id(self):x}>'


class Element(_Element):
    """<p>An <code>Element</code> is a constituent of a model that is uniquely identified relative to all other <code>Elements</code>. It can have <code>Relationships</code> with other <code>Elements</code>. Some of these <code>Relationships</code> might imply ownership of other <code>Elements</code>, which means that if an <code>Element</code> is deleted from a model, then so are all the <code>Elements</code> that it owns.</p>"""
    _PKG = "Elements"
    # (owner / namespace properties are hardcoded on _Element)
    _DECL = {
    # <p>Various alternative identifiers for this Element. Generally, these will be set by tools.</p>
    'aliasIds': _Ref('aliasIds', str, multi=True, lo=0, hi='*'),
    # <p>The declared name of this <code>Element</code>.</p>
    'declaredName': _Ref('declaredName', str),
    # <p>An optional alternative name for the <code>Element</code> that is intended to be shorter or i
    # n some way more succinct than its primary <code>name</code>. It may act as a modeler-specified i
    # dentifier for the <code>Element</code>, though it is then the responsibility of the modeler to m
    # aintain the uniqueness of this identifier within a model or relative to some other context.</p>
    'declaredShortName': _Ref('declaredShortName', str),
    # <p>The Documentation owned by this Element.</p>
    'documentation': _Ref('documentation', "Documentation", derived=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="Root-Elements-A_documentation_documentedElement"),
    # <p>The globally unique identifier for this Element. This is intended to be set by tooling, and i
    # t must not change during the lifetime of the Element.</p>
    'elementId': _Ref('elementId', str),
    # <p>Whether all necessary implied Relationships have been included in the <code>ownedRelationship
    # s</code> of this Element. This property may be true, even if there are not actually any <code>ow
    # nedRelationships</code> with <code>isImplied = true</code>, meaning that no such Relationships a
    # re actually implied for this Element. However, if it is false, then <code>ownedRelationships</co
    # de> may <em>not</em> contain any implied Relationships. That is, either <em>all</em> required im
    # plied Relationships must be included, or none of them.</p>
    'isImpliedIncluded': _Ref('isImpliedIncluded', bool),
    # <p>Whether this Element is contained in the ownership tree of a library model.</p>
    'isLibraryElement': _Ref('isLibraryElement', bool, derived=True),
    # <p>The name to be used for this <code>Element</code> during name resolution within its <code>own
    # ingNamespace</code>. This is derived using the <code>effectiveName()</code> operation. By defaul
    # t, it is the same as the <code>declaredName</code>, but this is overridden for certain kinds of 
    # <code>Elements</code> to compute a <code>name</code> even when the <code>declaredName</code> is 
    # null.</p>
    'name': _Ref('name', str, derived=True),
    # <p>The <code>ownedRelationships</code> of this <code>Element</code> that are <code>Annotations</
    # code>, for which this <code>Element</code> is the <code>annotatedElement</code>.</code>
    'ownedAnnotation': _Ref('ownedAnnotation', "Annotation", derived=True, multi=True, lo=0, hi='*', subsets=("ownedRelationship",), assoc="Root-Elements-A_ownedAnnotation_owningAnnotatedElement"),
    # <p>The Relationships for which this Element is the <tt>owningRelatedElement</tt>.</p>
    'ownedRelationship': _Ref('ownedRelationship', "Relationship", composite=True, multi=True, lo=0, hi='*', assoc="Root-Elements-A_ownedRelationship_owningRelatedElement"),
    # <p>The <code>owningRelationship</code> of this <code>Element</code>, if that <code>Relationship<
    # /code> is a <code>Membership</code>.</p>
    'owningMembership': _Ref('owningMembership', "OwningMembership", derived=True, subsets=("owningRelationship",), assoc="Root-Namespaces-A_ownedMemberElement_owningMembership"),
    # <p>The <code>Namespace</code> that owns this <code>Element</code>, which is the <code>membership
    # OwningNamespace</code> of the <code>owningMembership</code> of this <code>Element</code>, if any
    # .</p>
    'owningNamespace': _Ref('owningNamespace', "Namespace", derived=True, assoc="Root-Namespaces-A_ownedMember_owningNamespace"),
    # <p>The Relationship for which this Element is an <tt>ownedRelatedElement</tt>, if any.</p>
    'owningRelationship': _Ref('owningRelationship', "Relationship", assoc="Root-Elements-A_ownedRelatedElement_owningRelationship"),
    # <p>The full ownership-qualified name of this <code>Element</code>, represented in a form that is
    #  valid according to the KerML textual concrete syntax for qualified names (including use of unre
    # stricted name notation and escaped characters, as necessary). The <code>qualifiedName</code> is 
    # null if this <code>Element</code> has no <code>owningNamespace</code> or if there is not a compl
    # ete ownership chain of named <code>Namespaces</code> from a root <code>Namespace</code> to this 
    # <code>Element</code>. If the <code>owningNamespace</code> has other <code>Elements</code> with t
    # he same name as this one, then the <code>qualifiedName</code> is null for all such <code>Element
    # s</code> other than the first.</p>
    'qualifiedName': _Ref('qualifiedName', str, derived=True),
    # <p>The short name to be used for this <code>Element</code> during name resolution within its <co
    # de>owningNamespace</code>. This is derived using the <code>effectiveShortName()</code> operation
    # . By default, it is the same as the <code>declaredShortName</code>, but this is overridden for c
    # ertain kinds of <code>Elements</code> to compute a <code>shortName</code> even when the <code>de
    # claredName</code> is null.</p>
    'shortName': _Ref('shortName', str, derived=True),
    # <p>The <code>TextualRepresentations</code> that annotate this <code>Element</code>.</p>
    'textualRepresentation': _Ref('textualRepresentation', "TextualRepresentation", derived=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="Root-Elements-A_textualRepresentation_representedElement"),
    }
    CONSTRAINTS = (
        ("deriveElementName",
         "name = effectiveName()"
        ),
        ("deriveElementQualifiedName",
         "qualifiedName =     if owningNamespace = null then null     else if name <> null and    "
         "      owningNamespace.ownedMember->         select(m | m.name = name).indexOf(self) <> 1"
         " then null     else if owningNamespace.owner = null then escapedName()     else if ownin"
         "gNamespace.qualifiedName = null or              escapedName() = null then null     else "
         "owningNamespace.qualifiedName + '::' + escapedName()     endif endif endif endif"
        ),
        ("deriveElementOwnedAnnotation",
         "ownedAnnotation = ownedRelationship-> selectByKind(Annotation)-> select(a | a.annotatedE"
         "lement = self)"
        ),
        ("deriveElementShortName",
         "shortName = effectiveShortName()"
        ),
        ("deriveElementOwner",
         "owner = owningRelationship.owningRelatedElement"
        ),
        ("deriveElementIsLibraryElement",
         "isLibraryElement = libraryNamespace() <> null"
        ),
        ("deriveElementTextualRepresentation",
         "textualRepresentation = ownedElement->selectByKind(TextualRepresentation)"
        ),
        ("deriveElementOwnedElement",
         "ownedElement = ownedRelationship.ownedRelatedElement"
        ),
        ("deriveOwningNamespace",
         "owningNamespace = if owningMembership = null then null else owningMembership.membershipO"
         "wningNamespace endif"
        ),
        ("deriveElementDocumentation",
         "documentation = ownedElement->selectByKind(Documentation)"
        ),
        ("validateElementIsImpliedIncluded",
         "ownedRelationship->exists(isImplied) implies isImpliedIncluded"
        ),
    )
    def escapedName(self, arg: None = None) -> None:
        """
        <p>Return <code>name</code>, if that is not null, otherwise the <code>shortName</code>, if tha
        t is not null, otherwise null. If the returned value is non-null, it is returned as-is if it h
        as the form of a basic name, or, otherwise, represented as a restricted name according to the 
        lexical structure of the KerML textual notation (i.e., surrounded by single quote characters a
        nd with special characters escaped).</p>
        [Element operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def effectiveShortName(self, arg: None = None) -> None:
        """
        <p>Return an effective <code>shortName</code> for this <code>Element</code>. By default this i
        s the same as its <code>declaredShortName</code>.</p>
        [Element operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def effectiveName(self, arg: None = None) -> None:
        """
        <p>Return an effective <code>name</code> for this <code>Element</code>. By default this is the
         same as its <code>declaredName</code>.</p>
        [Element operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def libraryNamespace(self, arg: None = None) -> None:
        """
        <p>By default, return the library Namespace of the <code>owningRelationship</code> of this Ele
        ment, if it has one.</p>
        [Element operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def path(self, arg: None = None) -> None:
        """
        <p>Return a unique description of the location of this <code>Element</code> in the containment
         structure rooted in a root <code>Namespace</code>. If the <code>Element</code> has a non-null
         <code>qualifiedName</code>, then return that. Otherwise, if it has an <code>owningRelationshi
        p</code>, then return the string constructed by appending to the <code>path</code> of it's <co
        de>owningRelationship</code> the character <code>/</code> followed by the string representatio
        n of its position in the list of <code>ownedRelatedElements</code> of the <code>owningRelation
        ship</code> (indexed starting at 1). Otherwise, return the empty string.</p> <p>(Note that thi
        s operation is overridden for <code>Relationships</code> to use <code>owningRelatedElement</co
        de> when appropriate.)</p>
        [Element operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError

class Namespace(Element):
    """<p>A <code>Namespace</code> is an <code>Element</code> that contains other <code>Elements</code>, known as its <code>members</code>, via <code>Membership</code> <code>Relationships</code> with those <code>Elements</code>. The <code>members</code> of a <code>Namespace</code> may be owned by the <code>Namespace</code>, aliased in the <code>Namespace</code>, or imported into the <code>Namespace</code> via <code>Import</code> <code>Relationships</code>.</p> <p>A <code>Namespace</code> can provide names for its <code>members</code> via the <code>memberNames</code> and <code>memberShortNames</code> specified by the <code>Memberships</code> in the <code>Namespace</code>. If a <code>Membership</code> specifies a <code>memberName</code> and/or <code>memberShortName</code>, then those are names of the corresponding <code>memberElement</code> relative to the <code>Namespace</code>. For an <code>Own...[truncated]"""
    _PKG = "Namespaces"
    _DECL = {
    # <p>The <code>Memberships</code> in this <code>Namespace</code> that result from the <code>ownedI
    # mports</code> of this <code>Namespace</code>.</p>
    'importedMembership': _Ref('importedMembership', "Membership", derived=True, multi=True, lo=0, hi='*', subsets=("membership",), assoc="Root-Namespaces-A_importedMembership_importingNamespace"),
    # <p>The set of all member <code>Elements</code> of this <code>Namespace</code>, which are the <co
    # de>memberElements</code> of all <code>memberships</code> of the <code>Namespace</code>.</p>
    'member': _Ref('member', "Element", derived=True, multi=True, lo=0, hi='*', assoc="Root-Namespaces-A_member_namespace"),
    # <p>All <code>Memberships</code> in this <code>Namespace</code>, including (at least) the union o
    # f <code>ownedMemberships</code> and <code>importedMemberships</code>.</p>
    'membership': _Ref('membership', "Membership", derived=True, union=True, multi=True, lo=0, hi='*', assoc="Root-Namespaces-A_membership_membershipNamespace"),
    # <p>The <code>ownedRelationships</code> of this <code>Namespace</code> that are <code>Imports</co
    # de>, for which the <code>Namespace</code> is the <code>importOwningNamespace</code>.</p>
    'ownedImport': _Ref('ownedImport', "Import", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedRelationship",), assoc="Root-Namespaces-A_ownedImport_importOwningNamespace"),
    # <p>The owned <code>members</code> of this <code>Namespace</code>, which are the <cpde><code>owne
    # dMemberElements</code> of the <code>ownedMemberships</code> of the <code>Namespace</code>.</p>
    'ownedMember': _Ref('ownedMember', "Element", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("member",), assoc="Root-Namespaces-A_ownedMember_owningNamespace"),
    # <p>The <code>ownedRelationships</code> of this <code>Namespace</code> that are <code>Memberships
    # </code>, for which the <code>Namespace</code> is the <code>membershipOwningNamespace</code>.</p>
    'ownedMembership': _Ref('ownedMembership', "Membership", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("membership", "ownedRelationship",), assoc="Root-Namespaces-A_ownedMembership_membershipOwningNamespace"),
    }
    _UNIONS = {
        "membership": ("importedMembership", "ownedMembership",),
    }
    CONSTRAINTS = (
        ("validateNamespaceDistinguishibility",
         "membership->forAll(m1 | membership->forAll(m2 | m1 <> m2 implies m1.isDistinguishableFro"
         "m(m2)))"
        ),
        ("deriveNamespaceImportedMembership",
         "importedMembership = importedMemberships(Set{})"
        ),
        ("deriveNamespaceOwnedMembership",
         "ownedMembership = ownedRelationship->selectByKind(Membership)"
        ),
        ("deriveNamespaceOwnedMember",
         "ownedMember = ownedMembership->selectByKind(OwningMembership).ownedMemberElement"
        ),
        ("deriveNamespaceMembers",
         "member = membership.memberElement"
        ),
        ("deriveNamespaceOwnedImport",
         "ownedImport = ownedRelationship->selectByKind(Import)"
        ),
    )
    def namesOf(self, element: None = None, arg: None = None) -> None:
        """
        <p>Return the names of the given <code>element</code> as it is known in this <code>Namespace</
        code>.</p>
        [Namespace operation; params: element: ?, arg: ?; returns: nothing; stub - metamodel metadata 
        only]
        """
        raise NotImplementedError
    def visibilityOf(self, mem: None = None, arg: None = None) -> None:
        """
        <p>Returns this visibility of <code>mem</code> relative to this <code>Namespace</code>. If <co
        de>mem</code> is an <code>importedMembership</code>, this is the <code>visibility</code> of it
        s Import. Otherwise it is the <code>visibility</code> of the <code>Membership</code> itself.</
        p>
        [Namespace operation; params: mem: ?, arg: ?; returns: nothing; stub - metamodel metadata only
        ]
        """
        raise NotImplementedError
    def visibleMemberships(self, excluded: None = None, isRecursive: None = None, includeAll: None = None, arg: None = None) -> None:
        """
        <p>If <code>includeAll = true</code>, then return all the <code>Memberships</code> of this <co
        de>Namespace</code>. Otherwise, return only the publicly visible <code>Memberships</code> of t
        his <code>Namespace</code>, including <code>ownedMemberships</code> that have a <code>visibili
        ty</code> of <code>public</code> and <code>Memberships</code> imported with a <code>visibility
        </code> of <code>public</code>. If <code>isRecursive = true</code>, also recursively include a
        ll visible <code>Memberships</code> of any <code>public</code> owned <code>Namespaces</code>, 
        or, if <code>IncludeAll = true</code>, all <code>Memberships</code> of all owned <code>Namespa
        ces</code>. When computing imported <code>Memberships</code>, ignore this <code>Namespace</cod
        e> and any <code>Namespaces</code> in the given <code>excluded</code> set.</p>
        [Namespace operation; params: excluded: ?, isRecursive: ?, includeAll: ?, arg: ?; returns: not
        hing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def importedMemberships(self, excluded: None = None, arg: None = None) -> None:
        """
        <p>Derive the imported <code>Memberships</code> of this <code>Namespace</code> as the <code>im
        portedMembership</code> of all <code>ownedImports</code>, excluding those Imports whose <code>
        importOwningNamespace</code> is in the <code>excluded</code> set, and excluding <code>Membersh
        ips</code> that have distinguisibility collisions with each other or with any <code>ownedMembe
        rship</code>.</p>
        [Namespace operation; params: excluded: ?, arg: ?; returns: nothing; stub - metamodel metadata
         only]
        """
        raise NotImplementedError
    def membershipsOfVisibility(self, visibility: None = None, excluded: None = None, arg: None = None) -> None:
        """
        <p>If <code>visibility</code> is not null, return the <code>Memberships</code> of this <code>N
        amespace</code> with the given <code>visibility</code>, including <code>ownedMemberships</code
        > with the given <code>visibility</code> and <code>Memberships</code> imported with the given 
        <code>visibility</code>. If <code>visibility</code> is null, return all <code>ownedMemberships
        </code> and imported <code>Memberships</code> regardless of visibility. When computing importe
        d <code>Memberships</code>, ignore this <code>Namespace</code> and any <code>Namespaces</code>
         in the given <code>excluded</code> set.</p>
        [Namespace operation; params: visibility: ?, excluded: ?, arg: ?; returns: nothing; stub - met
        amodel metadata only]
        """
        raise NotImplementedError
    def resolve(self, qualifiedName: None = None, arg: None = None) -> None:
        """
        <p>Resolve the given qualified name to the named <code>Membership</code> (if any), starting wi
        th this <code>Namespace</code> as the local scope. The qualified name string must conform to t
        he concrete syntax of the KerML textual notation. According to the KerML name resolution rules
         every qualified name will resolve to either a single <code>Membership</code>, or to none.</p>
        [Namespace operation; params: qualifiedName: ?, arg: ?; returns: nothing; stub - metamodel met
        adata only]
        """
        raise NotImplementedError
    def resolveGlobal(self, qualifiedName: None = None, arg: None = None) -> None:
        """
        <p>Resolve the given qualified name to the named <code>Membership</code> (if any) in the effec
        tive global <code>Namespace</code> that is the outermost naming scope. The qualified name stri
        ng must conform to the concrete syntax of the KerML textual notation.</p>
        [Namespace operation; params: qualifiedName: ?, arg: ?; returns: nothing; stub - metamodel met
        adata only]
        """
        raise NotImplementedError
    def resolveLocal(self, name: None = None, arg: None = None) -> None:
        """
        <p>Resolve a simple <code>name</code> starting with this <code>Namespace</code> as the local s
        cope, and continuing with containing outer scopes as necessary. However, if this <code>Namespa
        ce</code> is a root <code>Namespace</code>, then the resolution is done directly in global sco
        pe.</p>
        [Namespace operation; params: name: ?, arg: ?; returns: nothing; stub - metamodel metadata onl
        y]
        """
        raise NotImplementedError
    def resolveVisible(self, name: None = None, arg: None = None) -> None:
        """
        <p>Resolve a simple name from the visible <code>Memberships</code> of this <code>Namespace</co
        de>.</p>
        [Namespace operation; params: name: ?, arg: ?; returns: nothing; stub - metamodel metadata onl
        y]
        """
        raise NotImplementedError
    def qualificationOf(self, qualifiedName: None = None, arg: None = None) -> None:
        """
        <p>Return a string with valid KerML syntax representing the qualification part of a given <cod
        e>qualifiedName</code>, that is, a qualified name with all the segment names of the given name
         except the last. If the given <code>qualifiedName</code> has only one segment, then return nu
        ll.</p>
        [Namespace operation; params: qualifiedName: ?, arg: ?; returns: nothing; stub - metamodel met
        adata only]
        """
        raise NotImplementedError
    def unqualifiedNameOf(self, qualifiedName: None = None, arg: None = None) -> None:
        """
        <p>Return the simple name that is the last segment name of the given <code>qualifiedName</code
        >. If this segment name has the form of a KerML unrestricted name, then "unescape" it by remov
        ing the surrounding single quotes and replacing all escape sequences with the specified charac
        ter.</p>
        [Namespace operation; params: qualifiedName: ?, arg: ?; returns: nothing; stub - metamodel met
        adata only]
        """
        raise NotImplementedError

class Type(Namespace):
    """<p>A <code>Type</code> is a <code>Namespace</code> that is the most general kind of <code>Element</code> supporting the semantics of classification. A <code>Type</code> may be a <code>Classifier</code> or a <code>Feature</code>, defining conditions on what is classified by the <code>Type</code> (see also the description of <code>isSufficient</code>).</p>"""
    _PKG = "Types"
    _DECL = {
    # <p>The interpretations of a <code>Type</code> with <code>differencingTypes</code> are asserted t
    # o be those of the first of those <code>Types</code>, but not including those of the remaining <c
    # ode>Types</code>. For example, a <code>Classifier</code> might be the difference of a <code>Clas
    # sifier</code> for people and another for people of a particular nationality, leaving people who 
    # are not of that nationality. Similarly, a feature of people might be the difference between a fe
    # ature for their children and a <code>Classifier</code> for people of a particular sex, identifyi
    # ng their children not of that sex (because the interpretations of the children <code>Feature</co
    # de> that identify those of that sex are also interpretations of the <code>Classifier</code> for 
    # that sex).</p>
    'differencingType': _Ref('differencingType', "Type", derived=True, multi=True, lo=0, hi='*', assoc="Core-Types-A_differencingType_differencedType"),
    # <p>The <code>features</code> of this <code>Type</code> that have a non-null <code>direction</cod
    # e>.</p>
    'directedFeature': _Ref('directedFeature', "Feature", derived=True, multi=True, lo=0, hi='*', subsets=("feature",), assoc="Core-Types-A_directedFeature_typeWithDirectedFeature"),
    # <p>All <code>features</code> of this <code>Type</code> with <code>isEnd = true</code>.</p>
    'endFeature': _Ref('endFeature', "Feature", derived=True, multi=True, lo=0, hi='*', subsets=("feature",), assoc="Core-Types-A_endFeature_typeWithEndFeature"),
    # <p>The <code>ownedMemberFeatures</code> of the <code>featureMemberships</code> of this <code>Typ
    # e</code>.</p>
    'feature': _Ref('feature', "Feature", derived=True, multi=True, lo=0, hi='*', subsets=("member",), assoc="Core-Types-A_typeWithFeature_feature"),
    # <p>The <code>FeatureMemberships</code> for <code>features</code> of this <code>Type</code>, whic
    # h include all <code>ownedFeatureMemberships</code> and those <code>inheritedMemberships</code> t
    # hat are <code>FeatureMemberships</code> (but does <em>not</em> include any <code>importedMembers
    # hips</code>).</p>
    'featureMembership': _Ref('featureMembership', "FeatureMembership", derived=True, multi=True, lo=0, hi='*', assoc="Core-Types-A_featureMembership_type"),
    # <p>All the <code>memberFeatures</code> of the <code>inheritedMemberships</code> of this <code>Ty
    # pe</code> that are <code>FeatureMemberships</code>.</p>
    'inheritedFeature': _Ref('inheritedFeature', "Feature", derived=True, multi=True, lo=0, hi='*', subsets=("feature",), assoc="Core-Types-A_inheritedFeature_inheritingType"),
    # <p>All <code>Memberships</code> inherited by this <code>Type</code> via <code>Specialization</co
    # de> or <code>Conjugation</code>. These are included in the derived union for the <code>membershi
    # ps</code> of the <code>Type</code>.</p>
    'inheritedMembership': _Ref('inheritedMembership', "Membership", derived=True, multi=True, lo=0, hi='*', subsets=("membership",), assoc="Core-Types-A_inheritedMembership_inheritingType"),
    # <p>All <code>features</code> related to this <code>Type</code> by <code>FeatureMemberships</code
    # > that have <code>direction</code> <code>in</code> or <code>inout</code>.</p>
    'input': _Ref('input', "Feature", derived=True, multi=True, lo=0, hi='*', subsets=("directedFeature",), assoc="Core-Types-A_input_typeWithInput"),
    # <p>The interpretations of a <code>Type</code> with <code>intersectingTypes</code> are asserted t
    # o be those in common among the <code>intersectingTypes</code>, which are the <code>Types</code> 
    # derived from the <code>intersectingType</code> of the <code>ownedIntersectings</code> of this <c
    # ode>Type</code>. For example, a <code>Classifier</code> might be an intersection of <code>Classi
    # fiers</code> for people of a particular sex and of a particular nationality. Similarly, a featur
    # e for people&#39;s children of a particular sex might be the intersection of a <code>Feature</co
    # de> for their children and a <code>Classifier</code> for people of that sex (because the interpr
    # etations of the children <code>Feature</code> that identify those of that sex are also interpret
    # ations of the Classifier for that sex).</p>
    'intersectingType': _Ref('intersectingType', "Type", derived=True, multi=True, lo=0, hi='*', assoc="Core-Types-A_intersectingType_intersectedType"),
    # <p>Indicates whether instances of this <code>Type</code> must also be instances of at least one 
    # of its specialized <code>Types</code>.</p>
    'isAbstract': _Ref('isAbstract', bool),
    # <p>Indicates whether this <code>Type</code> has an <code>ownedConjugator</code>.</p>
    'isConjugated': _Ref('isConjugated', bool, derived=True),
    # <p>Whether all things that meet the classification conditions of this <code>Type</code> must be 
    # classified by the <code>Type</code>.</p> <p>(A <code>Type</code>&nbsp;gives conditions that must
    #  be met by whatever it classifies, but when <code>isSufficient</code> is false, things may meet 
    # those conditions but still not be classified by the <code>Type</code>. For example, a Type <code
    # ><em>Car</em></code> that is not sufficient could require everything it classifies to have four 
    # wheels, but not all four wheeled things would classify as cars. However, if the <code>Type</code
    # > <code><em>Car</em></code> were sufficient, it would classify all four-wheeled things.)</p>
    'isSufficient': _Ref('isSufficient', bool),
    # <p>An <code>ownedMember</code> of this <code>Type</code> that is a <code>Multiplicity</code>, wh
    # ich constraints the cardinality of the <code>Type</code>. If there is no such <code>ownedMember<
    # /code>, then the cardinality of this <code>Type</code> is constrained by all the <code>Multiplic
    # ity</code> constraints applicable to any direct supertypes.</p>
    'multiplicity': _Ref('multiplicity', "Multiplicity", derived=True, subsets=("ownedMember",), assoc="Core-Features-A_multiplicity_typeWithMultiplicity"),
    # <p>All <code>features</code> related to this <code>Type</code> by <code>FeatureMemberships</code
    # > that have <code>direction</code> <code>out</code> or <code>inout</code>.</p>
    'output': _Ref('output', "Feature", derived=True, multi=True, lo=0, hi='*', subsets=("directedFeature",), assoc="Core-Types-A_output_typeWithOutput"),
    # <p>A <code>Conjugation</code> owned by this <code>Type</code> for which the <code>Type</code> is
    #  the <code>originalType</code>.</p>
    'ownedConjugator': _Ref('ownedConjugator', "Conjugation", derived=True, composite=True, subsets=("ownedRelationship",), assoc="Core-Types-A_ownedConjugator_owningType"),
    # <p>The <code>ownedRelationships</code> of this <code>Type</code> that are <code>Differencings</c
    # ode>, having this <code>Type</code> as their <code>typeDifferenced</code>.</p>
    'ownedDifferencing': _Ref('ownedDifferencing', "Differencing", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedRelationship",), assoc="Core-Types-A_typeDifferenced_ownedDifferencing"),
    # <p>The <code>ownedRelationships</code> of this <code>Type</code> that are <code>Disjoinings</cod
    # e>, for which the <code>Type</code> is the <code>typeDisjoined</code> <code>Type</code>.</p>
    'ownedDisjoining': _Ref('ownedDisjoining', "Disjoining", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedRelationship",), assoc="Core-Types-A_ownedDisjoining_owningType"),
    # <p>All <code>endFeatures</code> of this <code>Type</code> that are <code>ownedFeatures</code>.</
    # p>
    'ownedEndFeature': _Ref('ownedEndFeature', "Feature", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("endFeature", "ownedFeature",), assoc="Core-Types-A_ownedEndFeature_endOwningType"),
    # <p>The <code>ownedMemberFeatures</code> of the <code>ownedFeatureMemberships</code> of this <cod
    # e>Type</code>.</p>
    'ownedFeature': _Ref('ownedFeature', "Feature", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="Core-Types-A_ownedFeature_owningType"),
    # <p>The <code>ownedMemberships</code> of this <code>Type</code> that are <code>FeatureMemberships
    # </code>, for which the <code>Type</code> is the <code>owningType</code>. Each such <code>Feature
    # Membership</code> identifies an <code>ownedFeature</code> of the <code>Type</code>.</p>
    'ownedFeatureMembership': _Ref('ownedFeatureMembership', "FeatureMembership", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedMembership", "featureMembership",), assoc="Core-Types-A_ownedFeatureMembership_owningType"),
    # <p>The <code>ownedRelationships</code> of this <code>Type</code> that are <code>Intersectings</c
    # ode>, have the <code>Type</code> as their <code>typeIntersected</code>.</p>
    'ownedIntersecting': _Ref('ownedIntersecting', "Intersecting", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedRelationship",), assoc="Core-Types-A_ownedIntersecting_typeIntersected"),
    # <p>The <code>ownedRelationships</code> of this <code>Type</code> that are <code>Specializations<
    # /code>, for which the <code>Type</code> is the <code>specific</code> <code>Type</code>.</p>
    'ownedSpecialization': _Ref('ownedSpecialization', "Specialization", composite=True, multi=True, lo=0, hi='*', subsets=("ownedRelationship",), assoc="Core-Types-A_ownedSpecialization_owningType"),
    # <p>The <code>ownedRelationships</code> of this <code>Type</code> that are <code>Unionings</code>
    # , having the <code>Type</code> as their <code>typeUnioned</code>.</p>
    'ownedUnioning': _Ref('ownedUnioning', "Unioning", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedRelationship",), assoc="Core-Types-A_typeUnioned_ownedUnioning"),
    # <p>The interpretations of a <code>Type</code> with <code>unioningTypes</code> are asserted to be
    #  the same as those of all the <code>unioningTypes</code> together, which are the <code>Types</co
    # de> derived from the <code>unioningType</code> of the <code>ownedUnionings</code> of this <code>
    # Type</code>. For example, a <code>Classifier</code> for people might be the union of <code>Class
    # ifiers</code> for all the sexes. Similarly, a feature for people&#39;s children might be the uni
    # on of features dividing them in the same ways as people in general.</p>
    'unioningType': _Ref('unioningType', "Type", derived=True, multi=True, lo=0, hi='*', assoc="Core-Types-A_unioningType_unionedType"),
    }
    _UNIONS = {
        "membership": ("inheritedMembership", "ownedFeatureMembership",),
    }
    CONSTRAINTS = (
        ("deriveTypeOwnedConjugator",
         "ownedConjugator =     let ownedConjugators: Sequence(Conjugator) =          ownedRelatio"
         "nship->selectByKind(Conjugation) in     if ownedConjugators->isEmpty() then null      el"
         "se ownedConjugators->at(1) endif"
        ),
        ("validateTypeDifferencingTypesNotSelf",
         "differencingType->excludes(self)"
        ),
        ("deriveTypeUnioningType",
         "unioningType = ownedUnioning.unioningType"
        ),
        ("deriveTypeInheritedFeature",
         "inheritedFeature = inheritedMemberships-> selectByKind(FeatureMembership).memberFeature"
        ),
        ("deriveTypeDifferencingType",
         "differencingType = ownedDifferencing.differencingType"
        ),
        ("deriveTypeEndFeature",
         "endFeature = feature->select(isEnd)"
        ),
        ("deriveTypeOwnedIntersecting",
         "ownedRelationship->selectByKind(Intersecting)"
        ),
        ("deriveTypeInheritedMembership",
         "inheritedMembership = inheritedMemberships(Set{}, Set{}, false)"
        ),
        ("deriveTypeOwnedDisjoining",
         "ownedDisjoining = ownedRelationship->selectByKind(Disjoining)"
        ),
        ("deriveTypeOwnedDifferencing",
         "ownedDifferencing = ownedRelationship->selectByKind(Differencing)"
        ),
        ("validateTypeOwnedMultiplicity",
         "ownedMember->selectByKind(Multiplicity)->size() <= 1"
        ),
        ("deriveTypeOwnedFeatureMembership",
         "ownedFeatureMembership = ownedRelationship->selectByKind(FeatureMembership)"
        ),
        ("checkTypeSpecialization",
         "specializesFromLibrary('Base::Anything')"
        ),
        ("deriveTypeIntersectingType",
         "intersectingType = ownedIntersecting.intersectingType"
        ),
        ("deriveTypeMultiplicity",
         "multiplicity =      let ownedMultiplicities: Sequence(Multiplicity) =         ownedMembe"
         "r->selectByKind(Multiplicity) in     if ownedMultiplicities->isEmpty() then null     els"
         "e ownedMultiplicities->first()     endif"
        ),
        ("deriveTypeInput",
         "input = feature->select(f |      let direction: FeatureDirectionKind = directionOf(f) in"
         "     direction = FeatureDirectionKind::_'in' or     direction = FeatureDirectionKind::in"
         "out)"
        ),
        ("validateTypeUnioningTypesNotSelf",
         "unioningType->excludes(self)"
        ),
        ("validateTypeOwnedIntersectingNotOne",
         "ownedIntersecting->size() <> 1"
        ),
        ("deriveTypeOwnedSpecialization",
         "ownedSpecialization = ownedRelationship->selectByKind(Specialization)-> select(s | s.spe"
         "cial = self)"
        ),
        ("deriveTypeOutput",
         "output = feature->select(f |      let direction: FeatureDirectionKind = directionOf(f) i"
         "n     direction = FeatureDirectionKind::out or     direction = FeatureDirectionKind::ino"
         "ut)"
        ),
        ("deriveTypeOwnedEndFeature",
         "ownedEndFeature = ownedFeature->select(isEnd)"
        ),
        ("deriveTypeDirectedFeature",
         "directedFeature = feature->select(f | directionOf(f) <> null)"
        ),
        ("validateTypeOwnedUnioningNotOne",
         "ownedUnioning->size() <> 1"
        ),
        ("validateTypeAtMostOneConjugator",
         "ownedRelationship->selectByKind(Conjugation)->size() <= 1"
        ),
        ("deriveTypeOwnedFeature",
         "ownedFeature = ownedFeatureMembership.ownedMemberFeature"
        ),
        ("deriveTypeFeatureMembership",
         "featureMembership = ownedFeatureMembership->union( inheritedMembership->selectByKind(Fea"
         "tureMembership))"
        ),
        ("deriveTypeOwnedUnioning",
         "ownedUnioning = ownedRelationship->selectByKind(Unioning)"
        ),
        ("validateTypeOwnedDifferencingNotOne",
         "ownedDifferencing->size() <> 1"
        ),
        ("deriveTypeFeature",
         "feature = featureMembership.ownedMemberFeature"
        ),
        ("validateTypeIntersectingTypesNotSelf",
         "intersectingType->excludes(self)"
        ),
    )
    def visibleMemberships(self, excluded: None = None, isRecursive: None = None, includeAll: None = None, arg: None = None) -> None:
        """
        <p>The visible <code>Memberships</code> of a <code>Type</code> include <code>inheritedMembersh
        ips</code>.</p>
        [Type operation; params: excluded: ?, isRecursive: ?, includeAll: ?, arg: ?; returns: nothing;
         stub - metamodel metadata only]
        """
        raise NotImplementedError
    def inheritedMemberships(self, excludedNamespaces: None = None, excludedTypes: None = None, excludeImplied: None = None, arg: None = None) -> None:
        """
        <p>Return the <code>Memberships</code> inheritable from supertypes of this <code>Type</code> w
        ith redefined <code>Features</code> removed. When computing inheritable <code>Memberships</cod
        e>, exclude <code>Imports</code> of <code>excludedNamespaces</code>, <code>Specializations</co
        de> of <code>excludedTypes</code>, and, if <code>excludeImplied = true</code>, all implied <co
        de>Specializations</code>.</p>
        [Type operation; params: excludedNamespaces: ?, excludedTypes: ?, excludeImplied: ?, arg: ?; r
        eturns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def inheritableMemberships(self, excludedNamespaces: None = None, excludedTypes: None = None, excludeImplied: None = None, arg: None = None) -> None:
        """
        <p>Return all the non-<code>private</code> <code>Memberships</code> of all the supertypes of t
        his <code>Type</code>, excluding any supertypes that are this <code>Type</code> or are in the 
        given set of <code>excludedTypes</code>. If <code>excludeImplied = true</code>, then also tran
        sitively exclude any supertypes from implied <code>Specializations</code>.</p>
        [Type operation; params: excludedNamespaces: ?, excludedTypes: ?, excludeImplied: ?, arg: ?; r
        eturns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def nonPrivateMemberships(self, excludedNamespaces: None = None, excludedTypes: None = None, excludeImplied: None = None, arg: None = None) -> None:
        """
        <p>Return the <code>public</code>, <code>protected</code> and inherited <code>Memberships</cod
        e> of this <code>Type</code>. When computing imported <code>Memberships</code>, exclude the gi
        ven set of <code>excludedNamespaces</code>. When computing inherited <code>Memberships</code>,
         exclude <code>Types</code> in the given set of <code>excludedTypes</code>. If <code>excludeIm
        plied = true</code>, then also exclude any supertypes from implied <code>Specializations</code
        >.</p>
        [Type operation; params: excludedNamespaces: ?, excludedTypes: ?, excludeImplied: ?, arg: ?; r
        eturns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def removeRedefinedFeatures(self, memberships: None = None, arg: None = None) -> None:
        """
        <p>Return a subset of <code>memberships</code>, removing those <code>Memberships</code> whose 
        <code>memberElements</code> are <code>Features</code> and for which either of the following tw
        o conditions holds:</p> <ol> <li>The <code>memberElement</code> of the <code>Membership</code>
         is included in redefined <code>Features</code> of another <code>Membership</code> in <code>me
        mberships</code>.</li> <li>One of the redefined <code>Features</code> of the <code>Membership<
        /code> is a directly <code>redefinedFeature</code> of an <code>ownedFeature</code> of this <co
        de>Type</code>.</li> </ol> <p>For this purpose, the redefined <code>Features</code> of a <code
        >Membership</code> whose <code>memberElement</code> is a <code>Feature</code> includes the <co
        de>memberElement</code> and all <code>Features</code> directly or indirectly redefined by the 
        <code>memberElement</code>.</p>
        [Type operation; params: memberships: ?, arg: ?; returns: nothing; stub - metamodel metadata o
        nly]
        """
        raise NotImplementedError
    def allRedefinedFeaturesOf(self, membership: None = None, arg: None = None) -> None:
        """
        <p>If the <code>memberElement</code> of the given <code>membership</code> is a <code>Feature</
        code>, then return all <code>Features</code> directly or indirectly redefined by the <code>mem
        berElement</code>.</p>
        [Type operation; params: membership: ?, arg: ?; returns: nothing; stub - metamodel metadata on
        ly]
        """
        raise NotImplementedError
    def directionOf(self, feature: None = None, arg: None = None) -> None:
        """
        <p>If the given <code>feature</code> is a <code>feature</code> of this <code>Type</code>, then
         return its direction relative to this <code>Type</code>, taking conjugation into account.</p>
        [Type operation; params: feature: ?, arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def directionOfExcluding(self, feature: None = None, excluded: None = None, arg: None = None) -> None:
        """
        <p>Return the direction of the given <code>feature</code> relative to this <code>Type</code>, 
        excluding a given set of <code>Types</code> from the search of supertypes of this <code>Type</
        code>.</p>
        [Type operation; params: feature: ?, excluded: ?, arg: ?; returns: nothing; stub - metamodel m
        etadata only]
        """
        raise NotImplementedError
    def supertypes(self, excludeImplied: None = None, arg: None = None) -> None:
        """
        <p>If this <code>Type</code> is conjugated, then return just the <code>originalType</code> of 
        the <code>Conjugation</code>. Otherwise, return the <code>general</code> <code>Types</code> fr
        om all <code>ownedSpecializations</code> of this type, if <code>excludeImplied = false</code>,
         or all non-implied <code>ownedSpecializations</code>, if <code>excludeImplied = true</code>.<
        /p>
        [Type operation; params: excludeImplied: ?, arg: ?; returns: nothing; stub - metamodel metadat
        a only]
        """
        raise NotImplementedError
    def allSupertypes(self, result: None = None) -> None:
        """
        <p>Return this <code>Type</code> and all <code>Types</code> that are directly or transitively 
        supertypes of this <code>Type</code> (as determined by the <code>supertypes</code> operation w
        ith <code>excludeImplied = false</code>).</p>
        [Type operation; params: result: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def specializes(self, supertype: None = None, arg: None = None) -> None:
        """
        <p>Check whether this <code>Type</code> is a direct or indirect specialization of the given <c
        ode>supertype<code>.</p>
        [Type operation; params: supertype: ?, arg: ?; returns: nothing; stub - metamodel metadata onl
        y]
        """
        raise NotImplementedError
    def specializesFromLibrary(self, libraryTypeName: None = None, arg: None = None) -> None:
        """
        <p>Check whether this <code>Type</code> is a direct or indirect specialization of the named li
        brary <code>Type</code>. <code>libraryTypeName</code> must conform to the syntax of a KerML qu
        alified name and must resolve to a <code>Type</code> in global scope.</p>
        [Type operation; params: libraryTypeName: ?, arg: ?; returns: nothing; stub - metamodel metada
        ta only]
        """
        raise NotImplementedError
    def isCompatibleWith(self, otherType: None = None) -> None:
        """
        <p>By default, this <code>Type</code> is compatible with an <code>otherType</code> if it direc
        tly or indirectly specializes the <code>otherType</code>.</p>
        [Type operation; params: otherType: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def multiplicities(self, arg: None = None) -> None:
        """
        <p>Return the owned or inherited <code>Multiplicities</code> for this <code>Type<./code>.</p>
        [Type operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError

class Feature(Type):
    """<p>A <code>Feature</code> is a <code>Type</code> that classifies relations between multiple things (in the universe). The domain of the relation is the intersection of the <code>featuringTypes</code> of the <code>Feature</code>. (The domain of a <code>Feature</code> with no <code>featuringTyps</code> is implicitly the most general <code>Type</code> <em><code>Base::Anything</code></em> from the Kernel Semantic Library.) The co-domain of the relation is the intersection of the <code>types</code> of the <code>Feature</code>. <p>In the simplest cases, the <code>featuringTypes</code> and <code>types</code> are <code>Classifiers</code> and the <code>Feature</code> relates two things, one from the domain and one from the range. Examples include cars paired with wheels, people paired with other people, and cars paired with numbers representing the car length.</p> <p>Since <code>Features</code> a...[truncated]"""
    _PKG = "Features"
    _DECL = {
    # <p>The <code>Feature</code> that are chained together to determine the values of this <code>Feat
    # ure</code>, derived from the <code>chainingFeatures</code> of the <code>ownedFeatureChainings</c
    # ode> of this <code>Feature</code>, in the same order. The values of a <code>Feature</code> with 
    # <code>chainingFeatures</code> are the same as values of the last <code>Feature</code> in the cha
    # in, which can be found by starting with the values of the first <code>Feature</code> (for each i
    # nstance of the domain of the original <code>Feature</code>), then using each of those as domain 
    # instances to find the values of the second <code>Feature</code> in chainingFeatures, and so on, 
    # to values of the last <code>Feature</code>.</p>
    'chainingFeature': _Ref('chainingFeature', "Feature", derived=True, multi=True, lo=0, hi='*', assoc="Core-Features-A_chainingFeature_chainedFeature"),
    # <p>The second <code>chainingFeature</code> of the <code>crossedFeature</code> of the <code>owned
    # CrossSubsetting</code> of this <code>Feature</code>, if it has one. Semantically, the values of 
    # the <code>crossFeature</code> of an end <code>Feature</code> must include all values of the end 
    # <code>Feature</code> obtained when navigating from values of the other end <code>Features</code>
    #  of the same <code>owningType</code>. </p>
    'crossFeature': _Ref('crossFeature', "Feature", derived=True, assoc="Core-Features-A_crossFeature_featureCrossing"),
    # <p>Indicates how values of this <code>Feature</code> are determined or used (as specified for th
    # e <code>FeatureDirectionKind</code>).</p>
    'direction': _Ref('direction', None),
    # <p>The <code>Type</code> that is related to this <code>Feature</code> by an <code>EndFeatureMemb
    # ership</code> in which the <code>Feature</code> is an <code>ownedMemberFeature</code>.</p>
    'endOwningType': _Ref('endOwningType', "Type", derived=True, subsets=("owningType",), assoc="Core-Types-A_ownedEndFeature_endOwningType"),
    # <p>The last of the <code>chainingFeatures</code> of this <code>Feature</code>, if it has any. Ot
    # herwise, this <code>Feature</code> itself.</p>
    'featureTarget': _Ref('featureTarget', "Feature", derived=True, assoc="Core-Features-A_featureTarget_baseFeature"),
    # <p><code>Types</code> that feature this <code>Feature</code>, such that any instance in the doma
    # in of the <code>Feature</code> must be classified by all of these <code>Types</code>, including 
    # at least all the <code>featuringTypes</code> of its <code>typeFeaturings</code>. If the <code>Fe
    # ature</code> is chained, then the <code>featuringTypes</code> of the first <code>Feature</code> 
    # in the chain are also <code>featuringTypes</code> of the chained <code>Feature</code>.</p>
    'featuringType': _Ref('featuringType', "Type", derived=True, multi=True, lo=0, hi='*', assoc="Core-Features-A_featuringType_featureOfType"),
    # <p>Whether the <code>Feature</code> is a composite <code>feature</code> of its <code>featuringTy
    # pe</code>. If so, the values of the <code>Feature</code> cannot exist after its featuring instan
    # ce no longer does and cannot be values of another composite feature that is not on the same feat
    # uring instance.</p>
    'isComposite': _Ref('isComposite', bool),
    # <p>If <code>isVariable</code> is true, then whether the value of this <code>Feature</code> never
    # theless does not change over all <code><em>snapshots</em></code> of its <code>owningType</code>.
    # </p>
    'isConstant': _Ref('isConstant', bool),
    # <p>Whether the values of this <code>Feature</code> can always be computed from the values of oth
    # er <code>Features</code>.</p>
    'isDerived': _Ref('isDerived', bool),
    # <p>Whether or not this <code>Feature</code> is an end <code>Feature</code>. An end <code>Feature
    # </code> always has multiplicity 1, mapping each of its domain instances to a single co-domain in
    # stance. However, it may have a <code>crossFeature</code>, in which case values of the <code>cros
    # sFeature</code> must be the same as those found by navigation across instances of the <code>owni
    # ngType</code> from values of other end <code>Features</code> to values of this Feature. If the <
    # code>owningType</code> has <em>n</em> end <code>Features</code>, then the multiplicity, ordering
    # , and uniqueness declared for the <code>crossFeature</code> of any one of these end <code>Featur
    # es</code> constrains the cardinality, ordering, and uniqueness of the collection of values of th
    # at <code>Feature</code> reached by navigation when the values of the other <em>n-1</em> end <cod
    # e>Features</code> are held fixed.</p>
    'isEnd': _Ref('isEnd', bool),
    # <p>Whether an order exists for the values of this <code>Feature</code> or not.</p>
    'isOrdered': _Ref('isOrdered', bool),
    # <p>Whether the values of this <code>Feature</code> are contained in the space and time of instan
    # ces of the domain of the <code>Feature</code> and represent the same thing as those instances.</
    # p>
    'isPortion': _Ref('isPortion', bool),
    # <p>Whether or not values for this <code>Feature</code> must have no duplicates or not.</p>
    'isUnique': _Ref('isUnique', bool),
    # <p>Whether the value of this <code>Feature</code> might vary over time. That is, whether the <co
    # de>Feature</code> may have a different value for each <em><code>snapshot</code></em> of an <code
    # >owningType</code> that is an <em><code>Occurrence</code></em>.</p>
    'isVariable': _Ref('isVariable', bool),
    # <p>The one <code>ownedSubsetting</code> of this <code>Feature</code>, if any, that is a <code>Cr
    # ossSubsetting}, for which the <code>Feature</code> is the <code>crossingFeature</code>.</p>
    'ownedCrossSubsetting': _Ref('ownedCrossSubsetting', "CrossSubsetting", derived=True, composite=True, subsets=("ownedSubsetting",), assoc="Core-Features-A_ownedCrossSubsetting_crossingFeature"),
    # <p>The <code>ownedRelationships</code> of this <code>Feature</code> that are <code>FeatureChaini
    # ngs</code>, for which the <code>Feature</code> will be the <code>featureChained</code>.</p>
    'ownedFeatureChaining': _Ref('ownedFeatureChaining', "FeatureChaining", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedRelationship",), assoc="Core-Features-A_ownedFeatureChaining_featureChained"),
    # <p>The <code>ownedRelationships</code> of this <code>Feature</code> that are <code>FeatureInvert
    # ings</code> and for which the <code>Feature</code> is the <code>featureInverted</code>.</p>
    'ownedFeatureInverting': _Ref('ownedFeatureInverting', "FeatureInverting", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedRelationship",), assoc="Core-Features-A_ownedFeatureInverting_owningFeature"),
    # <p>The <code>ownedSubsettings</code> of this <code>Feature</code> that are <code>Redefinitions</
    # code>, for which the <code>Feature</code> is the <code>redefiningFeature</code>.</p>
    'ownedRedefinition': _Ref('ownedRedefinition', "Redefinition", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedSubsetting",), assoc="Core-Features-A_ownedRedefinition_owningFeature"),
    # <p>The one <code>ownedSubsetting</code> of this <code>Feature</code>, if any, that is a <code>Re
    # ferenceSubsetting</code>, for which the <code>Feature</code> is the <code>referencingFeature</co
    # de>.</p>
    'ownedReferenceSubsetting': _Ref('ownedReferenceSubsetting', "ReferenceSubsetting", derived=True, composite=True, subsets=("ownedSubsetting",), assoc="Core-Features-A_ownedReferenceSubsetting_referencingFeature"),
    # <p>The <code>ownedSpecializations</code> of this <code>Feature</code> that are <code>Subsettings
    # </code>, for which the <code>Feature</code> is the <code>subsettingFeature</code>.</p>
    'ownedSubsetting': _Ref('ownedSubsetting', "Subsetting", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedSpecialization",), assoc="Core-Features-A_owningFeature_ownedSubsetting"),
    # <p>The <code>ownedRelationships</code> of this <code>Feature</code> that are <code>TypeFeaturing
    # s</code> and for which the <code>Feature</code> is the <code>featureOfType</code>.</p>
    'ownedTypeFeaturing': _Ref('ownedTypeFeaturing', "TypeFeaturing", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedRelationship",), assoc="Core-Features-A_ownedTypeFeaturing_owningFeatureOfType"),
    # <p>The <code>ownedSpecializations</code> of this <code>Feature</code> that are <code>FeatureTypi
    # ngs</code>, for which the <code>Feature</code> is the <code>typedFeature</code>.</p>
    'ownedTyping': _Ref('ownedTyping', "FeatureTyping", composite=True, multi=True, lo=0, hi='*', subsets=("ownedSpecialization",), assoc="Core-Features-A_ownedTyping_owningFeature"),
    # <p>The <code>FeatureMembership</code> that owns this <code>Feature</code> as an <code>ownedMembe
    # rFeature</code>, determining its <code>owningType</code>.</p>
    'owningFeatureMembership': _Ref('owningFeatureMembership', "FeatureMembership", derived=True, subsets=("owningMembership",), assoc="Core-Types-A_ownedMemberFeature_owningFeatureMembership"),
    # <p>The <code>Type</code> that is the <code>owningType</code> of the <code>owningFeatureMembershi
    # p</code> of this <code>Feature</code>.</p>
    'owningType': _Ref('owningType', "Type", subsets=("featuringType", "owningNamespace",), assoc="Core-Types-A_ownedFeature_owningType"),
    # <p><code>Types</code> that restrict the values of this <code>Feature</code>, such that the value
    # s must be instances of all the <code>types</code>. The types of a <code>Feature</code> are deriv
    # ed from its <code>typings</code> and the <code>types</code> of its <code>subsettings</code>. If 
    # the <code>Feature</code> is chained, then the <code>types</code> of the last <code>Feature</code
    # > in the chain are also <code>types</code> of the chained <code>Feature</code>.</p>
    'type': _Ref('type', "Type", derived=True, multi=True, lo=0, hi='*', assoc="Core-Features-A_typedFeature_type"),
    }
    CONSTRAINTS = (
        ("validateFeatureEndNoDirection",
         "isEnd implied direction = null"
        ),
        ("checkFeatureCrossingSpecialization",
         "ownedCrossFeature() <> null implies crossFeature = ownedCrossFeature()"
        ),
        ("validateFeatureEndIsConstant",
         "isEnd and isVariable implies isConstant"
        ),
        ("checkFeatureObjectSpecialization",
         "ownedTyping.type->exists(selectByKind(Structure)) implies specializesFromLibary('Objects"
         "::objects')"
        ),
        ("deriveFeatureOwnedFeatureChaining",
         "ownedFeatureChaining = ownedRelationship->selectByKind(FeatureChaining)"
        ),
        ("checkFeatureOccurrenceSpecialization",
         "ownedTyping.type->exists(selectByKind(Class)) implies specializesFromLibrary('Occurrence"
         "s::occurrences')"
        ),
        ("deriveFeatureOwnedFeatureInverting",
         "ownedFeatureInverting = ownedRelationship->selectByKind(FeatureInverting)-> select(fi | "
         "fi.featureInverted = self)"
        ),
        ("validateFeatureIsVariable",
         "isVariable implies owningType <> null and owningType.specializes('Occurrences::Occurrenc"
         "e')"
        ),
        ("checkFeatureParameterRedefinition",
         "owningType <> null and not owningFeatureMembership.     oclIsKindOf(ReturnParameterMembe"
         "rship) and (owningType.oclIsKindOf(Behavior) or  owningType.oclIsKindOf(Step) and     (o"
         "wningType.oclIsKindOf(InvocationExpression) implies       not ownedRedefinition->exists("
         "not isImplied))  implies     let i : Integer =         owningType.ownedFeature->select(d"
         "irection <> null)->             reject(owningFeatureMembership.                 oclIsKin"
         "dOf(ReturnParameterMembership))->             indexOf(self) in     owningType.ownedSpeci"
         "alization.general->         forAll(supertype |             let ownedParameters : Sequenc"
         "e(Feature) =                 supertype.ownedFeature->select(direction <> null)->        "
         "              reject(owningFeatureMembership.                          oclIsKindOf(Retur"
         "nParameterMembership)) in             ownedParameters->size() >= i implies              "
         "   redefines(ownedParameters->at(i))"
        ),
        ("deriveFeatureOwnedRedefinition",
         "ownedRedefinition = ownedSubsetting->selectByKind(Redefinition)"
        ),
        ("validateFeatureChainingFeatureNotOne",
         "chainingFeature->size() <> 1"
        ),
        ("deriveFeatureChainingFeature",
         "chainingFeature = ownedFeatureChaining.chainingFeature"
        ),
        ("checkFeatureEndRedefinition",
         "isEnd and owningType <> null implies     let i : Integer =          owningType.ownedEndF"
         "eature->indexOf(self) in     owningType.ownedSpecialization.general->         forAll(sup"
         "ertype |              supertype.endFeature->size() >= i implies                 redefine"
         "s(supertype.endFeature->at(i))"
        ),
        ("checkFeatureValuationSpecialization",
         "direction = null and ownedSpecializations->forAll(isImplied) implies     ownedMembership"
         "->         selectByKind(FeatureValue)->         forAll(fv | specializes(fv.value.result)"
         ")"
        ),
        ("checkFeatureOwnedCrossFeatureSpecialization",
         "isOwnedCrossFeature() implies owner.oclAsType(Feature).type->forAll(t | self.specializes"
         "(t))"
        ),
        ("validateFeatureCrossFeatureType",
         "crossFeature <> null implies crossFeature.type->asSet() = type->asSet()"
        ),
        ("validateFeatureMultiplicityDomain",
         "multiplicity <> null implies multiplicity.featuringType = featuringType"
        ),
        ("validateFeatureChainingFeatureConformance",
         "Sequence{2..chainingFeature->size()}->forAll(i | chainingFeature->at(i).isFeaturedWithin"
         "(chainingFeature->at(i-1)))"
        ),
        ("deriveFeatureCrossFeature",
         "crossFeature =     if ownedCrossSubsetting = null then null     else          let chaini"
         "ngFeatures: Sequence(Feature) =              ownedCrossSubsetting.crossedFeature.chainin"
         "gFeature in         if chainingFeatures->size() < 2 then null         else chainingFeatu"
         "res->at(2)     endif"
        ),
        ("validateFeatureConstantIsVariable",
         "isConstant implies isVariable"
        ),
        ("validateFeaturePortionNotVariable",
         "isPortion implies not isVariable"
        ),
        ("deriveFeatureOwnedSubsetting",
         "ownedSubsetting = ownedSpecialization->selectByKind(Subsetting)"
        ),
        ("validateFeatureChainingFeaturesNotSelf",
         "chainingFeature->excludes(self)"
        ),
        ("deriveFeatureOwnedCrossSubsetting",
         "ownedCrossSubsetting =     let crossSubsettings: Sequence(CrossSubsetting) =          ow"
         "nedSubsetting->selectByKind(CrossSubsetting) in     if crossSubsettings->isEmpty() then "
         "null     else crossSubsettings->first()     endif"
        ),
        ("deriveFeatureFeaturingType",
         "featuringType =     let featuringTypes : OrderedSet(Type) =          featuring.type->asO"
         "rderedSet() in     if chainingFeature->isEmpty() then featuringTypes     else         fe"
         "aturingTypes->             union(chainingFeature->first().featuringType)->             a"
         "sOrderedSet()     endif"
        ),
        ("checkFeatureResultRedefinition",
         "owningType <> null and (owningType.oclIsKindOf(Function) and     self = owningType.oclAs"
         "Type(Function).result or  owningType.oclIsKindOf(Expression) and     self = owningType.o"
         "clAsType(Expression).result) implies     owningType.ownedSpecialization.general->       "
         "  select(oclIsKindOf(Function) or oclIsKindOf(Expression))->         forAll(supertype | "
         "            redefines(                 if superType.oclIsKindOf(Function) then          "
         "           superType.oclAsType(Function).result                 else                    "
         " superType.oclAsType(Expression).result                 endif)"
        ),
        ("deriveFeatureOwnedTyping",
         "ownedTyping = ownedGeneralization->selectByKind(FeatureTyping)"
        ),
        ("checkFeaturePortionSpecialization",
         "isPortion and ownedTyping.type->includes(oclIsKindOf(Class)) and owningType <> null and "
         "(owningType.oclIsKindOf(Class) or  owningType.oclIsKindOf(Feature) and     owningType.oc"
         "lAsType(Feature).type->         exists(oclIsKindOf(Class))) implies     specializesFromL"
         "ibrary('Occurrence::Occurrence::portions')"
        ),
        ("checkFeatureEndSpecialization",
         "isEnd and owningType <> null and (owningType.oclIsKindOf(Association) or  owningType.ocl"
         "IsKindOf(Connector)) implies     specializesFromLibrary('Links::Link::participant')"
        ),
        ("deriveFeatureType",
         "type =      let types : OrderedSet(Types) = OrderedSet{self}->         -- Note: The clos"
         "ure operation automatically handles circular relationships.         closure(typingFeatur"
         "es()).typing.type->asOrderedSet() in     types->reject(t1 | types->exist(t2 | t2 <> t1 a"
         "nd t2.specializes(t1)))"
        ),
        ("validateFeatureOwnedCrossSubsetting",
         "ownedSubsetting->selectByKind(CrossSubsetting)->size() <= 1"
        ),
        ("checkFeatureSuboccurrenceSpecialization",
         "isComposite and ownedTyping.type->includes(oclIsKindOf(Class)) and owningType <> null an"
         "d (owningType.oclIsKindOf(Class) or  owningType.oclIsKindOf(Feature) and     owningType."
         "oclAsType(Feature).type->         exists(oclIsKindOf(Class))) implies     specializesFro"
         "mLibrary('Occurrence::Occurrence::suboccurrences')"
        ),
        ("deriveFeatureOwnedReferenceSubsetting",
         "ownedReferenceSubsetting =     let referenceSubsettings : OrderedSet(ReferenceSubsetting"
         ") =         ownedSubsetting->selectByKind(ReferenceSubsetting) in     if referenceSubset"
         "tings->isEmpty() then null     else referenceSubsettings->first() endif"
        ),
        ("checkFeatureSubobjectSpecialization",
         "isComposite and ownedTyping.type->includes(oclIsKindOf(Structure)) and owningType <> nul"
         "l and (owningType.oclIsKindOf(Structure) or  owningType.type->includes(oclIsKindOf(Struc"
         "ture))) implies     specializesFromLibrary('Occurrence::Occurrence::suboccurrences')"
        ),
        ("validateFeatureCrossFeatureSpecialization",
         "crossFeature <> null implies     ownedRedefinition.redefinedFeature.crossFeature->      "
         "       forAll(f | f <> null implies crossFeature.specializes(f))"
        ),
        ("deriveFeatureOwnedTypeFeaturing",
         "ownedTypeFeaturing = ownedRelationship->selectByKind(TypeFeaturing)-> select(tf | tf.fea"
         "tureOfType = self)"
        ),
        ("validateFeatureOwnedReferenceSubsetting",
         "ownedSubsetting->selectByKind(ReferenceSubsetting)->size() <= 1"
        ),
        ("checkFeatureDataValueSpecialization",
         "ownedTyping.type->exists(selectByKind(DataType)) implies specializesFromLibrary('Base::d"
         "ataValues')"
        ),
        ("checkFeatureFlowFeatureRedefinition",
         "owningType <> null and owningType.oclIsKindOf(FlowEnd) and owningType.ownedFeature->at(1"
         ") = self implies     let flowType : Type = owningType.owningType in     flowType <> null"
         " implies         let i : Integer =              flowType.ownedFeature.indexOf(owningType"
         ") in         (i = 1 implies              redefinesFromLibrary('Transfers::Transfer::sour"
         "ce::sourceOutput')) and         (i = 2 implies             redefinesFromLibrary('Transfe"
         "rs::Transfer::source::targetInput'))"
        ),
        ("deriveFeatureFeatureTarget",
         "featureTarget = if chainingFeature->isEmpty() then self else chainingFeature->last() end"
         "if"
        ),
        ("validateFeatureEndMultiplicity",
         "isEnd implies multiplicities().allSuperTypes()->flatten()-> selectByKind(MultiplicityRan"
         "ge)->exists(hasBounds(1,1))"
        ),
        ("checkFeatureOwnedCrossFeatureTypeFeaturing",
         "isOwnedCrossFeature() implies     let otherEnds : OrderedSet(Feature) =          owner.o"
         "clAsType(Feature).owningType.endFeature->excluding(self) in     if (otherEnds->size() = "
         "1) then         featuringType = otherEnds->first().type     else         featuringType->"
         "size() = 1 and         featuringType->first().isCartesianProduct() and         featuring"
         "Type->first().asCartesianProduct() = otherEnds.type and         featuringType->first().a"
         "llSupertypes()->includesAll(             owner.oclAsType(Feature).ownedRedefinition.rede"
         "finedFeature->                select(crossFeature() <> null).crossFeature().featuringTyp"
         "e)           endif"
        ),
        ("checkFeatureOwnedCrossFeatureRedefinitionSpecialization",
         "isOwnedCrossFeature() implies     ownedSubsetting.subsettedFeature->includesAll(        "
         " owner.oclAsType(Feature).ownedRedefinition.redefinedFeature->             select(crossF"
         "eature <> null).crossFeature)"
        ),
        ("checkFeatureFeatureMembershipTypeFeaturing",
         "owningFeatureMembership <> null implies featuringTypes->exists(t | isFeaturingType(t))"
        ),
        ("validateFeatureEndNotDerivedAbstractCompositeOrPortion",
         "isEnd implies not (isDerived or isAbstract or isComposite or isPortion)"
        ),
        ("checkFeatureSpecialization",
         "specializesFromLibrary('Base::things')"
        ),
    )
    def directionFor(self, type: None = None, arg: None = None) -> None:
        """
        <p>Return the <code>directionOf</code> this <code>Feature</code> relative to the given <code>t
        ype</code>.</p>
        [Feature operation; params: type: ?, arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def effectiveShortName(self, arg: None = None) -> None:
        """
        <p>If a <code>Feature</code> has no <code>declaredShortName</code> or <code>declaredName</code
        >, then its effective <code>shortName</code> is given by the effective <code>shortName</code> 
        of the <code>Feature</code> returned by the <code>namingFeature()</code> operation, if any.</p
        >
        [Feature operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def effectiveName(self, arg: None = None) -> None:
        """
        <p>If a <code>Feature</code> has no <code>declaredName</code> or <code>declaredShortName</code
        > , then its effective <code>name</code> is given by the effective <code>name</code> of the <c
        ode>Feature</code> returned by the <code>namingFeature()</code> operation, if any.</p>
        [Feature operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def namingFeature(self, arg: None = None) -> None:
        """
        <p>By default, the naming <code>Feature</code> of a <code>Feature</code> is given by its first
         <code>redefinedFeature</code> of its first <code>ownedRedefinition</code>, if any.</p>
        [Feature operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def supertypes(self, excludeImplied: None = None, arg: None = None) -> None:
        """
        [Feature operation; params: excludeImplied: ?, arg: ?; returns: nothing; stub - metamodel meta
        data only]
        """
        raise NotImplementedError
    def redefines(self, redefinedFeature: None = None, arg: None = None) -> None:
        """
        <p>Check whether this <code>Feature</code> <em>directly</em> redefines the given <code>redefin
        edFeature</code>.</p>
        [Feature operation; params: redefinedFeature: ?, arg: ?; returns: nothing; stub - metamodel me
        tadata only]
        """
        raise NotImplementedError
    def redefinesFromLibrary(self, libraryFeatureName: None = None, arg: None = None) -> None:
        """
        <p>Check whether this <code>Feature</code> <em>directly</em> redefines the named library <code
        >Feature</code>. <code>libraryFeatureName</code> must conform to the syntax of a KerML qualifi
        ed name and must resolve to a <code>Feature</code> in global scope.</p>
        [Feature operation; params: libraryFeatureName: ?, arg: ?; returns: nothing; stub - metamodel 
        metadata only]
        """
        raise NotImplementedError
    def subsetsChain(self, first: None = None, second: None = None, arg: None = None) -> None:
        """
        <p>Check whether this <code>Feature</code> directly or indirectly specializes a <code>Feature<
        /code> whose last two <code>chainingFeatures</code> are the given <code>Features</code> <code>
        first</code> and <code>second</code>.</p>
        [Feature operation; params: first: ?, second: ?, arg: ?; returns: nothing; stub - metamodel me
        tadata only]
        """
        raise NotImplementedError
    def isCompatibleWith(self, otherType: None = None) -> None:
        """
        <p>A <code>Feature</code> is compatible with an <code>otherType</code> if it either directly o
        r indirectly specializes the <code>otherType</code> or if the <code>otherType</code> is also a
         <code>Feature</code> and all of the following are true.</p> <ol> <li>Neither this <code>Featu
        re</code> or the <code>otherType</code> have any <code>ownedFeatures</code>.</li> <li>This <co
        de>Feature</code> directly or indirectly redefines a <code>Feature</code> that is also directl
        y or indirectly redefined by the <code>otherType</code>.</li> <li>This <code>Feature</code> ca
        n access the <code>otherType</code>. </li></ol>
        [Feature operation; params: otherType: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def typingFeatures(self, arg: None = None) -> None:
        """
        <p>Return the <code>Features</code> used to determine the <code>types</code> of this <code>Fea
        ture</code> (other than this <code>Feature</code> itself). If this <code>Feature</code> is <em
        >not</em> conjugated, then the <code>typingFeatures</code> consist of all subsetted <code>Feat
        ures</code>, <em>except</em> from <code>CrossSubsetting</code>, and the last <code>chainingFea
        ture</code> (if any). If this <code>Feature</code> <em>is</em> conjugated, then the <code>typi
        ngFeatures</code> are only its <code>originalType</code> (if the <code>originalType</code> is 
        a <code>Feature</code>).</p> <p><strong>Note.</strong> <code>CrossSubsetting</code> is exclude
        d from the determination of the <code>type</code> of a <code>Feature</code> in order to avoid 
        circularity in the construction of implied <code>CrossSubsetting</code> relationships. The <co
        de>validateFeatureCrossFeatureType</code> requires that the <code>crossFeature</code> of a <co
        de>Feature</code> have the same <code>type</code> as the <code>Feature</code>.</p>
        [Feature operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def asCartesianProduct(self, arg: None = None) -> None:
        """
        <p>If <code>isCartesianProduct</code> is true, then return the list of <code>Types</code> whos
        e Cartesian product can be represented by this <code>Feature</code>. (If <code>isCartesianProd
        uct</code> is not true, the operation will still return a valid value, it will just not repres
        ent anything useful.)</p>
        [Feature operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isCartesianProduct(self, arg: None = None) -> None:
        """
        <p>Check whether this <code>Feature</code> can be used to represent a Cartesian product of <co
        de>Types</code>.</p>
        [Feature operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isOwnedCrossFeature(self, arg: None = None) -> None:
        """
        <p>Return whether this <code>Feature</code> is an owned cross <code>Feature</code> of an end <
        code>Feature</code>.</p>
        [Feature operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def ownedCrossFeature(self, arg: None = None) -> None:
        """
        <p>If this <code>Feature</code> is an end <code>Feature</code> of its <code>owningType</code>,
         then return the first <code>ownedMember</code> of the <code>Feature</code> that is a <code>Fe
        ature</code>, but not a <code>Multiplicity</code> or a <code>MetadataFeature</code>, and whose
         <code>owningMembership</code> is <em>not</em> a <code>FeatureMembership</code>. If this exist
        s, it is the <code>crossFeature</code> of the end <code>Feature</code>.</p>
        [Feature operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def allRedefinedFeatures(self, arg: None = None) -> None:
        """
        <p>Return this <code>Feature</code> and all the <code>Features</code> that are directly or ind
        irectly <code>Redefined</code> by this <code>Feature</code>.</p>
        [Feature operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isFeaturedWithin(self, type: None = None, arg: None = None) -> None:
        """
        <p>Return if the <code>featuringTypes</code> of this <code>Feature</code> are compatible with 
        the given <code>type</code>. If <code>type</code> is null, then check if this <code>Feature</c
        ode> is explicitly or implicitly featured by <em><code>Base::Anything</code></em>. If this <co
        de>Feature</code> has <code>isVariable = true</code>, then also consider it to be featured wit
        hin its <code>owningType</code>. If this <code>Feature</code> is a feature chain whose first <
        code>chainingFeature</code> has <code>isVariable = true</code>, then also consider it to be fe
        atured within the <code>owningType</code> of its first <code>chainingFeature</code>.</p>
        [Feature operation; params: type: ?, arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def canAccess(self, feature: None = None, arg: None = None) -> None:
        """
        <p>A <code>Feature</code> can access another <code>feature</code> if the other <code>feature</
        code> is featured within one of the direct or indirect <code>featuringTypes</code> of this <co
        de>Feature</code>.</p>
        [Feature operation; params: feature: ?, arg: ?; returns: nothing; stub - metamodel metadata on
        ly]
        """
        raise NotImplementedError
    def isFeaturingType(self, type: None = None, arg: None = None) -> None:
        """
        <p>Return whether the given <code>type</code> must be a <code>featuringType</code> of this <co
        de>Feature</code>. If this <code>Feature</code> has <code>isVariable = false</code>, then retu
        rn true if the <code>type</code> is the <code>owningType</code> of the <code>Feature</code>. I
        f <code>isVariable = true</code>, then return true if the <code>type</code> is a <code>Feature
        </code> representing the <em><code>snapshots</code></em> of the <code>owningType</code> of thi
        s <code>Feature</code>.</p>
        [Feature operation; params: type: ?, arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError

class Step(Feature):
    """<p>A <code>Step</code> is a <code>Feature</code> that is typed by one or more <code>Behaviors</code>. <code>Steps</code> may be used by one <code>Behavior</code> to coordinate the performance of other <code>Behaviors</code>, supporting a steady refinement of behavioral descriptions. <code>Steps</code> can be ordered in time and can be connected using <code>Flows</code> to specify things flowing between their <code>parameters</code>.</p>"""
    _PKG = "Behaviors"
    _DECL = {
    # <p>The <code>Behaviors</code> that type this <code>Step</code>.</p>
    'behavior': _Ref('behavior', "Behavior", derived=True, multi=True, lo=0, hi='*', subsets=("type",), assoc="Kernel-Behaviors-A_behavior_typedStep"),
    # <p>The <code>parameters</code> of this <code>Step</code>, which are defined as its <code>directe
    # dFeatures</code>, whose values are passed into and/or out of a performance of the <code>Step</co
    # de>.</p>
    'parameter': _Ref('parameter', "Feature", derived=True, multi=True, lo=0, hi='*', redefines=("directedFeature",), assoc="Kernel-Behaviors-A_parameter_parameteredStep"),
    }
    CONSTRAINTS = (
        ("deriveStepBehavior",
         "behavior = type->selectByKind(Behavior)"
        ),
        ("checkStepSubperformanceSpecialization",
         "owningType <> null and     (owningType.oclIsKindOf(Behavior) or      owningType.oclIsKin"
         "dOf(Step)) and     self.isComposite implies     specializesFromLibrary('Performances::Pe"
         "rformance::subperformance')"
        ),
        ("checkStepSpecialization",
         "specializesFromLibrary('Performances::performances')"
        ),
        ("checkStepEnclosedPerformanceSpecialization",
         "owningType <> null and     (owningType.oclIsKindOf(Behavior) or      owningType.oclIsKin"
         "dOf(Step)) implies     specializesFromLibrary('Performances::Performance::enclosedPerfor"
         "mance')"
        ),
        ("checkStepOwnedPerformanceSpecialization",
         "isComposite and owningType <> null and (owningType.oclIsKindOf(Structure) or  owningType"
         ".oclIsKindOf(Feature) and  owningType.oclAsType(Feature).type->     exists(oclIsKindOf(S"
         "tructure)) implies     specializesFromLibrary('Objects::Object::ownedPerformance')"
        ),
    )

class Usage(Feature):
    """<p>A <code>Usage</code> is a usage of a <code>Definition</code>.</p> <p>A <code>Usage</code> may have <code>nestedUsages</code> that model <code>features</code> that apply in the context of the <code>owningUsage</code>. A <code>Usage</code> may also have <code>Definitions</code> nested in it, but this has no semantic significance, other than the nested scoping resulting from the <code>Usage</code> being considered as a <code>Namespace</code> for any nested <code>Definitions</code>.</p> <p>However, if a <code>Usage</code> has <code>isVariation = true</code>, then it represents a <em>variation point</em> <code>Usage</code>. In this case, all of its <code>members</code> must be <code>variant</code> <code>Usages</code>, related to the <code>Usage</code> by <code>VariantMembership</code> <code>Relationships</code>. Rather than being <code>features</code> of the <code>Usage</code>, <code>varia...[truncated]"""
    _PKG = "DefinitionAndUsage"
    _DECL = {
    # <p>The <code>Classifiers</code> that are the types of this <code>Usage</code>. Nominally, these 
    # are <code>Definitions</code>, but other kinds of Kernel <code>Classifiers</code> are also allowe
    # d, to permit use of <code>Classifiers</code> from the Kernel Model Libraries.</p>
    'definition': _Ref('definition', "Classifier", derived=True, multi=True, lo=0, hi='*', assoc="Systems-DefinitionAndUsage-A_definition_definedUsage"),
    # <p>The <code>usages</code> of this <code>Usage</code> that are <code>directedFeatures</code>.</p
    # >
    'directedUsage': _Ref('directedUsage', "Usage", derived=True, multi=True, lo=0, hi='*', subsets=("usage",), assoc="Systems-DefinitionAndUsage-A_directedUsage_usageWithDirectedUsage"),
    # <p>Whether this <code>Usage</code> is a referential <code>Usage</code>, that is, it has <code>is
    # Composite = false</code>.<p>
    'isReference': _Ref('isReference', bool, derived=True),
    # <p>Whether this <code>Usage</code> is for a variation point or not. If true, then all the <code>
    # memberships</code> of the <code>Usage</code> must be <code>VariantMemberships</code>.</p>
    'isVariation': _Ref('isVariation', bool),
    # <p>Whether this <code>Usage</code> may be time varying (that is, whether it is featured by the s
    # napshots of its <code>owningType</code>, rather than being featured by the <code>owningType</cod
    # e> itself). However, if <code>isConstant</code> is also true, then the value of the <code>Usage<
    # /code> is nevertheless constant over the entire duration of an instance of its <code>owningType<
    # /code> (that is, it has the same value on all snapshots).</p> <p>The property <code>mayTimeVary<
    # /code> redefines the KerML property <code>Feature::isVariable</code>, making it derived. The pro
    # perty <code>isConstant</code> is inherited from <code>Feature</code>.</p>
    'mayTimeVary': _Ref('mayTimeVary', bool, derived=True),
    # <p>The <code>ActionUsages</code> that are <code>nestedUsages</code> of this <code>Usage</code>.<
    # /p>
    'nestedAction': _Ref('nestedAction', "ActionUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedOccurrence",), assoc="Systems-DefinitionAndUsage-A_nestedAction_actionOwningUsage"),
    # <p>The <code>AllocationUsages</code> that are <code>nestedUsages</code> of this <code>Usage</cod
    # e>.</p>
    'nestedAllocation': _Ref('nestedAllocation', "AllocationUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedConnection",), assoc="Systems-DefinitionAndUsage-A_nestedAllocation_allocationOwningUsage"),
    # <p>The <code>AnalysisCaseUsages</code> that are <code>nestedUsages</code> of this <code>Usage</c
    # ode>.</p>
    'nestedAnalysisCase': _Ref('nestedAnalysisCase', "AnalysisCaseUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedCase",), assoc="Systems-DefinitionAndUsage-A_analysisCaseOwningUsage_nestedAnalysisCase"),
    # <p>The code>AttributeUsages</code> that are <code>nestedUsages</code> of this <code>Usage</code>
    # .</p>
    'nestedAttribute': _Ref('nestedAttribute', "AttributeUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedUsage",), assoc="Systems-DefinitionAndUsage-A_nestedAttribute_attributeOwningUsage"),
    # <p>The <code>CalculationUsage</code> that are <code>nestedUsages</code> of this <code>Usage</cod
    # e>.</p>
    'nestedCalculation': _Ref('nestedCalculation', "CalculationUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedAction",), assoc="Systems-Calculations-A_calculationOwningUsage_nestedCalculation"),
    # <p>The <code>CaseUsages</code> that are <code>nestedUsages</code> of this <code>Usage</code>.</p
    # >
    'nestedCase': _Ref('nestedCase', "CaseUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedCalculation",), assoc="Systems-Cases-A_caseOwningUsage_nestedCase"),
    # <p>The <code>ConcernUsages</code> that are <code>nestedUsages</code> of this <code>Usage</code>.
    # </p>
    'nestedConcern': _Ref('nestedConcern', "ConcernUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedRequirement",), assoc="Systems-DefinitionAndUsage-A_nestedConcern_concernOwningUsage"),
    # <p>The <code>ConnectorAsUsages</code> that are <code>nestedUsages</code> of this <code>Usage</co
    # de>. Note that this list includes <code>BindingConnectorAsUsages</code>, <code>SuccessionAsUsage
    # s</code>, and <code>FlowConnectionUsages</code> because these are <code>ConnectorAsUsages</code>
    #  even though they are not <code>ConnectionUsages</code>.</p>
    'nestedConnection': _Ref('nestedConnection', "ConnectorAsUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedUsage",), assoc="Systems-DefinitionAndUsage-A_nestedConnection_connectionOwningUsage"),
    # <p>The <code>ConstraintUsages</code> that are <code>nestedUsages</code> of this <code>Usage</cod
    # e>.</p>
    'nestedConstraint': _Ref('nestedConstraint', "ConstraintUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedOccurrence",), assoc="Systems-DefinitionAndUsage-A_nestedConstraint_constraintOwningUsage"),
    # <p>The code>EnumerationUsages</code> that are <code>nestedUsages</code> of this <code>Usage</cod
    # e>.<p>
    'nestedEnumeration': _Ref('nestedEnumeration', "EnumerationUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedAttribute",), assoc="Systems-DefinitionAndUsage-A_nestedEnumeration_enumerationOwningUsage"),
    # <p>The code>FlowUsages</code> that are <code>nestedUsages</code> of this <code>Usage</code>.</p>
    'nestedFlow': _Ref('nestedFlow', "FlowUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedConnection",), assoc="Systems-DefinitionAndUsage-A_nestedFlow_flowOwningUsage"),
    # <p>The <code>InterfaceUsages</code> that are <code>nestedUsages</code> of this <code>Usage</code
    # >.</p>
    'nestedInterface': _Ref('nestedInterface', "InterfaceUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedConnection",), assoc="Systems-DefinitionAndUsage-A_nestedInterface_interfaceOwningUsage"),
    # <p>The <code>ItemUsages</code> that are <code>nestedUsages</code> of this <code>Usage</code>.</p
    # >
    'nestedItem': _Ref('nestedItem', "ItemUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedOccurrence",), assoc="Systems-DefinitionAndUsage-A_nestedItem_itemOwningUsage"),
    # <p>The <code>MetadataUsages</code> that are <code>nestedUsages</code> of this of this <code>Usag
    # e</code>.</p>
    'nestedMetadata': _Ref('nestedMetadata', "MetadataUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedItem",), assoc="Systems-DefinitionAndUsage-A_nestedMetadata_metadataOwningUsage"),
    # <p>The <code>OccurrenceUsages</code> that are <code>nestedUsages</code> of this <code>Usage</cod
    # e>.</p>
    'nestedOccurrence': _Ref('nestedOccurrence', "OccurrenceUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedUsage",), assoc="Systems-DefinitionAndUsage-A_nestedOccurrence_occurrenceOwningUsage"),
    # <p>The <code>PartUsages</code> that are <code>nestedUsages</code> of this <code>Usage</code>.</p
    # >
    'nestedPart': _Ref('nestedPart', "PartUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedItem",), assoc="Systems-DefinitionAndUsage-A_nestedPart_partOwningUsage"),
    # <p>The <code>PortUsages</code> that are <code>nestedUsages</code> of this <code>Usage</code>.</p
    # >
    'nestedPort': _Ref('nestedPort', "PortUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedUsage",), assoc="Systems-DefinitionAndUsage-A_nestedPort_portOwningUsage"),
    # <p>The <code>ReferenceUsages</code> that are <code>nestedUsages</code> of this <code>Usage</code
    # >.</p>
    'nestedReference': _Ref('nestedReference', "ReferenceUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedUsage",), assoc="Systems-DefinitionAndUsage-A_nestedReference_referenceOwningUsage"),
    # <p>The <code>RenderingUsages</code> that are <code>nestedUsages</code> of this <code>Usage</code
    # >.</p>
    'nestedRendering': _Ref('nestedRendering', "RenderingUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedPart",), assoc="Systems-DefinitionAndUsage-A_nestedRendering_renderingOwningUsage"),
    # <p>The <code>RequirementUsages</code> that are <code>nestedUsages</code> of this <code>Usage</co
    # de>.</p>
    'nestedRequirement': _Ref('nestedRequirement', "RequirementUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedConstraint",), assoc="Systems-DefinitionAndUsage-A_nestedRequirement_requirementOwningUsage"),
    # <p>The <code>StateUsages</code> that are <code>nestedUsages</code> of this <code>Usage</code>.</
    # p>
    'nestedState': _Ref('nestedState', "StateUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedAction",), assoc="Systems-DefinitionAndUsage-A_nestedState_stateOwningUsage"),
    # <p>The <code>TransitionUsages</code> that are <code>nestedUsages</code> of this <code>Usage</cod
    # e>.</p>
    'nestedTransition': _Ref('nestedTransition', "TransitionUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedUsage",), assoc="Systems-DefinitionAndUsage-A_nestedTransition_transitionOwningUsage"),
    # <p>The <code>Usages</code> that are <code>ownedFeatures</code> of this <code>Usage</code>.</p>
    'nestedUsage': _Ref('nestedUsage', "Usage", derived=True, multi=True, lo=0, hi='*', subsets=("usage",), assoc="Systems-DefinitionAndUsage-A_nestedUsage_owningUsage"),
    # <p>The <code>UseCaseUsages</code> that are <code>nestedUsages</code> of this <code>Usage</code>.
    # </p>
    'nestedUseCase': _Ref('nestedUseCase', "UseCaseUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedCase",), assoc="Systems-DefinitionAndUsage-A_nestedUseCase_useCaseOwningUsage"),
    # <p>The <code>VerificationCaseUsages</code> that are <code>nestedUsages</code> of this <code>Usag
    # e</code>.</p>
    'nestedVerificationCase': _Ref('nestedVerificationCase', "VerificationCaseUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedCase",), assoc="Systems-DefinitionAndUsage-A_nestedVerificationCase_verificationCaseOwningUsage"),
    # <p>The <code>ViewUsages</code> that are <code>nestedUsages</code> of this <code>Usage</code>.</p
    # >
    'nestedView': _Ref('nestedView', "ViewUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedPart",), assoc="Systems-DefinitionAndUsage-A_nestedView_viewOwningUsage"),
    # <p>The <code>ViewpointUsages</code> that are <code>nestedUsages</code> of this <code>Usage</code
    # >.</p>
    'nestedViewpoint': _Ref('nestedViewpoint', "ViewpointUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedRequirement",), assoc="Systems-DefinitionAndUsage-A_nestedViewpoint_viewpointOwningUsage"),
    # <p>The <code>Definition</code> that owns this <code>Usage</code> (if any).</p>
    'owningDefinition': _Ref('owningDefinition', "Definition", derived=True, assoc="Systems-DefinitionAndUsage-A_ownedUsage_owningDefinition"),
    # <p>The <code>Usage</code> in which this <code>Usage</code> is nested (if any).</p>
    'owningUsage': _Ref('owningUsage', "Usage", derived=True, assoc="Systems-DefinitionAndUsage-A_nestedUsage_owningUsage"),
    # <p>The <code>Usages</code> that are <code>features</code> of this <code>Usage</code> (not necess
    # arily owned).</p>
    'usage': _Ref('usage', "Usage", derived=True, multi=True, lo=0, hi='*', assoc="Systems-DefinitionAndUsage-A_featuringUsage_usage"),
    # <p>The <code>Usages</code> which represent the variants of this <code>Usage</code> as a variatio
    # n point <code>Usage</code>, if <code>isVariation = true</code>. If <code>isVariation = false</co
    # de>, then there must be no <code>variants</code>.</p>
    'variant': _Ref('variant', "Usage", derived=True, multi=True, lo=0, hi='*', assoc="Systems-DefinitionAndUsage-A_variant_owningVariationUsage"),
    # <p>The <code>ownedMemberships</code> of this <code>Usage</code> that are <code>VariantMembership
    # s</code>. If <code>isVariation = true</code>, then this must be all <code>memberships</code> of 
    # the <code>Usage</code>. If <code>isVariation = false</code>, then <code>variantMembership</code>
    # must be empty.</p>
    'variantMembership': _Ref('variantMembership', "VariantMembership", derived=True, multi=True, lo=0, hi='*', assoc="Systems-DefinitionAndUsage-A_variantMembership_owningVariationUsage"),
    }
    CONSTRAINTS = (
        ("deriveUsageNestedView",
         "nestedView = nestedUsage->selectByKind(ViewUsage)"
        ),
        ("validateUsageVariationIsAbstract",
         "isVariation implies isAbstract"
        ),
        ("deriveUsageUsage",
         "usage = feature->selectByKind(Usage)"
        ),
        ("deriveUsageNestedEnumeration",
         "ownedNested = nestedUsage->selectByKind(EnumerationUsage)"
        ),
        ("deriveUsageNestedConstraint",
         "nestedConstraint = nestedUsage->selectByKind(ConstraintUsage)"
        ),
        ("deriveUsageNestedOccurrence",
         "nestedOccurrence = nestedUsage->selectByKind(OccurrenceUsage)"
        ),
        ("deriveUsageNestedViewpoint",
         "nestedViewpoint = nestedUsage->selectByKind(ViewpointUsage)"
        ),
        ("deriveUsageNestedAction",
         "nestedAction = nestedUsage->selectByKind(ActionUsage)"
        ),
        ("deriveUsageNestedFlow",
         "nestedFlow = nestedUsage->selectByKind(FlowConnectionUsage)"
        ),
        ("checkUsageVariationUsageSpecialization",
         "owningVariationUsage <> null implies specializes(owningVariationUsage)"
        ),
        ("validateUsageVariationOwnedFeatureMembership",
         "isVariation implies ownedFeatureMembership->isEmpty()"
        ),
        ("deriveUsageNestedItem",
         "nestedItem = nestedUsage->selectByKind(ItemUsage)"
        ),
        ("validateUsageVariationSpecialization",
         "isVariation implies     not ownedSpecialization.specific->exists(         oclIsKindOf(De"
         "finition) and         oclAsType(Definition).isVariation or         oclIsKindOf(Usage) an"
         "d         oclAsType(Usage).isVariation)"
        ),
        ("deriveUsageNestedState",
         "nestedState = nestedUsage->selectByKind(StateUsage)"
        ),
        ("deriveUsageNestedConcern",
         "nestedConcern = nestedUsage->selectByKind(ConcernUsage)"
        ),
        ("deriveUsageNestedVerificationCase",
         "nestedVerificationCase = nestedUsage->selectByKind(VerificationCaseUsage)"
        ),
        ("deriveUsageNestedCalculation",
         "nestedCalculation = nestedUsage->selectByKind(CalculationUsage)"
        ),
        ("deriveUsageNestedAttribute",
         "nestedAttribute = nestedUsage->selectByKind(AttributeUsage)"
        ),
        ("deriveUsageDirectedUsage",
         "directedUsage = directedFeature->selectByKind(Usage)"
        ),
        ("deriveUsageNestedPart",
         "nestedPart = nestedUsage->selectByKind(PartUsage)"
        ),
        ("deriveUsageNestedMetadata",
         "nestedMetadata = nestedUsage->selectByKind(MetadataUsage)"
        ),
        ("deriveUsageNestedAllocation",
         "nestedAllocation = nestedUsage->selectByKind(AllocationUsage)"
        ),
        ("deriveUsageNestedUsage",
         "nestedUsage = ownedFeature->selectByKind(Usage)"
        ),
        ("deriveUsageNestedRendering",
         "nestedRendering = nestedUsage->selectByKind(RenderingUsage)"
        ),
        ("deriveUsageNestedConnection",
         "nestedConnection = nestedUsage->selectByKind(ConnectorAsUsage)"
        ),
        ("deriveUsageVariantMembership",
         "variantMembership = ownedMembership->selectByKind(VariantMembership)"
        ),
        ("deriveUsageNestedReference",
         "nestedReference = nestedUsage->selectByKind(ReferenceUsage)"
        ),
        ("deriveUsageNestedUseCase",
         "nestedUseCase = nestedUsage->selectByKind(UseCaseUsage)"
        ),
        ("deriveUsageMayTimeVary",
         "mayTimeVary =     owningType <> null and     owningType.specializesFromLibrary('Occurren"
         "ces::Occurrence') and     not (         isPortion or         specializesFromLibrary('Lin"
         "ks::SelfLink') or         specializesFromLibrary('Occurrences::HappensLink') or         "
         "isComposite and specializesFromLibrary('Actions::Action')     )"
        ),
        ("deriveUsageNestedRequirement",
         "nestedRequirement = nestedUsage->selectByKind(RequirementUsage)"
        ),
        ("deriveUsageNestedPort",
         "nestedPort = nestedUsage->selectByKind(PortUsage)"
        ),
        ("validateUsageIsReferential",
         "direction <> null or isEnd or featuringType->isEmpty() implies isReference"
        ),
        ("deriveUsageNestedTransition",
         "nestedTransition = nestedUsage->selectByKind(TransitionUsage)"
        ),
        ("deriveUsageNestedInterface",
         "nestedInterface = nestedUsage->selectByKind(ReferenceUsage)"
        ),
        ("deriveUsageNestedAnalysisCase",
         "nestedAnalysisCase = nestedUsage->selectByKind(AnalysisCaseUsage)"
        ),
        ("deriveUsageNestedCase",
         "nestedCase = nestedUsage->selectByKind(CaseUsage)"
        ),
        ("deriveUsageIsReference",
         "isReference = not isComposite"
        ),
        ("deriveUsageVariant",
         "variant = variantMembership.ownedVariantUsage"
        ),
        ("checkUsageVariationDefinitionSpecialization",
         "owningVariationDefinition <> null implies specializes(owningVariationDefinition)"
        ),
        ("checkUsageVariationUsageTypeFeaturing",
         "owningVariationUsage <> null implies featuringType->asSet() = owningVariationUsage.featu"
         "ringType->asSet()"
        ),
    )
    def namingFeature(self, arg: None = None) -> None:
        """
        <p>If this <code>Usage</code> is a variant, then its naming <code>Feature</code> is the <code>
        referencedFeature</code> of its <code>ownedReferenceSubsetting</code>.</p>
        [Usage operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def referencedFeatureTarget(self, arg: None = None) -> None:
        """
        <p>If <code>ownedReferenceSubsetting</code> is not null, return the <code>featureTarget</code>
         of the <code>referencedFeature</code> of the <code>ownedReferenceSubsetting</code>.</p>
        [Usage operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError

class OccurrenceUsage(Usage):
    """<p>An <code>OccurrenceUsage</code> is a <code>Usage</code> whose <code>types</code> are all <code>Classes</code>. Nominally, if a <code>type</code> is an <code>OccurrenceDefinition</code>, an <code>OccurrenceUsage</code> is a <code>Usage</code> of that <code>OccurrenceDefinition</code> within a system. However, other types of Kernel <code>Classes</code> are also allowed, to permit use of <code>Classes</code> from the Kernel Model Libraries.</p>"""
    _PKG = "Occurrences"
    _DECL = {
    # <p>The at most one <code>occurrenceDefinition</code> that has <code>isIndividual = true</code>.<
    # /p>
    'individualDefinition': _Ref('individualDefinition', "OccurrenceDefinition", derived=True, subsets=("occurrenceDefinition",), assoc="Systems-Occurrences-A_individualDefinition_individualUsage"),
    # <p>Whether this <code>OccurrenceUsage</code> represents the usage of the specific individual rep
    # resented by its <code>individualDefinition</code>.</p>
    'isIndividual': _Ref('isIndividual', bool),
    # <p>The <code>Classes</code> that are the types of this <code>OccurrenceUsage</code>. Nominally, 
    # these are <code>OccurrenceDefinitions</code>, but other kinds of kernel <code>Classes</code> are
    #  also allowed, to permit use of <code>Classes</code> from the Kernel Model Libraries.</p>
    'occurrenceDefinition': _Ref('occurrenceDefinition', "Class", derived=True, multi=True, lo=0, hi='*', redefines=("definition",), assoc="Systems-Occurrences-A_occurrenceDefinition_definedOccurrence"),
    # <p>The kind of temporal portion (time slice or snapshot) is represented by this <code>Occurrence
    # Usage</code>. If <code>portionKind</code> is not null, then the <code>owningType</code> of the <
    # code>OccurrenceUsage</code> must be non-null, and the <code>OccurrenceUsage</code> represents po
    # rtions of the featuring instance of the <code>owningType</code>.</p>
    'portionKind': _Ref('portionKind', None),
    }
    CONSTRAINTS = (
        ("validateOccurrenceUsageIndividualDefinition",
         "occurrenceDefinition-> selectByKind(OccurrenceDefinition)-> select(isIndividual).size() "
         "<= 1"
        ),
        ("checkOccurrenceUsageSnapshotSpecialization",
         "portionKind = PortionKind::snapshot implies specializesFromLibrary('Occurrences::Occurre"
         "nce::snapshots')"
        ),
        ("validateOccurrenceUsageIndividualUsage",
         "isIndividual implies individualDefinition <> null"
        ),
        ("checkOccurrenceUsageSpecialization",
         "specializesFromLibrary('Occurrences::occurrences')"
        ),
        ("deriveOccurrenceUsageIndividualDefinition",
         "individualDefinition =     let individualDefinitions : OrderedSet(OccurrenceDefinition) "
         "=          occurrenceDefinition->             selectByKind(OccurrenceDefinition)->      "
         "       select(isIndividual) in     if individualDefinitions->isEmpty() then null     els"
         "e individualDefinitions->first() endif"
        ),
        ("validateOccurrenceUsageIsPortion",
         "portionKind <> null implies isPortion"
        ),
        ("checkOccurrenceUsageSuboccurrenceSpecialization",
         "isComposite and owningType <> null and (owningType.oclIsKindOf(Class) or  owningType.ocl"
         "IsKindOf(OccurrenceUsage) or  owningType.oclIsKindOf(Feature) and     owningType.oclAsTy"
         "pe(Feature).type->         exists(oclIsKind(Class))) implies     specializesFromLibrary("
         "'Occurrences::Occurrence::suboccurrences')"
        ),
        ("checkOccurrenceUsageTimeSliceSpecialization",
         "portionKind = PortionKind::timeslice implies specializesFromLibrary('Occurrences::Occurr"
         "ence::timeSlices')"
        ),
        ("validateOccurrenceUsagePortionKind",
         "portionKind <> null implies     owningType <> null and     (owningType.oclIsKindOf(Occur"
         "renceDefinition) or      owningType.oclIsKindOf(OccurrenceUsage))"
        ),
    )

class ActionUsage(OccurrenceUsage, Step):
    """<p>An <code>ActionUsage</code> is a <code>Usage</code> that is also a <code>Step</code>, and, so, is typed by a <code>Behavior</code>. Nominally, if the type is an <code>ActionDefinition</code>, an <code>ActionUsage</code> is a <code>Usage</code> of that <code>ActionDefinition</code> within a system. However, other kinds of kernel <code>Behaviors</code> are also allowed, to permit use of <code>Behaviors</code> from the Kernel Model Libraries.</p>"""
    _PKG = "Actions"
    _DECL = {
    # <p>The <code>Behaviors</code> that are the <code>types</code> of this <code>ActionUsage</code>. 
    # Nominally, these would be <code>ActionDefinitions</code>, but other kinds of Kernel <code>Behavi
    # ors</code> are also allowed, to permit use of <code>Behaviors</code> from the Kernel Model Libra
    # ries.</p>
    'actionDefinition': _Ref('actionDefinition', "Behavior", derived=True, multi=True, lo=0, hi='*', redefines=("occurrenceDefinition",), assoc="Systems-Actions-A_actionDefinition_definedAction"),
    }
    CONSTRAINTS = (
        ("checkActionUsageStateActionRedefinition",
         "owningFeatureMembership <> null and owningFeatureMembership.oclIsKindOf(StateSubactionMe"
         "mbership) implies     let kind : StateSubactionKind =          owningFeatureMembership.o"
         "clAsType(StateSubactionMembership).kind in     if kind = StateSubactionKind::entry then "
         "        redefinesFromLibrary('States::StateAction::entryAction')     else if kind = Stat"
         "eSubactionKind::do then         redefinesFromLibrary('States::StateAction::doAction')   "
         "  else         redefinesFromLibrary('States::StateAction::exitAction')     endif endif"
        ),
        ("checkActionUsageSpecialization",
         "specializesFromLibrary('Actions::actions')"
        ),
        ("checkActionUsageSubactionSpecialization",
         "isSubactionUsage() implies specializesFromLibrary('Actions::Action::subactions')"
        ),
        ("checkActionUsageOwnedActionSpecialization",
         "isComposite and owningType <> null and (owningType.oclIsKindOf(PartDefinition) or  ownin"
         "gType.oclIsKindOf(PartUsage)) implies     specializesFromLibrary('Parts::Part::ownedActi"
         "ons')"
        ),
    )
    def inputParameters(self, arg: None = None) -> None:
        """
        <p>Return the owned input <code>parameters</code> of this <code>ActionUsage</code>.</p>
        [ActionUsage operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def inputParameter(self, i: None = None, arg: None = None) -> None:
        """
        <p>Return the <code>i</code>-th owned input <code>parameter</code> of the <code>ActionUsage</c
        ode>. Return null if the <code>ActionUsage</code> has less than <code>i</code> owned input <co
        de>parameters</code>.</p>
        [ActionUsage operation; params: i: ?, arg: ?; returns: nothing; stub - metamodel metadata only
        ]
        """
        raise NotImplementedError
    def argument(self, i: None = None, arg: None = None) -> None:
        """
        <p>Return the <code>i</code>-th argument <code>Expression</code> of an <code>ActionUsage</code
        >, defined as the <code>value</code> <code>Expression</code> of the <code>FeatureValue</code> 
        of the <code>i</code>-th owned input <code>parameter</code> of the <code>ActionUsage</code>. R
        eturn null if the <code>ActionUsage</code> has less than <code>i</code> owned input <code>para
        meters</code> or the <code>i</code>-th owned input <code>parameter</code> has no <code>Feature
        Value</code>.</p>
        [ActionUsage operation; params: i: ?, arg: ?; returns: nothing; stub - metamodel metadata only
        ]
        """
        raise NotImplementedError
    def isSubactionUsage(self, arg: None = None) -> None:
        """
        <p>Check if this <code>ActionUsage</code> is composite and has an <code>owningType</code> that
         is an <code>ActionDefinition</code> or <code>ActionUsage</code> but is <em>not</em> the <code
        >entryAction</code> or <code>exitAction</em></code> of a <code>StateDefinition</code> or <code
        >StateUsage</code>. If so, then it represents an <code><em>Action</em></code> that is a <code>
        <em>subaction</em></code> of another <code><em>Action</em></code>.</p>
        [ActionUsage operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError

class AcceptActionUsage(ActionUsage):
    """<p>An <code>AcceptActionUsage</code> is an <code>ActionUsage</code> that specifies the acceptance of an <em><code>incomingTransfer</code></em> from the <code><em>Occurrence</em></code> given by the result of its <code>receiverArgument</code> Expression. (If no <code>receiverArgument</code> is provided, the default is the <em><code>this</code></em> context of the AcceptActionUsage.) The payload of the accepted <em><code>Transfer</em></code> is output on its <code>payloadParameter</code>. Which <em><code>Transfers</em></code> may be accepted is determined by conformance to the typing and (potentially) binding of the <code>payloadParameter</code>.</p>"""
    _PKG = "Actions"
    _DECL = {
    # <p>An <code>Expression</code> whose <code>result</code> is bound to the <code><em>payload</em></
    # code> <code>parameter</code> of this <code>AcceptActionUsage</code>. If provided, the <code>Acce
    # ptActionUsage</code> will only accept a <code><em>Transfer</em></code> with exactly this <code><
    # em>payload</em></code>.</p>
    'payloadArgument': _Ref('payloadArgument', "Expression", derived=True, assoc="Systems-Actions-A_payloadArgument_acceptingActionUsage"),
    # <p>The <code>nestedReference</code> of this <code>AcceptActionUsage</code> that redefines the <c
    # ode>payload</code> output <code>parameter</code> of the base <code>AcceptActionUsage</code> <em>
    # <code>AcceptAction</code></em> from the Systems Model Library.</p>
    'payloadParameter': _Ref('payloadParameter', "ReferenceUsage", derived=True, subsets=("nestedReference",), assoc="Systems-Actions-A_payloadParameter_owningAcceptActionUsage"),
    # <p>An <code>Expression</code> whose <code>result</code> is bound to the <em><code>receiver</code
    # ></em> input <code>parameter</code> of this <code>AcceptActionUsage</code>.</p>
    'receiverArgument': _Ref('receiverArgument', "Expression", derived=True, assoc="Systems-Actions-A_receiverArgument_acceptActionUsage"),
    }
    CONSTRAINTS = (
        ("deriveAcceptActionUsagePayloadArgument",
         "payloadArgument = argument(1)"
        ),
        ("checkAcceptActionUsageReceiverBindingConnector",
         "payloadArgument <> null and payloadArgument.oclIsKindOf(TriggerInvocationExpression) imp"
         "lies     let invocation : Expression =         payloadArgument.oclAsType(Expression) in "
         "    parameter->size() >= 2 and     invocation.parameter->size() >= 2 and             own"
         "edFeature->selectByKind(BindingConnector)->exists(b |         b.relatedFeatures->include"
         "s(parameter->at(2)) and         b.relatedFeatures->includes(invocation.parameter->at(2))"
         ")"
        ),
        ("deriveAcceptActionUsagePayloadParameter",
         "payloadParameter = if parameter->isEmpty() then null else parameter->first() endif"
        ),
        ("checkAcceptActionUsageTriggerActionSpecialization",
         "isTriggerAction() implies specializesFromLibrary('Actions::TransitionAction::accepter')"
        ),
        ("validateAcceptActionUsageParameters",
         "inputParameters()->size() >= 2"
        ),
        ("deriveAcceptActionUsageReceiverArgument",
         "receiverArgument = argument(2)"
        ),
        ("checkAcceptActionUsageSubactionSpecialization",
         "isSubactionUsage() and not isTriggerAction() implies specializesFromLibrary('Actions::Ac"
         "tion::acceptSubactions')"
        ),
        ("checkAcceptActionUsageSpecialization",
         "not isTriggerAction() implies specializesFromLibrary('Actions::acceptActions')"
        ),
    )
    def isTriggerAction(self, arg: None = None) -> None:
        """
        <p>Check if this <code>AcceptActionUsage</code> is the <code>triggerAction</code> of a <code>T
        ransitionUsage</code>.</p>
        [AcceptActionUsage operation; params: arg: ?; returns: nothing; stub - metamodel metadata only
        ]
        """
        raise NotImplementedError

class Classifier(Type):
    """<p>A <code>Classifier</code> is a <code>Type</code> that classifies:</p> <ul> <li>Things (in the universe) regardless of how <code>Features</code> relate them. (These are interpreted semantically as sequences of exactly one thing.)</li> <li>How the above things are related by <code>Features.</code> (These are interpreted semantically as sequences of multiple things, such that the last thing in the sequence is also classified by the <code>Classifier</code>. Note that this means that a <code>Classifier</code> modeled as specializing a <code>Feature</code> cannot classify anything.)</li> </ul>"""
    _PKG = "Classifiers"
    _DECL = {
    # <p>The <code>ownedSpecializations</code> of this <code>Classifier</code> that are <code>Subclass
    # ifications</code>, for which this <code>Classifier</code> is the <code>subclassifier</code>.</p>
    'ownedSubclassification': _Ref('ownedSubclassification', "Subclassification", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedSpecialization",), assoc="Core-Classifiers-A_owningClassifier_ownedSubclassification"),
    }
    CONSTRAINTS = (
        ("deriveClassifierOwnedSubclassification",
         "ownedSubclassification = ownedSpecialization->selectByKind(Subclassification)"
        ),
        ("validateClassifierMultiplicityDomain",
         "multiplicity <> null implies multiplicity.featuringType->isEmpty()"
        ),
    )

class Definition(Classifier):
    """<p>A <code>Definition</code> is a <code>Classifier</code> of <code>Usages</code>. The actual kinds of <code>Definition</code> that may appear in a model are given by the subclasses of <code>Definition</code> (possibly as extended with user-defined <em><code>SemanticMetadata</code></em>).</p> <p>Normally, a <code>Definition</code> has owned Usages that model <code>features</code> of the thing being defined. A <code>Definition</code> may also have other <code>Definitions</code> nested in it, but this has no semantic significance, other than the nested scoping resulting from the <code>Definition</code> being considered as a <code>Namespace</code> for any nested <code>Definitions</code>.</p> <p>However, if a <code>Definition</code> has <code>isVariation</code> = <code>true</code>, then it represents a <em>variation point</em> <code>Definition</code>. In this case, all of its <code>members</c...[truncated]"""
    _PKG = "DefinitionAndUsage"
    _DECL = {
    # <p>The <code>usages</code> of this <code>Definition</code> that are <code>directedFeatures</code
    # >.</p>
    'directedUsage': _Ref('directedUsage', "Usage", derived=True, multi=True, lo=0, hi='*', subsets=("usage",), assoc="Systems-DefinitionAndUsage-A_directedUsage_definitionWithDirectedUsage"),
    # <p>Whether this <code>Definition</code> is for a variation point or not. If true, then all the <
    # code>memberships</code> of the <code>Definition</code> must be <code>VariantMemberships</code>.<
    # /p>
    'isVariation': _Ref('isVariation', bool),
    # <p>The <code>ActionUsages</code> that are <code>ownedUsages</code> of this <code>Definition</cod
    # e>.</p>
    'ownedAction': _Ref('ownedAction', "ActionUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedOccurrence",), assoc="Systems-DefinitionAndUsage-A_ownedAction_actionOwningDefinition"),
    # <p>The <code>AllocationUsages</code> that are <code>ownedUsages</code> of this <code>Definition<
    # /code>.</p>
    'ownedAllocation': _Ref('ownedAllocation', "AllocationUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedConnection",), assoc="Systems-DefinitionAndUsage-A_ownedAllocation_allocationOwningDefinition"),
    # <p>The <code>AnalysisCaseUsages</code> that are <code>ownedUsages</code> of this <code>Definitio
    # n</code>.</p>
    'ownedAnalysisCase': _Ref('ownedAnalysisCase', "AnalysisCaseUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedCase",), assoc="Systems-DefinitionAndUsage-A_analysisCaseOwningDefinition_ownedAnalysisCase"),
    # <p>The <code>AttributeUsages</code> that are <code>ownedUsages</code> of this <code>Definition</
    # code>.<p>
    'ownedAttribute': _Ref('ownedAttribute', "AttributeUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedUsage",), assoc="Systems-DefinitionAndUsage-A_ownedAttribute_attributeOwningDefinition"),
    # <p>The <code>CalculationUsages</code> that are <code>ownedUsages</code> of this <code>Definition
    # </code>.</p>
    'ownedCalculation': _Ref('ownedCalculation', "CalculationUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedAction",), assoc="Systems-Calculations-A_calculationOwningDefinition_ownedCalculation"),
    # <p>The code>CaseUsages</code> that are <code>ownedUsages</code> of this <code>Definition</code>.
    # </p>
    'ownedCase': _Ref('ownedCase', "CaseUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedCalculation",), assoc="Systems-DefinitionAndUsage-A_caseOwningDefinition_ownedCase"),
    # <p>The <code>ConcernUsages</code> that are <code>ownedUsages</code> of this <code>Definition</co
    # de>.</p>
    'ownedConcern': _Ref('ownedConcern', "ConcernUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedRequirement",), assoc="Systems-DefinitionAndUsage-A_ownedConcern_concernOwningDefinition"),
    # <p>The <code>ConnectorAsUsages</code> that are <code>ownedUsages</code> of this <code>Definition
    # </code>. Note that this list includes <code>BindingConnectorAsUsages</code>, <code>SuccessionAsU
    # sages</code>, and <code>FlowUsages</code> because these are <code>ConnectorAsUsages</code> even 
    # though they are not <code>ConnectionUsages</code>.</p>
    'ownedConnection': _Ref('ownedConnection', "ConnectorAsUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedUsage",), assoc="Systems-DefinitionAndUsage-A_ownedConnection_connectionOwningDefinition"),
    # <p>The <code>ConstraintUsages</code> that are <code>ownedUsages</code> of this <code>Definition<
    # /code>.</p>
    'ownedConstraint': _Ref('ownedConstraint', "ConstraintUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedOccurrence",), assoc="Systems-DefinitionAndUsage-A_ownedConstraint_constraintOwningDefinition"),
    # <p>The <code>EnumerationUsages</code> that are <code>ownedUsages</code> of this <code>Definition
    # </code>.<p>
    'ownedEnumeration': _Ref('ownedEnumeration', "EnumerationUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedAttribute",), assoc="Systems-DefinitionAndUsage-A_ownedEnumeration_enumerationOwningDefinition"),
    # <p>The <code>FlowUsages</code> that are <code>ownedUsages</code> of this <code>Definition</code>
    # .</p>
    'ownedFlow': _Ref('ownedFlow', "FlowUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedConnection",), assoc="Systems-DefinitionAndUsage-A_ownedFlow_flowOwningDefinition"),
    # <p>The <code>InterfaceUsages</code> that are <code>ownedUsages</code> of this <code>Definition</
    # code>.</p>
    'ownedInterface': _Ref('ownedInterface', "InterfaceUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedConnection",), assoc="Systems-DefinitionAndUsage-A_ownedInterface_interfaceOwningDefinition"),
    # <p>The <code>ItemUsages</code> that are <code>ownedUsages</code> of this <code>Definition</code>
    # .</p>
    'ownedItem': _Ref('ownedItem', "ItemUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedOccurrence",), assoc="Systems-DefinitionAndUsage-A_ownedItem_itemOwningDefinition"),
    # <p>The <code>MetadataUsages</code> that are <code>ownedUsages</code> of this <code>Definition</c
    # ode>.</p>
    'ownedMetadata': _Ref('ownedMetadata', "MetadataUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedItem",), assoc="Systems-DefinitionAndUsage-A_ownedMetadata_metadataOwningDefinition"),
    # <p>The <code>OccurrenceUsages</code> that are <code>ownedUsages</code> of this <code>Definition<
    # /code>.</p>
    'ownedOccurrence': _Ref('ownedOccurrence', "OccurrenceUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedUsage",), assoc="Systems-DefinitionAndUsage-A_ownedOccurrence_occurrenceOwningDefinition"),
    # <p>The <code>PartUsages</code> that are <code>ownedUsages</code> of this <code>Definition</code>
    # .</p>
    'ownedPart': _Ref('ownedPart', "PartUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedItem",), assoc="Systems-DefinitionAndUsage-A_ownedPart_partOwningDefinition"),
    # <p>The <code>PortUsages</code> that are <code>ownedUsages</code> of this <code>Definition</code>
    # .</p>
    'ownedPort': _Ref('ownedPort', "PortUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedUsage",), assoc="Systems-DefinitionAndUsage-A_ownedPort_portOwningDefinition"),
    # <p>The <code>ReferenceUsages</code> that are <code>ownedUsages</code> of this <code>Definition</
    # code>.</p>
    'ownedReference': _Ref('ownedReference', "ReferenceUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedUsage",), assoc="Systems-DefinitionAndUsage-A_ownedReference_referenceOwningDefinition"),
    # <p>The <code>RenderingUsages</code> that are <code>ownedUsages</code> of this <code>Definition</
    # code>.</p>
    'ownedRendering': _Ref('ownedRendering', "RenderingUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedPart",), assoc="Systems-DefinitionAndUsage-A_ownedRendering_redenderingOwningDefinition"),
    # <p>The <code>RequirementUsages</code> that are <code>ownedUsages</code> of this <code>Definition
    # </code>.</p>
    'ownedRequirement': _Ref('ownedRequirement', "RequirementUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedConstraint",), assoc="Systems-DefinitionAndUsage-A_ownedRequirement_requirementOwningDefinition"),
    # <p>The <code>StateUsages</code> that are <code>ownedUsages</code> of this <code>Definition</code
    # >.</p>
    'ownedState': _Ref('ownedState', "StateUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedAction",), assoc="Systems-DefinitionAndUsage-A_ownedState_stateOwningDefinition"),
    # <p>The <code>TransitionUsages</code> that are <code>ownedUsages</code> of this <code>Definition<
    # /code>.</p>
    'ownedTransition': _Ref('ownedTransition', "TransitionUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedUsage",), assoc="Systems-DefinitionAndUsage-A_ownedTransition_transitionOwningDefinition"),
    # <p>The <code>Usages</code> that are <code>ownedFeatures</code> of this <code>Definition</code>.<
    # /p>
    'ownedUsage': _Ref('ownedUsage', "Usage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("usage",), assoc="Systems-DefinitionAndUsage-A_ownedUsage_owningDefinition"),
    # <p>The <code>UseCaseUsages</code> that are <code>ownedUsages</code> of this <code>Definition</co
    # de>.</p>
    'ownedUseCase': _Ref('ownedUseCase', "UseCaseUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedCase",), assoc="Systems-DefinitionAndUsage-A_ownedUseCase_useCaseOwningDefinition"),
    # <p>The <code>VerificationCaseUsages</code> that are <code>ownedUsages</code> of this <code>Defin
    # ition</code>.</p>
    'ownedVerificationCase': _Ref('ownedVerificationCase', "VerificationCaseUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedCase",), assoc="Systems-DefinitionAndUsage-A_ownedVerificationCase_verificationCaseOwningDefinition"),
    # <p>The <code>ViewUsages</code> that are <code>ownedUsages</code> of this <code>Definition</code>
    # .</p>
    'ownedView': _Ref('ownedView', "ViewUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedPart",), assoc="Systems-DefinitionAndUsage-A_ownedView_viewOwningDefinition"),
    # <p>The <code>ViewpointUsages</code> that are <code>ownedUsages</code> of this <code>Definition</
    # code>.</p>
    'ownedViewpoint': _Ref('ownedViewpoint', "ViewpointUsage", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("ownedRequirement",), assoc="Systems-DefinitionAndUsage-A_ownedViewpoint_viewpointOwningDefinition"),
    # <p>The <code>Usages</code> that are <code>features</code> of this <code>Definition</code> (not n
    # ecessarily owned).</p>
    'usage': _Ref('usage', "Usage", derived=True, multi=True, lo=0, hi='*', assoc="Systems-DefinitionAndUsage-A_usage_featuringDefinition"),
    # <p>The <code>Usages</code> which represent the variants of this <code>Definition</code> as a var
    # iation point <code>Definition</code>, if <code>isVariation</code> = true. If <code>isVariation =
    #  false</code>, the there must be no <code>variants</code>.</p>
    'variant': _Ref('variant', "Usage", derived=True, multi=True, lo=0, hi='*', assoc="Systems-DefinitionAndUsage-A_variant_owningVariationDefinition"),
    # <p>The <code>ownedMemberships</code> of this <code>Definition</code> that are <code>VariantMembe
    # rships</code>. If <code>isVariation</code> = true, then this must be all <code>ownedMemberships<
    # /code> of the <code>Definition</code>. If <code>isVariation</code> = false, then <code>variantMe
    # mbership</code>must be empty.</p>
    'variantMembership': _Ref('variantMembership', "VariantMembership", derived=True, multi=True, lo=0, hi='*', assoc="Systems-DefinitionAndUsage-A_variantMembership_owningVariationDefinition"),
    }
    CONSTRAINTS = (
        ("deriveDefinitionOwnedOccurrence",
         "ownedOccurrence = ownedUsage->selectByKind(OccurrenceUsage)"
        ),
        ("deriveDefinitionUsage",
         "usage = feature->selectByKind(Usage)"
        ),
        ("deriveDefinitionOwnedUsage",
         "ownedUsage = ownedFeature->selectByKind(Usage)"
        ),
        ("deriveDefinitionOwnedPart",
         "ownedPart = ownedUsage->selectByKind(PartUsage)"
        ),
        ("deriveDefinitionDirectedUsage",
         "directedUsage = directedFeature->selectByKind(Usage)"
        ),
        ("deriveDefinitionOwnedVerificationCase",
         "ownedVerificationCase = ownedUsage->selectByKind(VerificationCaseUsage)"
        ),
        ("deriveDefinitionOwnedViewpoint",
         "ownedViewpoint = ownedUsage->selectByKind(ViewpointUsage)"
        ),
        ("deriveDefinitionOwnedAnalysisCase",
         "ownedAnalysisCase = ownedUsage->selectByKind(AnalysisCaseUsage)"
        ),
        ("deriveDefinitionOwnedFlow",
         "ownedFlow = ownedUsage->selectByKind(FlowConnectionUsage)"
        ),
        ("deriveDefinitionOwnedAction",
         "ownedAction = ownedUsage->selectByKind(ActionUsage)"
        ),
        ("deriveDefinitionOwnedMetadata",
         "ownedMetadata = ownedUsage->selectByKind(MetadataUsage)"
        ),
        ("validateDefinitionVariationSpecialization",
         "isVariation implies     not ownedSpecialization.specific->exists(         oclIsKindOf(De"
         "finition) and         oclAsType(Definition).isVariation)"
        ),
        ("deriveDefinitionVariantMembership",
         "variantMembership = ownedMembership->selectByKind(VariantMembership)"
        ),
        ("deriveDefinitionOwnedCalculation",
         "ownedCalculation = ownedUsage->selectByKind(CalculationUsage)"
        ),
        ("deriveDefinitionOwnedUseCase",
         "ownedUseCase = ownedUsage->selectByKind(UseCaseUsage)"
        ),
        ("deriveDefinitionOwnedRequirement",
         "ownedRequirement = ownedUsage->selectByKind(RequirementUsage)"
        ),
        ("deriveDefinitionOwnedItem",
         "ownedItem = ownedUsage->selectByKind(ItemUsage)"
        ),
        ("deriveDefinitionOwnedConcern",
         "ownedConcern = ownedUsage->selectByKind(ConcernUsage)"
        ),
        ("deriveDefinitionOwnedConstraint",
         "ownedConstraint = ownedUsage->selectByKind(ConstraintUsage)"
        ),
        ("deriveDefinitionOwnedReference",
         "ownedReference = ownedUsage->selectByKind(ReferenceUsage)"
        ),
        ("deriveDefinitionOwnedCase",
         "ownedCase = ownedUsage->selectByKind(CaseUsage)"
        ),
        ("deriveDefinitionOwnedEnumeration",
         "ownedEnumeration = ownedUsage->selectByKind(EnumerationUsage)"
        ),
        ("deriveDefinitionOwnedState",
         "ownedState = ownedUsage->selectByKind(StateUsage)"
        ),
        ("deriveDefinitionOwnedRendering",
         "ownedRendering = ownedUsage->selectByKind(RenderingUsage)"
        ),
        ("deriveDefinitionOwnedAttribute",
         "ownedAttribute = ownedUsage->selectByKind(AttributeUsage)"
        ),
        ("deriveDefinitionOwnedPort",
         "ownedPort = ownedUsage->selectByKind(PortUsage)"
        ),
        ("deriveDefinitionOwnedTransition",
         "ownedTransition = ownedUsage->selectByKind(TransitionUsage)"
        ),
        ("deriveDefinitionVariant",
         "variant = variantMembership.ownedVariantUsage"
        ),
        ("deriveDefinitionOwnedAllocation",
         "ownedAllocation = ownedUsage->selectByKind(AllocationUsage)"
        ),
        ("deriveDefinitionOwnedView",
         "ownedView = ownedUsage->selectByKind(ViewUsage)"
        ),
        ("validateDefinitionVariationIsAbstract",
         "isVariation implies isAbstract"
        ),
        ("validateDefinitionVariationOwnedFeatureMembership",
         "isVariation implies ownedFeatureMembership->isEmpty()"
        ),
        ("deriveDefinitionOwnedConnection",
         "ownedConnection = ownedUsage->selectByKind(ConnectorAsUsage)"
        ),
        ("deriveDefinitionOwnedInterface",
         "ownedInterface = ownedUsage->selectByKind(ReferenceUsage)"
        ),
    )

class Class(Classifier):
    """<p>A <code>Class</code> is a <code>Classifier</code> of things (in the universe) that can be distinguished without regard to how they are related to other things (via <code>Features</code>). This means multiple things classified by the same <code>Class</code> can be distinguished, even when they are related other things in exactly the same way.</p>"""
    _PKG = "Classes"
    CONSTRAINTS = (
        ("checkClassSpecialization",
         "specializesFromLibrary('Occurrences::Occurrence')"
        ),
        ("validateClassSpecialization",
         "ownedSpecialization.general->     forAll(not oclIsKindOf(DataType)) and not oclIsKindOf("
         "Association) implies     ownedSpecialization.general->         forAll(not oclIsKindOf(As"
         "sociation))"
        ),
    )

class OccurrenceDefinition(Definition, Class):
    """<p>An <code>OccurrenceDefinition</code> is a <code>Definition</code> of a <code>Class</code> of individuals that have an independent life over time and potentially an extent over space. This includes both structural things and behaviors that act on such structures. If <code>isIndividual</code> is true, then the <code>OccurrenceDefinition</code> is constrained to have (at most) a single instance that is the entire life of a single individual.</p>"""
    _PKG = "Occurrences"
    _DECL = {
    # <p>Whether this <code>OccurrenceDefinition</code> is constrained to represent at most one thing.
    # </p>
    'isIndividual': _Ref('isIndividual', bool),
    }
    CONSTRAINTS = (
        ("checkOccurrenceDefinitionIndividualSpecialization",
         "isIndividual implies specializesFromLibrary('Occurrences::Life')"
        ),
        ("checkOccurrenceDefinitionMultiplicitySpecialization",
         "isIndividual implies     multiplicity <> null and     multiplicity.specializesFromLibrar"
         "y('Base::zeroOrOne')"
        ),
    )

class Behavior(Class):
    """<p>A <code>Behavior </code>coordinates occurrences of other <code>Behaviors</code>, as well as changes in objects. <code>Behaviors</code> can be decomposed into <code>Steps</code> and be characterized by <code>parameters</code>.</p>"""
    _PKG = "Behaviors"
    _DECL = {
    # <p>The parameters of this <code>Behavior</code>, which are defined as its <code>directedFeatures
    # </code>, whose values are passed into and/or out of a performance of the <code>Behavior</code>.<
    # /p>
    'parameter': _Ref('parameter', "Feature", derived=True, multi=True, lo=0, hi='*', redefines=("directedFeature",), assoc="Kernel-Behaviors-A_parameter_parameteredBehavior"),
    # <p>The <code>Steps</code> that make up this <code>Behavior</code>.</p>
    'step': _Ref('step', "Step", derived=True, multi=True, lo=0, hi='*', subsets=("feature",), assoc="Kernel-Behaviors-A_step_featuringBehavior"),
    }
    CONSTRAINTS = (
        ("checkBehaviorSpecialization",
         "specializesFromLibrary('Performances::Performance')"
        ),
        ("validateBehaviorSpecialization",
         "ownedSpecialization.general->forAll(not oclIsKindOf(Structure))"
        ),
        ("deriveBehaviorStep",
         "step = feature->selectByKind(Step)"
        ),
    )

class ActionDefinition(OccurrenceDefinition, Behavior):
    """<p>An <code>ActionDefinition</code> is a <code>Definition</code> that is also a <code>Behavior</code> that defines an <em><code>Action</code></em> performed by a system or part of a system.</p>"""
    _PKG = "Actions"
    _DECL = {
    # <p>The <code>ActionUsages</code> that are <code>steps</code> in this <code>ActionDefinition</cod
    # e>, which define the actions that specify the behavior of the <code>ActionDefinition</code>.</p>
    'action': _Ref('action', "ActionUsage", derived=True, multi=True, lo=0, hi='*', subsets=("usage",), assoc="Systems-Actions-A_action_featuringActionDefinition"),
    }
    CONSTRAINTS = (
        ("checkActionDefinitionSpecialization",
         "specializesFromLibrary('Actions::Action')"
        ),
        ("deriveActionDefinitionAction",
         "action = usage->selectByKind(ActionUsage)"
        ),
    )

class Relationship(Element):
    """<p>A <code>Relationship</code> is an <code>Element</code> that relates other <code>Element</code>. Some of its <code>relatedElements</code> may be owned, in which case those <code>ownedRelatedElements</code> will be deleted from a model if their <code>owningRelationship</code> is. A <code>Relationship</code> may also be owned by another <code>Element</code>, in which case the <code>ownedRelatedElements</code> of the <code>Relationship</code> are also considered to be transitively owned by the <code>owningRelatedElement</code> of the <code>Relationship</code>.</p> <p>The <code>relatedElements</code> of a <code>Relationship</code> are divided into <code>source</code> and <code>target</code> <code>Elements</code>. The <code>Relationship</code> is considered to be directed from the <code>source</code> to the <code>target</code> <code>Elements</code>. An undirected <code>Relationship</code> m...[truncated]"""
    _PKG = "Elements"
    _DECL = {
    # <p>Whether this Relationship was generated by tooling to meet semantic rules, rather than being 
    # directly created by a modeler.</p>
    'isImplied': _Ref('isImplied', bool),
    # <p>The <tt>relatedElements</tt> of this Relationship that are owned by the Relationship.</p>
    'ownedRelatedElement': _Ref('ownedRelatedElement', "Element", composite=True, multi=True, lo=0, hi='*', subsets=("relatedElement",), assoc="Root-Elements-A_ownedRelatedElement_owningRelationship"),
    # <p>The <tt>relatedElement</tt> of this Relationship that owns the Relationship, if any.</p>
    'owningRelatedElement': _Ref('owningRelatedElement', "Element", subsets=("relatedElement",), assoc="Root-Elements-A_ownedRelationship_owningRelatedElement"),
    # <p>The Elements that are related by this Relationship, derived as the union of the <code>source<
    # /code> and <code>target</code> Elements of the Relationship.</p>
    'relatedElement': _Ref('relatedElement', "Element", derived=True, multi=True, lo=0, hi='*', assoc="Root-Elements-A_relatedElement_relationship"),
    # <p>The <code>relatedElements</c ode> from which this Relationship is considered to be directed.<
    # /p>
    'source': _Ref('source', "Element", multi=True, lo=0, hi='*', subsets=("relatedElement",), assoc="Root-Elements-A_source_sourceRelationship"),
    # <p>The <code>relatedElements</code> to which this Relationship is considered to be directed.</p>
    'target': _Ref('target', "Element", multi=True, lo=0, hi='*', subsets=("relatedElement",), assoc="Root-Elements-A_target_targetRelationship"),
    }
    CONSTRAINTS = (
        ("deriveRelationshipRelatedElement",
         "relatedElement = source->union(target)"
        ),
    )
    def libraryNamespace(self, arg: None = None) -> None:
        """
        <p>Return whether this Relationship has either an <code>owningRelatedElement</code> or <code>o
        wningRelationship</code> that is a library element.</p>
        [Relationship operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def path(self, arg: None = None) -> None:
        """
        <p>If the <code>owningRelationship</code> of the <code>Relationship</code> is null but its <co
        de>owningRelatedElement</code> is non-null, construct the <code>path</code> using the position
         of the <code>Relationship</code> in the list of <code>ownedRelationships</code> of its <code>
        owningRelatedElement</code>. Otherwise, return the <code>path</code> of the <code>Relationship
        </code> as specified for an <code>Element</code> in general.</p>
        [Relationship operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError

class Membership(Relationship):
    """<p>A <code>Membership</code> is a <code>Relationship</code> between a <code>Namespace</code> and an <code>Element</code> that indicates the <code>Element</code> is a <code>member</code> of (i.e., is contained in) the Namespace. Any <code>memberNames</code> specify how the <code>memberElement</code> is identified in the <code>Namespace</code> and the <code>visibility</code> specifies whether or not the <code>memberElement</code> is publicly visible from outside the <code>Namespace</code>.</p> <p>If a <code>Membership</code> is an <code>OwningMembership</code>, then it owns its <code>memberElement</code>, which becomes an <code>ownedMember</code> of the <code>membershipOwningNamespace</code>. Otherwise, the <code>memberNames</code> of a <code>Membership</code> are effectively aliases within the <code>membershipOwningNamespace</code> for an <code>Element</code> with a separate <code>OwningM...[truncated]"""
    _PKG = "Namespaces"
    _DECL = {
    # <p>The <code>Element</code> that becomes a <code>member</code> of the <code>membershipOwningName
    # space</code> due to this <code>Membership</code>.</p>
    'memberElement': _Ref('memberElement', "Element", redefines=("target",), assoc="Root-Namespaces-A_memberElement_membership"),
    # <p>The <code>elementId</code> of the <code>memberElement</code>.</p>
    'memberElementId': _Ref('memberElementId', str, derived=True),
    # <p>The name of the <code>memberElement</code> relative to the <code>membershipOwningNamespace</c
    # ode>.</p>
    'memberName': _Ref('memberName', str),
    # <p>The short name of the <code>memberElement</code> relative to the <code>membershipOwningNamesp
    # ace</code>.</p>
    'memberShortName': _Ref('memberShortName', str),
    # <p>The <code>Namespace</code> of which the <code>memberElement</code> becomes a <code>member</co
    # de> due to this <code>Membership</code>.</p>
    'membershipOwningNamespace': _Ref('membershipOwningNamespace', "Namespace", derived=True, subsets=("owningRelatedElement",), redefines=("source",), assoc="Root-Namespaces-A_ownedMembership_membershipOwningNamespace"),
    # <p>Whether or not the <code>Membership</code> of the <code>memberElement</code> in the <code>mem
    # bershipOwningNamespace</code> is publicly visible outside that <code>Namespace</code>.</p>
    'visibility': _Ref('visibility', None),
    }
    CONSTRAINTS = (
        ("deriveMembershipMemberElementId",
         "memberElementId = memberElement.elementId"
        ),
    )
    def isDistinguishableFrom(self, other: None = None, arg: None = None) -> None:
        """
        <p>Whether this <code>Membership</code> is distinguishable from a given <code>other</code> <co
        de>Membership</code>. By default, this is true if this <code>Membership</code> has no <code>me
        mberShortName</code> or <code>memberName</code>; or each of the <code>memberShortName</code> a
        nd <code>memberName</code> are different than both of those of the <code>other</code> <code>Me
        mbership</code>; or neither of the metaclasses of the <code>memberElement</code> of this <code
        >Membership</code> and the <code>memberElement</code> of the <code>other</code> <code>Membersh
        ip</code> conform to the other. But this may be overridden in specializations of <code>Members
        hip</code>.</p>
        [Membership operation; params: other: ?, arg: ?; returns: nothing; stub - metamodel metadata o
        nly]
        """
        raise NotImplementedError

class OwningMembership(Membership):
    """<p>An <code>OwningMembership</code> is a <code>Membership</code> that owns its <code>memberElement</code> as a <code>ownedRelatedElement</code>. The <code>ownedMemberElement</code> becomes an <code>ownedMember</code> of the <code>membershipOwningNamespace</code>.</p>"""
    _PKG = "Namespaces"
    _DECL = {
    # <p>The <code>Element</code> that becomes an <code>ownedMember</code> of the <code>membershipOwni
    # ngNamespace</code> due to this <code>OwningMembership</code>.</p>
    'ownedMemberElement': _Ref('ownedMemberElement', "Element", derived=True, composite=True, subsets=("ownedRelatedElement",), redefines=("memberElement",), assoc="Root-Namespaces-A_ownedMemberElement_owningMembership"),
    # <p>The <code>elementId</code> of the <code>ownedMemberElement</code>.</p>
    'ownedMemberElementId': _Ref('ownedMemberElementId', str, derived=True, composite=True, redefines=("memberElementId",)),
    # <p>The <code>name</code> of the <code>ownedMemberElement</code>.</p>
    'ownedMemberName': _Ref('ownedMemberName', str, derived=True, composite=True, redefines=("memberName",)),
    # <p>The <code>shortName</code> of the <code>ownedMemberElement</code>.</p>
    'ownedMemberShortName': _Ref('ownedMemberShortName', str, derived=True, composite=True, redefines=("memberShortName",)),
    }
    CONSTRAINTS = (
        ("deriveOwningMembershipOwnedMemberName",
         "ownedMemberName = ownedMemberElement.name"
        ),
        ("deriveOwningMembershipOwnedMemberShortName",
         "ownedMemberShortName = ownedMemberElement.shortName"
        ),
    )
    def path(self, arg: None = None) -> None:
        """
        <p>If the <code>ownedMemberElement</code> of this <code>OwningMembership</code> has a non-null
         <code>qualifiedName</code>, then return the string constructed by appending to that <code>qua
        lifiedName</code> the string <code>"/owningMembership"</code>. Otherwise, return the <code>pat
        h</code> of the <code>OwningMembership</code> as specified for a <code>Relationship</code> in 
        general.
        [OwningMembership operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError

class FeatureMembership(OwningMembership):
    """<p>A <code>FeatureMembership</code> is an <code>OwningMembership</code> between an <code>ownedMemberFeature</code> and an <code>owningType</code>. If the <code>ownedMemberFeature</code> has <code>isVariable = false</code>, then the <code>FeatureMembership</code> implies that the <code>owningType</code> is also a <code>featuringType</code> of the <code>ownedMemberFeature</code>. If the <code>ownedMemberFeature</code> has <code>isVariable = true</code>, then the <code>FeatureMembership</code> implies that the <code>ownedMemberFeature</code> is featured by the <em><code>snapshots</code></em> of the <code>owningType</code>, which must specialize the Kernel Semantic Library base class <em><code>Occurrence</code></em>.</p>"""
    _PKG = "Types"
    _DECL = {
    # <p>The <code>Feature</code> that this <code>FeatureMembership</code> relates to its <code>owning
    # Type</code>, making it an <code>ownedFeature</code> of the <code>owningType</code>.</p>
    'ownedMemberFeature': _Ref('ownedMemberFeature', "Feature", derived=True, composite=True, redefines=("ownedMemberElement",), assoc="Core-Types-A_ownedMemberFeature_owningFeatureMembership"),
    # <p>The <code>Type</code> that owns this <code>FeatureMembership</code>.</p>
    'owningType': _Ref('owningType', "Type", redefines=("membershipOwningNamespace",), assoc="Core-Types-A_ownedFeatureMembership_owningType"),
    }

class ParameterMembership(FeatureMembership):
    """<p>A <code>ParameterMembership</code> is a <code>FeatureMembership</code> that identifies its <code>memberFeature</code> as a parameter, which is always owned, and must have a <code>direction</code>. A <code>ParameterMembership</code> must be owned by a <code>Behavior</code>, a <code>Step</code>, or the <code>result</code> parameter of a <code>ConstructorExpression</code>.</p>"""
    _PKG = "Behaviors"
    _DECL = {
    # <p>The <code>Feature</code> that is identified as a <code>parameter</code> by this <code>Paramet
    # erMembership</code>.</p>
    'ownedMemberParameter': _Ref('ownedMemberParameter', "Feature", derived=True, composite=True, redefines=("ownedMemberFeature",), assoc="Kernel-Behaviors-A_ownedMemberParameter_owningParameterMembership"),
    }
    CONSTRAINTS = (
        ("validateParameterMembershipParameterDirection",
         "ownedMemberParameter.direction = parameterDirection()"
        ),
        ("validateParameterMembershipOwningType",
         "owningType.oclIsKindOf(Behavior) or owningType.oclIsKindOf(Step) or owningType.owningMem"
         "bership.oclIsKindOf(ReturnParameterMembership) and     owningType.owningNamespace.oclIsK"
         "indOf(ConstructorExpression)"
        ),
    )
    def parameterDirection(self, arg: None = None) -> None:
        """
        <p>Return the required value of the <code>direction</code> of the <code>ownedMemberParameter</
        code>. By default, this is <code>in</code>.</p>
        [ParameterMembership operation; params: arg: ?; returns: nothing; stub - metamodel metadata on
        ly]
        """
        raise NotImplementedError

class ActorMembership(ParameterMembership):
    """<p>An <code>ActorMembership</code> is a <code>ParameterMembership</code> that identifies a <code>PartUsage</code> as an <em>actor</em> <code>parameter</code>, which specifies a role played by an external entity in interaction with the <code>owningType</code> of the <code>ActorMembership</code>.</p>"""
    _PKG = "Requirements"
    _DECL = {
    # <p>The <code>PartUsage</code> specifying the actor.</p>
    'ownedActorParameter': _Ref('ownedActorParameter', "PartUsage", derived=True, composite=True, assoc="Systems-Requirements-A_ownedActorParameter_owningActorMembership"),
    }
    CONSTRAINTS = (
        ("validateActorMembershipOwningType",
         "owningType.oclIsKindOf(RequirementUsage) or owningType.oclIsKindOf(RequirementDefinition"
         ") or owningType.oclIsKindOf(CaseDefinition) or owningType.oclIsKindOf(CaseUsage)"
        ),
    )

class Structure(Class):
    """<p>A <code>Structure</code> is a <code>Class</code> of objects in the modeled universe that are primarily structural in nature. While such an object is not itself behavioral, it may be involved in and acted on by <code>Behaviors</code>, and it may be the performer of some of them.</p>"""
    _PKG = "Structures"
    CONSTRAINTS = (
        ("checkStructureSpecialization",
         "specializesFromLibrary('Objects::Object')"
        ),
        ("validateStructureSpecialization",
         "ownedSpecialization.general->forAll(not oclIsKindOf(Behavior))"
        ),
    )

class Association(Classifier, Relationship):
    """<p>An <code>Association</code> is a <code>Relationship</code> and a <code>Classifier</code> to enable classification of links between things (in the universe). The co-domains (<code>types</code>) of the <code>associationEnd</code> <code>Features</code> are the <code>relatedTypes</code>, as co-domain and participants (linked things) of an <code>Association</code> identify each other.</p>"""
    _PKG = "Associations"
    _DECL = {
    # <p>The <code>features</code> of the <code>Association</code> that identify the things that can b
    # e related by it. A concrete <code>Association</code> must have at least two <code>associationEnd
    # s</code>. When it has exactly two, the <code>Association</code> is called a <em>binary</em> <cod
    # e>Association</code>.</p>
    'associationEnd': _Ref('associationEnd', "Feature", derived=True, multi=True, lo=0, hi='*', redefines=("endFeature",), assoc="Kernel-Associations-A_associationEnd_associationWithEnd"),
    # <p>The <code>types</code> of the <code>associationEnds</code> of the <code>Association</code>, w
    # hich are the <code>relatedElements</code> of the <code>Association</code> considered as a <code>
    # Relationship</code>.</p>
    'relatedType': _Ref('relatedType', "Type", derived=True, multi=True, lo=0, hi='*', redefines=("relatedElement",), assoc="Kernel-Associations-A_relatedType_association"),
    # <p>The source <code>relatedType</code> for this <code>Association</code>. It is the first <code>
    # relatedType</code> of the <code>Association</code>.</p>
    'sourceType': _Ref('sourceType', "Type", derived=True, subsets=("relatedType",), redefines=("source",), assoc="Kernel-Associations-A_sourceType_sourceAssociation"),
    # <p>The target <code>relatedTypes</code> for this <code>Association</code>. This includes all the
    #  <code>relatedTypes</code> other than the <code>sourceType</code>.</p>
    'targetType': _Ref('targetType', "Type", derived=True, multi=True, lo=0, hi='*', subsets=("relatedType",), redefines=("target",), assoc="Kernel-Associations-A_targetType_targetAssociation"),
    }
    CONSTRAINTS = (
        ("validateAssociationStructureIntersection",
         "oclIsKindOf(Structure) = oclIsKindOf(AssociationStructure)"
        ),
        ("validateAssociationBinarySpecialization",
         "associationEnds->size() > 2 implies not specializesFromLibrary('Links::BinaryLink')"
        ),
        ("validateAssociationRelatedTypes",
         "not isAbstract implies relatedType->size() >= 2"
        ),
        ("deriveAssociationTargetType",
         "targetType =     if relatedType->size() < 2 then OrderedSet{}     else          relatedT"
         "ype->             subSequence(2, relatedType->size())->             asOrderedSet()      "
         "endif"
        ),
        ("checkAssociationSpecialization",
         "specializesFromLibrary('Links::Link')"
        ),
        ("deriveAssociationRelatedType",
         "relatedType = associationEnd.type"
        ),
        ("validateAssociationEndTypes",
         "ownedEndFeature->forAll(type->size() = 1)"
        ),
        ("deriveAssociationSourceType",
         "sourceType = if relatedType->isEmpty() then null else relatedType->first() endif"
        ),
        ("checkAssociationBinarySpecialization",
         "associationEnd->size() = 2 implies specializesFromLibrary('Links::BinaryLink')"
        ),
    )

class AssociationStructure(Structure, Association):
    """<p>An <code>AssociationStructure</code> is an <code>Association</code> that is also a <code>Structure</code>, classifying link objects that are both links and objects. As objects, link objects can be created and destroyed, and their non-end <code>Features</code> can change over time. However, the values of the end <code>Features</code> of a link object are fixed and cannot change over its lifetime.</p>"""
    _PKG = "Associations"
    CONSTRAINTS = (
        ("checkAssociationStructureSpecialization",
         "specializesFromLibrary('Objects::LinkObject')"
        ),
        ("checkAssociationStructureBinarySpecialization",
         "endFeature->size() = 2 implies specializesFromLibrary('Objects::BinaryLinkObject')"
        ),
    )

class ItemDefinition(Structure, OccurrenceDefinition):
    """<p>An <code>ItemDefinition</code> is an <code>OccurrenceDefinition</code> of the <code>Structure</code> of things that may themselves be systems or parts of systems, but may also be things that are acted on by a system or parts of a system, but which do not necessarily perform actions themselves. This includes items that can be exchanged between parts of a system, such as water or electrical signals.</p>"""
    _PKG = "Items"
    CONSTRAINTS = (
        ("checkItemDefinitionSpecialization",
         "specializesFromLibrary('Items::Item')"
        ),
    )

class PartDefinition(ItemDefinition):
    """<p>A <code>PartDefinition</code> is an <code>ItemDefinition</code> of a <code>Class</code> of systems or parts of systems. Note that all parts may be considered items for certain purposes, but not all items are parts that can perform actions within a system.</p>"""
    _PKG = "Parts"
    CONSTRAINTS = (
        ("checkPartDefinitionSpecialization",
         "specializesFromLibrary('Parts::Part')"
        ),
    )

class ConnectionDefinition(PartDefinition, AssociationStructure):
    """<p>A <code>ConnectionDefinition</code> is a <code>PartDefinition</code> that is also an <code>AssociationStructure</code>. The end <code>Features</code> of a <code>ConnectionDefinition</code> must be <code>Usages</code>.</p>"""
    _PKG = "Connections"
    _DECL = {
    # <p>The <code>Usages</code> that define the things related by the <code>ConnectionDefinition</cod
    # e>.</p>
    'connectionEnd': _Ref('connectionEnd', "Usage", derived=True, multi=True, lo=0, hi='*', assoc="Systems-Connections-A_connectionEnd_connectionDefinitionWithEnd"),
    # <p>A <code>ConnectionDefinition</code> always has <code>isSufficient = true</code>.</p>
    'isSufficient': _Ref('isSufficient', bool),
    }
    CONSTRAINTS = (
        ("checkConnectionDefinitionSpecializations",
         "specializesFromLibrary('Connections::Connection')"
        ),
        ("validateConnectionDefinitionIsSufficient",
         "isSufficient"
        ),
        ("checkConnectionDefinitionBinarySpecialization",
         "ownedEndFeature->size() = 2 implies specializesFromLibrary('Connections::BinaryConnectio"
         "ns')"
        ),
    )

class AllocationDefinition(ConnectionDefinition):
    """<p>An <code>AllocationDefinition</code> is a <code>ConnectionDefinition</code> that specifies that some or all of the responsibility to realize the intent of the <code>source</code> is allocated to the <code>target</code> instances. Such allocations define mappings across the various structures and hierarchies of a system model, perhaps as a precursor to more rigorous specifications and implementations. An <code>AllocationDefinition</code> can itself be refined using nested <code>allocations</code> that give a finer-grained decomposition of the containing allocation mapping.</p>"""
    _PKG = "Allocations"
    _DECL = {
    # <p>The <code>AllocationUsages</code> that refine the allocation mapping defined by this <code>Al
    # locationDefinition</code>.</p>
    'allocation': _Ref('allocation', "AllocationUsage", derived=True, multi=True, lo=0, hi='*', subsets=("usage",), assoc="Systems-Allocations-A_allocation_featuringAllocationDefinition"),
    }
    CONSTRAINTS = (
        ("deriveAllocationDefinitionAllocation",
         "allocation = usage->selectAsKind(AllocationUsage)"
        ),
        ("checkAllocationDefinitionSpecialization",
         "specializesFromLibrary('Allocations::Allocation')"
        ),
    )

class ItemUsage(OccurrenceUsage):
    """<p>An <code>ItemUsage</code> is a <code>ItemUsage</code> whose <code>definition</code> is a <code>Structure</code>. Nominally, if the <code>definition</code> is an <code>ItemDefinition</code>, an <code>ItemUsage</code> is a <code>ItemUsage</code> of that <code>ItemDefinition</code> within a system. However, other kinds of Kernel <code>Structures</code> are also allowed, to permit use of <code>Structures</code> from the Kernel Model Libraries.</p>"""
    _PKG = "Items"
    _DECL = {
    # <p>The Structures that are the <code>definitions</code> of this ItemUsage. Nominally, these are 
    # ItemDefinitions, but other kinds of Kernel Structures are also allowed, to permit use of Structu
    # res from the Kernel Library.</p>
    'itemDefinition': _Ref('itemDefinition', "Structure", derived=True, multi=True, lo=0, hi='*', subsets=("occurrenceDefinition",), assoc="Systems-DefinitionAndUsage-A_itemDefinition_definedItem"),
    }
    CONSTRAINTS = (
        ("deriveItemUsageItemDefinition",
         "itemDefinition = occurrenceDefinition->selectByKind(Structure)"
        ),
        ("checkItemUsageSpecialization",
         "specializesFromLibrary('Items::items')"
        ),
        ("checkItemUsageSubitemSpecialization",
         "isComposite and owningType <> null and (owningType.oclIsKindOf(ItemDefinition) or  ownin"
         "gType.oclIsKindOf(ItemUsage)) implies     specializesFromLibrary('Items::Item::subitem')"
        ),
    )

class PartUsage(ItemUsage):
    """<p>A <code>PartUsage</code> is a usage of a <code>PartDefinition</code> to represent a system or a part of a system. At least one of the <code>itemDefinitions</code> of the <code>PartUsage</code> must be a <code>PartDefinition</code>.</p> <p>A <code>PartUsage</code> must subset, directly or indirectly, the base <code>PartUsage</code> <em><code>parts</code></em> from the Systems Model Library.</p>"""
    _PKG = "Parts"
    _DECL = {
    # <p>The <code>itemDefinitions</code> of this PartUsage that are PartDefinitions.</p>
    'partDefinition': _Ref('partDefinition', "PartDefinition", derived=True, multi=True, lo=0, hi='*', subsets=("itemDefinition",), assoc="Systems-Parts-A_partDefinition_definedPart"),
    }
    CONSTRAINTS = (
        ("checkPartUsageActorSpecialization",
         "owningFeatureMembership <> null and owningFeatureMembership.oclIsKindOf(ActorMembership)"
         " implies     if owningType.oclIsKindOf(RequirementDefinition) or         owningType.oclI"
         "sKindOf(RequirementUsage)     then specializesFromLibrary('Requirements::RequirementChec"
         "k::actors')     else specializesFromLibrary('Cases::Case::actors')"
        ),
        ("checkPartUsageSpecialization",
         "specializesFromLibrary('Parts::parts')"
        ),
        ("checkPartUsageStakeholderSpecialization",
         "owningFeatureMembership <> null and owningFeatureMembership.oclIsKindOf(StakeholderMembe"
         "rship) implies     specializesFromLibrary('Requirements::RequirementCheck::stakeholders'"
         ")"
        ),
        ("validatePartUsagePartDefinition",
         "partDefinition->notEmpty()"
        ),
        ("derivePartUsagePartDefinition",
         "itemDefinition->selectByKind(PartDefinition)"
        ),
        ("checkPartUsageSubpartSpecialization",
         "isComposite and owningType <> null and (owningType.oclIsKindOf(ItemDefinition) or  ownin"
         "gType.oclIsKindOf(ItemUsage)) implies     specializesFromLibrary('Items::Item::subparts'"
         ")"
        ),
    )

class Connector(Feature, Relationship):
    """<p>A <code>Connector</code> is a usage of <code>Associations</code>, with links restricted according to instances of the <code>Type</code> in which they are used (domain of the <code>Connector</code>). The <code>associations</code> of the <code>Connector</code> restrict what kinds of things might be linked. The <code>Connector</code> further restricts these links to be between values of <code>Features</code> on instances of its domain.</p>"""
    _PKG = "Connectors"
    _DECL = {
    # <p>The <code>Associations</code> that type the <code>Connector</code>.</p>
    'association': _Ref('association', "Association", derived=True, multi=True, lo=0, hi='*', redefines=("type",), assoc="Kernel-Connectors-A_association_typedConnector"),
    # <p>The <code>endFeatures</code> of a <code>Connector</code>, which redefine the <code>endFeature
    # s</code> of the <code>associations</code> of the <code>Connector</code>. The <code>connectorEnds
    # </code> determine via <code>ReferenceSubsetting</code> <code>Relationships</code> which <code>Fe
    # atures</code> are related by the <code>Connector</code>.</p>
    'connectorEnd': _Ref('connectorEnd', "Feature", derived=True, multi=True, lo=0, hi='*', redefines=("endFeature",), assoc="Kernel-Connectors-A_connectorEnd_featuringConnector"),
    # <p>The innermost <code>Type</code> that is a common direct or indirect <code>featuringType</code
    # > of the <code>relatedFeatures</code>, such that, if it exists and was the <code>featuringType</
    # code> of this <code>Connector</code>, the <code>Connector</code> would satisfy the <code>checkCo
    # nnectorTypeFeaturing</code> constraint.</p>
    'defaultFeaturingType': _Ref('defaultFeaturingType', "Type", derived=True, assoc="Kernel-Connectors-A_defaultFeaturingType_featuredConnector"),
    # <p>The <code>Features</code> that are related by this <code>Connector</code> considered as a <co
    # de>Relationship</code> and that restrict the links it identifies, given by the referenced <code>
    # Features</code> of the <code>connectorEnds</code> of the <code>Connector</code>.</p>
    'relatedFeature': _Ref('relatedFeature', "Feature", derived=True, multi=True, lo=0, hi='*', redefines=("relatedElement",), assoc="Kernel-Connectors-A_relatedFeature_connector"),
    # <p>The source <code>relatedFeature</code> for this <code>Connector</code>. It is the first <code
    # >relatedFeature</code>.</p>
    'sourceFeature': _Ref('sourceFeature', "Feature", derived=True, subsets=("relatedFeature",), redefines=("source",), assoc="Kernel-Connectors-A_sourceFeature_sourceConnector"),
    # <p>The target <code>relatedFeatures</code> for this <code>Connector</code>. This includes all th
    # e <code>relatedFeatures</code> other than the <code>sourceFeature</code>.</p>
    'targetFeature': _Ref('targetFeature', "Feature", derived=True, multi=True, lo=0, hi='*', subsets=("relatedFeature",), redefines=("target",), assoc="Kernel-Connectors-A_targetFeature_targetConnector"),
    }
    CONSTRAINTS = (
        ("checkConnectorBinarySpecialization",
         "connectorEnd->size() = 2 implies specializesFromLibrary('Links::binaryLinks')"
        ),
        ("deriveConnectorSourceFeature",
         "sourceFeature = if relatedFeature->isEmpty() then null else relatedFeature->first() endi"
         "f"
        ),
        ("checkConnectorTypeFeaturing",
         "relatedFeature->forAll(f |      if featuringType->isEmpty() then f.isFeaturedWithin(null"
         ")     else featuringType->forAll(t | f.isFeaturedWithin(t))     endif)"
        ),
        ("deriveConnectorTargetFeature",
         "targetFeature =     if relatedFeature->size() < 2 then OrderedSet{}     else          re"
         "latedFeature->             subSequence(2, relatedFeature->size())->             asOrdere"
         "dSet()     endif"
        ),
        ("checkConnectorObjectSpecialization",
         "association->exists(oclIsKindOf(AssociationStructure)) implies specializesFromLibrary('O"
         "bjects::linkObjects')"
        ),
        ("validateConnectorBinarySpecialization",
         "connectorEnds->size() > 2 implies not specializesFromLibrary('Links::BinaryLink')"
        ),
        ("deriveConnectorRelatedFeature",
         "relatedFeature = connectorEnd.ownedReferenceSubsetting-> select(s | s <> null).subsetted"
         "Feature"
        ),
        ("checkConnectorSpecialization",
         "specializesFromLibrary('Links::links')"
        ),
        ("validateConnectorRelatedFeatures",
         "not isAbstract implies relatedFeature->size() >= 2"
        ),
        ("deriveConnectorDefaultFeaturingType",
         "let commonFeaturingTypes : OrderedSet(Type) =      relatedFeature->closure(featuringType"
         ")->select(t |          relatedFeature->forAll(f | f.isFeaturedWithin(t))     ) in let ne"
         "arestCommonFeaturingTypes : OrderedSet(Type) =     commonFeaturingTypes->reject(t1 |    "
         "      commonFeaturingTypes->exists(t2 |              t2 <> t1 and t2->closure(featuringT"
         "ype)->contains(t1)     )) in if nearestCommonFeaturingTypes->isEmpty() then null else ne"
         "arestCommonFeaturingTypes->first() endif"
        ),
        ("checkConnectorBinaryObjectSpecialization",
         "connectorEnds->size() = 2 and association->exists(oclIsKindOf(AssociationStructure)) imp"
         "lies     specializesFromLibrary('Objects::binaryLinkObjects')"
        ),
    )

class ConnectorAsUsage(Usage, Connector):
    """<p>A <code>ConnectorAsUsage</code> is both a <code>Connector</code> and a <code>Usage</code>. <code>ConnectorAsUsage</code> cannot itself be instantiated in a SysML model, but it is a base class for the concrete classes <code>BindingConnectorAsUsage</code>, <code>SuccessionAsUsage</code>, <code>ConnectionUsage</code> and <code>FlowConnectionUsage</code>.</p>"""
    _PKG = "Connections"

class ConnectionUsage(PartUsage, ConnectorAsUsage):
    """<p>A <code>ConnectionUsage</code> is a <code>ConnectorAsUsage</code> that is also a <code>PartUsage</code>. Nominally, if its type is a <code>ConnectionDefinition</code>, then a <code>ConnectionUsage</code> is a Usage of that <code>ConnectionDefinition</code>, representing a connection between parts of a system. However, other kinds of kernel <code>AssociationStructures</code> are also allowed, to permit use of <code>AssociationStructures</code> from the Kernel Model Libraries.</p>"""
    _PKG = "Connections"
    _DECL = {
    # <p>The <code>AssociationStructures</code> that are the types of this <code>ConnectionUsage</code
    # >. Nominally, these are , but other kinds of Kernel <code>AssociationStructures</code> are also 
    # allowed, to permit use of <code>AssociationStructures</code> from the Kernel Model Libraries</p>
    'connectionDefinition': _Ref('connectionDefinition', "AssociationStructure", derived=True, multi=True, lo=0, hi='*', subsets=("itemDefinition",), assoc="Systems-Connections-A_connectionDefinition_definedConnection"),
    }
    CONSTRAINTS = (
        ("checkConnectionUsageSpecialization",
         "specializesFromLibrary('Connections::connections')"
        ),
        ("checkConnectionUsageBinarySpecialization",
         "ownedEndFeature->size() = 2 implies specializesFromLibrary('Connections::binaryConnectio"
         "ns')"
        ),
    )

class AllocationUsage(ConnectionUsage):
    """<p>An <code>AllocationUsage</code> is a usage of an <code>AllocationDefinition</code> asserting the allocation of the <code>source</code> feature to the <code>target</code> feature.</p>"""
    _PKG = "Allocations"
    _DECL = {
    # <p>The <code>AllocationDefinitions</code> that are the types of this <code>AllocationUsage</code
    # >.</p>
    'allocationDefinition': _Ref('allocationDefinition', "AllocationDefinition", derived=True, multi=True, lo=0, hi='*', redefines=("connectionDefinition",), assoc="Systems-Allocations-A_allocationDefinition_definedAllocation"),
    }
    CONSTRAINTS = (
        ("checkAllocationUsageSpecialization",
         "specializesFromLibrary('Allocations::allocations')"
        ),
    )

class Function(Behavior):
    """<p>A <code>Function</code> is a <code>Behavior</code> that has an <code>out</code> <code>parameter</code> that is identified as its <code>result</code>. A <code>Function</code> represents the performance of a calculation that produces the values of its <code>result</code> <code>parameter</code>. This calculation may be decomposed into <code>Expressions</code> that are <code>steps</code> of the <code>Function</code>.</p>"""
    _PKG = "Functions"
    _DECL = {
    # <p>The <code>Expressions</code> that are <code>steps</code> in the calculation of the <code>resu
    # lt</code> of this <code>Function</code>.</p>
    'expression': _Ref('expression', "Expression", derived=True, multi=True, lo=0, hi='*', subsets=("step",), assoc="Kernel-Functions-A_expression_computedFunction"),
    # <p>Whether this <code>Function</code> can be used as the <code>function</code> of a model-level 
    # evaluable <code>InvocationExpression</code>. Certain <code>Functions</code> from the Kernel Func
    # tions Library are considered to have <code>isModelLevelEvaluable = true</code>. For all other <c
    # ode>Functions</code> it is <code>false</code>.</p> <p><strong>Note:</strong> See the specificati
    # on of the KerML concrete syntax notation for <code>Expressions</code> for an identification of w
    # hich library <code>Functions</code> are model-level evaluable.</p>
    'isModelLevelEvaluable': _Ref('isModelLevelEvaluable', bool, derived=True),
    # <p>The object or value that is the result of evaluating the Function.</p>
    'result': _Ref('result', "Feature", derived=True, subsets=("output", "parameter",), assoc="Kernel-Functions-A_result_computingFunction"),
    }
    CONSTRAINTS = (
        ("validateFunctionResultParameterMembership",
         "featureMembership-> selectByKind(ReturnParameterMembership)-> size() = 1"
        ),
        ("checkFunctionResultBindingConnector",
         "ownedMembership.selectByKind(ResultExpressionMembership)->     forAll(mem | ownedFeature"
         ".selectByKind(BindingConnector)->         exists(binding |             binding.relatedFe"
         "ature->includes(result) and             binding.relatedFeature->includes(mem.ownedResult"
         "Expression.result)))"
        ),
        ("deriveFunctionResult",
         "result =     let resultParams : Sequence(Feature) =         featureMemberships->        "
         "     selectByKind(ReturnParameterMembership).             ownedMemberParameter in     if"
         " resultParams->notEmpty() then resultParams->first()     else null     endif"
        ),
        ("validateFunctionResultExpressionMembership",
         "membership->selectByKind(ResultExpressionMembership)->size() <= 1"
        ),
        ("checkFunctionSpecialization",
         "specializesFromLibrary('Performances::Evaluation')"
        ),
    )

class CalculationDefinition(ActionDefinition, Function):
    """<p>A <code>CalculationDefinition</code> is an <coed>ActionDefinition</code> that also defines a <code>Function</code> producing a <code>result</code>.</p>"""
    _PKG = "Calculations"
    _DECL = {
    # <p>The <code>actions</code> of this <code>CalculationDefinition</code> that are <code>Calculatio
    # nUsages</code>.</p>
    'calculation': _Ref('calculation', "CalculationUsage", derived=True, multi=True, lo=0, hi='*', subsets=("action",), assoc="Systems-Calculations-A_calculation_featuringCalculationDefinition"),
    }
    CONSTRAINTS = (
        ("checkCalculationDefinitionSpecialization",
         "specializesFromLibrary('Calculations::Calculation')"
        ),
        ("deriveCalculationUsageCalculation",
         "calculation = action->selectByKind(CalculationUsage)"
        ),
    )

class CaseDefinition(CalculationDefinition):
    """<p>A <code>CaseDefinition</code> is a <code>CalculationDefinition</code> for a process, often involving collecting evidence or data, relative to a subject, possibly involving the collaboration of one or more other actors, producing a result that meets an objective.</p>"""
    _PKG = "Cases"
    _DECL = {
    # <p>The <code>parameters</code> of this <code>CaseDefinition</code> that represent actors involve
    # d in the case.</p>
    'actorParameter': _Ref('actorParameter', "PartUsage", derived=True, multi=True, lo=0, hi='*', subsets=("usage",), assoc="Systems-Cases-A_actorParameter_actorOwningCaseDefinition"),
    # <p>The <code>RequirementUsage</code> representing the objective of this <code>CaseDefinition</co
    # de>.</p>
    'objectiveRequirement': _Ref('objectiveRequirement', "RequirementUsage", derived=True, subsets=("usage",), assoc="Systems-Cases-A_objectiveRequirement_objectiveOwningCaseDefinition"),
    # <p>The <code>parameter</code> of this <code>CaseDefinition</code> that represents its subject.</
    # p>
    'subjectParameter': _Ref('subjectParameter', "Usage", derived=True, subsets=("usage",), assoc="Systems-Cases-A_subjectParameter_subjectOwningCaseDefinition"),
    }
    CONSTRAINTS = (
        ("checkCaseDefinitionSpecialization",
         "specializesFromLibrary('Cases::Case')"
        ),
        ("validateCaseDefinitionSubjectParameterPosition",
         "input->notEmpty() and input->first() = subjectParameter"
        ),
        ("validateCaseDefinitionOnlyOneObjective",
         "featureMembership-> selectByKind(ObjectiveMembership)-> size() <= 1"
        ),
        ("deriveCaseDefinitionActorParameter",
         "actorParameter = featureMembership-> selectByKind(ActorMembership). ownedActorParameter"
        ),
        ("validateCaseDefinitionOnlyOneSubject",
         "featureMembership->selectByKind(SubjectMembership)->size() <= 1"
        ),
        ("deriveCaseDefinitionObjectiveRequirement",
         "objectiveRequirement =      let objectives: OrderedSet(RequirementUsage) =          feat"
         "ureMembership->             selectByKind(ObjectiveMembership).             ownedRequirem"
         "ent in     if objectives->isEmpty() then null     else objectives->first().ownedObjectiv"
         "eRequirement     endif"
        ),
        ("deriveCaseDefinitionSubjectParameter",
         "subjectParameter =     let subjectMems : OrderedSet(SubjectMembership) =          featur"
         "eMembership->selectByKind(SubjectMembership) in     if subjectMems->isEmpty() then null "
         "    else subjectMems->first().ownedSubjectParameter     endif"
        ),
    )

class AnalysisCaseDefinition(CaseDefinition):
    """<p>An <code>AnalysisCaseDefinition</code> is a <code>CaseDefinition</code> for the case of carrying out an analysis.</p>"""
    _PKG = "AnalysisCases"
    _DECL = {
    # <p>An <code>Expression</code> used to compute the <code>result</code> of the <code>AnalysisCaseD
    # efinition</code>, owned via a <code>ResultExpressionMembership</code>.</p>
    'resultExpression': _Ref('resultExpression', "Expression", derived=True, assoc="Systems-AnalysisCases-A_resultExpression_analysisCaseDefintion"),
    }
    CONSTRAINTS = (
        ("deriveAnalysisCaseDefinitionResultExpression",
         "resultExpression =     let results : OrderedSet(ResultExpressionMembership) =         fe"
         "atureMembersip->             selectByKind(ResultExpressionMembership) in     if results-"
         ">isEmpty() then null     else results->first().ownedResultExpression     endif"
        ),
        ("checkAnalysisCaseDefinitionSpecialization",
         "specializesFromLibrary('AnalysisCases::AnalysisCase')"
        ),
    )

class Expression(Step):
    """<p>An <code>Expression</code> is a <code>Step</code> that is typed by a <code>Function</code>. An <code>Expression</code> that also has a <code>Function</code> as its <code>featuringType</code> is a computational step within that <code>Function</code>. An <code>Expression</code> always has a single <code>result</code> parameter, which redefines the <code>result</code> parameter of its defining <code>function</code>. This allows <code>Expressions</code> to be interconnected in tree structures, in which inputs to each <code>Expression</code> in the tree are determined as the results of other <code>Expression</code> in the tree.</p>"""
    _PKG = "Functions"
    _DECL = {
    # <p>The <code>Function</code> that types this <code>Expression</code>.</p>
    'function': _Ref('function', "Function", derived=True, redefines=("behavior",), assoc="Kernel-Functions-A_function_typedExpression"),
    # <p>Whether this <code>Expression</code> meets the constraints necessary to be evaluated at <em>m
    # odel level</em>, that is, using metadata within the model.</p>
    'isModelLevelEvaluable': _Ref('isModelLevelEvaluable', bool, derived=True),
    # <p><p>An <code>output</code> <code>parameter</code> of the <code>Expression</code> whose value i
    # s the result of the <code>Expression</code>. The result of an <code>Expression</code> is either 
    # inherited from its <code>function</code> or it is related to the <code>Expression</code> via a <
    # code>ReturnParameterMembership</code>, in which case it redefines the <code>result</code> <code>
    # parameter</code> of its <code>function</code>.</p>
    'result': _Ref('result', "Feature", derived=True, subsets=("output", "parameter",), assoc="Kernel-Functions-A_result_computingExpression"),
    }
    CONSTRAINTS = (
        ("validateExpressionResultParameterMembership",
         "featureMembership-> selectByKind(ReturnParameterMembership)-> size() = 1"
        ),
        ("deriveExpressionIsModelLevelEvaluable",
         "isModelLevelEvaluable = modelLevelEvaluable(Set(Element){})"
        ),
        ("deriveExpressionResult",
         "result =     let resultParams : Sequence(Feature) =         featureMemberships->        "
         "     selectByKind(ReturnParameterMembership).             ownedMemberParameter in     if"
         " resultParams->notEmpty() then resultParams->first()     else null     endif"
        ),
        ("checkExpressionResultBindingConnector",
         "ownedMembership.selectByKind(ResultExpressionMembership)->     forAll(mem | ownedFeature"
         ".selectByKind(BindingConnector)->         exists(binding |             binding.relatedFe"
         "ature->includes(result) and             binding.relatedFeature->includes(mem.ownedResult"
         "Expression.result)))"
        ),
        ("checkExpressionSpecialization",
         "specializesFromLibrary('Performances::evaluations')"
        ),
        ("checkExpressionTypeFeaturing",
         "owningMembership <> null and  owningMembership.oclIsKindOf(FeatureValue) implies     let"
         " featureWithValue : Feature =          owningMembership.oclAsType(FeatureValue).featureW"
         "ithValue in     featuringType = featureWithValue.featuringType"
        ),
        ("validateExpressionResultExpressionMembership",
         "membership->selectByKind(ResultExpressionMembership)->size() <= 1"
        ),
    )
    def modelLevelEvaluable(self, visited: None = None, arg: None = None) -> None:
        """
        <p>Return whether this <code>Expression</code> is model-level evaluable. The <code>visited</co
        de> parameter is used to track possible circular <code>Feature</code> references made from <co
        de>FeatureReferenceExpressions</code> (see the redefinition of this operation for <code>Featur
        eReferenceExpression</code>). Such circular references are not allowed in model-level evaluabl
        e expressions.</p> <p>An <code>Expression</code> that is not otherwise specialized is model-le
        vel evaluable if it has no (non-implied) <code>ownedSpecializations</code> and all its <code>o
        wnedFeatures</code> are either <code>in</code> parameters, the <code>result</code> <code>param
        eter</code> or a result <code>Expression</code> owned via a <code>ResultExpressionMembership</
        code>. The <code>parameters</code> must not have any <code>ownedFeatures</code> or a <code>Fea
        tureValue</code>, and the result <code>Expression</code> must be model-level evaluable.</p>
        [Expression operation; params: visited: ?, arg: ?; returns: nothing; stub - metamodel metadata
         only]
        """
        raise NotImplementedError
    def evaluate(self, target: None = None, result: None = None) -> None:
        """
        <p>If this <code>Expression</code> <code>isModelLevelEvaluable</code>, then evaluate it using 
        the <code>target</code> as the context <code>Element</code> for resolving <code>Feature</code>
         names and testing classification. The result is a collection of <code>Elements</code>, which,
         for a fully evaluable <code>Expression</code>, will be a <code>LiteralExpression</code> or a 
        <code>Feature</code> that is not an <code>Expression</code>.</p>
        [Expression operation; params: target: ?, result: ?; returns: nothing; stub - metamodel metada
        ta only]
        """
        raise NotImplementedError
    def checkCondition(self, target: None = None, arg: None = None) -> None:
        """
        <p>Model-level evaluate this <code>Expression</code> with the given <code>target</code>. If th
        e result is a <code>LiteralBoolean</code>, return its <code>value</code>. Otherwise return <co
        de>false</code>.</p>
        [Expression operation; params: target: ?, arg: ?; returns: nothing; stub - metamodel metadata 
        only]
        """
        raise NotImplementedError

class CalculationUsage(ActionUsage, Expression):
    """<p>A <code>CalculationUsage</code> is an <code>ActionUsage</code> that is also an <code>Expression</code>, and, so, is typed by a <code>Function</code>. Nominally, if the <code>type</code> is a <code>CalculationDefinition</code>, a <code>CalculationUsage</code> is a <code>Usage</code> of that <code>CalculationDefinition</code> within a system. However, other kinds of kernel <code>Functions</code> are also allowed, to permit use of <code>Functions</code> from the Kernel Model Libraries.</p>"""
    _PKG = "Calculations"
    _DECL = {
    # <p>The <ode>Function</code> that is the <code>type</code> of this <code>CalculationUsage</code>.
    #  Nominally, this would be a <code>CalculationDefinition</code>, but a kernel <code>Function</cod
    # e> is also allowed, to permit use of <code>Functions</code> from the Kernel Model Libraries.</p>
    'calculationDefinition': _Ref('calculationDefinition', "Function", derived=True, redefines=("actionDefinition",), assoc="Systems-Calculations-A_calculationDefinition_definedCalculation"),
    }
    CONSTRAINTS = (
        ("checkCalculationUsageSpecialization",
         "specializesFromLibrary('Calculations::calculations')"
        ),
        ("checkCalculationUsageSubcalculationSpecialization",
         "owningType <> null and (owningType.oclIsKindOf(CalculationDefinition) or  owningType.ocl"
         "IsKindOf(CalculationUsage)) implies     specializesFromLibrary('Calculations::Calculatio"
         "n::subcalculations')"
        ),
    )
    def modelLevelEvaluable(self, visited: None = None, arg: None = None) -> None:
        """
        <p>A <code>CalculationUsage</code> is not model-level evaluable.</p>
        [CalculationUsage operation; params: visited: ?, arg: ?; returns: nothing; stub - metamodel me
        tadata only]
        """
        raise NotImplementedError

class CaseUsage(CalculationUsage):
    """<p>A <code>CaseUsage</code> is a <code>Usage</code> of a <code>CaseDefinition</code>.</p>"""
    _PKG = "Cases"
    _DECL = {
    # <p>The <code>parameters</code> of this <code>CaseUsage</code> that represent actors involved in 
    # the case.</p>
    'actorParameter': _Ref('actorParameter', "PartUsage", derived=True, multi=True, lo=0, hi='*', subsets=("usage",), assoc="Systems-Cases-A_actorParameter_actorOwningCase"),
    # <p>The CaseDefinition that is the type of this CaseUsage.</p>
    'caseDefinition': _Ref('caseDefinition', "CaseDefinition", derived=True, redefines=("calculationDefinition",), assoc="Systems-Cases-A_definedCase_caseDefinition"),
    # <p>The <code>RequirementUsage</code> representing the objective of this <code>CaseUsage</code>.<
    # /p>
    'objectiveRequirement': _Ref('objectiveRequirement', "RequirementUsage", derived=True, subsets=("usage",), assoc="Systems-Cases-A_objectiveRequirement_objectiveOwningCase"),
    # <p>The <code>parameter</code> of this <code>CaseUsage</code> that represents its subject.</p>
    'subjectParameter': _Ref('subjectParameter', "Usage", derived=True, subsets=("usage",), assoc="Systems-Cases-A_subjectParameter_subjectOwningCase"),
    }
    CONSTRAINTS = (
        ("validateCaseUsageSubjectParameterPosition",
         "input->notEmpty() and input->first() = subjectParameter"
        ),
        ("deriveCaseUsageSubjectParameter",
         "subjectParameter =     let subjects : OrderedSet(SubjectMembership) =          featureMe"
         "mbership->selectByKind(SubjectMembership) in     if subjects->isEmpty() then null     el"
         "se subjects->first().ownedSubjectParameter     endif"
        ),
        ("checkCaseUsageSpecialization",
         "specializesFromLibrary('Cases::cases')"
        ),
        ("deriveCaseUsageActorParameter",
         "actorParameter = featureMembership-> selectByKind(ActorMembership). ownedActorParameter"
        ),
        ("deriveCaseUsageObjectiveRequirement",
         "objectiveRequirement =      let objectives: OrderedSet(RequirementUsage) =          feat"
         "ureMembership->             selectByKind(ObjectiveMembership).             ownedRequirem"
         "ent in     if objectives->isEmpty() then null     else objectives->first().ownedObjectiv"
         "eRequirement     endif"
        ),
        ("validateCaseUsageOnlyOneObjective",
         "featureMembership-> selectByKind(ObjectiveMembership)-> size() <= 1"
        ),
        ("validateCaseUsageOnlyOneSubject",
         "featureMembership-> selectByKind(SubjectMembership)-> size() <= 1"
        ),
        ("checkCaseUsageSubcaseSpecialization",
         "isComposite and owningType <> null and      (owningType.oclIsKindOf(CaseDefinition) or  "
         "    owningType.oclIsKindOf(CaseUsage)) implies     specializesFromLibrary('Cases::Case::"
         "subcases')"
        ),
    )

class AnalysisCaseUsage(CaseUsage):
    """<p>An <code>AnalysisCaseUsage</code> is a <code>Usage</code> of an <code>AnalysisCaseDefinition</code>.</p>"""
    _PKG = "AnalysisCases"
    _DECL = {
    # <p>The <code>AnalysisCaseDefinition</code> that is the <code>definition</code> of this <code>Ana
    # lysisCaseUsage</code>.</p>
    'analysisCaseDefinition': _Ref('analysisCaseDefinition', "AnalysisCaseDefinition", derived=True, redefines=("caseDefinition",), assoc="Systems-AnalysisCases-A_analysisCaseDefinition_definedAnalysisCase"),
    # <p>An <code>Expression</code> used to compute the <code>result</code> of the <code>AnalysisCaseU
    # sage</code>, owned via a <code>ResultExpressionMembership</code>.</p>
    'resultExpression': _Ref('resultExpression', "Expression", derived=True, assoc="Systems-AnalysisCases-A_resultExpression_analysisCase"),
    }
    CONSTRAINTS = (
        ("checkAnalysisCaseUsageSpecialization",
         "specializesFromLibrary('AnalysisCases::analysisCases')"
        ),
        ("deriveAnalysisCaseUsageResultExpression",
         "resultExpression =     let results : OrderedSet(ResultExpressionMembership) =         fe"
         "atureMembersip->             selectByKind(ResultExpressionMembership) in     if results-"
         ">isEmpty() then null     else results->first().ownedResultExpression     endif"
        ),
        ("checkAnalysisCaseUsageSubAnalysisCaseSpecialization",
         "isComposite and owningType <> null and     (owningType.oclIsKindOf(AnalysisCaseDefinitio"
         "n) or      owningType.oclIsKindOf(AnalysisCaseUsage)) implies     specializesFromLibrary"
         "('AnalysisCases::AnalysisCase::subAnalysisCases')"
        ),
    )

class AnnotatingElement(Element):
    """<p>An <code>AnnotatingElement</code> is an <code>Element</code> that provides additional description of or metadata on some other <code>Element</code>. An <code>AnnotatingElement</code> is either attached to its <code>annotatedElements</code> by <code>Annotation</code> <code>Relationships</code>, or it implicitly annotates its <code>owningNamespace</code>.</p>"""
    _PKG = "Annotations"
    _DECL = {
    # <p>The <code>Elements</code> that are annotated by this <code>AnnotatingElement</code>. If <code
    # >annotation</code> is not empty, these are the <code>annotatedElements</code> of the <code>annot
    # ations</code>. If <code>annotation</code> is empty, then it is the <code>owningNamespace</code> 
    # of the <code>AnnotatingElement</code>.</p>
    'annotatedElement': _Ref('annotatedElement', "Element", derived=True, multi=True, lo=1, hi='*', assoc="Root-Annotations-A_annotatedElement_annotatingElement"),
    # <p>The <code>Annotations</code> that relate this <code>AnnotatingElement</code> to its <code>ann
    # otatedElements</code>. This includes the <code>owningAnnotatingRelationship</code> (if any) foll
    # owed by all the <code>ownedAnnotatingRelationshps</code>.</p>
    'annotation': _Ref('annotation', "Annotation", derived=True, multi=True, lo=0, hi='*', assoc="Root-Annotations-A_annotation_annotatingElement"),
    # <p>The <code>ownedRelationships</code> of this <code>AnnotatingElement</code> that are <code>Ann
    # otations</code>, for which this <code>AnnotatingElement</code> is the <code>annotatingElement</c
    # ode>.</p>
    'ownedAnnotatingRelationship': _Ref('ownedAnnotatingRelationship', "Annotation", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("annotation", "ownedRelationship",), assoc="Root-Annotations-A_ownedAnnotatingRelationship_owningAnnotatingElement"),
    # <p>The <code>owningRelationship</code> of this <code>AnnotatingRelationship</code>, if it is an 
    # <code>Annotation</code></p>
    'owningAnnotatingRelationship': _Ref('owningAnnotatingRelationship', "Annotation", derived=True, subsets=("owningRelationship", "annotation",), assoc="Root-Annotations-A_ownedAnnotatingElement_owningAnnotatingRelationship"),
    }
    CONSTRAINTS = (
        ("deriveAnnotatingElementAnnotation",
         "annotation =      if owningAnnotatingRelationship = null then ownedAnnotatingRelationshi"
         "p     else owningAnnotatingRelationship->prepend(owningAnnotatingRelationship)     endif"
        ),
        ("deriveAnnotatingElementAnnotatedElement",
         "annotatedElement = if annotation->notEmpty() then annotation.annotatedElement else Seque"
         "nce{owningNamespace} endif"
        ),
        ("deriveAnnotatingElementOwnedAnnotatingRelationship",
         "ownedAnnotatingRelationship = ownedRelationship->     selectByKind(Annotation)->     sel"
         "ect(a | a.annotatedElement <> self)"
        ),
    )

class Annotation(Relationship):
    """<p>An <code>Annotation</code> is a Relationship between an <code>AnnotatingElement</code> and the <code>Element</code> that is annotated by that <code>AnnotatingElement</code>.</p>"""
    _PKG = "Annotations"
    _DECL = {
    # <p>The <code>Element</code> that is annotated by the <code>annotatingElement</code> of this Anno
    # tation.</p>
    'annotatedElement': _Ref('annotatedElement', "Element", redefines=("target",), assoc="Root-Annotations-A_annotatedElement_annotation"),
    # <p>The <code>AnnotatingElement</code> that annotates the <code>annotatedElement</code> of this <
    # code>Annotation</code>. This is always either the <code>ownedAnnotatingElement</code> or the <co
    # de>owningAnnotatingElement</code>.</p>
    'annotatingElement': _Ref('annotatingElement', "AnnotatingElement", derived=True, redefines=("source",), assoc="Root-Annotations-A_annotation_annotatingElement"),
    # <p>The <code>annotatingElement</code> of this <code>Annotation</code>, when it is an <code>owned
    # RelatedElement</code>.</p>
    'ownedAnnotatingElement': _Ref('ownedAnnotatingElement', "AnnotatingElement", derived=True, composite=True, subsets=("annotatingElement", "ownedRelatedElement",), assoc="Root-Annotations-A_ownedAnnotatingElement_owningAnnotatingRelationship"),
    # <p>The <code>annotatedElement</code> of this <code>Annotation</code>, when it is also the <code>
    # owningRelatedElement</code>.</p>
    'owningAnnotatedElement': _Ref('owningAnnotatedElement', "Element", derived=True, subsets=("annotatedElement", "owningRelatedElement",), assoc="Root-Elements-A_ownedAnnotation_owningAnnotatedElement"),
    # <p>The <code>annotatingElement</code> of this <code>Annotation</code>, when it is the <code>owni
    # ngRelatedElement</code>.</p>
    'owningAnnotatingElement': _Ref('owningAnnotatingElement', "AnnotatingElement", derived=True, subsets=("annotatingElement", "owningRelatedElement",), assoc="Root-Annotations-A_ownedAnnotatingRelationship_owningAnnotatingElement"),
    }
    CONSTRAINTS = (
        ("deriveAnnotationOwnedAnnotatingElement",
         "ownedAnnotatingElement =     let ownedAnnotatingElements : Sequence(AnnotatingElement) ="
         "          ownedRelatedElement->selectByKind(AnnotatingElement) in     if ownedAnnotating"
         "Elements->isEmpty() then null     else ownedAnnotatingElements->first()     endif"
        ),
        ("validateAnnotationAnnotatingElement",
         "ownedAnnotatingElement <> null xor owningAnnotatingElement <> null"
        ),
        ("validateAnnotationAnnotatedElementOwnership",
         "(owningAnnotatedElement <> null) = (ownedAnnotatingElement <> null)"
        ),
        ("deriveAnnotationAnnotatingElement",
         "annotatingElement = if ownedAnnotatingElement <> null then ownedAnnotatingElement else o"
         "wningAnnotatingElement endif"
        ),
    )

class BooleanExpression(Expression):
    """<p>A <code>BooleanExpression</code> is a <em><code>Boolean</code></em>-valued <code>Expression</code> whose type is a <code>Predicate</code>. It represents a logical condition resulting from the evaluation of the <code>Predicate</code>.</p>"""
    _PKG = "Functions"
    _DECL = {
    # <p>The Predicate that types the Expression.</p>
    'predicate': _Ref('predicate', "Predicate", derived=True, redefines=("function",), assoc="Kernel-Functions-A_predicate_typedBooleanExpression"),
    }
    CONSTRAINTS = (
        ("checkBooleanExpressionSpecialization",
         "specializesFromLibrary('Performances::booleanEvaluations')"
        ),
    )

class Invariant(BooleanExpression):
    """<p>An <code>Invariant</code> is a <code>BooleanExpression</code> that is asserted to have a specific <code><em>Boolean</em></code> result value. If <code>isNegated = false</code>, then the result is asserted to be true. If <code>isNegated = true</code>, then the result is asserted to be false.</p>"""
    _PKG = "Functions"
    _DECL = {
    # <p>Whether this <code>Invariant</code> is asserted to be false rather than true.</p>
    'isNegated': _Ref('isNegated', bool),
    }
    CONSTRAINTS = (
        ("checkInvariantSpecialization",
         "if isNegated then     specializesFromLibrary('Performances::falseEvaluations') else     "
         "specializesFromLibrary('Performances::trueEvaluations') endif"
        ),
    )

class ConstraintUsage(BooleanExpression, OccurrenceUsage):
    """<p>A <code>ConstraintUsage</code> is an <code>OccurrenceUsage</code> that is also a <code>BooleanExpression</code>, and, so, is typed by a <code>Predicate</code>. Nominally, if the type is a <code>ConstraintDefinition</code>, a <code>ConstraintUsage</code> is a <code>Usage</code> of that <code>ConstraintDefinition</code>. However, other kinds of kernel <code>Predicates</code> are also allowed, to permit use of <code>Predicates</code> from the Kernel Model Libraries.</p>"""
    _PKG = "Constraints"
    _DECL = {
    # <p>The (single) <code>Predicate</code> that is the type of this <code>ConstraintUsage</code>. No
    # minally, this will be a <code>ConstraintDefinition</code>, but other kinds of <code>Predicates</
    # code> are also allowed, to permit use of <code>Predicates</code> from the Kernel Model Libraries
    # .</p>
    'constraintDefinition': _Ref('constraintDefinition', "Predicate", derived=True, assoc="Systems-Constraints-A_constraintDefinition_definedConstraint"),
    }
    CONSTRAINTS = (
        ("checkConstraintUsageCheckedConstraintSpecialization",
         "owningType <> null and (owningType.oclIsKindOf(ItemDefinition) or  owningType.oclIsKindO"
         "f(ItemUsage)) implies     specializesFromLibrary('Items::Item::checkedConstraints')"
        ),
        ("checkConstraintUsageSpecialization",
         "specializesFromLibrary('Constraints::constraintChecks')"
        ),
        ("checkConstraintUsageRequirementConstraintSpecialization",
         "owningFeatureMembership <> null and owningFeatureMembership.oclIsKindOf(RequirementConst"
         "raintMembership) implies     if owningFeatureMembership.oclAsType(RequirementConstraintM"
         "embership).kind =          RequirementConstraintKind::assumption then         specialize"
         "sFromLibrary('Requirements::RequirementCheck::assumptions')     else         specializes"
         "FromLibrary('Requirements::RequirementCheck::constraints')     endif"
        ),
    )
    def namingFeature(self, arg: None = None) -> None:
        """
        <p>The naming <code>Feature</code> of a <code>ConstraintUsage</code> that is owned by a <code>
        RequirementConstraintMembership</code> and has an <code>ownedReferenceSubsetting</code> is the
         <code>featureTarget</code> of the <code>referencedFeature</code> of that <code>ownedReference
        Subsetting</code>.</p>
        [ConstraintUsage operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def modelLevelEvaluable(self, visited: None = None, arg: None = None) -> None:
        """
        <p>A <code>ConstraintUsage</code> is not model-level evaluable.</p>
        [ConstraintUsage operation; params: visited: ?, arg: ?; returns: nothing; stub - metamodel met
        adata only]
        """
        raise NotImplementedError

class AssertConstraintUsage(Invariant, ConstraintUsage):
    """<p>An <code>AssertConstraintUsage</code> is a <code>ConstraintUsage</code> that is also an <code>Invariant</code> and, so, is asserted to be true (by default). Unless it is the <code>AssertConstraintUsage</code> itself, the asserted <code>ConstraintUsage</code> is related to the <code>AssertConstraintUsage</code> by a ReferenceSubsetting <code>Relationship</code>.</p>"""
    _PKG = "Constraints"
    _DECL = {
    # <p>The <code>ConstraintUsage</code> to be performed by the <code>AssertConstraintUsage</code>. I
    # t is the <code>referenceFeature</code> of the <code>ownedReferenceSubsetting</code> for the <cod
    # e>AssertConstraintUsage</code>, if there is one, and, otherwise, the <code>AssertConstraintUsage
    # </code> itself.</p>
    'assertedConstraint': _Ref('assertedConstraint', "ConstraintUsage", derived=True, assoc="Systems-Constraints-A_assertedConstraint_constraintAssertion"),
    }
    CONSTRAINTS = (
        ("deriveAssertConstraintUsageAssertedConstraint",
         "assertedConstraint =     if referencedFeatureTarget() = null then self     else if refer"
         "encedFeatureTarget().oclIsKindOf(ConstraintUsage) then         referencedFeatureTarget()"
         ".oclAsType(ConstraintUsage)     else null     endif endif"
        ),
        ("checkAssertConstraintUsageSpecialization",
         "if isNegated then     specializesFromLibrary('Constraints::negatedConstraintChecks') els"
         "e     specializesFromLibrary('Constraints::assertedConstraintChecks') endif"
        ),
        ("validateAssertConstraintUsageReference",
         "referencedFeaureTarget() <> null implies referencedFeatureTarget().oclIsKindOf(Constrain"
         "tUsage)"
        ),
    )

class AssignmentActionUsage(ActionUsage):
    """<p>An <code>AssignmentActionUsage</code> is an <code>ActionUsage</code> that is defined, directly or indirectly, by the <code>ActionDefinition</code> <em><code>AssignmentAction</code></em> from the Systems Model Library. It specifies that the value of the <code>referent</code> <code>Feature</code>, relative to the target given by the result of the <code>targetArgument</code> <code>Expression</code>, should be set to the result of the <code>valueExpression</code>.</p>"""
    _PKG = "Actions"
    _DECL = {
    # <p>The <code>Feature</code> whose value is to be set.</p>
    'referent': _Ref('referent', "Feature", derived=True, assoc="Systems-Actions-A_referent_assignment"),
    # <p>The <code>Expression</code> whose value is an occurrence in the domain of the <code>referent<
    # /code> <code>Feature</code>, for which the value of the <code>referent</code> will be set to the
    #  result of the <code>valueExpression</code> by this <code>AssignmentActionUsage</code>.</p>
    'targetArgument': _Ref('targetArgument', "Expression", derived=True, assoc="Systems-Actions-A_targetArgument_assignmentAction"),
    # <p>The <code>Expression</code> whose result is to be assigned to the <code>referent</code> <code
    # >Feature</code>.</p>
    'valueExpression': _Ref('valueExpression', "Expression", derived=True, assoc="Systems-Actions-A_valueExpression_assigningAction"),
    }
    CONSTRAINTS = (
        ("checkAssignmentActionUsageAccessedFeatureRedefinition",
         "let targetParameter : Feature = inputParameter(1) in targetParameter <> null and targetP"
         "arameter.ownedFeature->notEmpty() and targetParameter->first().ownedFeature->notEmpty() "
         "and targetParameter->first().ownedFeature->first().     redefines('AssigmentAction::targ"
         "et::startingAt::accessedFeature')"
        ),
        ("checkAssignmentActionUsageStartingAtRedefinition",
         "let targetParameter : Feature = inputParameter(1) in targetParameter <> null and targetP"
         "arameter.ownedFeature->notEmpty() and targetParameter.ownedFeature->first().     redefin"
         "es('AssignmentAction::target::startingAt')"
        ),
        ("deriveAssignmentActionUsageValueExpression",
         "valueExpression = argument(2)"
        ),
        ("checkAssignmentActionUsageReferentRedefinition",
         "let targetParameter : Feature = inputParameter(1) in targetParameter <> null and targetP"
         "arameter.ownedFeature->notEmpty() and targetParameter->first().ownedFeature->notEmpty() "
         "and targetParameter->first().ownedFeature->first().redefines(referent)"
        ),
        ("validateAssignmentActionUsageReferent",
         "ownedMembership->exists( not oclIsKindOf(OwningMembership) and memberElement.oclIsKindOf"
         "(Feature))"
        ),
        ("validateAssignmentActionUsage",
         "referent <> null implies referent.featureTarget.mayTimeVary"
        ),
        ("deriveAssignmentUsageTargetArgument",
         "targetArgument = argument(1)"
        ),
        ("checkAssignmentActionUsageSubactionSpecialization",
         "isSubactionUsage() implies specializesFromLibrary('Actions::Action::assignments')"
        ),
        ("checkAssignmentActionUsageSpecialization",
         "specializesFromLibrary('Actions::assignmentActions')"
        ),
        ("deriveAssignmentActionUsageReferent",
         "referent =     let unownedFeatures : Sequence(Feature) = ownedMembership->         rejec"
         "t(oclIsKindOf(FeatureMembership)).memberElement->         selectByKind(Feature) in     i"
         "f unownedFeatures->isEmpty() then null     else unownedFeatures->first().oclAsType(Featu"
         "re)     endif"
        ),
    )

class DataType(Classifier):
    """<p>A <code>DataType</code> is a <code>Classifier</code> of things (in the universe) that can only be distinguished by how they are related to other things (via Features). This means multiple things classified by the same <code>DataType</code></p> <ul> <li>Cannot be distinguished when they are related to other things in exactly the same way, even when they are intended to be about different things.</li> <li>Can be distinguished when they are related to other things in different ways, even when they are intended to be about the same thing.</li> </ul>"""
    _PKG = "DataTypes"
    CONSTRAINTS = (
        ("validateDataTypeSpecialization",
         "ownedSpecialization.general-> forAll(not oclIsKindOf(Class) and not oclIsKindOf(Associat"
         "ion))"
        ),
        ("checkDataTypeSpecialization",
         "specializesFromLibrary('Base::DataValue')"
        ),
    )

class AttributeDefinition(DataType, Definition):
    """<p>An <code>AttributeDefinition</code> is a <code>Definition</code> and a <code>DataType</code> of information about a quality or characteristic of a system or part of a system that has no independent identity other than its value. All <code>features</code> of an <code>AttributeDefinition</code> must be referential (non-composite).</p> <p>As a <code>DataType</code>, an <code>AttributeDefinition</code> must specialize, directly or indirectly, the base <code>DataType</code> <code><em>Base::DataValue</em></code> from the Kernel Semantic Library.</p>"""
    _PKG = "Attributes"
    CONSTRAINTS = (
        ("validateAttributeDefinitionFeatures",
         "feature->forAll(not isComposite)"
        ),
    )

class AttributeUsage(Usage):
    """<p>An <code>AttributeUsage</code> is a <code>Usage</code> whose type is a <code>DataType</code>. Nominally, if the type is an <code>AttributeDefinition</code>, an <code>AttributeUsage</code> is a usage of a <code>AttributeDefinition</code> to represent the value of some system quality or characteristic. However, other kinds of kernel <code>DataTypes</code> are also allowed, to permit use of <code>DataTypes</code> from the Kernel Model Libraries. An <code>AttributeUsage</code> itself as well as all its nested <code>features</code> must be referential (non-composite).</p> <p>An <code>AttributeUsage</code> must specialize, directly or indirectly, the base <code>Feature</code> <code><em>Base::dataValues</em></code> from the Kernel Semantic Library.</p>"""
    _PKG = "Attributes"
    _DECL = {
    # <p>The <code>DataTypes</code> that are the types of this <code>AttributeUsage</code>. Nominally,
    #  these are <code>AttributeDefinitions</code>, but other kinds of kernel <code>DataTypes</code> a
    # re also allowed, to permit use of <code>DataTypes</code> from the Kernel Model Libraries.</p>
    'attributeDefinition': _Ref('attributeDefinition', "DataType", derived=True, multi=True, lo=0, hi='*', redefines=("definition",), assoc="Systems-Attributes-A_attributeDefinition_definedAttribute"),
    # <p>Always true for an <code>AttributeUsage</code>.</p>
    'isReference': _Ref('isReference', bool, derived=True, redefines=("isReference",)),
    }
    CONSTRAINTS = (
        ("validateAttributeUsageIsReference",
         "isReference"
        ),
        ("checkAttributeUsageSpecialization",
         "specializesFromLibrary('Base::dataValues')"
        ),
        ("validateAttributeUsageFeatures",
         "feature->forAll(not isComposite)"
        ),
    )

class BindingConnector(Connector):
    """<p>A <code>BindingConnector</code> is a binary <code>Connector</code> that requires its <code>relatedFeatures</code> to identify the same things (have the same values).</p>"""
    _PKG = "Connectors"
    CONSTRAINTS = (
        ("validateBindingConnectorIsBinary",
         "relatedFeature->size() = 2"
        ),
        ("checkBindingConnectorSpecialization",
         "specializesFromLibrary('Links::selfLinks')"
        ),
    )

class BindingConnectorAsUsage(BindingConnector, ConnectorAsUsage):
    """<p>A <code>BindingConnectorAsUsage</code> is both a <code>BindingConnector</code> and a <code>ConnectorAsUsage</code>.</p>"""
    _PKG = "Connections"

class InstantiationExpression(Expression):
    """<p>An <code>InstantiationExpression</code> is an <code>Expression</code> that instantiates its <code>instantiatedType</code>, binding some or all of the <code>features</code> of that <code>Type</code> to the <code>results</code> of its <code>arguments</code>.</p> <p><code>InstantiationExpression</code> is abstract, with concrete subclasses <code>InvocationExpression</code> and <code>ConstructorExpression</code>.</p>"""
    _PKG = "Expressions"
    _DECL = {
    # <p>The <code>Expressions</code> whose <code>results</code> are bound to <code>features</code> of
    #  the <code>instantiatedType</code>. The <code>arguments</code> are ordered consistent with the o
    # rder of the <code>features</code>, though they may not be one-to-one with all the <code>features
    # </code>.</p> <p><strong>Note.</strong> The derivation of <code>argument</code> is given in the c
    # oncrete subclasses of <code>InstantiationExpression</code>.</p>
    'argument': _Ref('argument', "Expression", derived=True, multi=True, lo=0, hi='*', assoc="Kernel-Expressions-A_argument_instantiation"),
    # <p>The <code>Type</code> that is being instantiated.</p>
    'instantiatedType': _Ref('instantiatedType', "Type", derived=True, subsets=("member",), assoc="Kernel-Expressions-A_instantiatedType_instantiationExpression"),
    }
    CONSTRAINTS = (
        ("deriveInstantiationExpressionInstantiatedType",
         "instantiatedType = instantiatedType()"
        ),
        ("validateInstantiationExpressionResult",
         "result.owningType = self"
        ),
        ("validateInstantiationExpressionInstantiatedType",
         "instantiatedType() <> null"
        ),
    )
    def instantiatedType(self, arg: None = None) -> None:
        """
        <p>Return the <code>Type</code> to act as the <code>instantiatedType</code> for this <code>Ins
        tantiationExpression</code>. By default, this is the <code>memberElement</code> of the first <
        code>ownedMembership</code> that is not a <code>FeatureMembership</code>, which must be a <cod
        e>Type</code>.</p> <p><b>Note.</b> This operation is overridden in the subclass <code>Operator
        Expression</code>.</p>
        [InstantiationExpression operation; params: arg: ?; returns: nothing; stub - metamodel metadat
        a only]
        """
        raise NotImplementedError

class InvocationExpression(InstantiationExpression):
    """<p>An <code>InvocationExpression</code> is an <code>InstantiationExpression</code> whose <code>instantiatedType</code> must be a <code>Behavior</code> or a <code>Feature</code> typed by a single <code>Behavior</code> (such as a <code>Step</code>). Each of the input <code>parameters</code> of the <code>instantiatedType</code> are bound to the <code>result</code> of an <code>argument</code> <code>Expression</code>. If the <code>instantiatedType</code> is a <code>Function</code> or a <code>Feature</code> typed by a <code>Function</code>, then the <code>result</code> of the <code>InvocationExpression</code> is the <code>result</code> of the invoked <code>Function</code>. Otherwise, the <code>result</code> is an instance of the <code>instantiatedType</code> (essentially like a behavioral <code>ConstructorExpression</code>).</p>"""
    _PKG = "Expressions"
    CONSTRAINTS = (
        ("validateInvocationExpressionParameterRedefinition",
         "let parameters : OrderedSet(Feature) = instantiatedType.input in input->forAll(inp |    "
         "  inp.ownedRedefinition.redefinedFeature->         intersection(parameters)->size() = 1)"
        ),
        ("checkInvocationExpressionBehaviorResultSpecialization",
         "not instantiatedType.oclIsKindOf(Function) and not (instantiatedType.oclIsKindOf(Feature"
         ") and       instantiatedType.oclAsType(Feature).type->exists(oclIsKindOf(Function))) imp"
         "lies     result.specializes(instantiatedType)"
        ),
        ("validateInvocationExpressionNoDuplicateParameterRedefinition",
         "let features : OrderedSet(Feature) = instantiatedType.feature in input->forAll(inp1 | in"
         "put->forAll(inp2 |     inp1 <> inp2 implies         inp1.ownedRedefinition.redefinedFeat"
         "ure->             intersection(inp2.ownedRedefinition.redefinedFeature)->             in"
         "tersection(features)->isEmpty()))"
        ),
        ("checkInvocationExpressionSpecialization",
         "specializes(instantiatedType)"
        ),
        ("deriveInvocationExpressionArgument",
         "instantiatedType.input->collect(inp |      ownedFeatures->select(redefines(inp)).valuati"
         "on->     select(v | v <> null).value )"
        ),
        ("checkInvocationExpressionBehaviorBindingConnector",
         "not instantiatedType.oclIsKindOf(Function) and not (instantiatedType.oclIsKindOf(Feature"
         ") and       instantiatedType.oclAsType(Feature).type->exists(oclIsKindOf(Function))) imp"
         "lies     ownedFeature.selectByKind(BindingConnector)->exists(         relatedFeature->in"
         "cludes(self) and         relatedFeature->includes(result))"
        ),
        ("validateInvocationExpressionOwnedFeatures",
         "ownedFeature->forAll(f | f <> result implies f.direction = FeatureDirectionKind::_'in')"
        ),
        ("checkInvocationExpressionDefaultValueBindingConnector",
         "TBD"
        ),
        ("validateInvocationExpressionInstantiatedType",
         "instantiatedType.oclIsKindOf(Behavior) or instantiatedType.oclIsKindOf(Feature) and     "
         "instantiatedType.type->exists(oclIsKindOf(Behavior)) and     instantiatedType.type->size"
         "(1)"
        ),
    )
    def modelLevelEvaluable(self, arg: None = None, visited: None = None) -> None:
        """
        <p>An <code>InvocationExpression</code> is model-level evaluable if all its <code>argument</co
        de> <code>Expressions</code> are model-level evaluable and its <code>function</code> is model-
        level evaluable.</p>
        [InvocationExpression operation; params: arg: ?, visited: ?; returns: nothing; stub - metamode
        l metadata only]
        """
        raise NotImplementedError
    def evaluate(self, target: None = None, result: None = None) -> None:
        """
        <p>Apply the <code>Function</code> that is the <code>type</code> of this <code>InvocationExpre
        ssion</code> to the argument values resulting from evaluating each of the <code>argument</code
        > <code>Expressions</code> on the given <code>target</code>. If the application is not possibl
        e, then return an empty sequence.</p>
        [InvocationExpression operation; params: target: ?, result: ?; returns: nothing; stub - metamo
        del metadata only]
        """
        raise NotImplementedError

class OperatorExpression(InvocationExpression):
    """<p>An <code>OperatorExpression</code> is an <code>InvocationExpression</code> whose <code>function</code> is determined by resolving its <code>operator</code> in the context of one of the standard packages from the Kernel Function Library.</p>"""
    _PKG = "Expressions"
    _DECL = {
    # <p>An <code>operator</code> symbol that names a corresponding <code>Function</code> from one of 
    # the standard packages from the Kernel Function Library .</p>
    'operator': _Ref('operator', str),
    }
    def instantiatedType(self, arg: None = None) -> None:
        """
        <p>The <code>instantiatedType</code> of an <code>OperatorExpression</code> is the resolution o
        f it's <code>operator</code> from one of the packages <em><code>BaseFunctions</code></em>, <em
        ><code>DataFunctions</code></em>, or <em><code>ControlFunctions</code></em> from the Kernel Fu
        nction Library.</p>
        [OperatorExpression operation; params: arg: ?; returns: nothing; stub - metamodel metadata onl
        y]
        """
        raise NotImplementedError

class CollectExpression(OperatorExpression):
    """<p>A <code>CollectExpression</code> is an <code>OperatorExpression</code> whose <code>operator</code> is <code>"collect"</code>, which resolves to the <code>Function</code> <em><code>ControlFunctions::collect</code></em> from the Kernel Functions Library.</p>"""
    _PKG = "Expressions"
    _DECL = {
    'operator': _Ref('operator', str, redefines=("operator",)),
    }
    CONSTRAINTS = (
        ("validateCollectExpressionOperator",
         "operator = 'collect'"
        ),
    )

class Comment(AnnotatingElement):
    """<p>A <code>Comment</code> is an <code>AnnotatingElement</code> whose <code>body</code> in some way describes its <code>annotatedElements</code>.</p>"""
    _PKG = "Annotations"
    _DECL = {
    # <p>The annotation text for the <code>Comment</code>.</p>
    'body': _Ref('body', str),
    # <p>Identification of the language of the <code>body</code> text and, optionally, the region and/
    # or encoding. The format shall be a POSIX locale conformant to ISO/IEC 15897, with the format <co
    # de>[language[_territory][.codeset][@modifier]]</code>.</p>
    'locale': _Ref('locale', str),
    }

class Predicate(Function):
    """<p>A <code>Predicate</code> is a <code>Function</code> whose <code>result</code> <code>parameter</code> has type <code><em>Boolean</em></code> and multiplicity <code>1..1</code>.</p>"""
    _PKG = "Functions"
    CONSTRAINTS = (
        ("checkPredicateSpecialization",
         "specializesFromLibrary('Performances::BooleanEvaluation')"
        ),
    )

class ConstraintDefinition(Predicate, OccurrenceDefinition):
    """<p>A <code>ConstraintDefinition</code> is an <code>OccurrenceDefinition</code> that is also a <code>Predicate</code> that defines a constraint that may be asserted to hold on a system or part of a system.</p>"""
    _PKG = "Constraints"
    CONSTRAINTS = (
        ("checkConstraintDefinitionSpecialization",
         "specializesFromLibrary('Constraints::ConstraintCheck')"
        ),
    )

class RequirementDefinition(ConstraintDefinition):
    """<p>A <code>RequirementDefinition</code> is a <code>ConstraintDefinition</code> that defines a requirement used in the context of a specification as a constraint that a valid solution must satisfy. The specification is relative to a specified subject, possibly in collaboration with one or more external actors.</p>"""
    _PKG = "Requirements"
    _DECL = {
    # <p>The <code>parameters</code> of this <code>RequirementDefinition</code> that represent actors 
    # involved in the requirement.</p>
    'actorParameter': _Ref('actorParameter', "PartUsage", derived=True, multi=True, lo=0, hi='*', subsets=("usage",), assoc="Systems-Requirements-A_actorParameter_actorOwningRequirementDefinition"),
    # <p>The owned <code>ConstraintUsages</code> that represent assumptions of this <code>RequirementD
    # efinition</code>, which are the <code>ownedConstraints</code> of the <code>RequirementConstraint
    # Memberships</code> of the <code>RequirementDefinition</code> with <code>kind = assumption</code>
    # .</p>
    'assumedConstraint': _Ref('assumedConstraint', "ConstraintUsage", derived=True, multi=True, lo=0, hi='*', assoc="Systems-Requirements-A_assumedConstraint_assumingRequirementDefinition"),
    # <p>The <code>ConcernUsages</code> framed by this <code>RequirementDefinition</code>, which are t
    # he <code>ownedConcerns</code> of all <code>FramedConcernMemberships</code> of the <code>Requirem
    # entDefinition</code>.</p>
    'framedConcern': _Ref('framedConcern', "ConcernUsage", derived=True, multi=True, lo=0, hi='*', subsets=("requiredConstraint",), assoc="Systems-Requirements-A_framedConcern_framingRequirementDefinition"),
    # <p>An optional modeler-specified identifier for this <code>RequirementDefinition</code> (used, e
    # .g., to link it to an original requirement text in some source document), which is the <code>dec
    # laredShortName</code> for the <code>RequirementDefinition</code>.</p>
    'reqId': _Ref('reqId', str),
    # <p>The owned <code>ConstraintUsages</code> that represent requirements of this <code>Requirement
    # Definition</code>, derived as the <code>ownedConstraints</code> of the <code>RequirementConstrai
    # ntMemberships</code> of the <code>RequirementDefinition</code> with <code>kind</code> = <code>re
    # quirement</code>.</p>
    'requiredConstraint': _Ref('requiredConstraint', "ConstraintUsage", derived=True, multi=True, lo=0, hi='*', assoc="Systems-Requirements-A_requiredConstraint_requiringRequirementDefinition"),
    # <p>The <code>parameters</code> of this <code>RequirementDefinition</code> that represent stakeho
    # lders for th requirement.</p>
    'stakeholderParameter': _Ref('stakeholderParameter', "PartUsage", derived=True, multi=True, lo=0, hi='*', subsets=("usage",), assoc="Systems-Requirements-A_stakeholderParameter_stakholderOwiningRequirementDefinition"),
    # <p>The <code>parameter</code> of this <code>RequirementDefinition</code> that represents its sub
    # ject.</p>
    'subjectParameter': _Ref('subjectParameter', "Usage", derived=True, subsets=("usage",), assoc="Systems-Requirements-A_subjectParameter_subjectOwningRequirementDefinition"),
    # <p>An optional textual statement of the requirement represented by this <code>RequirementDefinit
    # ion</code>, derived from the <code>bodies</code> of the <code>documentation</code> of the <code>
    # RequirementDefinition</code>.</p>
    'text': _Ref('text', str, derived=True, multi=True, lo=0, hi='*'),
    }
    CONSTRAINTS = (
        ("deriveRequirementDefinitionSubjectParameter",
         "subjectParameter =     let subjects : OrderedSet(SubjectMembership) =          featureMe"
         "mbership->selectByKind(SubjectMembership) in     if subjects->isEmpty() then null     el"
         "se subjects->first().ownedSubjectParameter     endif"
        ),
        ("validateRequirementDefinitionOnlyOneSubject",
         "featureMembership-> selectByKind(SubjectMembership)-> size() <= 1"
        ),
        ("validateRequirementDefinitionSubjectParameterPosition",
         "input->notEmpty() and input->first() = subjectParameter"
        ),
        ("deriveRequirementDefinitionText",
         "text = documentation.body"
        ),
        ("deriveRequirementDefinitionActorParameter",
         "actorParameter = featureMembership-> selectByKind(ActorMembership). ownedActorParameter"
        ),
        ("deriveRequirementDefinitionRequiredConstraint",
         "requiredConstraint = ownedFeatureMembership->     selectByKind(RequirementConstraintMemb"
         "ership)->     select(kind = RequirementConstraintKind::requirement).     ownedConstraint"
        ),
        ("deriveRequirementDefinitionAssumedConstraint",
         "assumedConstraint = ownedFeatureMembership->     selectByKind(RequirementConstraintMembe"
         "rship)->     select(kind = RequirementConstraintKind::assumption).     ownedConstraint"
        ),
        ("checkRequirementDefinitionSpecialization",
         "specializesFromLibrary('Requirements::RequirementCheck')"
        ),
        ("deriveRequirementDefinitionFramedConcern",
         "framedConcern = featureMembership-> selectByKind(FramedConcernMembership). ownedConcern"
        ),
        ("deriveRequirementDefinitionStakeholderParameter",
         "stakeholderParameter = featureMembership->     selectByKind(StakholderMembership).     o"
         "wnedStakeholderParameter"
        ),
    )

class ConcernDefinition(RequirementDefinition):
    """<p>A <code>ConcernDefinition</code> is a <code>RequirementDefinition</code> that one or more stakeholders may be interested in having addressed. These stakeholders are identified by the <code>ownedStakeholders</code>of the <code>ConcernDefinition</code>.</p>"""
    _PKG = "Requirements"
    CONSTRAINTS = (
        ("checkConcernDefinitionSpecialization",
         "specializesFromLibrary('Requirements::ConcernCheck')"
        ),
    )

class RequirementUsage(ConstraintUsage):
    """<p>A <code>RequirementUsage</code> is a <code>Usage</code> of a <code>RequirementDefinition</code>.</p>"""
    _PKG = "Requirements"
    _DECL = {
    # <p>The <code>parameters</code> of this <code>RequirementUsage</code> that represent actors invol
    # ved in the requirement.</p>
    'actorParameter': _Ref('actorParameter', "PartUsage", derived=True, multi=True, lo=0, hi='*', subsets=("usage",), assoc="Systems-Requirements-A_actorParameter_actorOwningRequirement"),
    # <p>The owned <code>ConstraintUsages</code> that represent assumptions of this <code>RequirementU
    # sage</code>, derived as the <code>ownedConstraints</code> of the <code>RequirementConstraintMemb
    # erships</code> of the <code>RequirementUsage</code> with <code>kind</code> = <code>assumption</c
    # ode>.</p>
    'assumedConstraint': _Ref('assumedConstraint', "ConstraintUsage", derived=True, multi=True, lo=0, hi='*', assoc="Systems-Requirements-A_assumedConstraint_assumingRequirement"),
    # <p>The <code>ConcernUsages</code> framed by this <code>RequirementUsage</code>, which are the <c
    # ode>ownedConcerns</code> of all <code>FramedConcernMemberships</code> of the <code>RequirementUs
    # age</code>.</p>
    'framedConcern': _Ref('framedConcern', "ConcernUsage", derived=True, multi=True, lo=0, hi='*', subsets=("requiredConstraint",), assoc="Systems-Requirements-A_framedConcern_framingRequirement"),
    # <p>An optional modeler-specified identifier for this <code>RequirementUsage</code> (used, e.g., 
    # to link it to an original requirement text in some source document), which is the <code>declared
    # ShortName</code> for the <code>RequirementUsage</code>.</p>
    'reqId': _Ref('reqId', str),
    # <p>The owned <code>ConstraintUsages</code> that represent requirements of this <code>Requirement
    # Usage</code>, which are the <code>ownedConstraints</code> of the <code>RequirementConstraintMemb
    # erships</code> of the <code>RequirementUsage</code> with <code>kind</code> = <code>requirement</
    # code>.</p>
    'requiredConstraint': _Ref('requiredConstraint', "ConstraintUsage", derived=True, multi=True, lo=0, hi='*', assoc="Systems-Requirements-A_requiredConstraint_requiringRequirement"),
    # <p>The <code>RequirementDefinition</code> that is the single <code>definition</code> of this <co
    # de>RequirementUsage</code>.</p>
    'requirementDefinition': _Ref('requirementDefinition', "RequirementDefinition", derived=True, redefines=("constraintDefinition",), assoc="Systems-Requirements-A_requirementDefinition_definedRequirement"),
    # <p>The <code>parameters</code> of this <code>RequirementUsage</code> that represent stakeholders
    #  for the requirement.</p>
    'stakeholderParameter': _Ref('stakeholderParameter', "PartUsage", derived=True, multi=True, lo=0, hi='*', subsets=("usage",), assoc="Systems-Requirements-A_stakeholderParameter_stakholderOwningRequirement"),
    # <p>The <code>parameter</code> of this <code>RequirementUsage</code> that represents its subject.
    # </p>
    'subjectParameter': _Ref('subjectParameter', "Usage", derived=True, subsets=("usage",), assoc="Systems-Requirements-A_subjectParameter_subjectOwningRequirement"),
    # <p>An optional textual statement of the requirement represented by this <code>RequirementUsage</
    # code>, derived from the <code>bodies<code> of the <code>documentation</code> of the <code>Requir
    # ementUsage</code>.</p>
    'text': _Ref('text', str, derived=True, multi=True, lo=0, hi='*'),
    }
    CONSTRAINTS = (
        ("checkRequirementUsageSubrequirementSpecialization",
         "isComposite and owningType <> null and     (owningType.oclIsKindOf(RequirementDefinition"
         ") or      owningType.oclIsKindOf(RequirementUsage)) implies     specializesFromLibrary('"
         "Requirements::RequirementCheck::subrequirements')"
        ),
        ("checkRequirementUsageObjectiveRedefinition",
         "owningfeatureMembership <> null and owningfeatureMembership.oclIsKindOf(ObjectiveMembers"
         "hip) implies     owningType.ownedSpecialization.general->forAll(gen |         (gen.oclIs"
         "KindOf(CaseDefinition) implies             redefines(gen.oclAsType(CaseDefinition).objec"
         "tiveRequirement)) and         (gen.oclIsKindOf(CaseUsage) implies             redefines("
         "gen.oclAsType(CaseUsage).objectiveRequirement))"
        ),
        ("deriveRequirementUsageRequiredConstraint",
         "requiredConstraint = ownedFeatureMembership->     selectByKind(RequirementConstraintMemb"
         "ership)->     select(kind = RequirementConstraintKind::requirement).     ownedConstraint"
        ),
        ("deriveRequirementUsageActorParameter",
         "actorParameter = featureMembership-> selectByKind(ActorMembership). ownedActorParameter"
        ),
        ("deriveRequirementUsageStakeholderParameter",
         "stakeholderParameter = featureMembership-> selectByKind(AStakholderMembership). ownedSta"
         "keholderParameter"
        ),
        ("validateRequirementUsageSubjectParameterPosition",
         "input->notEmpty() and input->first() = subjectParameter"
        ),
        ("deriveRequirementUsageFramedConcern",
         "framedConcern = featureMembership-> selectByKind(FramedConcernMembership). ownedConcern"
        ),
        ("deriveRequirementUsageSubjectParameter",
         "subjectParameter =     let subjects : OrderedSet(SubjectMembership) =          featureMe"
         "mbership->selectByKind(SubjectMembership) in     if subjects->isEmpty() then null     el"
         "se subjects->first().ownedSubjectParameter     endif"
        ),
        ("deriveRequirementUsageText",
         "text = documentation.body"
        ),
        ("checkRequirementUsageSpecialization",
         "specializesFromLibrary('Requirements::requirementChecks')"
        ),
        ("checkRequirementUsageRequirementVerificationSpecialization",
         "owningFeatureMembership <> null and owningFeatureMembership.oclIsKindOf(RequirementVerif"
         "icationMembership) implies     specializesFromLibrary('VerificationCases::VerificationCa"
         "se::obj::requirementVerifications')"
        ),
        ("deriveRequirementUsageAssumedConstraint",
         "assumedConstraint = ownedFeatureMembership->     selectByKind(RequirementConstraintMembe"
         "rship)->     select(kind = RequirementConstraintKind::assumption).     ownedConstraint"
        ),
        ("validateRequirementUsageOnlyOneSubject",
         "featureMembership-> selectByKind(SubjectMembership)-> size() <= 1"
        ),
    )

class ConcernUsage(RequirementUsage):
    """<p>A <code>ConcernUsage</code> is a <code>Usage</code> of a <code>ConcernDefinition</code>.</p> The <code>ownedStakeholder</code> features of the ConcernUsage shall all subset the <em><code>ConcernCheck::concernedStakeholders</code> </em>feature. If the ConcernUsage is an <code>ownedFeature</code> of a StakeholderDefinition or StakeholderUsage, then the ConcernUsage shall have an <code>ownedStakeholder</code> feature that is bound to the <em><code>self</code></em> feature of its owner.</p>"""
    _PKG = "Requirements"
    _DECL = {
    # <p>The ConcernDefinition that is the single type of this ConcernUsage.</p>
    'concernDefinition': _Ref('concernDefinition', "ConcernDefinition", derived=True, redefines=("requirementDefinition",), assoc="Systems-Requirements-A_concernDefinition_definedConcern"),
    }
    CONSTRAINTS = (
        ("checkConcernUsageSpecialization",
         "specializesFromLibrary('Requirements::concernChecks')"
        ),
        ("checkConcernUsageFramedConcernSpecialization",
         "owningFeatureMembership <> null and owningFeatureMembership.oclIsKindOf(FramedConcernMem"
         "bership) implies     specializesFromLibrary('Requirements::RequirementCheck::concerns')"
        ),
    )

class PortDefinition(Structure, OccurrenceDefinition):
    """<p>A <code>PortDefinition</code> defines a point at which external entities can connect to and interact with a system or part of a system. Any <code>ownedUsages</code> of a <code>PortDefinition</code>, other than <code>PortUsages</code>, must not be composite.</p>"""
    _PKG = "Ports"
    _DECL = {
    # <p>The <codeConjugatedPortDefinition</code> that is conjugate to this <code>PortDefinition</code
    # >.</p>
    'conjugatedPortDefinition': _Ref('conjugatedPortDefinition', "ConjugatedPortDefinition", derived=True, assoc="Systems-Ports-A_conjugatedPortDefinition_originalPortDefinition"),
    }
    CONSTRAINTS = (
        ("validatePortDefinitionOwnedUsagesNotComposite",
         "ownedUsage-> reject(oclIsKindOf(PortUsage))-> forAll(not isComposite)"
        ),
        ("validatePortDefinitionConjugatedPortDefinition",
         "not oclIsKindOf(ConjugatedPortDefinition) implies     ownedMember->         selectByKind"
         "(ConjugatedPortDefinition)->         size() = 1"
        ),
        ("derivePortDefinitionConjugatedPortDefinition",
         "conjugatedPortDefinition =  let conjugatedPortDefinitions : OrderedSet(ConjugatedPortDef"
         "inition) =     ownedMember->selectByKind(ConjugatedPortDefinition) in if conjugatedPortD"
         "efinitions->isEmpty() then null else conjugatedPortDefinitions->first() endif"
        ),
        ("checkPortDefinitionSpecialization",
         "specializesFromLibrary('Ports::Port')"
        ),
    )

class ConjugatedPortDefinition(PortDefinition):
    """<p>A <code>ConjugatedPortDefinition</code> is a <code>PortDefinition</code> that is a <code>PortDefinition</code> of its original <code>PortDefinition</code>. That is, a <code>ConjugatedPortDefinition</code> inherits all the <code>features</code> of the original <code>PortDefinition</code>, but input <code>flows</code> of the original <code>PortDefinition</code> become outputs on the <code>ConjugatedPortDefinition</code> and output <code>flows</code> of the original <code>PortDefinition</code> become inputs on the <code>ConjugatedPortDefinition</code>. Every <code>PortDefinition</code> (that is not itself a <code><code>ConjugatedPortDefinition</code></code>) has exactly one corresponding <code>ConjugatedPortDefinition</code>, whose effective name is the name of the <code>originalPortDefinition</code>, with the character <code>~</code> prepended.</p>"""
    _PKG = "Ports"
    _DECL = {
    # <p>The original <code>PortDefinition</code> for this <code>ConjugatedPortDefinition</code>, whic
    # h is the <code>owningNamespace</code> of the <code>ConjugatedPortDefinition</code>.</p>
    'originalPortDefinition': _Ref('originalPortDefinition', "PortDefinition", derived=True, assoc="Systems-Ports-A_conjugatedPortDefinition_originalPortDefinition"),
    # <p>The <code>PortConjugation</code> that is the <code>ownedConjugator</code> of this <code>Conju
    # gatedPortDefinition</code>, linking it to its <code>originalPortDefinition</code>.</p>
    'ownedPortConjugator': _Ref('ownedPortConjugator', "PortConjugation", derived=True, composite=True, assoc="Systems-Ports-A_conjugatedPortDefinition_ownedPortConjugator"),
    }
    CONSTRAINTS = (
        ("validateConjugatedPortDefinitionConjugatedPortDefinitionIsEmpty",
         "conjugatedPortDefinition = null"
        ),
        ("validateConjugatedPortDefinitionOriginalPortDefinition",
         "ownedPortConjugator.originalPortDefinition = originalPortDefinition"
        ),
    )
    def effectiveName(self, arg: None = None) -> None:
        """
        <p>If the <code>name</code> of the <code>originalPortDefinition</code> is non-empty, then retu
        rn that with the character <code>~</code> prepended.</p>
        [ConjugatedPortDefinition operation; params: arg: ?; returns: nothing; stub - metamodel metada
        ta only]
        """
        raise NotImplementedError

class Specialization(Relationship):
    """<p><code>Specialization</code> is a <code>Relationship</code> between two <code>Types</code> that requires all instances of the <code>specific</code> type to also be instances of the <code>general</code> Type (i.e., the set of instances of the <code>specific</code> Type is a <em>subset</em> of those of the <code>general</code> Type, which might be the same set).</p>"""
    _PKG = "Types"
    _DECL = {
    # <p>A <code>Type</code> with a superset of all instances of the <code>specific</code> <code>Type<
    # /code>, which might be the same set.</p>
    'general': _Ref('general', "Type", redefines=("target",), assoc="Core-Types-A_general_generalization"),
    # <p>The <code>Type</code> that is the <code>specific</code> <code>Type</code> of this <code>Speci
    # alization</code> and owns it as its <code>owningRelatedElement</code>.</p>
    'owningType': _Ref('owningType', "Type", subsets=("owningRelatedElement", "specific",), assoc="Core-Types-A_ownedSpecialization_owningType"),
    # <p>A <code>Type</code> with a subset of all instances of the <code>general</code> <code>Type</co
    # de>, which might be the same set.</p>
    'specific': _Ref('specific', "Type", redefines=("source",), assoc="Core-Types-A_specific_specialization"),
    }
    CONSTRAINTS = (
        ("validateSpecificationSpecificNotConjugated",
         "not specific.isConjugated"
        ),
    )

class FeatureTyping(Specialization):
    """<p><code>FeatureTyping</code> is <code>Specialization</code> in which the <code>specific</code> <code>Type</code> is a <code>Feature</code>. This means the set of instances of the (specific) <code>typedFeature</code> is a subset of the set of instances of the (general) <code>type</code>. In the simplest case, the <code>type</code> is a <code>Classifier</code>, whereupon the <code>typedFeature</code> has values that are instances of the <code>Classifier</code>.</p>"""
    _PKG = "Features"
    _DECL = {
    # <p>A <code>typedFeature</code> that is also the <code>owningRelatedElement</code> of this <code>
    # FeatureTyping</code>.</p>
    'owningFeature': _Ref('owningFeature', "Feature", subsets=("typedFeature",), redefines=("owningType",), assoc="Core-Features-A_ownedTyping_owningFeature"),
    # <p>The <code>Type</code> that is being applied by this <code>FeatureTyping</code>.</p>
    'type': _Ref('type', "Type", redefines=("general",), assoc="Core-Features-A_type_typingByType"),
    # <p>The <code>Feature</code> that has a <code>type</code> determined by this <code>FeatureTyping<
    # /code>.</p>
    'typedFeature': _Ref('typedFeature', "Feature", redefines=("specific",), assoc="Core-Features-A_typing_typedFeature"),
    }

class ConjugatedPortTyping(FeatureTyping):
    """<p>A <code>ConjugatedPortTyping</code> is a <code>FeatureTyping</code> whose <code>type</code> is a <code>ConjugatedPortDefinition</code>. (This relationship is intended to be an abstract-syntax marker for a special surface notation for conjugated typing of ports.)</p>"""
    _PKG = "Ports"
    _DECL = {
    # <p>The <code>type</code> of this <code>ConjugatedPortTyping</code> considered as a <code>Feature
    # Typing</code>, which must be a <code>ConjugatedPortDefinition</code>.</p>
    'conjugatedPortDefinition': _Ref('conjugatedPortDefinition', "ConjugatedPortDefinition", assoc="Systems-Ports-A_conjugatedPortDefinition_typingByConjugatedPort"),
    # <p>The <code>originalPortDefinition</code> of the <code>conjugatedPortDefinition</code> of this 
    # <code>ConjugatedPortTyping</code>.</p>
    'portDefinition': _Ref('portDefinition', "PortDefinition", derived=True, assoc="Systems-Ports-A_portDefinition_conjugatedPortTyping"),
    }
    CONSTRAINTS = (
        ("deriveConjugatedPortTypingPortDefinition",
         "portDefinition = conjugatedPortDefinition.originalPortDefinition"
        ),
    )

class Conjugation(Relationship):
    """<p><code>Conjugation</code> is a <code>Relationship</code> between two types in which the <code>conjugatedType</code> inherits all the <code>Features</code> of the <code>originalType</code>, but with all <code>input</code> and <code>output</code> <code>Features</code> reversed. That is, any <code>Features</code> with a <code>direction</code> <em>in</em> relative to the <code>originalType</code> are considered to have an effective <code>direction</code> of <em>out</em> relative to the <code>conjugatedType</code> and, similarly, <code>Features</code> with <code>direction</code> <em>out</em> in the <code>originalType</code> are considered to have an effective <code>direction</code> of <em>in</em> in the <code>conjugatedType</code>. <code>Features</code> with <code>direction</code> <em>inout</em>, or with no <code>direction</code>, in the <code>originalType</code>, are inherited without chan...[truncated]"""
    _PKG = "Types"
    _DECL = {
    # <p>The <code>Type</code> that is the result of applying <code>Conjugation</code> to the <code>or
    # iginalType</code>.</p>
    'conjugatedType': _Ref('conjugatedType', "Type", redefines=("source",), assoc="Core-Types-A_conjugatedType_conjugator"),
    # <p>The <code>Type</code> to be conjugated.</p>
    'originalType': _Ref('originalType', "Type", redefines=("target",), assoc="Core-Types-A_originalType_conjugation"),
    # <p>The <code>conjugatedType</code> of this <code>Conjugation</code> that is also its <code>ownin
    # gRelatedElement</code>.</p>
    'owningType': _Ref('owningType', "Type", subsets=("conjugatedType", "owningRelatedElement",), assoc="Core-Types-A_ownedConjugator_owningType"),
    }

class ConstructorExpression(InstantiationExpression):
    """<p>A <code>ConstructorExpression</code> is an <code>InstantiationExpression</code> whose <code>result</code> specializes its <code>instantiatedType</code>, binding some or all of the <code>features</code> of the <code>instantiatedType</code> to the <code>results</code> of its <code>argument</code> <code>Expressions</code>.</p>"""
    _PKG = "Expressions"
    CONSTRAINTS = (
        ("checkConstructorExpressionSpecialization",
         "specializes('Performances::constructorEvaluations')"
        ),
        ("checkConstructorExpressionResultDefaultValueBindingConnector",
         "TBD"
        ),
        ("deriveConstructorExpressionArgument",
         "instantiatedType.feature->collect(f |      result.ownedFeatures->select(redefines(f)).va"
         "luation->     select(v | v <> null).value )"
        ),
        ("checkConstructorExpressionResultSpecialization",
         "result.specializes(instantiatedType)"
        ),
        ("validateConstructorExpressionNoDuplicateFeatureRedefinition",
         "let features : OrderedSet(Feature) = instantiatedType.feature->     select(visibility = "
         "VisibilityKind::public) in result.ownedFeature->forAll(f1 | result.ownedFeature->forAll("
         "f2 |     f1 <> f2 implies         f1.ownedRedefinition.redefinedFeature->             in"
         "tersection(f2.ownedRedefinition.redefinedFeature)->             intersection(features)->"
         "isEmpty()))"
        ),
        ("validateConstructorExpressionOwnedFeatures",
         "ownedFeatures->excluding(result)->isEmpty()"
        ),
        ("checkConstructorExpressionResultFeatureRedefinition",
         "let features : OrderedSet(Feature) = instantiatedType.feature->     select(owningMembers"
         "hip.visibility = VisibilityKind::public) in result.ownedFeature->forAll(f |      f.owned"
         "Redefinition.redefinedFeature->         intersection(features)->size() = 1)"
        ),
    )
    def modelLevelEvaluable(self, arg: None = None, visited: None = None) -> None:
        """
        <p>A <code>ConstructorExpression</code> is model-level evaluable if all its argument <code>Exp
        ressions</code> are model-level evaluable.</p>
        [ConstructorExpression operation; params: arg: ?, visited: ?; returns: nothing; stub - metamod
        el metadata only]
        """
        raise NotImplementedError

class ControlNode(ActionUsage):
    """<p>A <code>ControlNode</code> is an <code>ActionUsage</code> that does not have any inherent behavior but provides constraints on incoming and outgoing <code>Successions</code> that are used to control other <code>Actions</code>. A <code>ControlNode</code> must be a composite owned <code>usage</code> of an <code>ActionDefinition</code> or <code>ActionUsage</code>.</p>"""
    _PKG = "Actions"
    CONSTRAINTS = (
        ("validateControlNodeOwningType",
         "owningType <> null and (owningType.oclIsKindOf(ActionDefinition) or owningType.oclIsKind"
         "Of(ActionUsage))"
        ),
        ("checkControlNodeSpecialization",
         "specializesFromLibrary('Action::Action::controls')"
        ),
        ("validateControlNodeIncomingSuccessions",
         "targetConnector->selectByKind(Succession)->     collect(connectorEnd->at(2).multiplicity"
         ")->     forAll(targetMult |          multiplicityHasBounds(targetMult, 1, 1))"
        ),
        ("validateControlNodeOutgoingSuccessions",
         "sourceConnector->selectByKind(Succession)->     collect(connectorEnd->at(1).multiplicity"
         ")->     forAll(sourceMult |          multiplicityHasBounds(sourceMult, 1, 1))"
        ),
        ("validateControlNodeIsComposite",
         "isComposite"
        ),
    )
    def multiplicityHasBounds(self, mult: None = None, lower: None = None, upper: None = None, arg: None = None) -> None:
        """
        <p>Check that the given <code>Multiplicity</code> has <code>lowerBound</code> and <code>upperB
        ound</code> expressions that are model-level evaluable to the given <code>lower</code> and <co
        de>upper</code> values.</p>
        [ControlNode operation; params: mult: ?, lower: ?, upper: ?, arg: ?; returns: nothing; stub - 
        metamodel metadata only]
        """
        raise NotImplementedError

class Subsetting(Specialization):
    """<p><code>Subsetting</code> is <code>Specialization</code> in which the <code>specific</code> and <code>general</code> <code>Types</code> are <code>Features</code>. This means all values of the <code>subsettingFeature</code> (on instances of its domain, i.e., the intersection of its <code>featuringTypes</code>) are values of the <code>subsettedFeature</code> on instances of its domain. To support this the domain of the <code>subsettingFeature</code> must be the same or specialize (at least indirectly) the domain of the <code>subsettedFeature</code> (via <code>Specialization</code>), and the co-domain (intersection of the <code>types</code>) of the <code>subsettingFeature</code> must specialize the co-domain of the <code>subsettedFeature</code>.</p>"""
    _PKG = "Features"
    _DECL = {
    # <p>A <code>subsettingFeature</code> that is also the <code>owningRelatedElement</code> of this <
    # code>Subsetting</code>.</p>
    'owningFeature': _Ref('owningFeature', "Feature", subsets=("subsettingFeature",), redefines=("owningType",), assoc="Core-Features-A_owningFeature_ownedSubsetting"),
    # <p>The <code>Feature</code> that is subsetted by the <code>subsettingFeature</code> of this <cod
    # e>Subsetting</code>.</p>
    'subsettedFeature': _Ref('subsettedFeature', "Feature", redefines=("general",), assoc="Core-Features-A_subsettedFeature_supersetting"),
    # <p>The <code>Feature</code> that is a subset of the <code>subsettedFeature</code> of this <code>
    # Subsetting</code>.</p>
    'subsettingFeature': _Ref('subsettingFeature', "Feature", redefines=("specific",), assoc="Core-Features-A_subsettingFeature_subsetting"),
    }
    CONSTRAINTS = (
        ("validateSubsettingConstantConformance",
         "subsettedFeature.isConstant and subsettingFeature.isVariable implies subsettingFeature.i"
         "sConstant"
        ),
        ("validateSubsettingUniquenessConformance",
         "subsettedFeature.isUnique implies subsettingFeature.isUnique"
        ),
        ("validateSubsettingFeaturingTypes",
         "subsettingFeature.canAccess(subsettedFeature)"
        ),
    )

class CrossSubsetting(Subsetting):
    """<p><code>CrossSubsetting</code> is a kind of <code>Subsetting</code> for end <code>Features</code>, as identified by <code>crossingFeature</code>, to subset a chained <code>Feature</code>, identified by <code>crossedFeature.</code> It navigates to instances of the end <code>Feature</code>’s type from instances of other end <code>Feature</code> types on the same <code>owningType</code> (at least two end <code>Features</code> are required for any of them to have a <code>CrossSubsetting</code>).</p> <p>The <code>crossedFeature</code> of a <code>CrossSubsetting</code> must have a feature chain of exactly two <code>Features</code>. The second <code>Feature</code> in the chain is the <code>crossFeature</code> of the <code>crossingFeature</code> (end <code>Feature</code>), which has the same type as the <code>crossingFeature</code>. When the <code>owningType</code> of the <code>crossingFeature<...[truncated]"""
    _PKG = "Features"
    _DECL = {
    # <p>The chained <code>Feature</code> that is cross subset by the <code>crossingFeature</code> of 
    # this <code>CrossSubsetting</code>.</p>
    'crossedFeature': _Ref('crossedFeature', "Feature", redefines=("subsettedFeature",), assoc="Core-Features-A_crossedFeature_crossSupersetting"),
    # <p>The end <code>Feature</code> that owns this <code>CrossSubsetting</code> relationship and is 
    # also its </code>subsettingFeature</code>.</p>
    'crossingFeature': _Ref('crossingFeature', "Feature", derived=True, redefines=("owningFeature", "subsettingFeature",), assoc="Core-Features-A_ownedCrossSubsetting_crossingFeature"),
    }
    CONSTRAINTS = (
        ("validateCrossSubsettingCrossedFeature",
         "crossingFeature.isEnd and crossingFeature.owningType <> null implies     let endFeatures"
         ": Sequence(Feature) = crossingFeature.owningType.endFeature in     let chainingFeatures:"
         " Sequence(Feature) = crossedFeature.chainingFeature in     chainingFeatures->size() = 2 "
         "and     endFeatures->size() = 2 implies          chainingFeatures->at(1) = endFeatures->"
         "excluding(crossingFeature)->at(1)"
        ),
        ("validateCrossSubsettingCrossingFeature",
         "crossingFeature.isEnd and crossingFeature.owningType<>null and crossingFeature.owningTyp"
         "e.endFeature ->size() > 1"
        ),
    )

class DecisionNode(ControlNode):
    """<p>A <code>DecisionNode</code> is a <code>ControlNode</code> that makes a selection from its outgoing <code>Successions</code>.</p>"""
    _PKG = "Actions"
    CONSTRAINTS = (
        ("validateDecisionNodeIncomingSuccessions",
         "targetConnector->selectByKind(Succession)->size() <= 1"
        ),
        ("validateDecisionNodeOutgoingSuccessions",
         "sourceConnector->selectAsKind(Succession)->     collect(connectorEnd->at(2))->     forAl"
         "l(targetMult |         multiplicityHasBounds(targetMult, 0, 1))"
        ),
        ("checkDecisionNodeSpecialization",
         "specializesFromLibrary('Actions::Action::decisions')"
        ),
        ("checkDecisionNodeOutgoingSuccessionSpecialization",
         "sourceConnector->selectByKind(Succession)->     forAll(subsetsChain(self,          resol"
         "veGlobal('ControlPerformances::MergePerformance::outgoingHBLink')))"
        ),
    )

class Dependency(Relationship):
    """<p>A <code>Dependency</code> is a <code>Relationship</code> that indicates that one or more <code>client</code> <code>Elements</code> require one more <code>supplier</code> <code>Elements</code> for their complete specification. In general, this means that a change to one of the <code>supplier</code> <code>Elements</code> may necessitate a change to, or re-specification of, the <code>client</code> <code>Elements</code>.</p> <p>Note that a <code>Dependency</code> is entirely a model-level <code>Relationship</code>, without instance-level semantics.</p>"""
    _PKG = "Dependencies"
    _DECL = {
    # <p>The <code>Element</code> or <code>Elements</code> dependent on the <code>supplier</code> <cod
    # e>Elements</code>.</p>
    'client': _Ref('client', "Element", multi=True, lo=1, hi='*', redefines=("source",), assoc="Root-Dependencies-A_client_clientDependency"),
    # <p>The <code>Element</code> or <code>Elements</code> on which the <code>client</code> <code>Elem
    # ents</code> depend in some respect.</p>
    'supplier': _Ref('supplier', "Element", multi=True, lo=1, hi='*', redefines=("target",), assoc="Root-Dependencies-A_supplier_supplierDependency"),
    }

class Differencing(Relationship):
    """<p><code>Differencing</code> is a <code>Relationship</code> that makes its <code>differencingType</code> one of the <code>differencingTypes</code> of its <code>typeDifferenced</code>.</p>"""
    _PKG = "Types"
    _DECL = {
    # <p><code>Type</code> that partly determines interpretations of <code>typeDifferenced</code>, as 
    # described in <code>Type::differencingType</code>.</p>
    'differencingType': _Ref('differencingType', "Type", redefines=("target",), assoc="Core-Types-A_differencingType_differencedDifferencing"),
    # <p><code>Type</code> with interpretations partly determined by <code>differencingType</code>, as
    #  described in <code>Type::differencingType</code>.</p>
    'typeDifferenced': _Ref('typeDifferenced', "Type", derived=True, subsets=("owningRelatedElement",), redefines=("source",), assoc="Core-Types-A_typeDifferenced_ownedDifferencing"),
    }

class Disjoining(Relationship):
    """<p>A <code>Disjoining</code> is a <code>Relationship</code> between <code>Types</code> asserted to have interpretations that are not shared (disjoint) between them, identified as <code>typeDisjoined</code> and <code>disjoiningType</code>. For example, a <code>Classifier</code> for mammals is disjoint from a <code>Classifier</code> for minerals, and a <code>Feature</code> for people&#39;s parents is disjoint from a <code>Feature</code> for their children.</p>"""
    _PKG = "Types"
    _DECL = {
    # <p><code>Type</code> asserted to be disjoint with the <code>typeDisjoined</code>.</p>
    'disjoiningType': _Ref('disjoiningType', "Type", redefines=("target",), assoc="Core-Types-A_disjoiningType_disjoinedTypeDisjoining"),
    # <p>A <code>typeDisjoined</code> that is also an <code>owningRelatedElement</code>.</p>
    'owningType': _Ref('owningType', "Type", subsets=("owningRelatedElement", "typeDisjoined",), assoc="Core-Types-A_ownedDisjoining_owningType"),
    # <p><code>Type</code> asserted to be disjoint with the <code>disjoiningType</code>.</p>
    'typeDisjoined': _Ref('typeDisjoined', "Type", redefines=("source",), assoc="Core-Types-A_disjoiningTypeDisjoining_typeDisjoined"),
    }

class Documentation(Comment):
    """<p><code>Documentation</code> is a <code>Comment</code> that specifically documents a <code>documentedElement</code>, which must be its <code>owner</code>.</p>"""
    _PKG = "Annotations"
    _DECL = {
    # <p>The <code>Element</code> that is documented by this <code>Documentation</code>.</p>
    'documentedElement': _Ref('documentedElement', "Element", derived=True, subsets=("owner",), redefines=("annotatedElement",), assoc="Root-Elements-A_documentation_documentedElement"),
    }

class ElementFilterMembership(OwningMembership):
    """<p><code>ElementFilterMembership</code> is a <code>Membership</code> between a <code>Namespace</code> and a model-level evaluable <code><em>Boolean</em></code>-valued <code>Expression</code>, asserting that imported <code>members</code> of the <code>Namespace</code> should be filtered using the <code>condition</code> <code>Expression</code>. A general <code>Namespace</code> does not define any specific filtering behavior, but such behavior may be defined for various specialized kinds of <code>Namespaces</code>.</p>"""
    _PKG = "Packages"
    _DECL = {
    # <p>The model-level evaluable <code>Boolean</code>-valued <code>Expression</code> used to filter 
    # the imported <code>members</code> of the <code>membershipOwningNamespace</code> of this <code>El
    # ementFilterMembership</code>.</p>
    'condition': _Ref('condition', "Expression", derived=True, redefines=("ownedMemberElement",), assoc="Kernel-Packages-A_condition_owningFilter"),
    }
    CONSTRAINTS = (
        ("validateElementFilterMembershipConditionIsModelLevelEvaluable",
         "condition.isModelLevelEvaluable"
        ),
        ("validateElementFilterMembershipConditionIsBoolean",
         "condition.result.specializesFromLibrary('ScalarValues::Boolean')"
        ),
    )

class EndFeatureMembership(FeatureMembership):
    """<p><code>EndFeatureMembership</code> is a <code>FeatureMembership</code> that requires its <code>memberFeature</code> be owned and have <code>isEnd = true</code>.</p>"""
    _PKG = "Features"
    _DECL = {
    'ownedMemberFeature': _Ref('ownedMemberFeature', "Feature", derived=True, composite=True, redefines=("ownedMemberFeature",), assoc="Core-Features-A_ownedMemberFeature_owningEndFeatureMembership"),
    }
    CONSTRAINTS = (
        ("validateEndFeatureMembershipIsEnd",
         "ownedMemberFeature.isEnd"
        ),
    )

class EnumerationDefinition(AttributeDefinition):
    """<p>An <code>EnumerationDefinition</code> is an <code>AttributeDefinition</code> all of whose instances are given by an explicit list of <code>enumeratedValues</code>. This is realized by requiring that the <code>EnumerationDefinition</code> have <code>isVariation = true</code>, with the <code>enumeratedValues</code> being its <code>variants</code>.</p>"""
    _PKG = "Enumerations"
    _DECL = {
    # <p><code>EnumerationUsages</code> of this <code>EnumerationDefinition</code>that have distinct, 
    # fixed values. Each <code>enumeratedValue</code> specifies one of the allowed instances of the <c
    # ode>EnumerationDefinition</code>.</p>
    'enumeratedValue': _Ref('enumeratedValue', "EnumerationUsage", derived=True, multi=True, lo=0, hi='*', redefines=("variant",), assoc="Systems-Enumerations-A_enumeratedValue_owningEnumerationDefinition"),
    # <p>An EnumerationDefinition is considered semantically to be a variation whose allowed variants 
    # are its <code>enumerationValues</code>.</p>
    'isVariation': _Ref('isVariation', bool, redefines=("isVariation",)),
    }
    CONSTRAINTS = (
        ("validateEnumerationDefinitionIsVariation",
         "isVariation"
        ),
    )

class EnumerationUsage(AttributeUsage):
    """<p>An <code>EnumerationUsage</code> is an <code>AttributeUsage</code> whose <code>attributeDefinition</code> is an <code>EnumerationDefinition</code>.</p>"""
    _PKG = "Enumerations"
    _DECL = {
    # <p>The single EnumerationDefinition that is the type of this EnumerationUsage.</p>
    'enumerationDefinition': _Ref('enumerationDefinition', "EnumerationDefinition", derived=True, redefines=("attributeDefinition",), assoc="Systems-Enumerations-A_enumerationDefinition_definedEnumeration"),
    }

class EventOccurrenceUsage(OccurrenceUsage):
    """<p>An <code>EventOccurrenceUsage</code> is an <code>OccurrenceUsage</code> that represents another <code>OccurrenceUsage</code> occurring as a <code><em>suboccurrence</em></code> of the containing occurrence of the <code>EventOccurrenceUsage</code>. Unless it is the <code>EventOccurrenceUsage</code> itself, the referenced <code>OccurrenceUsage</code> is related to the <code>EventOccurrenceUsage</code> by a <code>ReferenceSubsetting</code> <code>Relationship</code>.</p> <p>If the <code>EventOccurrenceUsage</code> is owned by an <code>OccurrenceDefinition</code> or <code>OccurrenceUsage</code>, then it also subsets the <em><code>timeEnclosedOccurrences</code></em> property of the <code>Class</code> <em><code>Occurrence</code></em> from the Kernel Semantic Library model <em><code>Occurrences</code></em>.</p>"""
    _PKG = "Occurrences"
    _DECL = {
    # <p>The <code>OccurrenceUsage</code> referenced as an event by this <code>EventOccurrenceUsage</c
    # ode>. It is the <code>referenceFeature</code> of the <code>ownedReferenceSubsetting</code> for t
    # he <code>EventOccurrenceUsage</code>, if there is one, and, otherwise, the <code>EventOccurrence
    # Usage</code> itself.</p>
    'eventOccurrence': _Ref('eventOccurrence', "OccurrenceUsage", derived=True, assoc="Systems-Occurrences-A_eventOccurrence_referencingOccurrence"),
    # <p>Always true for an <code>EventOccurrenceUsage</code>.</p>
    'isReference': _Ref('isReference', bool, derived=True, redefines=("isReference",)),
    }
    CONSTRAINTS = (
        ("validateEventOccurrenceUsageReference",
         "referencedFeatureTarget() <> null implies referencedFeatureTarget().oclIsKindOf(Occurren"
         "ceUsage)"
        ),
        ("deriveEventOccurrenceUsageEventOccurrence",
         "eventOccurrence =     if referencedFeatureTarget() = null then self     else if referenc"
         "edFeatureTarget().oclIsKindOf(OccurrenceUsage) then         referencedFeatureTarget().oc"
         "lAsType(OccurrenceUsage)     else null     endif endif"
        ),
        ("checkEventOccurrenceUsageSpecialization",
         "owningType <> null and (owningType.oclIsKindOf(OccurrenceDefinition) or  owningType.oclI"
         "sKindOf(OccurrenceUsage)) implies     specializesFromLibrary('Occurrences::Occurrence::t"
         "imeEnclosedOccurrences')"
        ),
        ("validateEventOccurrenceUsageIsReference",
         "isReference"
        ),
    )

class PerformActionUsage(EventOccurrenceUsage, ActionUsage):
    """<p>A <code>PerformActionUsage</code> is an <code>ActionUsage</code> that represents the performance of an <code>ActionUsage</code>. Unless it is the <code>PerformActionUsage</code> itself, the <code>ActionUsage</code> to be performed is related to the <code>PerformActionUsage</code> by a <code>ReferenceSubsetting</code> relationship. A <code>PerformActionUsage</code> is also an <code>EventOccurrenceUsage</code>, with its <code>performedAction</code> as the <code>eventOccurrence</code>.</p>"""
    _PKG = "Actions"
    _DECL = {
    # <p>The <code>ActionUsage</code> to be performed by this <code>PerformedActionUsage</code>. It is
    #  the <code>eventOccurrence</code> of the <code>PerformActionUsage</code> considered as an <code>
    # EventOccurrenceUsage</code>, which must be an <code>ActionUsage</code>.</p>
    'performedAction': _Ref('performedAction', "ActionUsage", derived=True, redefines=("eventOccurrence",), assoc="Systems-Actions-A_performedAction_performingAction"),
    }
    CONSTRAINTS = (
        ("validatePerformActionUsageReference",
         "referencedFeatureTarget() <> null implies referencedFeatureTarget().oclIsKindOf(ActionUs"
         "age)"
        ),
        ("checkPerformActionUsageSpecialization",
         "owningType <> null and (owningType.oclIsKindOf(PartDefinition) or  owningType.oclIsKindO"
         "f(PartUsage)) implies     specializesFromLibrary('Parts::Part::performedActions')"
        ),
    )
    def namingFeature(self, arg: None = None) -> None:
        """
        <p>The naming <code>Feature</code> of a <code>PerformActionUsage</code> is its <code>performed
        Action</code>, if this is different than the <code>PerformActionUsage</code>. If the <code>Per
        formActionUsage</code> is its own <code>performedAction</code>, then the naming <code>Feature<
        /code> is the same as the usual default for a <code>Usage</code>.</p>
        [PerformActionUsage operation; params: arg: ?; returns: nothing; stub - metamodel metadata onl
        y]
        """
        raise NotImplementedError

class StateUsage(ActionUsage):
    """<p>A <code>StateUsage</code> is an <code>ActionUsage</code> that is nominally the <code>Usage</code> of a <code>StateDefinition</code>. However, other kinds of kernel <code>Behaviors</code> are also allowed as <code>types</code>, to permit use of <code>Behaviors</code from the Kernel Model Libraries.</p> <p>A <code>StateUsage</code> may be related to up to three of its <code>ownedFeatures</code> by <code>StateSubactionMembership</code> <code>Relationships</code>, all of different <code>kinds</code>, corresponding to the entry, do and exit actions of the <code>StateUsage</code>.</p>"""
    _PKG = "States"
    _DECL = {
    # <p>The <code>ActionUsage</code> of this <code>StateUsage</code> to be performed while in the sta
    # te defined by the <code>StateDefinition</code>. It is the owned <code>ActionUsage</code> related
    #  to the <code>StateUsage</code> by a <code>StateSubactionMembership</code> with <code>kind = do<
    # /code>.</p>
    'doAction': _Ref('doAction', "ActionUsage", derived=True, assoc="Systems-States-A_doAction_activeState"),
    # <p>The <code>ActionUsage</code> of this <code>StateUsage</code> to be performed on entry to the 
    # state defined by the <code>StateDefinition</code>. It is the owned <code>ActionUsage</code> rela
    # ted to the <code>StateUsage</code> by a <code>StateSubactionMembership</code> with <code>kind = 
    # entry</code>.</p>
    'entryAction': _Ref('entryAction', "ActionUsage", derived=True, assoc="Systems-States-A_entryAction_enteredState"),
    # <p>The <code>ActionUsage</code> of this <code>StateUsage</code> to be performed on exit to the s
    # tate defined by the <code>StateDefinition</code>. It is the owned <code>ActionUsage</code> relat
    # ed to the <code>StateUsage</code> by a <code>StateSubactionMembership</code> with <code>kind = e
    # xit</code>.</p>
    'exitAction': _Ref('exitAction', "ActionUsage", derived=True, assoc="Systems-States-A_exitAction_exitedState"),
    # <p>Whether the <code>nestedStates</code> of this <code>StateUsage</code> are to all be performed
    #  in parallel. If true, none of the <code>nestedActions</code> (which include <code>nestedStates<
    # /code>) may have any incoming or outgoing <code>Transitions</code>. If false, only one <code>nes
    # tedState</code> may be performed at a time.</p>
    'isParallel': _Ref('isParallel', bool),
    # <p>The <code>Behaviors</code> that are the <code>types</code> of this <code>StateUsage</code>. N
    # ominally, these would be <code>StateDefinitions</code>, but kernel <code>Behaviors</code> are al
    # so allowed, to permit use of <code>Behaviors</code> from the Kernel Model Libraries.</p>
    'stateDefinition': _Ref('stateDefinition', "Behavior", derived=True, multi=True, lo=0, hi='*', redefines=("actionDefinition",), assoc="Systems-States-A_stateDefinition_definedState"),
    }
    CONSTRAINTS = (
        ("validateStateUsageParallelSubactions",
         "isParallel implies nestedAction.incomingTransition->isEmpty() and nestedAction.outgoingT"
         "ransition->isEmpty()"
        ),
        ("checkStateUsageExclusiveStateSpecialization",
         "isSubstateUsage(false) implies specializesFromLibrary('States::StateAction::exclusiveSta"
         "tes')"
        ),
        ("deriveStateUsageDoAction",
         "doAction =     let doMemberships : Sequence(StateSubactionMembership) =         ownedMem"
         "bership->             selectByKind(StateSubactionMembership)->             select(kind ="
         " StateSubactionKind::do) in     if doMemberships->isEmpty() then null     else doMembers"
         "hips->at(1)     endif"
        ),
        ("validateStateUsageStateSubactionKind",
         "ownedMembership-> selectByKind(StateSubactionMembership)-> isUnique(kind)"
        ),
        ("deriveStateUsageEntryAction",
         "entryAction =     let entryMemberships : Sequence(StateSubactionMembership) =         ow"
         "nedMembership->             selectByKind(StateSubactionMembership)->             select("
         "kind = StateSubactionKind::entry) in     if entryMemberships->isEmpty() then null     el"
         "se entryMemberships->at(1)     endif"
        ),
        ("checkStateUsageOwnedStateSpecialization",
         "isComposite and owningType <> null and (owningType.oclIsKindOf(PartDefinition) or  ownin"
         "gType.oclIsKindOf(PartUsage)) implies     specializesFromLibrary('Parts::Part::ownedStat"
         "es')"
        ),
        ("checkStateUsageSubstateSpecialization",
         "isSubstateUsage(true) implies specializesFromLibrary('States::StateAction::substates')"
        ),
        ("checkStateUsageSpecialization",
         "specializesFromLibrary('States::stateActions')"
        ),
        ("deriveStateUsageExitAction",
         "exitAction =     let exitMemberships : Sequence(StateSubactionMembership) =         owne"
         "dMembership->             selectByKind(StateSubactionMembership)->             select(ki"
         "nd = StateSubactionKind::exit) in     if exitMemberships->isEmpty() then null     else e"
         "xitMemberships->at(1)     endif"
        ),
    )
    def isSubstateUsage(self, isParallel: None = None, arg: None = None) -> None:
        """
        <p>Check if this <code>StateUsage</code> is composite and has an <code>owningType</code> that 
        is a <code>StateDefinition</code> or <code>StateUsage</code> with the given value of <code>isP
        arallel</code>, but is <em>not</em> an <code>entryAction</code>, <code>doAction</code>, or <co
        de>exitAction</code>. If so, then it represents a <code><em>StateAction</em></code> that is a 
        <code><em>substate</em></code> or <code><em>exclusiveState</em></code> (for <code>isParallel =
         false</code>) of another <code><em>StateAction</em></code>.</p>
        [StateUsage operation; params: isParallel: ?, arg: ?; returns: nothing; stub - metamodel metad
        ata only]
        """
        raise NotImplementedError

class ExhibitStateUsage(PerformActionUsage, StateUsage):
    """<p>An <code>ExhibitStateUsage</code> is a <code>StateUsage</code> that represents the exhibiting of a <code>StateUsage</code>. Unless it is the <code>StateUsage</code> itself, the <code>StateUsage</code> to be exhibited is related to the <code>ExhibitStateUsage</code> by a <code>ReferenceSubsetting</code> <code>Relationship</code>. An <code>ExhibitStateUsage</code> is also a <code>PerformActionUsage</code>, with its <code>exhibitedState</code> as the <code>performedAction</code>.</p>"""
    _PKG = "States"
    _DECL = {
    # <p>The <code>StateUsage</code> to be exhibited by the <code>ExhibitStateUsage</code>. It is the 
    # <code>performedAction</code> of the <code>ExhibitStateUsage</code> considered as a <code>Perform
    # ActionUsage</code>, which must be a <code>StateUsage</code>.</p>
    'exhibitedState': _Ref('exhibitedState', "StateUsage", derived=True, redefines=("performedAction",), assoc="Systems-States-A_exhibitedState_exhibitingState"),
    }
    CONSTRAINTS = (
        ("checkExhibitStateUsageSpecialization",
         "owningType <> null and (owningType.oclIsKindOf(PartDefinition) or  owningType.oclIsKindO"
         "f(PartUsage)) implies     specializesFromLibrary('Parts::Part::exhibitedStates')"
        ),
        ("validateExhibitStateUsageReference",
         "referencedFeatureTarget() <> null implies referencedFeatureTarget().oclIsKindOf(StateUsa"
         "ge)"
        ),
    )

class Import(Relationship):
    """<p>An <code>Import</code> is an <code>Relationship</code> between its <code>importOwningNamespace</code> and either a <code>Membership</code> (for a <code>MembershipImport</code>) or another <code>Namespace</code> (for a <code>NamespaceImport</code>), which determines a set of <code>Memberships</code> that become <code>importedMemberships</code> of the <code>importOwningNamespace</code>. If <code>isImportAll = false</code> (the default), then only public <code>Memberships</code> are considered &quot;visible&quot;. If <code>isImportAll = true</code>, then all <code>Memberships</code> are considered &quot;visible&quot;, regardless of their declared <code>visibility</code>. If <code>isRecursive = true</code>, then visible <code>Memberships</code> are also recursively imported from owned sub-<code>Namespaces</code>.</p>"""
    _PKG = "Namespaces"
    _DECL = {
    # <p>The Namespace into which Memberships are imported by this Import, which must be the <code>own
    # ingRelatedElement</code> of the Import.</p>
    'importOwningNamespace': _Ref('importOwningNamespace', "Namespace", derived=True, subsets=("owningRelatedElement",), redefines=("source",), assoc="Root-Namespaces-A_ownedImport_importOwningNamespace"),
    # <p>The effectively imported <code>Element</code> for this </code>Import</code>. For a <code>Memb
    # ershipImport</code>, this is the <code>memberElement</code> of the <code>importedMembership</cod
    # e>. For a <code>NamespaceImport</code>, it is the <code>importedNamespace</code>.</p>
    'importedElement': _Ref('importedElement', "Element", derived=True, assoc="Root-Namespaces-A_importedElement_membershipImport"),
    # <p>Whether to import memberships without regard to declared visibility.</p>
    'isImportAll': _Ref('isImportAll', bool),
    # <p>Whether to recursively import Memberships from visible, owned sub-Namespaces.</p>
    'isRecursive': _Ref('isRecursive', bool),
    # <p>The visibility level of the imported <code>members</code> from this Import relative to the <c
    # ode>importOwningNamespace</code>. The default is <code>private</code>.</p>
    'visibility': _Ref('visibility', None),
    }
    CONSTRAINTS = (
        ("validateImportTopLevelVisibility",
         "importOwningNamespace.owner = null implies visibility = VisibilityKind::private"
        ),
    )
    def importedMemberships(self, excluded: None = None, arg: None = None) -> None:
        """
        <p>Returns Memberships that are to become <code>importedMemberships</code> of the <code>import
        OwningNamespace</code>. (The <code>excluded</code> parameter is used to handle the possibility
         of circular Import Relationships.)</p>
        [Import operation; params: excluded: ?, arg: ?; returns: nothing; stub - metamodel metadata on
        ly]
        """
        raise NotImplementedError

class Expose(Import):
    """<p>An <code>Expose</code> is an <code>Import</code> of <code>Memberships</code> into a <code>ViewUsage</code> that provide the <code>Elements</code> to be included in a view. Visibility is always ignored for an <code>Expose</code> (i.e., <code>isImportAll = true</code>).</p>"""
    _PKG = "Views"
    _DECL = {
    # <p>An <code>Expose</code> always imports all <code>Elements</code>, regardless of visibility (<c
    # ode>isImportAll = true</code>).</p>
    'isImportAll': _Ref('isImportAll', bool),
    # <p>An <code>Expose</code> always has <code>protected</code> visibility.</p>
    'visibility': _Ref('visibility', None),
    }
    CONSTRAINTS = (
        ("validateExposeVisibility",
         "visibility = VisibilityKind::protected"
        ),
        ("validateExposeIsImportAll",
         "isImportAll"
        ),
        ("validateExposeOwningNamespace",
         "importOwningNamespace.oclIsType(ViewUsage)"
        ),
    )

class FeatureChainExpression(OperatorExpression):
    """<p>A <code>FeatureChainExpression</code> is an <code>OperatorExpression</code> whose operator is <code>"."</code>, which resolves to the <code>Function</code> <em><code>ControlFunctions::'.'</code></em> from the Kernel Functions Library. It evaluates to the result of chaining the <code>result</code> <code>Feature</code> of its single <code>argument</code> <code>Expression</code> with its <code>targetFeature</code>.</p>"""
    _PKG = "Expressions"
    _DECL = {
    'operator': _Ref('operator', str, redefines=("operator",)),
    # <p>The <code>Feature</code> that is accessed by this <code>FeatureChainExpression<code>, which i
    # s its first non-<code>parameter</code> <code>member</code>.<p>
    'targetFeature': _Ref('targetFeature', "Feature", derived=True, subsets=("member",), assoc="Kernel-Expressions-A_targetFeature_chainExpression"),
    }
    CONSTRAINTS = (
        ("checkFeatureChainExpressionResultSpecialization",
         "let inputParameters : Sequence(Feature) =      ownedFeatures->select(direction = _'in') "
         "in let sourceTargetFeature : Feature =      owningExpression.sourceTargetFeature() in so"
         "urceTargetFeature <> null and result.subsetsChain(inputParameters->first(), sourceTarget"
         "Feature) and result.owningType = self"
        ),
        ("validateFeatureChainExpressionOperator",
         "operator = '.'"
        ),
        ("validateFeatureChainExpressionConformance",
         "argument->notEmpty() implies targetFeature.isFeaturedWithin(argument->first().result)"
        ),
        ("deriveFeatureChainExpressionTargetFeature",
         "targetFeature =     let nonParameterMemberships : Sequence(Membership) = ownedMembership"
         "->         reject(oclIsKindOf(ParameterMembership)) in     if nonParameterMemberships->i"
         "sEmpty() or        not nonParameterMemberships->first().memberElement.oclIsKindOf(Featur"
         "e)     then null     else nonParameterMemberships->first().memberElement.oclAsType(Featu"
         "re)     endif"
        ),
        ("checkFeatureChainExpressionTargetRedefinition",
         "let sourceParameter : Feature = sourceTargetFeature() in sourceTargetFeature <> null and"
         " sourceTargetFeature.redefinesFromLibrary('ControlFunctions::\\'.\\'::source::target')"
        ),
        ("checkFeatureChainExpressionSourceTargetRedefinition",
         "let sourceParameter : Feature = sourceTargetFeature() in sourceTargetFeature <> null and"
         " sourceTargetFeature.redefines(targetFeature)"
        ),
    )
    def sourceTargetFeature(self, arg: None = None) -> None:
        """
        <p>Return the first <code>ownedFeature</code> of the first owned input <code>parameter</code> 
        of this <code>FeatureChainExpression</code> (if any).</p>
        [FeatureChainExpression operation; params: arg: ?; returns: nothing; stub - metamodel metadata
         only]
        """
        raise NotImplementedError

class FeatureChaining(Relationship):
    """<p><code>FeatureChaining</code> is a <code>Relationship</code> that makes its target <code>Feature</code> one of the <code>chainingFeatures</code> of its owning <code>Feature</code>.</p>"""
    _PKG = "Features"
    _DECL = {
    # <p>The <code>Feature</code> whose values partly determine values of <code>featureChained</code>,
    #  as described in <code>Feature::chainingFeature</code>.</p>
    'chainingFeature': _Ref('chainingFeature', "Feature", redefines=("target",), assoc="Core-Features-A_chainingFeature_chainedFeatureChaining"),
    # <p>The <code>Feature</code> whose values are partly determined by values of the <code>chainingFe
    # ature</code>, as described in <code>Feature::chainingFeature</code>.</p>
    'featureChained': _Ref('featureChained', "Feature", derived=True, subsets=("owningRelatedElement",), redefines=("source",), assoc="Core-Features-A_ownedFeatureChaining_featureChained"),
    }

class FeatureInverting(Relationship):
    """<p>A <code>FeatureInverting</code> is a <code>Relationship</code> between <code>Features</code> asserting that their interpretations (sequences) are the reverse of each other, identified as <code>featureInverted</code> and <code>invertingFeature</code>. For example, a <code>Feature</code> identifying each person&#39;s parents is the inverse of a <code>Feature</code> identifying each person&#39;s children. A person identified as a parent of another will identify that other as one of their children.</p>"""
    _PKG = "Features"
    _DECL = {
    # <p>The <code>Feature</code> that is an inverse of the <code>invertingFeature</code>.</p>
    'featureInverted': _Ref('featureInverted', "Feature", redefines=("source",), assoc="Core-Features-A_invertingFeatureInverting_featureInverted"),
    # <p>The <code>Feature</code> that is an inverse of the <code>invertedFeature</code>.</p>
    'invertingFeature': _Ref('invertingFeature', "Feature", redefines=("target",), assoc="Core-Features-A_invertingFeature_invertedFeatureInverting"),
    # <p>A <code>featureInverted</code> that is also the <code>owningRelatedElement</code> of this <co
    # de>FeatureInverting</code>.</p>
    'owningFeature': _Ref('owningFeature', "Feature", subsets=("featureInverted", "owningRelatedElement",), assoc="Core-Features-A_ownedFeatureInverting_owningFeature"),
    }

class FeatureReferenceExpression(Expression):
    """<p>A <code>FeatureReferenceExpression</code> is an <code>Expression</code> whose <code>result</code> is bound to a <code>referent</code> <code>Feature</code>.</p>"""
    _PKG = "Expressions"
    _DECL = {
    # <p>The <code>Feature</code> that is referenced by this <code>FeatureReferenceExpression</code>, 
    # which is its first non-<code>parameter</code> <code>member</code>.<p>
    'referent': _Ref('referent', "Feature", derived=True, subsets=("member",), assoc="Kernel-Expressions-A_referent_referenceExpression"),
    }
    CONSTRAINTS = (
        ("validateFeatureReferenceExpressionReferentIsFeature",
         "let membership : Membership =      ownedMembership->reject(m | m.oclIsKindOf(ParameterMe"
         "mbership)) in membership->notEmpty() and membership->at(1).memberElement.oclIsKindOf(Fea"
         "ture)"
        ),
        ("checkFeatureReferenceExpressionBindingConnector",
         "ownedMember->selectByKind(BindingConnector)->exists(b |     b.relatedFeatures->includes("
         "targetFeature) and     b.relatedFeatures->includes(result))"
        ),
        ("checkFeatureReferenceExpressionResultSpecialization",
         "result.owningType() = self and result.specializes(referent)"
        ),
        ("deriveFeatureReferenceExpressionReferent",
         "referent =     let nonParameterMemberships : Sequence(Membership) = ownedMembership->   "
         "      reject(oclIsKindOf(ParameterMembership)) in     if nonParameterMemberships->isEmpt"
         "y() or        not nonParameterMemberships->first().memberElement.oclIsKindOf(Feature)   "
         "  then null     else nonParameterMemberships->first().memberElement.oclAsType(Feature)  "
         "   endif"
        ),
        ("validateFeatureReferenceExpressionResult",
         "result.owningType = self"
        ),
    )
    def modelLevelEvaluable(self, arg: None = None, visited: None = None) -> None:
        """
        <p>A <code>FeatureReferenceExpression</code> is model-level evaluable if it&#39;s <code>refere
        nt</code></p> <ul> <li>conforms to the self-reference feature <code><em>Anything::self</em></c
        ode>;</li> <li>is an <code>Expression</code> that is model-level evaluable;</li> <li>has an <c
        ode>owningType</code> that is a <code>Metaclass</code> or <code>MetadataFeature</code>; or</li
        > <li>has no <code>featuringTypes</code> and, if it has a <code>FeatureValue</code>, the <code
        >value</code> <code>Expression</code> is model-level evaluable.</li> </ul>
        [FeatureReferenceExpression operation; params: arg: ?, visited: ?; returns: nothing; stub - me
        tamodel metadata only]
        """
        raise NotImplementedError
    def evaluate(self, target: None = None, result: None = None) -> None:
        """
        <p>First, determine a <code>value</code> <code>Expression</code> for the <code>referent</code>
        :</p> <ul> <li>If the <code>target</code> <code>Element</code> is a Type that has a <code>feat
        ure</code> that is the <code>referent</code> or (directly or indirectly) redefines it, then th
        e <code>value</code> <code>Expression</code> of the <code>FeatureValue</code> for that <code>f
        eature</code> (if any).</li> <li>Else, if the <code>referent</code> has no <code>featuringType
        s</code>, the <code>value</code> <code>Expression</code> of the <code>FeatureValue</code> for 
        the <code>referent</code> (if any).</li> </ul> <p>Then:</p> <ul> <li>If such a value <code>Exp
        ression</code> exists, return the result of evaluating that <code>Expression</code> on the <co
        de>target</code>.</li> <li>Else, if the <code>referent</code> is not an <code>Expression</code
        >, return the <code>referent</code>.</li> <li>Else return the empty sequence.</li> </ul>
        [FeatureReferenceExpression operation; params: target: ?, result: ?; returns: nothing; stub - 
        metamodel metadata only]
        """
        raise NotImplementedError

class FeatureValue(OwningMembership):
    """<p>A <code>FeatureValue</code> is a <code>Membership</code> that identifies a particular member <code>Expression</code> that provides the value of the <code>Feature</code> that owns the <code>FeatureValue</code>. The value is specified as either a bound value or an initial value, and as either a concrete or default value. A <code>Feature</code> can have at most one <code>FeatureValue</code>.</p> <p>The result of the <code>value</code> <code>Expression</code> is bound to the <code>featureWithValue</code> using a <code>BindingConnector</code>. If <code>isInitial = false</code>, then the <code>featuringType</code> of the <code>BindingConnector</code> is the same as the <code>featuringType</code> of the <code>featureWithValue</code>. If <code>isInitial = true</code>, then the <code>featuringType</code> of the <code>BindingConnector</code> is restricted to its <code>startShot</code>. <p>If <c...[truncated]"""
    _PKG = "FeatureValues"
    _DECL = {
    # <p>The Feature to be provided a value.</p>
    'featureWithValue': _Ref('featureWithValue', "Feature", derived=True, subsets=("membershipOwningNamespace",), assoc="Kernel-FeatureValues-A_featureWithValue_valuation"),
    # <p>Whether this <code>FeatureValue</code> is a concrete specification of the bound or initial va
    # lue of the <code>featureWithValue</code>, or just a default value that may be overridden.</p>
    'isDefault': _Ref('isDefault', bool),
    # <p>Whether this <code>FeatureValue</code> specifies a bound value or an initial value for the <c
    # ode>featureWithValue</code>.</p>
    'isInitial': _Ref('isInitial', bool),
    # <p>The Expression that provides the value as a result.</p>
    'value': _Ref('value', "Expression", derived=True, redefines=("ownedMemberElement",), assoc="Kernel-FeatureValues-A_value_expressedValuation"),
    }
    CONSTRAINTS = (
        ("validateFeatureValueIsInitial",
         "isInitial implies featureWithValue.isVariable"
        ),
        ("validateFeatureValueOverriding",
         "featureWithValue.redefinition.redefinedFeature-> closure(redefinition.redefinedFeature)."
         "valuation-> forAll(isDefault)"
        ),
        ("checkFeatureValueBindingConnector",
         "not isDefault implies     featureWithValue.ownedMember->         selectByKind(BindingCon"
         "nector)->exists(b |             b.relatedFeature->includes(featureWithValue) and        "
         "     b.relatedFeature->exists(f |                  f.chainingFeature = Sequence{value, v"
         "alue.result}) and             if not isInitial then                  b.featuringType = f"
         "eatureWithValue.featuringType             else                  b.featuringType->exists("
         "t |                     t.oclIsKindOf(Feature) and                     t.oclAsType(Featu"
         "re).chainingFeature =                         Sequence{                             reso"
         "lveGlobal('Base::things::that').                                 memberElement,         "
         "                    resolveGlobal('Occurrences::Occurrence::startShot').                "
         "                 memberElement                         }                 )             e"
         "ndif)"
        ),
    )

class Flow(Connector, Step):
    """<p>An <code>Flow</code> is a <code>Step</code> that represents the transfer of values from one <code>Feature</code> to another. <code>Flows</code> can take non-zero time to complete.</p>"""
    _PKG = "Interactions"
    _DECL = {
    # <p>The <code>connectorEnds</code> of this <code>Flow</code> that are <code>FlowEnds</code>.</p>
    'flowEnd': _Ref('flowEnd', "FlowEnd", derived=True, subsets=("connectorEnd",), assoc="Kernel-Interactions-A_flowEnd_featuringFlow"),
    # <p>The <code>Interactions</code> that type this <code>Flow</code>. <code>Interactions</code> are
    #  both <code>Associations</code> and <code>Behaviors</code>, which can type <code>Connectors</cod
    # e> and <code>Steps</code>, respectively.</p>
    'interaction': _Ref('interaction', "Interaction", derived=True, multi=True, lo=0, hi='*', redefines=("association", "behavior",), assoc="Kernel-Interactions-A_interaction_typedFlow"),
    # <p>The <code>ownedFeature</code> of the <code>Flow</code> that is a <code>PayloadFeature</code> 
    # (if any).</p>
    'payloadFeature': _Ref('payloadFeature', "PayloadFeature", derived=True, subsets=("ownedFeature",), assoc="Kernel-Interactions-A_payloadFeature_flowWithPayloadFeature"),
    # <p>The type of values transferred, which is the <code>type</code> of the <code>payloadFeature</c
    # ode> of the <code>Flow</code>.</p>
    'payloadType': _Ref('payloadType', "Classifier", derived=True, multi=True, lo=0, hi='*', assoc="Kernel-Interactions-A_payloadType_flowForPayloadType"),
    # <p>The <code>Feature</code> that provides the items carried by the <code>Flow</code>. It must be
    #  a <code>feature</code> of the <code>source</code> of the <code>Flow</code>.</p>
    'sourceOutputFeature': _Ref('sourceOutputFeature', "Feature", derived=True, assoc="Kernel-Interactions-A_sourceOutputFeature_flowFromOutput"),
    # <p>The <code>Feature</code> that receives the values carried by the <code>Flow</code>. It must b
    # e a <code>feature</code> of the <code>target</code> of the <code>Flow</code>.</p>
    'targetInputFeature': _Ref('targetInputFeature', "Feature", derived=True, assoc="Kernel-Interactions-A_targetInputFeature_flowToInput"),
    }
    CONSTRAINTS = (
        ("deriveFlowFlowEnd",
         "flowEnd = connectorEnd->selectByKind(FlowEnd)"
        ),
        ("validateFlowPayloadFeature",
         "ownedFeature->selectByKind(PayloadFeature)->size() <= 1"
        ),
        ("deriveFlowTargetInputFeature",
         "targetInputFeature =     if connectorEnd->size() < 2 or          connectorEnd->at(2).own"
         "edFeature->isEmpty()     then null     else connectorEnd->at(2).ownedFeature->first()   "
         "  endif"
        ),
        ("deriveFlowPayloadType",
         "payloadType = if payloadFeature = null then Sequence{} else payloadFeature.type endif"
        ),
        ("deriveFlowPayloadFeature",
         "payloadFeature =     let payloadFeatures : Sequence(PayloadFeature) =         ownedFeatu"
         "re->selectByKind(PayloadFeature) in     if payloadFeatures->isEmpty() then null     else"
         " payloadFeatures->first()     endif"
        ),
        ("checkFlowSpecialization",
         "specializesFromLibrary('Transfers::transfers')"
        ),
        ("checkFlowWithEndsSpecialization",
         "ownedEndFeatures->notEmpty() implies specializesFromLibrary('Transfers::flowTransfers')"
        ),
        ("deriveFlowSourceOutputFeature",
         "sourceOutputFeature =     if connectorEnd->isEmpty() or          connectorEnd.ownedFeatu"
         "re->isEmpty()     then null     else connectorEnd.ownedFeature->first()     endif"
        ),
    )

class Interaction(Behavior, Association):
    """<p>An <code>Interaction</code> is a <code>Behavior</code> that is also an <code>Association</code>, providing a context for multiple objects that have behaviors that impact one another.</p>"""
    _PKG = "Interactions"

class FlowDefinition(ActionDefinition, Interaction):
    """<p>A <code>FlowDefinition</code> is an <code>ActionDefinition</code> that is also an <code>Interaction</code> (which is both a KerML <code>Behavior</code> and <code>Association</code>), representing flows between <code>Usages</code>.</p>"""
    _PKG = "Flows"
    _DECL = {
    # <p>The <code>Usages</code> that define the things related by the <code>FlowDefinition</code>.</p
    # >
    'flowEnd': _Ref('flowEnd', "Usage", derived=True, multi=True, lo=0, hi='*', assoc="Systems-Flows-A_flowEnd_flowDefinitionWithEnd"),
    }
    CONSTRAINTS = (
        ("checkFlowDefinitionSpecialization",
         "specializesFromLibrary('Flows::MessageAction')"
        ),
        ("checkFlowDefinitionBinarySpecialization",
         "flowEnd->size() = 2 implies specializesFromLibrary('Flows::Message')"
        ),
        ("validateFlowDefinitionFlowEnds",
         "flowEnd->size() <= 2"
        ),
    )

class FlowEnd(Feature):
    """<p>A <code>FlowEnd</code> is a <code>Feature</code> that is one of the <code>connectorEnds</code> giving the <code><em>source</em></code> or <code><em>target</em></code> of a <code>Flow</code>. For <code>Flows</code> typed by <code><em>FlowTransfer</em></code> or its specializations, <code>FlowEnds</code> must have exactly one <code>ownedFeature</code>, which redefines <code><em>Transfer::source::sourceOutput</em></code> or <code><em>Transfer::target::targetInput</em></code> and redefines the corresponding feature of the <code>relatedElement</code> for its end.</p>"""
    _PKG = "Interactions"
    CONSTRAINTS = (
        ("validateFlowEndIsEnd",
         "isEnd"
        ),
        ("validateFlowEndNestedFeature",
         "ownedFeature->size() = 1"
        ),
        ("validateFlowEndOwningType",
         "owningType <> null and owningType.oclIsKindOf(Flow)"
        ),
    )

class FlowUsage(ActionUsage, ConnectorAsUsage, Flow):
    """<p>A <code>FlowUsage</code> is an <code>ActionUsage</code> that is also a <code>ConnectorAsUsage</code> and a KerML <code>Flow</code>.</p>"""
    _PKG = "Flows"
    _DECL = {
    # <p>The <code>Interactions</code> that are the <code>types</code> of this <code>FlowUsage</code>.
    #  Nominally, these are <code>FlowDefinitions</code>, but other kinds of Kernel <code>Interactions
    # </code> are also allowed, to permit use of Interactions from the Kernel Model Libraries.</p>
    'flowDefinition': _Ref('flowDefinition', "Interaction", derived=True, multi=True, lo=0, hi='*', redefines=("actionDefinition",), assoc="Systems-Flows-A_flowDefinition_definedFlow"),
    }
    CONSTRAINTS = (
        ("checkFlowUsageSpecialization",
         "specializesFromLibrary('Flows::messages')"
        ),
        ("checkFlowUsageFlowSpecialization",
         "ownedEndFeatures->notEmpty() implies specializesFromLibrary('Flows::flows')"
        ),
    )

class LoopActionUsage(ActionUsage):
    """<p>A <code>LoopActionUsage</code> is an <code>ActionUsage</code> that specifies that its <code>bodyAction</code> should be performed repeatedly. Its subclasses <code>WhileLoopActionUsage</code> and <code>ForLoopActionUsage</code> provide different ways to determine how many times the <code>bodyAction</code> should be performed.</p>"""
    _PKG = "Actions"
    _DECL = {
    # <p>The <code>ActionUsage</code> to be performed repeatedly by the <code>LoopActionUsage</code>. 
    # It is the second <code>parameter</code> of the <code>LoopActionUsage</code>.</p>
    'bodyAction': _Ref('bodyAction', "ActionUsage", derived=True, assoc="Systems-Actions-A_bodyAction_loopAction"),
    }
    CONSTRAINTS = (
        ("deriveLoopActionUsageBodyAction",
         "bodyAction =     let parameter : Feature = inputParameter(2) in     if parameter <> null"
         " and parameter.oclIsKindOf(Action) then         parameter.oclAsType(Action)     else    "
         "     null     endif"
        ),
    )

class ForLoopActionUsage(LoopActionUsage):
    """<p>A <code>ForLoopActionUsage</code> is a <code>LoopActionUsage</code> that specifies that its <code>bodyAction</code> <code>ActionUsage</code> should be performed once for each value, in order, from the sequence of values obtained as the result of the <code>seqArgument</code> <code>Expression</code>, with the <code>loopVariable</code> set to the value for each iteration.</p>"""
    _PKG = "Actions"
    _DECL = {
    # <p>The <code>ownedFeature</code> of this <co>ForLoopActionUsage</code> that acts as the loop var
    # iable, which is assigned the successive values of the input sequence on each iteration. It is th
    # e <code>ownedFeature</code> that redefines <em><code>ForLoopAction::var</code></em>.</p>
    'loopVariable': _Ref('loopVariable', "ReferenceUsage", derived=True, assoc="Systems-Actions-A_loopVariable_forLoopAction"),
    # <p>The <code>Expression</code> whose result provides the sequence of values to which the <code>l
    # oopVariable</code> is set for each iterative performance of the <code>bodyAction</code>. It is t
    # he <code>Expression</code> whose <code>result</code> is bound to the <em><code>seq</code></em> <
    # code>input</code> <code>parameter</code> of this <code>ForLoopActionUsage</code>.</p>
    'seqArgument': _Ref('seqArgument', "Expression", derived=True, assoc="Systems-Actions-A_seqArgument_forLoopAction"),
    }
    CONSTRAINTS = (
        ("checkForLoopActionUsageSubactionSpecialization",
         "isSubactionUsage() implies specializesFromLibrary('Actions::Action::forLoops')"
        ),
        ("checkForLoopActionUsageVarRedefinition",
         "loopVariable <> null and loopVariable.redefinesFromLibrary('Actions::ForLoopAction::var'"
         ")"
        ),
        ("validateForLoopActionUsageLoopVariable",
         "ownedFeature->notEmpty() and ownedFeature->at(1).oclIsKindOf(ReferenceUsage)"
        ),
        ("deriveForLoopActionUsageLoopVariable",
         "loopVariable =     if ownedFeature->isEmpty() or          not ownedFeature->first().oclI"
         "sKindOf(ReferenceUsage) then          null     else          ownedFeature->first().oclAs"
         "Type(ReferenceUsage)     endif"
        ),
        ("validateForLoopActionUsageParameters",
         "inputParameters()->size() = 2"
        ),
        ("deriveForLoopActionUsageSeqArgument",
         "seqArgument = argument(1)"
        ),
        ("checkForLoopActionUsageSpecialization",
         "specializesFromLibrary('Actions::forLoopActions')"
        ),
    )

class ForkNode(ControlNode):
    """<p>A <code>ForkNode</code> is a <code>ControlNode</code> that must be followed by successor <code>Actions</code> as given by all its outgoing <code>Successions</code>.</p>"""
    _PKG = "Actions"
    CONSTRAINTS = (
        ("validateForkNodeIncomingSuccessions",
         "targetConnector->selectByKind(Succession)->size() <= 1"
        ),
        ("checkForkNodeSpecialization",
         "specializesFromLibrary('Actions::Action::forks')"
        ),
    )

class RequirementConstraintMembership(FeatureMembership):
    """<p>A <code>RequirementConstraintMembership</code> is a <code>FeatureMembership</code> for an assumed or required <code>ConstraintUsage</code> of a <code>RequirementDefinition</code> or <code>RequirementUsage<code>.</p>"""
    _PKG = "Requirements"
    _DECL = {
    # <p>Whether the <code>RequirementConstraintMembership</code> is for an assumed or required <code>
    # ConstraintUsage</code>.</p>
    'kind': _Ref('kind', None),
    # <p>The <code>ConstraintUsage</code> that is the <code>ownedMemberFeature</code> of this <code>Re
    # quirementConstraintMembership</code>.</p>
    'ownedConstraint': _Ref('ownedConstraint', "ConstraintUsage", derived=True, composite=True, assoc="Systems-Requirements-A_ownedConstraint_requirementConstraintMembership"),
    # <p> The <code>ConstraintUsage</code> that is referenced through this <code>RequirementConstraint
    # Membership</code>. It is the <code>referencedFeature</code> of the <code>ownedReferenceSubsettin
    # g</code> of the <code>ownedConstraint</code>, if there is one, and, otherwise, the <code>ownedCo
    # nstraint</code> itself.</p>
    'referencedConstraint': _Ref('referencedConstraint', "ConstraintUsage", derived=True, assoc="Systems-Requirements-A_referencedConstraint_referencingConstraintMembership"),
    }
    CONSTRAINTS = (
        ("validateRequirementConstraintMembershipIsComposite",
         "ownedConstraint.isComposite"
        ),
        ("deriveRequirementConstraintMembershipReferencedConstraint",
         "referencedConstraint =     let referencedFeature : Feature =          ownedConstraint.re"
         "ferencedFeatureTarget() in     if referencedFeature = null then ownedConstraint     else"
         " if referencedFeature.oclIsKindOf(ConstraintUsage) then         refrencedFeature.oclAsTy"
         "pe(ConstraintUsage)     else null     endif endif"
        ),
        ("validateRequirementConstraintMembershipOwningType",
         "owningType.oclIsKindOf(RequirementDefinition) or owningType.oclIsKindOf(RequirementUsage"
         ")"
        ),
    )

class FramedConcernMembership(RequirementConstraintMembership):
    """<p>A <code>FramedConcernMembership</code> is a <code>RequirementConstraintMembership</code> for a framed <code>ConcernUsage</code> of a <code>RequirementDefinition</code> or <code>RequirementUsage</code>.</p>"""
    _PKG = "Requirements"
    _DECL = {
    # <p>The <code>kind</code> of an <code>FramedConcernMembership</code> must be <code>requirement</c
    # ode>.</p>
    'kind': _Ref('kind', None, redefines=("kind",)),
    # <p>The <code>ConcernUsage</code> that is the <code>ownedConstraint</code> of this <code>FramedCo
    # ncernMembership</code>.</p>
    'ownedConcern': _Ref('ownedConcern', "ConcernUsage", derived=True, composite=True, redefines=("ownedConstraint",), assoc="Systems-Requirements-A_ownedConcern_framedConstraintMembership"),
    # <p> The <code>ConcernUsage</code> that is referenced through this <code>FramedConcernMembership<
    # /code>. It is the <code>referencedConstraint</code> of the <code>FramedConcernMembership</code> 
    # considered as a <code>RequirementConstraintMembership</code>, which must be a <code>ConcernUsage
    # </code>.</p>
    'referencedConcern': _Ref('referencedConcern', "ConcernUsage", derived=True, redefines=("referencedConstraint",), assoc="Systems-Requirements-A_referencedConcern_referencingConcernMembership"),
    }
    CONSTRAINTS = (
        ("validateFramedConcernMembershipConstraintKind",
         "kind = RequirementConstraintKind::requirement"
        ),
    )

class IfActionUsage(ActionUsage):
    """<p>An <code>IfActionUsage</code> is an <code>ActionUsage</code> that specifies that the <code>thenAction</code> <code>ActionUsage</code> should be performed if the result of the <code>ifArgument</code> <code>Expression</code> is true. It may also optionally specify an <code>elseAction</code> <code>ActionUsage</code> that is performed if the result of the <code>ifArgument</code> is false.</p>"""
    _PKG = "Actions"
    _DECL = {
    # <p>The <code>ActionUsage</code> that is to be performed if the result of the <code>ifArgument</c
    # ode> is false. It is the (optional) third <code>parameter</code> of the <code>IfActionUsage</cod
    # e>.</p>
    'elseAction': _Ref('elseAction', "ActionUsage", derived=True, assoc="Systems-Actions-A_elseAction_ifElseAction"),
    # <p>The <code>Expression</code> whose result determines whether the <code>thenAction</code> or (o
    # ptionally) the <code>elseAction</code> is performed. It is the first <code>parameter<code> of th
    # e <code>IfActionUsage</code>.</p>
    'ifArgument': _Ref('ifArgument', "Expression", derived=True, assoc="Systems-Actions-A_ifArgument_ifAction"),
    # <p>The <code>ActionUsage</code> that is to be performed if the result of the <code>ifArgument</c
    # ode> is true. It is the second <code>parameter<code> of the <code>IfActionUsage</code>.</p>
    'thenAction': _Ref('thenAction', "ActionUsage", derived=True, assoc="Systems-Actions-A_thenAction_ifThenAction"),
    }
    CONSTRAINTS = (
        ("deriveIfActionUsageThenAction",
         "thenAction =      let parameter : Feature = inputParameter(2) in     if parameter <> nul"
         "l and parameter.oclIsKindOf(ActionUsage) then         parameter.oclAsType(ActionUsage)  "
         "   else         null     endif"
        ),
        ("checkIfActionUsageSpecialization",
         "if elseAction = null then     specializesFromLibrary('Actions::ifThenActions') else     "
         "specializesFromLibrary('Actions::ifThenElseActions') endif"
        ),
        ("validateIfActionUsageParameters",
         "inputParameters()->size() >= 2"
        ),
        ("deriveIfActionUsageElseAction",
         "elseAction =      let parameter : Feature = inputParameter(3) in     if parameter <> nul"
         "l and parameter.oclIsKindOf(ActionUsage) then         parameter.oclAsType(ActionUsage)  "
         "   else         null     endif"
        ),
        ("deriveIfActionUsageIfArgument",
         "ifArgument =      let parameter : Feature = inputParameter(1) in     if parameter <> nul"
         "l and parameter.oclIsKindOf(Expression) then         parameter.oclAsType(Expression)    "
         " else         null     endif"
        ),
        ("checkIfActionUsageSubactionSpecialization",
         "isSubactionUsage() implies specializesFromLibrary('Actions::Action::ifSubactions')"
        ),
    )

class UseCaseUsage(CaseUsage):
    """<p>A <code>UseCaseUsage</code> is a <code>Usage</code> of a <code>UseCaseDefinition</code>.</p>"""
    _PKG = "UseCases"
    _DECL = {
    # <p>The <code>UseCaseUsages</code> that are included by this <code>UseCaseUse</code>, which are t
    # he <code>useCaseIncludeds</code> of the <code>IncludeUseCaseUsages</code> owned by this <code>Us
    # eCaseUsage<code>.</p>
    'includedUseCase': _Ref('includedUseCase', "UseCaseUsage", derived=True, multi=True, lo=0, hi='*', assoc="Systems-UseCases-A_includedUseCase_includingUseCase"),
    # <p>The <code>UseCaseDefinition</code> that is the <code>definition</code> of this <code>UseCaseU
    # sage</code>.</p>
    'useCaseDefinition': _Ref('useCaseDefinition', "UseCaseDefinition", derived=True, redefines=("caseDefinition",), assoc="Systems-UseCases-A_useCaseDefinition_definedUseCase"),
    }
    CONSTRAINTS = (
        ("checkUseCaseUsageSubUseCaseSpecialization",
         "isComposite and owningType <> null and (owningType.oclIsKindOf(UseCaseDefinition) or  ow"
         "ningType.oclIsKindOf(UseCaseUsage)) implies     specializesFromLibrary('UseCases::UseCas"
         "e::subUseCases')"
        ),
        ("deriveUseCaseUsageIncludedUseCase",
         "includedUseCase = ownedUseCase-> selectByKind(IncludeUseCaseUsage). useCaseIncluded"
        ),
        ("checkUseCaseUsageSpecialization",
         "specializesFromLibrary('UseCases::useCases')"
        ),
    )

class IncludeUseCaseUsage(UseCaseUsage, PerformActionUsage):
    """<p>An <code>IncludeUseCaseUsage</code> is a <code>UseCaseUsage</code> that represents the inclusion of a <code>UseCaseUsage</code> by a <code>UseCaseDefinition</code> or <code>UseCaseUsage</code>. Unless it is the <code>IncludeUseCaseUsage</code> itself, the <code>UseCaseUsage</code> to be included is related to the <code>includedUseCase</code> by a <code>ReferenceSubsetting</code> <code>Relationship</code>. An <code>IncludeUseCaseUsage</code> is also a PerformActionUsage, with its <code>useCaseIncluded</code> as the <code>performedAction</code>.</p>"""
    _PKG = "UseCases"
    _DECL = {
    # <p>The <code>UseCaseUsage</code> to be included by this <code>IncludeUseCaseUsage</code>. It is 
    # the <code>performedAction</code> of the <code>IncludeUseCaseUsage</code> considered as a <code>P
    # erformActionUsage</code>, which must be a <code>UseCaseUsage</code>.</p>
    'useCaseIncluded': _Ref('useCaseIncluded', "UseCaseUsage", derived=True, redefines=("performedAction",), assoc="Systems-UseCases-A_useCaseIncluded_useCaseInclusion"),
    }
    CONSTRAINTS = (
        ("checkIncludeUseCaseSpecialization",
         "owningType <> null and (owningType.oclIsKindOf(UseCaseDefinition) or  owningType.oclIsKi"
         "ndOf(UseCaseUsage) implies     specializesFromLibrary('UseCases::UseCase::includedUseCas"
         "es')"
        ),
        ("validateIncludeUseCaseUsageReference",
         "referencedFeatureTarget() <> null implies referencedFeatureTarget().oclIsKindOf(UseCaseU"
         "sage)"
        ),
    )

class IndexExpression(OperatorExpression):
    """<p>An <code>IndexExpression</code> is an <code>OperatorExpression</code> whose operator is <code>"#"</code>, which resolves to the <code>Function</code> <em><code>BasicFunctions::'#'</code></em> from the Kernel Functions Library.</p>"""
    _PKG = "Expressions"
    _DECL = {
    'operator': _Ref('operator', str, redefines=("operator",)),
    }
    CONSTRAINTS = (
        ("checkIndexExpressionResultSpecialization",
         "arguments->notEmpty() and  not arguments->first().result.specializesFromLibrary('Collect"
         "ions::Array') implies     result.specializes(arguments->first().result)"
        ),
        ("validateIndexExpressionOperator",
         "operator = '#'"
        ),
    )

class InterfaceDefinition(ConnectionDefinition):
    """<p>An <code>InterfaceDefinition</code> is a <code>ConnectionDefinition</code> all of whose ends are <code>PortUsages</code>, defining an interface between elements that interact through such ports.</p>"""
    _PKG = "Interfaces"
    _DECL = {
    # <p>The <code>PortUsages</code> that are the <code>connectionEnds</code> of this <code>InterfaceD
    # efinition</code>.
    'interfaceEnd': _Ref('interfaceEnd', "PortUsage", derived=True, multi=True, lo=0, hi='*', redefines=("connectionEnd",), assoc="Systems-Interfaces-A_interfaceEnd_interfaceDefinitionWithEnd"),
    }
    CONSTRAINTS = (
        ("checkInterfaceDefinitionSpecialization",
         "specializesFromLibrary('Interfaces::Interface')"
        ),
        ("checkInterfaceDefinitionBinarySpecialization",
         "ownedEndFeature->size() = 2 implies specializesFromLibrary('Interfaces::BinaryInterface'"
         ")"
        ),
    )

class InterfaceUsage(ConnectionUsage):
    """<p>An <code>InterfaceUsage</code> is a Usage of an <code>InterfaceDefinition</code> to represent an interface connecting parts of a system through specific ports.</p>"""
    _PKG = "Interfaces"
    _DECL = {
    # <p>The <code>InterfaceDefinitions</code> that type this <code>InterfaceUsage</code>.</p>
    'interfaceDefinition': _Ref('interfaceDefinition', "InterfaceDefinition", derived=True, multi=True, lo=0, hi='*', redefines=("connectionDefinition",), assoc="Systems-Interfaces-A_interfaceDefinition_definedInterface"),
    }
    CONSTRAINTS = (
        ("checkInterfaceUsageBinarySpecialization",
         "ownedEndFeature->size() = 2 implies specializesFromLibrary('Interfaces::binaryInterfaces"
         "')"
        ),
        ("checkInterfaceUsageSpecialization",
         "specializesFromLibrary('Interfaces::interfaces')"
        ),
    )

class Intersecting(Relationship):
    """<p><code>Intersecting</code> is a <code>Relationship</code> that makes its <code>intersectingType</code> one of the <code>intersectingTypes</code> of its <code>typeIntersected</code>.</p>"""
    _PKG = "Types"
    _DECL = {
    # <p><code>Type</code> that partly determines interpretations of <code>typeIntersected</code>, as 
    # described in <code>Type::intersectingType</code>.</p>
    'intersectingType': _Ref('intersectingType', "Type", redefines=("target",), assoc="Core-Types-A_intersectingType_intersectedIntersecting"),
    # <p><code>Type</code> with interpretations partly determined by <code>intersectingType</code>, as
    #  described in <code>Type::intersectingType</code>.</p>
    'typeIntersected': _Ref('typeIntersected', "Type", derived=True, subsets=("owningRelatedElement",), redefines=("source",), assoc="Core-Types-A_ownedIntersecting_typeIntersected"),
    }

class JoinNode(ControlNode):
    """<p>A <code>JoinNode</code> is a <code>ControlNode</code> that waits for the completion of all the predecessor <code>Actions</code> given by incoming <code>Successions</code>.</p>"""
    _PKG = "Actions"
    CONSTRAINTS = (
        ("validateJoinNodeOutgoingSuccessions",
         "sourceConnector->selectByKind(Succession)->size() <= 1"
        ),
        ("checkJoinNodeSpecialization",
         "specializesFromLibrary('Actions::Action::join')"
        ),
    )

class Package(Namespace):
    """<p>A <code>Package</code> is a <code>Namespace</code> used to group <code>Elements</code>, without any instance-level semantics. It may have one or more model-level evaluable <code>filterCondition</code> <code>Expressions</code> used to filter its <code>importedMemberships</code>. Any imported <code>member</code> must meet all of the <code>filterConditions</code>.</p>"""
    _PKG = "Packages"
    _DECL = {
    # <p>The model-level evaluable <code><em>Boolean</em></code>-valued <code>Expression</code> used t
    # o filter the <code>members</code> of this <code>Package</code>, which are owned by the <code>Pac
    # kage</code> are via <code>ElementFilterMemberships</code>.</p>
    'filterCondition': _Ref('filterCondition', "Expression", derived=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="Kernel-Packages-A_filterCondition_conditionedPackage"),
    }
    CONSTRAINTS = (
        ("derivePackageFilterCondition",
         "filterCondition = ownedMembership-> selectByKind(ElementFilterMembership).condition"
        ),
    )
    def importedMemberships(self, excluded: None = None, arg: None = None) -> None:
        """
        <p>Exclude <code>Elements</code> that do not meet all the <code>filterConditions</code>.</p>
        [Package operation; params: excluded: ?, arg: ?; returns: nothing; stub - metamodel metadata o
        nly]
        """
        raise NotImplementedError
    def includeAsMember(self, element: None = None, arg: None = None) -> None:
        """
        <p>Determine whether the given <code>element</code> meets all the <code>filterConditions</code
        >.</p>
        [Package operation; params: element: ?, arg: ?; returns: nothing; stub - metamodel metadata on
        ly]
        """
        raise NotImplementedError

class LibraryPackage(Package):
    """<p>A <code>LibraryPackage</code> is a <code>Package</code> that is the container for a model library. A <code>LibraryPackage</code> is itself a library <code>Element</code> as are all <code>Elements</code> that are directly or indirectly contained in it.</p>"""
    _PKG = "Packages"
    _DECL = {
    # <p>Whether this <code>LibraryPackage</code> contains a standard library model. This should only 
    # be set to true for <code>LibraryPackages</code> in the standard Kernel Model Libraries or in nor
    # mative model libraries for a language built on KerML.</p>
    'isStandard': _Ref('isStandard', bool),
    }
    def libraryNamespace(self, arg: None = None) -> None:
        """
        <p>The <code>libraryNamespace</code> for a <code>LibraryPackage</code> is itself.</p>
        [LibraryPackage operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError

class LiteralExpression(Expression):
    """<p>A <code>LiteralExpression</code> is an <code>Expression</code> that provides a basic <code><em>DataValue</em></code> as a result.</p>"""
    _PKG = "Expressions"
    CONSTRAINTS = (
        ("deriveLiteralExpressionIsModelLevelEvaluable",
         "isModelLevelEvaluable = true"
        ),
        ("checkLiteralExpressionSpecialization",
         "specializesFromLibrary('Performances::literalEvaluations')"
        ),
    )
    def modelLevelEvaluable(self, arg: None = None, visited: None = None) -> None:
        """
        <p>A <code>LiteralExpression</code> is always model-level evaluable.</p>
        [LiteralExpression operation; params: arg: ?, visited: ?; returns: nothing; stub - metamodel m
        etadata only]
        """
        raise NotImplementedError
    def evaluate(self, target: None = None, result: None = None) -> None:
        """
        <p>The model-level value of a <code>LiteralExpression</code> is itself.</p>
        [LiteralExpression operation; params: target: ?, result: ?; returns: nothing; stub - metamodel
         metadata only]
        """
        raise NotImplementedError

class LiteralBoolean(LiteralExpression):
    """<p><code>LiteralBoolean</code> is a <code>LiteralExpression</code> that provides a <code><em>Boolean</em></code> value as a result. Its <code>result</code> <code>parameter</code> must have type <code><em>Boolean</em></code>.</p>"""
    _PKG = "Expressions"
    _DECL = {
    # <p>The <code><em>Boolean</em></code> value that is the result of evaluating this <code>LiteralBo
    # olean</code>.</p>
    'value': _Ref('value', bool),
    }
    CONSTRAINTS = (
        ("checkLiteralBooleanSpecialization",
         "specializesFromLibrary('Performances::literalBooleanEvaluations')"
        ),
    )

class LiteralInfinity(LiteralExpression):
    """<p>A <code>LiteralInfinity</code> is a <code>LiteralExpression</code> that provides the positive infinity value (<code>*</code>). It's <code>result</code> must have the type <code><em>Positive</em></code>.</p>"""
    _PKG = "Expressions"
    CONSTRAINTS = (
        ("checkLiteralInfinitySpecialization",
         "specializesFromLibrary('Performances::literalIntegerEvaluations')"
        ),
    )

class LiteralInteger(LiteralExpression):
    """<p>A <code>LiteralInteger</code> is a <code>LiteralExpression</code> that provides an <code><em>Integer</em></code> value as a result. Its <code>result</code> <code>parameter</code> must have the type <code><em>Integer</em></code>.</p>"""
    _PKG = "Expressions"
    _DECL = {
    # <p>The <code><em>Integer</em></code> value that is the result of evaluating this <code>LiteralIn
    # teger</code>.</p>
    'value': _Ref('value', int),
    }
    CONSTRAINTS = (
        ("checkLiteralIntegerSpecialization",
         "specializesFromLibrary('Performances::literalIntegerEvaluations')"
        ),
    )

class LiteralRational(LiteralExpression):
    """<p>A <code>LiteralRational</code> is a <code>LiteralExpression</code> that provides a <code><em>Rational</em></code> value as a result. Its <code>result</code> <code>parameter</code> must have the type <code><em>Rational</em></code>.</p>"""
    _PKG = "Expressions"
    _DECL = {
    # <p>The value whose rational approximation is the result of evaluating this <code>LiteralRational
    # </code>.</p>
    'value': _Ref('value', float),
    }
    CONSTRAINTS = (
        ("checkLiteralRationalSpecialization",
         "specializesFromLibrary('Performances::literalRationalEvaluations')"
        ),
    )

class LiteralString(LiteralExpression):
    """<p>A <code>LiteralString</code> is a <code>LiteralExpression</code> that provides a <code><em>String</em></code> value as a result. Its <code>result</code> <code>parameter</code> must have the type <code><em>String</em></code>.</p>"""
    _PKG = "Expressions"
    _DECL = {
    # <p>The String value that is the result of evaluating this Expression.</p>
    'value': _Ref('value', str),
    }
    CONSTRAINTS = (
        ("checkLiteralStringSpecialization",
         "specializesFromLibrary('Performances::literalStringEvaluations')"
        ),
    )

class MembershipImport(Import):
    """<p>A <code>MembershipImport</code> is an <code>Import</code> that imports its <code>importedMembership</code> into the <code>importOwningNamespace</code>. If <code>isRecursive = true</code> and the <code>memberElement</code> of the <code>importedMembership</code> is a <code>Namespace</code>, then the equivalent of a recursive <code>NamespaceImport</code> is also performed on that <code>Namespace</code>.</p>"""
    _PKG = "Namespaces"
    _DECL = {
    # <p>The <code>Membership</code> to be imported.</p>
    'importedMembership': _Ref('importedMembership', "Membership", redefines=("target",), assoc="Root-Namespaces-A_importedMembership_import"),
    }
    CONSTRAINTS = (
        ("deriveMembershipImportImportedElement",
         "importedElement = importedMembership.memberElement"
        ),
    )
    def importedMemberships(self, excluded: None = None, arg: None = None) -> None:
        """
        <p>Returns at least the <code>importedMembership</code>. If <code>isRecursive = true</code> an
        d the <code>memberElement</code> of the <code>importedMembership</code> is a <code>Namespace</
        code>, then <code>Memberships</code> are also recursively imported from that <code>Namespace</
        code>.</p>
        [MembershipImport operation; params: excluded: ?, arg: ?; returns: nothing; stub - metamodel m
        etadata only]
        """
        raise NotImplementedError

class MembershipExpose(MembershipImport, Expose):
    """<p>A <code>MembershipExpose</code> is an <code>Expose</code> <code.Relationship</code> that exposes a specific <code>importedMembership</code> and, if <code>isRecursive = true</code>, additional <code>Memberships</code> recursively.</p>"""
    _PKG = "Views"

class MergeNode(ControlNode):
    """<p>A <code>MergeNode</code> is a <code>ControlNode</code> that asserts the merging of its incoming <code>Successions</code>. A <code>MergeNode</code> may have at most one outgoing <code>Successions</code>.</p>"""
    _PKG = "Actions"
    CONSTRAINTS = (
        ("validateMergeNodeOutgoingSuccessions",
         "sourceConnector->selectAsKind(Succession)->size() <= 1"
        ),
        ("validateMergeNodeIncomingSuccessions",
         "targetConnector->selectByKind(Succession)->     collect(connectorEnd->at(1))->     forAl"
         "l(sourceMult |         multiplicityHasBounds(sourceMult, 0, 1))"
        ),
        ("checkMergeNodeIncomingSuccessionSpecialization",
         "targetConnector->selectByKind(Succession)->     forAll(subsetsChain(self,          resol"
         "veGlobal('ControlPerformances::MergePerformance::incomingHBLink')))"
        ),
        ("checkMergeNodeSpecialization",
         "specializesFromLibrary('Actions::Action::merges')"
        ),
    )

class Metaclass(Structure):
    """<p>A <code>Metaclass</code> is a <code>Structure</code> used to type <code>MetadataFeatures</code>.</p>"""
    _PKG = "Metadata"
    CONSTRAINTS = (
        ("checkMetaclassSpecialization",
         "specializesFromLibrary('Metaobjects::Metaobject')"
        ),
    )

class MetadataAccessExpression(Expression):
    """<p>A <code>MetadataAccessExpression</code> is an <code>Expression</code> whose <code>result</code> is a sequence of instances of <code>Metaclasses</code> representing all the <code>MetadataFeature</code> annotations of the <code>referencedElement</code>. In addition, the sequence includes an instance of the reflective <code>Metaclass</code> corresponding to the MOF class of the <code>referencedElement</code>, with values for all the abstract syntax properties of the <code>referencedElement</code>.</p>"""
    _PKG = "Expressions"
    _DECL = {
    # <p>The <code>Element</code> whose metadata is being accessed.</p>
    'referencedElement': _Ref('referencedElement', "Element", derived=True, subsets=("member",), assoc="Kernel-Expressions-A_referencedElement_accessExpression"),
    }
    CONSTRAINTS = (
        ("validateMetadataAccessExpressionReferencedElement",
         "ownedMembership->exists(not oclIsKindOf(FeatureMembership))"
        ),
        ("deriveMetadataAccessExpressionReferencdElement",
         "referencedElement =     let elements : Sequence(Element) = ownedMembership->         rej"
         "ect(oclIsKindOf(FeatureMembership)).memberElement in     if elements->isEmpty() then nul"
         "l     else elements->first()     endif"
        ),
        ("checkMetadataAccessExpressionSpecialization",
         "specializesFromLibrary('Performances::metadataAccessEvaluations')"
        ),
    )
    def modelLevelEvaluable(self, arg: None = None, visited: None = None) -> None:
        """
        <p>A <code>MetadataAccessExpression</code> is always model-level evaluable.</p>
        [MetadataAccessExpression operation; params: arg: ?, visited: ?; returns: nothing; stub - meta
        model metadata only]
        """
        raise NotImplementedError
    def evaluate(self, target: None = None, result: None = None) -> None:
        """
        <p>Return the <code>ownedElements</code> of the <code>referencedElement</code> that are <code>
        MetadataFeatures</code> and have the <code>referencedElement</code> as an <code>annotatedEleme
        nt</code>, plus a <code>MetadataFeature</code> whose <code>annotatedElement</code> is the <cod
        e>referencedElement</code>, whose <code>metaclass</code> is the reflective <code>Metaclass</co
        de> corresponding to the MOF class of the <code>referencedElement</code> and whose <code>owned
        Features</code> are bound to the values of the MOF properties of the <code>referencedElement</
        code>.</p>
        [MetadataAccessExpression operation; params: target: ?, result: ?; returns: nothing; stub - me
        tamodel metadata only]
        """
        raise NotImplementedError
    def metaclassFeature(self, arg: None = None) -> None:
        """
        <p>Return a <code>MetadataFeature</code> whose <code>annotatedElement</code> is the <code>refe
        rencedElement</code>, whose <code>metaclass</code> is the reflective <code>Metaclass</code> co
        rresponding to the MOF class of the <code>referencedElement</code> and whose <code>ownedFeatur
        es</code> are bound to the MOF properties of the <code>referencedElement</code>.</p>
        [MetadataAccessExpression operation; params: arg: ?; returns: nothing; stub - metamodel metada
        ta only]
        """
        raise NotImplementedError

class MetadataDefinition(ItemDefinition, Metaclass):
    """<p>A <code>MetadataDefinition</code> is an <code>ItemDefinition</code> that is also a <code>Metaclass</code>.</p>"""
    _PKG = "Metadata"
    CONSTRAINTS = (
        ("checkMetadataDefinitionSpecialization",
         "specializesFromLibrary('Metadata::MetadataItem')"
        ),
    )

class MetadataFeature(Feature, AnnotatingElement):
    """<p>A <code>MetadataFeature</code> is a <code>Feature</code> that is an <code>AnnotatingElement</code> used to annotate another <code>Element</code> with metadata. It is typed by a <code>Metaclass</code>. All its <code>ownedFeatures</code> must redefine <code>features</code> of its <code>metaclass</code> and any feature bindings must be model-level evaluable.</p>"""
    _PKG = "Metadata"
    _DECL = {
    # <p>The <code>type</code> of this <code>MetadataFeature</code>, which must be a <code>Metaclass</
    # code>.</p>
    'metaclass': _Ref('metaclass', "Metaclass", derived=True, subsets=("type",), assoc="Kernel-Metadata-A_metaclass_typedMetadata"),
    }
    CONSTRAINTS = (
        ("deriveMetadataFeatureMetaclass",
         "metaclass =      let metaclassTypes : Sequence(Type) = type->selectByKind(Metaclass) in "
         "    if metaclassTypes->isEmpty() then null     else metaClassTypes->first()     endif"
        ),
        ("validateMetadataFeatureMetaclass",
         "type->selectByKind(Metaclass).size() = 1"
        ),
        ("checkMetadataFeatureSpecialization",
         "specializesFromLibrary('Metaobjects::metaobjects')"
        ),
        ("validateMetadataFeatureMetaclassNotAbstract",
         "not metaclass.isAbstract"
        ),
        ("checkMetadataFeatureSemanticSpecialization",
         "isSemantic() implies     let annotatedTypes : Sequence(Type) =          annotatedElement"
         "->selectAsKind(Type) in     let baseTypes : Sequence(MetadataFeature) =          evaluat"
         "eFeature(resolveGlobal(             'Metaobjects::SemanticMetadata::baseType').         "
         "    memberElement.             oclAsType(Feature))->         selectAsKind(MetadataFeatur"
         "e) in     annotatedTypes->notEmpty() and      baseTypes()->notEmpty() and      baseTypes"
         "()->first().isSyntactic() implies         let annotatedType : Type = annotatedTypes->fir"
         "st() in         let baseType : Element = baseTypes->first().syntaxElement() in         i"
         "f annotatedType.oclIsKindOf(Classifier) and              baseType.oclIsKindOf(Feature) t"
         "hen             baseType.oclAsType(Feature).type->                 forAll(t | annotatedT"
         "ype.specializes(t))         else if baseType.oclIsKindOf(Type) then             annotate"
         "dType.specializes(baseType.oclAsType(Type))         else             true         endif"
        ),
        ("validateMetadataFeatureBody",
         "ownedFeature->closure(ownedFeature)->forAll(f |     f.declaredName = null and f.declared"
         "ShortName = null and     f.valuation <> null implies f.valuation.value.isModelLevelEvalu"
         "able and     f.redefinition.redefinedFeature->size() = 1)"
        ),
        ("validateMetadataFeatureAnnotatedElement",
         "let baseAnnotatedElementFeature : Feature =     resolveGlobal('Metaobjects::Metaobject::"
         "annotatedElement').memberElement.     oclAsType(Feature) in let annotatedElementFeatures"
         " : OrderedSet(Feature) = feature->     select(specializes(baseAnnotatedElementFeature))-"
         ">     excluding(baseAnnotatedElementFeature) in annotatedElementFeatures->notEmpty() imp"
         "lies     let annotatedElementTypes : Set(Feature) =         annotatedElementFeatures.typ"
         "ing.type->asSet() in     let metaclasses : Set(Metaclass) =         annotatedElement.ocl"
         "Type().qualifiedName->collect(qn |              resolveGlobal(qn).memberElement.oclAsTyp"
         "e(Metaclass)) in    metaclasses->forAll(m | annotatedElementTypes->exists(t | m.speciali"
         "zes(t)))"
        ),
    )
    def evaluateFeature(self, baseFeature: None = None, arg: None = None) -> None:
        """
        <p>If the given <code>baseFeature</code> is a <code>feature</code> of this <code>MetadataFeatu
        re</code>, or is directly or indirectly redefined by a <code>feature</code>, then return the r
        esult of evaluating the appropriate (model-level evaluable) <code>value</code> <code>Expressio
        n</code> for it (if any), with the <code>MetadataFeature</code> as the target.</p>
        [MetadataFeature operation; params: baseFeature: ?, arg: ?; returns: nothing; stub - metamodel
         metadata only]
        """
        raise NotImplementedError
    def isSemantic(self, arg: None = None) -> None:
        """
        <p>Check if this <code>MetadataFeature</code> has a <code>metaclass</code> which is a kind of 
        <code><em>SemanticMetadata</code>.<p>
        [MetadataFeature operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isSyntactic(self, arg: None = None) -> None:
        """
        <p>Check if this <code>MetadataFeature</code> has a <code>metaclass</code> that is a kind of <
        code><em>KerML::Element</em></code> (that is, it is from the reflective abstract syntax model)
        .</p>
        [MetadataFeature operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def syntaxElement(self, arg: None = None) -> None:
        """
        <p>If this <code>MetadataFeature</code> reflectively represents a model element, then return t
        he corresponding <code>Element</code> instance from the MOF abstract syntax representation of 
        the model.</p>
        [MetadataFeature operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError

class MetadataUsage(ItemUsage, MetadataFeature):
    """<p>A <code>MetadataUsage</code> is a <code>Usage</code> and a <code>MetadataFeature</code>, used to annotate other <code>Elements</code> in a system model with metadata. As a <code>MetadataFeature</code>, its type must be a <code>Metaclass</code>, which will nominally be a <code>MetadataDefinition</code>. However, any kernel <code>Metaclass</code> is also allowed, to permit use of <code>Metaclasses</code> from the Kernel Model Libraries.</p>"""
    _PKG = "Metadata"
    _DECL = {
    # <p>The <code>MetadataDefinition</code> that is the <code>definition</code> of this <code>Metadat
    # aUsage</code>.</p>
    'metadataDefinition': _Ref('metadataDefinition', "Metaclass", derived=True, redefines=("itemDefinition",), assoc="Systems-Metadata-A_metadataDefinition_definedMetadata"),
    }
    CONSTRAINTS = (
        ("checkMetadataUsageSpecialization",
         "specializesFromLibrary('Metadata::metadataItems')"
        ),
    )

class Multiplicity(Feature):
    """<p>A <code>Multiplicity</code> is a <code>Feature</code> whose co-domain is a set of natural numbers giving the allowed cardinalities of each <code>typeWithMultiplicity</code>. The <em>cardinality</em> of a <code>Type</code> is defined as follows, depending on whether the <code>Type</code> is a <code>Classifier</code> or <code>Feature</code>. <ul> <li><code>Classifier</code> – The number of basic instances of the <code>Classifier</code>, that is, those instances representing things, which are not instances of any subtypes of the <code>Classifier</code> that are <code>Features</code>. <li><code>Features</code> – The number of instances with the same featuring instances. In the case of a <code>Feature</code> with a <code>Classifier</code> as its <code>featuringType</code>, this is the number of values of <code>Feature</code> for each basic instance of the <code>Classifier</code>. Note that...[truncated]"""
    _PKG = "Types"
    CONSTRAINTS = (
        ("checkMultiplicityTypeFeaturing",
         "if owningType <> null and owningType.oclIsKindOf(Feature) then     featuringType =      "
         "    owningType.oclAsType(Feature).featuringType else     featuringType->isEmpty() endif"
        ),
        ("checkMultiplicitySpecialization",
         "specializesFromLibrary('Base::naturals')"
        ),
    )

class MultiplicityRange(Multiplicity):
    """<p>A <code>MultiplicityRange</code> is a <code>Multiplicity</code> whose value is defined to be the (inclusive) range of natural numbers given by the result of a <code>lowerBound</code> <code>Expression</code> and the result of an <code>upperBound</code> <code>Expression</code>. The result of these <code>Expressions</code> shall be of type <code><em>Natural</em></code>. If the result of the <code>upperBound</code> <code>Expression</code> is the unbounded value <code>*</code>, then the specified range includes all natural numbers greater than or equal to the <code>lowerBound</code> value. If no <code>lowerBound</code> <code>Expression</code>, then the default is that the lower bound has the same value as the upper bound, except if the <code>upperBound</code> evaluates to <code>*</code>, in which case the default for the lower bound is 0.</p>"""
    _PKG = "Multiplicities"
    _DECL = {
    # <p>The owned <code>Expressions</code> of the <code>MultiplicityRange</code> whose results provid
    # e its bounds. These must be the first <code>ownedMembers</code> of the <code>MultiplicityRange</
    # code>.</p>
    'bound': _Ref('bound', "Expression", derived=True, subsets=("ownedMember",), assoc="Kernel-Multiplicities-A_bound_multiplicity"),
    # <p>The <code>Expression</code> whose result provides the lower bound of the <code>MultiplicityRa
    # nge</code>. If no <code>lowerBound</code> <code>Expression</code> is given, then the lower bound
    #  shall have the same value as the upper bound, unless the upper bound is unbounded (<code>*</cod
    # e>), in which case the lower bound shall be 0.</p>
    'lowerBound': _Ref('lowerBound', "Expression", derived=True, subsets=("bound",), assoc="Kernel-Multiplicities-A_lowerBound_multiplicity"),
    # <p>The <code>Expression</code> whose result is the upper bound of the <code>MultiplicityRange</c
    # ode>.</p>
    'upperBound': _Ref('upperBound', "Expression", derived=True, subsets=("bound",), assoc="Kernel-Multiplicities-A_upperBound_multiplicity"),
    }
    CONSTRAINTS = (
        ("checkMultiplicityRangeExpressionTypeFeaturing",
         "bound->forAll(b | b.featuringType = self.featuringType)"
        ),
        ("deriveMultiplicityRangeBound",
         "bound =     if upperBound = null then Sequence{}     else if lowerBound = null then Sequ"
         "ence{upperBound}     else Sequence{lowerBound, upperBound}     endif endif"
        ),
        ("validateMultiplicityRangeBoundResultTypes",
         "bound->forAll(b |     b.result.specializesFromLibrary('ScalarValues::Integer') and     l"
         "et value : UnlimitedNatural = valueOf(b) in     value <> null implies value >= 0 )"
        ),
        ("validateMultiplicityRangeBounds",
         "if lowerBound = null then     ownedMember->notEmpty() and     ownedMember->at(1) = upper"
         "Bound else     ownedMember->size() > 1 and     ownedMember->at(1) = lowerBound and     o"
         "wnedMember->at(2) = upperBound endif"
        ),
        ("deriveMultiplicityRangeUpperBound",
         "upperBound =     let ownedExpressions : Sequence(Expression) =         ownedMember->sele"
         "ctByKind(Expression) in     if ownedExpressions->isEmpty() then null     else if ownedEx"
         "pressions->size() = 1 then ownedExpressions->at(1)     else ownedExpressions->at(2)     "
         "endif endif"
        ),
        ("deriveMultiplicityRangeLowerBound",
         "lowerBound =     let ownedExpressions : Sequence(Expression) =         ownedMember->sele"
         "ctByKind(Expression) in     if ownedExpressions->size() < 2 then null     else ownedExpr"
         "essions->first()     endif"
        ),
    )
    def hasBounds(self, lower: None = None, upper: None = None, arg: None = None) -> None:
        """
        <p>Check whether this <code>MultiplicityRange</code> represents the range bounded by the given
         values <code>lower</code> and <code>upper</code>, presuming the <code>lowerBound</code> and <
        code>upperBound</code> <code>Expressions</code> are model-level evaluable.</p>
        [MultiplicityRange operation; params: lower: ?, upper: ?, arg: ?; returns: nothing; stub - met
        amodel metadata only]
        """
        raise NotImplementedError
    def valueOf(self, bound: None = None, arg: None = None) -> None:
        """
        <p>Evaluate the given <code>bound</code> <code>Expression</code> (at model level) and return t
        he result represented as a MOF <code>UnlimitedNatural</code> value.</p>
        [MultiplicityRange operation; params: bound: ?, arg: ?; returns: nothing; stub - metamodel met
        adata only]
        """
        raise NotImplementedError

class NamespaceImport(Import):
    """<p>A <code>NamespaceImport</code> is an Import that imports <code>Memberships</code> from its <code>importedNamespace</code> into the <code>importOwningNamespace</code>. If <code> isRecursive = false</code>, then only the visible <code>Memberships</code> of the <code>importedNamespace</code> are imported. If <code> isRecursive = true</code>, then, in addition, <code>Memberships</code> are recursively imported from any <code>ownedMembers</code> of the <code>importedNamespace</code> that are <code>Namespaces</code>.</p>"""
    _PKG = "Namespaces"
    _DECL = {
    # <p>The <code>Namespace</code> whose visible <code>Memberships</code> are imported by this <code>
    # NamespaceImport</code>.</p>
    'importedNamespace': _Ref('importedNamespace', "Namespace", redefines=("target",), assoc="Root-Namespaces-A_importedNamespace_import"),
    }
    CONSTRAINTS = (
        ("deriveNamespaceImportImportedElement",
         "importedElement = importedNamespace"
        ),
    )
    def importedMemberships(self, excluded: None = None, arg: None = None) -> None:
        """
        <p>Returns at least the visible <code>Memberships</code> of the <code>importedNamespace</code>
        . If <code>isRecursive = true</code>, then <code>Memberships</code> are also recursively impor
        ted from any <code>ownedMembers</code> of the <code>importedNamespace</code> that are themselv
        es <code>Namespaces</code>.</p>
        [NamespaceImport operation; params: excluded: ?, arg: ?; returns: nothing; stub - metamodel me
        tadata only]
        """
        raise NotImplementedError

class NamespaceExpose(Expose, NamespaceImport):
    """<p>A <code>NamespaceExpose</code> is an <code>Expose</code> <code>Relationship</code> that exposes the <code>Memberships</code> of a specific <code>importedNamespace</code> and, if <code>isRecursive = true</code>, additional <code>Memberships</code> recursively.</p>"""
    _PKG = "Views"

class NullExpression(Expression):
    """<p>A <code>NullExpression</code> is an <code>Expression</code> that results in a null value.</p>"""
    _PKG = "Expressions"
    CONSTRAINTS = (
        ("checkNullExpressionSpecialization",
         "specializesFromLibrary('Performances::nullEvaluations')"
        ),
    )
    def modelLevelEvaluable(self, arg: None = None, visited: None = None) -> None:
        """
        <p>A <code>NullExpression</code> is always model-level evaluable.</p>
        [NullExpression operation; params: arg: ?, visited: ?; returns: nothing; stub - metamodel meta
        data only]
        """
        raise NotImplementedError
    def evaluate(self, target: None = None, result: None = None) -> None:
        """
        <p>The model-level value of a <code>NullExpression</code> is an empty sequence.</p>
        [NullExpression operation; params: target: ?, result: ?; returns: nothing; stub - metamodel me
        tadata only]
        """
        raise NotImplementedError

class ObjectiveMembership(FeatureMembership):
    """<p>An <code>ObjectiveMembership</code> is a <code>FeatureMembership</code> that indicates that its <code>ownedObjectiveRequirement</code> is the objective <code>RequirementUsage</code> for its <code>owningType</code>, which must be a <code>CaseDefinition</code> or <code>CaseUsage</code>.</p>"""
    _PKG = "Cases"
    _DECL = {
    # <p>The RequirementUsage that is the <code>ownedMemberFeature</code> of this RequirementUsage.</p
    # >
    'ownedObjectiveRequirement': _Ref('ownedObjectiveRequirement', "RequirementUsage", derived=True, composite=True, assoc="Systems-Cases-A_ownedObjectiveRequirement_owningObjectiveMembership"),
    }
    CONSTRAINTS = (
        ("validateObjectiveMembershipOwningType",
         "owningType.oclIsType(CaseDefinition) or owningType.oclIsType(CaseUsage)"
        ),
        ("validateObjectiveMembershipIsComposite",
         "ownedObjectiveRequirement.isComposite"
        ),
    )

class PayloadFeature(Feature):
    """<p>A <code>PayloadFeature</code> is the <code>ownedFeature</code> of a <code>Flow</code> that identifies the things carried by the kinds of transfers that are instances of the <code>Flow</code>.</p>"""
    _PKG = "Interactions"
    CONSTRAINTS = (
        ("checkPayloadFeatureRedefinition",
         "redefinesFromLibrary('Transfers::Transfer::payload')"
        ),
    )

class PortConjugation(Conjugation):
    """<p>A <code>PortConjugation</code> is a <code>Conjugation</code> <code>Relationship</code> between a <code>PortDefinition</code> and its corresponding <code>ConjugatedPortDefinition</code>. As a result of this <code>Relationship</code>, the <code>ConjugatedPortDefinition</code> inherits all the <code>features</code> of the original <code>PortDefinition</code>, but input <code>flows</code> of the original <code>PortDefinition</code> become outputs on the <code>ConjugatedPortDefinition</code> and output <code>flows</code> of the original <code>PortDefinition</code> become inputs on the <code>ConjugatedPortDefinition</code>.</code></p>"""
    _PKG = "Ports"
    _DECL = {
    # <p>The <code>ConjugatedPortDefinition</code> that is conjugate to the <code>originalPortDefiniti
    # on</code>.</p>
    'conjugatedPortDefinition': _Ref('conjugatedPortDefinition', "ConjugatedPortDefinition", derived=True, assoc="Systems-Ports-A_conjugatedPortDefinition_ownedPortConjugator"),
    # <p>The <code>PortDefinition</code> being conjugated.</p>
    'originalPortDefinition': _Ref('originalPortDefinition', "PortDefinition", assoc="Systems-Ports-A_originalPortDefinition_portConjugation"),
    }

class PortUsage(OccurrenceUsage):
    """<p>A <code>PortUsage</code> is a usage of a <code>PortDefinition</code>. A <code>PortUsage</code> itself as well as all its <code>nestedUsages</code> must be referential (non-composite).</p>"""
    _PKG = "Ports"
    _DECL = {
    # <p>The <code>occurrenceDefinitions</code> of this <code>PortUsage</code>, which must all be <cod
    # e>PortDefinitions<code>.</p>
    'portDefinition': _Ref('portDefinition', "PortDefinition", derived=True, multi=True, lo=0, hi='*', redefines=("occurrenceDefinition",), assoc="Systems-Ports-A_portDefinition_definedPort"),
    }
    CONSTRAINTS = (
        ("validatePortUsageNestedUsagesNotComposite",
         "nestedUsage-> reject(oclIsKindOf(PortUsage))-> forAll(not isComposite)"
        ),
        ("checkPortUsageSubportSpecialization",
         "isComposite and owningType <> null and (owningType.oclIsKindOf(PortDefinition) or  ownin"
         "gType.oclIsKindOf(PortUsage)) implies     specializesFromLibrary('Ports::Port::subports'"
         ")"
        ),
        ("validatePortUsageIsReference",
         "owningType = null or not owningType.oclIsKindOf(PortDefinition) and not owningType.oclIs"
         "KindOf(PortUsage) implies isReference"
        ),
        ("checkPortUsageSpecialization",
         "specializesFromLibrary('Ports::ports')"
        ),
        ("checkPortUsageOwnedPortSpecialization",
         "owningType <> null and (owningType.oclIsKindOf(PartDefinition) or  owningType.oclIsKindO"
         "f(PartUsage)) implies     specializesFromLibrary('Parts::Part::ownedPorts')"
        ),
    )

class Redefinition(Subsetting):
    """<p><code>Redefinition</code> is a kind of <code>Subsetting</code> that requires the <code>redefinedFeature</code> and the <code>redefiningFeature</code> to have the same values (on each instance of the domain of the <code>redefiningFeature</code>). This means any restrictions on the <code>redefiningFeature</code>, such as <code>type</code> or <code>multiplicity</code>, also apply to the <code>redefinedFeature</code> (on each instance of the domain of the <code>redefiningFeature</code>), and vice versa. The <code>redefinedFeature</code> might have values for instances of the domain of the <code>redefiningFeature</code>, but only as instances of the domain of the <code>redefinedFeature</code> that happen to also be instances of the domain of the <code>redefiningFeature</code>. This is supported by the constraints inherited from <code>Subsetting</code> on the domains of the <code>redefining...[truncated]"""
    _PKG = "Features"
    _DECL = {
    # <p>The <code>Feature</code> that is redefined by the <code>redefiningFeature</code> of this <cod
    # e>Redefinition</code>.</p>
    'redefinedFeature': _Ref('redefinedFeature', "Feature", redefines=("subsettedFeature",), assoc="Core-Features-A_redefinedFeature_redefining"),
    # <p>The <code>Feature</code> that is redefining the <code>redefinedFeature</code> of this <code>R
    # edefinition</code>.</p>
    'redefiningFeature': _Ref('redefiningFeature', "Feature", redefines=("subsettingFeature",), assoc="Core-Features-A_redefiningFeature_redefinition"),
    }
    CONSTRAINTS = (
        ("validateRedefinitionEndConformance",
         "redefinedFeature.isEnd implies redefiningFeature.isEnd"
        ),
        ("validateRedefinitionFeaturingTypes",
         "let anythingType: Type =     redefiningFeature.resolveGlobal('Base::Anything').modelElem"
         "ent.oclAsType(Type) in  -- Including \"Anything\" accounts for implicit featuringType of"
         " Features -- with no explicit featuringType. let redefiningFeaturingTypes: Set(Type) =  "
         "   if redefiningFeature.isVariable then Set{redefiningFeature.owningType}     else redef"
         "iningFeature.featuringTypes->asSet()->including(anythingType)      endif in let redefine"
         "dFeaturingTypes: Set(Type) =     if redefinedFeature.isVariable then Set{redefinedFeatur"
         "e.owningType}     else redefinedFeature.featuringTypes->asSet()->including(anythingType)"
         "     endif in redefiningFeaturingTypes <> redefinedFeaturingType"
        ),
        ("validateRedefinitionDirectionConformance",
         "let featuringTypes : Sequence(Type) =     if redefiningFeature.isVariable then Sequence{"
         "redefiningFeature.owningType}     else redefiningFeature.featuringType     endif in feat"
         "uringTypes->forAll(t |     let direction : FeatureDirectionKind = t.directionOf(redefine"
         "dFeature) in     ((direction = FeatureDirectionKind::_'in' or        direction = Feature"
         "DirectionKind::out) implies          redefiningFeature.direction = direction)     and   "
         "   (direction = FeatureDirectionKind::inout implies         redefiningFeature.direction "
         "<> null))"
        ),
    )

class ReferenceSubsetting(Subsetting):
    """<p><code>ReferenceSubsetting</code> is a kind of <code>Subsetting</code> in which the <code>referencedFeature</code> is syntactically distinguished from other <code>Features</code> subsetted by the <code>referencingFeature</code>. <code>ReferenceSubsetting</code> has the same semantics as <code>Subsetting</code>, but the <code>referencedFeature</code> may have a special purpose relative to the <code>referencingFeature</code>. For instance, <code>ReferenceSubsetting</code> is used to identify the <code>relatedFeatures</code> of a <code>Connector</code>.</p> <p><code>ReferenceSubsetting</code> is always an <code>ownedRelationship</code> of its <code>referencingFeature</code>. A <code>Feature</code> can have at most one <code>ownedReferenceSubsetting</code>.</p>"""
    _PKG = "Features"
    _DECL = {
    # <p>The <code>Feature</code> that is referenced by the <code>referencingFeature</code> of this <c
    # ode>ReferenceSubsetting</code>.</p>
    'referencedFeature': _Ref('referencedFeature', "Feature", redefines=("subsettedFeature",), assoc="Core-Features-A_referencedFeature_referencing"),
    # <p>The <code>Feature</code> that owns this <code>ReferenceSubsetting</code> relationship, which 
    # is also its <code>subsettingFeature</code>.</p>
    'referencingFeature': _Ref('referencingFeature', "Feature", derived=True, redefines=("owningFeature", "subsettingFeature",), assoc="Core-Features-A_ownedReferenceSubsetting_referencingFeature"),
    }

class ReferenceUsage(Usage):
    """<p>A <code>ReferenceUsage</code> is a <code>Usage</code> that specifies a non-compositional (<code>isComposite = false</code>) reference to something. The <code>definition</code> of a <code>ReferenceUsage</code> can be any kind of <code>Classifier</code>, with the default being the top-level <code>Classifier</code> <code><em>Base::Anything</em></code> from the Kernel Semantic Library. This allows the specification of a generic reference without distinguishing if the thing referenced is an attribute value, item, action, etc.</p>"""
    _PKG = "DefinitionAndUsage"
    _DECL = {
    # <p>Always <code>true</code> for a <code>ReferenceUsage</code>.</code>
    'isReference': _Ref('isReference', bool, derived=True, redefines=("isReference",)),
    }
    CONSTRAINTS = (
        ("validateReferenceUsageIsReference",
         "isReference"
        ),
    )
    def namingFeature(self, arg: None = None) -> None:
        """
        <p>If this <code>ReferenceUsage</code> is the <em><code>payload</code></em> <code>parameter</c
        ode> of a <code>TransitionUsage</code>, then its naming <code>Feature</code> is the <code>payl
        oadParameter</code> of the <code>triggerAction</code> of that <code>TransitionUsage</code> (if
         any).</p>
        [ReferenceUsage operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError

class RenderingDefinition(PartDefinition):
    """<p>A <code>RenderingDefinition</code> is a <code>PartDefinition</code> that defines a specific rendering of the content of a model view (e.g., symbols, style, layout, etc.).</p>"""
    _PKG = "Views"
    _DECL = {
    # <p>The <code>usages</code> of a <code>RenderingDefinition</code> that are <code>RenderingUsages<
    # /code>.</p>
    'rendering': _Ref('rendering', "RenderingUsage", derived=True, multi=True, lo=0, hi='*', subsets=("usage",), assoc="Systems-Views-A_rendering_featuringRenderingDefinition"),
    }
    CONSTRAINTS = (
        ("deriveRenderingDefinitionRendering",
         "rendering = usages->selectByKind(RenderingUsage)"
        ),
        ("checkRenderingDefinitionSpecialization",
         "specializesFromLibrary('Views::Rendering')"
        ),
    )

class RenderingUsage(PartUsage):
    """<p>A <code>RenderingUsage</code> is the usage of a <code>RenderingDefinition</code> to specify the rendering of a specific model view to produce a physical view artifact.</p>"""
    _PKG = "Views"
    _DECL = {
    # <p>The <code>RenderingDefinition</code> that is the <code>definition</code> of this <code>Render
    # ingUsage</code>.</p>
    'renderingDefinition': _Ref('renderingDefinition', "RenderingDefinition", derived=True, redefines=("partDefinition",), assoc="Systems-Views-A_renderingDefinition_definedRendering"),
    }
    CONSTRAINTS = (
        ("checkRenderingUsageSpecialization",
         "specializesFromLibrary('Views::renderings')"
        ),
        ("checkRenderingUsageSubrenderingSpecialization",
         "owningType <> null and (owningType.oclIsKindOf(RenderingDefinition) or  owningType.oclIs"
         "KindOf(RenderingUsage)) implies     specializesFromLibrary('Views::Rendering::subrenderi"
         "ngs')"
        ),
        ("checkRenderingUsageRedefinition",
         "owningFeatureMembership <> null and owningFeatureMembership.oclIsKindOf(ViewRenderingMem"
         "bership) implies     redefinesFromLibrary('Views::View::viewRendering')"
        ),
    )

class RequirementVerificationMembership(RequirementConstraintMembership):
    """<p>A <code>RequirementVerificationMembership</code> is a <code>RequirementConstraintMembership </code> used in the objective of a <code>VerificationCase</code> to identify a <code>RequirementUsage</code> that is verified by the <code>VerificationCase</code>.</p>"""
    _PKG = "VerificationCases"
    _DECL = {
    # <p>The <code>kind</code> of a <code>RequirementVerificationMembership</code> must be <code>requi
    # rement</code>.</p>
    'kind': _Ref('kind', None, redefines=("kind",)),
    # <p>The owned <code>RequirementUsage</code> that acts as the <code>ownedConstraint</code> for thi
    # s <code>RequirementVerificationMembership</code>. This will either be the <code>verifiedRequirem
    # ent</code>, or it will subset the <code>verifiedRequirement</code>.</p>
    'ownedRequirement': _Ref('ownedRequirement', "RequirementUsage", derived=True, composite=True, redefines=("ownedConstraint",), assoc="Systems-VerificationCases-A_ownedRequirement_requirementVerificationMembership"),
    # <p> The <code>RequirementUsage</code> that is identified as being verified. It is the <code>refe
    # rencedConstraint</code> of the <code>RequirementVerificationMembership</code> considered as a <c
    # ode>RequirementConstraintMembership</code>, which must be a <code>RequirementUsage</code>.</p>
    'verifiedRequirement': _Ref('verifiedRequirement', "RequirementUsage", derived=True, redefines=("referencedConstraint",), assoc="Systems-VerificationCases-A_verifiedRequirement_requirementVerification"),
    }
    CONSTRAINTS = (
        ("validateRequirementVerificationMembershipOwningType",
         "owningType.oclIsKindOf(RequirementUsage) and owningType.owningFeatureMembership <> null "
         "and owningType.owningFeatureMembership.oclIsKindOf(ObjectiveMembership)"
        ),
        ("validateRequirementVerificationMembershipKind",
         "kind = RequirementConstraintKind::requirement"
        ),
    )

class ResultExpressionMembership(FeatureMembership):
    """<p>A <code>ResultExpressionMembership</code> is a <code>FeatureMembership</code> that indicates that the <code>ownedResultExpression</code> provides the result values for the <code>Function</code> or <code>Expression</code> that owns it. The owning <code>Function</code> or <code>Expression</code> must contain a <code>BindingConnector</code> between the <code>result</code> <code>parameter</code> of the <code>ownedResultExpression</code> and the <code>result</code> <code>parameter</code> of the owning <code>Function</code> or <code>Expression</code>.</p>"""
    _PKG = "Functions"
    _DECL = {
    # <p>The <code>Expression</code> that provides the result for the owner of the <code>ResultExpress
    # ionMembership</code>.</p>
    'ownedResultExpression': _Ref('ownedResultExpression', "Expression", derived=True, composite=True, redefines=("ownedMemberFeature",), assoc="Kernel-Functions-A_ownedResultExpression_owningResultExpressionMembership"),
    }
    CONSTRAINTS = (
        ("validateResultExpressionMembershipOwningType",
         "owningType.oclIsKindOf(Function) or owningType.oclIsKindOf(Expression)"
        ),
    )

class ReturnParameterMembership(ParameterMembership):
    """<p>A <code>ReturnParameterMembership</code> is a <code>ParameterMembership</code> that indicates that the <code>ownedMemberParameter</code> is the <code>result</code> <code>parameter</code> of a <code>Function</code> or <code>Expression</code>. The <code>direction</code> of the <code>ownedMemberParameter</code> must be <code>out</code>.</p>"""
    _PKG = "Functions"
    CONSTRAINTS = (
        ("validateReturnParameterMembershipOwningType",
         "owningType.oclIsKindOf(Function) or owningType.oclIsKindOf(Expression)"
        ),
    )
    def parameterDirection(self, arg: None = None) -> None:
        """
        <p>The <code>ownedMemberParameter</code> of a <code>ReturnParameterMembership</code> must have
         direction <code>out</code>. (This is a leaf operation that cannot be further redefined.)</p>
        [ReturnParameterMembership operation; params: arg: ?; returns: nothing; stub - metamodel metad
        ata only]
        """
        raise NotImplementedError

class SatisfyRequirementUsage(RequirementUsage, AssertConstraintUsage):
    """<p>A <code>SatisfyRequirementUsage</code> is an <code>AssertConstraintUsage</code> that asserts, by default, that a satisfied <code>RequirementUsage</code> is true for a specific <code>satisfyingFeature</code>, or, if <code>isNegated = true</code>, that the <code>RequirementUsage</code> is false. The satisfied <code>RequirementUsage</code> is related to the <code>SatisfyRequirementUsage</code> by a <code>ReferenceSubsetting</code> <code>Relationship</code>.</p>"""
    _PKG = "Requirements"
    _DECL = {
    # <p>The <code>RequirementUsage</code> that is satisfied by the <code>satisfyingSubject</code> of 
    # this <code>SatisfyRequirementUsage</code>. It is the <code>assertedConstraint</code> of the <cod
    # e>SatisfyRequirementUsage</code> considered as an <code>AssertConstraintUsage</code>, which must
    #  be a <code>RequirementUsage</code>.</p>
    'satisfiedRequirement': _Ref('satisfiedRequirement', "RequirementUsage", derived=True, redefines=("assertedConstraint",), assoc="Systems-Requirements-A_satisfiedRequirement_requirementSatisfaction"),
    # <p>The <code>Feature</code> that represents the actual subject that is asserted to satisfy the <
    # code>satisfiedRequirement</code>. The <code>satisfyingFeature</code> is bound to the <code>subje
    # ctParameter</code> of the <code>SatisfyRequirementUsage</code>.</p>
    'satisfyingFeature': _Ref('satisfyingFeature', "Feature", derived=True, assoc="Systems-Requirements-A_satisfyingFeature_satisfiedRequirement"),
    }
    CONSTRAINTS = (
        ("checkSatisfyRequirementUsageBindingConnector",
         "ownedMember->selectByKind(BindingConnector)->     select(b |         b.relatedElement->i"
         "ncludes(subjectParameter) and         b.relatedElement->exists(r | r <> subjectParameter"
         "))->     size() = 1"
        ),
        ("checkSatisfyRequirementUsageSpecialization",
         "if isNegated then     specializesFromLibrary('Requirements::notSatisfiedRequirementCheck"
         "s') else     specializesFromLibrary('Requirements::satisfiedRequirementChecks') endif"
        ),
        ("deriveSatisfyRequirementUsageSatisfyingFeature",
         "satisfyingFeature =     let bindings: BindingConnector = ownedMember->         selectByK"
         "ind(BindingConnector)->         select(b | b.relatedElement->includes(subjectParameter))"
         " in     if bindings->isEmpty() or         bindings->first().relatedElement->exits(r | r "
         "<> subjectParameter)      then null     else bindings->first().relatedElement->any(r | r"
         " <> subjectParameter)     endif"
        ),
        ("validateSatisfyRequirementUsageReference",
         "referencedFeatureTarget() <> null implies referencedFeatureTarget().oclIsKindOf(Requirem"
         "entUsage)"
        ),
    )

class SelectExpression(OperatorExpression):
    """<p>A <code>SelectExpression</code> is an <code>OperatorExpression</code> whose operator is <code>"select"</code>, which resolves to the <code>Function</code> <em><code>ControlFunctions::select</code></em> from the Kernel Functions Library.</p>"""
    _PKG = "Expressions"
    _DECL = {
    'operator': _Ref('operator', str, redefines=("operator",)),
    }
    CONSTRAINTS = (
        ("validateSelectExpressionOperator",
         "operator = 'select'"
        ),
        ("checkSelectExpressionResultSpecialization",
         "arguments->notEmpty() implies result.specializes(arguments->first().result)"
        ),
    )

class SendActionUsage(ActionUsage):
    """<p>A <code>SendActionUsage</code> is an <code>ActionUsage</code> that specifies the sending of a payload given by the result of its <code>payloadArgument</code> <code>Expression</code> via a <em><code>MessageTransfer</code></em> whose <em><code>source</code></em> is given by the result of the <code>senderArgument</code> <code>Expression</code> and whose <code>target</code> is given by the result of the <code>receiverArgument</code> <code>Expression</code>. If no <code>senderArgument</code> is provided, the default is the <em><code>this</code></em> context for the action. If no <code>receiverArgument</code> is given, then the receiver is to be determined by, e.g., outgoing <em><code>Connections</code></em> from the sender.</p>"""
    _PKG = "Actions"
    _DECL = {
    # <p>An <code>Expression</code> whose result is bound to the <code><em>payload</em></code> input p
    # arameter of this <code>SendActionUsage</code>.</p>
    'payloadArgument': _Ref('payloadArgument', "Expression", derived=True, assoc="Systems-Actions-A_payloadArgument_sendingActionUsage"),
    # <p>An <code>Expression</code> whose result is bound to the <em><code>receiver</code></em> input 
    # parameter of this <code>SendActionUsage</code>.</p>
    'receiverArgument': _Ref('receiverArgument', "Expression", derived=True, assoc="Systems-Actions-A_receiverArgument_sendActionUsage"),
    # <p>An <code>Expression</code> whose result is bound to the <em><code>sender</code></em> input pa
    # rameter of this <code>SendActionUsage</code>.</p>
    'senderArgument': _Ref('senderArgument', "Expression", derived=True, assoc="Systems-Actions-A_senderArgument_senderActionUsage"),
    }
    CONSTRAINTS = (
        ("deriveSendActionUsageSenderArgument",
         "senderArgument = argument(2)"
        ),
        ("checkSendActionUsageSubactionSpecialization",
         "isSubactionUsage() implies specializesFromLibrary('Actions::Action::acceptSubactions')"
        ),
        ("deriveSendActionUsageReceiverArgument",
         "receiverArgument = argument(3)"
        ),
        ("validateSendActionParameters",
         "inputParameters()->size() >= 3"
        ),
        ("deriveSendActionUsagePayloadArgument",
         "payloadArgument = argument(1)"
        ),
        ("checkSendActionUsageSpecialization",
         "specializesFromLibrary('Actions::sendActions')"
        ),
    )

class StakeholderMembership(ParameterMembership):
    """<p>A <code>StakeholderMembership</code> is a <code>ParameterMembership</code> that identifies a <code>PartUsage</code> as a <code>stakeholderParameter</code> of a <code>RequirementDefinition</code> or <code>RequirementUsage</code>, which specifies a role played by an entity with concerns framed by the <code>owningType</code>.</p>"""
    _PKG = "Requirements"
    _DECL = {
    # <p>The <code>PartUsage</code> specifying the stakeholder.</p>
    'ownedStakeholderParameter': _Ref('ownedStakeholderParameter', "PartUsage", derived=True, composite=True, assoc="Systems-Requirements-A_ownedStakeholderParameter_owningStakeholderMembership"),
    }
    CONSTRAINTS = (
        ("validateStakeholderMembershipOwningType",
         "owningType.oclIsKindOf(RequirementUsage) or owningType.oclIsKindOf(RequirementDefinition"
         ")"
        ),
    )

class StateDefinition(ActionDefinition):
    """<p>A <code>StateDefinition</code> is the <code>Definition</code> of the </code>Behavior</code> of a system or part of a system in a certain state condition.</p> <p>A <code>StateDefinition</code> may be related to up to three of its <code>ownedFeatures</code> by <code>StateBehaviorMembership</code> <code>Relationships</code>, all of different <code>kinds</code>, corresponding to the entry, do and exit actions of the <code>StateDefinition</code>.</p>"""
    _PKG = "States"
    _DECL = {
    # <p>The <code>ActionUsage</code> of this <code>StateDefinition</code> to be performed while in th
    # e state defined by the <code>StateDefinition</code>. It is the owned <code>ActionUsage</code> re
    # lated to the <code>StateDefinition</code> by a <code>StateSubactionMembership</code> with <code>
    # kind = do</code>.</p>
    'doAction': _Ref('doAction', "ActionUsage", derived=True, assoc="Systems-States-A_doAction_activeStateDefintion"),
    # <p>The <code>ActionUsage</code> of this <code>StateDefinition</code> to be performed on entry to
    #  the state defined by the <code>StateDefinition</code>. It is the owned <code>ActionUsage</code>
    #  related to the <code>StateDefinition</code> by a <code>StateSubactionMembership</code> with <co
    # de>kind = entry</code>.</p>
    'entryAction': _Ref('entryAction', "ActionUsage", derived=True, assoc="Systems-States-A_entryAction_enteredStateDefinition"),
    # <p>The <code>ActionUsage</code> of this <code>StateDefinition</code> to be performed on exit to 
    # the state defined by the <code>StateDefinition</code>. It is the owned <code>ActionUsage</code> 
    # related to the <code>StateDefinition</code> by a <code>StateSubactionMembership</code> with <cod
    # e>kind = exit</code>.</p>
    'exitAction': _Ref('exitAction', "ActionUsage", derived=True, assoc="Systems-States-A_exitAction_exitedStateDefinition"),
    # <p>Whether the <code>ownedStates</code> of this <code>StateDefinition</code> are to all be perfo
    # rmed in parallel. If true, none of the <code>ownedActions</code> (which includes <code>ownedStat
    # es</code>) may have any incoming or outgoing <code>Transitions</code>. If false, only one <code>
    # ownedState</code> may be performed at a time.</p>
    'isParallel': _Ref('isParallel', bool),
    # <p>The <code>StateUsages</code>, which are <code>actions</code> in the <code>StateDefinition</co
    # de>, that specify the discrete states in the behavior defined by the <code>StateDefinition</code
    # >.</p>
    'state': _Ref('state', "StateUsage", derived=True, multi=True, lo=0, hi='*', subsets=("action",), assoc="Systems-States-A_state_featuringStateDefinition"),
    }
    CONSTRAINTS = (
        ("deriveStateDefinitionState",
         "state = action->selectByKind(StateUsage)"
        ),
        ("deriveStateDefinitionDoAction",
         "doAction =     let doMemberships : Sequence(StateSubactionMembership) =         ownedMem"
         "bership->             selectByKind(StateSubactionMembership)->             select(kind ="
         " StateSubactionKind::do) in     if doMemberships->isEmpty() then null     else doMembers"
         "hips->at(1)     endif"
        ),
        ("deriveStateDefinitionEntryAction",
         "entryAction =     let entryMemberships : Sequence(StateSubactionMembership) =         ow"
         "nedMembership->             selectByKind(StateSubactionMembership)->             select("
         "kind = StateSubactionKind::entry) in     if entryMemberships->isEmpty() then null     el"
         "se entryMemberships->at(1)     endif"
        ),
        ("checkStateDefinitionSpecialization",
         "specializesFromLibrary('States::StateAction')"
        ),
        ("validateStateDefinitionParallelSubactions",
         "isParallel implies ownedAction.incomingTransition->isEmpty() and ownedAction.outgoingTra"
         "nsition->isEmpty()"
        ),
        ("validateStateDefinitionStateSubactionKind",
         "ownedMembership-> selectByKind(StateSubactionMembership)-> isUnique(kind)"
        ),
        ("deriveStateDefinitionExitAction",
         "exitAction =      let exitMemberships : Sequence(StateSubactionMembership) =         own"
         "edMembership->             selectByKind(StateSubactionMembership)->             select(k"
         "ind = StateSubactionKind::exit) in     if exitMemberships->isEmpty() then null     else "
         "exitMemberships->at(1)     endif"
        ),
    )

class StateSubactionMembership(FeatureMembership):
    """<p>A <code>StateSubactionMembership</code> is a <code>FeatureMembership</code> for an entry, do or exit <code>ActionUsage<code> of a <code>StateDefinition</code> or <code>StateUsage</code>.</p>"""
    _PKG = "States"
    _DECL = {
    # <p>The <code>ActionUsage</code> that is the <code>ownedMemberFeature</code> of this <code>StateS
    # ubactionMembership</code>.</p>
    'action': _Ref('action', "ActionUsage", derived=True, assoc="Systems-States-A_action_stateSubactionMembership"),
    # <p>Whether this <code>StateSubactionMembership</code> is for an <code>entry<code>, <code>do</cod
    # e> or <code>exit</code> <code>ActionUsage</code>.</p>
    'kind': _Ref('kind', None),
    }
    CONSTRAINTS = (
        ("validateStateSubactionMembershipOwningType",
         "owningType.oclIsKindOf(StateDefinition) or owningType.oclIsKindOf(StateUsage)"
        ),
    )

class Subclassification(Specialization):
    """<p><code>Subclassification</code> is <code>Specialization</code> in which both the <code>specific</code> and <code>general</code> <code>Types</code> are <code>Classifier</code>. This means all instances of the specific <code>Classifier</code> are also instances of the general <code>Classifier</code>.</p>"""
    _PKG = "Classifiers"
    _DECL = {
    # <p>The <code>Classifier</code> that owns this <code>Subclassification</code> relationship, which
    #  must also be its <code>subclassifier</code>.</p>
    'owningClassifier': _Ref('owningClassifier', "Classifier", redefines=("owningType",), assoc="Core-Classifiers-A_owningClassifier_ownedSubclassification"),
    # <p>The more specific <code>Classifier</code> in this <code>Subclassification</code>.</p>
    'subclassifier': _Ref('subclassifier', "Classifier", redefines=("specific",), assoc="Core-Classifiers-A_subclassifier_subclassification"),
    # <p>The more <code>general</code> Classifier in this <code>Subclassification</code>.</p>
    'superclassifier': _Ref('superclassifier', "Classifier", redefines=("general",), assoc="Core-Classifiers-A_superclassifier_superclassification"),
    }

class SubjectMembership(ParameterMembership):
    """<p>A <code>SubjectMembership</code> is a <code>ParameterMembership</code> that indicates that its <code>ownedSubjectParameter</code> is the subject of its <code>owningType</code>. The <code>owningType</code> of a <code>SubjectMembership</code> must be a <code>RequirementDefinition</code>, <code>RequirementUsage</code>, <code>CaseDefinition</code>, or <code>CaseUsage</code>.</p>"""
    _PKG = "Requirements"
    _DECL = {
    # <p>The <code>Usage</code< that is the <code>ownedMemberParameter</code> of this <code>SubjectMem
    # bership</code>.</p>
    'ownedSubjectParameter': _Ref('ownedSubjectParameter', "Usage", derived=True, composite=True, assoc="Systems-Requirements-A_ownedSubjectParameter_owningSubjectMembership"),
    }
    CONSTRAINTS = (
        ("validateSubjectMembershipOwningType",
         "owningType.oclIsType(RequirementDefinition) or owningType.oclIsType(RequiremenCaseRequir"
         "ementDefinition) or owningType.oclIsType(CaseDefinition) or owningType.oclIsType(CaseUsa"
         "ge)"
        ),
    )

class Succession(Connector):
    """<p>A <code>Succession</code> is a binary <code>Connector</code> that requires its <code>relatedFeatures</code> to happen separately in time.</p>"""
    _PKG = "Connectors"
    CONSTRAINTS = (
        ("checkSuccessionSpecialization",
         "specializesFromLibrary('Occurrences::happensBeforeLinks')"
        ),
    )

class SuccessionAsUsage(ConnectorAsUsage, Succession):
    """<p>A <code>SuccessionAsUsage</code> is both a <code>ConnectorAsUsage</code> and a <code>Succession</code>.<p>"""
    _PKG = "Connections"

class SuccessionFlow(Succession, Flow):
    """<p>A <code>SuccessionFlow</code> is a <code>Flow</code> that also provides temporal ordering. It classifies <code><em>Transfers</em></code> that cannot start until the source <code><em>Occurrence</em></code> has completed and that must complete before the target <code><em>Occurrence</em></code> can start.</p>"""
    _PKG = "Interactions"
    CONSTRAINTS = (
        ("checkSuccessionFlowSpecialization",
         "specializesFromLibrary('Transfers::flowTransfersBefore')"
        ),
    )

class SuccessionFlowUsage(FlowUsage, SuccessionFlow):
    """<p>A <code>SuccessionFlowUsage</code> is a <code>FlowUsage</code> that is also a KerML <code>SuccessionFlow</code>.</p>"""
    _PKG = "Flows"
    CONSTRAINTS = (
        ("checkSuccessionFlowUsageSpecialization",
         "specializesFromLibrary('Flows::successionFlows')"
        ),
    )

class TerminateActionUsage(ActionUsage):
    """<p>A <code>TerminateActionUsage</code> is an <code>ActionUsage</code> that directly or indirectly specializes the <code>ActionDefinition</code> <em><code>TerminateAction</code></em> from the Systems Model Library, which causes a given <em><code>terminatedOccurrence</code></em> to end during its performance. By default, the <code>terminatedOccurrence</code> is the featuring instance (<em><code>that</code></em>) of the performance of the <code>TerminateActionUsage</code>, generally the performance of its immediately containing <code>ActionDefinition</code> or <code>ActionUsage</code>.</p>"""
    _PKG = "Actions"
    _DECL = {
    # <p>The <code>Expression</code> that is the <code>featureValue</code> of the <em><code>terminateO
    # ccurrence</code></em> <code>parameter</code> of this <code>TerminateActionUsage</code>.
    'terminatedOccurrenceArgument': _Ref('terminatedOccurrenceArgument', "Expression", derived=True, assoc="Systems-Actions-A_terminatedOccurrenceArgument_terminateActionUsage"),
    }
    CONSTRAINTS = (
        ("checkTerminateActionUsageSpecialization",
         "specializesFromLibrary('Actions::terminateActions')"
        ),
        ("deriveTerminateActionUsageTerminatedOccurrenceArgument",
         "terminatedOccurrenceArgument = argument(1)"
        ),
        ("checkTerminateActionUsageSubactionSpecialization",
         "isSubactionUsage() implies specializesFromLibrary('Actions::Action::terminateSubactions'"
         ")"
        ),
    )

class TextualRepresentation(AnnotatingElement):
    """<p>A <code>TextualRepresentation</code> is an <code>AnnotatingElement</code> whose <code>body</code> represents the <code>representedElement</code> in a given <code>language</code>. The <code>representedElement</code> must be the <code>owner</code> of the <code>TextualRepresentation</code>. The named <code>language</code> can be a natural language, in which case the <code>body</code> is an informal representation, or an artificial language, in which case the <code>body</code> is expected to be a formal, machine-parsable representation.</p> <p>If the named <code>language</code> of a <code>TextualRepresentation</code> is machine-parsable, then the <code>body</code> text should be legal input text as defined for that <code>language</code>. The interpretation of the named language string shall be case insensitive. The following <code>language</code> names are defined to correspond to the giv...[truncated]"""
    _PKG = "Annotations"
    _DECL = {
    # <p>The textual representation of the <code>representedElement</code> in the given <code>language
    # </code>.</p>
    'body': _Ref('body', str),
    # <p>The natural or artifical language in which the <code>body</code> text is written.</p>
    'language': _Ref('language', str),
    # <p>The <code>Element</code> that is represented by this <code>TextualRepresentation</code>.</p>
    'representedElement': _Ref('representedElement', "Element", derived=True, subsets=("owner",), redefines=("annotatedElement",), assoc="Root-Elements-A_textualRepresentation_representedElement"),
    }

class TransitionFeatureMembership(FeatureMembership):
    """<p>A <code>TransitionFeatureMembership</code> is a <code>FeatureMembership</code> for a trigger, guard or effect of a <code>TransitionUsage</code>, whose <code>transitionFeature</code> is a <code>AcceptActionUsage</code>, <em><code>Boolean</code></em>-valued <code>Expression</code> or <code>ActionUsage</code>, depending on its <code>kind</code>. </p>"""
    _PKG = "States"
    _DECL = {
    # <p>Whether this <code>TransitionFeatureMembership </code> is for a <code>trigger</code>, <code>g
    # uard</code> or <code>effect</code>.</p>
    'kind': _Ref('kind', None),
    # <p>The <code>Step</code> that is the <code>ownedMemberFeature</code> of this <code>TransitionFea
    # tureMembership</code>.</p>
    'transitionFeature': _Ref('transitionFeature', "Step", derived=True, assoc="Systems-States-A_transitionFeature_transitionFeatureMembership"),
    }
    CONSTRAINTS = (
        ("validateTransitionFeatureMembershipGuardExpression",
         "kind = TransitionFeatureKind::guard implies     transitionFeature.oclIsKindOf(Expression"
         ") and     let guard : Expression = transitionFeature.oclIsKindOf(Expression) in     guar"
         "d.result.specializesFromLibrary('ScalarValues::Boolean') and     guard.result.multiplici"
         "ty <> null and     guard.result.multiplicity.hasBounds(1,1)"
        ),
        ("validateTransitionFeatureMembershipOwningType",
         "owningType.oclIsKindOf(TransitionUsage)"
        ),
        ("validateTransitionFeatureMembershipEffectAction",
         "kind = TransitionFeatureKind::effect implies transitionFeature.oclIsKindOf(ActionUsage)"
        ),
        ("validateTransitionFeatureMembershipTriggerAction",
         "kind = TransitionFeatureKind::trigger implies transitionFeature.oclIsKindOf(AcceptAction"
         "Usage)"
        ),
    )

class TransitionUsage(ActionUsage):
    """<p>A <code>TransitionUsage</code> is an <code>ActionUsage</code> representing a triggered transition between <code>ActionUsages</code> or <code>StateUsages</code>. When triggered by a <code>triggerAction</code>, when its <code>guardExpression</code> is true, the <code>TransitionUsage</code> asserts that its <code>source</code> is exited, then its <code>effectAction</code> (if any) is performed, and then its <code>target</code> is entered.</p> <p>A <code>TransitionUsage</code> can be related to some of its <code>ownedFeatures</code> using <code>TransitionFeatureMembership</code> <code>Relationships</code>, corresponding to the <code>triggerAction</code>, <code>guardExpression</code> and <code>effectAction</code> of the <code>TransitionUsage</code>.</p>"""
    _PKG = "States"
    _DECL = {
    # <p>The <code>ActionUsages</code> that define the effects of this <code>TransitionUsage</code>, w
    # hich are the <code>ownedFeatures</code> of the <code>TransitionUsage</code> related to it by <co
    # de>TransitionFeatureMemberships</code> with <code>kind = effect</code>, which must all be <code>
    # ActionUsages</code>.</p>
    'effectAction': _Ref('effectAction', "ActionUsage", derived=True, multi=True, lo=0, hi='*', assoc="Systems-States-A_effectAction_activeTransition"),
    # <p>The <code>Expressions</code> that define the guards of this <code>TransitionUsage</code>, whi
    # ch are the <code>ownedFeatures</code> of the <code>TransitionUsage</code> related to it by <code
    # >TransitionFeatureMemberships</code> with <code>kind = guard</code>, which must all be <code>Exp
    # ressions</code>.</p>
    'guardExpression': _Ref('guardExpression', "Expression", derived=True, multi=True, lo=0, hi='*', assoc="Systems-States-A_guardExpression_guardedTransition"),
    # <p>The source <code>ActionUsage</code> of this <code>TransitionUsage</code>, which becomes the <
    # code>source</code> of the <code>succession</code> for the <code>TransitionUsage</code>.</p>
    'source': _Ref('source', "ActionUsage", derived=True, assoc="Systems-States-A_source_outgoingTransition"),
    # <p>The <code>Succession</code> that is the <code>ownedFeature</code> of this <code>TransitionUsa
    # ge</code>, which, if the <code>TransitionUsage</code> is triggered, asserts the temporal orderin
    # g of the <code>source</code> and <code>target</code>.</p>
    'succession': _Ref('succession', "Succession", derived=True, assoc="Systems-States-A_succession_linkedTransition"),
    # <p>The target <code>ActionUsage</code> of this <code>TransitionUsage<code>, which is the <code>t
    # argetFeature</code> of the <code>succession</code> for the <code>TransitionUsage</code>.</p>
    'target': _Ref('target', "ActionUsage", derived=True, assoc="Systems-States-A_target_incomingTransition"),
    # <p>The <code>AcceptActionUsages</code> that define the triggers of this <code>TransitionUsage</c
    # ode>, which are the <code>ownedFeatures</code> of the <code>TransitionUsage</code> related to it
    #  by <code>TransitionFeatureMemberships</code> with <code>kind = trigger</code>, which must all b
    # e <code>AcceptActionUsages</code>.</p>
    'triggerAction': _Ref('triggerAction', "AcceptActionUsage", derived=True, multi=True, lo=0, hi='*', assoc="Systems-States-A_triggerAction_triggeredTransition"),
    }
    CONSTRAINTS = (
        ("deriveTransitionUsageTarget",
         "target =     if succession.targetFeature->isEmpty() then null     else         let targe"
         "tFeature : Feature =             succession.targetFeature->first().featureTarget in     "
         "    if not targetFeature.oclIsKindOf(ActionUsage) then null         else targetFeature.o"
         "clAsType(ActionUsage)         endif     endif"
        ),
        ("checkTransitionUsageSpecialization",
         "specializesFromLibrary('Actions::transitionActions')"
        ),
        ("validateTransitionUsageSuccession",
         "let successions : Sequence(Successions) =      ownedMember->selectByKind(Succession) in "
         "successions->notEmpty() and successions->at(1).targetFeature.featureTarget->     forAll("
         "oclIsKindOf(ActionUsage))"
        ),
        ("deriveTransitionUsageGuardExpression",
         "guardExpression = ownedFeatureMembership->     selectByKind(TransitionFeatureMembership)"
         "->     select(kind = TransitionFeatureKind::trigger).transitionFeature->     selectByKin"
         "d(Expression)"
        ),
        ("deriveTransitionUsageSource",
         "source =     let sourceFeature : Feature = sourceFeature() in     if sourceFeature = nul"
         "l then null     else sourceFeature.featureTarget.oclAsType(ActionUsage)"
        ),
        ("validateTransitionUsageTriggerActions",
         "source <> null and not source.oclIsKindOf(StateUsage) implies triggerAction->isEmpty()"
        ),
        ("deriveTransitionUsageEffectAction",
         "triggerAction = ownedFeatureMembership->     selectByKind(TransitionFeatureMembership)->"
         "     select(kind = TransitionFeatureKind::trigger).transitionFeatures->     selectByKind"
         "(AcceptActionUsage)"
        ),
        ("checkTransitionUsageSuccessionBindingConnector",
         "ownedMember->selectByKind(BindingConnector)->exists(b |     b.relatedFeatures->includes("
         "succession) and     b.relatedFeatures->includes(resolveGlobal(         'TransitionPerfor"
         "mances::TransitionPerformance::transitionLink')))"
        ),
        ("checkTransitionUsageSourceBindingConnector",
         "ownedMember->selectByKind(BindingConnector)->exists(b |     b.relatedFeatures->includes("
         "source) and     b.relatedFeatures->includes(inputParameter(1)))"
        ),
        ("checkTransitionUsagePayloadSpecialization",
         "triggerAction->notEmpty() implies     let payloadParameter : Feature = inputParameter(2)"
         " in     payloadParameter <> null and     payloadParameter.subsetsChain(triggerAction->at"
         "(1), triggerPayloadParameter())"
        ),
        ("checkTransitionUsageTransitionFeatureSpecialization",
         "triggerAction->forAll(specializesFromLibrary('Actions::TransitionAction::accepter') and "
         "guardExpression->forAll(specializesFromLibrary('Actions::TransitionAction::guard') and e"
         "ffectAction->forAll(specializesFromLibrary('Actions::TransitionAction::effect'))"
        ),
        ("checkTransitionUsageSuccessionSourceSpecialization",
         "succession.sourceFeature = source"
        ),
        ("checkTransitionUsageStateSpecialization",
         "isComposite and owningType <> null and (owningType.oclIsKindOf(StateDefinition) or  owni"
         "ngType.oclIsKindOf(StateUsage)) and source <> null and source.oclIsKindOf(StateUsage) im"
         "plies     specializesFromLibrary('States::StateAction::stateTransitions')"
        ),
        ("deriveTransitionUsageSuccession",
         "succession = ownedMember->selectByKind(Succession)->at(1)"
        ),
        ("validateTransitionUsageParameters",
         "if triggerAction->isEmpty() then inputParameters()->size() >= 1 else inputParameters()->"
         "size() >= 2 endif"
        ),
        ("deriveTransitionUsageTriggerAction",
         "triggerAction = ownedFeatureMembership->     selectByKind(TransitionFeatureMembership)->"
         "     select(kind = TransitionFeatureKind::trigger).transitionFeature->     selectByKind("
         "AcceptActionUsage)"
        ),
        ("checkTransitionUsageActionSpecialization",
         "isComposite and owningType <> null and (owningType.oclIsKindOf(ActionDefinition) or  own"
         "ingType.oclIsKindOf(ActionUsage)) and source <> null and not source.oclIsKindOf(StateUsa"
         "ge) implies     specializesFromLibrary('Actions::Action::decisionTransitions')"
        ),
    )
    def triggerPayloadParameter(self, arg: None = None) -> None:
        """
        <p>Return the <code>payloadParameter</code> of the <code>triggerAction</code> of this <code>Tr
        ansitionUsage</code>, if it has one.</p>
        [TransitionUsage operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def sourceFeature(self, arg: None = None) -> None:
        """
        <p>Return the <code>Feature</code> to be used as the <code>source</code> of the <code>successi
        on</code> of this <code>TransitionUsage</code>, which is the first <code>member</code> of the 
        <code>TransitionUsage</code> that is a <code>Feature</code>, that is owned by the <code>Transi
        tionUsage</code> via a <code>Membership</code> that is <em>not</em> a <code>FeatureMembership<
        /code>, and whose <code>featureTarget</code> is an <code>ActionUsage</code>.</p>
        [TransitionUsage operation; params: arg: ?; returns: nothing; stub - metamodel metadata only]
        """
        raise NotImplementedError

class TriggerInvocationExpression(InvocationExpression):
    """<p>A <code>TriggerInvocationExpression</code> is an <code>InvocationExpression</code> that invokes one of the trigger <code>Functions</code> from the Kernel Semantic Library <code><em>Triggers<em></code> package, as indicated by its <code>kind</code>.</p>"""
    _PKG = "Actions"
    _DECL = {
    # <p>Indicates which of the <code>Functions</code> from the <code><em>Triggers</em></code> model i
    # n the Kernel Semantic Library is to be invoked by this <code>TriggerInvocationExpression</code>.
    # </p>
    'kind': _Ref('kind', None),
    }
    CONSTRAINTS = (
        ("validateTriggerInvocationExpressionAfterArgument",
         "kind = TriggerKind::after implies     argument->notEmpty() and     argument->at(1).resul"
         "t.specializesFromLibrary('Quantities::ScalarQuantityValue') and     let mRef : Element ="
         "          resolveGlobal('Quantities::TensorQuantityValue::mRef').ownedMemberElement in  "
         "   argument->at(1).result.feature->         select(ownedRedefinition.redefinedFeature-> "
         "           closure(ownedRedefinition.redefinedFeature)->            includes(mRef))->   "
         "      exists(specializesFromLibrary('ISQBase::DurationUnit'))"
        ),
        ("validateTriggerInvocationExpressionAtArgument",
         "kind = TriggerKind::at implies     argument->notEmpty() and     argument->at(1).result.s"
         "pecializesFromLibrary('Time::TimeInstantValue')"
        ),
        ("validateTriggerInvocationExpressionWhenArgument",
         "kind = TriggerKind::when implies     argument->notEmpty() and     argument->at(1).oclIsK"
         "indOf(FeatureReferenceExpression) and     let referent : Feature =          argument->at"
         "(1).oclAsType(FeatureReferenceExpression).referent in     referent.oclIsKindOf(Expressio"
         "n) and     referent.oclAsType(Expression).result.specializesFromLibrary('ScalarValues::B"
         "oolean')"
        ),
    )
    def instantiatedType(self, arg: None = None) -> None:
        """
        <p>Return one of the <code>Functions</code> <em><code>TriggerWhen</code></em>, <em><code>Trigg
        erAt</code></em> or <em><code>TriggerAfter</code></em>, from the Kernel Semantic Library <em><
        code>Triggers</code></em> package, depending on whether the <code>kind</code> of this <code>Tr
        iggerInvocationExpression</code> is <code>when</code>, <code>at</code> or <code>after</code>, 
        respectively.</p>
        [TriggerInvocationExpression operation; params: arg: ?; returns: nothing; stub - metamodel met
        adata only]
        """
        raise NotImplementedError

class TypeFeaturing(Relationship):
    """<p>A <code>TypeFeaturing</code> is a <code>Featuring</code> <code>Relationship</code> in which the <code>featureOfType</code> is the <code>source</code> and the <code>featuringType</code> is the <code>target</code>.</p>"""
    _PKG = "Features"
    _DECL = {
    # <p>The <code>Feature</code> that is featured by the <code>featuringType</code>. It is the <code>
    # source</code> of the <code>TypeFeaturing</code>.</p>
    'featureOfType': _Ref('featureOfType', "Feature", redefines=("source",), assoc="Core-Features-A_featureOfType_typeFeaturing"),
    # <p>The <code>Type</code> that features the <code>featureOfType</code>. It is the <code>target</c
    # ode> of the <code>TypeFeaturing</code>.</p>
    'featuringType': _Ref('featuringType', "Type", redefines=("target",), assoc="Core-Features-A_featuringType_typeFeaturingOfType"),
    # <p>A <code>featureOfType</code> that is also the <code>owningRelatedElement</code> of this <code
    # >TypeFeaturing</code>.</p>
    'owningFeatureOfType': _Ref('owningFeatureOfType', "Feature", derived=True, subsets=("owningRelatedElement", "featureOfType",), assoc="Core-Features-A_ownedTypeFeaturing_owningFeatureOfType"),
    }

class Unioning(Relationship):
    """<p><code>Unioning</code> is a <code>Relationship</code> that makes its <code>unioningType</code> one of the <code>unioningTypes</code> of its <code>typeUnioned</code>.</p>"""
    _PKG = "Types"
    _DECL = {
    # <p><code>Type</code> with interpretations partly determined by <code>unioningType</code>, as des
    # cribed in <code>Type::unioningType</code>.</p>
    'typeUnioned': _Ref('typeUnioned', "Type", derived=True, subsets=("owningRelatedElement",), redefines=("source",), assoc="Core-Types-A_typeUnioned_ownedUnioning"),
    # <p><code>Type</code> that partly determines interpretations of <code>typeUnioned</code>, as desc
    # ribed in <code>Type::unioningType</code>.</p>
    'unioningType': _Ref('unioningType', "Type", redefines=("target",), assoc="Core-Types-A_unioningType_unionedUnioning"),
    }

class UseCaseDefinition(CaseDefinition):
    """<p>A <code>UseCaseDefinition</code> is a <code>CaseDefinition</code> that specifies a set of actions performed by its subject, in interaction with one or more actors external to the subject. The objective is to yield an observable result that is of value to one or more of the actors.</p>"""
    _PKG = "UseCases"
    _DECL = {
    # <p>The <code>UseCaseUsages</code> that are included by this <code>UseCaseDefinition</code>, whic
    # h are the <code>useCaseIncludeds</code> of the <code>IncludeUseCaseUsages</code> owned by this <
    # code>UseCaseDefinition<code>.</p>
    'includedUseCase': _Ref('includedUseCase', "UseCaseUsage", derived=True, multi=True, lo=0, hi='*', assoc="Systems-UseCases-A_includedUseCase_includingUseCaseDefinition"),
    }
    CONSTRAINTS = (
        ("deriveUseCaseDefinitionIncludedUseCase",
         "includedUseCase = ownedUseCase-> selectByKind(IncludeUseCaseUsage). useCaseIncluded"
        ),
        ("checkUseCaseDefinitionSpecialization",
         "specializesFromLibrary('UseCases::UseCase')"
        ),
    )

class VariantMembership(OwningMembership):
    """<p>A <code>VariantMembership</code> is a <code>Membership</code> between a variation point <code>Definition</code> or <code>Usage</code> and a <code>Usage</code> that represents a variant in the context of that variation. The <code>membershipOwningNamespace</code> for the <code>VariantMembership</code> must be either a Definition or a <code>Usage</code> with <code>isVariation = true</code>.</p>"""
    _PKG = "DefinitionAndUsage"
    _DECL = {
    # <p>The <code>Usage</code> that represents a variant in the context of the <code>owningVariationD
    # efinition</code> or <code>owningVariationUsage</code>.</p>
    'ownedVariantUsage': _Ref('ownedVariantUsage', "Usage", derived=True, composite=True, assoc="Systems-DefinitionAndUsage-A_ownedVariantUsage_owningVariantMembership"),
    }
    CONSTRAINTS = (
        ("validateVariantMembershipOwningNamespace",
         "membershipOwningNamespace.oclIsKindOf(Definition) and     membershipOwningNamespace.oclA"
         "sType(Definition).isVariation or membershipOwningNamespace.oclIsKindOf(Usage) and     me"
         "mbershipOwningNamespace.oclAsType(Usage).isVariation"
        ),
    )

class VerificationCaseDefinition(CaseDefinition):
    """<p>A <code>VerificationCaseDefinition</code> is a <code>CaseDefinition</code> for the purpose of verification of the subject of the case against its requirements.</p>"""
    _PKG = "VerificationCases"
    _DECL = {
    # <p>The <code>RequirementUsages</code> verified by this <code>VerificationCaseDefinition</code>, 
    # which are the <code>verifiedRequirements</code> of all <code>RequirementVerificationMemberships<
    # /code> of the <code>objectiveRequirement</code>.</p>
    'verifiedRequirement': _Ref('verifiedRequirement', "RequirementUsage", derived=True, multi=True, lo=0, hi='*', assoc="Systems-VerificationCases-A_verifiedRequirement_verifyingCaseDefinition"),
    }
    CONSTRAINTS = (
        ("deriveVerificationCaseDefinitionVerifiedRequirement",
         "verifiedRequirement =     if objectiveRequirement = null then OrderedSet{}     else     "
         "     objectiveRequirement.featureMembership->             selectByKind(RequirementVerifi"
         "cationMembership).             verifiedRequirement->asOrderedSet()     endif"
        ),
        ("checkVerificationCaseSpecialization",
         "specializesFromLibrary('VerificationCases::VerificationCase')"
        ),
    )

class VerificationCaseUsage(CaseUsage):
    """<p>A <code>VerificationCaseUsage</code> is a </code>Usage</code> of a <code>VerificationCaseDefinition</code>.</p>"""
    _PKG = "VerificationCases"
    _DECL = {
    # <p>The <code>VerificationCase</code> that is the <code>definition</code> of this <code>Verificat
    # ionCaseUsage</code>.</p>
    'verificationCaseDefinition': _Ref('verificationCaseDefinition', "VerificationCaseDefinition", derived=True, subsets=("caseDefinition",), assoc="Systems-VerificationCases-A_verificationCaseDefinition_definedVerificationCase"),
    # <p>The <code>RequirementUsages</code> verified by this <code>VerificationCaseUsage</code>, which
    #  are the <code>verifiedRequirements</code> of all <code>RequirementVerificationMemberships</code
    # > of the <code>objectiveRequirement</code>.</p>
    'verifiedRequirement': _Ref('verifiedRequirement', "RequirementUsage", derived=True, multi=True, lo=0, hi='*', assoc="Systems-VerificationCases-A_verifiedRequirement_verifyingCase"),
    }
    CONSTRAINTS = (
        ("deriveVerificationCaseUsageVerifiedRequirement",
         "verifiedRequirement =     if objectiveRequirement = null then OrderedSet{}     else     "
         "     objectiveRequirement.featureMembership->             selectByKind(RequirementVerifi"
         "cationMembership).             verifiedRequirement->asOrderedSet()     endif"
        ),
        ("checkVerificationCaseUsageSpecialization",
         "specializesFromLibrary('VerificationCases::verificationCases')"
        ),
        ("checkVerificationCaseUsageSubVerificationCaseSpecialization",
         "isComposite and owningType <> null and     (owningType.oclIsKindOf(VerificationCaseDefin"
         "ition) or      owningType.oclIsKindOf(VerificationCaseUsage)) implies      specializesFr"
         "omLibrary('VerificationCases::VerificationCase::subVerificationCases')"
        ),
    )

class ViewDefinition(PartDefinition):
    """<p>A <code>ViewDefinition</code> is a <code>PartDefinition</code> that specifies how a view artifact is constructed to satisfy a <code>viewpoint</code>. It specifies a <code>viewConditions</code> to define the model content to be presented and a <code>viewRendering</code> to define how the model content is presented.</p>"""
    _PKG = "Views"
    _DECL = {
    # <p>The composite <code>ownedRequirements</code> of this <code>ViewDefinition</code> that are <co
    # de>ViewpointUsages</code> for viewpoints satisfied by the <code>ViewDefinition</code>.</p>
    'satisfiedViewpoint': _Ref('satisfiedViewpoint', "ViewpointUsage", derived=True, multi=True, lo=0, hi='*', subsets=("ownedRequirement",), assoc="Systems-Views-A_satisfiedViewpoint_viewpointSatisfyingViewDefinition"),
    # <p>The <code>usages</code> of this <code>ViewDefinition</code> that are <code>ViewUsages</code>.
    # </p>
    'view': _Ref('view', "ViewUsage", derived=True, multi=True, lo=0, hi='*', subsets=("usage",), assoc="Systems-Views-A_view_featuringView"),
    # <p>The <code>Expressions</code> related to this <code>ViewDefinition</code> by <code>ElementFilt
    # erMemberships</code>, which specify conditions on <code>Elements</code> to be rendered in a view
    # .</p>
    'viewCondition': _Ref('viewCondition', "Expression", derived=True, multi=True, lo=0, hi='*', assoc="Systems-Views-A_viewCondition_owningViewDefinition"),
    # <p>The <code>RenderingUsage</code> to be used to render views defined by this <code>ViewDefiniti
    # on</code>, which is the <code>referencedRendering</code> of the <code>ViewRenderingMembership</c
    # ode> of the <code>ViewDefinition</code>.<p>
    'viewRendering': _Ref('viewRendering', "RenderingUsage", derived=True, assoc="Systems-Views-A_viewRendering_renderingOwningViewDefinition"),
    }
    CONSTRAINTS = (
        ("deriveViewDefinitionViewCondition",
         "viewCondition = ownedMembership-> selectByKind(ElementFilterMembership). condition"
        ),
        ("deriveViewDefinitionSatisfiedViewpoint",
         "satisfiedViewpoint = ownedRequirement-> selectByKind(ViewpointUsage)-> select(isComposit"
         "e)"
        ),
        ("deriveViewDefinitionViewRendering",
         "viewRendering =     let renderings: OrderedSet(ViewRenderingMembership) =         featur"
         "eMembership->selectByKind(ViewRenderingMembership) in     if renderings->isEmpty() then "
         "null     else renderings->first().referencedRendering     endif"
        ),
        ("checkViewDefinitionSpecialization",
         "specializesFromLibrary('Views::View')"
        ),
        ("deriveViewDefinitionView",
         "view = usage->selectByKind(ViewUsage)"
        ),
        ("validateViewDefinitionOnlyOneViewRendering",
         "featureMembership-> selectByKind(ViewRenderingMembership)-> size() <= 1"
        ),
    )

class ViewRenderingMembership(FeatureMembership):
    """<p>A <code>ViewRenderingMembership</code> is a <coed>FeatureMembership</code> that identifies the <code>viewRendering</code> of a <code>ViewDefinition</code> or <code>ViewUsage</code>.</p>"""
    _PKG = "Views"
    _DECL = {
    # <p>The owned <code>RenderingUsage</code> that is either itself the <code>referencedRendering</co
    # de> or subsets the <code>referencedRendering</code>.
    'ownedRendering': _Ref('ownedRendering', "RenderingUsage", derived=True, composite=True, assoc="Systems-Views-A_ownedRendering_viewRenderingMembership"),
    # <p> The <code>RenderingUsage</code> that is referenced through this <code>ViewRenderingMembershi
    # p</code>. It is the <code>referencedFeature</code> of the <code>ownedReferenceSubsetting</code> 
    # for the <code>ownedRendering</code>, if there is one, and, otherwise, the <code>ownedRendering</
    # code> itself.</p>
    'referencedRendering': _Ref('referencedRendering', "RenderingUsage", derived=True, assoc="Systems-Views-A_referencedRendering_referencingRenderingMembership"),
    }
    CONSTRAINTS = (
        ("deriveVewRenderingMembershipReferencedRendering",
         "referencedRendering =     let referencedFeature : Feature =          ownedRendering.refe"
         "rencedFeatureTarget() in     if referencedFeature = null then ownedRendering     else if"
         " referencedFeature.oclIsKindOf(RenderingUsage) then         refrencedFeature.oclAsType(R"
         "enderingUsage)     else null     endif endif"
        ),
        ("validateViewRenderingMembershipOwningType",
         "owningType.oclIsKindOf(ViewDefinition) or owningType.oclIsKindOf(ViewUsage)"
        ),
    )

class ViewUsage(PartUsage):
    """<p>A <code>ViewUsage</code> is a usage of a <code>ViewDefinition</code> to specify the generation of a view of the <code>members</code> of a collection of <code>exposedNamespaces</code>. The <code>ViewUsage</code> can satisfy more <code>viewpoints</code> than its definition, and it can specialize the <code>viewRendering</code> specified by its definition.<p>"""
    _PKG = "Views"
    _DECL = {
    # <p>The <code>Elements</code> that are exposed by this <code>ViewUsage</code>, which are those <c
    # ode>memberElements</code> of the imported <code>Memberships</code> from all the <code>Expose</co
    # de> <code>Relationships</code> that meet all the owned and inherited <code>viewConditions</code>
    # .</p>
    'exposedElement': _Ref('exposedElement', "Element", derived=True, multi=True, lo=0, hi='*', assoc="Systems-Views-A_exposedElement_exposingView"),
    # <p>The <code>nestedRequirements</code> of this <code>ViewUsage</code> that are <code>ViewpointUs
    # ages</code> for (additional) viewpoints satisfied by the <code>ViewUsage</code>.</p>
    'satisfiedViewpoint': _Ref('satisfiedViewpoint', "ViewpointUsage", derived=True, multi=True, lo=0, hi='*', subsets=("nestedRequirement",), assoc="Systems-Views-A_satisfiedViewpoint_viewpointSatisfyingView"),
    # <p>The <code>Expressions</code> related to this <code>ViewUsage</code> by <code>ElementFilterMem
    # berships</code>, which specify conditions on <code>Elements</code> to be rendered in a view.</p>
    'viewCondition': _Ref('viewCondition', "Expression", derived=True, multi=True, lo=0, hi='*', assoc="Systems-Views-A_viewCondition_owningView"),
    # <p>The <code>ViewDefinition</code> that is the <code>definition</code> of this <code>ViewUsage</
    # code>.</p>
    'viewDefinition': _Ref('viewDefinition', "ViewDefinition", derived=True, redefines=("partDefinition",), assoc="Systems-Views-A_viewDefinition_definedView"),
    # <p>The <code>RenderingUsage</code> to be used to render views defined by this <code>ViewUsage</c
    # ode>, which is the <code>referencedRendering</code> of the <code>ViewRenderingMembership</code> 
    # of the <code>ViewUsage</code>.<p>
    'viewRendering': _Ref('viewRendering', "RenderingUsage", derived=True, assoc="Systems-Views-A_viewRendering_renderingOwningView"),
    }
    CONSTRAINTS = (
        ("checkViewUsageSubviewSpecialization",
         "owningType <> null and (owningType.oclIsKindOf(ViewDefinition) or  owningType.oclIsKindO"
         "f(ViewUsage)) implies     specializesFromLibrary('Views::View::subviews')"
        ),
        ("deriveViewUsageSatisfiedViewpoint",
         "satisfiedViewpoint = ownedRequirement-> selectByKind(ViewpointUsage)-> select(isComposit"
         "e)"
        ),
        ("checkViewUsageSpecialization",
         "specializesFromLibrary('Views::views')"
        ),
        ("deriveViewUsageExposedElement",
         "exposedElement = ownedImport->selectByKind(Expose).     importedMemberships(Set{}).membe"
         "rElement->     select(elm | includeAsExposed(elm))->     asOrderedSet()"
        ),
        ("validateViewUsageOnlyOneViewRendering",
         "featureMembership-> selectByKind(ViewRenderingMembership)-> size() <= 1"
        ),
        ("deriveViewUsageViewCondition",
         "viewCondition = ownedMembership-> selectByKind(ElementFilterMembership). condition"
        ),
        ("deriveViewUsageViewRendering",
         "viewRendering =     let renderings: OrderedSet(ViewRenderingMembership) =         featur"
         "eMembership->selectByKind(ViewRenderingMembership) in     if renderings->isEmpty() then "
         "null     else renderings->first().referencedRendering     endif"
        ),
    )
    def includeAsExposed(self, element: None = None, arg: None = None) -> None:
        """
        <p>Determine whether the given <code>element</code> meets all the owned and inherited <code>vi
        ewConditions</code>.</p>
        [ViewUsage operation; params: element: ?, arg: ?; returns: nothing; stub - metamodel metadata 
        only]
        """
        raise NotImplementedError

class ViewpointDefinition(RequirementDefinition):
    """<p>A <code>ViewpointDefinition</code> is a <code>RequirementDefinition</code> that specifies one or more stakeholder concerns that are to be satisfied by creating a view of a model.</p>"""
    _PKG = "Views"
    _DECL = {
    # <p>The <code>PartUsages</code> that identify the stakeholders with concerns framed by this <code
    # >ViewpointDefinition</code>, which are the owned and inherited <code>stakeholderParameters</code
    # > of the <code>framedConcerns</code> of this <code>ViewpointDefinition</code>.</p>
    'viewpointStakeholder': _Ref('viewpointStakeholder', "PartUsage", derived=True, multi=True, lo=0, hi='*', assoc="Systems-Views-A_viewpointStakeholder_viewpointDefinitionForStakeholder"),
    }
    CONSTRAINTS = (
        ("deriveViewpointDefinitionViewpointStakeholder",
         "viewpointStakeholder = framedConcern.featureMemberhsip->     selectByKind(StakeholderMem"
         "bership).     ownedStakeholderParameter"
        ),
        ("checkViewpointDefinitionSpecialization",
         "specializesFromLibrary('Views::Viewpoint')"
        ),
    )

class ViewpointUsage(RequirementUsage):
    """<p>A <code>ViewpointUsage</code> is a <code>Usage</code> of a <code>ViewpointDefinition</code>.</p>"""
    _PKG = "Views"
    _DECL = {
    # <p>The <code>ViewpointDefinition</code> that is the <code>definition</code> of this <code>Viewpo
    # intUsage<code>.</p>
    'viewpointDefinition': _Ref('viewpointDefinition', "ViewpointDefinition", derived=True, redefines=("requirementDefinition",), assoc="Systems-Views-A_viewpointDefinition_definedViewpoint"),
    # <p>The <code>PartUsages</code> that identify the stakeholders with concerns framed by this <code
    # >ViewpointUsage</code>, which are the owned and inherited <code>stakeholderParameters</code> of 
    # the <code>framedConcerns</code> of this <code>ViewpointUsage</code>.</p>
    'viewpointStakeholder': _Ref('viewpointStakeholder', "PartUsage", derived=True, multi=True, lo=0, hi='*', assoc="Systems-Views-A_viewpointStakeholder_viewpointForStakeholder"),
    }
    CONSTRAINTS = (
        ("checkViewpointUsageViewpointSatisfactionSpecialization",
         "isComposite and owningType <> null and (owningType.oclIsKindOf(ViewDefinition) or  ownin"
         "gType.oclIsKindOf(ViewUsage)) implies     specializesFromLibrary('Views::View::viewpoint"
         "Satisfactions')"
        ),
        ("checkViewpointUsageSpecialization",
         "specializesFromLibrary('Views::viewpoints')"
        ),
        ("deriveViewpointUsageViewpointStakeholder",
         "viewpointStakeholder = framedConcern.featureMemberhsip-> selectByKind(StakeholderMembers"
         "hip). ownedStakeholderParameter"
        ),
    )

class WhileLoopActionUsage(LoopActionUsage):
    """<p>A <code>WhileLoopActionUsage</code> is a <code>LoopActionUsage</code> that specifies that the <code>bodyAction</code> <code>ActionUsage</code> should be performed repeatedly while the result of the <code>whileArgument</code> <code>Expression</code> is true or until the result of the <code>untilArgument</code> <code>Expression</code> (if provided) is true. The <code>whileArgument</code> <code>Expression</code> is evaluated before each (possible) performance of the <code>bodyAction</code>, and the <code>untilArgument</code> <code>Expression</code> is evaluated after each performance of the <code>bodyAction</code>.</p>"""
    _PKG = "Actions"
    _DECL = {
    # <p>The <code>Expression</code> whose result, if false, determines that the <code>bodyAction</cod
    # e> should continue to be performed. It is the (optional) third owned <code>parameter</code> of t
    # he <code>WhileLoopActionUsage</code>.</p>
    'untilArgument': _Ref('untilArgument', "Expression", derived=True, assoc="Systems-Actions-A_untilArgument_untilLoopAction"),
    # <p>The <code>Expression</code> whose result, if true, determines that the <code>bodyAction</code
    # > should continue to be performed. It is the first owned <code>parameter</code> of the <code>Whi
    # leLoopActionUsage</code>.</p>
    'whileArgument': _Ref('whileArgument', "Expression", derived=True, assoc="Systems-Actions-A_whileArgument_whileLoopAction"),
    }
    CONSTRAINTS = (
        ("checkWhileLoopActionUsageSpecialization",
         "specializesFromLibrary('Actions::whileLoopActions')"
        ),
        ("deriveWhileLoopActionUsageWhileArgument",
         "whileArgument =     let parameter : Feature = inputParameter(1) in     if parameter <> n"
         "ull and parameter.oclIsKindOf(Expression) then         parameter.oclAsType(Expression)  "
         "   else         null     endif"
        ),
        ("validateWhileLoopActionUsage",
         "inputParameters()->size() >= 2"
        ),
        ("deriveWhileLoopActionUsageUntilArgument",
         "untilArgument =     let parameter : Feature = inputParameter(3) in     if parameter <> n"
         "ull and parameter.oclIsKindOf(Expression) then         parameter.oclAsType(Expression)  "
         "   else         null     endif"
        ),
        ("checkWhileLoopActionUsageSubactionSpecialization",
         "isSubactionUsage() implies specializesFromLibrary('Actions::Action::whileLoops')"
        ),
    )

_CLASSES = [Element, Namespace, Type, Feature, Step, Usage, OccurrenceUsage, ActionUsage, AcceptActionUsage, Classifier, Definition, Class, OccurrenceDefinition, Behavior, ActionDefinition, Relationship, Membership, OwningMembership, FeatureMembership, ParameterMembership, ActorMembership, Structure, Association, AssociationStructure, ItemDefinition, PartDefinition, ConnectionDefinition, AllocationDefinition, ItemUsage, PartUsage, Connector, ConnectorAsUsage, ConnectionUsage, AllocationUsage, Function, CalculationDefinition, CaseDefinition, AnalysisCaseDefinition, Expression, CalculationUsage, CaseUsage, AnalysisCaseUsage, AnnotatingElement, Annotation, BooleanExpression, Invariant, ConstraintUsage, AssertConstraintUsage, AssignmentActionUsage, DataType, AttributeDefinition, AttributeUsage, BindingConnector, BindingConnectorAsUsage, InstantiationExpression, InvocationExpression, OperatorExpression, CollectExpression, Comment, Predicate, ConstraintDefinition, RequirementDefinition, ConcernDefinition, RequirementUsage, ConcernUsage, PortDefinition, ConjugatedPortDefinition, Specialization, FeatureTyping, ConjugatedPortTyping, Conjugation, ConstructorExpression, ControlNode, Subsetting, CrossSubsetting, DecisionNode, Dependency, Differencing, Disjoining, Documentation, ElementFilterMembership, EndFeatureMembership, EnumerationDefinition, EnumerationUsage, EventOccurrenceUsage, PerformActionUsage, StateUsage, ExhibitStateUsage, Import, Expose, FeatureChainExpression, FeatureChaining, FeatureInverting, FeatureReferenceExpression, FeatureValue, Flow, Interaction, FlowDefinition, FlowEnd, FlowUsage, LoopActionUsage, ForLoopActionUsage, ForkNode, RequirementConstraintMembership, FramedConcernMembership, IfActionUsage, UseCaseUsage, IncludeUseCaseUsage, IndexExpression, InterfaceDefinition, InterfaceUsage, Intersecting, JoinNode, Package, LibraryPackage, LiteralExpression, LiteralBoolean, LiteralInfinity, LiteralInteger, LiteralRational, LiteralString, MembershipImport, MembershipExpose, MergeNode, Metaclass, MetadataAccessExpression, MetadataDefinition, MetadataFeature, MetadataUsage, Multiplicity, MultiplicityRange, NamespaceImport, NamespaceExpose, NullExpression, ObjectiveMembership, PayloadFeature, PortConjugation, PortUsage, Redefinition, ReferenceSubsetting, ReferenceUsage, RenderingDefinition, RenderingUsage, RequirementVerificationMembership, ResultExpressionMembership, ReturnParameterMembership, SatisfyRequirementUsage, SelectExpression, SendActionUsage, StakeholderMembership, StateDefinition, StateSubactionMembership, Subclassification, SubjectMembership, Succession, SuccessionAsUsage, SuccessionFlow, SuccessionFlowUsage, TerminateActionUsage, TextualRepresentation, TransitionFeatureMembership, TransitionUsage, TriggerInvocationExpression, TypeFeaturing, Unioning, UseCaseDefinition, VariantMembership, VerificationCaseDefinition, VerificationCaseUsage, ViewDefinition, ViewRenderingMembership, ViewUsage, ViewpointDefinition, ViewpointUsage, WhileLoopActionUsage]
_OPPOSITES = {
    ("AnnotatingElement", "annotation"): ("Annotation", "annotatingElement"),
    ("AnnotatingElement", "ownedAnnotatingRelationship"): ("Annotation", "owningAnnotatingElement"),
    ("AnnotatingElement", "owningAnnotatingRelationship"): ("Annotation", "ownedAnnotatingElement"),
    ("Annotation", "annotatingElement"): ("AnnotatingElement", "annotation"),
    ("Annotation", "ownedAnnotatingElement"): ("AnnotatingElement", "owningAnnotatingRelationship"),
    ("Annotation", "owningAnnotatedElement"): ("Element", "ownedAnnotation"),
    ("Annotation", "owningAnnotatingElement"): ("AnnotatingElement", "ownedAnnotatingRelationship"),
    ("Classifier", "ownedSubclassification"): ("Subclassification", "owningClassifier"),
    ("ConjugatedPortDefinition", "originalPortDefinition"): ("PortDefinition", "conjugatedPortDefinition"),
    ("ConjugatedPortDefinition", "ownedPortConjugator"): ("PortConjugation", "conjugatedPortDefinition"),
    ("Conjugation", "owningType"): ("Type", "ownedConjugator"),
    ("CrossSubsetting", "crossingFeature"): ("Feature", "ownedCrossSubsetting"),
    ("Definition", "ownedUsage"): ("Usage", "owningDefinition"),
    ("Differencing", "typeDifferenced"): ("Type", "ownedDifferencing"),
    ("Disjoining", "owningType"): ("Type", "ownedDisjoining"),
    ("Documentation", "documentedElement"): ("Element", "documentation"),
    ("Element", "documentation"): ("Documentation", "documentedElement"),
    ("Element", "ownedAnnotation"): ("Annotation", "owningAnnotatedElement"),
    ("Element", "ownedElement"): ("Element", "owner"),
    ("Element", "ownedRelationship"): ("Relationship", "owningRelatedElement"),
    ("Element", "owner"): ("Element", "ownedElement"),
    ("Element", "owningMembership"): ("OwningMembership", "ownedMemberElement"),
    ("Element", "owningNamespace"): ("Namespace", "ownedMember"),
    ("Element", "owningRelationship"): ("Relationship", "ownedRelatedElement"),
    ("Element", "textualRepresentation"): ("TextualRepresentation", "representedElement"),
    ("Feature", "endOwningType"): ("Type", "ownedEndFeature"),
    ("Feature", "ownedCrossSubsetting"): ("CrossSubsetting", "crossingFeature"),
    ("Feature", "ownedFeatureChaining"): ("FeatureChaining", "featureChained"),
    ("Feature", "ownedFeatureInverting"): ("FeatureInverting", "owningFeature"),
    ("Feature", "ownedReferenceSubsetting"): ("ReferenceSubsetting", "referencingFeature"),
    ("Feature", "ownedSubsetting"): ("Subsetting", "owningFeature"),
    ("Feature", "ownedTypeFeaturing"): ("TypeFeaturing", "owningFeatureOfType"),
    ("Feature", "ownedTyping"): ("FeatureTyping", "owningFeature"),
    ("Feature", "owningFeatureMembership"): ("FeatureMembership", "ownedMemberFeature"),
    ("Feature", "owningType"): ("Type", "ownedFeature"),
    ("FeatureChaining", "featureChained"): ("Feature", "ownedFeatureChaining"),
    ("FeatureInverting", "owningFeature"): ("Feature", "ownedFeatureInverting"),
    ("FeatureMembership", "ownedMemberFeature"): ("Feature", "owningFeatureMembership"),
    ("FeatureMembership", "owningType"): ("Type", "ownedFeatureMembership"),
    ("FeatureTyping", "owningFeature"): ("Feature", "ownedTyping"),
    ("Import", "importOwningNamespace"): ("Namespace", "ownedImport"),
    ("Intersecting", "typeIntersected"): ("Type", "ownedIntersecting"),
    ("Membership", "membershipOwningNamespace"): ("Namespace", "ownedMembership"),
    ("Namespace", "ownedImport"): ("Import", "importOwningNamespace"),
    ("Namespace", "ownedMember"): ("Element", "owningNamespace"),
    ("Namespace", "ownedMembership"): ("Membership", "membershipOwningNamespace"),
    ("OwningMembership", "ownedMemberElement"): ("Element", "owningMembership"),
    ("PortConjugation", "conjugatedPortDefinition"): ("ConjugatedPortDefinition", "ownedPortConjugator"),
    ("PortDefinition", "conjugatedPortDefinition"): ("ConjugatedPortDefinition", "originalPortDefinition"),
    ("ReferenceSubsetting", "referencingFeature"): ("Feature", "ownedReferenceSubsetting"),
    ("Relationship", "ownedRelatedElement"): ("Element", "owningRelationship"),
    ("Relationship", "owningRelatedElement"): ("Element", "ownedRelationship"),
    ("Specialization", "owningType"): ("Type", "ownedSpecialization"),
    ("Subclassification", "owningClassifier"): ("Classifier", "ownedSubclassification"),
    ("Subsetting", "owningFeature"): ("Feature", "ownedSubsetting"),
    ("TextualRepresentation", "representedElement"): ("Element", "textualRepresentation"),
    ("Type", "ownedConjugator"): ("Conjugation", "owningType"),
    ("Type", "ownedDifferencing"): ("Differencing", "typeDifferenced"),
    ("Type", "ownedDisjoining"): ("Disjoining", "owningType"),
    ("Type", "ownedEndFeature"): ("Feature", "endOwningType"),
    ("Type", "ownedFeature"): ("Feature", "owningType"),
    ("Type", "ownedFeatureMembership"): ("FeatureMembership", "owningType"),
    ("Type", "ownedIntersecting"): ("Intersecting", "typeIntersected"),
    ("Type", "ownedSpecialization"): ("Specialization", "owningType"),
    ("Type", "ownedUnioning"): ("Unioning", "typeUnioned"),
    ("TypeFeaturing", "owningFeatureOfType"): ("Feature", "ownedTypeFeaturing"),
    ("Unioning", "typeUnioned"): ("Type", "ownedUnioning"),
    ("Usage", "nestedUsage"): ("Usage", "owningUsage"),
    ("Usage", "owningDefinition"): ("Definition", "ownedUsage"),
    ("Usage", "owningUsage"): ("Usage", "nestedUsage"),
}
_ABSTRACT_NAMES = {"Element", "Relationship", "ConnectorAsUsage", "InstantiationExpression", "ControlNode", "Import", "Expose", "LoopActionUsage"}

def _finish():
    for c in _CLASSES:
        props = {}
        for k in reversed(c.__mro__):
            for n, d in getattr(k, '_DECL', {}).items():
                    props[n] = d
        c._props = props
        c._ABSTRACT = c.__name__ in _ABSTRACT_NAMES
    for c in _CLASSES:
        decl = c.__dict__.get('_DECL')
        if not decl:
            continue
        for d in decl.values():
            d.owner_cls = c.__name__
            opp = _OPPOSITES.get((c.__name__, d.name))
            d.opp = opp[1] if opp else None
        for n, d in decl.items():
            setattr(c, n, d)
_finish()

def metaclass(name):
    """Look up a generated metaclass by metamodel name."""
    for c in _CLASSES:
        if c.__name__ == name: return c
    raise KeyError(name)

_ENUMS = {"FeatureDirectionKind": FeatureDirectionKind, "PortionKind": PortionKind, "RequirementConstraintKind": RequirementConstraintKind, "StateSubactionKind": StateSubactionKind, "TransitionFeatureKind": TransitionFeatureKind, "TriggerKind": TriggerKind, "VisibilityKind": VisibilityKind}

