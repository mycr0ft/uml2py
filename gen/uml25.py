"""UML 2.5.1 metaclass hierarchy generated from the OMG-published XMI.

Source: UML.xmi (metamodel URI http://www.omg.org/spec/UML/20161101).
Pure-stdlib Python, no dependencies. Do not edit by hand; regenerate.

Contents: 242 metaclasses, 622 properties, 205 operations,
13 enumerations, 449 normative OCL constraints (metadata).
Derived unions / subsets / composite ownership / association opposites wired.
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

class AggregationKind(_enum.Enum):
    """AggregationKind is an Enumeration for specifying the kind of aggregation of a Property."""
    none = "none"
    shared = "shared"
    composite = "composite"

class CallConcurrencyKind(_enum.Enum):
    """CallConcurrencyKind is an Enumeration used to specify the semantics of concurrent calls to a BehavioralFeature."""
    sequential = "sequential"
    guarded = "guarded"
    concurrent = "concurrent"

class ConnectorKind(_enum.Enum):
    """ConnectorKind is an enumeration that defines whether a Connector is an assembly or a delegation."""
    assembly = "assembly"
    delegation = "delegation"

class ExpansionKind(_enum.Enum):
    """ExpansionKind is an enumeration type used to specify how an ExpansionRegion executes its contents."""
    parallel = "parallel"
    iterative = "iterative"
    stream = "stream"

class InteractionOperatorKind(_enum.Enum):
    """InteractionOperatorKind is an enumeration designating the different kinds of operators of CombinedFragments. The InteractionOperand defines the type of operator of a CombinedFragment."""
    seq = "seq"
    alt = "alt"
    opt = "opt"
    break_ = "break"
    par = "par"
    strict = "strict"
    loop = "loop"
    critical = "critical"
    neg = "neg"
    assert_ = "assert"
    ignore = "ignore"
    consider = "consider"

class MessageKind(_enum.Enum):
    """This is an enumerated type that identifies the type of Message."""
    complete = "complete"
    lost = "lost"
    found = "found"
    unknown = "unknown"

class MessageSort(_enum.Enum):
    """This is an enumerated type that identifies the type of communication action that was used to generate the Message."""
    synchCall = "synchCall"
    asynchCall = "asynchCall"
    asynchSignal = "asynchSignal"
    createMessage = "createMessage"
    deleteMessage = "deleteMessage"
    reply = "reply"

class ObjectNodeOrderingKind(_enum.Enum):
    """ObjectNodeOrderingKind is an enumeration indicating queuing order for offering the tokens held by an ObjectNode."""
    unordered = "unordered"
    ordered = "ordered"
    LIFO = "LIFO"
    FIFO = "FIFO"

class ParameterDirectionKind(_enum.Enum):
    """ParameterDirectionKind is an Enumeration that defines literals used to specify direction of parameters."""
    in_ = "in"
    inout = "inout"
    out = "out"
    return_ = "return"

class ParameterEffectKind(_enum.Enum):
    """ParameterEffectKind is an Enumeration that indicates the effect of a Behavior on values passed in or out of its parameters."""
    create = "create"
    read = "read"
    update = "update"
    delete = "delete"

class PseudostateKind(_enum.Enum):
    """PseudostateKind is an Enumeration type that is used to differentiate various kinds of Pseudostates."""
    initial = "initial"
    deepHistory = "deepHistory"
    shallowHistory = "shallowHistory"
    join = "join"
    fork = "fork"
    junction = "junction"
    choice = "choice"
    entryPoint = "entryPoint"
    exitPoint = "exitPoint"
    terminate = "terminate"

class TransitionKind(_enum.Enum):
    """TransitionKind is an Enumeration type used to differentiate the various kinds of Transitions."""
    internal = "internal"
    local = "local"
    external = "external"

class VisibilityKind(_enum.Enum):
    """VisibilityKind is an enumeration type that defines literals to determine the visibility of Elements in a model."""
    public = "public"
    private = "private"
    protected = "protected"
    package = "package"

class _Ref:
    """Descriptor carrying one UML property and its metamodel semantics."""
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
                f'{type(inst).__name__}.{self.name} is derived/read-only in'
                f' the UML 2.5.1 metamodel; it is computed, not assigned.')
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
    """List-valued UML property; every mutation fires the wiring hooks."""
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
    """Common base of all UML metaclasses (UML 2.5.1 Element)."""
    _DECL: dict = {}
    _UNIONS: dict = {}
    _ABSTRACT = False
    def __init__(self, **kw):
        if type(self)._ABSTRACT:
            raise TypeError(
                f'{type(self).__name__} is abstract in the UML 2.5.1'
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
        """Derived-union read: collect all values of properties that subset."""
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
        """NamedElement.namespace: derived from composite ownership."""
        return self._namespace
    def __repr__(self):
        n = self._vals.get('name')
        if isinstance(n, str) and n:
            return f'<{type(self).__name__} {n!r}>'
        return f'<{type(self).__name__} #{id(self):x}>'

class Element(_Element):
    """An Element is a constituent of a model. As such, it has the capability of owning other Elements."""
    _PKG = "CommonStructure"
    # (owner / namespace properties are hardcoded on _Element)
    _DECL = {
    # The Comments owned by this Element.
    'ownedComment': _Ref('ownedComment', "Comment", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_ownedComment_owningElement"),
    # The Elements owned by this Element.
    'ownedElement': _Ref('ownedElement', "Element", derived=True, union=True, composite=True, readonly=True, multi=True, lo=0, hi='*', assoc="A_ownedElement_owner"),
    }
    _UNIONS = {
        "ownedElement": ("ownedComment",),
    }
    CONSTRAINTS = (
        ("has_owner",
         "mustBeOwned() implies owner->notEmpty()"
        ),
        ("not_own_self",
         "not allOwnedElements()->includes(self)"
        ),
    )
    def allOwnedElements(self) -> "Element":
        """
        The query allOwnedElements() gives all of the direct and indirect ownedElements of an Element.
        [Element operation (query); params: none; returns: "Element"; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def mustBeOwned(self) -> bool:
        """
        The query mustBeOwned() indicates whether Elements of this type must have an owner. Subclasses
         of Element that do not require an owner must override this operation.
        [Element operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError

class Relationship(Element):
    """Relationship is an abstract concept that specifies some kind of relationship between Elements."""
    _PKG = "CommonStructure"
    _DECL = {
    # Specifies the elements related by the Relationship.
    'relatedElement': _Ref('relatedElement', "Element", derived=True, union=True, readonly=True, multi=True, lo=0, hi='*', assoc="A_relatedElement_relationship"),
    }

class DirectedRelationship(Relationship):
    """A DirectedRelationship represents a relationship between a collection of source model Elements and a collection of target model Elements."""
    _PKG = "CommonStructure"
    _DECL = {
    # Specifies the source Element(s) of the DirectedRelationship.
    'source': _Ref('source', "Element", derived=True, union=True, readonly=True, multi=True, lo=0, hi='*', subsets=("relatedElement",), assoc="A_source_directedRelationship"),
    # Specifies the target Element(s) of the DirectedRelationship.
    'target': _Ref('target', "Element", derived=True, union=True, readonly=True, multi=True, lo=0, hi='*', subsets=("relatedElement",), assoc="A_target_directedRelationship"),
    }

class ParameterableElement(Element):
    """A ParameterableElement is an Element that can be exposed as a formal TemplateParameter for a template, or specified as an actual parameter in a binding of a template."""
    _PKG = "CommonStructure"
    _DECL = {
    # The formal TemplateParameter that owns this ParameterableElement.
    'owningTemplateParameter': _Ref('owningTemplateParameter', "TemplateParameter", subsets=("owner", "templateParameter",), assoc="A_ownedParameteredElement_owningTemplateParameter"),
    # The TemplateParameter that exposes this ParameterableElement as a formal parameter.
    'templateParameter': _Ref('templateParameter', "TemplateParameter", assoc="A_parameteredElement_templateParameter"),
    }
    _UNIONS = {
        "owner": ("owningTemplateParameter",),
    }
    def isCompatibleWith(self, p: "ParameterableElement" = None) -> bool:
        """
        The query isCompatibleWith() determines if this ParameterableElement is compatible with the sp
        ecified ParameterableElement. By default, this ParameterableElement is compatible with another
         ParameterableElement p if the kind of this ParameterableElement is the same as or a subtype o
        f the kind of p. Subclasses of ParameterableElement should override this operation to specify 
        different compatibility constraints.
        [ParameterableElement operation (query); params: p: "ParameterableElement"; returns: bool; stu
        b - metamodel metadata only]
        """
        raise NotImplementedError
    def isTemplateParameter(self) -> bool:
        """
        The query isTemplateParameter() determines if this ParameterableElement is exposed as a formal
         TemplateParameter.
        [ParameterableElement operation (query); params: none; returns: bool; stub - metamodel metadat
        a only]
        """
        raise NotImplementedError

class NamedElement(Element):
    """A NamedElement is an Element in a model that may have a name. The name may be given directly and/or via the use of a StringExpression."""
    _PKG = "CommonStructure"
    # (owner / namespace properties are hardcoded on _Element)
    _DECL = {
    # Indicates the Dependencies that reference this NamedElement as a client.
    'clientDependency': _Ref('clientDependency', "Dependency", derived=True, multi=True, lo=0, hi='*', subsets=("directedRelationship",), assoc="A_clientDependency_client"),
    # The name of the NamedElement.
    'name': _Ref('name', str),
    # The StringExpression used to define the name of this NamedElement.
    'nameExpression': _Ref('nameExpression', "StringExpression", composite=True, subsets=("ownedElement",), assoc="A_nameExpression_namedElement"),
    # A name that allows the NamedElement to be identified within a hierarchy of nested Namespaces. It
    #  is constructed from the names of the containing Namespaces starting at the root of the hierarch
    # y and ending with the name of the NamedElement itself.
    'qualifiedName': _Ref('qualifiedName', str, derived=True, readonly=True),
    # Determines whether and how the NamedElement is visible outside its owning Namespace.
    'visibility': _Ref('visibility', VisibilityKind),
    }
    _UNIONS = {
        "directedRelationship": ("clientDependency",),
        "ownedElement": ("nameExpression",),
        "relationship": ("clientDependency",),
    }
    CONSTRAINTS = (
        ("visibility_needs_ownership",
         "(namespace = null and owner <> null) implies visibility = null"
        ),
        ("has_qualified_name",
         "(name <> null and allNamespaces()->select(ns | ns.name = null)->isEmpty()) implies quali"
         "fiedName = allNamespaces()->iterate( ns : Namespace; agg: String = name | ns.name.concat"
         "(self.separator()).concat(agg))"
        ),
        ("has_no_qualified_name",
         "name=null or allNamespaces()->select( ns | ns.name=null )->notEmpty() implies qualifiedN"
         "ame = null"
        ),
    )
    def allNamespaces(self) -> "Namespace":
        """
        The query allNamespaces() gives the sequence of Namespaces in which the NamedElement is nested
        , working outwards.
        [NamedElement operation (query); params: none; returns: "Namespace"; stub - metamodel metadata
         only]
        """
        raise NotImplementedError
    def allOwningPackages(self) -> "Package":
        """
        The query allOwningPackages() returns the set of all the enclosing Namespaces of this NamedEle
        ment, working outwards, that are Packages, up to but not including the first such Namespace th
        at is not a Package.
        [NamedElement operation (query); params: none; returns: "Package"; stub - metamodel metadata o
        nly]
        """
        raise NotImplementedError
    def isDistinguishableFrom(self, n: "NamedElement" = None, ns: "Namespace" = None) -> bool:
        """
        The query isDistinguishableFrom() determines whether two NamedElements may logically co-exist 
        within a Namespace. By default, two named elements are distinguishable if (a) they have types 
        neither of which is a kind of the other or (b) they have different names.
        [NamedElement operation (query); params: n: "NamedElement", ns: "Namespace"; returns: bool; st
        ub - metamodel metadata only]
        """
        raise NotImplementedError
    def qualifiedName(self) -> str:
        """
        When a NamedElement has a name, and all of its containing Namespaces have a name, the qualifie
        dName is constructed from the name of the NamedElement and the names of the containing Namespa
        ces.
        [NamedElement operation (query); params: none; returns: str; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def separator(self) -> str:
        """
        The query separator() gives the string that is used to separate names when constructing a qual
        ifiedName.
        [NamedElement operation (query); params: none; returns: str; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def clientDependency(self) -> "Dependency":
        """
        [NamedElement operation (query); params: none; returns: "Dependency"; stub - metamodel metadat
        a only]
        """
        raise NotImplementedError

class PackageableElement(ParameterableElement, NamedElement):
    """A PackageableElement is a NamedElement that may be owned directly by a Package. A PackageableElement is also able to serve as the parameteredElement of a TemplateParameter."""
    _PKG = "CommonStructure"
    _DECL = {
    # A PackageableElement must have a visibility specified if it is owned by a Namespace. The default
    #  visibility is public.
    'visibility': _Ref('visibility', VisibilityKind, redefines=("visibility",)),
    }
    CONSTRAINTS = (
        ("namespace_needs_visibility",
         "visibility = null implies namespace = null"
        ),
    )

class Dependency(DirectedRelationship, PackageableElement):
    """A Dependency is a Relationship that signifies that a single model Element or a set of model Elements requires other model Elements for their specification or implementation. This means that the complete semantics of the client Element(s) are either semantically or structurally dependent on the definition of the supplier Element(s)."""
    _PKG = "CommonStructure"
    _DECL = {
    # The Element(s) dependent on the supplier Element(s). In some cases (such as a trace Abstraction)
    #  the assignment of direction (that is, the designation of the client Element) is at the discreti
    # on of the modeler and is a stipulation.
    'client': _Ref('client', "NamedElement", multi=True, lo=0, hi='*', subsets=("source",), assoc="A_clientDependency_client"),
    # The Element(s) on which the client Element(s) depend in some respect. The modeler may stipulate 
    # a sense of Dependency direction suitable for their domain.
    'supplier': _Ref('supplier', "NamedElement", multi=True, lo=0, hi='*', subsets=("target",), assoc="A_supplier_supplierDependency"),
    }
    _UNIONS = {
        "relatedElement": ("client", "supplier",),
        "source": ("client",),
        "target": ("supplier",),
    }

class Abstraction(Dependency):
    """An Abstraction is a Relationship that relates two Elements or sets of Elements that represent the same concept at different levels of abstraction or from different viewpoints."""
    _PKG = "CommonStructure"
    _DECL = {
    # An OpaqueExpression that states the abstraction relationship between the supplier(s) and the cli
    # ent(s). In some cases, such as derivation, it is usually formal and unidirectional; in other cas
    # es, such as trace, it is usually informal and bidirectional. The mapping expression is optional 
    # and may be omitted if the precise relationship between the Elements is not specified.
    'mapping': _Ref('mapping', "OpaqueExpression", composite=True, subsets=("ownedElement",), assoc="A_mapping_abstraction"),
    }
    _UNIONS = {
        "ownedElement": ("mapping",),
    }

class RedefinableElement(NamedElement):
    """A RedefinableElement is an element that, when defined in the context of a Classifier, can be redefined more specifically or differently in the context of another Classifier that specializes (directly or indirectly) the context Classifier."""
    _PKG = "Classification"
    _DECL = {
    # Indicates whether it is possible to further redefine a RedefinableElement. If the value is true,
    #  then it is not possible to further redefine the RedefinableElement.
    'isLeaf': _Ref('isLeaf', bool),
    # The RedefinableElement that is being redefined by this element.
    'redefinedElement': _Ref('redefinedElement', "RedefinableElement", derived=True, union=True, readonly=True, multi=True, lo=0, hi='*', assoc="A_redefinedElement_redefinableElement"),
    # The contexts that this element may be redefined from.
    'redefinitionContext': _Ref('redefinitionContext', "Classifier", derived=True, union=True, readonly=True, multi=True, lo=0, hi='*', assoc="A_redefinitionContext_redefinableElement"),
    }
    CONSTRAINTS = (
        ("redefinition_consistent",
         "redefinedElement->forAll(re | re.isConsistentWith(self))"
        ),
        ("non_leaf_redefinition",
         "redefinedElement->forAll(re | not re.isLeaf)"
        ),
        ("redefinition_context_valid",
         "redefinedElement->forAll(re | self.isRedefinitionContextValid(re))"
        ),
    )
    def isConsistentWith(self, redefiningElement: "RedefinableElement" = None) -> bool:
        """
        The query isConsistentWith() specifies, for any two RedefinableElements in a context in which 
        redefinition is possible, whether redefinition would be logically consistent. By default, this
         is false; this operation must be overridden for subclasses of RedefinableElement to define th
        e consistency conditions.
        [RedefinableElement operation (query); params: redefiningElement: "RedefinableElement"; return
        s: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isRedefinitionContextValid(self, redefinedElement: "RedefinableElement" = None) -> bool:
        """
        The query isRedefinitionContextValid() specifies whether the redefinition contexts of this Red
        efinableElement are properly related to the redefinition contexts of the specified Redefinable
        Element to allow this element to redefine the other. By default at least one of the redefiniti
        on contexts of this element must be a specialization of at least one of the redefinition conte
        xts of the specified element.
        [RedefinableElement operation (query); params: redefinedElement: "RedefinableElement"; returns
        : bool; stub - metamodel metadata only]
        """
        raise NotImplementedError

class ActivityNode(RedefinableElement):
    """ActivityNode is an abstract class for points in the flow of an Activity connected by ActivityEdges."""
    _PKG = "Activities"
    _DECL = {
    # The Activity containing the ActivityNode, if it is directly owned by an Activity.
    'activity': _Ref('activity', "Activity", subsets=("owner",), assoc="A_node_activity"),
    # ActivityGroups containing the ActivityNode.
    'inGroup': _Ref('inGroup', "ActivityGroup", derived=True, union=True, readonly=True, multi=True, lo=0, hi='*', assoc="A_containedNode_inGroup"),
    # InterruptibleActivityRegions containing the ActivityNode.
    'inInterruptibleRegion': _Ref('inInterruptibleRegion', "InterruptibleActivityRegion", multi=True, lo=0, hi='*', subsets=("inGroup",), assoc="A_inInterruptibleRegion_node"),
    # ActivityPartitions containing the ActivityNode.
    'inPartition': _Ref('inPartition', "ActivityPartition", multi=True, lo=0, hi='*', subsets=("inGroup",), assoc="A_inPartition_node"),
    # The StructuredActivityNode containing the ActvityNode, if it is directly owned by a StructuredAc
    # tivityNode.
    'inStructuredNode': _Ref('inStructuredNode', "StructuredActivityNode", subsets=("inGroup", "owner",), assoc="A_node_inStructuredNode"),
    # ActivityEdges that have the ActivityNode as their target.
    'incoming': _Ref('incoming', "ActivityEdge", multi=True, lo=0, hi='*', assoc="A_incoming_target_node"),
    # ActivityEdges that have the ActivityNode as their source.
    'outgoing': _Ref('outgoing', "ActivityEdge", multi=True, lo=0, hi='*', assoc="A_outgoing_source_node"),
    # ActivityNodes from a generalization of the Activity containining this ActivityNode that are rede
    # fined by this ActivityNode.
    'redefinedNode': _Ref('redefinedNode', "ActivityNode", multi=True, lo=0, hi='*', subsets=("redefinedElement",), assoc="A_redefinedNode_activityNode"),
    }
    _UNIONS = {
        "inGroup": ("inInterruptibleRegion", "inPartition", "inStructuredNode",),
        "owner": ("activity", "inStructuredNode",),
        "redefinedElement": ("redefinedNode",),
    }
    def containingActivity(self) -> "Activity":
        """
        The Activity that directly or indirectly contains this ActivityNode.
        [ActivityNode operation (query); params: none; returns: "Activity"; stub - metamodel metadata 
        only]
        """
        raise NotImplementedError
    def isConsistentWith(self, redefiningElement: "RedefinableElement" = None) -> bool:
        """
        [ActivityNode operation (query); params: redefiningElement: "RedefinableElement"; returns: boo
        l; stub - metamodel metadata only]
        """
        raise NotImplementedError

class ExecutableNode(ActivityNode):
    """An ExecutableNode is an abstract class for ActivityNodes whose execution may be controlled using ControlFlows and to which ExceptionHandlers may be attached."""
    _PKG = "Activities"
    _DECL = {
    # A set of ExceptionHandlers that are examined if an exception propagates out of the ExceptionNode
    # .
    'handler': _Ref('handler', "ExceptionHandler", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_handler_protectedNode"),
    }
    _UNIONS = {
        "ownedElement": ("handler",),
    }

class Action(ExecutableNode):
    """An Action is the fundamental unit of executable functionality. The execution of an Action represents some transformation or processing in the modeled system. Actions provide the ExecutableNodes within Activities and may also be used within Interactions."""
    _PKG = "Actions"
    _DECL = {
    # The context Classifier of the Behavior that contains this Action, or the Behavior itself if it h
    # as no context.
    'context': _Ref('context', "Classifier", derived=True, readonly=True, assoc="A_context_action"),
    # The ordered set of InputPins representing the inputs to the Action.
    'input': _Ref('input', "InputPin", derived=True, union=True, composite=True, readonly=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_input_action"),
    # If true, the Action can begin a new, concurrent execution, even if there is already another exec
    # ution of the Action ongoing. If false, the Action cannot begin a new execution until any previou
    # s execution has completed.
    'isLocallyReentrant': _Ref('isLocallyReentrant', bool),
    # A Constraint that must be satisfied when execution of the Action is completed.
    'localPostcondition': _Ref('localPostcondition', "Constraint", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_localPostcondition_action"),
    # A Constraint that must be satisfied when execution of the Action is started.
    'localPrecondition': _Ref('localPrecondition', "Constraint", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_localPrecondition_action"),
    # The ordered set of OutputPins representing outputs from the Action.
    'output': _Ref('output', "OutputPin", derived=True, union=True, composite=True, readonly=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_output_action"),
    }
    _UNIONS = {
        "ownedElement": ("localPostcondition", "localPrecondition",),
    }
    def context(self) -> "Classifier":
        """
        The derivation for the context property.
        [Action operation (query); params: none; returns: "Classifier"; stub - metamodel metadata only
        ]
        """
        raise NotImplementedError
    def allActions(self) -> "Action":
        """
        Return this Action and all Actions contained directly or indirectly in it. By default only the
         Action itself is returned, but the operation is overridden for StructuredActivityNodes.
        [Action operation (query); params: none; returns: "Action"; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def allOwnedNodes(self) -> "ActivityNode":
        """
        Returns all the ActivityNodes directly or indirectly owned by this Action. This includes at le
        ast all the Pins of the Action.
        [Action operation (query); params: none; returns: "ActivityNode"; stub - metamodel metadata on
        ly]
        """
        raise NotImplementedError
    def containingBehavior(self) -> "Behavior":
        """
        [Action operation (query); params: none; returns: "Behavior"; stub - metamodel metadata only]
        """
        raise NotImplementedError

class AcceptEventAction(Action):
    """An AcceptEventAction is an Action that waits for the occurrence of one or more specific Events."""
    _PKG = "Actions"
    _DECL = {
    # Indicates whether there is a single OutputPin for a SignalEvent occurrence, or multiple OutputPi
    # ns for attribute values of the instance of the Signal associated with a SignalEvent occurrence.
    'isUnmarshall': _Ref('isUnmarshall', bool),
    # OutputPins holding the values received from an Event occurrence.
    'result': _Ref('result', "OutputPin", composite=True, multi=True, lo=0, hi='*', subsets=("output",), assoc="A_result_acceptEventAction"),
    # The Triggers specifying the Events of which the AcceptEventAction waits for occurrences.
    'trigger': _Ref('trigger', "Trigger", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_trigger_acceptEventAction"),
    }
    _UNIONS = {
        "output": ("result",),
        "ownedElement": ("result", "trigger",),
    }
    CONSTRAINTS = (
        ("one_output_pin",
         "not isUnmarshall and trigger->exists(event.oclIsKindOf(SignalEvent) or event.oclIsKindOf"
         "(TimeEvent)) implies output->size() = 1 and output->first().is(1,1)"
        ),
        ("no_input_pins",
         "input->size() = 0"
        ),
        ("no_output_pins",
         "(self.oclIsTypeOf(AcceptEventAction) and (trigger->forAll(event.oclIsKindOf(ChangeEvent)"
         " or event.oclIsKindOf(CallEvent)))) implies output->size() = 0"
        ),
        ("unmarshall_signal_events",
         "isUnmarshall and self.oclIsTypeOf(AcceptEventAction) implies trigger->size()=1 and trigg"
         "er->asSequence()->first().event.oclIsKindOf(SignalEvent) and let attribute: OrderedSet(P"
         "roperty) = trigger->asSequence()->first().event.oclAsType(SignalEvent).signal.allAttribu"
         "tes() in attribute->size()>0 and result->size() = attribute->size() and Sequence{1..resu"
         "lt->size()}->forAll(i | result->at(i).type = attribute->at(i).type and result->at(i).isO"
         "rdered = attribute->at(i).isOrdered and result->at(i).includesMultiplicity(attribute->at"
         "(i)))"
        ),
        ("conforming_type",
         "not isUnmarshall implies result->isEmpty() or let type: Type = result->first().type in t"
         "ype=null or (trigger->forAll(event.oclIsKindOf(SignalEvent)) and trigger.event.oclAsType"
         "(SignalEvent).signal->forAll(s | s.conformsTo(type)))"
        ),
    )

class AcceptCallAction(AcceptEventAction):
    """An AcceptCallAction is an AcceptEventAction that handles the receipt of a synchronous call request. In addition to the values from the Operation input parameters, the Action produces an output that is needed later to supply the information to the ReplyAction necessary to return control to the caller. An AcceptCallAction is for synchronous calls. If it is used to handle an asynchronous call, execution of the subsequent ReplyAction will complete immediately with no effect."""
    _PKG = "Actions"
    _DECL = {
    # An OutputPin where a value is placed containing sufficient information to perform a subsequent R
    # eplyAction and return control to the caller. The contents of this value are opaque. It can be pa
    # ssed and copied but it cannot be manipulated by the model.
    'returnInformation': _Ref('returnInformation', "OutputPin", composite=True, subsets=("output",), assoc="A_returnInformation_acceptCallAction"),
    }
    _UNIONS = {
        "output": ("returnInformation",),
        "ownedElement": ("returnInformation",),
    }
    CONSTRAINTS = (
        ("result_pins",
         "let parameter: OrderedSet(Parameter) = trigger.event->asSequence()->first().oclAsType(Ca"
         "llEvent).operation.inputParameters() in result->size() = parameter->size() and Sequence{"
         "1..result->size()}->forAll(i | parameter->at(i).type.conformsTo(result->at(i).type) and "
         "parameter->at(i).isOrdered = result->at(i).isOrdered and parameter->at(i).compatibleWith"
         "(result->at(i)))"
        ),
        ("trigger_call_event",
         "trigger->size()=1 and trigger->asSequence()->first().event.oclIsKindOf(CallEvent)"
        ),
        ("unmarshall",
         "isUnmarshall = true"
        ),
    )

class InteractionFragment(NamedElement):
    """InteractionFragment is an abstract notion of the most general interaction unit. An InteractionFragment is a piece of an Interaction. Each InteractionFragment is conceptually like an Interaction by itself."""
    _PKG = "Interactions"
    _DECL = {
    # References the Lifelines that the InteractionFragment involves.
    'covered': _Ref('covered', "Lifeline", multi=True, lo=0, hi='*', assoc="A_covered_coveredBy"),
    # The Interaction enclosing this InteractionFragment.
    'enclosingInteraction': _Ref('enclosingInteraction', "Interaction", subsets=("namespace",), assoc="A_fragment_enclosingInteraction"),
    # The operand enclosing this InteractionFragment (they may nest recursively).
    'enclosingOperand': _Ref('enclosingOperand', "InteractionOperand", subsets=("namespace",), assoc="A_fragment_enclosingOperand"),
    # The general ordering relationships contained in this fragment.
    'generalOrdering': _Ref('generalOrdering', "GeneralOrdering", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_generalOrdering_interactionFragment"),
    }
    _UNIONS = {
        "memberNamespace": ("enclosingInteraction", "enclosingOperand",),
        "namespace": ("enclosingInteraction", "enclosingOperand",),
        "ownedElement": ("generalOrdering",),
        "owner": ("enclosingInteraction", "enclosingOperand",),
    }

class ExecutionSpecification(InteractionFragment):
    """An ExecutionSpecification is a specification of the execution of a unit of Behavior or Action within the Lifeline. The duration of an ExecutionSpecification is represented by two OccurrenceSpecifications, the start OccurrenceSpecification and the finish OccurrenceSpecification."""
    _PKG = "Interactions"
    _DECL = {
    # References the OccurrenceSpecification that designates the finish of the Action or Behavior.
    'finish': _Ref('finish', "OccurrenceSpecification", assoc="A_finish_executionSpecification"),
    # References the OccurrenceSpecification that designates the start of the Action or Behavior.
    'start': _Ref('start', "OccurrenceSpecification", assoc="A_start_executionSpecification"),
    }
    CONSTRAINTS = (
        ("same_lifeline",
         "start.covered = finish.covered"
        ),
    )

class ActionExecutionSpecification(ExecutionSpecification):
    """An ActionExecutionSpecification is a kind of ExecutionSpecification representing the execution of an Action."""
    _PKG = "Interactions"
    _DECL = {
    # Action whose execution is occurring.
    'action': _Ref('action', "Action", assoc="A_action_actionExecutionSpecification"),
    }
    CONSTRAINTS = (
        ("action_referenced",
         "(enclosingInteraction->notEmpty() or enclosingOperand.combinedFragment->notEmpty()) and "
         "let parentInteraction : Set(Interaction) = enclosingInteraction.oclAsType(Interaction)->"
         "asSet()->union( enclosingOperand.combinedFragment->closure(enclosingOperand.combinedFrag"
         "ment)-> collect(enclosingInteraction).oclAsType(Interaction)->asSet()) in (parentInterac"
         "tion->size() = 1) and self.action.interaction->asSet() = parentInteraction"
        ),
    )

class TypedElement(NamedElement):
    """A TypedElement is a NamedElement that may have a Type specified for it."""
    _PKG = "CommonStructure"
    _DECL = {
    # The type of the TypedElement.
    'type': _Ref('type', "Type", assoc="A_type_typedElement"),
    }

class ObjectNode(ActivityNode, TypedElement):
    """An ObjectNode is an abstract ActivityNode that may hold tokens within the object flow in an Activity. ObjectNodes also support token selection, limitation on the number of tokens held, specification of the state required for tokens being held, and carrying control values."""
    _PKG = "Activities"
    _DECL = {
    # The States required to be associated with the values held by tokens on this ObjectNode.
    'inState': _Ref('inState', "State", multi=True, lo=0, hi='*', assoc="A_inState_objectNode"),
    # Indicates whether the type of the ObjectNode is to be treated as representing control values tha
    # t may traverse ControlFlows.
    'isControlType': _Ref('isControlType', bool),
    # Indicates how the tokens held by the ObjectNode are ordered for selection to traverse ActivityEd
    # ges outgoing from the ObjectNode.
    'ordering': _Ref('ordering', ObjectNodeOrderingKind),
    # A Behavior used to select tokens to be offered on outgoing ActivityEdges.
    'selection': _Ref('selection', "Behavior", assoc="A_selection_objectNode"),
    # The maximum number of tokens that may be held by this ObjectNode. Tokens cannot flow into the Ob
    # jectNode if the upperBound is reached. If no upperBound is specified, then there is no limit on 
    # how many tokens the ObjectNode can hold.
    'upperBound': _Ref('upperBound', "ValueSpecification", composite=True, subsets=("ownedElement",), assoc="A_upperBound_objectNode"),
    }
    _UNIONS = {
        "ownedElement": ("upperBound",),
    }
    CONSTRAINTS = (
        ("input_output_parameter",
         "selection<>null implies selection.inputParameters()->size()=1 and selection.inputParamet"
         "ers()->forAll(p | not p.isUnique and p.is(0,*) and self.type.conformsTo(p.type)) and sel"
         "ection.outputParameters()->size()=1 and selection.inputParameters()->forAll(p | self.typ"
         "e.conformsTo(p.type))"
        ),
        ("selection_behavior",
         "(selection<>null) = (ordering=ObjectNodeOrderingKind::ordered)"
        ),
        ("object_flow_edges",
         "(not isControlType) implies incoming->union(outgoing)->forAll(oclIsKindOf(ObjectFlow))"
        ),
    )

class MultiplicityElement(Element):
    """A multiplicity is a definition of an inclusive interval of non-negative integers beginning with a lower bound and ending with a (possibly infinite) upper bound. A MultiplicityElement embeds this information to specify the allowable cardinalities for an instantiation of the Element."""
    _PKG = "CommonStructure"
    _DECL = {
    # For a multivalued multiplicity, this attribute specifies whether the values in an instantiation 
    # of this MultiplicityElement are sequentially ordered.
    'isOrdered': _Ref('isOrdered', bool),
    # For a multivalued multiplicity, this attributes specifies whether the values in an instantiation
    #  of this MultiplicityElement are unique.
    'isUnique': _Ref('isUnique', bool),
    # The lower bound of the multiplicity interval.
    'lower': _Ref('lower', int, derived=True),
    # The specification of the lower bound for this multiplicity.
    'lowerValue': _Ref('lowerValue', "ValueSpecification", composite=True, subsets=("ownedElement",), assoc="A_lowerValue_owningLower"),
    # The upper bound of the multiplicity interval.
    'upper': _Ref('upper', UnlimitedNatural, derived=True),
    # The specification of the upper bound for this multiplicity.
    'upperValue': _Ref('upperValue', "ValueSpecification", composite=True, subsets=("ownedElement",), assoc="A_upperValue_owningUpper"),
    }
    _UNIONS = {
        "ownedElement": ("lowerValue", "upperValue",),
    }
    CONSTRAINTS = (
        ("upper_ge_lower",
         "upperBound() >= lowerBound()"
        ),
        ("lower_ge_0",
         "lowerBound() >= 0"
        ),
        ("value_specification_no_side_effects",
         "(no specification serialized)"
        ),
        ("value_specification_constant",
         "(no specification serialized)"
        ),
        ("lower_is_integer",
         "lowerValue <> null implies lowerValue.integerValue() <> null"
        ),
        ("upper_is_unlimitedNatural",
         "upperValue <> null implies upperValue.unlimitedValue() <> null"
        ),
    )
    def compatibleWith(self, other: "MultiplicityElement" = None) -> bool:
        """
        The operation compatibleWith takes another multiplicity as input. It returns true if the other
         multiplicity is wider than, or the same as, self.
        [MultiplicityElement operation (query); params: other: "MultiplicityElement"; returns: bool; s
        tub - metamodel metadata only]
        """
        raise NotImplementedError
    def includesMultiplicity(self, M: "MultiplicityElement" = None) -> bool:
        """
        The query includesMultiplicity() checks whether this multiplicity includes all the cardinaliti
        es allowed by the specified multiplicity.
        [MultiplicityElement operation (query); params: M: "MultiplicityElement"; returns: bool; stub 
        - metamodel metadata only]
        """
        raise NotImplementedError
    def is_(self, lowerbound: int = None, upperbound: UnlimitedNatural = None) -> bool:
        """
        The operation is determines if the upper and lower bound of the ranges are the ones given.
        [MultiplicityElement operation (query); params: lowerbound: int, upperbound: UnlimitedNatural;
         returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isMultivalued(self) -> bool:
        """
        The query isMultivalued() checks whether this multiplicity has an upper bound greater than one
        .
        [MultiplicityElement operation (query); params: none; returns: bool; stub - metamodel metadata
         only]
        """
        raise NotImplementedError
    def lower(self) -> int:
        """
        The derived lower attribute must equal the lowerBound.
        [MultiplicityElement operation (query); params: none; returns: int; stub - metamodel metadata 
        only]
        """
        raise NotImplementedError
    def lowerBound(self) -> int:
        """
        The query lowerBound() returns the lower bound of the multiplicity as an integer, which is the
         integerValue of lowerValue, if this is given, and 1 otherwise.
        [MultiplicityElement operation (query); params: none; returns: int; stub - metamodel metadata 
        only]
        """
        raise NotImplementedError
    def upper(self) -> UnlimitedNatural:
        """
        The derived upper attribute must equal the upperBound.
        [MultiplicityElement operation (query); params: none; returns: UnlimitedNatural; stub - metamo
        del metadata only]
        """
        raise NotImplementedError
    def upperBound(self) -> UnlimitedNatural:
        """
        The query upperBound() returns the upper bound of the multiplicity for a bounded multiplicity 
        as an unlimited natural, which is the unlimitedNaturalValue of upperValue, if given, and 1, ot
        herwise.
        [MultiplicityElement operation (query); params: none; returns: UnlimitedNatural; stub - metamo
        del metadata only]
        """
        raise NotImplementedError

class Pin(ObjectNode, MultiplicityElement):
    """A Pin is an ObjectNode and MultiplicityElement that provides input values to an Action or accepts output values from an Action."""
    _PKG = "Actions"
    _DECL = {
    # Indicates whether the Pin provides data to the Action or just controls how the Action executes.
    'isControl': _Ref('isControl', bool),
    }
    CONSTRAINTS = (
        ("control_pins",
         "isControl implies isControlType"
        ),
        ("not_unique",
         "not isUnique"
        ),
    )

class InputPin(Pin):
    """An InputPin is a Pin that holds input values to be consumed by an Action."""
    _PKG = "Actions"
    CONSTRAINTS = (
        ("outgoing_edges_structured_only",
         "outgoing->notEmpty() implies action<>null and action.oclIsKindOf(StructuredActivityNode)"
         " and action.oclAsType(StructuredActivityNode).allOwnedNodes()->includesAll(outgoing.targ"
         "et)"
        ),
    )

class ActionInputPin(InputPin):
    """An ActionInputPin is a kind of InputPin that executes an Action to determine the values to input to another Action."""
    _PKG = "Actions"
    _DECL = {
    # The Action used to provide the values of the ActionInputPin.
    'fromAction': _Ref('fromAction', "Action", composite=True, subsets=("ownedElement",), assoc="A_fromAction_actionInputPin"),
    }
    _UNIONS = {
        "ownedElement": ("fromAction",),
    }
    CONSTRAINTS = (
        ("input_pin",
         "fromAction.input->forAll(oclIsKindOf(ActionInputPin))"
        ),
        ("one_output_pin",
         "fromAction.output->size() = 1"
        ),
        ("no_control_or_object_flow",
         "fromAction.incoming->union(outgoing)->isEmpty() and fromAction.input.incoming->isEmpty()"
         " and fromAction.output.outgoing->isEmpty()"
        ),
    )

class Namespace(NamedElement):
    """A Namespace is an Element in a model that owns and/or imports a set of NamedElements that can be identified by name."""
    _PKG = "CommonStructure"
    _DECL = {
    # References the ElementImports owned by the Namespace.
    'elementImport': _Ref('elementImport', "ElementImport", composite=True, multi=True, lo=0, hi='*', subsets=("directedRelationship", "ownedElement",), assoc="A_elementImport_importingNamespace"),
    # References the PackageableElements that are members of this Namespace as a result of either Pack
    # ageImports or ElementImports.
    'importedMember': _Ref('importedMember', "PackageableElement", derived=True, readonly=True, multi=True, lo=0, hi='*', subsets=("member",), assoc="A_importedMember_namespace"),
    # A collection of NamedElements identifiable within the Namespace, either by being owned or by bei
    # ng introduced by importing or inheritance.
    'member': _Ref('member', "NamedElement", derived=True, union=True, readonly=True, multi=True, lo=0, hi='*', assoc="A_member_memberNamespace"),
    # A collection of NamedElements owned by the Namespace.
    'ownedMember': _Ref('ownedMember', "NamedElement", derived=True, union=True, composite=True, readonly=True, multi=True, lo=0, hi='*', subsets=("ownedElement", "member",), assoc="A_ownedMember_namespace"),
    # Specifies a set of Constraints owned by this Namespace.
    'ownedRule': _Ref('ownedRule', "Constraint", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_ownedRule_context"),
    # References the PackageImports owned by the Namespace.
    'packageImport': _Ref('packageImport', "PackageImport", composite=True, multi=True, lo=0, hi='*', subsets=("directedRelationship", "ownedElement",), assoc="A_packageImport_importingNamespace"),
    }
    _UNIONS = {
        "directedRelationship": ("elementImport", "packageImport",),
        "member": ("importedMember", "ownedRule",),
        "ownedElement": ("elementImport", "ownedRule", "packageImport",),
        "ownedMember": ("ownedRule",),
        "relationship": ("elementImport", "packageImport",),
    }
    CONSTRAINTS = (
        ("members_distinguishable",
         "membersAreDistinguishable()"
        ),
        ("cannot_import_self",
         "packageImport.importedPackage.oclAsType(Namespace)->excludes(self)"
        ),
        ("cannot_import_ownedMembers",
         "elementImport.importedElement.oclAsType(Element)->excludesAll(ownedMember)"
        ),
    )
    def excludeCollisions(self, imps: "PackageableElement" = None) -> "PackageableElement":
        """
        The query excludeCollisions() excludes from a set of PackageableElements any that would not be
         distinguishable from each other in this Namespace.
        [Namespace operation (query); params: imps: "PackageableElement"; returns: "PackageableElement
        "; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def getNamesOfMember(self, element: "NamedElement" = None) -> str:
        """
        The query getNamesOfMember() gives a set of all of the names that a member would have in a Nam
        espace, taking importing into account. In general a member can have multiple names in a Namesp
        ace if it is imported more than once with different aliases.
        [Namespace operation (query); params: element: "NamedElement"; returns: str; stub - metamodel 
        metadata only]
        """
        raise NotImplementedError
    def importMembers(self, imps: "PackageableElement" = None) -> "PackageableElement":
        """
        The query importMembers() defines which of a set of PackageableElements are actually imported 
        into the Namespace. This excludes hidden ones, i.e., those which have names that conflict with
         names of ownedMembers, and it also excludes PackageableElements that would have the indisting
        uishable names when imported.
        [Namespace operation (query); params: imps: "PackageableElement"; returns: "PackageableElement
        "; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def importedMember(self) -> "PackageableElement":
        """
        The importedMember property is derived as the PackageableElements that are members of this Nam
        espace as a result of either PackageImports or ElementImports.
        [Namespace operation (query); params: none; returns: "PackageableElement"; stub - metamodel me
        tadata only]
        """
        raise NotImplementedError
    def membersAreDistinguishable(self) -> bool:
        """
        The Boolean query membersAreDistinguishable() determines whether all of the Namespace's member
        s are distinguishable within it.
        [Namespace operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError

class Type(PackageableElement):
    """A Type constrains the values represented by a TypedElement."""
    _PKG = "CommonStructure"
    _DECL = {
    # Specifies the owning Package of this Type, if any.
    'package': _Ref('package', "Package", subsets=("owningPackage",), assoc="A_ownedType_package"),
    }
    _UNIONS = {
        "memberNamespace": ("package",),
        "namespace": ("package",),
        "owner": ("package",),
    }
    def conformsTo(self, other: "Type" = None) -> bool:
        """
        The query conformsTo() gives true for a Type that conforms to another. By default, two Types d
        o not conform to each other. This query is intended to be redefined for specific conformance s
        ituations.
        [Type operation (query); params: other: "Type"; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError

class TemplateableElement(Element):
    """A TemplateableElement is an Element that can optionally be defined as a template and bound to other templates."""
    _PKG = "CommonStructure"
    _DECL = {
    # The optional TemplateSignature specifying the formal TemplateParameters for this TemplateableEle
    # ment. If a TemplateableElement has a TemplateSignature, then it is a template.
    'ownedTemplateSignature': _Ref('ownedTemplateSignature', "TemplateSignature", composite=True, subsets=("ownedElement",), assoc="A_ownedTemplateSignature_template"),
    # The optional TemplateBindings from this TemplateableElement to one or more templates.
    'templateBinding': _Ref('templateBinding', "TemplateBinding", composite=True, multi=True, lo=0, hi='*', subsets=("directedRelationship", "ownedElement",), assoc="A_templateBinding_boundElement"),
    }
    _UNIONS = {
        "directedRelationship": ("templateBinding",),
        "ownedElement": ("ownedTemplateSignature", "templateBinding",),
        "relationship": ("templateBinding",),
    }
    def isTemplate(self) -> bool:
        """
        The query isTemplate() returns whether this TemplateableElement is actually a template.
        [TemplateableElement operation (query); params: none; returns: bool; stub - metamodel metadata
         only]
        """
        raise NotImplementedError
    def parameterableElements(self) -> "ParameterableElement":
        """
        The query parameterableElements() returns the set of ParameterableElements that may be used as
         the parameteredElements for a TemplateParameter of this TemplateableElement. By default, this
         set includes all the ownedElements. Subclasses may override this operation if they choose to 
        restrict the set of ParameterableElements.
        [TemplateableElement operation (query); params: none; returns: "ParameterableElement"; stub - 
        metamodel metadata only]
        """
        raise NotImplementedError

class Classifier(Type, Namespace, RedefinableElement, TemplateableElement):
    """A Classifier represents a classification of instances according to their Features."""
    _PKG = "Classification"
    _DECL = {
    # All of the Properties that are direct (i.e., not inherited or imported) attributes of the Classi
    # fier.
    'attribute': _Ref('attribute', "Property", derived=True, union=True, readonly=True, multi=True, lo=0, hi='*', subsets=("redefinableElement", "feature",), assoc="A_attribute_classifier"),
    # The CollaborationUses owned by the Classifier.
    'collaborationUse': _Ref('collaborationUse', "CollaborationUse", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_collaborationUse_classifier"),
    # Specifies each Feature directly defined in the classifier. Note that there may be members of the
    #  Classifier that are of the type Feature but are not included, e.g., inherited features.
    'feature': _Ref('feature', "Feature", derived=True, union=True, readonly=True, multi=True, lo=0, hi='*', subsets=("member",), assoc="A_feature_featuringClassifier"),
    # The generalizing Classifiers for this Classifier.
    'general': _Ref('general', "Classifier", derived=True, multi=True, lo=0, hi='*', assoc="A_general_classifier"),
    # The Generalization relationships for this Classifier. These Generalizations navigate to more gen
    # eral Classifiers in the generalization hierarchy.
    'generalization': _Ref('generalization', "Generalization", composite=True, multi=True, lo=0, hi='*', subsets=("directedRelationship", "ownedElement",), assoc="A_generalization_specific"),
    # All elements inherited by this Classifier from its general Classifiers.
    'inheritedMember': _Ref('inheritedMember', "NamedElement", derived=True, readonly=True, multi=True, lo=0, hi='*', subsets=("member",), assoc="A_inheritedMember_inheritingClassifier"),
    # If true, the Classifier can only be instantiated by instantiating one of its specializations. An
    #  abstract Classifier is intended to be used by other Classifiers e.g., as the target of Associat
    # ions or Generalizations.
    'isAbstract': _Ref('isAbstract', bool),
    # If true, the Classifier cannot be specialized.
    'isFinalSpecialization': _Ref('isFinalSpecialization', bool),
    # The optional RedefinableTemplateSignature specifying the formal template parameters.
    'ownedTemplateSignature': _Ref('ownedTemplateSignature', "RedefinableTemplateSignature", composite=True, subsets=("redefinableElement",), redefines=("ownedTemplateSignature",), assoc="A_ownedTemplateSignature_classifier"),
    # The UseCases owned by this classifier.
    'ownedUseCase': _Ref('ownedUseCase', "UseCase", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_ownedUseCase_classifier"),
    # The GeneralizationSet of which this Classifier is a power type.
    'powertypeExtent': _Ref('powertypeExtent', "GeneralizationSet", multi=True, lo=0, hi='*', assoc="A_powertypeExtent_powertype"),
    # The Classifiers redefined by this Classifier.
    'redefinedClassifier': _Ref('redefinedClassifier', "Classifier", multi=True, lo=0, hi='*', subsets=("redefinedElement",), assoc="A_redefinedClassifier_classifier"),
    # A CollaborationUse which indicates the Collaboration that represents this Classifier.
    'representation': _Ref('representation', "CollaborationUse", subsets=("collaborationUse",), assoc="A_representation_classifier"),
    # The Substitutions owned by this Classifier.
    'substitution': _Ref('substitution', "Substitution", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement", "clientDependency",), assoc="A_substitution_substitutingClassifier"),
    # TheClassifierTemplateParameter that exposes this element as a formal parameter.
    'templateParameter': _Ref('templateParameter', "ClassifierTemplateParameter", redefines=("templateParameter",), assoc="A_classifier_templateParameter_parameteredElement"),
    # The set of UseCases for which this Classifier is the subject.
    'useCase': _Ref('useCase', "UseCase", multi=True, lo=0, hi='*', assoc="A_subject_useCase"),
    }
    _UNIONS = {
        "directedRelationship": ("generalization", "substitution",),
        "member": ("inheritedMember", "ownedUseCase",),
        "ownedElement": ("collaborationUse", "generalization", "ownedUseCase", "representation", "substitution",),
        "ownedMember": ("ownedUseCase",),
        "redefinableElement": ("ownedTemplateSignature",),
        "redefinedElement": ("redefinedClassifier",),
        "relationship": ("generalization", "substitution",),
    }
    CONSTRAINTS = (
        ("specialize_type",
         "parents()->forAll(c | self.maySpecializeType(c))"
        ),
        ("maps_to_generalization_set",
         "powertypeExtent->forAll( gs | gs.generalization->forAll( gen | not (gen.general = self) "
         "and not gen.general.allParents()->includes(self) and not (gen.specific = self) and not s"
         "elf.allParents()->includes(gen.specific) ))"
        ),
        ("non_final_parents",
         "parents()->forAll(not isFinalSpecialization)"
        ),
        ("no_cycles_in_generalization",
         "not allParents()->includes(self)"
        ),
    )
    def allFeatures(self) -> "Feature":
        """
        The query allFeatures() gives all of the Features in the namespace of the Classifier. In gener
        al, through mechanisms such as inheritance, this will be a larger set than feature.
        [Classifier operation (query); params: none; returns: "Feature"; stub - metamodel metadata onl
        y]
        """
        raise NotImplementedError
    def allParents(self) -> "Classifier":
        """
        The query allParents() gives all of the direct and indirect ancestors of a generalized Classif
        ier.
        [Classifier operation (query); params: none; returns: "Classifier"; stub - metamodel metadata 
        only]
        """
        raise NotImplementedError
    def conformsTo(self, other: "Type" = None) -> bool:
        """
        The query conformsTo() gives true for a Classifier that defines a type that conforms to anothe
        r. This is used, for example, in the specification of signature conformance for operations.
        [Classifier operation (query); params: other: "Type"; returns: bool; stub - metamodel metadata
         only]
        """
        raise NotImplementedError
    def general(self) -> "Classifier":
        """
        The general Classifiers are the ones referenced by the Generalization relationships.
        [Classifier operation (query); params: none; returns: "Classifier"; stub - metamodel metadata 
        only]
        """
        raise NotImplementedError
    def hasVisibilityOf(self, n: "NamedElement" = None) -> bool:
        """
        The query hasVisibilityOf() determines whether a NamedElement is visible in the classifier. No
        n-private members are visible. It is only called when the argument is something owned by a par
        ent.
        [Classifier operation (query); params: n: "NamedElement"; returns: bool; stub - metamodel meta
        data only]
        """
        raise NotImplementedError
    def inherit(self, inhs: "NamedElement" = None) -> "NamedElement":
        """
        The query inherit() defines how to inherit a set of elements passed as its argument. It exclud
        es redefined elements from the result.
        [Classifier operation (query); params: inhs: "NamedElement"; returns: "NamedElement"; stub - m
        etamodel metadata only]
        """
        raise NotImplementedError
    def inheritableMembers(self, c: "Classifier" = None) -> "NamedElement":
        """
        The query inheritableMembers() gives all of the members of a Classifier that may be inherited 
        in one of its descendants, subject to whatever visibility restrictions apply.
        [Classifier operation (query); params: c: "Classifier"; returns: "NamedElement"; stub - metamo
        del metadata only]
        """
        raise NotImplementedError
    def inheritedMember(self) -> "NamedElement":
        """
        The inheritedMember association is derived by inheriting the inheritable members of the parent
        s.
        [Classifier operation (query); params: none; returns: "NamedElement"; stub - metamodel metadat
        a only]
        """
        raise NotImplementedError
    def isTemplate(self) -> bool:
        """
        The query isTemplate() returns whether this Classifier is actually a template.
        [Classifier operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def maySpecializeType(self, c: "Classifier" = None) -> bool:
        """
        The query maySpecializeType() determines whether this classifier may have a generalization rel
        ationship to classifiers of the specified type. By default a classifier may specialize classif
        iers of the same or a more general type. It is intended to be redefined by classifiers that ha
        ve different specialization constraints.
        [Classifier operation (query); params: c: "Classifier"; returns: bool; stub - metamodel metada
        ta only]
        """
        raise NotImplementedError
    def parents(self) -> "Classifier":
        """
        The query parents() gives all of the immediate ancestors of a generalized Classifier.
        [Classifier operation (query); params: none; returns: "Classifier"; stub - metamodel metadata 
        only]
        """
        raise NotImplementedError
    def directlyRealizedInterfaces(self) -> "Interface":
        """
        The Interfaces directly realized by this Classifier
        [Classifier operation (query); params: none; returns: "Interface"; stub - metamodel metadata o
        nly]
        """
        raise NotImplementedError
    def directlyUsedInterfaces(self) -> "Interface":
        """
        The Interfaces directly used by this Classifier
        [Classifier operation (query); params: none; returns: "Interface"; stub - metamodel metadata o
        nly]
        """
        raise NotImplementedError
    def allRealizedInterfaces(self) -> "Interface":
        """
        The Interfaces realized by this Classifier and all of its generalizations
        [Classifier operation (query); params: none; returns: "Interface"; stub - metamodel metadata o
        nly]
        """
        raise NotImplementedError
    def allUsedInterfaces(self) -> "Interface":
        """
        The Interfaces used by this Classifier and all of its generalizations
        [Classifier operation (query); params: none; returns: "Interface"; stub - metamodel metadata o
        nly]
        """
        raise NotImplementedError
    def isSubstitutableFor(self, contract: "Classifier" = None) -> bool:
        """
        [Classifier operation (query); params: contract: "Classifier"; returns: bool; stub - metamodel
         metadata only]
        """
        raise NotImplementedError
    def allAttributes(self) -> "Property":
        """
        The query allAttributes gives an ordered set of all owned and inherited attributes of the Clas
        sifier. All owned attributes appear before any inherited attributes, and the attributes inheri
        ted from any more specific parent Classifier appear before those of any more general parent Cl
        assifier. However, if the Classifier has multiple immediate parents, then the relative orderin
        g of the sets of attributes from those parents is not defined.
        [Classifier operation (query); params: none; returns: "Property"; stub - metamodel metadata on
        ly]
        """
        raise NotImplementedError
    def allSlottableFeatures(self) -> "StructuralFeature":
        """
        All StructuralFeatures related to the Classifier that may have Slots, including direct attribu
        tes, inherited attributes, private attributes in generalizations, and memberEnds of Associatio
        ns, but excluding redefined StructuralFeatures.
        [Classifier operation (query); params: none; returns: "StructuralFeature"; stub - metamodel me
        tadata only]
        """
        raise NotImplementedError

class BehavioredClassifier(Classifier):
    """A BehavioredClassifier may have InterfaceRealizations, and owns a set of Behaviors one of which may specify the behavior of the BehavioredClassifier itself."""
    _PKG = "SimpleClassifiers"
    _DECL = {
    # A Behavior that specifies the behavior of the BehavioredClassifier itself.
    'classifierBehavior': _Ref('classifierBehavior', "Behavior", subsets=("ownedBehavior",), assoc="A_classifierBehavior_behavioredClassifier"),
    # The set of InterfaceRealizations owned by the BehavioredClassifier. Interface realizations refer
    # ence the Interfaces of which the BehavioredClassifier is an implementation.
    'interfaceRealization': _Ref('interfaceRealization', "InterfaceRealization", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement", "clientDependency",), assoc="A_interfaceRealization_implementingClassifier"),
    # Behaviors owned by a BehavioredClassifier.
    'ownedBehavior': _Ref('ownedBehavior', "Behavior", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_ownedBehavior_behavioredClassifier"),
    }
    _UNIONS = {
        "directedRelationship": ("interfaceRealization",),
        "member": ("classifierBehavior", "ownedBehavior",),
        "ownedElement": ("classifierBehavior", "interfaceRealization", "ownedBehavior",),
        "ownedMember": ("classifierBehavior", "ownedBehavior",),
        "relationship": ("interfaceRealization",),
    }
    CONSTRAINTS = (
        ("class_behavior",
         "classifierBehavior->notEmpty() implies classifierBehavior.specification->isEmpty()"
        ),
    )

class StructuredClassifier(Classifier):
    """StructuredClassifiers may contain an internal structure of connected elements each of which plays a role in the overall Behavior modeled by the StructuredClassifier."""
    _PKG = "StructuredClassifiers"
    _DECL = {
    # The Properties owned by the StructuredClassifier.
    'ownedAttribute': _Ref('ownedAttribute', "Property", composite=True, multi=True, lo=0, hi='*', subsets=("attribute", "ownedMember", "role",), assoc="A_ownedAttribute_structuredClassifier"),
    # The connectors owned by the StructuredClassifier.
    'ownedConnector': _Ref('ownedConnector', "Connector", composite=True, multi=True, lo=0, hi='*', subsets=("redefinableElement", "feature", "ownedMember",), assoc="A_ownedConnector_structuredClassifier"),
    # The Properties specifying instances that the StructuredClassifier owns by composition. This coll
    # ection is derived, selecting those owned Properties where isComposite is true.
    'part': _Ref('part', "Property", derived=True, readonly=True, multi=True, lo=0, hi='*', assoc="A_part_structuredClassifier"),
    # The roles that instances may play in this StructuredClassifier.
    'role': _Ref('role', "ConnectableElement", derived=True, union=True, readonly=True, multi=True, lo=0, hi='*', subsets=("member",), assoc="A_role_structuredClassifier"),
    }
    _UNIONS = {
        "attribute": ("ownedAttribute",),
        "feature": ("ownedAttribute", "ownedConnector",),
        "member": ("ownedAttribute", "ownedConnector",),
        "ownedElement": ("ownedAttribute", "ownedConnector",),
        "ownedMember": ("ownedAttribute", "ownedConnector",),
        "redefinableElement": ("ownedAttribute", "ownedConnector",),
        "role": ("ownedAttribute",),
    }
    def part(self) -> "Property":
        """
        Derivation for StructuredClassifier::/part
        [StructuredClassifier operation (query); params: none; returns: "Property"; stub - metamodel m
        etadata only]
        """
        raise NotImplementedError
    def allRoles(self) -> "ConnectableElement":
        """
        All features of type ConnectableElement, equivalent to all direct and inherited roles.
        [StructuredClassifier operation (query); params: none; returns: "ConnectableElement"; stub - m
        etamodel metadata only]
        """
        raise NotImplementedError

class EncapsulatedClassifier(StructuredClassifier):
    """An EncapsulatedClassifier may own Ports to specify typed interaction points."""
    _PKG = "StructuredClassifiers"
    _DECL = {
    # The Ports owned by the EncapsulatedClassifier.
    'ownedPort': _Ref('ownedPort', "Port", derived=True, composite=True, readonly=True, multi=True, lo=0, hi='*', subsets=("ownedAttribute",), assoc="A_ownedPort_encapsulatedClassifier"),
    }
    _UNIONS = {
        "attribute": ("ownedPort",),
        "feature": ("ownedPort",),
        "member": ("ownedPort",),
        "ownedElement": ("ownedPort",),
        "ownedMember": ("ownedPort",),
        "redefinableElement": ("ownedPort",),
        "role": ("ownedPort",),
    }
    def ownedPort(self) -> "Port":
        """
        Derivation for EncapsulatedClassifier::/ownedPort : Port
        [EncapsulatedClassifier operation (query); params: none; returns: "Port"; stub - metamodel met
        adata only]
        """
        raise NotImplementedError

class Class(EncapsulatedClassifier, BehavioredClassifier):
    """A Class classifies a set of objects and specifies the features that characterize the structure and behavior of those objects. A Class may have an internal structure and Ports."""
    _PKG = "StructuredClassifiers"
    _DECL = {
    # This property is used when the Class is acting as a metaclass. It references the Extensions that
    #  specify additional properties of the metaclass. The property is derived from the Extensions who
    # se memberEnds are typed by the Class.
    'extension': _Ref('extension', "Extension", derived=True, readonly=True, multi=True, lo=0, hi='*', assoc="A_extension_metaclass"),
    # If true, the Class does not provide a complete declaration and cannot be instantiated. An abstra
    # ct Class is typically used as a target of Associations or Generalizations.
    'isAbstract': _Ref('isAbstract', bool, redefines=("isAbstract",)),
    # Determines whether an object specified by this Class is active or not. If true, then the owning 
    # Class is referred to as an active Class. If false, then such a Class is referred to as a passive
    #  Class.
    'isActive': _Ref('isActive', bool),
    # The Classifiers owned by the Class that are not ownedBehaviors.
    'nestedClassifier': _Ref('nestedClassifier', "Classifier", composite=True, multi=True, lo=0, hi='*', subsets=("redefinableElement", "ownedMember",), assoc="A_nestedClassifier_nestingClass"),
    # The attributes (i.e., the Properties) owned by the Class.
    'ownedAttribute': _Ref('ownedAttribute', "Property", composite=True, multi=True, lo=0, hi='*', subsets=("attribute", "ownedMember",), redefines=("ownedAttribute",), assoc="A_ownedAttribute_class"),
    # The Operations owned by the Class.
    'ownedOperation': _Ref('ownedOperation', "Operation", composite=True, multi=True, lo=0, hi='*', subsets=("redefinableElement", "feature", "ownedMember",), assoc="A_ownedOperation_class"),
    # The Receptions owned by the Class.
    'ownedReception': _Ref('ownedReception', "Reception", composite=True, multi=True, lo=0, hi='*', subsets=("feature", "ownedMember",), assoc="A_ownedReception_class"),
    # The superclasses of a Class, derived from its Generalizations.
    'superClass': _Ref('superClass', "Class", derived=True, multi=True, lo=0, hi='*', redefines=("general",), assoc="A_superClass_class"),
    }
    _UNIONS = {
        "attribute": ("ownedAttribute",),
        "feature": ("ownedAttribute", "ownedOperation", "ownedReception",),
        "member": ("nestedClassifier", "ownedAttribute", "ownedOperation", "ownedReception",),
        "ownedElement": ("nestedClassifier", "ownedAttribute", "ownedOperation", "ownedReception",),
        "ownedMember": ("nestedClassifier", "ownedAttribute", "ownedOperation", "ownedReception",),
        "redefinableElement": ("nestedClassifier", "ownedAttribute", "ownedOperation",),
    }
    CONSTRAINTS = (
        ("passive_class",
         "not isActive implies (ownedReception->isEmpty() and classifierBehavior = null)"
        ),
    )
    def extension(self) -> "Extension":
        """
        Derivation for Class::/extension : Extension
        [Class operation (query); params: none; returns: "Extension"; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def superClass(self) -> "Class":
        """
        Derivation for Class::/superClass : Class
        [Class operation (query); params: none; returns: "Class"; stub - metamodel metadata only]
        """
        raise NotImplementedError

class Behavior(Class):
    """Behavior is a specification of how its context BehavioredClassifier changes state over time. This specification may be either a definition of possible behavior execution or emergent behavior, or a selective illustration of an interesting subset of possible executions. The latter form is typically used for capturing examples, such as a trace of a particular execution."""
    _PKG = "CommonBehavior"
    _DECL = {
    # The BehavioredClassifier that is the context for the execution of the Behavior. A Behavior that 
    # is directly owned as a nestedClassifier does not have a context. Otherwise, to determine the con
    # text of a Behavior, find the first BehavioredClassifier reached by following the chain of owner 
    # relationships from the Behavior, if any. If there is such a BehavioredClassifier, then it is the
    #  context, unless it is itself a Behavior with a non-empty context, in which case that is also th
    # e context for the original Behavior. For example, following this algorithm, the context of an en
    # try Behavior in a StateMachine is the BehavioredClassifier that owns the StateMachine. The featu
    # res of the context BehavioredClassifier as well as the Elements visible to the context Classifie
    # r are visible to the Behavior.
    'context': _Ref('context', "BehavioredClassifier", derived=True, readonly=True, subsets=("redefinitionContext",), assoc="A_context_behavior"),
    # Tells whether the Behavior can be invoked while it is still executing from a previous invocation
    # .
    'isReentrant': _Ref('isReentrant', bool),
    # References a list of Parameters to the Behavior which describes the order and type of arguments 
    # that can be given when the Behavior is invoked and of the values which will be returned when the
    #  Behavior completes its execution.
    'ownedParameter': _Ref('ownedParameter', "Parameter", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_ownedParameter_behavior"),
    # The ParameterSets owned by this Behavior.
    'ownedParameterSet': _Ref('ownedParameterSet', "ParameterSet", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_ownedParameterSet_behavior"),
    # An optional set of Constraints specifying what is fulfilled after the execution of the Behavior 
    # is completed, if its precondition was fulfilled before its invocation.
    'postcondition': _Ref('postcondition', "Constraint", composite=True, multi=True, lo=0, hi='*', subsets=("ownedRule",), assoc="A_postcondition_behavior"),
    # An optional set of Constraints specifying what must be fulfilled before the Behavior is invoked.
    'precondition': _Ref('precondition', "Constraint", composite=True, multi=True, lo=0, hi='*', subsets=("ownedRule",), assoc="A_precondition_behavior"),
    # References the Behavior that this Behavior redefines. A subtype of Behavior may redefine any oth
    # er subtype of Behavior. If the Behavior implements a BehavioralFeature, it replaces the redefine
    # d Behavior. If the Behavior is a classifierBehavior, it extends the redefined Behavior.
    'redefinedBehavior': _Ref('redefinedBehavior', "Behavior", multi=True, lo=0, hi='*', subsets=("redefinedClassifier",), assoc="A_redefinedBehavior_behavior"),
    # Designates a BehavioralFeature that the Behavior implements. The BehavioralFeature must be owned
    #  by the BehavioredClassifier that owns the Behavior or be inherited by it. The Parameters of the
    #  BehavioralFeature and the implementing Behavior must match. A Behavior does not need to have a 
    # specification, in which case it either is the classifierBehavior of a BehavioredClassifier or it
    #  can only be invoked by another Behavior of the Classifier.
    'specification': _Ref('specification', "BehavioralFeature", assoc="A_method_specification"),
    }
    _UNIONS = {
        "member": ("ownedParameter", "ownedParameterSet", "postcondition", "precondition",),
        "ownedElement": ("ownedParameter", "ownedParameterSet", "postcondition", "precondition",),
        "ownedMember": ("ownedParameter", "ownedParameterSet", "postcondition", "precondition",),
        "redefinedElement": ("redefinedBehavior",),
        "redefinitionContext": ("context",),
    }
    CONSTRAINTS = (
        ("most_one_behavior",
         "specification <> null implies _'context'.ownedBehavior->select(specification=self.specif"
         "ication)->size() = 1"
        ),
        ("parameters_match",
         "specification <> null implies ownedParameter->size() = specification.ownedParameter->siz"
         "e()"
        ),
        ("feature_of_context_classifier",
         "_'context'.feature->includes(specification)"
        ),
    )
    def context(self) -> "BehavioredClassifier":
        """
        A Behavior that is directly owned as a nestedClassifier does not have a context. Otherwise, to
         determine the context of a Behavior, find the first BehavioredClassifier reached by following
         the chain of owner relationships from the Behavior, if any. If there is such a BehavioredClas
        sifier, then it is the context, unless it is itself a Behavior with a non-empty context, in wh
        ich case that is also the context for the original Behavior.
        [Behavior operation (query); params: none; returns: "BehavioredClassifier"; stub - metamodel m
        etadata only]
        """
        raise NotImplementedError
    def behavioredClassifier(self, from_: "Element" = None) -> "BehavioredClassifier":
        """
        The first BehavioredClassifier reached by following the chain of owner relationships from the 
        Behavior, if any.
        [Behavior operation (query); params: from_: "Element"; returns: "BehavioredClassifier"; stub -
         metamodel metadata only]
        """
        raise NotImplementedError
    def inputParameters(self) -> "Parameter":
        """
        The in and inout ownedParameters of the Behavior.
        [Behavior operation (query); params: none; returns: "Parameter"; stub - metamodel metadata onl
        y]
        """
        raise NotImplementedError
    def outputParameters(self) -> "Parameter":
        """
        The out, inout and return ownedParameters.
        [Behavior operation (query); params: none; returns: "Parameter"; stub - metamodel metadata onl
        y]
        """
        raise NotImplementedError

class Activity(Behavior):
    """An Activity is the specification of parameterized Behavior as the coordinated sequencing of subordinate units."""
    _PKG = "Activities"
    _DECL = {
    # ActivityEdges expressing flow between the nodes of the Activity.
    'edge': _Ref('edge', "ActivityEdge", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_edge_activity"),
    # Top-level ActivityGroups in the Activity.
    'group': _Ref('group', "ActivityGroup", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_group_inActivity"),
    # If true, this Activity must not make any changes to objects. The default is false (an Activity m
    # ay make nonlocal changes). (This is an assertion, not an executable property. It may be used by 
    # an execution engine to optimize model execution. If the assertion is violated by the Activity, t
    # hen the model is ill-formed.)
    'isReadOnly': _Ref('isReadOnly', bool),
    # If true, all invocations of the Activity are handled by the same execution.
    'isSingleExecution': _Ref('isSingleExecution', bool),
    # ActivityNodes coordinated by the Activity.
    'node': _Ref('node', "ActivityNode", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_node_activity"),
    # Top-level ActivityPartitions in the Activity.
    'partition': _Ref('partition', "ActivityPartition", multi=True, lo=0, hi='*', subsets=("group",), assoc="A_partition_activity"),
    # Top-level StructuredActivityNodes in the Activity.
    'structuredNode': _Ref('structuredNode', "StructuredActivityNode", composite=True, multi=True, lo=0, hi='*', subsets=("group", "node",), assoc="A_structuredNode_activity"),
    # Top-level Variables defined by the Activity.
    'variable': _Ref('variable', "Variable", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_variable_activityScope"),
    }
    _UNIONS = {
        "member": ("variable",),
        "ownedElement": ("edge", "group", "node", "partition", "structuredNode", "variable",),
        "ownedMember": ("variable",),
    }
    CONSTRAINTS = (
        ("maximum_one_parameter_node",
         "ownedParameter->forAll(p | p.direction <> ParameterDirectionKind::inout implies node->se"
         "lect( oclIsKindOf(ActivityParameterNode) and oclAsType(ActivityParameterNode).parameter "
         "= p)->size()= 1)"
        ),
        ("maximum_two_parameter_nodes",
         "ownedParameter->forAll(p | p.direction = ParameterDirectionKind::inout implies let assoc"
         "iatedNodes : Set(ActivityNode) = node->select( oclIsKindOf(ActivityParameterNode) and oc"
         "lAsType(ActivityParameterNode).parameter = p) in associatedNodes->size()=2 and associate"
         "dNodes->select(incoming->notEmpty())->size()<=1 and associatedNodes->select(outgoing->no"
         "tEmpty())->size()<=1 )"
        ),
    )

class ActivityEdge(RedefinableElement):
    """An ActivityEdge is an abstract class for directed connections between two ActivityNodes."""
    _PKG = "Activities"
    _DECL = {
    # The Activity containing the ActivityEdge, if it is directly owned by an Activity.
    'activity': _Ref('activity', "Activity", subsets=("owner",), assoc="A_edge_activity"),
    # A ValueSpecification that is evaluated to determine if a token can traverse the ActivityEdge. If
    #  an ActivityEdge has no guard, then there is no restriction on tokens traversing the edge.
    'guard': _Ref('guard', "ValueSpecification", composite=True, subsets=("ownedElement",), assoc="A_guard_activityEdge"),
    # ActivityGroups containing the ActivityEdge.
    'inGroup': _Ref('inGroup', "ActivityGroup", derived=True, union=True, readonly=True, multi=True, lo=0, hi='*', assoc="A_containedEdge_inGroup"),
    # ActivityPartitions containing the ActivityEdge.
    'inPartition': _Ref('inPartition', "ActivityPartition", multi=True, lo=0, hi='*', subsets=("inGroup",), assoc="A_edge_inPartition"),
    # The StructuredActivityNode containing the ActivityEdge, if it is owned by a StructuredActivityNo
    # de.
    'inStructuredNode': _Ref('inStructuredNode', "StructuredActivityNode", subsets=("inGroup", "owner",), assoc="A_edge_inStructuredNode"),
    # The InterruptibleActivityRegion for which this ActivityEdge is an interruptingEdge.
    'interrupts': _Ref('interrupts', "InterruptibleActivityRegion", assoc="A_interruptingEdge_interrupts"),
    # ActivityEdges from a generalization of the Activity containing this ActivityEdge that are redefi
    # ned by this ActivityEdge.
    'redefinedEdge': _Ref('redefinedEdge', "ActivityEdge", multi=True, lo=0, hi='*', subsets=("redefinedElement",), assoc="A_redefinedEdge_activityEdge"),
    # The ActivityNode from which tokens are taken when they traverse the ActivityEdge.
    'source': _Ref('source', "ActivityNode", assoc="A_outgoing_source_node"),
    # The ActivityNode to which tokens are put when they traverse the ActivityEdge.
    'target': _Ref('target', "ActivityNode", assoc="A_incoming_target_node"),
    # The minimum number of tokens that must traverse the ActivityEdge at the same time. If no weight 
    # is specified, this is equivalent to specifying a constant value of 1.
    'weight': _Ref('weight', "ValueSpecification", composite=True, subsets=("ownedElement",), assoc="A_weight_activityEdge"),
    }
    _UNIONS = {
        "inGroup": ("inPartition", "inStructuredNode",),
        "ownedElement": ("guard", "weight",),
        "owner": ("activity", "inStructuredNode",),
        "redefinedElement": ("redefinedEdge",),
    }
    CONSTRAINTS = (
        ("source_and_target",
         "activity<>null implies source.containingActivity() = activity and target.containingActiv"
         "ity() = activity"
        ),
    )
    def isConsistentWith(self, redefiningElement: "RedefinableElement" = None) -> bool:
        """
        [ActivityEdge operation (query); params: redefiningElement: "RedefinableElement"; returns: boo
        l; stub - metamodel metadata only]
        """
        raise NotImplementedError

class ControlNode(ActivityNode):
    """A ControlNode is an abstract ActivityNode that coordinates flows in an Activity."""
    _PKG = "Activities"

class FinalNode(ControlNode):
    """A FinalNode is an abstract ControlNode at which a flow in an Activity stops."""
    _PKG = "Activities"
    CONSTRAINTS = (
        ("no_outgoing_edges",
         "outgoing->isEmpty()"
        ),
    )

class ActivityFinalNode(FinalNode):
    """An ActivityFinalNode is a FinalNode that terminates the execution of its owning Activity or StructuredActivityNode."""
    _PKG = "Activities"

class ActivityGroup(NamedElement):
    """ActivityGroup is an abstract class for defining sets of ActivityNodes and ActivityEdges in an Activity."""
    _PKG = "Activities"
    _DECL = {
    # ActivityEdges immediately contained in the ActivityGroup.
    'containedEdge': _Ref('containedEdge', "ActivityEdge", derived=True, union=True, readonly=True, multi=True, lo=0, hi='*', assoc="A_containedEdge_inGroup"),
    # ActivityNodes immediately contained in the ActivityGroup.
    'containedNode': _Ref('containedNode', "ActivityNode", derived=True, union=True, readonly=True, multi=True, lo=0, hi='*', assoc="A_containedNode_inGroup"),
    # The Activity containing the ActivityGroup, if it is directly owned by an Activity.
    'inActivity': _Ref('inActivity', "Activity", subsets=("owner",), assoc="A_group_inActivity"),
    # Other ActivityGroups immediately contained in this ActivityGroup.
    'subgroup': _Ref('subgroup', "ActivityGroup", derived=True, union=True, composite=True, readonly=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_subgroup_superGroup"),
    # The ActivityGroup immediately containing this ActivityGroup, if it is directly owned by another 
    # ActivityGroup.
    'superGroup': _Ref('superGroup', "ActivityGroup", derived=True, union=True, readonly=True, subsets=("owner",), assoc="A_subgroup_superGroup"),
    }
    _UNIONS = {
        "owner": ("inActivity",),
    }
    CONSTRAINTS = (
        ("nodes_and_edges",
         "containedNode->forAll(activity = self.containingActivity()) and containedEdge->forAll(ac"
         "tivity = self.containingActivity())"
        ),
        ("not_contained",
         "subgroup->closure(subgroup).containedNode->excludesAll(containedNode) and superGroup->cl"
         "osure(superGroup).containedNode->excludesAll(containedNode) and subgroup->closure(subgro"
         "up).containedEdge->excludesAll(containedEdge) and superGroup->closure(superGroup).contai"
         "nedEdge->excludesAll(containedEdge)"
        ),
    )
    def containingActivity(self) -> "Activity":
        """
        The Activity that directly or indirectly contains this ActivityGroup.
        [ActivityGroup operation (query); params: none; returns: "Activity"; stub - metamodel metadata
         only]
        """
        raise NotImplementedError

class ActivityParameterNode(ObjectNode):
    """An ActivityParameterNode is an ObjectNode for accepting values from the input Parameters or providing values to the output Parameters of an Activity."""
    _PKG = "Activities"
    _DECL = {
    # The Parameter for which the ActivityParameterNode will be accepting or providing values.
    'parameter': _Ref('parameter', "Parameter", assoc="A_parameter_activityParameterNode"),
    }
    CONSTRAINTS = (
        ("no_outgoing_edges",
         "(incoming->notEmpty() and outgoing->isEmpty()) implies (parameter.direction = ParameterD"
         "irectionKind::out or parameter.direction = ParameterDirectionKind::inout or parameter.di"
         "rection = ParameterDirectionKind::return)"
        ),
        ("has_parameters",
         "activity.ownedParameter->includes(parameter)"
        ),
        ("same_type",
         "type = parameter.type"
        ),
        ("no_incoming_edges",
         "(outgoing->notEmpty() and incoming->isEmpty()) implies (parameter.direction = ParameterD"
         "irectionKind::_'in' or parameter.direction = ParameterDirectionKind::inout)"
        ),
        ("no_edges",
         "incoming->isEmpty() or outgoing->isEmpty()"
        ),
    )

class ActivityPartition(ActivityGroup):
    """An ActivityPartition is a kind of ActivityGroup for identifying ActivityNodes that have some characteristic in common."""
    _PKG = "Activities"
    _DECL = {
    # ActivityEdges immediately contained in the ActivityPartition.
    'edge': _Ref('edge', "ActivityEdge", multi=True, lo=0, hi='*', subsets=("containedEdge",), assoc="A_edge_inPartition"),
    # Indicates whether the ActivityPartition groups other ActivityPartitions along a dimension.
    'isDimension': _Ref('isDimension', bool),
    # Indicates whether the ActivityPartition represents an entity to which the partitioning structure
    #  does not apply.
    'isExternal': _Ref('isExternal', bool),
    # ActivityNodes immediately contained in the ActivityPartition.
    'node': _Ref('node', "ActivityNode", multi=True, lo=0, hi='*', subsets=("containedNode",), assoc="A_inPartition_node"),
    # An Element represented by the functionality modeled within the ActivityPartition.
    'represents': _Ref('represents', "Element", assoc="A_represents_activityPartition"),
    # Other ActivityPartitions immediately contained in this ActivityPartition (as its subgroups).
    'subpartition': _Ref('subpartition', "ActivityPartition", composite=True, multi=True, lo=0, hi='*', subsets=("subgroup",), assoc="A_subpartition_superPartition"),
    # Other ActivityPartitions immediately containing this ActivityPartition (as its superGroups).
    'superPartition': _Ref('superPartition', "ActivityPartition", subsets=("superGroup",), assoc="A_subpartition_superPartition"),
    }
    _UNIONS = {
        "containedEdge": ("edge",),
        "containedNode": ("node",),
        "ownedElement": ("subpartition",),
        "owner": ("superPartition",),
        "subgroup": ("subpartition",),
        "superGroup": ("superPartition",),
    }
    CONSTRAINTS = (
        ("represents_classifier",
         "(not isExternal and represents.oclIsKindOf(Classifier) and superPartition->notEmpty()) i"
         "mplies ( let representedClassifier : Classifier = represents.oclAsType(Classifier) in su"
         "perPartition.represents.oclIsKindOf(Classifier) and let representedSuperClassifier : Cla"
         "ssifier = superPartition.represents.oclAsType(Classifier) in (representedSuperClassifier"
         ".oclIsKindOf(BehavioredClassifier) and representedClassifier.oclIsKindOf(Behavior) and r"
         "epresentedSuperClassifier.oclAsType(BehavioredClassifier).ownedBehavior->includes(repres"
         "entedClassifier.oclAsType(Behavior))) or (representedSuperClassifier.oclIsKindOf(Class) "
         "and representedSuperClassifier.oclAsType(Class).nestedClassifier->includes(representedCl"
         "assifier)) or (Association.allInstances()->exists(a | a.memberEnd->exists(end1 | end1.is"
         "Composite and end1.type = representedClassifier and a.memberEnd->exists(end2 | end1<>end"
         "2 and end2.type = representedSuperClassifier)))) )"
        ),
        ("represents_property_and_is_contained",
         "(represents.oclIsKindOf(Property) and superPartition->notEmpty()) implies ( (superPartit"
         "ion.represents.oclIsKindOf(Classifier) and represents.owner = superPartition.represents)"
         " or (superPartition.represents.oclIsKindOf(Property) and represents.owner = superPartiti"
         "on.represents.oclAsType(Property).type) )"
        ),
        ("represents_property",
         "(represents.oclIsKindOf(Property) and superPartition->notEmpty() and superPartition.repr"
         "esents.oclIsKindOf(Classifier)) implies ( let representedClassifier : Classifier = super"
         "Partition.represents.oclAsType(Classifier) in superPartition.subpartition->reject(isExte"
         "rnal)->forAll(p | p.represents.oclIsKindOf(Property) and p.owner=representedClassifier) "
         ")"
        ),
        ("dimension_not_contained",
         "isDimension implies superPartition->isEmpty()"
        ),
    )

class Actor(BehavioredClassifier):
    """An Actor specifies a role played by a user or any other system that interacts with the subject."""
    _PKG = "UseCases"
    CONSTRAINTS = (
        ("associations",
         "Association.allInstances()->forAll( a | a.memberEnd->collect(type)->includes(self) impli"
         "es ( a.memberEnd->size() = 2 and let actorEnd : Property = a.memberEnd->any(type = self)"
         " in actorEnd.opposite.class.oclIsKindOf(UseCase) or ( actorEnd.opposite.class.oclIsKindO"
         "f(Class) and not actorEnd.opposite.class.oclIsKindOf(Behavior)) ) )"
        ),
        ("must_have_name",
         "name->notEmpty()"
        ),
    )

class StructuralFeatureAction(Action):
    """StructuralFeatureAction is an abstract class for all Actions that operate on StructuralFeatures."""
    _PKG = "Actions"
    _DECL = {
    # The InputPin from which the object whose StructuralFeature is to be read or written is obtained.
    'object': _Ref('object', "InputPin", composite=True, subsets=("input",), assoc="A_object_structuralFeatureAction"),
    # The StructuralFeature to be read or written.
    'structuralFeature': _Ref('structuralFeature', "StructuralFeature", assoc="A_structuralFeature_structuralFeatureAction"),
    }
    _UNIONS = {
        "input": ("object",),
        "ownedElement": ("object",),
    }
    CONSTRAINTS = (
        ("multiplicity",
         "object.is(1,1)"
        ),
        ("object_type",
         "object.type.oclAsType(Classifier).allFeatures()->includes(structuralFeature) or object.t"
         "ype.conformsTo(structuralFeature.oclAsType(Property).opposite.type)"
        ),
        ("visibility",
         "structuralFeature.visibility = VisibilityKind::public or _'context'.allFeatures()->inclu"
         "des(structuralFeature) or structuralFeature.visibility=VisibilityKind::protected and _'c"
         "ontext'.conformsTo(structuralFeature.oclAsType(Property).opposite.type.oclAsType(Classif"
         "ier))"
        ),
        ("not_static",
         "not structuralFeature.isStatic"
        ),
        ("one_featuring_classifier",
         "structuralFeature.featuringClassifier->size() = 1"
        ),
    )

class WriteStructuralFeatureAction(StructuralFeatureAction):
    """WriteStructuralFeatureAction is an abstract class for StructuralFeatureActions that change StructuralFeature values."""
    _PKG = "Actions"
    _DECL = {
    # The OutputPin on which is put the input object as modified by the WriteStructuralFeatureAction.
    'result': _Ref('result', "OutputPin", composite=True, subsets=("output",), assoc="A_result_writeStructuralFeatureAction"),
    # The InputPin that provides the value to be added or removed from the StructuralFeature.
    'value': _Ref('value', "InputPin", composite=True, subsets=("input",), assoc="A_value_writeStructuralFeatureAction"),
    }
    _UNIONS = {
        "input": ("value",),
        "output": ("result",),
        "ownedElement": ("result", "value",),
    }
    CONSTRAINTS = (
        ("multiplicity_of_result",
         "result <> null implies result.is(1,1)"
        ),
        ("type_of_value",
         "value <> null implies value.type.conformsTo(structuralFeature.type)"
        ),
        ("multiplicity_of_value",
         "value<>null implies value.is(1,1)"
        ),
        ("type_of_result",
         "result <> null implies result.type = object.type"
        ),
    )

class AddStructuralFeatureValueAction(WriteStructuralFeatureAction):
    """An AddStructuralFeatureValueAction is a WriteStructuralFeatureAction for adding values to a StructuralFeature."""
    _PKG = "Actions"
    _DECL = {
    # The InputPin that gives the position at which to insert the value in an ordered StructuralFeatur
    # e. The type of the insertAt InputPin is UnlimitedNatural, but the value cannot be zero. It is om
    # itted for unordered StructuralFeatures.
    'insertAt': _Ref('insertAt', "InputPin", composite=True, subsets=("input",), assoc="A_insertAt_addStructuralFeatureValueAction"),
    # Specifies whether existing values of the StructuralFeature should be removed before adding the n
    # ew value.
    'isReplaceAll': _Ref('isReplaceAll', bool),
    }
    _UNIONS = {
        "input": ("insertAt",),
        "ownedElement": ("insertAt",),
    }
    CONSTRAINTS = (
        ("required_value",
         "value<>null"
        ),
        ("insertAt_pin",
         "if not structuralFeature.isOrdered then insertAt = null else not isReplaceAll implies in"
         "sertAt<>null and insertAt->forAll(type=UnlimitedNatural and is(1,1.oclAsType(UnlimitedNa"
         "tural))) endif"
        ),
    )

class VariableAction(Action):
    """VariableAction is an abstract class for Actions that operate on a specified Variable."""
    _PKG = "Actions"
    _DECL = {
    # The Variable to be read or written.
    'variable': _Ref('variable', "Variable", assoc="A_variable_variableAction"),
    }
    CONSTRAINTS = (
        ("scope_of_variable",
         "variable.isAccessibleBy(self)"
        ),
    )

class WriteVariableAction(VariableAction):
    """WriteVariableAction is an abstract class for VariableActions that change Variable values."""
    _PKG = "Actions"
    _DECL = {
    # The InputPin that gives the value to be added or removed from the Variable.
    'value': _Ref('value', "InputPin", composite=True, subsets=("input",), assoc="A_value_writeVariableAction"),
    }
    _UNIONS = {
        "input": ("value",),
        "ownedElement": ("value",),
    }
    CONSTRAINTS = (
        ("value_type",
         "value <> null implies value.type.conformsTo(variable.type)"
        ),
        ("multiplicity",
         "value<>null implies value.is(1,1)"
        ),
    )

class AddVariableValueAction(WriteVariableAction):
    """An AddVariableValueAction is a WriteVariableAction for adding values to a Variable."""
    _PKG = "Actions"
    _DECL = {
    # The InputPin that gives the position at which to insert a new value or move an existing value in
    #  ordered Variables. The type of the insertAt InputPin is UnlimitedNatural, but the value cannot 
    # be zero. It is omitted for unordered Variables.
    'insertAt': _Ref('insertAt', "InputPin", composite=True, subsets=("input",), assoc="A_insertAt_addVariableValueAction"),
    # Specifies whether existing values of the Variable should be removed before adding the new value.
    'isReplaceAll': _Ref('isReplaceAll', bool),
    }
    _UNIONS = {
        "input": ("insertAt",),
        "ownedElement": ("insertAt",),
    }
    CONSTRAINTS = (
        ("required_value",
         "value <> null"
        ),
        ("insertAt_pin",
         "if not variable.isOrdered then insertAt = null else not isReplaceAll implies insertAt<>n"
         "ull and insertAt->forAll(type=UnlimitedNatural and is(1,1.oclAsType(UnlimitedNatural))) "
         "endif"
        ),
    )

class Event(PackageableElement):
    """An Event is the specification of some occurrence that may potentially trigger effects by an object."""
    _PKG = "CommonBehavior"

class MessageEvent(Event):
    """A MessageEvent specifies the receipt by an object of either an Operation call or a Signal instance."""
    _PKG = "CommonBehavior"

class AnyReceiveEvent(MessageEvent):
    """A trigger for an AnyReceiveEvent is triggered by the receipt of any message that is not explicitly handled by any related trigger."""
    _PKG = "CommonBehavior"

class DeployedArtifact(NamedElement):
    """A deployed artifact is an artifact or artifact instance that has been deployed to a deployment target."""
    _PKG = "Deployments"

class Artifact(Classifier, DeployedArtifact):
    """An artifact is the specification of a physical piece of information that is used or produced by a software development process, or by deployment and operation of a system. Examples of artifacts include model files, source files, scripts, and binary executable files, a table in a database system, a development deliverable, or a word-processing document, a mail message. An artifact is the source of a deployment to a node."""
    _PKG = "Deployments"
    _DECL = {
    # A concrete name that is used to refer to the Artifact in a physical context. Example: file syste
    # m name, universal resource locator.
    'fileName': _Ref('fileName', str),
    # The set of model elements that are manifested in the Artifact. That is, these model elements are
    #  utilized in the construction (or generation) of the artifact.
    'manifestation': _Ref('manifestation', "Manifestation", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement", "clientDependency",), assoc="A_manifestation_artifact"),
    # The Artifacts that are defined (nested) within the Artifact. The association is a specialization
    #  of the ownedMember association from Namespace to NamedElement.
    'nestedArtifact': _Ref('nestedArtifact', "Artifact", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_nestedArtifact_artifact"),
    # The attributes or association ends defined for the Artifact. The association is a specialization
    #  of the ownedMember association.
    'ownedAttribute': _Ref('ownedAttribute', "Property", composite=True, multi=True, lo=0, hi='*', subsets=("attribute", "ownedMember",), assoc="A_ownedAttribute_artifact"),
    # The Operations defined for the Artifact. The association is a specialization of the ownedMember 
    # association.
    'ownedOperation': _Ref('ownedOperation', "Operation", composite=True, multi=True, lo=0, hi='*', subsets=("redefinableElement", "feature", "ownedMember",), assoc="A_ownedOperation_artifact"),
    }
    _UNIONS = {
        "attribute": ("ownedAttribute",),
        "directedRelationship": ("manifestation",),
        "feature": ("ownedAttribute", "ownedOperation",),
        "member": ("nestedArtifact", "ownedAttribute", "ownedOperation",),
        "ownedElement": ("manifestation", "nestedArtifact", "ownedAttribute", "ownedOperation",),
        "ownedMember": ("nestedArtifact", "ownedAttribute", "ownedOperation",),
        "redefinableElement": ("ownedAttribute", "ownedOperation",),
        "relationship": ("manifestation",),
    }

class Association(Classifier, Relationship):
    """A link is a tuple of values that refer to typed objects. An Association classifies a set of links, each of which is an instance of the Association. Each value in the link refers to an instance of the type of the corresponding end of the Association."""
    _PKG = "StructuredClassifiers"
    _DECL = {
    # The Classifiers that are used as types of the ends of the Association.
    'endType': _Ref('endType', "Type", derived=True, readonly=True, multi=True, lo=0, hi='*', subsets=("relatedElement",), assoc="A_endType_association"),
    # Specifies whether the Association is derived from other model elements such as other Association
    # s.
    'isDerived': _Ref('isDerived', bool),
    # Each end represents participation of instances of the Classifier connected to the end in links o
    # f the Association.
    'memberEnd': _Ref('memberEnd', "Property", multi=True, lo=2, hi='*', subsets=("member",), assoc="A_memberEnd_association"),
    # The navigable ends that are owned by the Association itself.
    'navigableOwnedEnd': _Ref('navigableOwnedEnd', "Property", multi=True, lo=0, hi='*', subsets=("ownedEnd",), assoc="A_navigableOwnedEnd_association"),
    # The ends that are owned by the Association itself.
    'ownedEnd': _Ref('ownedEnd', "Property", composite=True, multi=True, lo=0, hi='*', subsets=("redefinableElement", "memberEnd", "feature", "ownedMember",), assoc="A_ownedEnd_owningAssociation"),
    }
    _UNIONS = {
        "feature": ("navigableOwnedEnd", "ownedEnd",),
        "member": ("memberEnd", "navigableOwnedEnd", "ownedEnd",),
        "ownedElement": ("navigableOwnedEnd", "ownedEnd",),
        "ownedMember": ("navigableOwnedEnd", "ownedEnd",),
        "redefinableElement": ("navigableOwnedEnd", "ownedEnd",),
        "relatedElement": ("endType",),
    }
    CONSTRAINTS = (
        ("specialized_end_number",
         "parents()->select(oclIsKindOf(Association)).oclAsType(Association)->forAll(p | p.memberE"
         "nd->size() = self.memberEnd->size())"
        ),
        ("specialized_end_types",
         "Sequence{1..memberEnd->size()}-> forAll(i | general->select(oclIsKindOf(Association)).oc"
         "lAsType(Association)-> forAll(ga | self.memberEnd->at(i).type.conformsTo(ga.memberEnd->a"
         "t(i).type)))"
        ),
        ("binary_associations",
         "memberEnd->exists(aggregation <> AggregationKind::none) implies (memberEnd->size() = 2 a"
         "nd memberEnd->exists(aggregation = AggregationKind::none))"
        ),
        ("association_ends",
         "memberEnd->size() > 2 implies ownedEnd->includesAll(memberEnd)"
        ),
        ("ends_must_be_typed",
         "memberEnd->forAll(type->notEmpty())"
        ),
    )
    def endType(self) -> "Type":
        """
        endType is derived from the types of the member ends.
        [Association operation (query); params: none; returns: "Type"; stub - metamodel metadata only]
        """
        raise NotImplementedError

class AssociationClass(Class, Association):
    """A model element that has both Association and Class properties. An AssociationClass can be seen as an Association that also has Class properties, or as a Class that also has Association properties. It not only connects a set of Classifiers but also defines a set of Features that belong to the Association itself and not to any of the associated Classifiers."""
    _PKG = "StructuredClassifiers"
    CONSTRAINTS = (
        ("cannot_be_defined",
         "self.endType()->excludes(self) and self.endType()->collect(et|et.oclAsType(Classifier).a"
         "llParents())->flatten()->excludes(self)"
        ),
        ("disjoint_attributes_ends",
         "ownedAttribute->intersection(ownedEnd)->isEmpty()"
        ),
    )

class BehaviorExecutionSpecification(ExecutionSpecification):
    """A BehaviorExecutionSpecification is a kind of ExecutionSpecification representing the execution of a Behavior."""
    _PKG = "Interactions"
    _DECL = {
    # Behavior whose execution is occurring.
    'behavior': _Ref('behavior', "Behavior", assoc="A_behavior_behaviorExecutionSpecification"),
    }

class Feature(RedefinableElement):
    """A Feature declares a behavioral or structural characteristic of Classifiers."""
    _PKG = "Classification"
    _DECL = {
    # The Classifiers that have this Feature as a feature.
    'featuringClassifier': _Ref('featuringClassifier', "Classifier", derived=True, union=True, readonly=True, subsets=("memberNamespace",), assoc="A_feature_featuringClassifier"),
    # Specifies whether this Feature characterizes individual instances classified by the Classifier (
    # false) or the Classifier itself (true).
    'isStatic': _Ref('isStatic', bool),
    }

class BehavioralFeature(Feature, Namespace):
    """A BehavioralFeature is a feature of a Classifier that specifies an aspect of the behavior of its instances. A BehavioralFeature is implemented (realized) by a Behavior. A BehavioralFeature specifies that a Classifier will respond to a designated request by invoking its implementing method."""
    _PKG = "Classification"
    _DECL = {
    # Specifies the semantics of concurrent calls to the same passive instance (i.e., an instance orig
    # inating from a Class with isActive being false). Active instances control access to their own Be
    # havioralFeatures.
    'concurrency': _Ref('concurrency', CallConcurrencyKind),
    # If true, then the BehavioralFeature does not have an implementation, and one must be supplied by
    #  a more specific Classifier. If false, the BehavioralFeature must have an implementation in the 
    # Classifier or one must be inherited.
    'isAbstract': _Ref('isAbstract', bool),
    # A Behavior that implements the BehavioralFeature. There may be at most one Behavior for a partic
    # ular pairing of a Classifier (as owner of the Behavior) and a BehavioralFeature (as specificatio
    # n of the Behavior).
    'method': _Ref('method', "Behavior", multi=True, lo=0, hi='*', assoc="A_method_specification"),
    # The ordered set of formal Parameters of this BehavioralFeature.
    'ownedParameter': _Ref('ownedParameter', "Parameter", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_ownedParameter_ownerFormalParam"),
    # The ParameterSets owned by this BehavioralFeature.
    'ownedParameterSet': _Ref('ownedParameterSet', "ParameterSet", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_ownedParameterSet_behavioralFeature"),
    # The Types representing exceptions that may be raised during an invocation of this BehavioralFeat
    # ure.
    'raisedException': _Ref('raisedException', "Type", multi=True, lo=0, hi='*', assoc="A_raisedException_behavioralFeature"),
    }
    _UNIONS = {
        "member": ("ownedParameter", "ownedParameterSet",),
        "ownedElement": ("ownedParameter", "ownedParameterSet",),
        "ownedMember": ("ownedParameter", "ownedParameterSet",),
    }
    CONSTRAINTS = (
        ("abstract_no_method",
         "isAbstract implies method->isEmpty()"
        ),
    )
    def isDistinguishableFrom(self, n: "NamedElement" = None, ns: "Namespace" = None) -> bool:
        """
        The query isDistinguishableFrom() determines whether two BehavioralFeatures may coexist in the
         same Namespace. It specifies that they must have different signatures.
        [BehavioralFeature operation (query); params: n: "NamedElement", ns: "Namespace"; returns: boo
        l; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def inputParameters(self) -> "Parameter":
        """
        The ownedParameters with direction in and inout.
        [BehavioralFeature operation (query); params: none; returns: "Parameter"; stub - metamodel met
        adata only]
        """
        raise NotImplementedError
    def outputParameters(self) -> "Parameter":
        """
        The ownedParameters with direction out, inout, or return.
        [BehavioralFeature operation (query); params: none; returns: "Parameter"; stub - metamodel met
        adata only]
        """
        raise NotImplementedError

class InvocationAction(Action):
    """InvocationAction is an abstract class for the various actions that request Behavior invocation."""
    _PKG = "Actions"
    _DECL = {
    # The InputPins that provide the argument values passed in the invocation request.
    'argument': _Ref('argument', "InputPin", composite=True, multi=True, lo=0, hi='*', subsets=("input",), assoc="A_argument_invocationAction"),
    # For CallOperationActions, SendSignalActions, and SendObjectActions, an optional Port of the targ
    # et object through which the invocation request is sent.
    'onPort': _Ref('onPort', "Port", assoc="A_onPort_invocationAction"),
    }
    _UNIONS = {
        "input": ("argument",),
        "ownedElement": ("argument",),
    }

class BroadcastSignalAction(InvocationAction):
    """A BroadcastSignalAction is an InvocationAction that transmits a Signal instance to all the potential target objects in the system. Values from the argument InputPins are used to provide values for the attributes of the Signal. The requestor continues execution immediately after the Signal instances are sent out and cannot receive reply values."""
    _PKG = "Actions"
    _DECL = {
    # The Signal whose instances are to be sent.
    'signal': _Ref('signal', "Signal", assoc="A_signal_broadcastSignalAction"),
    }
    CONSTRAINTS = (
        ("number_of_arguments",
         "argument->size() = signal.allAttributes()->size()"
        ),
        ("type_ordering_multiplicity",
         "let attribute: OrderedSet(Property) = signal.allAttributes() in Sequence{1..argument->si"
         "ze()}->forAll(i | argument->at(i).type.conformsTo(attribute->at(i).type) and argument->a"
         "t(i).isOrdered = attribute->at(i).isOrdered and argument->at(i).compatibleWith(attribute"
         "->at(i)))"
        ),
        ("no_onport",
         "onPort=null"
        ),
    )

class CallAction(InvocationAction):
    """CallAction is an abstract class for Actions that invoke a Behavior with given argument values and (if the invocation is synchronous) receive reply values."""
    _PKG = "Actions"
    _DECL = {
    # If true, the call is synchronous and the caller waits for completion of the invoked Behavior. If
    #  false, the call is asynchronous and the caller proceeds immediately and cannot receive return v
    # alues.
    'isSynchronous': _Ref('isSynchronous', bool),
    # The OutputPins on which the reply values from the invocation are placed (if the call is synchron
    # ous).
    'result': _Ref('result', "OutputPin", composite=True, multi=True, lo=0, hi='*', subsets=("output",), assoc="A_result_callAction"),
    }
    _UNIONS = {
        "output": ("result",),
        "ownedElement": ("result",),
    }
    CONSTRAINTS = (
        ("argument_pins",
         "let parameter: OrderedSet(Parameter) = self.inputParameters() in argument->size() = para"
         "meter->size() and Sequence{1..argument->size()}->forAll(i | argument->at(i).type.conform"
         "sTo(parameter->at(i).type) and argument->at(i).isOrdered = parameter->at(i).isOrdered an"
         "d argument->at(i).compatibleWith(parameter->at(i)))"
        ),
        ("result_pins",
         "let parameter: OrderedSet(Parameter) = self.outputParameters() in result->size() = param"
         "eter->size() and Sequence{1..result->size()}->forAll(i | parameter->at(i).type.conformsT"
         "o(result->at(i).type) and parameter->at(i).isOrdered = result->at(i).isOrdered and param"
         "eter->at(i).compatibleWith(result->at(i)))"
        ),
        ("synchronous_call",
         "result->notEmpty() implies isSynchronous"
        ),
    )
    def inputParameters(self) -> "Parameter":
        """
        Return the in and inout ownedParameters of the Behavior or Operation being called. (This opera
        tion is abstract and should be overridden by subclasses of CallAction.)
        [CallAction operation (query); params: none; returns: "Parameter"; stub - metamodel metadata o
        nly]
        """
        raise NotImplementedError
    def outputParameters(self) -> "Parameter":
        """
        Return the inout, out and return ownedParameters of the Behavior or Operation being called. (T
        his operation is abstract and should be overridden by subclasses of CallAction.)
        [CallAction operation (query); params: none; returns: "Parameter"; stub - metamodel metadata o
        nly]
        """
        raise NotImplementedError

class CallBehaviorAction(CallAction):
    """A CallBehaviorAction is a CallAction that invokes a Behavior directly. The argument values of the CallBehaviorAction are passed on the input Parameters of the invoked Behavior. If the call is synchronous, the execution of the CallBehaviorAction waits until the execution of the invoked Behavior completes and the values of output Parameters of the Behavior are placed on the result OutputPins. If the call is asynchronous, the CallBehaviorAction completes immediately and no results values can be provided."""
    _PKG = "Actions"
    _DECL = {
    # The Behavior being invoked.
    'behavior': _Ref('behavior', "Behavior", assoc="A_behavior_callBehaviorAction"),
    }
    CONSTRAINTS = (
        ("no_onport",
         "onPort=null"
        ),
    )
    def outputParameters(self) -> "Parameter":
        """
        Return the inout, out and return ownedParameters of the Behavior being called.
        [CallBehaviorAction operation (query); params: none; returns: "Parameter"; stub - metamodel me
        tadata only]
        """
        raise NotImplementedError
    def inputParameters(self) -> "Parameter":
        """
        Return the in and inout ownedParameters of the Behavior being called.
        [CallBehaviorAction operation (query); params: none; returns: "Parameter"; stub - metamodel me
        tadata only]
        """
        raise NotImplementedError

class CallEvent(MessageEvent):
    """A CallEvent models the receipt by an object of a message invoking a call of an Operation."""
    _PKG = "CommonBehavior"
    _DECL = {
    # Designates the Operation whose invocation raised the CalEvent.
    'operation': _Ref('operation', "Operation", assoc="A_operation_callEvent"),
    }

class CallOperationAction(CallAction):
    """A CallOperationAction is a CallAction that transmits an Operation call request to the target object, where it may cause the invocation of associated Behavior. The argument values of the CallOperationAction are passed on the input Parameters of the Operation. If call is synchronous, the execution of the CallOperationAction waits until the execution of the invoked Operation completes and the values of output Parameters of the Operation are placed on the result OutputPins. If the call is asynchronous, the CallOperationAction completes immediately and no results values can be provided."""
    _PKG = "Actions"
    _DECL = {
    # The Operation being invoked.
    'operation': _Ref('operation', "Operation", assoc="A_operation_callOperationAction"),
    # The InputPin that provides the target object to which the Operation call request is sent.
    'target': _Ref('target', "InputPin", composite=True, subsets=("input",), assoc="A_target_callOperationAction"),
    }
    _UNIONS = {
        "input": ("target",),
        "ownedElement": ("target",),
    }
    CONSTRAINTS = (
        ("type_target_pin",
         "if onPort=null then target.type.oclAsType(Classifier).allFeatures()->includes(operation)"
         " else target.type.oclAsType(Classifier).allFeatures()->includes(onPort) and onPort.provi"
         "ded->union(onPort.required).allFeatures()->includes(operation) endif"
        ),
    )
    def outputParameters(self) -> "Parameter":
        """
        Return the inout, out and return ownedParameters of the Operation being called.
        [CallOperationAction operation (query); params: none; returns: "Parameter"; stub - metamodel m
        etadata only]
        """
        raise NotImplementedError
    def inputParameters(self) -> "Parameter":
        """
        Return the in and inout ownedParameters of the Operation being called.
        [CallOperationAction operation (query); params: none; returns: "Parameter"; stub - metamodel m
        etadata only]
        """
        raise NotImplementedError

class CentralBufferNode(ObjectNode):
    """A CentralBufferNode is an ObjectNode for managing flows from multiple sources and targets."""
    _PKG = "Activities"

class ChangeEvent(Event):
    """A ChangeEvent models a change in the system configuration that makes a condition true."""
    _PKG = "CommonBehavior"
    _DECL = {
    # A Boolean-valued ValueSpecification that will result in a ChangeEvent whenever its value changes
    #  from false to true.
    'changeExpression': _Ref('changeExpression', "ValueSpecification", composite=True, subsets=("ownedElement",), assoc="A_changeExpression_changeEvent"),
    }
    _UNIONS = {
        "ownedElement": ("changeExpression",),
    }

class TemplateParameter(Element):
    """A TemplateParameter exposes a ParameterableElement as a formal parameter of a template."""
    _PKG = "CommonStructure"
    _DECL = {
    # The ParameterableElement that is the default for this formal TemplateParameter.
    'default': _Ref('default', "ParameterableElement", assoc="A_default_templateParameter"),
    # The ParameterableElement that is owned by this TemplateParameter for the purpose of providing a 
    # default.
    'ownedDefault': _Ref('ownedDefault', "ParameterableElement", composite=True, subsets=("ownedElement", "default",), assoc="A_ownedDefault_templateParameter"),
    # The ParameterableElement that is owned by this TemplateParameter for the purpose of exposing it 
    # as the parameteredElement.
    'ownedParameteredElement': _Ref('ownedParameteredElement', "ParameterableElement", composite=True, subsets=("ownedElement", "parameteredElement",), assoc="A_ownedParameteredElement_owningTemplateParameter"),
    # The ParameterableElement exposed by this TemplateParameter.
    'parameteredElement': _Ref('parameteredElement', "ParameterableElement", assoc="A_parameteredElement_templateParameter"),
    # The TemplateSignature that owns this TemplateParameter.
    'signature': _Ref('signature', "TemplateSignature", subsets=("templateSignature", "owner",), assoc="A_ownedParameter_signature"),
    }
    _UNIONS = {
        "ownedElement": ("ownedDefault", "ownedParameteredElement",),
        "owner": ("signature",),
    }
    CONSTRAINTS = (
        ("must_be_compatible",
         "default <> null implies default.isCompatibleWith(parameteredElement)"
        ),
    )

class ClassifierTemplateParameter(TemplateParameter):
    """A ClassifierTemplateParameter exposes a Classifier as a formal template parameter."""
    _PKG = "Classification"
    _DECL = {
    # Constrains the required relationship between an actual parameter and the parameteredElement for 
    # this formal parameter.
    'allowSubstitutable': _Ref('allowSubstitutable', bool),
    # The classifiers that constrain the argument that can be used for the parameter. If the allowSubs
    # titutable attribute is true, then any Classifier that is compatible with this constraining Class
    # ifier can be substituted; otherwise, it must be either this Classifier or one of its specializat
    # ions. If this property is empty, there are no constraints on the Classifier that can be used as 
    # an argument.
    'constrainingClassifier': _Ref('constrainingClassifier', "Classifier", multi=True, lo=0, hi='*', assoc="A_constrainingClassifier_classifierTemplateParameter"),
    # The Classifier exposed by this ClassifierTemplateParameter.
    'parameteredElement': _Ref('parameteredElement', "Classifier", redefines=("parameteredElement",), assoc="A_classifier_templateParameter_parameteredElement"),
    }
    CONSTRAINTS = (
        ("has_constraining_classifier",
         "allowSubstitutable implies constrainingClassifier->notEmpty()"
        ),
        ("parametered_element_no_features",
         "parameteredElement.feature->isEmpty() and (constrainingClassifier->isEmpty() implies par"
         "ameteredElement.allParents()->isEmpty())"
        ),
        ("matching_abstract",
         "(not parameteredElement.isAbstract) implies templateParameterSubstitution.actual->forAll"
         "(a | not a.oclAsType(Classifier).isAbstract)"
        ),
        ("actual_is_classifier",
         "templateParameterSubstitution.actual->forAll(a | a.oclIsKindOf(Classifier))"
        ),
        ("constraining_classifiers_constrain_args",
         "templateParameterSubstitution.actual->forAll( a | let arg : Classifier = a.oclAsType(Cla"
         "ssifier) in constrainingClassifier->forAll( cc | arg = cc or arg.conformsTo(cc) or (allo"
         "wSubstitutable and arg.isSubstitutableFor(cc)) ) )"
        ),
        ("constraining_classifiers_constrain_parametered_element",
         "constrainingClassifier->forAll( cc | parameteredElement = cc or parameteredElement.confo"
         "rmsTo(cc) or (allowSubstitutable and parameteredElement.isSubstitutableFor(cc)) )"
        ),
    )

class Clause(Element):
    """A Clause is an Element that represents a single branch of a ConditionalNode, including a test and a body section. The body section is executed only if (but not necessarily if) the test section evaluates to true."""
    _PKG = "Actions"
    _DECL = {
    # The set of ExecutableNodes that are executed if the test evaluates to true and the Clause is cho
    # sen over other Clauses within the ConditionalNode that also have tests that evaluate to true.
    'body': _Ref('body', "ExecutableNode", multi=True, lo=0, hi='*', assoc="A_body_clause"),
    # The OutputPins on Actions within the body section whose values are moved to the result OutputPin
    # s of the containing ConditionalNode after execution of the body.
    'bodyOutput': _Ref('bodyOutput', "OutputPin", multi=True, lo=0, hi='*', assoc="A_bodyOutput_clause"),
    # An OutputPin on an Action in the test section whose Boolean value determines the result of the t
    # est.
    'decider': _Ref('decider', "OutputPin", assoc="A_decider_clause"),
    # A set of Clauses whose tests must all evaluate to false before this Clause can evaluate its test
    # .
    'predecessorClause': _Ref('predecessorClause', "Clause", multi=True, lo=0, hi='*', assoc="A_predecessorClause_successorClause"),
    # A set of Clauses that may not evaluate their tests unless the test for this Clause evaluates to 
    # false.
    'successorClause': _Ref('successorClause', "Clause", multi=True, lo=0, hi='*', assoc="A_predecessorClause_successorClause"),
    # The set of ExecutableNodes that are executed in order to provide a test result for the Clause.
    'test': _Ref('test', "ExecutableNode", multi=True, lo=0, hi='*', assoc="A_test_clause"),
    }
    CONSTRAINTS = (
        ("body_output_pins",
         "_'body'.oclAsType(Action).allActions().output->includesAll(bodyOutput)"
        ),
        ("decider_output",
         "test.oclAsType(Action).allActions().output->includes(decider) and decider.type = Boolean"
         " and decider.is(1,1)"
        ),
        ("test_and_body",
         "test->intersection(_'body')->isEmpty()"
        ),
    )

class ClearAssociationAction(Action):
    """A ClearAssociationAction is an Action that destroys all links of an Association in which a particular object participates."""
    _PKG = "Actions"
    _DECL = {
    # The Association to be cleared.
    'association': _Ref('association', "Association", assoc="A_association_clearAssociationAction"),
    # The InputPin that gives the object whose participation in the Association is to be cleared.
    'object': _Ref('object', "InputPin", composite=True, subsets=("input",), assoc="A_object_clearAssociationAction"),
    }
    _UNIONS = {
        "input": ("object",),
        "ownedElement": ("object",),
    }
    CONSTRAINTS = (
        ("multiplicity",
         "object.is(1,1)"
        ),
        ("same_type",
         "association.memberEnd->exists(self.object.type.conformsTo(type))"
        ),
    )

class ClearStructuralFeatureAction(StructuralFeatureAction):
    """A ClearStructuralFeatureAction is a StructuralFeatureAction that removes all values of a StructuralFeature."""
    _PKG = "Actions"
    _DECL = {
    # The OutputPin on which is put the input object as modified by the ClearStructuralFeatureAction.
    'result': _Ref('result', "OutputPin", composite=True, subsets=("output",), assoc="A_result_clearStructuralFeatureAction"),
    }
    _UNIONS = {
        "output": ("result",),
        "ownedElement": ("result",),
    }
    CONSTRAINTS = (
        ("type_of_result",
         "result<>null implies result.type = object.type"
        ),
        ("multiplicity_of_result",
         "result<>null implies result.is(1,1)"
        ),
    )

class ClearVariableAction(VariableAction):
    """A ClearVariableAction is a VariableAction that removes all values of a Variable."""
    _PKG = "Actions"

class Collaboration(StructuredClassifier, BehavioredClassifier):
    """A Collaboration describes a structure of collaborating elements (roles), each performing a specialized function, which collectively accomplish some desired functionality."""
    _PKG = "StructuredClassifiers"
    _DECL = {
    # Represents the participants in the Collaboration.
    'collaborationRole': _Ref('collaborationRole', "ConnectableElement", multi=True, lo=0, hi='*', subsets=("role",), assoc="A_collaborationRole_collaboration"),
    }
    _UNIONS = {
        "member": ("collaborationRole",),
        "role": ("collaborationRole",),
    }

class CollaborationUse(NamedElement):
    """A CollaborationUse is used to specify the application of a pattern specified by a Collaboration to a specific situation."""
    _PKG = "StructuredClassifiers"
    _DECL = {
    # A mapping between features of the Collaboration and features of the owning Classifier. This mapp
    # ing indicates which ConnectableElement of the Classifier plays which role(s) in the Collaboratio
    # n. A ConnectableElement may be bound to multiple roles in the same CollaborationUse (that is, it
    #  may play multiple roles).
    'roleBinding': _Ref('roleBinding', "Dependency", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_roleBinding_collaborationUse"),
    # The Collaboration which is used in this CollaborationUse. The Collaboration defines the cooperat
    # ion between its roles which are mapped to ConnectableElements relating to the Classifier owning 
    # the CollaborationUse.
    'type': _Ref('type', "Collaboration", assoc="A_type_collaborationUse"),
    }
    _UNIONS = {
        "ownedElement": ("roleBinding",),
    }
    CONSTRAINTS = (
        ("client_elements",
         "roleBinding->collect(client)->forAll(ne1, ne2 | ne1.oclIsKindOf(ConnectableElement) and "
         "ne2.oclIsKindOf(ConnectableElement) and let ce1 : ConnectableElement = ne1.oclAsType(Con"
         "nectableElement), ce2 : ConnectableElement = ne2.oclAsType(ConnectableElement) in ce1.st"
         "ructuredClassifier = ce2.structuredClassifier) and roleBinding->collect(supplier)->forAl"
         "l(ne1, ne2 | ne1.oclIsKindOf(ConnectableElement) and ne2.oclIsKindOf(ConnectableElement)"
         " and let ce1 : ConnectableElement = ne1.oclAsType(ConnectableElement), ce2 : Connectable"
         "Element = ne2.oclAsType(ConnectableElement) in ce1.collaboration = ce2.collaboration)"
        ),
        ("every_role",
         "type.collaborationRole->forAll(role | roleBinding->exists(rb | rb.supplier->includes(rol"
         "e)))"
        ),
        ("connectors",
         "type.ownedConnector->forAll(connector | let rolesConnectedInCollab : Set(ConnectableElem"
         "ent) = connector.end.role->asSet(), relevantBindings : Set(Dependency) = roleBinding->se"
         "lect(rb | rb.supplier->intersection(rolesConnectedInCollab)->notEmpty()), boundRoles : S"
         "et(ConnectableElement) = relevantBindings->collect(client.oclAsType(ConnectableElement))"
         "->asSet(), contextClassifier : StructuredClassifier = boundRoles->any(true).structuredCl"
         "assifier->any(true) in contextClassifier.ownedConnector->exists( correspondingConnector "
         "| correspondingConnector.end.role->forAll( role | boundRoles->includes(role) ) and (conn"
         "ector.type->notEmpty() and correspondingConnector.type->notEmpty()) implies connector.ty"
         "pe->forAll(conformsTo(correspondingConnector.type)) ) )"
        ),
    )

class CombinedFragment(InteractionFragment):
    """A CombinedFragment defines an expression of InteractionFragments. A CombinedFragment is defined by an interaction operator and corresponding InteractionOperands. Through the use of CombinedFragments the user will be able to describe a number of traces in a compact and concise manner."""
    _PKG = "Interactions"
    _DECL = {
    # Specifies the gates that form the interface between this CombinedFragment and its surroundings
    'cfragmentGate': _Ref('cfragmentGate', "Gate", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_cfragmentGate_combinedFragment"),
    # Specifies the operation which defines the semantics of this combination of InteractionFragments.
    'interactionOperator': _Ref('interactionOperator', InteractionOperatorKind),
    # The set of operands of the combined fragment.
    'operand': _Ref('operand', "InteractionOperand", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_operand_combinedFragment"),
    }
    _UNIONS = {
        "ownedElement": ("cfragmentGate", "operand",),
    }
    CONSTRAINTS = (
        ("break",
         "interactionOperator=InteractionOperatorKind::break implies enclosingInteraction.oclAsTyp"
         "e(InteractionFragment)->asSet()->union( enclosingOperand.oclAsType(InteractionFragment)-"
         ">asSet()).covered->asSet() = self.covered->asSet()"
        ),
        ("consider_and_ignore",
         "((interactionOperator = InteractionOperatorKind::consider) or (interactionOperator = Int"
         "eractionOperatorKind::ignore)) implies oclIsKindOf(ConsiderIgnoreFragment)"
        ),
        ("opt_loop_break_neg",
         "(interactionOperator = InteractionOperatorKind::opt or interactionOperator = Interaction"
         "OperatorKind::loop or interactionOperator = InteractionOperatorKind::break or interactio"
         "nOperator = InteractionOperatorKind::assert or interactionOperator = InteractionOperator"
         "Kind::neg) implies operand->size()=1"
        ),
    )

class Comment(Element):
    """A Comment is a textual annotation that can be attached to a set of Elements."""
    _PKG = "CommonStructure"
    _DECL = {
    # References the Element(s) being commented.
    'annotatedElement': _Ref('annotatedElement', "Element", multi=True, lo=0, hi='*', assoc="A_annotatedElement_comment"),
    # Specifies a string that is the comment.
    'body': _Ref('body', str),
    }

class CommunicationPath(Association):
    """A communication path is an association between two deployment targets, through which they are able to exchange signals and messages."""
    _PKG = "Deployments"
    CONSTRAINTS = (
        ("association_ends",
         "endType->forAll (oclIsKindOf(DeploymentTarget))"
        ),
    )

class Component(Class):
    """A Component represents a modular part of a system that encapsulates its contents and whose manifestation is replaceable within its environment."""
    _PKG = "StructuredClassifiers"
    _DECL = {
    # If true, the Component is defined at design-time, but at run-time (or execution-time) an object 
    # specified by the Component does not exist, that is, the Component is instantiated indirectly, th
    # rough the instantiation of its realizing Classifiers or parts.
    'isIndirectlyInstantiated': _Ref('isIndirectlyInstantiated', bool),
    # The set of PackageableElements that a Component owns. In the namespace of a Component, all model
    #  elements that are involved in or related to its definition may be owned or imported explicitly.
    #  These may include e.g., Classes, Interfaces, Components, Packages, UseCases, Dependencies (e.g.
    # , mappings), and Artifacts.
    'packagedElement': _Ref('packagedElement', "PackageableElement", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_packagedElement_component"),
    # The Interfaces that the Component exposes to its environment. These Interfaces may be Realized b
    # y the Component or any of its realizingClassifiers, or they may be the Interfaces that are provi
    # ded by its public Ports.
    'provided': _Ref('provided', "Interface", derived=True, readonly=True, multi=True, lo=0, hi='*', assoc="A_provided_component"),
    # The set of Realizations owned by the Component. Realizations reference the Classifiers of which 
    # the Component is an abstraction; i.e., that realize its behavior.
    'realization': _Ref('realization', "ComponentRealization", composite=True, multi=True, lo=0, hi='*', subsets=("supplierDependency", "ownedElement",), assoc="A_realization_abstraction_component"),
    # The Interfaces that the Component requires from other Components in its environment in order to 
    # be able to offer its full set of provided functionality. These Interfaces may be used by the Com
    # ponent or any of its realizingClassifiers, or they may be the Interfaces that are required by it
    # s public Ports.
    'required': _Ref('required', "Interface", derived=True, readonly=True, multi=True, lo=0, hi='*', assoc="A_required_component"),
    }
    _UNIONS = {
        "directedRelationship": ("realization",),
        "member": ("packagedElement",),
        "ownedElement": ("packagedElement", "realization",),
        "ownedMember": ("packagedElement",),
        "relationship": ("realization",),
    }
    CONSTRAINTS = (
        ("no_nested_classifiers",
         "nestedClassifier->isEmpty()"
        ),
        ("no_packaged_elements",
         "nestingClass <> null implies packagedElement->isEmpty()"
        ),
    )
    def provided(self) -> "Interface":
        """
        Derivation for Component::/provided
        [Component operation (query); params: none; returns: "Interface"; stub - metamodel metadata on
        ly]
        """
        raise NotImplementedError
    def required(self) -> "Interface":
        """
        Derivation for Component::/required
        [Component operation (query); params: none; returns: "Interface"; stub - metamodel metadata on
        ly]
        """
        raise NotImplementedError

class Realization(Abstraction):
    """Realization is a specialized Abstraction relationship between two sets of model Elements, one representing a specification (the supplier) and the other represents an implementation of the latter (the client). Realization can be used to model stepwise refinement, optimizations, transformations, templates, model synthesis, framework composition, etc."""
    _PKG = "CommonStructure"

class ComponentRealization(Realization):
    """Realization is specialized to (optionally) define the Classifiers that realize the contract offered by a Component in terms of its provided and required Interfaces. The Component forms an abstraction from these various Classifiers."""
    _PKG = "StructuredClassifiers"
    _DECL = {
    # The Component that owns this ComponentRealization and which is implemented by its realizing Clas
    # sifiers.
    'abstraction': _Ref('abstraction', "Component", subsets=("supplier", "owner",), assoc="A_realization_abstraction_component"),
    # The Classifiers that are involved in the implementation of the Component that owns this Realizat
    # ion.
    'realizingClassifier': _Ref('realizingClassifier', "Classifier", multi=True, lo=0, hi='*', subsets=("client",), assoc="A_realizingClassifier_componentRealization"),
    }
    _UNIONS = {
        "owner": ("abstraction",),
        "relatedElement": ("abstraction", "realizingClassifier",),
        "source": ("realizingClassifier",),
        "target": ("abstraction",),
    }

class StructuredActivityNode(Action, Namespace, ActivityGroup):
    """A StructuredActivityNode is an Action that is also an ActivityGroup and whose behavior is specified by the ActivityNodes and ActivityEdges it so contains. Unlike other kinds of ActivityGroup, a StructuredActivityNode owns the ActivityNodes and ActivityEdges it contains, and so a node or edge can only be directly contained in one StructuredActivityNode, though StructuredActivityNodes may be nested."""
    _PKG = "Actions"
    _DECL = {
    # The Activity immediately containing the StructuredActivityNode, if it is not contained in anothe
    # r StructuredActivityNode.
    'activity': _Ref('activity', "Activity", redefines=("inActivity", "activity",), assoc="A_structuredNode_activity"),
    # The ActivityEdges immediately contained in the StructuredActivityNode.
    'edge': _Ref('edge', "ActivityEdge", composite=True, multi=True, lo=0, hi='*', subsets=("containedEdge", "ownedElement",), assoc="A_edge_inStructuredNode"),
    # If true, then any object used by an Action within the StructuredActivityNode cannot be accessed 
    # by any Action outside the node until the StructuredActivityNode as a whole completes. Any concur
    # rent Actions that would result in accessing such objects are required to have their execution de
    # ferred until the completion of the StructuredActivityNode.
    'mustIsolate': _Ref('mustIsolate', bool),
    # The ActivityNodes immediately contained in the StructuredActivityNode.
    'node': _Ref('node', "ActivityNode", composite=True, multi=True, lo=0, hi='*', subsets=("containedNode", "ownedElement",), assoc="A_node_inStructuredNode"),
    # The InputPins owned by the StructuredActivityNode.
    'structuredNodeInput': _Ref('structuredNodeInput', "InputPin", composite=True, multi=True, lo=0, hi='*', subsets=("input",), assoc="A_structuredNodeInput_structuredActivityNode"),
    # The OutputPins owned by the StructuredActivityNode.
    'structuredNodeOutput': _Ref('structuredNodeOutput', "OutputPin", composite=True, multi=True, lo=0, hi='*', subsets=("output",), assoc="A_structuredNodeOutput_structuredActivityNode"),
    # The Variables defined in the scope of the StructuredActivityNode.
    'variable': _Ref('variable', "Variable", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_variable_scope"),
    }
    _UNIONS = {
        "containedEdge": ("edge",),
        "containedNode": ("node",),
        "input": ("structuredNodeInput",),
        "member": ("variable",),
        "output": ("structuredNodeOutput",),
        "ownedElement": ("edge", "node", "structuredNodeInput", "structuredNodeOutput", "variable",),
        "ownedMember": ("variable",),
    }
    CONSTRAINTS = (
        ("output_pin_edges",
         "output.outgoing.target->excludesAll(allOwnedNodes()-input)"
        ),
        ("edges",
         "edge=self.sourceNodes().outgoing->intersection(self.allOwnedNodes().incoming)-> union(se"
         "lf.targetNodes().incoming->intersection(self.allOwnedNodes().outgoing))->asSet()"
        ),
        ("input_pin_edges",
         "input.incoming.source->excludesAll(allOwnedNodes()-output)"
        ),
    )
    def allActions(self) -> "Action":
        """
        Returns this StructuredActivityNode and all Actions contained in it.
        [StructuredActivityNode operation (query); params: none; returns: "Action"; stub - metamodel m
        etadata only]
        """
        raise NotImplementedError
    def allOwnedNodes(self) -> "ActivityNode":
        """
        Returns all the ActivityNodes contained directly or indirectly within this StructuredActivityN
        ode, in addition to the Pins of the StructuredActivityNode.
        [StructuredActivityNode operation (query); params: none; returns: "ActivityNode"; stub - metam
        odel metadata only]
        """
        raise NotImplementedError
    def sourceNodes(self) -> "ActivityNode":
        """
        Return those ActivityNodes contained immediately within the StructuredActivityNode that may ac
        t as sources of edges owned by the StructuredActivityNode.
        [StructuredActivityNode operation (query); params: none; returns: "ActivityNode"; stub - metam
        odel metadata only]
        """
        raise NotImplementedError
    def targetNodes(self) -> "ActivityNode":
        """
        Return those ActivityNodes contained immediately within the StructuredActivityNode that may ac
        t as targets of edges owned by the StructuredActivityNode.
        [StructuredActivityNode operation (query); params: none; returns: "ActivityNode"; stub - metam
        odel metadata only]
        """
        raise NotImplementedError
    def containingActivity(self) -> "Activity":
        """
        The Activity that directly or indirectly contains this StructuredActivityNode (considered as a
        n Action).
        [StructuredActivityNode operation (query); params: none; returns: "Activity"; stub - metamodel
         metadata only]
        """
        raise NotImplementedError

class ConditionalNode(StructuredActivityNode):
    """A ConditionalNode is a StructuredActivityNode that chooses one among some number of alternative collections of ExecutableNodes to execute."""
    _PKG = "Actions"
    _DECL = {
    # The set of Clauses composing the ConditionalNode.
    'clause': _Ref('clause', "Clause", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_clause_conditionalNode"),
    # If true, the modeler asserts that the test for at least one Clause of the ConditionalNode will s
    # ucceed.
    'isAssured': _Ref('isAssured', bool),
    # If true, the modeler asserts that the test for at most one Clause of the ConditionalNode will su
    # cceed.
    'isDeterminate': _Ref('isDeterminate', bool),
    # The OutputPins that onto which are moved values from the bodyOutputs of the Clause selected for 
    # execution.
    'result': _Ref('result', "OutputPin", composite=True, multi=True, lo=0, hi='*', redefines=("structuredNodeOutput",), assoc="A_result_conditionalNode"),
    }
    _UNIONS = {
        "ownedElement": ("clause",),
    }
    CONSTRAINTS = (
        ("result_no_incoming",
         "result.incoming->isEmpty()"
        ),
        ("no_input_pins",
         "input->isEmpty()"
        ),
        ("one_clause_with_executable_node",
         "node->select(oclIsKindOf(ExecutableNode)).oclAsType(ExecutableNode)->forAll(n | self.cla"
         "use->select(test->union(_'body')->includes(n))->size()=1)"
        ),
        ("matching_output_pins",
         "clause->forAll( bodyOutput->size()=self.result->size() and Sequence{1..self.result->size"
         "()}->forAll(i | bodyOutput->at(i).type.conformsTo(result->at(i).type) and bodyOutput->at"
         "(i).isOrdered = result->at(i).isOrdered and bodyOutput->at(i).isUnique = result->at(i).i"
         "sUnique and bodyOutput->at(i).compatibleWith(result->at(i))))"
        ),
        ("executable_nodes",
         "clause.test->union(clause._'body') = node->select(oclIsKindOf(ExecutableNode)).oclAsType"
         "(ExecutableNode)"
        ),
        ("clause_no_predecessor",
         "clause->closure(predecessorClause)->intersection(clause)->isEmpty()"
        ),
    )
    def allActions(self) -> "Action":
        """
        Return only this ConditionalNode. This prevents Actions within the ConditionalNode from having
         their OutputPins used as bodyOutputs or decider Pins in containing LoopNodes or ConditionalNo
        des.
        [ConditionalNode operation (query); params: none; returns: "Action"; stub - metamodel metadata
         only]
        """
        raise NotImplementedError

class ConnectableElement(TypedElement, ParameterableElement):
    """ConnectableElement is an abstract metaclass representing a set of instances that play roles of a StructuredClassifier. ConnectableElements may be joined by attached Connectors and specify configurations of linked instances to be created within an instance of the containing StructuredClassifier."""
    _PKG = "StructuredClassifiers"
    _DECL = {
    # A set of ConnectorEnds that attach to this ConnectableElement.
    'end': _Ref('end', "ConnectorEnd", derived=True, readonly=True, multi=True, lo=0, hi='*', assoc="A_end_role"),
    # The ConnectableElementTemplateParameter for this ConnectableElement parameter.
    'templateParameter': _Ref('templateParameter', "ConnectableElementTemplateParameter", redefines=("templateParameter",), assoc="A_connectableElement_templateParameter_parameteredElement"),
    }
    def end(self) -> "ConnectorEnd":
        """
        Derivation for ConnectableElement::/end : ConnectorEnd
        [ConnectableElement operation (query); params: none; returns: "ConnectorEnd"; stub - metamodel
         metadata only]
        """
        raise NotImplementedError

class ConnectableElementTemplateParameter(TemplateParameter):
    """A ConnectableElementTemplateParameter exposes a ConnectableElement as a formal parameter for a template."""
    _PKG = "StructuredClassifiers"
    _DECL = {
    # The ConnectableElement for this ConnectableElementTemplateParameter.
    'parameteredElement': _Ref('parameteredElement', "ConnectableElement", redefines=("parameteredElement",), assoc="A_connectableElement_templateParameter_parameteredElement"),
    }

class Vertex(RedefinableElement, NamedElement):
    """A Vertex is an abstraction of a node in a StateMachine graph. It can be the source or destination of any number of Transitions."""
    _PKG = "StateMachines"
    _DECL = {
    # The Region that contains this Vertex.
    'container': _Ref('container', "Region", subsets=("namespace",), assoc="A_subvertex_container"),
    # Specifies the Transitions entering this Vertex.
    'incoming': _Ref('incoming', "Transition", derived=True, readonly=True, multi=True, lo=0, hi='*', assoc="A_incoming_target_vertex"),
    # Specifies the Transitions departing from this Vertex.
    'outgoing': _Ref('outgoing', "Transition", derived=True, readonly=True, multi=True, lo=0, hi='*', assoc="A_outgoing_source_vertex"),
    # The Vertex of which this Vertex is a redefinition.
    'redefinedVertex': _Ref('redefinedVertex', "Vertex", subsets=("redefinedElement",), assoc="A_redefinedState_state"),
    # References the Classifier in which context this element may be redefined.
    'redefinitionContext': _Ref('redefinitionContext', "Classifier", derived=True, readonly=True, redefines=("redefinitionContext",), assoc="A_redefinitionContext_state"),
    }
    _UNIONS = {
        "memberNamespace": ("container",),
        "namespace": ("container",),
        "owner": ("container",),
        "redefinedElement": ("redefinedVertex",),
    }
    def containingStateMachine(self) -> "StateMachine":
        """
        The operation containingStateMachine() returns the StateMachine in which this Vertex is define
        d.
        [Vertex operation (query); params: none; returns: "StateMachine"; stub - metamodel metadata on
        ly]
        """
        raise NotImplementedError
    def incoming(self) -> "Transition":
        """
        Derivation for Vertex::/incoming.
        [Vertex operation (query); params: none; returns: "Transition"; stub - metamodel metadata only
        ]
        """
        raise NotImplementedError
    def outgoing(self) -> "Transition":
        """
        Derivation for Vertex::/outgoing
        [Vertex operation (query); params: none; returns: "Transition"; stub - metamodel metadata only
        ]
        """
        raise NotImplementedError
    def isContainedInState(self, s: "State" = None) -> bool:
        """
        This utility operation returns true if the Vertex is contained in the State s (input argument)
        .
        [Vertex operation (query); params: s: "State"; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isContainedInRegion(self, r: "Region" = None) -> bool:
        """
        This utility query returns true if the Vertex is contained in the Region r (input argument).
        [Vertex operation (query); params: r: "Region"; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def redefinitionContext(self) -> "Classifier":
        """
        The redefinition context of a Vertex is the nearest containing StateMachine.
        [Vertex operation (query); params: none; returns: "Classifier"; stub - metamodel metadata only
        ]
        """
        raise NotImplementedError
    def isConsistentWith(self, redefiningElement: "RedefinableElement" = None) -> bool:
        """
        The query isRedefinitionContextValid specifies that the redefinition context of a redefining V
        ertex is properly related to the redefinition context of the redefined Vertex if the owner of 
        the redefining Vertex is a redefinition of the owner of the redefined Vertex. Note that the ow
        ner of a Vertex may be a Region, a StateMachine (for a connectionPoint Pseudostate), or a Stat
        e (for a connectionPoint Pseudostate or a connection ConnectionPointReference), all of which a
        re RedefinableElements.
        [Vertex operation (query); params: redefiningElement: "RedefinableElement"; returns: bool; stu
        b - metamodel metadata only]
        """
        raise NotImplementedError

class ConnectionPointReference(Vertex):
    """A ConnectionPointReference represents a usage (as part of a submachine State) of an entry/exit point Pseudostate defined in the StateMachine referenced by the submachine State."""
    _PKG = "StateMachines"
    _DECL = {
    # The entryPoint Pseudostates corresponding to this connection point.
    'entry': _Ref('entry', "Pseudostate", multi=True, lo=0, hi='*', assoc="A_entry_connectionPointReference"),
    # The exitPoints kind Pseudostates corresponding to this connection point.
    'exit': _Ref('exit', "Pseudostate", multi=True, lo=0, hi='*', assoc="A_exit_connectionPointReference"),
    # The State in which the ConnectionPointReference is defined.
    'state': _Ref('state', "State", subsets=("namespace",), assoc="A_connection_state"),
    }
    _UNIONS = {
        "memberNamespace": ("state",),
        "namespace": ("state",),
        "owner": ("state",),
    }
    CONSTRAINTS = (
        ("exit_pseudostates",
         "exit->forAll(kind = PseudostateKind::exitPoint)"
        ),
        ("entry_pseudostates",
         "entry->forAll(kind = PseudostateKind::entryPoint)"
        ),
    )
    def isConsistentWith(self, redefiningElement: "RedefinableElement" = None) -> bool:
        """
        The query isConsistentWith() specifies a ConnectionPointReference can only be redefined by a C
        onnectionPointReference.
        [ConnectionPointReference operation; params: redefiningElement: "RedefinableElement"; returns:
         bool; stub - metamodel metadata only]
        """
        raise NotImplementedError

class Connector(Feature):
    """A Connector specifies links that enables communication between two or more instances. In contrast to Associations, which specify links between any instance of the associated Classifiers, Connectors specify links between instances playing the connected parts only."""
    _PKG = "StructuredClassifiers"
    _DECL = {
    # The set of Behaviors that specify the valid interaction patterns across the Connector.
    'contract': _Ref('contract', "Behavior", multi=True, lo=0, hi='*', assoc="A_contract_connector"),
    # A Connector has at least two ConnectorEnds, each representing the participation of instances of 
    # the Classifiers typing the ConnectableElements attached to the end. The set of ConnectorEnds is 
    # ordered.
    'end': _Ref('end', "ConnectorEnd", composite=True, multi=True, lo=2, hi='*', subsets=("ownedElement",), assoc="A_end_connector"),
    # Indicates the kind of Connector. This is derived: a Connector with one or more ends connected to
    #  a Port which is not on a Part and which is not a behavior port is a delegation; otherwise it is
    #  an assembly.
    'kind': _Ref('kind', ConnectorKind, derived=True, readonly=True),
    # A Connector may be redefined when its containing Classifier is specialized. The redefining Conne
    # ctor may have a type that specializes the type of the redefined Connector. The types of the Conn
    # ectorEnds of the redefining Connector may specialize the types of the ConnectorEnds of the redef
    # ined Connector. The properties of the ConnectorEnds of the redefining Connector may be replaced.
    'redefinedConnector': _Ref('redefinedConnector', "Connector", multi=True, lo=0, hi='*', subsets=("redefinedElement",), assoc="A_redefinedConnector_connector"),
    # An optional Association that classifies links corresponding to this Connector.
    'type': _Ref('type', "Association", assoc="A_type_connector"),
    }
    _UNIONS = {
        "ownedElement": ("end",),
        "redefinedElement": ("redefinedConnector",),
    }
    CONSTRAINTS = (
        ("types",
         "type<>null implies let noOfEnds : Integer = end->size() in (type.memberEnd->size() = noO"
         "fEnds) and Sequence{1..noOfEnds}->forAll(i | end->at(i).role.type.conformsTo(type.member"
         "End->at(i).type))"
        ),
        ("roles",
         "structuredClassifier <> null and end->forAll( e | structuredClassifier.allRoles()->inclu"
         "des(e.role) or e.role.oclIsKindOf(Port) and structuredClassifier.allRoles()->includes(e."
         "partWithPort))"
        ),
    )
    def kind(self) -> ConnectorKind:
        """
        Derivation for Connector::/kind : ConnectorKind
        [Connector operation (query); params: none; returns: ConnectorKind; stub - metamodel metadata 
        only]
        """
        raise NotImplementedError

class ConnectorEnd(MultiplicityElement):
    """A ConnectorEnd is an endpoint of a Connector, which attaches the Connector to a ConnectableElement."""
    _PKG = "StructuredClassifiers"
    _DECL = {
    # A derived property referencing the corresponding end on the Association which types the Connecto
    # r owing this ConnectorEnd, if any. It is derived by selecting the end at the same place in the o
    # rdering of Association ends as this ConnectorEnd.
    'definingEnd': _Ref('definingEnd', "Property", derived=True, readonly=True, assoc="A_definingEnd_connectorEnd"),
    # Indicates the role of the internal structure of a Classifier with the Port to which the Connecto
    # rEnd is attached.
    'partWithPort': _Ref('partWithPort', "Property", assoc="A_partWithPort_connectorEnd"),
    # The ConnectableElement attached at this ConnectorEnd. When an instance of the containing Classif
    # ier is created, a link may (depending on the multiplicities) be created to an instance of the Cl
    # assifier that types this ConnectableElement.
    'role': _Ref('role', "ConnectableElement", assoc="A_end_role"),
    }
    CONSTRAINTS = (
        ("role_and_part_with_port",
         "partWithPort->notEmpty() implies (role.oclIsKindOf(Port) and partWithPort.type.oclAsType"
         "(Namespace).member->includes(role))"
        ),
        ("part_with_port_empty",
         "(role.oclIsKindOf(Port) and role.owner = connector.owner) implies partWithPort->isEmpty("
         ")"
        ),
        ("multiplicity",
         "self.compatibleWith(definingEnd)"
        ),
        ("self_part_with_port",
         "partWithPort->notEmpty() implies not partWithPort.oclIsKindOf(Port)"
        ),
    )
    def definingEnd(self) -> "Property":
        """
        Derivation for ConnectorEnd::/definingEnd : Property
        [ConnectorEnd operation (query); params: none; returns: "Property"; stub - metamodel metadata 
        only]
        """
        raise NotImplementedError

class ConsiderIgnoreFragment(CombinedFragment):
    """A ConsiderIgnoreFragment is a kind of CombinedFragment that is used for the consider and ignore cases, which require lists of pertinent Messages to be specified."""
    _PKG = "Interactions"
    _DECL = {
    # The set of messages that apply to this fragment.
    'message': _Ref('message', "NamedElement", multi=True, lo=0, hi='*', assoc="A_message_considerIgnoreFragment"),
    }
    CONSTRAINTS = (
        ("consider_or_ignore",
         "(interactionOperator = InteractionOperatorKind::consider) or (interactionOperator = Inte"
         "ractionOperatorKind::ignore)"
        ),
        ("type",
         "message->forAll(m | m.oclIsKindOf(Operation) or m.oclIsKindOf(Signal))"
        ),
    )

class Constraint(PackageableElement):
    """A Constraint is a condition or restriction expressed in natural language text or in a machine readable language for the purpose of declaring some of the semantics of an Element or set of Elements."""
    _PKG = "CommonStructure"
    _DECL = {
    # The ordered set of Elements referenced by this Constraint.
    'constrainedElement': _Ref('constrainedElement', "Element", multi=True, lo=0, hi='*', assoc="A_constrainedElement_constraint"),
    # Specifies the Namespace that owns the Constraint.
    'context': _Ref('context', "Namespace", subsets=("namespace",), assoc="A_ownedRule_context"),
    # A condition that must be true when evaluated in order for the Constraint to be satisfied.
    'specification': _Ref('specification', "ValueSpecification", composite=True, subsets=("ownedElement",), assoc="A_specification_owningConstraint"),
    }
    _UNIONS = {
        "memberNamespace": ("context",),
        "namespace": ("context",),
        "ownedElement": ("specification",),
        "owner": ("context",),
    }
    CONSTRAINTS = (
        ("boolean_value",
         "(no specification serialized)"
        ),
        ("no_side_effects",
         "(no specification serialized)"
        ),
        ("not_apply_to_self",
         "not constrainedElement->includes(self)"
        ),
    )

class Continuation(InteractionFragment):
    """A Continuation is a syntactic way to define continuations of different branches of an alternative CombinedFragment. Continuations are intuitively similar to labels representing intermediate points in a flow of control."""
    _PKG = "Interactions"
    _DECL = {
    # True: when the Continuation is at the end of the enclosing InteractionFragment and False when it
    #  is in the beginning.
    'setting': _Ref('setting', bool),
    }
    CONSTRAINTS = (
        ("first_or_last_interaction_fragment",
         "enclosingOperand->notEmpty() and let peerFragments : OrderedSet(InteractionFragment) = e"
         "nclosingOperand.fragment in ( peerFragments->notEmpty() and ((peerFragments->first() = s"
         "elf) or (peerFragments->last() = self)))"
        ),
        ("same_name",
         "enclosingOperand.combinedFragment->notEmpty() and let parentInteraction : Set(Interactio"
         "n) = enclosingOperand.combinedFragment->closure(enclosingOperand.combinedFragment)-> col"
         "lect(enclosingInteraction).oclAsType(Interaction)->asSet() in (parentInteraction->size()"
         " = 1) and let peerInteractions : Set(Interaction) = (parentInteraction->union(parentInte"
         "raction->collect(_'context')->collect(behavior)-> select(oclIsKindOf(Interaction)).oclAs"
         "Type(Interaction)->asSet())->asSet()) in (peerInteractions->notEmpty()) and let combined"
         "Fragments1 : Set(CombinedFragment) = peerInteractions.fragment-> select(oclIsKindOf(Comb"
         "inedFragment)).oclAsType(CombinedFragment)->asSet() in combinedFragments1->notEmpty() an"
         "d combinedFragments1->closure(operand.fragment-> select(oclIsKindOf(CombinedFragment)).o"
         "clAsType(CombinedFragment))->asSet().operand.fragment-> select(oclIsKindOf(Continuation)"
         ").oclAsType(Continuation)->asSet()-> forAll(c : Continuation | (c.name = self.name) impl"
         "ies (c.covered->asSet()->forAll(cl : Lifeline | -- cl must be common to one lifeline cov"
         "ered by self self.covered->asSet()-> select(represents = cl.represents and selector = cl"
         ".selector)->asSet()->size()=1)) and (self.covered->asSet()->forAll(cl : Lifeline | -- cl"
         " must be common to one lifeline covered by c c.covered->asSet()-> select(represents = cl"
         ".represents and selector = cl.selector)->asSet()->size()=1)) )"
        ),
        ("global",
         "enclosingOperand->notEmpty() and let operandLifelines : Set(Lifeline) = enclosingOperand"
         ".covered in (operandLifelines->notEmpty() and operandLifelines->forAll(ol :Lifeline |sel"
         "f.covered->includes(ol)))"
        ),
    )

class ControlFlow(ActivityEdge):
    """A ControlFlow is an ActivityEdge traversed by control tokens or object tokens of control type, which are use to control the execution of ExecutableNodes."""
    _PKG = "Activities"
    CONSTRAINTS = (
        ("object_nodes",
         "(source.oclIsKindOf(ObjectNode) implies source.oclAsType(ObjectNode).isControlType) and "
         "(target.oclIsKindOf(ObjectNode) implies target.oclAsType(ObjectNode).isControlType)"
        ),
    )

class LinkAction(Action):
    """LinkAction is an abstract class for all Actions that identify the links to be acted on using LinkEndData."""
    _PKG = "Actions"
    _DECL = {
    # The LinkEndData identifying the values on the ends of the links acting on by this LinkAction.
    'endData': _Ref('endData', "LinkEndData", composite=True, multi=True, lo=2, hi='*', subsets=("ownedElement",), assoc="A_endData_linkAction"),
    # InputPins used by the LinkEndData of the LinkAction.
    'inputValue': _Ref('inputValue', "InputPin", composite=True, multi=True, lo=0, hi='*', subsets=("input",), assoc="A_inputValue_linkAction"),
    }
    _UNIONS = {
        "input": ("inputValue",),
        "ownedElement": ("endData", "inputValue",),
    }
    CONSTRAINTS = (
        ("same_pins",
         "inputValue->asBag()=endData.allPins()"
        ),
        ("same_association",
         "endData.end = self.association().memberEnd->asBag()"
        ),
        ("not_static",
         "endData->forAll(not end.isStatic)"
        ),
    )
    def association(self) -> "Association":
        """
        Returns the Association acted on by this LinkAction.
        [LinkAction operation (query); params: none; returns: "Association"; stub - metamodel metadata
         only]
        """
        raise NotImplementedError

class WriteLinkAction(LinkAction):
    """WriteLinkAction is an abstract class for LinkActions that create and destroy links."""
    _PKG = "Actions"
    CONSTRAINTS = (
        ("allow_access",
         "endData.end->exists(end | end.type=_'context' or end.visibility=VisibilityKind::public o"
         "r end.visibility=VisibilityKind::protected and endData.end->exists(other | other<>end an"
         "d _'context'.conformsTo(other.type.oclAsType(Classifier))))"
        ),
    )

class CreateLinkAction(WriteLinkAction):
    """A CreateLinkAction is a WriteLinkAction for creating links."""
    _PKG = "Actions"
    _DECL = {
    # The LinkEndData that specifies the values to be placed on the Association ends for the new link.
    'endData': _Ref('endData', "LinkEndCreationData", composite=True, multi=True, lo=2, hi='*', redefines=("endData",), assoc="A_endData_createLinkAction"),
    }
    CONSTRAINTS = (
        ("association_not_abstract",
         "not self.association().isAbstract"
        ),
    )

class CreateLinkObjectAction(CreateLinkAction):
    """A CreateLinkObjectAction is a CreateLinkAction for creating link objects (AssociationClasse instances)."""
    _PKG = "Actions"
    _DECL = {
    # The output pin on which the newly created link object is placed.
    'result': _Ref('result', "OutputPin", composite=True, subsets=("output",), assoc="A_result_createLinkObjectAction"),
    }
    _UNIONS = {
        "output": ("result",),
        "ownedElement": ("result",),
    }
    CONSTRAINTS = (
        ("multiplicity",
         "result.is(1,1)"
        ),
        ("type_of_result",
         "result.type = association()"
        ),
        ("association_class",
         "self.association().oclIsKindOf(AssociationClass)"
        ),
    )

class CreateObjectAction(Action):
    """A CreateObjectAction is an Action that creates an instance of the specified Classifier."""
    _PKG = "Actions"
    _DECL = {
    # The Classifier to be instantiated.
    'classifier': _Ref('classifier', "Classifier", assoc="A_classifier_createObjectAction"),
    # The OutputPin on which the newly created object is placed.
    'result': _Ref('result', "OutputPin", composite=True, subsets=("output",), assoc="A_result_createObjectAction"),
    }
    _UNIONS = {
        "output": ("result",),
        "ownedElement": ("result",),
    }
    CONSTRAINTS = (
        ("classifier_not_abstract",
         "not classifier.isAbstract"
        ),
        ("multiplicity",
         "result.is(1,1)"
        ),
        ("classifier_not_association_class",
         "not classifier.oclIsKindOf(AssociationClass)"
        ),
        ("same_type",
         "result.type = classifier"
        ),
    )

class DataStoreNode(CentralBufferNode):
    """A DataStoreNode is a CentralBufferNode for persistent data."""
    _PKG = "Activities"

class DataType(Classifier):
    """A DataType is a type whose instances are identified only by their value."""
    _PKG = "SimpleClassifiers"
    _DECL = {
    # The attributes owned by the DataType.
    'ownedAttribute': _Ref('ownedAttribute', "Property", composite=True, multi=True, lo=0, hi='*', subsets=("attribute", "ownedMember",), assoc="A_ownedAttribute_datatype"),
    # The Operations owned by the DataType.
    'ownedOperation': _Ref('ownedOperation', "Operation", composite=True, multi=True, lo=0, hi='*', subsets=("redefinableElement", "feature", "ownedMember",), assoc="A_ownedOperation_datatype"),
    }
    _UNIONS = {
        "attribute": ("ownedAttribute",),
        "feature": ("ownedAttribute", "ownedOperation",),
        "member": ("ownedAttribute", "ownedOperation",),
        "ownedElement": ("ownedAttribute", "ownedOperation",),
        "ownedMember": ("ownedAttribute", "ownedOperation",),
        "redefinableElement": ("ownedAttribute", "ownedOperation",),
    }

class DecisionNode(ControlNode):
    """A DecisionNode is a ControlNode that chooses between outgoing ActivityEdges for the routing of tokens."""
    _PKG = "Activities"
    _DECL = {
    # A Behavior that is executed to provide an input to guard ValueSpecifications on ActivityEdges ou
    # tgoing from the DecisionNode.
    'decisionInput': _Ref('decisionInput', "Behavior", assoc="A_decisionInput_decisionNode"),
    # An additional ActivityEdge incoming to the DecisionNode that provides a decision input value for
    #  the guards ValueSpecifications on ActivityEdges outgoing from the DecisionNode.
    'decisionInputFlow': _Ref('decisionInputFlow', "ObjectFlow", assoc="A_decisionInputFlow_decisionNode"),
    }
    CONSTRAINTS = (
        ("zero_input_parameters",
         "(decisionInput<>null and decisionInputFlow=null and incoming->exists(oclIsKindOf(Control"
         "Flow))) implies decisionInput.inputParameters()->isEmpty()"
        ),
        ("edges",
         "let allEdges: Set(ActivityEdge) = incoming->union(outgoing) in let allRelevantEdges: Set"
         "(ActivityEdge) = if decisionInputFlow->notEmpty() then allEdges->excluding(decisionInput"
         "Flow) else allEdges endif in allRelevantEdges->forAll(oclIsKindOf(ControlFlow)) or allRe"
         "levantEdges->forAll(oclIsKindOf(ObjectFlow))"
        ),
        ("decision_input_flow_incoming",
         "incoming->includes(decisionInputFlow)"
        ),
        ("two_input_parameters",
         "(decisionInput<>null and decisionInputFlow<>null and incoming->forAll(oclIsKindOf(Object"
         "Flow))) implies decisionInput.inputParameters()->size()=2"
        ),
        ("incoming_outgoing_edges",
         "(incoming->size() = 1 or incoming->size() = 2) and outgoing->size() > 0"
        ),
        ("incoming_control_one_input_parameter",
         "(decisionInput<>null and decisionInputFlow<>null and incoming->exists(oclIsKindOf(Contro"
         "lFlow))) implies decisionInput.inputParameters()->size()=1"
        ),
        ("parameters",
         "decisionInput<>null implies (decisionInput.ownedParameter->forAll(par | par.direction <>"
         " ParameterDirectionKind::out and par.direction <> ParameterDirectionKind::inout ) and de"
         "cisionInput.ownedParameter->one(par | par.direction <> ParameterDirectionKind::return))"
        ),
        ("incoming_object_one_input_parameter",
         "(decisionInput<>null and decisionInputFlow=null and incoming->forAll(oclIsKindOf(ObjectF"
         "low))) implies decisionInput.inputParameters()->size()=1"
        ),
    )

class Deployment(Dependency):
    """A deployment is the allocation of an artifact or artifact instance to a deployment target. A component deployment is the deployment of one or more artifacts or artifact instances to a deployment target, optionally parameterized by a deployment specification. Examples are executables and configuration files."""
    _PKG = "Deployments"
    _DECL = {
    # The specification of properties that parameterize the deployment and execution of one or more Ar
    # tifacts.
    'configuration': _Ref('configuration', "DeploymentSpecification", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_configuration_deployment"),
    # The Artifacts that are deployed onto a Node. This association specializes the supplier associati
    # on.
    'deployedArtifact': _Ref('deployedArtifact', "DeployedArtifact", multi=True, lo=0, hi='*', subsets=("supplier",), assoc="A_deployedArtifact_deploymentForArtifact"),
    # The DeployedTarget which is the target of a Deployment.
    'location': _Ref('location', "DeploymentTarget", subsets=("client", "owner",), assoc="A_deployment_location"),
    }
    _UNIONS = {
        "ownedElement": ("configuration",),
        "owner": ("location",),
        "relatedElement": ("deployedArtifact", "location",),
        "source": ("location",),
        "target": ("deployedArtifact",),
    }

class DeploymentSpecification(Artifact):
    """A deployment specification specifies a set of properties that determine execution parameters of a component artifact that is deployed on a node. A deployment specification can be aimed at a specific type of container. An artifact that reifies or implements deployment specification properties is a deployment descriptor."""
    _PKG = "Deployments"
    _DECL = {
    # The deployment with which the DeploymentSpecification is associated.
    'deployment': _Ref('deployment', "Deployment", subsets=("owner",), assoc="A_configuration_deployment"),
    # The location where an Artifact is deployed onto a Node. This is typically a 'directory' or 'memo
    # ry address.'
    'deploymentLocation': _Ref('deploymentLocation', str),
    # The location where a component Artifact executes. This may be a local or remote location.
    'executionLocation': _Ref('executionLocation', str),
    }
    _UNIONS = {
        "owner": ("deployment",),
    }
    CONSTRAINTS = (
        ("deployment_target",
         "deployment->forAll (location.oclIsKindOf(ExecutionEnvironment))"
        ),
        ("deployed_elements",
         "deployment->forAll (location.deployedElement->forAll (oclIsKindOf(Component)))"
        ),
    )

class DeploymentTarget(NamedElement):
    """A deployment target is the location for a deployed artifact."""
    _PKG = "Deployments"
    _DECL = {
    # The set of elements that are manifested in an Artifact that is involved in Deployment to a Deplo
    # ymentTarget.
    'deployedElement': _Ref('deployedElement', "PackageableElement", derived=True, readonly=True, multi=True, lo=0, hi='*', assoc="A_deployedElement_deploymentTarget"),
    # The set of Deployments for a DeploymentTarget.
    'deployment': _Ref('deployment', "Deployment", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement", "clientDependency",), assoc="A_deployment_location"),
    }
    _UNIONS = {
        "directedRelationship": ("deployment",),
        "ownedElement": ("deployment",),
        "relationship": ("deployment",),
    }
    def deployedElement(self) -> "PackageableElement":
        """
        Derivation for DeploymentTarget::/deployedElement
        [DeploymentTarget operation (query); params: none; returns: "PackageableElement"; stub - metam
        odel metadata only]
        """
        raise NotImplementedError

class DestroyLinkAction(WriteLinkAction):
    """A DestroyLinkAction is a WriteLinkAction that destroys links (including link objects)."""
    _PKG = "Actions"
    _DECL = {
    # The LinkEndData that the values of the Association ends for the links to be destroyed.
    'endData': _Ref('endData', "LinkEndDestructionData", composite=True, multi=True, lo=2, hi='*', redefines=("endData",), assoc="A_endData_destroyLinkAction"),
    }

class DestroyObjectAction(Action):
    """A DestroyObjectAction is an Action that destroys objects."""
    _PKG = "Actions"
    _DECL = {
    # Specifies whether links in which the object participates are destroyed along with the object.
    'isDestroyLinks': _Ref('isDestroyLinks', bool),
    # Specifies whether objects owned by the object (via composition) are destroyed along with the obj
    # ect.
    'isDestroyOwnedObjects': _Ref('isDestroyOwnedObjects', bool),
    # The InputPin providing the object to be destroyed.
    'target': _Ref('target', "InputPin", composite=True, subsets=("input",), assoc="A_target_destroyObjectAction"),
    }
    _UNIONS = {
        "input": ("target",),
        "ownedElement": ("target",),
    }
    CONSTRAINTS = (
        ("multiplicity",
         "target.is(1,1)"
        ),
        ("no_type",
         "target.type= null"
        ),
    )

class MessageEnd(NamedElement):
    """MessageEnd is an abstract specialization of NamedElement that represents what can occur at the end of a Message."""
    _PKG = "Interactions"
    _DECL = {
    # References a Message.
    'message': _Ref('message', "Message", assoc="A_message_messageEnd"),
    }
    def oppositeEnd(self) -> "MessageEnd":
        """
        This query returns a set including the MessageEnd (if exists) at the opposite end of the Messa
        ge for this MessageEnd.
        [MessageEnd operation (query); params: none; returns: "MessageEnd"; stub - metamodel metadata 
        only]
        """
        raise NotImplementedError
    def isSend(self) -> bool:
        """
        This query returns value true if this MessageEnd is a sendEvent.
        [MessageEnd operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isReceive(self) -> bool:
        """
        This query returns value true if this MessageEnd is a receiveEvent.
        [MessageEnd operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def enclosingFragment(self) -> "InteractionFragment":
        """
        This query returns a set including the enclosing InteractionFragment this MessageEnd is enclos
        ed within.
        [MessageEnd operation (query); params: none; returns: "InteractionFragment"; stub - metamodel 
        metadata only]
        """
        raise NotImplementedError

class OccurrenceSpecification(InteractionFragment):
    """An OccurrenceSpecification is the basic semantic unit of Interactions. The sequences of occurrences specified by them are the meanings of Interactions."""
    _PKG = "Interactions"
    _DECL = {
    # References the Lifeline on which the OccurrenceSpecification appears.
    'covered': _Ref('covered', "Lifeline", redefines=("covered",), assoc="A_covered_events"),
    # References the GeneralOrderings that specify EventOcurrences that must occur after this Occurren
    # ceSpecification.
    'toAfter': _Ref('toAfter', "GeneralOrdering", multi=True, lo=0, hi='*', assoc="A_before_toAfter"),
    # References the GeneralOrderings that specify EventOcurrences that must occur before this Occurre
    # nceSpecification.
    'toBefore': _Ref('toBefore', "GeneralOrdering", multi=True, lo=0, hi='*', assoc="A_toBefore_after"),
    }

class MessageOccurrenceSpecification(OccurrenceSpecification, MessageEnd):
    """A MessageOccurrenceSpecification specifies the occurrence of Message events, such as sending and receiving of Signals or invoking or receiving of Operation calls. A MessageOccurrenceSpecification is a kind of MessageEnd. Messages are generated either by synchronous Operation calls or asynchronous Signal sends. They are received by the execution of corresponding AcceptEventActions."""
    _PKG = "Interactions"

class DestructionOccurrenceSpecification(MessageOccurrenceSpecification):
    """A DestructionOccurenceSpecification models the destruction of an object."""
    _PKG = "Interactions"
    CONSTRAINTS = (
        ("no_occurrence_specifications_below",
         "let o : InteractionOperand = enclosingOperand in o->notEmpty() and let peerEvents : Orde"
         "redSet(OccurrenceSpecification) = covered.events->select(enclosingOperand = o) in peerEv"
         "ents->last() = self"
        ),
    )

class Node(Class, DeploymentTarget):
    """A Node is computational resource upon which artifacts may be deployed for execution. Nodes can be interconnected through communication paths to define network structures."""
    _PKG = "Deployments"
    _DECL = {
    # The Nodes that are defined (nested) within the Node.
    'nestedNode': _Ref('nestedNode', "Node", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_nestedNode_node"),
    }
    _UNIONS = {
        "member": ("nestedNode",),
        "ownedElement": ("nestedNode",),
        "ownedMember": ("nestedNode",),
    }
    CONSTRAINTS = (
        ("internal_structure",
         "part->forAll(oclIsKindOf(Node))"
        ),
    )

class Device(Node):
    """A device is a physical computational resource with processing capability upon which artifacts may be deployed for execution. Devices may be complex (i.e., they may consist of other devices)."""
    _PKG = "Deployments"

class ValueSpecification(TypedElement, PackageableElement):
    """A ValueSpecification is the specification of a (possibly empty) set of values. A ValueSpecification is a ParameterableElement that may be exposed as a formal TemplateParameter and provided as the actual parameter in the binding of a template."""
    _PKG = "Values"
    def booleanValue(self) -> bool:
        """
        The query booleanValue() gives a single Boolean value when one can be computed.
        [ValueSpecification operation (query); params: none; returns: bool; stub - metamodel metadata 
        only]
        """
        raise NotImplementedError
    def integerValue(self) -> int:
        """
        The query integerValue() gives a single Integer value when one can be computed.
        [ValueSpecification operation (query); params: none; returns: int; stub - metamodel metadata o
        nly]
        """
        raise NotImplementedError
    def isCompatibleWith(self, p: "ParameterableElement" = None) -> bool:
        """
        The query isCompatibleWith() determines if this ValueSpecification is compatible with the spec
        ified ParameterableElement. This ValueSpecification is compatible with ParameterableElement p 
        if the kind of this ValueSpecification is the same as or a subtype of the kind of p. Further, 
        if p is a TypedElement, then the type of this ValueSpecification must be conformant with the t
        ype of p.
        [ValueSpecification operation (query); params: p: "ParameterableElement"; returns: bool; stub 
        - metamodel metadata only]
        """
        raise NotImplementedError
    def isComputable(self) -> bool:
        """
        The query isComputable() determines whether a value specification can be computed in a model. 
        This operation cannot be fully defined in OCL. A conforming implementation is expected to deli
        ver true for this operation for all ValueSpecifications that it can compute, and to compute al
        l of those for which the operation is true. A conforming implementation is expected to be able
         to compute at least the value of all LiteralSpecifications.
        [ValueSpecification operation (query); params: none; returns: bool; stub - metamodel metadata 
        only]
        """
        raise NotImplementedError
    def isNull(self) -> bool:
        """
        The query isNull() returns true when it can be computed that the value is null.
        [ValueSpecification operation (query); params: none; returns: bool; stub - metamodel metadata 
        only]
        """
        raise NotImplementedError
    def realValue(self) -> float:
        """
        The query realValue() gives a single Real value when one can be computed.
        [ValueSpecification operation (query); params: none; returns: float; stub - metamodel metadata
         only]
        """
        raise NotImplementedError
    def stringValue(self) -> str:
        """
        The query stringValue() gives a single String value when one can be computed.
        [ValueSpecification operation (query); params: none; returns: str; stub - metamodel metadata o
        nly]
        """
        raise NotImplementedError
    def unlimitedValue(self) -> UnlimitedNatural:
        """
        The query unlimitedValue() gives a single UnlimitedNatural value when one can be computed.
        [ValueSpecification operation (query); params: none; returns: UnlimitedNatural; stub - metamod
        el metadata only]
        """
        raise NotImplementedError

class Duration(ValueSpecification):
    """A Duration is a ValueSpecification that specifies the temporal distance between two time instants."""
    _PKG = "Values"
    _DECL = {
    # A ValueSpecification that evaluates to the value of the Duration.
    'expr': _Ref('expr', "ValueSpecification", composite=True, subsets=("ownedElement",), assoc="A_expr_duration"),
    # Refers to the Observations that are involved in the computation of the Duration value
    'observation': _Ref('observation', "Observation", multi=True, lo=0, hi='*', assoc="A_observation_duration"),
    }
    _UNIONS = {
        "ownedElement": ("expr",),
    }
    CONSTRAINTS = (
        ("no_expr_requires_observation",
         "expr = null implies (observation->size() = 1 and observation->forAll(oclIsKindOf(Duratio"
         "nObservation)))"
        ),
    )

class IntervalConstraint(Constraint):
    """An IntervalConstraint is a Constraint that is specified by an Interval."""
    _PKG = "Values"
    _DECL = {
    # The Interval that specifies the condition of the IntervalConstraint.
    'specification': _Ref('specification', "Interval", composite=True, redefines=("specification",), assoc="A_specification_intervalConstraint"),
    }

class DurationConstraint(IntervalConstraint):
    """A DurationConstraint is a Constraint that refers to a DurationInterval."""
    _PKG = "Values"
    _DECL = {
    # The value of firstEvent[i] is related to constrainedElement[i] (where i is 1 or 2). If firstEven
    # t[i] is true, then the corresponding observation event is the first time instant the execution e
    # nters constrainedElement[i]. If firstEvent[i] is false, then the corresponding observation event
    #  is the last time instant the execution is within constrainedElement[i].
    'firstEvent': _Ref('firstEvent', bool, multi=True, lo=0, hi='2'),
    # The DurationInterval constraining the duration.
    'specification': _Ref('specification', "DurationInterval", composite=True, redefines=("specification",), assoc="A_specification_durationConstraint"),
    }
    CONSTRAINTS = (
        ("first_event_multiplicity",
         "if (constrainedElement->size() = 2) then (firstEvent->size() = 2) else (firstEvent->size"
         "() = 0) endif"
        ),
        ("has_one_or_two_constrainedElements",
         "constrainedElement->size() = 1 or constrainedElement->size()=2"
        ),
    )

class Interval(ValueSpecification):
    """An Interval defines the range between two ValueSpecifications."""
    _PKG = "Values"
    _DECL = {
    # Refers to the ValueSpecification denoting the maximum value of the range.
    'max': _Ref('max', "ValueSpecification", assoc="A_max_interval"),
    # Refers to the ValueSpecification denoting the minimum value of the range.
    'min': _Ref('min', "ValueSpecification", assoc="A_min_interval"),
    }

class DurationInterval(Interval):
    """A DurationInterval defines the range between two Durations."""
    _PKG = "Values"
    _DECL = {
    # Refers to the Duration denoting the maximum value of the range.
    'max': _Ref('max', "Duration", redefines=("max",), assoc="A_max_durationInterval"),
    # Refers to the Duration denoting the minimum value of the range.
    'min': _Ref('min', "Duration", redefines=("min",), assoc="A_min_durationInterval"),
    }

class Observation(PackageableElement):
    """Observation specifies a value determined by observing an event or events that occur relative to other model Elements."""
    _PKG = "Values"

class DurationObservation(Observation):
    """A DurationObservation is a reference to a duration during an execution. It points out the NamedElement(s) in the model to observe and whether the observations are when this NamedElement is entered or when it is exited."""
    _PKG = "Values"
    _DECL = {
    # The DurationObservation is determined as the duration between the entering or exiting of a singl
    # e event Element during execution, or the entering/exiting of one event Element and the entering/
    # exiting of a second.
    'event': _Ref('event', "NamedElement", multi=True, lo=0, hi='2', assoc="A_event_durationObservation"),
    # The value of firstEvent[i] is related to event[i] (where i is 1 or 2). If firstEvent[i] is true,
    #  then the corresponding observation event is the first time instant the execution enters event[i
    # ]. If firstEvent[i] is false, then the corresponding observation event is the time instant the e
    # xecution exits event[i].
    'firstEvent': _Ref('firstEvent', bool, multi=True, lo=0, hi='2'),
    }
    CONSTRAINTS = (
        ("first_event_multiplicity",
         "if (event->size() = 2) then (firstEvent->size() = 2) else (firstEvent->size() = 0) endif"
        ),
    )

class ElementImport(DirectedRelationship):
    """An ElementImport identifies a NamedElement in a Namespace other than the one that owns that NamedElement and allows the NamedElement to be referenced using an unqualified name in the Namespace owning the ElementImport."""
    _PKG = "CommonStructure"
    _DECL = {
    # Specifies the name that should be added to the importing Namespace in lieu of the name of the im
    # ported PackagableElement. The alias must not clash with any other member in the importing Namesp
    # ace. By default, no alias is used.
    'alias': _Ref('alias', str),
    # Specifies the PackageableElement whose name is to be added to a Namespace.
    'importedElement': _Ref('importedElement', "PackageableElement", subsets=("target",), assoc="A_importedElement_import"),
    # Specifies the Namespace that imports a PackageableElement from another Namespace.
    'importingNamespace': _Ref('importingNamespace', "Namespace", subsets=("source", "owner",), assoc="A_elementImport_importingNamespace"),
    # Specifies the visibility of the imported PackageableElement within the importingNamespace, i.e.,
    #  whether the importedElement will in turn be visible to other Namespaces. If the ElementImport i
    # s public, the importedElement will be visible outside the importingNamespace while, if the Eleme
    # ntImport is private, it will not.
    'visibility': _Ref('visibility', VisibilityKind),
    }
    _UNIONS = {
        "owner": ("importingNamespace",),
        "relatedElement": ("importedElement", "importingNamespace",),
        "source": ("importingNamespace",),
        "target": ("importedElement",),
    }
    CONSTRAINTS = (
        ("imported_element_is_public",
         "importedElement.visibility <> null implies importedElement.visibility = VisibilityKind::"
         "public"
        ),
        ("visibility_public_or_private",
         "visibility = VisibilityKind::public or visibility = VisibilityKind::private"
        ),
    )
    def getName(self) -> str:
        """
        The query getName() returns the name under which the imported PackageableElement will be known
         in the importing namespace.
        [ElementImport operation (query); params: none; returns: str; stub - metamodel metadata only]
        """
        raise NotImplementedError

class Enumeration(DataType):
    """An Enumeration is a DataType whose values are enumerated in the model as EnumerationLiterals."""
    _PKG = "SimpleClassifiers"
    _DECL = {
    # The ordered set of literals owned by this Enumeration.
    'ownedLiteral': _Ref('ownedLiteral', "EnumerationLiteral", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_ownedLiteral_enumeration"),
    }
    _UNIONS = {
        "member": ("ownedLiteral",),
        "ownedElement": ("ownedLiteral",),
        "ownedMember": ("ownedLiteral",),
    }
    CONSTRAINTS = (
        ("immutable",
         "ownedAttribute->forAll(isReadOnly)"
        ),
    )

class InstanceSpecification(DeploymentTarget, PackageableElement, DeployedArtifact):
    """An InstanceSpecification is a model element that represents an instance in a modeled system. An InstanceSpecification can act as a DeploymentTarget in a Deployment relationship, in the case that it represents an instance of a Node. It can also act as a DeployedArtifact, if it represents an instance of an Artifact."""
    _PKG = "Classification"
    _DECL = {
    # The Classifier or Classifiers of the represented instance. If multiple Classifiers are specified
    # , the instance is classified by all of them.
    'classifier': _Ref('classifier', "Classifier", multi=True, lo=0, hi='*', assoc="A_classifier_instanceSpecification"),
    # A Slot giving the value or values of a StructuralFeature of the instance. An InstanceSpecificati
    # on can have one Slot per StructuralFeature of its Classifiers, including inherited features. It 
    # is not necessary to model a Slot for every StructuralFeature, in which case the InstanceSpecific
    # ation is a partial description.
    'slot': _Ref('slot', "Slot", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_slot_owningInstance"),
    # A specification of how to compute, derive, or construct the instance.
    'specification': _Ref('specification', "ValueSpecification", composite=True, subsets=("ownedElement",), assoc="A_specification_owningInstanceSpec"),
    }
    _UNIONS = {
        "ownedElement": ("slot", "specification",),
    }
    CONSTRAINTS = (
        ("deployment_artifact",
         "deploymentForArtifact->notEmpty() implies classifier->exists(oclIsKindOf(Artifact))"
        ),
        ("structural_feature",
         "classifier->forAll(c | (c.allSlottableFeatures()->forAll(f | slot->select(s | s.defining"
         "Feature = f)->size() <= 1)))"
        ),
        ("defining_feature",
         "slot->forAll(s | classifier->exists (c | c.allSlottableFeatures()->includes (s.definingF"
         "eature)))"
        ),
        ("deployment_target",
         "deployment->notEmpty() implies classifier->exists(node | node.oclIsKindOf(Node) and Node"
         ".allInstances()->exists(n | n.part->exists(p | p.type = node)))"
        ),
    )

class EnumerationLiteral(InstanceSpecification):
    """An EnumerationLiteral is a user-defined data value for an Enumeration."""
    _PKG = "SimpleClassifiers"
    _DECL = {
    # The classifier of this EnumerationLiteral derived to be equal to its Enumeration.
    'classifier': _Ref('classifier', "Enumeration", derived=True, readonly=True, redefines=("classifier",), assoc="A_classifier_enumerationLiteral"),
    # The Enumeration that this EnumerationLiteral is a member of.
    'enumeration': _Ref('enumeration', "Enumeration", subsets=("namespace",), assoc="A_ownedLiteral_enumeration"),
    }
    _UNIONS = {
        "memberNamespace": ("enumeration",),
        "namespace": ("enumeration",),
        "owner": ("enumeration",),
    }
    def classifier(self) -> "Enumeration":
        """
        Derivation of Enumeration::/classifier
        [EnumerationLiteral operation (query); params: none; returns: "Enumeration"; stub - metamodel 
        metadata only]
        """
        raise NotImplementedError

class ExceptionHandler(Element):
    """An ExceptionHandler is an Element that specifies a handlerBody ExecutableNode to execute in case the specified exception occurs during the execution of the protected ExecutableNode."""
    _PKG = "Activities"
    _DECL = {
    # An ObjectNode within the handlerBody. When the ExceptionHandler catches an exception, the except
    # ion token is placed on this ObjectNode, causing the handlerBody to execute.
    'exceptionInput': _Ref('exceptionInput', "ObjectNode", assoc="A_exceptionInput_exceptionHandler"),
    # The Classifiers whose instances the ExceptionHandler catches as exceptions. If an exception occu
    # rs whose type is any exceptionType, the ExceptionHandler catches the exception and executes the 
    # handlerBody.
    'exceptionType': _Ref('exceptionType', "Classifier", multi=True, lo=0, hi='*', assoc="A_exceptionType_exceptionHandler"),
    # An ExecutableNode that is executed if the ExceptionHandler catches an exception.
    'handlerBody': _Ref('handlerBody', "ExecutableNode", assoc="A_handlerBody_exceptionHandler"),
    # The ExecutableNode protected by the ExceptionHandler. If an exception propagates out of the prot
    # ectedNode and has a type matching one of the exceptionTypes, then it is caught by this Exception
    # Handler.
    'protectedNode': _Ref('protectedNode', "ExecutableNode", subsets=("owner",), assoc="A_handler_protectedNode"),
    }
    _UNIONS = {
        "owner": ("protectedNode",),
    }
    CONSTRAINTS = (
        ("handler_body_edges",
         "handlerBody.incoming->isEmpty() and handlerBody.outgoing->isEmpty() and exceptionInput.i"
         "ncoming->isEmpty()"
        ),
        ("output_pins",
         "(protectedNode.oclIsKindOf(Action) and protectedNode.oclAsType(Action).output->notEmpty("
         ")) implies ( handlerBody.oclIsKindOf(Action) and let protectedNodeOutput : OrderedSet(Ou"
         "tputPin) = protectedNode.oclAsType(Action).output, handlerBodyOutput : OrderedSet(Output"
         "Pin) = handlerBody.oclAsType(Action).output in protectedNodeOutput->size() = handlerBody"
         "Output->size() and Sequence{1..protectedNodeOutput->size()}->forAll(i | handlerBodyOutpu"
         "t->at(i).type.conformsTo(protectedNodeOutput->at(i).type) and handlerBodyOutput->at(i).i"
         "sOrdered=protectedNodeOutput->at(i).isOrdered and handlerBodyOutput->at(i).compatibleWit"
         "h(protectedNodeOutput->at(i))) )"
        ),
        ("one_input",
         "handlerBody.oclIsKindOf(Action) and let inputs: OrderedSet(InputPin) = handlerBody.oclAs"
         "Type(Action).input in inputs->size()=1 and inputs->first()=exceptionInput"
        ),
        ("edge_source_target",
         "let nodes:Set(ActivityNode) = handlerBody.oclAsType(Action).allOwnedNodes() in nodes.out"
         "going->forAll(nodes->includes(target)) and nodes.incoming->forAll(nodes->includes(source"
         "))"
        ),
        ("handler_body_owner",
         "handlerBody.owner=protectedNode.owner"
        ),
        ("exception_input_type",
         "exceptionInput.type=null or exceptionType->forAll(conformsTo(exceptionInput.type.oclAsTy"
         "pe(Classifier)))"
        ),
    )

class ExecutionEnvironment(Node):
    """An execution environment is a node that offers an execution environment for specific types of components that are deployed on it in the form of executable artifacts."""
    _PKG = "Deployments"

class ExecutionOccurrenceSpecification(OccurrenceSpecification):
    """An ExecutionOccurrenceSpecification represents moments in time at which Actions or Behaviors start or finish."""
    _PKG = "Interactions"
    _DECL = {
    # References the execution specification describing the execution that is started or finished at t
    # his execution event.
    'execution': _Ref('execution', "ExecutionSpecification", assoc="A_execution_executionOccurrenceSpecification"),
    }

class ExpansionNode(ObjectNode):
    """An ExpansionNode is an ObjectNode used to indicate a collection input or output for an ExpansionRegion. A collection input of an ExpansionRegion contains a collection that is broken into its individual elements inside the region, whose content is executed once per element. A collection output of an ExpansionRegion combines individual elements produced by the execution of the region into a collection for use outside the region."""
    _PKG = "Actions"
    _DECL = {
    # The ExpansionRegion for which the ExpansionNode is an input.
    'regionAsInput': _Ref('regionAsInput', "ExpansionRegion", assoc="A_inputElement_regionAsInput"),
    # The ExpansionRegion for which the ExpansionNode is an output.
    'regionAsOutput': _Ref('regionAsOutput', "ExpansionRegion", assoc="A_outputElement_regionAsOutput"),
    }
    CONSTRAINTS = (
        ("region_as_input_or_output",
         "regionAsInput->notEmpty() xor regionAsOutput->notEmpty()"
        ),
    )

class ExpansionRegion(StructuredActivityNode):
    """An ExpansionRegion is a StructuredActivityNode that executes its content multiple times corresponding to elements of input collection(s)."""
    _PKG = "Actions"
    _DECL = {
    # The ExpansionNodes that hold the input collections for the ExpansionRegion.
    'inputElement': _Ref('inputElement', "ExpansionNode", multi=True, lo=0, hi='*', assoc="A_inputElement_regionAsInput"),
    # The mode in which the ExpansionRegion executes its contents. If parallel, executions are concurr
    # ent. If iterative, executions are sequential. If stream, a stream of values flows into a single 
    # execution.
    'mode': _Ref('mode', ExpansionKind),
    # The ExpansionNodes that form the output collections of the ExpansionRegion.
    'outputElement': _Ref('outputElement', "ExpansionNode", multi=True, lo=0, hi='*', assoc="A_outputElement_regionAsOutput"),
    }

class Expression(ValueSpecification):
    """An Expression represents a node in an expression tree, which may be non-terminal or terminal. It defines a symbol, and has a possibly empty sequence of operands that are ValueSpecifications. It denotes a (possibly empty) set of values when evaluated in a context."""
    _PKG = "Values"
    _DECL = {
    # Specifies a sequence of operand ValueSpecifications.
    'operand': _Ref('operand', "ValueSpecification", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_operand_expression"),
    # The symbol associated with this node in the expression tree.
    'symbol': _Ref('symbol', str),
    }
    _UNIONS = {
        "ownedElement": ("operand",),
    }

class Extend(DirectedRelationship, NamedElement):
    """A relationship from an extending UseCase to an extended UseCase that specifies how and when the behavior defined in the extending UseCase can be inserted into the behavior defined in the extended UseCase."""
    _PKG = "UseCases"
    _DECL = {
    # References the condition that must hold when the first ExtensionPoint is reached for the extensi
    # on to take place. If no constraint is associated with the Extend relationship, the extension is 
    # unconditional.
    'condition': _Ref('condition', "Constraint", composite=True, subsets=("ownedElement",), assoc="A_condition_extend"),
    # The UseCase that is being extended.
    'extendedCase': _Ref('extendedCase', "UseCase", subsets=("target",), assoc="A_extendedCase_extend"),
    # The UseCase that represents the extension and owns the Extend relationship.
    'extension': _Ref('extension', "UseCase", subsets=("source", "namespace",), assoc="A_extend_extension"),
    # An ordered list of ExtensionPoints belonging to the extended UseCase, specifying where the respe
    # ctive behavioral fragments of the extending UseCase are to be inserted. The first fragment in th
    # e extending UseCase is associated with the first extension point in the list, the second fragmen
    # t with the second point, and so on. Note that, in most practical cases, the extending UseCase ha
    # s just a single behavior fragment, so that the list of ExtensionPoints is trivial.
    'extensionLocation': _Ref('extensionLocation', "ExtensionPoint", multi=True, lo=0, hi='*', assoc="A_extensionLocation_extension"),
    }
    _UNIONS = {
        "memberNamespace": ("extension",),
        "namespace": ("extension",),
        "ownedElement": ("condition",),
        "owner": ("extension",),
        "relatedElement": ("extendedCase", "extension",),
        "source": ("extension",),
        "target": ("extendedCase",),
    }
    CONSTRAINTS = (
        ("extension_points",
         "extensionLocation->forAll (xp | extendedCase.extensionPoint->includes(xp))"
        ),
    )

class Extension(Association):
    """An extension is used to indicate that the properties of a metaclass are extended through a stereotype, and gives the ability to flexibly add (and later remove) stereotypes to classes."""
    _PKG = "Packages"
    _DECL = {
    # Indicates whether an instance of the extending stereotype must be created when an instance of th
    # e extended class is created. The attribute value is derived from the value of the lower property
    #  of the ExtensionEnd referenced by Extension::ownedEnd; a lower value of 1 means that isRequired
    #  is true, but otherwise it is false. Since the default value of ExtensionEnd::lower is 0, the de
    # fault value of isRequired is false.
    'isRequired': _Ref('isRequired', bool, derived=True, readonly=True),
    # References the Class that is extended through an Extension. The property is derived from the typ
    # e of the memberEnd that is not the ownedEnd.
    'metaclass': _Ref('metaclass', "Class", derived=True, readonly=True, assoc="A_extension_metaclass"),
    # References the end of the extension that is typed by a Stereotype.
    'ownedEnd': _Ref('ownedEnd', "ExtensionEnd", composite=True, redefines=("ownedEnd",), assoc="A_ownedEnd_extension"),
    }
    CONSTRAINTS = (
        ("non_owned_end",
         "metaclassEnd()->notEmpty() and metaclassEnd().type.oclIsKindOf(Class)"
        ),
        ("is_binary",
         "memberEnd->size() = 2"
        ),
    )
    def isRequired(self) -> bool:
        """
        The query isRequired() is true if the owned end has a multiplicity with the lower bound of 1.
        [Extension operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def metaclass(self) -> "Class":
        """
        The query metaclass() returns the metaclass that is being extended (as opposed to the extendin
        g stereotype).
        [Extension operation (query); params: none; returns: "Class"; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def metaclassEnd(self) -> "Property":
        """
        The query metaclassEnd() returns the Property that is typed by a metaclass (as opposed to a st
        ereotype).
        [Extension operation (query); params: none; returns: "Property"; stub - metamodel metadata onl
        y]
        """
        raise NotImplementedError

class StructuralFeature(Feature, TypedElement, MultiplicityElement):
    """A StructuralFeature is a typed feature of a Classifier that specifies the structure of instances of the Classifier."""
    _PKG = "Classification"
    _DECL = {
    # If isReadOnly is true, the StructuralFeature may not be written to after initialization.
    'isReadOnly': _Ref('isReadOnly', bool),
    }

class Property(StructuralFeature, ConnectableElement, DeploymentTarget):
    """A Property is a StructuralFeature. A Property related by ownedAttribute to a Classifier (other than an association) represents an attribute and might also represent an association end. It relates an instance of the Classifier to a value or set of values of the type of the attribute. A Property related by memberEnd to an Association represents an end of the Association. The type of the Property is the type of the end of the Association. A Property has the capability of being a DeploymentTarget in a Deployment relationship. This enables modeling the deployment to hierarchical nodes that have Properties functioning as internal parts. Property specializes ParameterableElement to specify that a Property can be exposed as a formal template parameter, and provided as an actual parameter in a binding of a template."""
    _PKG = "Classification"
    _DECL = {
    # Specifies the kind of aggregation that applies to the Property.
    'aggregation': _Ref('aggregation', AggregationKind),
    # The Association of which this Property is a member, if any.
    'association': _Ref('association', "Association", subsets=("memberNamespace",), assoc="A_memberEnd_association"),
    # Designates the optional association end that owns a qualifier attribute.
    'associationEnd': _Ref('associationEnd', "Property", subsets=("owner",), assoc="A_qualifier_associationEnd"),
    # The Class that owns this Property, if any.
    'class_': _Ref('class', "Class", subsets=("classifier", "structuredClassifier", "namespace",), assoc="A_ownedAttribute_class"),
    # The DataType that owns this Property, if any.
    'datatype': _Ref('datatype', "DataType", subsets=("classifier", "namespace",), assoc="A_ownedAttribute_datatype"),
    # A ValueSpecification that is evaluated to give a default value for the Property when an instance
    #  of the owning Classifier is instantiated.
    'defaultValue': _Ref('defaultValue', "ValueSpecification", composite=True, subsets=("ownedElement",), assoc="A_defaultValue_owningProperty"),
    # The Interface that owns this Property, if any.
    'interface': _Ref('interface', "Interface", subsets=("classifier", "namespace",), assoc="A_ownedAttribute_interface"),
    # If isComposite is true, the object containing the attribute is a container for the object or val
    # ue contained in the attribute. This is a derived value, indicating whether the aggregation of th
    # e Property is composite or not.
    'isComposite': _Ref('isComposite', bool, derived=True),
    # Specifies whether the Property is derived, i.e., whether its value or values can be computed fro
    # m other information.
    'isDerived': _Ref('isDerived', bool),
    # Specifies whether the property is derived as the union of all of the Properties that are constra
    # ined to subset it.
    'isDerivedUnion': _Ref('isDerivedUnion', bool),
    # True indicates this property can be used to uniquely identify an instance of the containing Clas
    # s.
    'isID': _Ref('isID', bool),
    # In the case where the Property is one end of a binary association this gives the other end.
    'opposite': _Ref('opposite', "Property", derived=True, assoc="A_opposite_property"),
    # The owning association of this property, if any.
    'owningAssociation': _Ref('owningAssociation', "Association", subsets=("featuringClassifier", "namespace", "association", "redefinitionContext",), assoc="A_ownedEnd_owningAssociation"),
    # An optional list of ordered qualifier attributes for the end.
    'qualifier': _Ref('qualifier', "Property", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_qualifier_associationEnd"),
    # The properties that are redefined by this property, if any.
    'redefinedProperty': _Ref('redefinedProperty', "Property", multi=True, lo=0, hi='*', subsets=("redefinedElement",), assoc="A_redefinedProperty_property"),
    # The properties of which this Property is constrained to be a subset, if any.
    'subsettedProperty': _Ref('subsettedProperty', "Property", multi=True, lo=0, hi='*', assoc="A_subsettedProperty_property"),
    }
    _UNIONS = {
        "classifier": ("class_", "datatype", "interface",),
        "featuringClassifier": ("class_", "datatype", "interface", "owningAssociation",),
        "memberNamespace": ("association", "class_", "datatype", "interface", "owningAssociation",),
        "namespace": ("class_", "datatype", "interface", "owningAssociation",),
        "ownedElement": ("defaultValue", "qualifier",),
        "owner": ("associationEnd", "class_", "datatype", "interface", "owningAssociation",),
        "redefinedElement": ("redefinedProperty",),
        "redefinitionContext": ("class_", "datatype", "interface", "owningAssociation",),
    }
    CONSTRAINTS = (
        ("subsetting_context_conforms",
         "subsettedProperty->notEmpty() implies (subsettingContext()->notEmpty() and subsettingCon"
         "text()->forAll (sc | subsettedProperty->forAll(sp | sp.subsettingContext()->exists(c | s"
         "c.conformsTo(c)))))"
        ),
        ("derived_union_is_read_only",
         "isDerivedUnion implies isReadOnly"
        ),
        ("multiplicity_of_composite",
         "isComposite and association <> null implies opposite.upperBound() <= 1"
        ),
        ("redefined_property_inherited",
         "(redefinedProperty->notEmpty()) implies (redefinitionContext->notEmpty() and redefinedPr"
         "operty->forAll(rp| ((redefinitionContext->collect(fc| fc.allParents()))->asSet())->colle"
         "ct(c| c.allFeatures())->asSet()->includes(rp)))"
        ),
        ("subsetting_rules",
         "subsettedProperty->forAll(sp | self.type.conformsTo(sp.type) and ((self.upperBound()->no"
         "tEmpty() and sp.upperBound()->notEmpty()) implies self.upperBound() <= sp.upperBound() )"
         ")"
        ),
        ("binding_to_attribute",
         "(self.isAttribute() and (templateParameterSubstitution->notEmpty()) implies (templatePar"
         "ameterSubstitution->forAll(ts | ts.formal.oclIsKindOf(Property) and ts.formal.oclAsType("
         "Property).isAttribute())))"
        ),
        ("derived_union_is_derived",
         "isDerivedUnion implies isDerived"
        ),
        ("deployment_target",
         "deployment->notEmpty() implies owner.oclIsKindOf(Node) and Node.allInstances()->exists(n"
         " | n.part->exists(p | p = self))"
        ),
        ("subsetted_property_names",
         "subsettedProperty->forAll(sp | sp.name <> name)"
        ),
        ("type_of_opposite_end",
         "(opposite->notEmpty() and owningAssociation->isEmpty()) implies classifier = opposite.ty"
         "pe"
        ),
        ("qualified_is_association_end",
         "qualifier->notEmpty() implies association->notEmpty()"
        ),
    )
    def isAttribute(self) -> bool:
        """
        The query isAttribute() is true if the Property is defined as an attribute of some Classifier.
        [Property operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isCompatibleWith(self, p: "ParameterableElement" = None) -> bool:
        """
        The query isCompatibleWith() determines if this Property is compatible with the specified Para
        meterableElement. This Property is compatible with ParameterableElement p if the kind of this 
        Property is thesame as or a subtype of the kind of p. Further, if p is a TypedElement, then th
        e type of this Property must be conformant with the type of p.
        [Property operation (query); params: p: "ParameterableElement"; returns: bool; stub - metamode
        l metadata only]
        """
        raise NotImplementedError
    def isComposite(self) -> bool:
        """
        The value of isComposite is true only if aggregation is composite.
        [Property operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isConsistentWith(self, redefiningElement: "RedefinableElement" = None) -> bool:
        """
        The query isConsistentWith() specifies, for any two Properties in a context in which redefinit
        ion is possible, whether redefinition would be logically consistent. A redefining Property is 
        consistent with a redefined Property if the type of the redefining Property conforms to the ty
        pe of the redefined Property, and the multiplicity of the redefining Property (if specified) i
        s contained in the multiplicity of the redefined Property.
        [Property operation (query); params: redefiningElement: "RedefinableElement"; returns: bool; s
        tub - metamodel metadata only]
        """
        raise NotImplementedError
    def isNavigable(self) -> bool:
        """
        The query isNavigable() indicates whether it is possible to navigate across the property.
        [Property operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def opposite(self) -> "Property":
        """
        If this property is a memberEnd of a binary association, then opposite gives the other end.
        [Property operation (query); params: none; returns: "Property"; stub - metamodel metadata only
        ]
        """
        raise NotImplementedError
    def subsettingContext(self) -> "Type":
        """
        The query subsettingContext() gives the context for subsetting a Property. It consists, in the
         case of an attribute, of the corresponding Classifier, and in the case of an association end,
         all of the Classifiers at the other ends.
        [Property operation (query); params: none; returns: "Type"; stub - metamodel metadata only]
        """
        raise NotImplementedError

class ExtensionEnd(Property):
    """An extension end is used to tie an extension to a stereotype when extending a metaclass. The default multiplicity of an extension end is 0..1."""
    _PKG = "Packages"
    _DECL = {
    # This redefinition changes the default multiplicity of association ends, since model elements are
    #  usually extended by 0 or 1 instance of the extension stereotype.
    'lower': _Ref('lower', int, derived=True, redefines=("lower",)),
    # References the type of the ExtensionEnd. Note that this association restricts the possible types
    #  of an ExtensionEnd to only be Stereotypes.
    'type': _Ref('type', "Stereotype", redefines=("type",), assoc="A_type_extensionEnd"),
    }
    CONSTRAINTS = (
        ("multiplicity",
         "(lowerBound() = 0 or lowerBound() = 1) and upperBound() = 1"
        ),
        ("aggregation",
         "self.aggregation = AggregationKind::composite"
        ),
    )
    def lowerBound(self) -> int:
        """
        The query lowerBound() returns the lower bound of the multiplicity as an Integer. This is a re
        definition of the default lower bound, which normally, for MultiplicityElements, evaluates to 
        1 if empty.
        [ExtensionEnd operation (query); params: none; returns: int; stub - metamodel metadata only]
        """
        raise NotImplementedError

class ExtensionPoint(RedefinableElement):
    """An ExtensionPoint identifies a point in the behavior of a UseCase where that behavior can be extended by the behavior of some other (extending) UseCase, as specified by an Extend relationship."""
    _PKG = "UseCases"
    _DECL = {
    # The UseCase that owns this ExtensionPoint.
    'useCase': _Ref('useCase', "UseCase", subsets=("namespace",), assoc="A_extensionPoint_useCase"),
    }
    _UNIONS = {
        "memberNamespace": ("useCase",),
        "namespace": ("useCase",),
        "owner": ("useCase",),
    }
    CONSTRAINTS = (
        ("must_have_name",
         "name->notEmpty ()"
        ),
    )

class State(Vertex, Namespace):
    """A State models a situation during which some (usually implicit) invariant condition holds."""
    _PKG = "StateMachines"
    _DECL = {
    # The entry and exit connection points used in conjunction with this (submachine) State, i.e., as 
    # targets and sources, respectively, in the Region with the submachine State. A connection point r
    # eference references the corresponding definition of a connection point Pseudostate in the StateM
    # achine referenced by the submachine State.
    'connection': _Ref('connection', "ConnectionPointReference", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_connection_state"),
    # The entry and exit Pseudostates of a composite State. These can only be entry or exit Pseudostat
    # es, and they must have different names. They can only be defined for composite States.
    'connectionPoint': _Ref('connectionPoint', "Pseudostate", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_connectionPoint_state"),
    # A list of Triggers that are candidates to be retained by the StateMachine if they trigger no Tra
    # nsitions out of the State (not consumed). A deferred Trigger is retained until the StateMachine 
    # reaches a State configuration where it is no longer deferred.
    'deferrableTrigger': _Ref('deferrableTrigger', "Trigger", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_deferrableTrigger_state"),
    # An optional Behavior that is executed while being in the State. The execution starts when this S
    # tate is entered, and ceases either by itself when done, or when the State is exited, whichever c
    # omes first.
    'doActivity': _Ref('doActivity', "Behavior", composite=True, subsets=("ownedElement",), assoc="A_doActivity_state"),
    # An optional Behavior that is executed whenever this State is entered regardless of the Transitio
    # n taken to reach the State. If defined, entry Behaviors are always executed to completion prior 
    # to any internal Behavior or Transitions performed within the State.
    'entry': _Ref('entry', "Behavior", composite=True, subsets=("ownedElement",), assoc="A_entry_state"),
    # An optional Behavior that is executed whenever this State is exited regardless of which Transiti
    # on was taken out of the State. If defined, exit Behaviors are always executed to completion only
    #  after all internal and transition Behaviors have completed execution.
    'exit': _Ref('exit', "Behavior", composite=True, subsets=("ownedElement",), assoc="A_exit_state"),
    # A state with isComposite=true is said to be a composite State. A composite State is a State that
    #  contains at least one Region.
    'isComposite': _Ref('isComposite', bool, derived=True, readonly=True),
    # A State with isOrthogonal=true is said to be an orthogonal composite State An orthogonal composi
    # te State contains two or more Regions.
    'isOrthogonal': _Ref('isOrthogonal', bool, derived=True, readonly=True),
    # A State with isSimple=true is said to be a simple State A simple State does not have any Regions
    #  and it does not refer to any submachine StateMachine.
    'isSimple': _Ref('isSimple', bool, derived=True, readonly=True),
    # A State with isSubmachineState=true is said to be a submachine State Such a State refers to anot
    # her StateMachine(submachine).
    'isSubmachineState': _Ref('isSubmachineState', bool, derived=True, readonly=True),
    # The Regions owned directly by the State.
    'region': _Ref('region', "Region", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_region_state"),
    # Specifies conditions that are always true when this State is the current State. In ProtocolState
    # Machines state invariants are additional conditions to the preconditions of the outgoing Transit
    # ions, and to the postcondition of the incoming Transitions.
    'stateInvariant': _Ref('stateInvariant', "Constraint", composite=True, subsets=("ownedRule",), assoc="A_stateInvariant_owningState"),
    # The StateMachine that is to be inserted in place of the (submachine) State.
    'submachine': _Ref('submachine', "StateMachine", assoc="A_submachineState_submachine"),
    }
    _UNIONS = {
        "member": ("connection", "connectionPoint", "region", "stateInvariant",),
        "ownedElement": ("connection", "connectionPoint", "deferrableTrigger", "doActivity", "entry", "exit", "region", "stateInvariant",),
        "ownedMember": ("connection", "connectionPoint", "region", "stateInvariant",),
    }
    CONSTRAINTS = (
        ("entry_or_exit",
         "connectionPoint->forAll(kind = PseudostateKind::entryPoint or kind = PseudostateKind::ex"
         "itPoint)"
        ),
        ("submachine_states",
         "isSubmachineState implies connection->notEmpty( )"
        ),
        ("composite_states",
         "connectionPoint->notEmpty() implies isComposite"
        ),
        ("destinations_or_sources_of_transitions",
         "self.isSubmachineState implies (self.connection->forAll (cp | cp.entry->forAll (ps | ps."
         "stateMachine = self.submachine) and cp.exit->forAll (ps | ps.stateMachine = self.submach"
         "ine)))"
        ),
        ("submachine_or_regions",
         "isComposite implies not isSubmachineState"
        ),
    )
    def containingStateMachine(self) -> "StateMachine":
        """
        The query containingStateMachine() returns the StateMachine that contains the State either dir
        ectly or transitively.
        [State operation (query); params: none; returns: "StateMachine"; stub - metamodel metadata onl
        y]
        """
        raise NotImplementedError
    def isComposite(self) -> bool:
        """
        A composite State is a State with at least one Region.
        [State operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isConsistentWith(self, redefiningElement: "RedefinableElement" = None) -> bool:
        """
        The query isConsistentWith specifies that a non-final State can only be redefined by a non-fin
        al State (this is overridden by FinalState to allow a FinalState to be redefined by a FinalSta
        te) and, if the redefined State is a submachine State, then the redefining State must be a sub
        machine state whose submachine is a redefinition of the submachine of the redefined State. Not
        e that consistency requirements for the redefinition of Regions and connectionPoint Pseudostat
        es within a composite State and connection ConnectionPoints of a submachine State are specifie
        d by the isConsistentWith and isRedefinitionContextValid operations for Region and Vertex (and
         its subclasses, Pseudostate and ConnectionPointReference).
        [State operation (query); params: redefiningElement: "RedefinableElement"; returns: bool; stub
         - metamodel metadata only]
        """
        raise NotImplementedError
    def isOrthogonal(self) -> bool:
        """
        An orthogonal State is a composite state with at least 2 regions.
        [State operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isSimple(self) -> bool:
        """
        A simple State is a State without any regions.
        [State operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isSubmachineState(self) -> bool:
        """
        Only submachine State references another StateMachine.
        [State operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError

class FinalState(State):
    """A special kind of State, which, when entered, signifies that the enclosing Region has completed. If the enclosing Region is directly contained in a StateMachine and all other Regions in that StateMachine also are completed, then it means that the entire StateMachine behavior is completed."""
    _PKG = "StateMachines"
    CONSTRAINTS = (
        ("no_exit_behavior",
         "exit->isEmpty()"
        ),
        ("no_outgoing_transitions",
         "outgoing->size() = 0"
        ),
        ("no_regions",
         "region->size() = 0"
        ),
        ("cannot_reference_submachine",
         "submachine->isEmpty()"
        ),
        ("no_entry_behavior",
         "entry->isEmpty()"
        ),
        ("no_state_behavior",
         "doActivity->isEmpty()"
        ),
    )
    def isConsistentWith(self, redefiningElement: "RedefinableElement" = None) -> bool:
        """
        The query isConsistentWith() specifies a FinalState can only be redefined by a FinalState.
        [FinalState operation; params: redefiningElement: "RedefinableElement"; returns: bool; stub - 
        metamodel metadata only]
        """
        raise NotImplementedError

class FlowFinalNode(FinalNode):
    """A FlowFinalNode is a FinalNode that terminates a flow by consuming the tokens offered to it."""
    _PKG = "Activities"

class ForkNode(ControlNode):
    """A ForkNode is a ControlNode that splits a flow into multiple concurrent flows."""
    _PKG = "Activities"
    CONSTRAINTS = (
        ("edges",
         "let allEdges : Set(ActivityEdge) = incoming->union(outgoing) in allEdges->forAll(oclIsKi"
         "ndOf(ControlFlow)) or allEdges->forAll(oclIsKindOf(ObjectFlow))"
        ),
        ("one_incoming_edge",
         "incoming->size()=1"
        ),
    )

class OpaqueBehavior(Behavior):
    """An OpaqueBehavior is a Behavior whose specification is given in a textual language other than UML."""
    _PKG = "CommonBehavior"
    _DECL = {
    # Specifies the behavior in one or more languages.
    'body': _Ref('body', str, multi=True, lo=0, hi='*'),
    # Languages the body strings use in the same order as the body strings.
    'language': _Ref('language', str, multi=True, lo=0, hi='*'),
    }

class FunctionBehavior(OpaqueBehavior):
    """A FunctionBehavior is an OpaqueBehavior that does not access or modify any objects or other external data."""
    _PKG = "CommonBehavior"
    CONSTRAINTS = (
        ("one_output_parameter",
         "self.ownedParameter-> select(p | p.direction = ParameterDirectionKind::out or p.directio"
         "n= ParameterDirectionKind::inout or p.direction= ParameterDirectionKind::return)->size()"
         " >= 1"
        ),
        ("types_of_parameters",
         "ownedParameter->forAll(p | p.type <> null and p.type.oclIsTypeOf(DataType) and hasAllDat"
         "aTypeAttributes(p.type.oclAsType(DataType)))"
        ),
    )
    def hasAllDataTypeAttributes(self, d: "DataType" = None) -> bool:
        """
        The hasAllDataTypeAttributes query tests whether the types of the attributes of the given Data
        Type are all DataTypes, and similarly for all those DataTypes.
        [FunctionBehavior operation (query); params: d: "DataType"; returns: bool; stub - metamodel me
        tadata only]
        """
        raise NotImplementedError

class Gate(MessageEnd):
    """A Gate is a MessageEnd which serves as a connection point for relating a Message which has a MessageEnd (sendEvent / receiveEvent) outside an InteractionFragment with another Message which has a MessageEnd (receiveEvent / sendEvent) inside that InteractionFragment."""
    _PKG = "Interactions"
    CONSTRAINTS = (
        ("actual_gate_matched",
         "interactionUse->notEmpty() implies interactionUse.refersTo.formalGate->select(matches(se"
         "lf))->size()=1"
        ),
        ("inside_cf_matched",
         "isInsideCF() implies combinedFragment.cfragmentGate->select(isOutsideCF() and matches(se"
         "lf))->size()=1"
        ),
        ("outside_cf_matched",
         "isOutsideCF() implies if self.combinedFragment.interactionOperator->asOrderedSet()->firs"
         "t() = InteractionOperatorKind::alt then self.combinedFragment.operand->forAll(op : Inter"
         "actionOperand | self.combinedFragment.cfragmentGate->select(isInsideCF() and oppositeEnd"
         "().enclosingFragment()->includes(self.combinedFragment) and matches(self))->size()=1) el"
         "se self.combinedFragment.cfragmentGate->select(isInsideCF() and matches(self))->size()=1"
         " endif"
        ),
        ("formal_gate_distinguishable",
         "isFormal() implies interaction.formalGate->select(getName() = self.getName())->size()=1"
        ),
        ("actual_gate_distinguishable",
         "isActual() implies interactionUse.actualGate->select(getName() = self.getName())->size()"
         "=1"
        ),
        ("outside_cf_gate_distinguishable",
         "isOutsideCF() implies combinedFragment.cfragmentGate->select(getName() = self.getName())"
         "->size()=1"
        ),
        ("inside_cf_gate_distinguishable",
         "isInsideCF() implies let selfOperand : InteractionOperand = self.getOperand() in combine"
         "dFragment.cfragmentGate->select(isInsideCF() and getName() = self.getName())->select(get"
         "Operand() = selfOperand)->size()=1"
        ),
    )
    def isOutsideCF(self) -> bool:
        """
        This query returns true if this Gate is attached to the boundary of a CombinedFragment, and it
        s other end (if present) is outside of the same CombinedFragment.
        [Gate operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isInsideCF(self) -> bool:
        """
        This query returns true if this Gate is attached to the boundary of a CombinedFragment, and it
        s other end (if present) is inside of an InteractionOperator of the same CombinedFragment.
        [Gate operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isActual(self) -> bool:
        """
        This query returns true value if this Gate is an actualGate of an InteractionUse.
        [Gate operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isFormal(self) -> bool:
        """
        This query returns true if this Gate is a formalGate of an Interaction.
        [Gate operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def getName(self) -> str:
        """
        This query returns the name of the gate, either the explicit name (.name) or the constructed n
        ame ('out_" or 'in_' concatenated in front of .message.name) if the explicit name is not prese
        nt.
        [Gate operation (query); params: none; returns: str; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def matches(self, gateToMatch: "Gate" = None) -> bool:
        """
        This query returns true if the name of this Gate matches the name of the in parameter Gate, an
        d the messages for the two Gates correspond. The Message for one Gate (say A) corresponds to t
        he Message for another Gate (say B) if (A and B have the same name value) and (if A is a sendE
        vent then B is a receiveEvent) and (if A is a receiveEvent then B is a sendEvent) and (A and B
         have the same messageSort value) and (A and B have the same signature value).
        [Gate operation (query); params: gateToMatch: "Gate"; returns: bool; stub - metamodel metadata
         only]
        """
        raise NotImplementedError
    def isDistinguishableFrom(self, n: "NamedElement" = None, ns: "Namespace" = None) -> bool:
        """
        The query isDistinguishableFrom() specifies that two Gates may coexist in the same Namespace, 
        without an explicit name property. The association end formalGate subsets ownedElement, and si
        nce the Gate name attribute is optional, it is allowed to have two formal gates without an exp
        licit name, but having derived names which are distinct.
        [Gate operation (query); params: n: "NamedElement", ns: "Namespace"; returns: bool; stub - met
        amodel metadata only]
        """
        raise NotImplementedError
    def getOperand(self) -> "InteractionOperand":
        """
        If the Gate is an inside Combined Fragment Gate, this operation returns the InteractionOperand
         that the opposite end of this Gate is included within.
        [Gate operation (query); params: none; returns: "InteractionOperand"; stub - metamodel metadat
        a only]
        """
        raise NotImplementedError

class GeneralOrdering(NamedElement):
    """A GeneralOrdering represents a binary relation between two OccurrenceSpecifications, to describe that one OccurrenceSpecification must occur before the other in a valid trace. This mechanism provides the ability to define partial orders of OccurrenceSpecifications that may otherwise not have a specified order."""
    _PKG = "Interactions"
    _DECL = {
    # The OccurrenceSpecification referenced comes after the OccurrenceSpecification referenced by bef
    # ore.
    'after': _Ref('after', "OccurrenceSpecification", assoc="A_toBefore_after"),
    # The OccurrenceSpecification referenced comes before the OccurrenceSpecification referenced by af
    # ter.
    'before': _Ref('before', "OccurrenceSpecification", assoc="A_before_toAfter"),
    }
    CONSTRAINTS = (
        ("irreflexive_transitive_closure",
         "after->closure(toAfter.after)->excludes(before)"
        ),
    )

class Generalization(DirectedRelationship):
    """A Generalization is a taxonomic relationship between a more general Classifier and a more specific Classifier. Each instance of the specific Classifier is also an instance of the general Classifier. The specific Classifier inherits the features of the more general Classifier. A Generalization is owned by the specific Classifier."""
    _PKG = "Classification"
    _DECL = {
    # The general classifier in the Generalization relationship.
    'general': _Ref('general', "Classifier", subsets=("target",), assoc="A_general_generalization"),
    # Represents a set of instances of Generalization. A Generalization may appear in many Generalizat
    # ionSets.
    'generalizationSet': _Ref('generalizationSet', "GeneralizationSet", multi=True, lo=0, hi='*', assoc="A_generalizationSet_generalization"),
    # Indicates whether the specific Classifier can be used wherever the general Classifier can be use
    # d. If true, the execution traces of the specific Classifier shall be a superset of the execution
    #  traces of the general Classifier. If false, there is no such constraint on execution traces. If
    #  unset, the modeler has not stated whether there is such a constraint or not.
    'isSubstitutable': _Ref('isSubstitutable', bool),
    # The specializing Classifier in the Generalization relationship.
    'specific': _Ref('specific', "Classifier", subsets=("source", "owner",), assoc="A_generalization_specific"),
    }
    _UNIONS = {
        "owner": ("specific",),
        "relatedElement": ("general", "specific",),
        "source": ("specific",),
        "target": ("general",),
    }

class GeneralizationSet(PackageableElement):
    """A GeneralizationSet is a PackageableElement whose instances represent sets of Generalization relationships."""
    _PKG = "Classification"
    _DECL = {
    # Designates the instances of Generalization that are members of this GeneralizationSet.
    'generalization': _Ref('generalization', "Generalization", multi=True, lo=0, hi='*', assoc="A_generalizationSet_generalization"),
    # Indicates (via the associated Generalizations) whether or not the set of specific Classifiers ar
    # e covering for a particular general classifier. When isCovering is true, every instance of a par
    # ticular general Classifier is also an instance of at least one of its specific Classifiers for t
    # he GeneralizationSet. When isCovering is false, there are one or more instances of the particula
    # r general Classifier that are not instances of at least one of its specific Classifiers defined 
    # for the GeneralizationSet.
    'isCovering': _Ref('isCovering', bool),
    # Indicates whether or not the set of specific Classifiers in a Generalization relationship have i
    # nstance in common. If isDisjoint is true, the specific Classifiers for a particular Generalizati
    # onSet have no members in common; that is, their intersection is empty. If isDisjoint is false, t
    # he specific Classifiers in a particular GeneralizationSet have one or more members in common; th
    # at is, their intersection is not empty.
    'isDisjoint': _Ref('isDisjoint', bool),
    # Designates the Classifier that is defined as the power type for the associated GeneralizationSet
    # , if there is one.
    'powertype': _Ref('powertype', "Classifier", assoc="A_powertypeExtent_powertype"),
    }
    CONSTRAINTS = (
        ("generalization_same_classifier",
         "generalization->collect(general)->asSet()->size() <= 1"
        ),
        ("maps_to_generalization_set",
         "powertype <> null implies generalization->forAll( gen | not (gen.general = powertype) an"
         "d not gen.general.allParents()->includes(powertype) and not (gen.specific = powertype) a"
         "nd not powertype.allParents()->includes(gen.specific) )"
        ),
    )

class Image(Element):
    """Physical definition of a graphical image."""
    _PKG = "Packages"
    _DECL = {
    # This contains the serialization of the image according to the format. The value could represent 
    # a bitmap, image such as a GIF file, or drawing 'instructions' using a standard such as Scalable 
    # Vector Graphic (SVG) (which is XML based).
    'content': _Ref('content', str),
    # This indicates the format of the content, which is how the string content should be interpreted.
    #  The following values are reserved: SVG, GIF, PNG, JPG, WMF, EMF, BMP. In addition the prefix 'M
    # IME: ' is also reserved. This option can be used as an alternative to express the reserved value
    # s above, for example "SVG" could instead be expressed as "MIME: image/svg+xml".
    'format': _Ref('format', str),
    # This contains a location that can be used by a tool to locate the image as an alternative to emb
    # edding it in the stereotype.
    'location': _Ref('location', str),
    }

class Include(DirectedRelationship, NamedElement):
    """An Include relationship specifies that a UseCase contains the behavior defined in another UseCase."""
    _PKG = "UseCases"
    _DECL = {
    # The UseCase that is to be included.
    'addition': _Ref('addition', "UseCase", subsets=("target",), assoc="A_addition_include"),
    # The UseCase which includes the addition and owns the Include relationship.
    'includingCase': _Ref('includingCase', "UseCase", subsets=("source", "namespace",), assoc="A_include_includingCase"),
    }
    _UNIONS = {
        "memberNamespace": ("includingCase",),
        "namespace": ("includingCase",),
        "owner": ("includingCase",),
        "relatedElement": ("addition", "includingCase",),
        "source": ("includingCase",),
        "target": ("addition",),
    }

class InformationFlow(DirectedRelationship, PackageableElement):
    """InformationFlows describe circulation of information through a system in a general manner. They do not specify the nature of the information, mechanisms by which it is conveyed, sequences of exchange or any control conditions. During more detailed modeling, representation and realization links may be added to specify which model elements implement an InformationFlow and to show how information is conveyed. InformationFlows require some kind of “information channel” for unidirectional transmission of information items from sources to targets. They specify the information channel’s realizations, if any, and identify the information that flows along them. Information moving along the information channel may be represented by abstract InformationItems and by concrete Classifiers."""
    _PKG = "InformationFlows"
    _DECL = {
    # Specifies the information items that may circulate on this information flow.
    'conveyed': _Ref('conveyed', "Classifier", multi=True, lo=0, hi='*', assoc="A_conveyed_conveyingFlow"),
    # Defines from which source the conveyed InformationItems are initiated.
    'informationSource': _Ref('informationSource', "NamedElement", multi=True, lo=0, hi='*', subsets=("source",), assoc="A_informationSource_informationFlow"),
    # Defines to which target the conveyed InformationItems are directed.
    'informationTarget': _Ref('informationTarget', "NamedElement", multi=True, lo=0, hi='*', subsets=("target",), assoc="A_informationTarget_informationFlow"),
    # Determines which Relationship will realize the specified flow.
    'realization': _Ref('realization', "Relationship", multi=True, lo=0, hi='*', assoc="A_realization_abstraction_flow"),
    # Determines which ActivityEdges will realize the specified flow.
    'realizingActivityEdge': _Ref('realizingActivityEdge', "ActivityEdge", multi=True, lo=0, hi='*', assoc="A_realizingActivityEdge_informationFlow"),
    # Determines which Connectors will realize the specified flow.
    'realizingConnector': _Ref('realizingConnector', "Connector", multi=True, lo=0, hi='*', assoc="A_realizingConnector_informationFlow"),
    # Determines which Messages will realize the specified flow.
    'realizingMessage': _Ref('realizingMessage', "Message", multi=True, lo=0, hi='*', assoc="A_realizingMessage_informationFlow"),
    }
    _UNIONS = {
        "relatedElement": ("informationSource", "informationTarget",),
        "source": ("informationSource",),
        "target": ("informationTarget",),
    }
    CONSTRAINTS = (
        ("must_conform",
         "(no specification serialized)"
        ),
        ("sources_and_targets_kind",
         "(self.informationSource->forAll( sis | oclIsKindOf(Actor) or oclIsKindOf(Node) or oclIsK"
         "indOf(UseCase) or oclIsKindOf(Artifact) or oclIsKindOf(Class) or oclIsKindOf(Component) "
         "or oclIsKindOf(Port) or oclIsKindOf(Property) or oclIsKindOf(Interface) or oclIsKindOf(P"
         "ackage) or oclIsKindOf(ActivityNode) or oclIsKindOf(ActivityPartition) or (oclIsKindOf(I"
         "nstanceSpecification) and not sis.oclAsType(InstanceSpecification).classifier->exists(oc"
         "lIsKindOf(Relationship))))) and (self.informationTarget->forAll( sit | oclIsKindOf(Actor"
         ") or oclIsKindOf(Node) or oclIsKindOf(UseCase) or oclIsKindOf(Artifact) or oclIsKindOf(C"
         "lass) or oclIsKindOf(Component) or oclIsKindOf(Port) or oclIsKindOf(Property) or oclIsKi"
         "ndOf(Interface) or oclIsKindOf(Package) or oclIsKindOf(ActivityNode) or oclIsKindOf(Acti"
         "vityPartition) or (oclIsKindOf(InstanceSpecification) and not sit.oclAsType(InstanceSpec"
         "ification).classifier->exists(oclIsKindOf(Relationship)))))"
        ),
        ("convey_classifiers",
         "self.conveyed->forAll(oclIsKindOf(Class) or oclIsKindOf(Interface) or oclIsKindOf(Inform"
         "ationItem) or oclIsKindOf(Signal) or oclIsKindOf(Component))"
        ),
    )

class InformationItem(Classifier):
    """InformationItems represent many kinds of information that can flow from sources to targets in very abstract ways. They represent the kinds of information that may move within a system, but do not elaborate details of the transferred information. Details of transferred information are the province of other Classifiers that may ultimately define InformationItems. Consequently, InformationItems cannot be instantiated and do not themselves have features, generalizations, or associations. An important use of InformationItems is to represent information during early design stages, possibly before the detailed modeling decisions that will ultimately define them have been made. Another purpose of InformationItems is to abstract portions of complex models in less precise, but perhaps more general and communicable, ways."""
    _PKG = "InformationFlows"
    _DECL = {
    # Determines the classifiers that will specify the structure and nature of the information. An inf
    # ormation item represents all its represented classifiers.
    'represented': _Ref('represented', "Classifier", multi=True, lo=0, hi='*', assoc="A_represented_representation"),
    }
    CONSTRAINTS = (
        ("sources_and_targets",
         "(self.represented->select(oclIsKindOf(InformationItem))->forAll(p | p.conveyingFlow.sour"
         "ce->forAll(q | self.conveyingFlow.source->includes(q)) and p.conveyingFlow.target->forAl"
         "l(q | self.conveyingFlow.target->includes(q)))) and (self.represented->forAll(oclIsKindO"
         "f(Class) or oclIsKindOf(Interface) or oclIsKindOf(InformationItem) or oclIsKindOf(Signal"
         ") or oclIsKindOf(Component)))"
        ),
        ("has_no",
         "self.generalization->isEmpty() and self.feature->isEmpty()"
        ),
        ("not_instantiable",
         "isAbstract"
        ),
    )

class InitialNode(ControlNode):
    """An InitialNode is a ControlNode that offers a single control token when initially enabled."""
    _PKG = "Activities"
    CONSTRAINTS = (
        ("no_incoming_edges",
         "incoming->isEmpty()"
        ),
        ("control_edges",
         "outgoing->forAll(oclIsKindOf(ControlFlow))"
        ),
    )

class InstanceValue(ValueSpecification):
    """An InstanceValue is a ValueSpecification that identifies an instance."""
    _PKG = "Classification"
    _DECL = {
    # The InstanceSpecification that represents the specified value.
    'instance': _Ref('instance', "InstanceSpecification", assoc="A_instance_instanceValue"),
    }

class Interaction(Behavior, InteractionFragment):
    """An Interaction is a unit of Behavior that focuses on the observable exchange of information between connectable elements."""
    _PKG = "Interactions"
    _DECL = {
    # Actions owned by the Interaction.
    'action': _Ref('action', "Action", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_action_interaction"),
    # Specifies the gates that form the message interface between this Interaction and any Interaction
    # Uses which reference it.
    'formalGate': _Ref('formalGate', "Gate", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_formalGate_interaction"),
    # The ordered set of fragments in the Interaction.
    'fragment': _Ref('fragment', "InteractionFragment", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_fragment_enclosingInteraction"),
    # Specifies the participants in this Interaction.
    'lifeline': _Ref('lifeline', "Lifeline", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_lifeline_interaction"),
    # The Messages contained in this Interaction.
    'message': _Ref('message', "Message", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_message_interaction"),
    }
    _UNIONS = {
        "member": ("formalGate", "fragment", "lifeline", "message",),
        "ownedElement": ("action", "formalGate", "fragment", "lifeline", "message",),
        "ownedMember": ("formalGate", "fragment", "lifeline", "message",),
    }
    CONSTRAINTS = (
        ("not_contained",
         "enclosingInteraction->isEmpty()"
        ),
    )

class InteractionConstraint(Constraint):
    """An InteractionConstraint is a Boolean expression that guards an operand in a CombinedFragment."""
    _PKG = "Interactions"
    _DECL = {
    # The maximum number of iterations of a loop
    'maxint': _Ref('maxint', "ValueSpecification", composite=True, subsets=("ownedElement",), assoc="A_maxint_interactionConstraint"),
    # The minimum number of iterations of a loop
    'minint': _Ref('minint', "ValueSpecification", composite=True, subsets=("ownedElement",), assoc="A_minint_interactionConstraint"),
    }
    _UNIONS = {
        "ownedElement": ("maxint", "minint",),
    }
    CONSTRAINTS = (
        ("minint_maxint",
         "maxint->notEmpty() or minint->notEmpty() implies interactionOperand.combinedFragment.int"
         "eractionOperator = InteractionOperatorKind::loop"
        ),
        ("minint_non_negative",
         "minint->notEmpty() implies minint->asSequence()->first().integerValue() >= 0"
        ),
        ("maxint_positive",
         "maxint->notEmpty() implies maxint->asSequence()->first().integerValue() > 0"
        ),
        ("dynamic_variables",
         "(no specification serialized)"
        ),
        ("global_data",
         "(no specification serialized)"
        ),
        ("maxint_greater_equal_minint",
         "maxint->notEmpty() implies (minint->notEmpty() and maxint->asSequence()->first().integer"
         "Value() >= minint->asSequence()->first().integerValue() )"
        ),
    )

class InteractionOperand(InteractionFragment, Namespace):
    """An InteractionOperand is contained in a CombinedFragment. An InteractionOperand represents one operand of the expression given by the enclosing CombinedFragment."""
    _PKG = "Interactions"
    _DECL = {
    # The fragments of the operand.
    'fragment': _Ref('fragment', "InteractionFragment", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_fragment_enclosingOperand"),
    # Constraint of the operand.
    'guard': _Ref('guard', "InteractionConstraint", composite=True, subsets=("ownedElement",), assoc="A_guard_interactionOperand"),
    }
    _UNIONS = {
        "member": ("fragment",),
        "ownedElement": ("fragment", "guard",),
        "ownedMember": ("fragment",),
    }
    CONSTRAINTS = (
        ("guard_contain_references",
         "(no specification serialized)"
        ),
        ("guard_directly_prior",
         "(no specification serialized)"
        ),
    )

class InteractionUse(InteractionFragment):
    """An InteractionUse refers to an Interaction. The InteractionUse is a shorthand for copying the contents of the referenced Interaction where the InteractionUse is. To be accurate the copying must take into account substituting parameters with arguments and connect the formal Gates with the actual ones."""
    _PKG = "Interactions"
    _DECL = {
    # The actual gates of the InteractionUse.
    'actualGate': _Ref('actualGate', "Gate", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_actualGate_interactionUse"),
    # The actual arguments of the Interaction.
    'argument': _Ref('argument', "ValueSpecification", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_argument_interactionUse"),
    # Refers to the Interaction that defines its meaning.
    'refersTo': _Ref('refersTo', "Interaction", assoc="A_refersTo_interactionUse"),
    # The value of the executed Interaction.
    'returnValue': _Ref('returnValue', "ValueSpecification", composite=True, subsets=("ownedElement",), assoc="A_returnValue_interactionUse"),
    # The recipient of the return value.
    'returnValueRecipient': _Ref('returnValueRecipient', "Property", assoc="A_returnValueRecipient_interactionUse"),
    }
    _UNIONS = {
        "ownedElement": ("actualGate", "argument", "returnValue",),
    }
    CONSTRAINTS = (
        ("gates_match",
         "actualGate->notEmpty() implies refersTo.formalGate->forAll( fg : Gate | self.actualGate-"
         ">select(matches(fg))->size()=1) and self.actualGate->forAll(ag : Gate | refersTo.formalG"
         "ate->select(matches(ag))->size()=1)"
        ),
        ("arguments_are_constants",
         "(no specification serialized)"
        ),
        ("returnValueRecipient_coverage",
         "returnValueRecipient->asSet()->notEmpty() implies let covCE : Set(ConnectableElement) = "
         "covered.represents->asSet() in covCE->notEmpty() and let classes:Set(Classifier) = covCE"
         ".type.oclIsKindOf(Classifier).oclAsType(Classifier)->asSet() in let allProps : Set(Prope"
         "rty) = classes.attribute->union(classes.allParents().attribute)->asSet() in allProps->in"
         "cludes(returnValueRecipient)"
        ),
        ("arguments_correspond_to_parameters",
         "(no specification serialized)"
        ),
        ("returnValue_type_recipient_correspondence",
         "returnValue.type->asSequence()->notEmpty() implies returnValue.type->asSequence()->first"
         "() = returnValueRecipient.type->asSequence()->first()"
        ),
        ("all_lifelines",
         "let parentInteraction : Set(Interaction) = enclosingInteraction->asSet()-> union(enclosi"
         "ngOperand.combinedFragment->closure(enclosingOperand.combinedFragment)-> collect(enclosi"
         "ngInteraction).oclAsType(Interaction)->asSet()) in parentInteraction->size()=1 and let r"
         "efInteraction : Interaction = refersTo in parentInteraction.covered-> forAll(intLifeline"
         " : Lifeline | refInteraction.covered-> forAll( refLifeline : Lifeline | refLifeline.repr"
         "esents = intLifeline.represents and ( ( refLifeline.selector.oclIsKindOf(LiteralString) "
         "implies intLifeline.selector.oclIsKindOf(LiteralString) and refLifeline.selector.oclAsTy"
         "pe(LiteralString).value = intLifeline.selector.oclAsType(LiteralString).value ) and ( re"
         "fLifeline.selector.oclIsKindOf(LiteralInteger) implies intLifeline.selector.oclIsKindOf("
         "LiteralInteger) and refLifeline.selector.oclAsType(LiteralInteger).value = intLifeline.s"
         "elector.oclAsType(LiteralInteger).value ) ) implies self.covered->asSet()->includes(intL"
         "ifeline)))"
        ),
    )

class Interface(Classifier):
    """Interfaces declare coherent services that are implemented by BehavioredClassifiers that implement the Interfaces via InterfaceRealizations."""
    _PKG = "SimpleClassifiers"
    _DECL = {
    # References all the Classifiers that are defined (nested) within the Interface.
    'nestedClassifier': _Ref('nestedClassifier', "Classifier", composite=True, multi=True, lo=0, hi='*', subsets=("redefinableElement", "ownedMember",), assoc="A_nestedClassifier_interface"),
    # The attributes (i.e., the Properties) owned by the Interface.
    'ownedAttribute': _Ref('ownedAttribute', "Property", composite=True, multi=True, lo=0, hi='*', subsets=("attribute", "ownedMember",), assoc="A_ownedAttribute_interface"),
    # The Operations owned by the Interface.
    'ownedOperation': _Ref('ownedOperation', "Operation", composite=True, multi=True, lo=0, hi='*', subsets=("redefinableElement", "feature", "ownedMember",), assoc="A_ownedOperation_interface"),
    # Receptions that objects providing this Interface are willing to accept.
    'ownedReception': _Ref('ownedReception', "Reception", composite=True, multi=True, lo=0, hi='*', subsets=("feature", "ownedMember",), assoc="A_ownedReception_interface"),
    # References a ProtocolStateMachine specifying the legal sequences of the invocation of the Behavi
    # oralFeatures described in the Interface.
    'protocol': _Ref('protocol', "ProtocolStateMachine", composite=True, subsets=("ownedMember",), assoc="A_protocol_interface"),
    # References all the Interfaces redefined by this Interface.
    'redefinedInterface': _Ref('redefinedInterface', "Interface", multi=True, lo=0, hi='*', subsets=("redefinedClassifier",), assoc="A_redefinedInterface_interface"),
    }
    _UNIONS = {
        "attribute": ("ownedAttribute",),
        "feature": ("ownedAttribute", "ownedOperation", "ownedReception",),
        "member": ("nestedClassifier", "ownedAttribute", "ownedOperation", "ownedReception", "protocol",),
        "ownedElement": ("nestedClassifier", "ownedAttribute", "ownedOperation", "ownedReception", "protocol",),
        "ownedMember": ("nestedClassifier", "ownedAttribute", "ownedOperation", "ownedReception", "protocol",),
        "redefinableElement": ("nestedClassifier", "ownedAttribute", "ownedOperation",),
        "redefinedElement": ("redefinedInterface",),
    }
    CONSTRAINTS = (
        ("visibility",
         "feature->forAll(visibility = VisibilityKind::public)"
        ),
    )

class InterfaceRealization(Realization):
    """An InterfaceRealization is a specialized realization relationship between a BehavioredClassifier and an Interface. This relationship signifies that the realizing BehavioredClassifier conforms to the contract specified by the Interface."""
    _PKG = "SimpleClassifiers"
    _DECL = {
    # References the Interface specifying the conformance contract.
    'contract': _Ref('contract', "Interface", subsets=("supplier",), assoc="A_contract_interfaceRealization"),
    # References the BehavioredClassifier that owns this InterfaceRealization, i.e., the BehavioredCla
    # ssifier that realizes the Interface to which it refers.
    'implementingClassifier': _Ref('implementingClassifier', "BehavioredClassifier", subsets=("client", "owner",), assoc="A_interfaceRealization_implementingClassifier"),
    }
    _UNIONS = {
        "owner": ("implementingClassifier",),
        "relatedElement": ("contract", "implementingClassifier",),
        "source": ("implementingClassifier",),
        "target": ("contract",),
    }

class InterruptibleActivityRegion(ActivityGroup):
    """An InterruptibleActivityRegion is an ActivityGroup that supports the termination of tokens flowing in the portions of an activity within it."""
    _PKG = "Activities"
    _DECL = {
    # The ActivityEdges leaving the InterruptibleActivityRegion on which a traversing token will resul
    # t in the termination of other tokens flowing in the InterruptibleActivityRegion.
    'interruptingEdge': _Ref('interruptingEdge', "ActivityEdge", multi=True, lo=0, hi='*', assoc="A_interruptingEdge_interrupts"),
    # ActivityNodes immediately contained in the InterruptibleActivityRegion.
    'node': _Ref('node', "ActivityNode", multi=True, lo=0, hi='*', subsets=("containedNode",), assoc="A_inInterruptibleRegion_node"),
    }
    _UNIONS = {
        "containedNode": ("node",),
    }
    CONSTRAINTS = (
        ("interrupting_edges",
         "interruptingEdge->forAll(edge | node->includes(edge.source) and node->excludes(edge.targ"
         "et) and edge.target.containingActivity() = inActivity)"
        ),
    )

class JoinNode(ControlNode):
    """A JoinNode is a ControlNode that synchronizes multiple flows."""
    _PKG = "Activities"
    _DECL = {
    # Indicates whether incoming tokens having objects with the same identity are combined into one by
    #  the JoinNode.
    'isCombineDuplicate': _Ref('isCombineDuplicate', bool),
    # A ValueSpecification giving the condition under which the JoinNode will offer a token on its out
    # going ActivityEdge. If no joinSpec is specified, then the JoinNode will offer an outgoing token 
    # if tokens are offered on all of its incoming ActivityEdges (an "and" condition).
    'joinSpec': _Ref('joinSpec', "ValueSpecification", composite=True, subsets=("ownedElement",), assoc="A_joinSpec_joinNode"),
    }
    _UNIONS = {
        "ownedElement": ("joinSpec",),
    }
    CONSTRAINTS = (
        ("one_outgoing_edge",
         "outgoing->size() = 1"
        ),
        ("incoming_object_flow",
         "if incoming->exists(oclIsKindOf(ObjectFlow)) then outgoing->forAll(oclIsKindOf(ObjectFlo"
         "w)) else outgoing->forAll(oclIsKindOf(ControlFlow)) endif"
        ),
    )

class Lifeline(NamedElement):
    """A Lifeline represents an individual participant in the Interaction. While parts and structural features may have multiplicity greater than 1, Lifelines represent only one interacting entity."""
    _PKG = "Interactions"
    _DECL = {
    # References the InteractionFragments in which this Lifeline takes part.
    'coveredBy': _Ref('coveredBy', "InteractionFragment", multi=True, lo=0, hi='*', assoc="A_covered_coveredBy"),
    # References the Interaction that represents the decomposition.
    'decomposedAs': _Ref('decomposedAs', "PartDecomposition", assoc="A_decomposedAs_lifeline"),
    # References the Interaction enclosing this Lifeline.
    'interaction': _Ref('interaction', "Interaction", subsets=("namespace",), assoc="A_lifeline_interaction"),
    # References the ConnectableElement within the classifier that contains the enclosing interaction.
    'represents': _Ref('represents', "ConnectableElement", assoc="A_represents_lifeline"),
    # If the referenced ConnectableElement is multivalued, then this specifies the specific individual
    #  part within that set.
    'selector': _Ref('selector', "ValueSpecification", composite=True, subsets=("ownedElement",), assoc="A_selector_lifeline"),
    }
    _UNIONS = {
        "memberNamespace": ("interaction",),
        "namespace": ("interaction",),
        "ownedElement": ("selector",),
        "owner": ("interaction",),
    }
    CONSTRAINTS = (
        ("selector_specified",
         "self.selector->notEmpty() = (self.represents.oclIsKindOf(MultiplicityElement) and self.r"
         "epresents.oclAsType(MultiplicityElement).isMultivalued())"
        ),
        ("interaction_uses_share_lifeline",
         "let intUses : Set(InteractionUse) = interaction.interactionUse in intUses->forAll ( iuse"
         " : InteractionUse | let usingInteraction : Set(Interaction) = iuse.enclosingInteraction-"
         ">asSet() ->union( iuse.enclosingOperand.combinedFragment->asSet()->closure(enclosingOper"
         "and.combinedFragment).enclosingInteraction->asSet() ) in let peerUses : Set(InteractionU"
         "se) = usingInteraction.fragment->select(oclIsKindOf(InteractionUse)).oclAsType(Interacti"
         "onUse)->asSet() ->union( usingInteraction.fragment->select(oclIsKindOf(CombinedFragment)"
         ").oclAsType(CombinedFragment)->asSet() ->closure(operand.fragment->select(oclIsKindOf(Co"
         "mbinedFragment)).oclAsType(CombinedFragment)).operand.fragment-> select(oclIsKindOf(Inte"
         "ractionUse)).oclAsType(InteractionUse)->asSet() )->excluding(iuse) in peerUses->forAll( "
         "peerUse : InteractionUse | peerUse.refersTo.lifeline->forAll( l : Lifeline | (l.represen"
         "ts = self.represents and ( self.selector.oclIsKindOf(LiteralString) implies l.selector.o"
         "clIsKindOf(LiteralString) and self.selector.oclAsType(LiteralString).value = l.selector."
         "oclAsType(LiteralString).value ) and ( self.selector.oclIsKindOf(LiteralInteger) implies"
         " l.selector.oclIsKindOf(LiteralInteger) and self.selector.oclAsType(LiteralInteger).valu"
         "e = l.selector.oclAsType(LiteralInteger).value ) ) implies usingInteraction.lifeline->se"
         "lect(represents = self.represents and ( self.selector.oclIsKindOf(LiteralString) implies"
         " l.selector.oclIsKindOf(LiteralString) and self.selector.oclAsType(LiteralString).value "
         "= l.selector.oclAsType(LiteralString).value ) and ( self.selector.oclIsKindOf(LiteralInt"
         "eger) implies l.selector.oclIsKindOf(LiteralInteger) and self.selector.oclAsType(Literal"
         "Integer).value = l.selector.oclAsType(LiteralInteger).value ) ) ) ) )"
        ),
        ("same_classifier",
         "represents.namespace->closure(namespace)->includes(interaction._'context')"
        ),
        ("selector_int_or_string",
         "self.selector->notEmpty() implies self.selector.oclIsKindOf(LiteralInteger) or self.sele"
         "ctor.oclIsKindOf(LiteralString)"
        ),
    )

class LinkEndData(Element):
    """LinkEndData is an Element that identifies on end of a link to be read or written by a LinkAction. As a link (that is not a link object) cannot be passed as a runtime value to or from an Action, it is instead identified by its end objects and qualifier values, if any. A LinkEndData instance provides these values for a single Association end."""
    _PKG = "Actions"
    _DECL = {
    # The Association end for which this LinkEndData specifies values.
    'end': _Ref('end', "Property", assoc="A_end_linkEndData"),
    # A set of QualifierValues used to provide values for the qualifiers of the end.
    'qualifier': _Ref('qualifier', "QualifierValue", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_qualifier_linkEndData"),
    # The InputPin that provides the specified value for the given end. This InputPin is omitted if th
    # e LinkEndData specifies the "open" end for a ReadLinkAction.
    'value': _Ref('value', "InputPin", assoc="A_value_linkEndData"),
    }
    _UNIONS = {
        "ownedElement": ("qualifier",),
    }
    CONSTRAINTS = (
        ("same_type",
         "value<>null implies value.type.conformsTo(end.type)"
        ),
        ("multiplicity",
         "value<>null implies value.is(1,1)"
        ),
        ("end_object_input_pin",
         "value->excludesAll(qualifier.value)"
        ),
        ("property_is_association_end",
         "end.association <> null"
        ),
        ("qualifiers",
         "end.qualifier->includesAll(qualifier.qualifier)"
        ),
    )
    def allPins(self) -> "InputPin":
        """
        Returns all the InputPins referenced by this LinkEndData. By default this includes the value a
        nd qualifier InputPins, but subclasses may override the operation to add other InputPins.
        [LinkEndData operation (query); params: none; returns: "InputPin"; stub - metamodel metadata o
        nly]
        """
        raise NotImplementedError

class LinkEndCreationData(LinkEndData):
    """LinkEndCreationData is LinkEndData used to provide values for one end of a link to be created by a CreateLinkAction."""
    _PKG = "Actions"
    _DECL = {
    # For ordered Association ends, the InputPin that provides the position where the new link should 
    # be inserted or where an existing link should be moved to. The type of the insertAt InputPin is U
    # nlimitedNatural, but the input cannot be zero. It is omitted for Association ends that are not o
    # rdered.
    'insertAt': _Ref('insertAt', "InputPin", assoc="A_insertAt_linkEndCreationData"),
    # Specifies whether the existing links emanating from the object on this end should be destroyed b
    # efore creating a new link.
    'isReplaceAll': _Ref('isReplaceAll', bool),
    }
    CONSTRAINTS = (
        ("insertAt_pin",
         "if not end.isOrdered then insertAt = null else not isReplaceAll=false implies insertAt <"
         "> null and insertAt->forAll(type=UnlimitedNatural and is(1,1)) endif"
        ),
    )
    def allPins(self) -> "InputPin":
        """
        Adds the insertAt InputPin (if any) to the set of all Pins.
        [LinkEndCreationData operation (query); params: none; returns: "InputPin"; stub - metamodel me
        tadata only]
        """
        raise NotImplementedError

class LinkEndDestructionData(LinkEndData):
    """LinkEndDestructionData is LinkEndData used to provide values for one end of a link to be destroyed by a DestroyLinkAction."""
    _PKG = "Actions"
    _DECL = {
    # The InputPin that provides the position of an existing link to be destroyed in an ordered, nonun
    # ique Association end. The type of the destroyAt InputPin is UnlimitedNatural, but the value cann
    # ot be zero or unlimited.
    'destroyAt': _Ref('destroyAt', "InputPin", assoc="A_destroyAt_linkEndDestructionData"),
    # Specifies whether to destroy duplicates of the value in nonunique Association ends.
    'isDestroyDuplicates': _Ref('isDestroyDuplicates', bool),
    }
    CONSTRAINTS = (
        ("destroyAt_pin",
         "if not end.isOrdered or end.isUnique or isDestroyDuplicates then destroyAt = null else d"
         "estroyAt <> null and destroyAt->forAll(type=UnlimitedNatural and is(1,1)) endif"
        ),
    )
    def allPins(self) -> "InputPin":
        """
        Adds the destroyAt InputPin (if any) to the set of all Pins.
        [LinkEndDestructionData operation (query); params: none; returns: "InputPin"; stub - metamodel
         metadata only]
        """
        raise NotImplementedError

class LiteralSpecification(ValueSpecification):
    """A LiteralSpecification identifies a literal constant being modeled."""
    _PKG = "Values"

class LiteralBoolean(LiteralSpecification):
    """A LiteralBoolean is a specification of a Boolean value."""
    _PKG = "Values"
    _DECL = {
    # The specified Boolean value.
    'value': _Ref('value', bool),
    }
    def booleanValue(self) -> bool:
        """
        The query booleanValue() gives the value.
        [LiteralBoolean operation (query); params: none; returns: bool; stub - metamodel metadata only
        ]
        """
        raise NotImplementedError
    def isComputable(self) -> bool:
        """
        The query isComputable() is redefined to be true.
        [LiteralBoolean operation (query); params: none; returns: bool; stub - metamodel metadata only
        ]
        """
        raise NotImplementedError

class LiteralInteger(LiteralSpecification):
    """A LiteralInteger is a specification of an Integer value."""
    _PKG = "Values"
    _DECL = {
    # The specified Integer value.
    'value': _Ref('value', int),
    }
    def integerValue(self) -> int:
        """
        The query integerValue() gives the value.
        [LiteralInteger operation (query); params: none; returns: int; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isComputable(self) -> bool:
        """
        The query isComputable() is redefined to be true.
        [LiteralInteger operation (query); params: none; returns: bool; stub - metamodel metadata only
        ]
        """
        raise NotImplementedError

class LiteralNull(LiteralSpecification):
    """A LiteralNull specifies the lack of a value."""
    _PKG = "Values"
    def isComputable(self) -> bool:
        """
        The query isComputable() is redefined to be true.
        [LiteralNull operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isNull(self) -> bool:
        """
        The query isNull() returns true.
        [LiteralNull operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError

class LiteralReal(LiteralSpecification):
    """A LiteralReal is a specification of a Real value."""
    _PKG = "Values"
    _DECL = {
    # The specified Real value.
    'value': _Ref('value', float),
    }
    def isComputable(self) -> bool:
        """
        The query isComputable() is redefined to be true.
        [LiteralReal operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def realValue(self) -> float:
        """
        The query realValue() gives the value.
        [LiteralReal operation (query); params: none; returns: float; stub - metamodel metadata only]
        """
        raise NotImplementedError

class LiteralString(LiteralSpecification):
    """A LiteralString is a specification of a String value."""
    _PKG = "Values"
    _DECL = {
    # The specified String value.
    'value': _Ref('value', str),
    }
    def isComputable(self) -> bool:
        """
        The query isComputable() is redefined to be true.
        [LiteralString operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def stringValue(self) -> str:
        """
        The query stringValue() gives the value.
        [LiteralString operation (query); params: none; returns: str; stub - metamodel metadata only]
        """
        raise NotImplementedError

class LiteralUnlimitedNatural(LiteralSpecification):
    """A LiteralUnlimitedNatural is a specification of an UnlimitedNatural number."""
    _PKG = "Values"
    _DECL = {
    # The specified UnlimitedNatural value.
    'value': _Ref('value', UnlimitedNatural),
    }
    def isComputable(self) -> bool:
        """
        The query isComputable() is redefined to be true.
        [LiteralUnlimitedNatural operation (query); params: none; returns: bool; stub - metamodel meta
        data only]
        """
        raise NotImplementedError
    def unlimitedValue(self) -> UnlimitedNatural:
        """
        The query unlimitedValue() gives the value.
        [LiteralUnlimitedNatural operation (query); params: none; returns: UnlimitedNatural; stub - me
        tamodel metadata only]
        """
        raise NotImplementedError

class LoopNode(StructuredActivityNode):
    """A LoopNode is a StructuredActivityNode that represents an iterative loop with setup, test, and body sections."""
    _PKG = "Actions"
    _DECL = {
    # The OutputPins on Actions within the bodyPart, the values of which are moved to the loopVariable
    #  OutputPins after the completion of each execution of the bodyPart, before the next iteration of
    #  the loop begins or before the loop exits.
    'bodyOutput': _Ref('bodyOutput', "OutputPin", multi=True, lo=0, hi='*', assoc="A_bodyOutput_loopNode"),
    # The set of ExecutableNodes that perform the repetitive computations of the loop. The bodyPart is
    #  executed as long as the test section produces a true value.
    'bodyPart': _Ref('bodyPart', "ExecutableNode", multi=True, lo=0, hi='*', assoc="A_bodyPart_loopNode"),
    # An OutputPin on an Action in the test section whose Boolean value determines whether to continue
    #  executing the loop bodyPart.
    'decider': _Ref('decider', "OutputPin", assoc="A_decider_loopNode"),
    # If true, the test is performed before the first execution of the bodyPart. If false, the bodyPar
    # t is executed once before the test is performed.
    'isTestedFirst': _Ref('isTestedFirst', bool),
    # A list of OutputPins that hold the values of the loop variables during an execution of the loop.
    #  When the test fails, the values are moved to the result OutputPins of the loop.
    'loopVariable': _Ref('loopVariable', "OutputPin", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_loopVariable_loopNode"),
    # A list of InputPins whose values are moved into the loopVariable Pins before the first iteration
    #  of the loop.
    'loopVariableInput': _Ref('loopVariableInput', "InputPin", composite=True, multi=True, lo=0, hi='*', redefines=("structuredNodeInput",), assoc="A_loopVariableInput_loopNode"),
    # A list of OutputPins that receive the loopVariable values after the last iteration of the loop a
    # nd constitute the output of the LoopNode.
    'result': _Ref('result', "OutputPin", composite=True, multi=True, lo=0, hi='*', redefines=("structuredNodeOutput",), assoc="A_result_loopNode"),
    # The set of ExecutableNodes executed before the first iteration of the loop, in order to initiali
    # ze values or perform other setup computations.
    'setupPart': _Ref('setupPart', "ExecutableNode", multi=True, lo=0, hi='*', assoc="A_setupPart_loopNode"),
    # The set of ExecutableNodes executed in order to provide the test result for the loop.
    'test': _Ref('test', "ExecutableNode", multi=True, lo=0, hi='*', assoc="A_test_loopNode"),
    }
    _UNIONS = {
        "ownedElement": ("loopVariable",),
    }
    CONSTRAINTS = (
        ("result_no_incoming",
         "result.incoming->isEmpty()"
        ),
        ("input_edges",
         "loopVariableInput.outgoing->isEmpty()"
        ),
        ("executable_nodes",
         "setupPart->union(test)->union(bodyPart)=node->select(oclIsKindOf(ExecutableNode)).oclAsT"
         "ype(ExecutableNode)->asSet()"
        ),
        ("body_output_pins",
         "bodyPart.oclAsType(Action).allActions().output->includesAll(bodyOutput)"
        ),
        ("setup_test_and_body",
         "setupPart->intersection(test)->isEmpty() and setupPart->intersection(bodyPart)->isEmpty("
         ") and test->intersection(bodyPart)->isEmpty()"
        ),
        ("matching_output_pins",
         "bodyOutput->size()=loopVariable->size() and Sequence{1..loopVariable->size()}->forAll(i "
         "| bodyOutput->at(i).type.conformsTo(loopVariable->at(i).type) and bodyOutput->at(i).isOr"
         "dered = loopVariable->at(i).isOrdered and bodyOutput->at(i).isUnique = loopVariable->at("
         "i).isUnique and loopVariable->at(i).includesMultiplicity(bodyOutput->at(i)))"
        ),
        ("matching_loop_variables",
         "loopVariableInput->size()=loopVariable->size() and loopVariableInput.type=loopVariable.t"
         "ype and loopVariableInput.isUnique=loopVariable.isUnique and loopVariableInput.lower=loo"
         "pVariable.lower and loopVariableInput.upper=loopVariable.upper"
        ),
        ("matching_result_pins",
         "result->size()=loopVariable->size() and result.type=loopVariable.type and result.isUniqu"
         "e=loopVariable.isUnique and result.lower=loopVariable.lower and result.upper=loopVariabl"
         "e.upper"
        ),
        ("loop_variable_outgoing",
         "allOwnedNodes()->includesAll(loopVariable.outgoing.target)"
        ),
    )
    def allActions(self) -> "Action":
        """
        Return only this LoopNode. This prevents Actions within the LoopNode from having their OutputP
        ins used as bodyOutputs or decider Pins in containing LoopNodes or ConditionalNodes.
        [LoopNode operation (query); params: none; returns: "Action"; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def sourceNodes(self) -> "ActivityNode":
        """
        Return the loopVariable OutputPins in addition to other source nodes for the LoopNode as a Str
        ucturedActivityNode.
        [LoopNode operation (query); params: none; returns: "ActivityNode"; stub - metamodel metadata 
        only]
        """
        raise NotImplementedError

class Manifestation(Abstraction):
    """A manifestation is the concrete physical rendering of one or more model elements by an artifact."""
    _PKG = "Deployments"
    _DECL = {
    # The model element that is utilized in the manifestation in an Artifact.
    'utilizedElement': _Ref('utilizedElement', "PackageableElement", subsets=("supplier",), assoc="A_utilizedElement_manifestation"),
    }
    _UNIONS = {
        "relatedElement": ("utilizedElement",),
        "target": ("utilizedElement",),
    }

class MergeNode(ControlNode):
    """A merge node is a control node that brings together multiple alternate flows. It is not used to synchronize concurrent flows but to accept one among several alternate flows."""
    _PKG = "Activities"
    CONSTRAINTS = (
        ("one_outgoing_edge",
         "outgoing->size()=1"
        ),
        ("edges",
         "let allEdges : Set(ActivityEdge) = incoming->union(outgoing) in allEdges->forAll(oclIsKi"
         "ndOf(ControlFlow)) or allEdges->forAll(oclIsKindOf(ObjectFlow))"
        ),
    )

class Message(NamedElement):
    """A Message defines a particular communication between Lifelines of an Interaction."""
    _PKG = "Interactions"
    _DECL = {
    # The arguments of the Message.
    'argument': _Ref('argument', "ValueSpecification", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_argument_message"),
    # The Connector on which this Message is sent.
    'connector': _Ref('connector', "Connector", assoc="A_connector_message"),
    # The enclosing Interaction owning the Message.
    'interaction': _Ref('interaction', "Interaction", subsets=("namespace",), assoc="A_message_interaction"),
    # The derived kind of the Message (complete, lost, found, or unknown).
    'messageKind': _Ref('messageKind', MessageKind, derived=True, readonly=True),
    # The sort of communication reflected by the Message.
    'messageSort': _Ref('messageSort', MessageSort),
    # References the Receiving of the Message.
    'receiveEvent': _Ref('receiveEvent', "MessageEnd", subsets=("messageEnd",), assoc="A_receiveEvent_endMessage"),
    # References the Sending of the Message.
    'sendEvent': _Ref('sendEvent', "MessageEnd", subsets=("messageEnd",), assoc="A_sendEvent_endMessage"),
    # The signature of the Message is the specification of its content. It refers either an Operation 
    # or a Signal.
    'signature': _Ref('signature', "NamedElement", assoc="A_signature_message"),
    }
    _UNIONS = {
        "memberNamespace": ("interaction",),
        "namespace": ("interaction",),
        "ownedElement": ("argument",),
        "owner": ("interaction",),
    }
    CONSTRAINTS = (
        ("sending_receiving_message_event",
         "receiveEvent.oclIsKindOf(MessageOccurrenceSpecification) implies let f : Lifeline = send"
         "Event->select(oclIsKindOf(MessageOccurrenceSpecification)).oclAsType(MessageOccurrenceSp"
         "ecification)->asOrderedSet()->first().covered in f = receiveEvent->select(oclIsKindOf(Me"
         "ssageOccurrenceSpecification)).oclAsType(MessageOccurrenceSpecification)->asOrderedSet()"
         "->first().covered implies f.events->indexOf(sendEvent.oclAsType(MessageOccurrenceSpecifi"
         "cation)->asOrderedSet()->first() ) < f.events->indexOf(receiveEvent.oclAsType(MessageOcc"
         "urrenceSpecification)->asOrderedSet()->first() )"
        ),
        ("arguments",
         "(no specification serialized)"
        ),
        ("cannot_cross_boundaries",
         "sendEvent->notEmpty() and receiveEvent->notEmpty() implies let sendEnclosingFrag : Set(I"
         "nteractionFragment) = sendEvent->asOrderedSet()->first().enclosingFragment() in let rece"
         "iveEnclosingFrag : Set(InteractionFragment) = receiveEvent->asOrderedSet()->first().encl"
         "osingFragment() in sendEnclosingFrag = receiveEnclosingFrag"
        ),
        ("signature_is_signal",
         "(messageSort = MessageSort::asynchSignal ) and signature.oclIsKindOf(Signal) implies let"
         " signalAttributes : OrderedSet(Property) = signature.oclAsType(Signal).inheritedMember()"
         "-> select(n:NamedElement | n.oclIsTypeOf(Property))->collect(oclAsType(Property))->asOrd"
         "eredSet() in signalAttributes->size() = self.argument->size() and self.argument->forAll("
         " o: ValueSpecification | not (o.oclIsKindOf(Expression) and o.oclAsType(Expression).symb"
         "ol->size()=0 and o.oclAsType(Expression).operand->isEmpty() ) implies let p : Property ="
         " signalAttributes->at(self.argument->indexOf(o)) in o.type.oclAsType(Classifier).conform"
         "sTo(p.type.oclAsType(Classifier)))"
        ),
        ("occurrence_specifications",
         "(no specification serialized)"
        ),
        ("signature_refer_to",
         "signature->notEmpty() implies ((signature.oclIsKindOf(Operation) and (messageSort = Mess"
         "ageSort::asynchCall or messageSort = MessageSort::synchCall or messageSort = MessageSort"
         "::reply) ) or (signature.oclIsKindOf(Signal) and messageSort = MessageSort::asynchSignal"
         " ) ) and name = signature.name"
        ),
        ("signature_is_operation_request",
         "(messageSort = MessageSort::asynchCall or messageSort = MessageSort::synchCall) and sign"
         "ature.oclIsKindOf(Operation) implies let requestParms : OrderedSet(Parameter) = signatur"
         "e.oclAsType(Operation).ownedParameter-> select(direction = ParameterDirectionKind::inout"
         " or direction = ParameterDirectionKind::_'in' ) in requestParms->size() = self.argument-"
         ">size() and self.argument->forAll( o: ValueSpecification | not (o.oclIsKindOf(Expression"
         ") and o.oclAsType(Expression).symbol->size()=0 and o.oclAsType(Expression).operand->isEm"
         "pty() ) implies let p : Parameter = requestParms->at(self.argument->indexOf(o)) in o.typ"
         "e.oclAsType(Classifier).conformsTo(p.type.oclAsType(Classifier)) )"
        ),
        ("signature_is_operation_reply",
         "(messageSort = MessageSort::reply) and signature.oclIsKindOf(Operation) implies let repl"
         "yParms : OrderedSet(Parameter) = signature.oclAsType(Operation).ownedParameter-> select("
         "direction = ParameterDirectionKind::inout or direction = ParameterDirectionKind::out or "
         "direction = ParameterDirectionKind::return) in replyParms->size() = self.argument->size("
         ") and self.argument->forAll( o: ValueSpecification | o.oclIsKindOf(Expression) and let e"
         " : Expression = o.oclAsType(Expression) in e.operand->notEmpty() implies let p : Paramet"
         "er = replyParms->at(self.argument->indexOf(o)) in e.operand->asSequence()->first().type."
         "oclAsType(Classifier).conformsTo(p.type.oclAsType(Classifier)) )"
        ),
    )
    def messageKind(self) -> MessageKind:
        """
        This query returns the MessageKind value for this Message.
        [Message operation (query); params: none; returns: MessageKind; stub - metamodel metadata only
        ]
        """
        raise NotImplementedError
    def isDistinguishableFrom(self, n: "NamedElement" = None, ns: "Namespace" = None) -> bool:
        """
        The query isDistinguishableFrom() specifies that any two Messages may coexist in the same Name
        space, regardless of their names.
        [Message operation (query); params: n: "NamedElement", ns: "Namespace"; returns: bool; stub - 
        metamodel metadata only]
        """
        raise NotImplementedError

class Package(PackageableElement, Namespace, TemplateableElement):
    """A package can have one or more profile applications to indicate which profiles have been applied. Because a profile is a package, it is possible to apply a profile not only to packages, but also to profiles. Package specializes TemplateableElement and PackageableElement specializes ParameterableElement to specify that a package can be used as a template and a PackageableElement as a template parameter. A package is used to group elements, and provides a namespace for the grouped elements."""
    _PKG = "Packages"
    _DECL = {
    # Provides an identifier for the package that can be used for many purposes. A URI is the universa
    # lly unique identification of the package following the IETF URI specification, RFC 2396 http://w
    # ww.ietf.org/rfc/rfc2396.txt and it must comply with those syntax rules.
    'URI': _Ref('URI', str),
    # References the packaged elements that are Packages.
    'nestedPackage': _Ref('nestedPackage', "Package", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("packagedElement",), assoc="A_nestedPackage_nestingPackage"),
    # References the Package that owns this Package.
    'nestingPackage': _Ref('nestingPackage', "Package", subsets=("owningPackage",), assoc="A_nestedPackage_nestingPackage"),
    # References the Stereotypes that are owned by the Package.
    'ownedStereotype': _Ref('ownedStereotype', "Stereotype", derived=True, composite=True, readonly=True, multi=True, lo=0, hi='*', subsets=("packagedElement",), assoc="A_ownedStereotype_owningPackage"),
    # References the packaged elements that are Types.
    'ownedType': _Ref('ownedType', "Type", derived=True, composite=True, multi=True, lo=0, hi='*', subsets=("packagedElement",), assoc="A_ownedType_package"),
    # References the PackageMerges that are owned by this Package.
    'packageMerge': _Ref('packageMerge', "PackageMerge", composite=True, multi=True, lo=0, hi='*', subsets=("directedRelationship", "ownedElement",), assoc="A_packageMerge_receivingPackage"),
    # Specifies the packageable elements that are owned by this Package.
    'packagedElement': _Ref('packagedElement', "PackageableElement", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_packagedElement_owningPackage"),
    # References the ProfileApplications that indicate which profiles have been applied to the Package
    # .
    'profileApplication': _Ref('profileApplication', "ProfileApplication", composite=True, multi=True, lo=0, hi='*', subsets=("directedRelationship", "ownedElement",), assoc="A_profileApplication_applyingPackage"),
    }
    _UNIONS = {
        "directedRelationship": ("packageMerge", "profileApplication",),
        "member": ("nestedPackage", "ownedStereotype", "ownedType", "packagedElement",),
        "memberNamespace": ("nestingPackage",),
        "namespace": ("nestingPackage",),
        "ownedElement": ("nestedPackage", "ownedStereotype", "ownedType", "packageMerge", "packagedElement", "profileApplication",),
        "ownedMember": ("nestedPackage", "ownedStereotype", "ownedType", "packagedElement",),
        "owner": ("nestingPackage",),
        "relationship": ("packageMerge", "profileApplication",),
    }
    CONSTRAINTS = (
        ("elements_public_or_private",
         "packagedElement->forAll(e | e.visibility<> null implies e.visibility = VisibilityKind::p"
         "ublic or e.visibility = VisibilityKind::private)"
        ),
    )
    def allApplicableStereotypes(self) -> "Stereotype":
        """
        The query allApplicableStereotypes() returns all the directly or indirectly owned stereotypes,
         including stereotypes contained in sub-profiles.
        [Package operation (query); params: none; returns: "Stereotype"; stub - metamodel metadata onl
        y]
        """
        raise NotImplementedError
    def containingProfile(self) -> "Profile":
        """
        The query containingProfile() returns the closest profile directly or indirectly containing th
        is package (or this package itself, if it is a profile).
        [Package operation (query); params: none; returns: "Profile"; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def makesVisible(self, el: "NamedElement" = None) -> bool:
        """
        The query makesVisible() defines whether a Package makes an element visible outside itself. El
        ements with no visibility and elements with public visibility are made visible.
        [Package operation (query); params: el: "NamedElement"; returns: bool; stub - metamodel metada
        ta only]
        """
        raise NotImplementedError
    def mustBeOwned(self) -> bool:
        """
        The query mustBeOwned() indicates whether elements of this type must have an owner.
        [Package operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def nestedPackage(self) -> "Package":
        """
        Derivation for Package::/nestedPackage
        [Package operation (query); params: none; returns: "Package"; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def ownedStereotype(self) -> "Stereotype":
        """
        Derivation for Package::/ownedStereotype
        [Package operation (query); params: none; returns: "Stereotype"; stub - metamodel metadata onl
        y]
        """
        raise NotImplementedError
    def ownedType(self) -> "Type":
        """
        Derivation for Package::/ownedType
        [Package operation (query); params: none; returns: "Type"; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def visibleMembers(self) -> "PackageableElement":
        """
        The query visibleMembers() defines which members of a Package can be accessed outside it.
        [Package operation (query); params: none; returns: "PackageableElement"; stub - metamodel meta
        data only]
        """
        raise NotImplementedError

class Model(Package):
    """A model captures a view of a physical system. It is an abstraction of the physical system, with a certain purpose. This purpose determines what is to be included in the model and what is irrelevant. Thus the model completely describes those aspects of the physical system that are relevant to the purpose of the model, at the appropriate level of detail."""
    _PKG = "Packages"
    _DECL = {
    # The name of the viewpoint that is expressed by a model (this name may refer to a profile definit
    # ion).
    'viewpoint': _Ref('viewpoint', str),
    }

class ObjectFlow(ActivityEdge):
    """An ObjectFlow is an ActivityEdge that is traversed by object tokens that may hold values. Object flows also support multicast/receive, token selection from object nodes, and transformation of tokens."""
    _PKG = "Activities"
    _DECL = {
    # Indicates whether the objects in the ObjectFlow are passed by multicasting.
    'isMulticast': _Ref('isMulticast', bool),
    # Indicates whether the objects in the ObjectFlow are gathered from respondents to multicasting.
    'isMultireceive': _Ref('isMultireceive', bool),
    # A Behavior used to select tokens from a source ObjectNode.
    'selection': _Ref('selection', "Behavior", assoc="A_selection_objectFlow"),
    # A Behavior used to change or replace object tokens flowing along the ObjectFlow.
    'transformation': _Ref('transformation', "Behavior", assoc="A_transformation_objectFlow"),
    }
    CONSTRAINTS = (
        ("input_and_output_parameter",
         "selection<>null implies selection.inputParameters()->size()=1 and selection.inputParamet"
         "ers()->forAll(not isUnique and is(0,*)) and selection.outputParameters()->size()=1"
        ),
        ("no_executable_nodes",
         "not (source.oclIsKindOf(ExecutableNode) or target.oclIsKindOf(ExecutableNode))"
        ),
        ("transformation_behavior",
         "transformation<>null implies transformation.inputParameters()->size()=1 and transformati"
         "on.outputParameters()->size()=1"
        ),
        ("selection_behavior",
         "selection<>null implies source.oclIsKindOf(ObjectNode)"
        ),
        ("compatible_types",
         "(no specification serialized)"
        ),
        ("same_upper_bounds",
         "(no specification serialized)"
        ),
        ("target",
         "(no specification serialized)"
        ),
        ("is_multicast_or_is_multireceive",
         "not (isMulticast and isMultireceive)"
        ),
    )

class OpaqueAction(Action):
    """An OpaqueAction is an Action whose functionality is not specified within UML."""
    _PKG = "Actions"
    _DECL = {
    # Provides a textual specification of the functionality of the Action, in one or more languages ot
    # her than UML.
    'body': _Ref('body', str, multi=True, lo=0, hi='*'),
    # The InputPins providing inputs to the OpaqueAction.
    'inputValue': _Ref('inputValue', "InputPin", composite=True, multi=True, lo=0, hi='*', subsets=("input",), assoc="A_inputValue_opaqueAction"),
    # If provided, a specification of the language used for each of the body Strings.
    'language': _Ref('language', str, multi=True, lo=0, hi='*'),
    # The OutputPins on which the OpaqueAction provides outputs.
    'outputValue': _Ref('outputValue', "OutputPin", composite=True, multi=True, lo=0, hi='*', subsets=("output",), assoc="A_outputValue_opaqueAction"),
    }
    _UNIONS = {
        "input": ("inputValue",),
        "output": ("outputValue",),
        "ownedElement": ("inputValue", "outputValue",),
    }
    CONSTRAINTS = (
        ("language_body_size",
         "language->notEmpty() implies (_'body'->size() = language->size())"
        ),
    )

class OpaqueExpression(ValueSpecification):
    """An OpaqueExpression is a ValueSpecification that specifies the computation of a collection of values either in terms of a UML Behavior or based on a textual statement in a language other than UML"""
    _PKG = "Values"
    _DECL = {
    # Specifies the behavior of the OpaqueExpression as a UML Behavior.
    'behavior': _Ref('behavior', "Behavior", assoc="A_behavior_opaqueExpression"),
    # A textual definition of the behavior of the OpaqueExpression, possibly in multiple languages.
    'body': _Ref('body', str, multi=True, lo=0, hi='*'),
    # Specifies the languages used to express the textual bodies of the OpaqueExpression. Languages ar
    # e matched to body Strings by order. The interpretation of the body depends on the languages. If 
    # the languages are unspecified, they may be implicit from the expression body or the context.
    'language': _Ref('language', str, multi=True, lo=0, hi='*'),
    # If an OpaqueExpression is specified using a UML Behavior, then this refers to the single require
    # d return Parameter of that Behavior. When the Behavior completes execution, the values on this P
    # arameter give the result of evaluating the OpaqueExpression.
    'result': _Ref('result', "Parameter", derived=True, readonly=True, assoc="A_result_opaqueExpression"),
    }
    CONSTRAINTS = (
        ("language_body_size",
         "language->notEmpty() implies (_'body'->size() = language->size())"
        ),
        ("one_return_result_parameter",
         "behavior <> null implies behavior.ownedParameter->select(direction=ParameterDirectionKin"
         "d::return)->size() = 1"
        ),
        ("only_in_or_return_parameters",
         "behavior <> null implies behavior.ownedParameter->forAll(not isStream and (direction=Par"
         "ameterDirectionKind::in or direction=ParameterDirectionKind::return))"
        ),
    )
    def isIntegral(self) -> bool:
        """
        The query isIntegral() tells whether an expression is intended to produce an Integer.
        [OpaqueExpression operation (query); params: none; returns: bool; stub - metamodel metadata on
        ly]
        """
        raise NotImplementedError
    def isNonNegative(self) -> bool:
        """
        The query isNonNegative() tells whether an integer expression has a non-negative value.
        [OpaqueExpression operation (query); params: none; returns: bool; stub - metamodel metadata on
        ly]
        """
        raise NotImplementedError
    def isPositive(self) -> bool:
        """
        The query isPositive() tells whether an integer expression has a positive value.
        [OpaqueExpression operation (query); params: none; returns: bool; stub - metamodel metadata on
        ly]
        """
        raise NotImplementedError
    def result(self) -> "Parameter":
        """
        Derivation for OpaqueExpression::/result
        [OpaqueExpression operation (query); params: none; returns: "Parameter"; stub - metamodel meta
        data only]
        """
        raise NotImplementedError
    def value(self) -> int:
        """
        The query value() gives an integer value for an expression intended to produce one.
        [OpaqueExpression operation (query); params: none; returns: int; stub - metamodel metadata onl
        y]
        """
        raise NotImplementedError

class Operation(BehavioralFeature, TemplateableElement, ParameterableElement):
    """An Operation is a BehavioralFeature of a Classifier that specifies the name, type, parameters, and constraints for invoking an associated Behavior. An Operation may invoke both the execution of method behaviors as well as other behavioral responses. Operation specializes TemplateableElement in order to support specification of template operations and bound operations. Operation specializes ParameterableElement to specify that an operation can be exposed as a formal template parameter, and provided as an actual parameter in a binding of a template."""
    _PKG = "Classification"
    _DECL = {
    # An optional Constraint on the result values of an invocation of this Operation.
    'bodyCondition': _Ref('bodyCondition', "Constraint", composite=True, subsets=("ownedRule",), assoc="A_bodyCondition_bodyContext"),
    # The Class that owns this operation, if any.
    'class_': _Ref('class', "Class", subsets=("featuringClassifier", "namespace", "redefinitionContext",), assoc="A_ownedOperation_class"),
    # The DataType that owns this Operation, if any.
    'datatype': _Ref('datatype', "DataType", subsets=("featuringClassifier", "namespace", "redefinitionContext",), assoc="A_ownedOperation_datatype"),
    # The Interface that owns this Operation, if any.
    'interface': _Ref('interface', "Interface", subsets=("featuringClassifier", "namespace", "redefinitionContext",), assoc="A_ownedOperation_interface"),
    # Specifies whether the return parameter is ordered or not, if present. This information is derive
    # d from the return result for this Operation.
    'isOrdered': _Ref('isOrdered', bool, derived=True, readonly=True),
    # Specifies whether an execution of the BehavioralFeature leaves the state of the system unchanged
    #  (isQuery=true) or whether side effects may occur (isQuery=false).
    'isQuery': _Ref('isQuery', bool),
    # Specifies whether the return parameter is unique or not, if present. This information is derived
    #  from the return result for this Operation.
    'isUnique': _Ref('isUnique', bool, derived=True, readonly=True),
    # Specifies the lower multiplicity of the return parameter, if present. This information is derive
    # d from the return result for this Operation.
    'lower': _Ref('lower', int, derived=True, readonly=True),
    # The parameters owned by this Operation.
    'ownedParameter': _Ref('ownedParameter', "Parameter", composite=True, multi=True, lo=0, hi='*', redefines=("ownedParameter",), assoc="A_ownedParameter_operation"),
    # An optional set of Constraints specifying the state of the system when the Operation is complete
    # d.
    'postcondition': _Ref('postcondition', "Constraint", composite=True, multi=True, lo=0, hi='*', subsets=("ownedRule",), assoc="A_postcondition_postContext"),
    # An optional set of Constraints on the state of the system when the Operation is invoked.
    'precondition': _Ref('precondition', "Constraint", composite=True, multi=True, lo=0, hi='*', subsets=("ownedRule",), assoc="A_precondition_preContext"),
    # The Types representing exceptions that may be raised during an invocation of this operation.
    'raisedException': _Ref('raisedException', "Type", multi=True, lo=0, hi='*', redefines=("raisedException",), assoc="A_raisedException_operation"),
    # The Operations that are redefined by this Operation.
    'redefinedOperation': _Ref('redefinedOperation', "Operation", multi=True, lo=0, hi='*', subsets=("redefinedElement",), assoc="A_redefinedOperation_operation"),
    # The OperationTemplateParameter that exposes this element as a formal parameter.
    'templateParameter': _Ref('templateParameter', "OperationTemplateParameter", redefines=("templateParameter",), assoc="A_operation_templateParameter_parameteredElement"),
    # The return type of the operation, if present. This information is derived from the return result
    #  for this Operation.
    'type': _Ref('type', "Type", derived=True, readonly=True, assoc="A_type_operation"),
    # The upper multiplicity of the return parameter, if present. This information is derived from the
    #  return result for this Operation.
    'upper': _Ref('upper', UnlimitedNatural, derived=True, readonly=True),
    }
    _UNIONS = {
        "featuringClassifier": ("class_", "datatype", "interface",),
        "member": ("bodyCondition", "postcondition", "precondition",),
        "memberNamespace": ("class_", "datatype", "interface",),
        "namespace": ("class_", "datatype", "interface",),
        "ownedElement": ("bodyCondition", "postcondition", "precondition",),
        "ownedMember": ("bodyCondition", "postcondition", "precondition",),
        "owner": ("class_", "datatype", "interface",),
        "redefinedElement": ("redefinedOperation",),
        "redefinitionContext": ("class_", "datatype", "interface",),
    }
    CONSTRAINTS = (
        ("at_most_one_return",
         "self.ownedParameter->select(direction = ParameterDirectionKind::return)->size() <= 1"
        ),
        ("only_body_for_query",
         "bodyCondition <> null implies isQuery"
        ),
    )
    def isConsistentWith(self, redefiningElement: "RedefinableElement" = None) -> bool:
        """
        The query isConsistentWith() specifies, for any two Operations in a context in which redefinit
        ion is possible, whether redefinition would be consistent. A redefining operation is consisten
        t with a redefined operation if it has the same number of owned parameters, and for each param
        eter the following holds: - Direction, ordering and uniqueness are the same. - The correspondi
        ng types are covariant, contravariant or invariant. - The multiplicities are compatible, depen
        ding on the parameter direction.
        [Operation operation (query); params: redefiningElement: "RedefinableElement"; returns: bool; 
        stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isOrdered(self) -> bool:
        """
        If this operation has a return parameter, isOrdered equals the value of isOrdered for that par
        ameter. Otherwise isOrdered is false.
        [Operation operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isUnique(self) -> bool:
        """
        If this operation has a return parameter, isUnique equals the value of isUnique for that param
        eter. Otherwise isUnique is true.
        [Operation operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def lower(self) -> int:
        """
        If this operation has a return parameter, lower equals the value of lower for that parameter. 
        Otherwise lower has no value.
        [Operation operation (query); params: none; returns: int; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def returnResult(self) -> "Parameter":
        """
        The query returnResult() returns the set containing the return parameter of the Operation if o
        ne exists, otherwise, it returns an empty set
        [Operation operation (query); params: none; returns: "Parameter"; stub - metamodel metadata on
        ly]
        """
        raise NotImplementedError
    def type(self) -> "Type":
        """
        If this operation has a return parameter, type equals the value of type for that parameter. Ot
        herwise type has no value.
        [Operation operation (query); params: none; returns: "Type"; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def upper(self) -> UnlimitedNatural:
        """
        If this operation has a return parameter, upper equals the value of upper for that parameter. 
        Otherwise upper has no value.
        [Operation operation (query); params: none; returns: UnlimitedNatural; stub - metamodel metada
        ta only]
        """
        raise NotImplementedError

class OperationTemplateParameter(TemplateParameter):
    """An OperationTemplateParameter exposes an Operation as a formal parameter for a template."""
    _PKG = "Classification"
    _DECL = {
    # The Operation exposed by this OperationTemplateParameter.
    'parameteredElement': _Ref('parameteredElement', "Operation", redefines=("parameteredElement",), assoc="A_operation_templateParameter_parameteredElement"),
    }
    CONSTRAINTS = (
        ("match_default_signature",
         "default->notEmpty() implies (default.oclIsKindOf(Operation) and (let defaultOp : Operati"
         "on = default.oclAsType(Operation) in defaultOp.ownedParameter->size() = parameteredEleme"
         "nt.ownedParameter->size() and Sequence{1.. defaultOp.ownedParameter->size()}->forAll( ix"
         " | let p1: Parameter = defaultOp.ownedParameter->at(ix), p2 : Parameter = parameteredEle"
         "ment.ownedParameter->at(ix) in p1.type = p2.type and p1.upper = p2.upper and p1.lower = "
         "p2.lower and p1.direction = p2.direction and p1.isOrdered = p2.isOrdered and p1.isUnique"
         " = p2.isUnique)))"
        ),
    )

class OutputPin(Pin):
    """An OutputPin is a Pin that holds output values produced by an Action."""
    _PKG = "Actions"
    CONSTRAINTS = (
        ("incoming_edges_structured_only",
         "incoming->notEmpty() implies action<>null and action.oclIsKindOf(StructuredActivityNode)"
         " and action.oclAsType(StructuredActivityNode).allOwnedNodes()->includesAll(incoming.sour"
         "ce)"
        ),
    )

class PackageImport(DirectedRelationship):
    """A PackageImport is a Relationship that imports all the non-private members of a Package into the Namespace owning the PackageImport, so that those Elements may be referred to by their unqualified names in the importingNamespace."""
    _PKG = "CommonStructure"
    _DECL = {
    # Specifies the Package whose members are imported into a Namespace.
    'importedPackage': _Ref('importedPackage', "Package", subsets=("target",), assoc="A_importedPackage_packageImport"),
    # Specifies the Namespace that imports the members from a Package.
    'importingNamespace': _Ref('importingNamespace', "Namespace", subsets=("source", "owner",), assoc="A_packageImport_importingNamespace"),
    # Specifies the visibility of the imported PackageableElements within the importingNamespace, i.e.
    # , whether imported Elements will in turn be visible to other Namespaces. If the PackageImport is
    #  public, the imported Elements will be visible outside the importingNamespace, while, if the Pac
    # kageImport is private, they will not.
    'visibility': _Ref('visibility', VisibilityKind),
    }
    _UNIONS = {
        "owner": ("importingNamespace",),
        "relatedElement": ("importedPackage", "importingNamespace",),
        "source": ("importingNamespace",),
        "target": ("importedPackage",),
    }
    CONSTRAINTS = (
        ("public_or_private",
         "visibility = VisibilityKind::public or visibility = VisibilityKind::private"
        ),
    )

class PackageMerge(DirectedRelationship):
    """A package merge defines how the contents of one package are extended by the contents of another package."""
    _PKG = "Packages"
    _DECL = {
    # References the Package that is to be merged with the receiving package of the PackageMerge.
    'mergedPackage': _Ref('mergedPackage', "Package", subsets=("target",), assoc="A_mergedPackage_packageMerge"),
    # References the Package that is being extended with the contents of the merged package of the Pac
    # kageMerge.
    'receivingPackage': _Ref('receivingPackage', "Package", subsets=("source", "owner",), assoc="A_packageMerge_receivingPackage"),
    }
    _UNIONS = {
        "owner": ("receivingPackage",),
        "relatedElement": ("mergedPackage", "receivingPackage",),
        "source": ("receivingPackage",),
        "target": ("mergedPackage",),
    }

class Parameter(ConnectableElement, MultiplicityElement):
    """A Parameter is a specification of an argument used to pass information into or out of an invocation of a BehavioralFeature. Parameters can be treated as ConnectableElements within Collaborations."""
    _PKG = "Classification"
    _DECL = {
    # A String that represents a value to be used when no argument is supplied for the Parameter.
    'default': _Ref('default', str, derived=True),
    # Specifies a ValueSpecification that represents a value to be used when no argument is supplied f
    # or the Parameter.
    'defaultValue': _Ref('defaultValue', "ValueSpecification", composite=True, subsets=("ownedElement",), assoc="A_defaultValue_owningParameter"),
    # Indicates whether a parameter is being sent into or out of a behavioral element.
    'direction': _Ref('direction', ParameterDirectionKind),
    # Specifies the effect that executions of the owner of the Parameter have on objects passed in or 
    # out of the parameter.
    'effect': _Ref('effect', ParameterEffectKind),
    # Tells whether an output parameter may emit a value to the exclusion of the other outputs.
    'isException': _Ref('isException', bool),
    # Tells whether an input parameter may accept values while its behavior is executing, or whether a
    # n output parameter may post values while the behavior is executing.
    'isStream': _Ref('isStream', bool),
    # The Operation owning this parameter.
    'operation': _Ref('operation', "Operation", subsets=("ownerFormalParam",), assoc="A_ownedParameter_operation"),
    # The ParameterSets containing the parameter. See ParameterSet.
    'parameterSet': _Ref('parameterSet', "ParameterSet", multi=True, lo=0, hi='*', assoc="A_parameterSet_parameter"),
    }
    _UNIONS = {
        "memberNamespace": ("operation",),
        "namespace": ("operation",),
        "ownedElement": ("defaultValue",),
        "owner": ("operation",),
    }
    CONSTRAINTS = (
        ("in_and_out",
         "(effect = ParameterEffectKind::delete implies (direction = ParameterDirectionKind::_'in'"
         " or direction = ParameterDirectionKind::inout)) and (effect = ParameterEffectKind::creat"
         "e implies (direction = ParameterDirectionKind::out or direction = ParameterDirectionKind"
         "::inout or direction = ParameterDirectionKind::return))"
        ),
        ("not_exception",
         "isException implies (direction <> ParameterDirectionKind::_'in' and direction <> Paramet"
         "erDirectionKind::inout)"
        ),
        ("connector_end",
         "end->notEmpty() implies collaboration->notEmpty()"
        ),
        ("reentrant_behaviors",
         "(isStream and behavior <> null) implies not behavior.isReentrant"
        ),
        ("stream_and_exception",
         "not (isException and isStream)"
        ),
        ("object_effect",
         "(type.oclIsKindOf(DataType)) implies (effect = null)"
        ),
    )
    def default(self) -> str:
        """
        Derivation for Parameter::/default
        [Parameter operation (query); params: none; returns: str; stub - metamodel metadata only]
        """
        raise NotImplementedError

class ParameterSet(NamedElement):
    """A ParameterSet designates alternative sets of inputs or outputs that a Behavior may use."""
    _PKG = "Classification"
    _DECL = {
    # A constraint that should be satisfied for the owner of the Parameters in an input ParameterSet t
    # o start execution using the values provided for those Parameters, or the owner of the Parameters
    #  in an output ParameterSet to end execution providing the values for those Parameters, if all pr
    # econditions and conditions on input ParameterSets were satisfied.
    'condition': _Ref('condition', "Constraint", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_condition_parameterSet"),
    # Parameters in the ParameterSet.
    'parameter': _Ref('parameter', "Parameter", multi=True, lo=0, hi='*', assoc="A_parameterSet_parameter"),
    }
    _UNIONS = {
        "ownedElement": ("condition",),
    }
    CONSTRAINTS = (
        ("same_parameterized_entity",
         "parameter->forAll(p1, p2 | self.owner = p1.owner and self.owner = p2.owner and p1.direct"
         "ion = p2.direction)"
        ),
        ("input",
         "((parameter->exists(direction = ParameterDirectionKind::_'in')) implies behavioralFeatur"
         "e.ownedParameter->select(p | p.direction = ParameterDirectionKind::_'in' and p.parameter"
         "Set->isEmpty())->forAll(isStream)) and ((parameter->exists(direction = ParameterDirectio"
         "nKind::out)) implies behavioralFeature.ownedParameter->select(p | p.direction = Paramete"
         "rDirectionKind::out and p.parameterSet->isEmpty())->forAll(isStream))"
        ),
        ("two_parameter_sets",
         "parameter->forAll(parameterSet->forAll(s1, s2 | s1->size() = s2->size() implies s1.param"
         "eter->exists(p | not s2.parameter->includes(p))))"
        ),
    )

class PartDecomposition(InteractionUse):
    """A PartDecomposition is a description of the internal Interactions of one Lifeline relative to an Interaction."""
    _PKG = "Interactions"
    CONSTRAINTS = (
        ("commutativity_of_decomposition",
         "(no specification serialized)"
        ),
        ("assume",
         "(no specification serialized)"
        ),
        ("parts_of_internal_structures",
         "(no specification serialized)"
        ),
    )

class Port(Property):
    """A Port is a property of an EncapsulatedClassifier that specifies a distinct interaction point between that EncapsulatedClassifier and its environment or between the (behavior of the) EncapsulatedClassifier and its internal parts. Ports are connected to Properties of the EncapsulatedClassifier by Connectors through which requests can be made to invoke BehavioralFeatures. A Port may specify the services an EncapsulatedClassifier provides (offers) to its environment as well as the services that an EncapsulatedClassifier expects (requires) of its environment. A Port may have an associated ProtocolStateMachine."""
    _PKG = "StructuredClassifiers"
    _DECL = {
    # Specifies whether requests arriving at this Port are sent to the classifier behavior of this Enc
    # apsulatedClassifier. Such a Port is referred to as a behavior Port. Any invocation of a Behavior
    # alFeature targeted at a behavior Port will be handled by the instance of the owning Encapsulated
    # Classifier itself, rather than by any instances that it may contain.
    'isBehavior': _Ref('isBehavior', bool),
    # Specifies the way that the provided and required Interfaces are derived from the Port’s Type.
    'isConjugated': _Ref('isConjugated', bool),
    # If true, indicates that this Port is used to provide the published functionality of an Encapsula
    # tedClassifier. If false, this Port is used to implement the EncapsulatedClassifier but is not pa
    # rt of the essential externally-visible functionality of the EncapsulatedClassifier and can, ther
    # efore, be altered or deleted along with the internal implementation of the EncapsulatedClassifie
    # r and other properties that are considered part of its implementation.
    'isService': _Ref('isService', bool),
    # An optional ProtocolStateMachine which describes valid interactions at this interaction point.
    'protocol': _Ref('protocol', "ProtocolStateMachine", assoc="A_protocol_port"),
    # The Interfaces specifying the set of Operations and Receptions that the EncapsulatedCclassifier 
    # offers to its environment via this Port, and which it will handle either directly or by forwardi
    # ng it to a part of its internal structure. This association is derived according to the value of
    #  isConjugated. If isConjugated is false, provided is derived as the union of the sets of Interfa
    # ces realized by the type of the port and its supertypes, or directly from the type of the Port i
    # f the Port is typed by an Interface. If isConjugated is true, it is derived as the union of the 
    # sets of Interfaces used by the type of the Port and its supertypes.
    'provided': _Ref('provided', "Interface", derived=True, readonly=True, multi=True, lo=0, hi='*', assoc="A_provided_port"),
    # A Port may be redefined when its containing EncapsulatedClassifier is specialized. The redefinin
    # g Port may have additional Interfaces to those that are associated with the redefined Port or it
    #  may replace an Interface by one of its subtypes.
    'redefinedPort': _Ref('redefinedPort', "Port", multi=True, lo=0, hi='*', subsets=("redefinedProperty",), assoc="A_redefinedPort_port"),
    # The Interfaces specifying the set of Operations and Receptions that the EncapsulatedCassifier ex
    # pects its environment to handle via this port. This association is derived according to the valu
    # e of isConjugated. If isConjugated is false, required is derived as the union of the sets of Int
    # erfaces used by the type of the Port and its supertypes. If isConjugated is true, it is derived 
    # as the union of the sets of Interfaces realized by the type of the Port and its supertypes, or d
    # irectly from the type of the Port if the Port is typed by an Interface.
    'required': _Ref('required', "Interface", derived=True, readonly=True, multi=True, lo=0, hi='*', assoc="A_required_port"),
    }
    _UNIONS = {
        "redefinedElement": ("redefinedPort",),
    }
    CONSTRAINTS = (
        ("port_aggregation",
         "aggregation = AggregationKind::composite"
        ),
        ("default_value",
         "type.oclIsKindOf(Interface) implies defaultValue->isEmpty()"
        ),
        ("encapsulated_owner",
         "owner = encapsulatedClassifier"
        ),
    )
    def provided(self) -> "Interface":
        """
        Derivation for Port::/provided
        [Port operation (query); params: none; returns: "Interface"; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def required(self) -> "Interface":
        """
        Derivation for Port::/required
        [Port operation (query); params: none; returns: "Interface"; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def basicProvided(self) -> "Interface":
        """
        The union of the sets of Interfaces realized by the type of the Port and its supertypes, or di
        rectly the type of the Port if the Port is typed by an Interface.
        [Port operation (query); params: none; returns: "Interface"; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def basicRequired(self) -> "Interface":
        """
        The union of the sets of Interfaces used by the type of the Port and its supertypes.
        [Port operation (query); params: none; returns: "Interface"; stub - metamodel metadata only]
        """
        raise NotImplementedError

class PrimitiveType(DataType):
    """A PrimitiveType defines a predefined DataType, without any substructure. A PrimitiveType may have an algebra and operations defined outside of UML, for example, mathematically."""
    _PKG = "SimpleClassifiers"

class Profile(Package):
    """A profile defines limited extensions to a reference metamodel with the purpose of adapting the metamodel to a specific platform or domain."""
    _PKG = "Packages"
    _DECL = {
    # References a metaclass that may be extended.
    'metaclassReference': _Ref('metaclassReference', "ElementImport", composite=True, multi=True, lo=0, hi='*', subsets=("elementImport",), assoc="A_metaclassReference_profile"),
    # References a package containing (directly or indirectly) metaclasses that may be extended.
    'metamodelReference': _Ref('metamodelReference', "PackageImport", composite=True, multi=True, lo=0, hi='*', subsets=("packageImport",), assoc="A_metamodelReference_profile"),
    }
    _UNIONS = {
        "directedRelationship": ("metaclassReference", "metamodelReference",),
        "ownedElement": ("metaclassReference", "metamodelReference",),
        "relationship": ("metaclassReference", "metamodelReference",),
    }
    CONSTRAINTS = (
        ("metaclass_reference_not_specialized",
         "metaclassReference.importedElement-> select(c | c.oclIsKindOf(Classifier) and (c.oclAsTy"
         "pe(Classifier).allParents()->collect(namespace)->includes(self)))->isEmpty() and package"
         "dElement-> select(oclIsKindOf(Classifier))->collect(oclAsType(Classifier).allParents())-"
         "> intersection(metaclassReference.importedElement->select(oclIsKindOf(Classifier))->coll"
         "ect(oclAsType(Classifier)))->isEmpty()"
        ),
        ("references_same_metamodel",
         "metamodelReference.importedPackage.elementImport.importedElement.allOwningPackages()-> u"
         "nion(metaclassReference.importedElement.allOwningPackages() )->notEmpty()"
        ),
    )

class ProfileApplication(DirectedRelationship):
    """A profile application is used to show which profiles have been applied to a package."""
    _PKG = "Packages"
    _DECL = {
    # References the Profiles that are applied to a Package through this ProfileApplication.
    'appliedProfile': _Ref('appliedProfile', "Profile", subsets=("target",), assoc="A_appliedProfile_profileApplication"),
    # The package that owns the profile application.
    'applyingPackage': _Ref('applyingPackage', "Package", subsets=("source", "owner",), assoc="A_profileApplication_applyingPackage"),
    # Specifies that the Profile filtering rules for the metaclasses of the referenced metamodel shall
    #  be strictly applied.
    'isStrict': _Ref('isStrict', bool),
    }
    _UNIONS = {
        "owner": ("applyingPackage",),
        "relatedElement": ("appliedProfile", "applyingPackage",),
        "source": ("applyingPackage",),
        "target": ("appliedProfile",),
    }

class ProtocolConformance(DirectedRelationship):
    """A ProtocolStateMachine can be redefined into a more specific ProtocolStateMachine or into behavioral StateMachine. ProtocolConformance declares that the specific ProtocolStateMachine specifies a protocol that conforms to the general ProtocolStateMachine or that the specific behavioral StateMachine abides by the protocol of the general ProtocolStateMachine."""
    _PKG = "StateMachines"
    _DECL = {
    # Specifies the ProtocolStateMachine to which the specific ProtocolStateMachine conforms.
    'generalMachine': _Ref('generalMachine', "ProtocolStateMachine", subsets=("target",), assoc="A_generalMachine_protocolConformance"),
    # Specifies the ProtocolStateMachine which conforms to the general ProtocolStateMachine.
    'specificMachine': _Ref('specificMachine', "ProtocolStateMachine", subsets=("source", "owner",), assoc="A_conformance_specificMachine"),
    }
    _UNIONS = {
        "owner": ("specificMachine",),
        "relatedElement": ("generalMachine", "specificMachine",),
        "source": ("specificMachine",),
        "target": ("generalMachine",),
    }

class StateMachine(Behavior):
    """StateMachines can be used to express event-driven behaviors of parts of a system. Behavior is modeled as a traversal of a graph of Vertices interconnected by one or more joined Transition arcs that are triggered by the dispatching of successive Event occurrences. During this traversal, the StateMachine may execute a sequence of Behaviors associated with various elements of the StateMachine."""
    _PKG = "StateMachines"
    _DECL = {
    # The connection points defined for this StateMachine. They represent the interface of the StateMa
    # chine when used as part of submachine State
    'connectionPoint': _Ref('connectionPoint', "Pseudostate", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_connectionPoint_stateMachine"),
    # The StateMachines of which this is an extension.
    'extendedStateMachine': _Ref('extendedStateMachine', "StateMachine", multi=True, lo=0, hi='*', redefines=("redefinedBehavior",), assoc="A_extendedStateMachine_stateMachine"),
    # The Regions owned directly by the StateMachine.
    'region': _Ref('region', "Region", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_region_stateMachine"),
    # References the submachine(s) in case of a submachine State. Multiple machines are referenced in 
    # case of a concurrent State.
    'submachineState': _Ref('submachineState', "State", multi=True, lo=0, hi='*', assoc="A_submachineState_submachine"),
    }
    _UNIONS = {
        "member": ("connectionPoint", "region",),
        "ownedElement": ("connectionPoint", "region",),
        "ownedMember": ("connectionPoint", "region",),
    }
    CONSTRAINTS = (
        ("connection_points",
         "connectionPoint->forAll (kind = PseudostateKind::entryPoint or kind = PseudostateKind::e"
         "xitPoint)"
        ),
        ("classifier_context",
         "_'context' <> null implies not _'context'.oclIsKindOf(Interface)"
        ),
        ("method",
         "specification <> null implies connectionPoint->isEmpty()"
        ),
        ("context_classifier",
         "specification <> null implies ( _'context' <> null and specification.featuringClassifier"
         "->exists(c | c = _'context'))"
        ),
    )
    def LCA(self, s1: "Vertex" = None, s2: "Vertex" = None) -> "Region":
        """
        The operation LCA(s1,s2) returns the Region that is the least common ancestor of Vertices s1 a
        nd s2, based on the StateMachine containment hierarchy.
        [StateMachine operation (query); params: s1: "Vertex", s2: "Vertex"; returns: "Region"; stub -
         metamodel metadata only]
        """
        raise NotImplementedError
    def ancestor(self, s1: "Vertex" = None, s2: "Vertex" = None) -> bool:
        """
        The query ancestor(s1, s2) checks whether Vertex s2 is an ancestor of Vertex s1.
        [StateMachine operation (query); params: s1: "Vertex", s2: "Vertex"; returns: bool; stub - met
        amodel metadata only]
        """
        raise NotImplementedError
    def isConsistentWith(self, redefiningElement: "RedefinableElement" = None) -> bool:
        """
        The query isConsistentWith specifies that a StateMachine can be redefined by any other StateMa
        chine for which the redefinition context is valid (see the isRedefinitionContextValid operatio
        n). Note that consistency requirements for the redefinition of Regions and connectionPoint Pse
        udostates owned by a StateMachine are specified by the isConsistentWith and isRedefinitionCont
        extValid operations for Region and Vertex (and its subclass Pseudostate).
        [StateMachine operation (query); params: redefiningElement: "RedefinableElement"; returns: boo
        l; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def isRedefinitionContextValid(self, redefinedElement: "RedefinableElement" = None) -> bool:
        """
        The query isRedefinitionContextValid specifies whether the redefinition context of a StateMach
        ine is properly related to the redefinition contexts of a StateMachine it redefines. The requi
        rement is that the context BehavioredClassifier of a redefining StateMachine must specialize t
        he context Classifier of the redefined StateMachine. If the redefining StateMachine does not h
        ave a context BehavioredClassifier, then then the redefining StateMachine also must not have a
         context BehavioredClassifier but must, instead, specialize the redefining StateMachine.
        [StateMachine operation (query); params: redefinedElement: "RedefinableElement"; returns: bool
        ; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def LCAState(self, v1: "Vertex" = None, v2: "Vertex" = None) -> "State":
        """
        This utility funciton is like the LCA, except that it returns the nearest composite State that
         contains both input Vertices.
        [StateMachine operation (query); params: v1: "Vertex", v2: "Vertex"; returns: "State"; stub - 
        metamodel metadata only]
        """
        raise NotImplementedError

class ProtocolStateMachine(StateMachine):
    """A ProtocolStateMachine is always defined in the context of a Classifier. It specifies which BehavioralFeatures of the Classifier can be called in which State and under which conditions, thus specifying the allowed invocation sequences on the Classifier's BehavioralFeatures. A ProtocolStateMachine specifies the possible and permitted Transitions on the instances of its context Classifier, together with the BehavioralFeatures that carry the Transitions. In this manner, an instance lifecycle can be specified for a Classifier, by defining the order in which the BehavioralFeatures can be activated and the States through which an instance progresses during its existence."""
    _PKG = "StateMachines"
    _DECL = {
    # Conformance between ProtocolStateMachine
    'conformance': _Ref('conformance', "ProtocolConformance", composite=True, multi=True, lo=0, hi='*', subsets=("directedRelationship", "ownedElement",), assoc="A_conformance_specificMachine"),
    }
    _UNIONS = {
        "directedRelationship": ("conformance",),
        "ownedElement": ("conformance",),
        "relationship": ("conformance",),
    }
    CONSTRAINTS = (
        ("classifier_context",
         "_'context' <> null and specification = null"
        ),
        ("deep_or_shallow_history",
         "region->forAll (r | r.subvertex->forAll (v | v.oclIsKindOf(Pseudostate) implies ((v.oclA"
         "sType(Pseudostate).kind <> PseudostateKind::deepHistory) and (v.oclAsType(Pseudostate).k"
         "ind <> PseudostateKind::shallowHistory))))"
        ),
        ("entry_exit_do",
         "region->forAll(r | r.subvertex->forAll(v | v.oclIsKindOf(State) implies (v.oclAsType(Sta"
         "te).entry->isEmpty() and v.oclAsType(State).exit->isEmpty() and v.oclAsType(State).doAct"
         "ivity->isEmpty())))"
        ),
        ("protocol_transitions",
         "region->forAll(r | r.transition->forAll(t | t.oclIsTypeOf(ProtocolTransition)))"
        ),
    )

class Transition(Namespace, RedefinableElement):
    """A Transition represents an arc between exactly one source Vertex and exactly one Target vertex (the source and targets may be the same Vertex). It may form part of a compound transition, which takes the StateMachine from one steady State configuration to another, representing the full response of the StateMachine to an occurrence of an Event that triggered it."""
    _PKG = "StateMachines"
    _DECL = {
    # Designates the Region that owns this Transition.
    'container': _Ref('container', "Region", subsets=("namespace",), assoc="A_transition_container"),
    # Specifies an optional behavior to be performed when the Transition fires.
    'effect': _Ref('effect', "Behavior", composite=True, subsets=("ownedElement",), assoc="A_effect_transition"),
    # A guard is a Constraint that provides a fine-grained control over the firing of the Transition. 
    # The guard is evaluated when an Event occurrence is dispatched by the StateMachine. If the guard 
    # is true at that time, the Transition may be enabled, otherwise, it is disabled. Guards should be
    #  pure expressions without side effects. Guard expressions with side effects are ill formed.
    'guard': _Ref('guard', "Constraint", composite=True, subsets=("ownedRule",), assoc="A_guard_transition"),
    # Indicates the precise type of the Transition.
    'kind': _Ref('kind', TransitionKind),
    # The Transition that is redefined by this Transition.
    'redefinedTransition': _Ref('redefinedTransition', "Transition", subsets=("redefinedElement",), assoc="A_redefinedTransition_transition"),
    # References the Classifier in which context this element may be redefined.
    'redefinitionContext': _Ref('redefinitionContext', "Classifier", derived=True, readonly=True, redefines=("redefinitionContext",), assoc="A_redefinitionContext_transition"),
    # Designates the originating Vertex (State or Pseudostate) of the Transition.
    'source': _Ref('source', "Vertex", assoc="A_outgoing_source_vertex"),
    # Designates the target Vertex that is reached when the Transition is taken.
    'target': _Ref('target', "Vertex", assoc="A_incoming_target_vertex"),
    # Specifies the Triggers that may fire the transition.
    'trigger': _Ref('trigger', "Trigger", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_trigger_transition"),
    }
    _UNIONS = {
        "member": ("guard",),
        "memberNamespace": ("container",),
        "namespace": ("container",),
        "ownedElement": ("effect", "guard", "trigger",),
        "ownedMember": ("guard",),
        "owner": ("container",),
        "redefinedElement": ("redefinedTransition",),
    }
    CONSTRAINTS = (
        ("state_is_external",
         "(kind = TransitionKind::external) implies not (source.oclIsKindOf(Pseudostate) and sourc"
         "e.oclAsType(Pseudostate).kind = PseudostateKind::entryPoint)"
        ),
        ("join_segment_guards",
         "(target.oclIsKindOf(Pseudostate) and target.oclAsType(Pseudostate).kind = PseudostateKin"
         "d::join) implies (guard = null and trigger->isEmpty())"
        ),
        ("state_is_internal",
         "(kind = TransitionKind::internal) implies (source.oclIsKindOf (State) and source = targe"
         "t)"
        ),
        ("outgoing_pseudostates",
         "source.oclIsKindOf(Pseudostate) and (source.oclAsType(Pseudostate).kind <> PseudostateKi"
         "nd::initial) implies trigger->isEmpty()"
        ),
        ("join_segment_state",
         "(target.oclIsKindOf(Pseudostate) and target.oclAsType(Pseudostate).kind = PseudostateKin"
         "d::join) implies (source.oclIsKindOf(State))"
        ),
        ("fork_segment_state",
         "(source.oclIsKindOf(Pseudostate) and source.oclAsType(Pseudostate).kind = PseudostateKin"
         "d::fork) implies (target.oclIsKindOf(State))"
        ),
        ("state_is_local",
         "(kind = TransitionKind::local) implies ((source.oclIsKindOf (State) and source.oclAsType"
         "(State).isComposite) or (source.oclIsKindOf (Pseudostate) and source.oclAsType(Pseudosta"
         "te).kind = PseudostateKind::entryPoint))"
        ),
        ("initial_transition",
         "(source.oclIsKindOf(Pseudostate) and container.stateMachine->notEmpty()) implies trigger"
         "->isEmpty()"
        ),
        ("fork_segment_guards",
         "(source.oclIsKindOf(Pseudostate) and source.oclAsType(Pseudostate).kind = PseudostateKin"
         "d::fork) implies (guard = null and trigger->isEmpty())"
        ),
        ("transition_vertices",
         "let stateMachine = self.containingStateMachine() in source.containingStateMachine() = st"
         "ateMachine and target.containingStateMachine() = stateMachine"
        ),
    )
    def containingStateMachine(self) -> "StateMachine":
        """
        The query containingStateMachine() returns the StateMachine that contains the Transition eithe
        r directly or transitively.
        [Transition operation (query); params: none; returns: "StateMachine"; stub - metamodel metadat
        a only]
        """
        raise NotImplementedError
    def isConsistentWith(self, redefiningElement: "RedefinableElement" = None) -> bool:
        """
        The query isConsistentWith specifies that a redefining Transition is consistent with a redefin
        ed Transition provided that the source Vertex of the redefining Transition redefines the sourc
        e Vertex of the redefined Transition.
        [Transition operation (query); params: redefiningElement: "RedefinableElement"; returns: bool;
         stub - metamodel metadata only]
        """
        raise NotImplementedError
    def redefinitionContext(self) -> "Classifier":
        """
        The redefinition context of a Transition is the nearest containing StateMachine.
        [Transition operation (query); params: none; returns: "Classifier"; stub - metamodel metadata 
        only]
        """
        raise NotImplementedError

class ProtocolTransition(Transition):
    """A ProtocolTransition specifies a legal Transition for an Operation. Transitions of ProtocolStateMachines have the following information: a pre-condition (guard), a Trigger, and a post-condition. Every ProtocolTransition is associated with at most one BehavioralFeature belonging to the context Classifier of the ProtocolStateMachine."""
    _PKG = "StateMachines"
    _DECL = {
    # Specifies the post condition of the Transition which is the Condition that should be obtained on
    # ce the Transition is triggered. This post condition is part of the post condition of the Operati
    # on connected to the Transition.
    'postCondition': _Ref('postCondition', "Constraint", composite=True, subsets=("ownedRule",), assoc="A_postCondition_owningTransition"),
    # Specifies the precondition of the Transition. It specifies the Condition that should be verified
    #  before triggering the Transition. This guard condition added to the source State will be evalua
    # ted as part of the precondition of the Operation referred by the Transition if any.
    'preCondition': _Ref('preCondition', "Constraint", composite=True, subsets=("guard",), assoc="A_preCondition_protocolTransition"),
    # This association refers to the associated Operation. It is derived from the Operation of the Cal
    # lEvent Trigger when applicable.
    'referred': _Ref('referred', "Operation", derived=True, readonly=True, multi=True, lo=0, hi='*', assoc="A_referred_protocolTransition"),
    }
    _UNIONS = {
        "member": ("postCondition", "preCondition",),
        "ownedElement": ("postCondition", "preCondition",),
        "ownedMember": ("postCondition", "preCondition",),
    }
    CONSTRAINTS = (
        ("refers_to_operation",
         "if (referred()->notEmpty() and containingStateMachine()._'context'->notEmpty()) then con"
         "tainingStateMachine()._'context'.oclAsType(BehavioredClassifier).allFeatures()->includes"
         "All(referred()) else true endif"
        ),
        ("associated_actions",
         "effect = null"
        ),
        ("belongs_to_psm",
         "container.belongsToPSM()"
        ),
    )
    def referred(self) -> "Operation":
        """
        Derivation for ProtocolTransition::/referred
        [ProtocolTransition operation (query); params: none; returns: "Operation"; stub - metamodel me
        tadata only]
        """
        raise NotImplementedError

class Pseudostate(Vertex):
    """A Pseudostate is an abstraction that encompasses different types of transient Vertices in the StateMachine graph. A StateMachine instance never comes to rest in a Pseudostate, instead, it will exit and enter the Pseudostate within a single run-to-completion step."""
    _PKG = "StateMachines"
    _DECL = {
    # Determines the precise type of the Pseudostate and can be one of: entryPoint, exitPoint, initial
    # , deepHistory, shallowHistory, join, fork, junction, terminate or choice.
    'kind': _Ref('kind', PseudostateKind),
    # The State that owns this Pseudostate and in which it appears.
    'state': _Ref('state', "State", subsets=("namespace",), assoc="A_connectionPoint_state"),
    # The StateMachine in which this Pseudostate is defined. This only applies to Pseudostates of the 
    # kind entryPoint or exitPoint.
    'stateMachine': _Ref('stateMachine', "StateMachine", subsets=("namespace",), assoc="A_connectionPoint_stateMachine"),
    }
    _UNIONS = {
        "memberNamespace": ("state", "stateMachine",),
        "namespace": ("state", "stateMachine",),
        "owner": ("state", "stateMachine",),
    }
    CONSTRAINTS = (
        ("transitions_outgoing",
         "(kind = PseudostateKind::fork) implies -- for any pair of outgoing transitions there exi"
         "sts an orthogonal state which contains the targets of these transitions -- such that the"
         "se targets belong to different regions of that orthogonal state outgoing->forAll(t1:Tran"
         "sition, t2:Transition | let contState:State = containingStateMachine().LCAState(t1.targe"
         "t, t2.target) in ((contState <> null) and (contState.region ->exists(r1:Region, r2: Regi"
         "on | (r1 <> r2) and t1.target.isContainedInRegion(r1) and t2.target.isContainedInRegion("
         "r2)))))"
        ),
        ("choice_vertex",
         "(kind = PseudostateKind::choice) implies (incoming->size() >= 1 and outgoing->size() >= "
         "1)"
        ),
        ("outgoing_from_initial",
         "(kind = PseudostateKind::initial) implies (outgoing.guard = null and outgoing.trigger->i"
         "sEmpty())"
        ),
        ("join_vertex",
         "(kind = PseudostateKind::join) implies (outgoing->size() = 1 and incoming->size() >= 2)"
        ),
        ("junction_vertex",
         "(kind = PseudostateKind::junction) implies (incoming->size() >= 1 and outgoing->size() >"
         "= 1)"
        ),
        ("history_vertices",
         "((kind = PseudostateKind::deepHistory) or (kind = PseudostateKind::shallowHistory)) impl"
         "ies (outgoing->size() <= 1)"
        ),
        ("initial_vertex",
         "(kind = PseudostateKind::initial) implies (outgoing->size() <= 1)"
        ),
        ("fork_vertex",
         "(kind = PseudostateKind::fork) implies (incoming->size() = 1 and outgoing->size() >= 2)"
        ),
        ("transitions_incoming",
         "(kind = PseudostateKind::join) implies -- for any pair of incoming transitions there exi"
         "sts an orthogonal state which contains the source vetices of these transitions -- such t"
         "hat these source vertices belong to different regions of that orthogonal state incoming-"
         ">forAll(t1:Transition, t2:Transition | let contState:State = containingStateMachine().LC"
         "AState(t1.source, t2.source) in ((contState <> null) and (contState.region ->exists(r1:R"
         "egion, r2: Region | (r1 <> r2) and t1.source.isContainedInRegion(r1) and t2.source.isCon"
         "tainedInRegion(r2)))))"
        ),
    )
    def isConsistentWith(self, redefiningElement: "RedefinableElement" = None) -> bool:
        """
        The query isConsistentWith() specifies a Pseudostate can only be redefined by a Pseudostate of
         the same kind.
        [Pseudostate operation; params: redefiningElement: "RedefinableElement"; returns: bool; stub -
         metamodel metadata only]
        """
        raise NotImplementedError

class QualifierValue(Element):
    """A QualifierValue is an Element that is used as part of LinkEndData to provide the value for a single qualifier of the end given by the LinkEndData."""
    _PKG = "Actions"
    _DECL = {
    # The qualifier Property for which the value is to be specified.
    'qualifier': _Ref('qualifier', "Property", assoc="A_qualifier_qualifierValue"),
    # The InputPin from which the specified value for the qualifier is taken.
    'value': _Ref('value', "InputPin", assoc="A_value_qualifierValue"),
    }
    CONSTRAINTS = (
        ("multiplicity_of_qualifier",
         "value.is(1,1)"
        ),
        ("type_of_qualifier",
         "value.type.conformsTo(qualifier.type)"
        ),
        ("qualifier_attribute",
         "linkEndData.end.qualifier->includes(qualifier)"
        ),
    )

class RaiseExceptionAction(Action):
    """A RaiseExceptionAction is an Action that causes an exception to occur. The input value becomes the exception object."""
    _PKG = "Actions"
    _DECL = {
    # An InputPin whose value becomes the exception object.
    'exception': _Ref('exception', "InputPin", composite=True, subsets=("input",), assoc="A_exception_raiseExceptionAction"),
    }
    _UNIONS = {
        "input": ("exception",),
        "ownedElement": ("exception",),
    }

class ReadExtentAction(Action):
    """A ReadExtentAction is an Action that retrieves the current instances of a Classifier."""
    _PKG = "Actions"
    _DECL = {
    # The Classifier whose instances are to be retrieved.
    'classifier': _Ref('classifier', "Classifier", assoc="A_classifier_readExtentAction"),
    # The OutputPin on which the Classifier instances are placed.
    'result': _Ref('result', "OutputPin", composite=True, subsets=("output",), assoc="A_result_readExtentAction"),
    }
    _UNIONS = {
        "output": ("result",),
        "ownedElement": ("result",),
    }
    CONSTRAINTS = (
        ("type_is_classifier",
         "result.type = classifier"
        ),
        ("multiplicity_of_result",
         "result.is(0,*)"
        ),
    )

class ReadIsClassifiedObjectAction(Action):
    """A ReadIsClassifiedObjectAction is an Action that determines whether an object is classified by a given Classifier."""
    _PKG = "Actions"
    _DECL = {
    # The Classifier against which the classification of the input object is tested.
    'classifier': _Ref('classifier', "Classifier", assoc="A_classifier_readIsClassifiedObjectAction"),
    # Indicates whether the input object must be directly classified by the given Classifier or whethe
    # r it may also be an instance of a specialization of the given Classifier.
    'isDirect': _Ref('isDirect', bool),
    # The InputPin that holds the object whose classification is to be tested.
    'object': _Ref('object', "InputPin", composite=True, subsets=("input",), assoc="A_object_readIsClassifiedObjectAction"),
    # The OutputPin that holds the Boolean result of the test.
    'result': _Ref('result', "OutputPin", composite=True, subsets=("output",), assoc="A_result_readIsClassifiedObjectAction"),
    }
    _UNIONS = {
        "input": ("object",),
        "output": ("result",),
        "ownedElement": ("object", "result",),
    }
    CONSTRAINTS = (
        ("no_type",
         "object.type = null"
        ),
        ("multiplicity_of_output",
         "result.is(1,1)"
        ),
        ("boolean_result",
         "result.type = Boolean"
        ),
        ("multiplicity_of_input",
         "object.is(1,1)"
        ),
    )

class ReadLinkAction(LinkAction):
    """A ReadLinkAction is a LinkAction that navigates across an Association to retrieve the objects on one end."""
    _PKG = "Actions"
    _DECL = {
    # The OutputPin on which the objects retrieved from the "open" end of those links whose values on 
    # other ends are given by the endData.
    'result': _Ref('result', "OutputPin", composite=True, subsets=("output",), assoc="A_result_readLinkAction"),
    }
    _UNIONS = {
        "output": ("result",),
        "ownedElement": ("result",),
    }
    CONSTRAINTS = (
        ("type_and_ordering",
         "self.openEnd()->forAll(type=result.type and isOrdered=result.isOrdered)"
        ),
        ("compatible_multiplicity",
         "self.openEnd()->first().compatibleWith(result)"
        ),
        ("visibility",
         "let openEnd : Property = self.openEnd()->first() in openEnd.visibility = VisibilityKind:"
         ":public or endData->exists(oed | oed.end<>openEnd and (_'context' = oed.end.type or (ope"
         "nEnd.visibility = VisibilityKind::protected and _'context'.conformsTo(oed.end.type.oclAs"
         "Type(Classifier)))))"
        ),
        ("one_open_end",
         "self.openEnd()->size() = 1"
        ),
        ("navigable_open_end",
         "self.openEnd()->first().isNavigable()"
        ),
    )
    def openEnd(self) -> "Property":
        """
        Returns the ends corresponding to endData with no value InputPin. (A well-formed ReadLinkActio
        n is constrained to have only one of these.)
        [ReadLinkAction operation (query); params: none; returns: "Property"; stub - metamodel metadat
        a only]
        """
        raise NotImplementedError

class ReadLinkObjectEndAction(Action):
    """A ReadLinkObjectEndAction is an Action that retrieves an end object from a link object."""
    _PKG = "Actions"
    _DECL = {
    # The Association end to be read.
    'end': _Ref('end', "Property", assoc="A_end_readLinkObjectEndAction"),
    # The input pin from which the link object is obtained.
    'object': _Ref('object', "InputPin", composite=True, subsets=("input",), assoc="A_object_readLinkObjectEndAction"),
    # The OutputPin where the result value is placed.
    'result': _Ref('result', "OutputPin", composite=True, subsets=("output",), assoc="A_result_readLinkObjectEndAction"),
    }
    _UNIONS = {
        "input": ("object",),
        "output": ("result",),
        "ownedElement": ("object", "result",),
    }
    CONSTRAINTS = (
        ("property",
         "end.association <> null"
        ),
        ("multiplicity_of_object",
         "object.is(1,1)"
        ),
        ("ends_of_association",
         "end.association.memberEnd->forAll(e | not e.isStatic)"
        ),
        ("type_of_result",
         "result.type = end.type"
        ),
        ("multiplicity_of_result",
         "result.is(1,1)"
        ),
        ("type_of_object",
         "object.type = end.association"
        ),
        ("association_of_association",
         "end.association.oclIsKindOf(AssociationClass)"
        ),
    )

class ReadLinkObjectEndQualifierAction(Action):
    """A ReadLinkObjectEndQualifierAction is an Action that retrieves a qualifier end value from a link object."""
    _PKG = "Actions"
    _DECL = {
    # The InputPin from which the link object is obtained.
    'object': _Ref('object', "InputPin", composite=True, subsets=("input",), assoc="A_object_readLinkObjectEndQualifierAction"),
    # The qualifier Property to be read.
    'qualifier': _Ref('qualifier', "Property", assoc="A_qualifier_readLinkObjectEndQualifierAction"),
    # The OutputPin where the result value is placed.
    'result': _Ref('result', "OutputPin", composite=True, subsets=("output",), assoc="A_result_readLinkObjectEndQualifierAction"),
    }
    _UNIONS = {
        "input": ("object",),
        "output": ("result",),
        "ownedElement": ("object", "result",),
    }
    CONSTRAINTS = (
        ("multiplicity_of_object",
         "object.is(1,1)"
        ),
        ("type_of_object",
         "object.type = qualifier.associationEnd.association"
        ),
        ("multiplicity_of_qualifier",
         "qualifier.is(1,1)"
        ),
        ("ends_of_association",
         "qualifier.associationEnd.association.memberEnd->forAll(e | not e.isStatic)"
        ),
        ("multiplicity_of_result",
         "result.is(1,1)"
        ),
        ("same_type",
         "result.type = qualifier.type"
        ),
        ("association_of_association",
         "qualifier.associationEnd.association.oclIsKindOf(AssociationClass)"
        ),
        ("qualifier_attribute",
         "qualifier.associationEnd <> null"
        ),
    )

class ReadSelfAction(Action):
    """A ReadSelfAction is an Action that retrieves the context object of the Behavior execution within which the ReadSelfAction execution is taking place."""
    _PKG = "Actions"
    _DECL = {
    # The OutputPin on which the context object is placed.
    'result': _Ref('result', "OutputPin", composite=True, subsets=("output",), assoc="A_result_readSelfAction"),
    }
    _UNIONS = {
        "output": ("result",),
        "ownedElement": ("result",),
    }
    CONSTRAINTS = (
        ("contained",
         "_'context' <> null"
        ),
        ("multiplicity",
         "result.is(1,1)"
        ),
        ("not_static",
         "let behavior: Behavior = self.containingBehavior() in behavior.specification<>null impli"
         "es not behavior.specification.isStatic"
        ),
        ("type",
         "result.type = _'context'"
        ),
    )

class ReadStructuralFeatureAction(StructuralFeatureAction):
    """A ReadStructuralFeatureAction is a StructuralFeatureAction that retrieves the values of a StructuralFeature."""
    _PKG = "Actions"
    _DECL = {
    # The OutputPin on which the result values are placed.
    'result': _Ref('result', "OutputPin", composite=True, subsets=("output",), assoc="A_result_readStructuralFeatureAction"),
    }
    _UNIONS = {
        "output": ("result",),
        "ownedElement": ("result",),
    }
    CONSTRAINTS = (
        ("multiplicity",
         "structuralFeature.compatibleWith(result)"
        ),
        ("type_and_ordering",
         "result.type =structuralFeature.type and result.isOrdered = structuralFeature.isOrdered"
        ),
    )

class ReadVariableAction(VariableAction):
    """A ReadVariableAction is a VariableAction that retrieves the values of a Variable."""
    _PKG = "Actions"
    _DECL = {
    # The OutputPin on which the result values are placed.
    'result': _Ref('result', "OutputPin", composite=True, subsets=("output",), assoc="A_result_readVariableAction"),
    }
    _UNIONS = {
        "output": ("result",),
        "ownedElement": ("result",),
    }
    CONSTRAINTS = (
        ("type_and_ordering",
         "result.type =variable.type and result.isOrdered = variable.isOrdered"
        ),
        ("compatible_multiplicity",
         "variable.compatibleWith(result)"
        ),
    )

class Reception(BehavioralFeature):
    """A Reception is a declaration stating that a Classifier is prepared to react to the receipt of a Signal."""
    _PKG = "SimpleClassifiers"
    _DECL = {
    # The Signal that this Reception handles.
    'signal': _Ref('signal', "Signal", assoc="A_signal_reception"),
    }
    CONSTRAINTS = (
        ("same_name_as_signal",
         "name = signal.name"
        ),
        ("same_structure_as_signal",
         "signal.ownedAttribute->size() = ownedParameter->size() and Sequence{1..signal.ownedAttri"
         "bute->size()}->forAll( i | ownedParameter->at(i).direction = ParameterDirectionKind::_'i"
         "n' and ownedParameter->at(i).name = signal.ownedAttribute->at(i).name and ownedParameter"
         "->at(i).type = signal.ownedAttribute->at(i).type and ownedParameter->at(i).lowerBound() "
         "= signal.ownedAttribute->at(i).lowerBound() and ownedParameter->at(i).upperBound() = sig"
         "nal.ownedAttribute->at(i).upperBound() )"
        ),
    )

class ReclassifyObjectAction(Action):
    """A ReclassifyObjectAction is an Action that changes the Classifiers that classify an object."""
    _PKG = "Actions"
    _DECL = {
    # Specifies whether existing Classifiers should be removed before adding the new Classifiers.
    'isReplaceAll': _Ref('isReplaceAll', bool),
    # A set of Classifiers to be added to the Classifiers of the given object.
    'newClassifier': _Ref('newClassifier', "Classifier", multi=True, lo=0, hi='*', assoc="A_newClassifier_reclassifyObjectAction"),
    # The InputPin that holds the object to be reclassified.
    'object': _Ref('object', "InputPin", composite=True, subsets=("input",), assoc="A_object_reclassifyObjectAction"),
    # A set of Classifiers to be removed from the Classifiers of the given object.
    'oldClassifier': _Ref('oldClassifier', "Classifier", multi=True, lo=0, hi='*', assoc="A_oldClassifier_reclassifyObjectAction"),
    }
    _UNIONS = {
        "input": ("object",),
        "ownedElement": ("object",),
    }
    CONSTRAINTS = (
        ("input_pin",
         "object.type = null"
        ),
        ("classifier_not_abstract",
         "not newClassifier->exists(isAbstract)"
        ),
        ("multiplicity",
         "object.is(1,1)"
        ),
    )

class TemplateSignature(Element):
    """A Template Signature bundles the set of formal TemplateParameters for a template."""
    _PKG = "CommonStructure"
    _DECL = {
    # The formal parameters that are owned by this TemplateSignature.
    'ownedParameter': _Ref('ownedParameter', "TemplateParameter", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement", "parameter",), assoc="A_ownedParameter_signature"),
    # The ordered set of all formal TemplateParameters for this TemplateSignature.
    'parameter': _Ref('parameter', "TemplateParameter", multi=True, lo=0, hi='*', assoc="A_parameter_templateSignature"),
    # The TemplateableElement that owns this TemplateSignature.
    'template': _Ref('template', "TemplateableElement", subsets=("owner",), assoc="A_ownedTemplateSignature_template"),
    }
    _UNIONS = {
        "ownedElement": ("ownedParameter",),
        "owner": ("template",),
    }
    CONSTRAINTS = (
        ("own_elements",
         "template.ownedElement->includesAll(parameter.parameteredElement->asSet() - parameter.own"
         "edParameteredElement->asSet())"
        ),
        ("unique_parameters",
         "parameter->forAll( p1, p2 | (p1 <> p2 and p1.parameteredElement.oclIsKindOf(NamedElement"
         ") and p2.parameteredElement.oclIsKindOf(NamedElement) ) implies p1.parameteredElement.oc"
         "lAsType(NamedElement).name <> p2.parameteredElement.oclAsType(NamedElement).name)"
        ),
    )

class RedefinableTemplateSignature(RedefinableElement, TemplateSignature):
    """A RedefinableTemplateSignature supports the addition of formal template parameters in a specialization of a template classifier."""
    _PKG = "Classification"
    _DECL = {
    # The Classifier that owns this RedefinableTemplateSignature.
    'classifier': _Ref('classifier', "Classifier", subsets=("redefinitionContext",), redefines=("template",), assoc="A_ownedTemplateSignature_classifier"),
    # The signatures extended by this RedefinableTemplateSignature.
    'extendedSignature': _Ref('extendedSignature', "RedefinableTemplateSignature", multi=True, lo=0, hi='*', subsets=("redefinedElement",), assoc="A_extendedSignature_redefinableTemplateSignature"),
    # The formal template parameters of the extended signatures.
    'inheritedParameter': _Ref('inheritedParameter', "TemplateParameter", derived=True, readonly=True, multi=True, lo=0, hi='*', subsets=("parameter",), assoc="A_inheritedParameter_redefinableTemplateSignature"),
    }
    _UNIONS = {
        "redefinedElement": ("extendedSignature",),
        "redefinitionContext": ("classifier",),
    }
    CONSTRAINTS = (
        ("redefines_parents",
         "classifier.allParents()->forAll(c | c.ownedTemplateSignature->notEmpty() implies self->c"
         "losure(extendedSignature)->includes(c.ownedTemplateSignature))"
        ),
    )
    def inheritedParameter(self) -> "TemplateParameter":
        """
        Derivation for RedefinableTemplateSignature::/inheritedParameter
        [RedefinableTemplateSignature operation (query); params: none; returns: "TemplateParameter"; s
        tub - metamodel metadata only]
        """
        raise NotImplementedError
    def isConsistentWith(self, redefiningElement: "RedefinableElement" = None) -> bool:
        """
        The query isConsistentWith() specifies, for any two RedefinableTemplateSignatures in a context
         in which redefinition is possible, whether redefinition would be logically consistent. A rede
        fining template signature is always consistent with a redefined template signature, as redefin
        ition only adds new formal parameters.
        [RedefinableTemplateSignature operation (query); params: redefiningElement: "RedefinableElemen
        t"; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError

class ReduceAction(Action):
    """A ReduceAction is an Action that reduces a collection to a single value by repeatedly combining the elements of the collection using a reducer Behavior."""
    _PKG = "Actions"
    _DECL = {
    # The InputPin that provides the collection to be reduced.
    'collection': _Ref('collection', "InputPin", composite=True, subsets=("input",), assoc="A_collection_reduceAction"),
    # Indicates whether the order of the input collection should determine the order in which the redu
    # cer Behavior is applied to its elements.
    'isOrdered': _Ref('isOrdered', bool),
    # A Behavior that is repreatedly applied to two elements of the input collection to produce a valu
    # e that is of the same type as elements of the collection.
    'reducer': _Ref('reducer', "Behavior", assoc="A_reducer_reduceAction"),
    # The output pin on which the result value is placed.
    'result': _Ref('result', "OutputPin", composite=True, subsets=("output",), assoc="A_result_reduceAction"),
    }
    _UNIONS = {
        "input": ("collection",),
        "output": ("result",),
        "ownedElement": ("collection", "result",),
    }
    CONSTRAINTS = (
        ("reducer_inputs_output",
         "let inputs: OrderedSet(Parameter) = reducer.inputParameters() in let outputs: OrderedSet"
         "(Parameter) = reducer.outputParameters() in inputs->size()=2 and outputs->size()=1 and i"
         "nputs.type->forAll(t | outputs.type->forAll(conformsTo(t)) and -- Note that the followin"
         "g only checks the case when the collection is via multiple tokens. collection.upperBound"
         "()>1 implies collection.type.conformsTo(t))"
        ),
        ("input_type_is_collection",
         "(no specification serialized)"
        ),
        ("output_types_are_compatible",
         "reducer.outputParameters().type->forAll(conformsTo(result.type))"
        ),
    )

class Region(Namespace, RedefinableElement):
    """A Region is a top-level part of a StateMachine or a composite State, that serves as a container for the Vertices and Transitions of the StateMachine. A StateMachine or composite State may contain multiple Regions representing behaviors that may occur in parallel."""
    _PKG = "StateMachines"
    _DECL = {
    # The region of which this region is an extension.
    'extendedRegion': _Ref('extendedRegion', "Region", subsets=("redefinedElement",), assoc="A_extendedRegion_region"),
    # References the Classifier in which context this element may be redefined.
    'redefinitionContext': _Ref('redefinitionContext', "Classifier", derived=True, readonly=True, redefines=("redefinitionContext",), assoc="A_redefinitionContext_region"),
    # The State that owns the Region. If a Region is owned by a State, then it cannot also be owned by
    #  a StateMachine.
    'state': _Ref('state', "State", subsets=("namespace",), assoc="A_region_state"),
    # The StateMachine that owns the Region. If a Region is owned by a StateMachine, then it cannot al
    # so be owned by a State.
    'stateMachine': _Ref('stateMachine', "StateMachine", subsets=("namespace",), assoc="A_region_stateMachine"),
    # The set of Vertices that are owned by this Region.
    'subvertex': _Ref('subvertex', "Vertex", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_subvertex_container"),
    # The set of Transitions owned by the Region.
    'transition': _Ref('transition', "Transition", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_transition_container"),
    }
    _UNIONS = {
        "member": ("subvertex", "transition",),
        "memberNamespace": ("state", "stateMachine",),
        "namespace": ("state", "stateMachine",),
        "ownedElement": ("subvertex", "transition",),
        "ownedMember": ("subvertex", "transition",),
        "owner": ("state", "stateMachine",),
        "redefinedElement": ("extendedRegion",),
    }
    CONSTRAINTS = (
        ("deep_history_vertex",
         "self.subvertex->select (oclIsKindOf(Pseudostate))->collect(oclAsType(Pseudostate))-> sel"
         "ect(kind = PseudostateKind::deepHistory)->size() <= 1"
        ),
        ("shallow_history_vertex",
         "subvertex->select(oclIsKindOf(Pseudostate))->collect(oclAsType(Pseudostate))-> select(ki"
         "nd = PseudostateKind::shallowHistory)->size() <= 1"
        ),
        ("owned",
         "(stateMachine <> null implies state = null) and (state <> null implies stateMachine = nu"
         "ll)"
        ),
        ("initial_vertex",
         "self.subvertex->select (oclIsKindOf(Pseudostate))->collect(oclAsType(Pseudostate))-> sel"
         "ect(kind = PseudostateKind::initial)->size() <= 1"
        ),
    )
    def belongsToPSM(self) -> bool:
        """
        The operation belongsToPSM () checks if the Region belongs to a ProtocolStateMachine.
        [Region operation (query); params: none; returns: bool; stub - metamodel metadata only]
        """
        raise NotImplementedError
    def containingStateMachine(self) -> "StateMachine":
        """
        The operation containingStateMachine() returns the StateMachine in which this Region is define
        d.
        [Region operation (query); params: none; returns: "StateMachine"; stub - metamodel metadata on
        ly]
        """
        raise NotImplementedError
    def isConsistentWith(self, redefiningElement: "RedefinableElement" = None) -> bool:
        """
        The query isConsistentWith specifies that a Region can be redefined by any Region for which th
        e redefinition context is valid (see the isRedefinitionContextValid operation). Note that cons
        istency requirements for the redefinition of Vertices and Transitions within a redefining Regi
        on are specified by the isConsistentWith and isRedefinitionContextValid operations for Vertex 
        (and its subclasses) and Transition.
        [Region operation (query); params: redefiningElement: "RedefinableElement"; returns: bool; stu
        b - metamodel metadata only]
        """
        raise NotImplementedError
    def isRedefinitionContextValid(self, redefinedElement: "RedefinableElement" = None) -> bool:
        """
        The query isRedefinitionContextValid() specifies whether the redefinition contexts of a Region
         are properly related to the redefinition contexts of the specified Region to allow this eleme
        nt to redefine the other. The containing StateMachine or State of a redefining Region must Red
        efine the containing StateMachine or State of the redefined Region.
        [Region operation (query); params: redefinedElement: "RedefinableElement"; returns: bool; stub
         - metamodel metadata only]
        """
        raise NotImplementedError
    def redefinitionContext(self) -> "Classifier":
        """
        The redefinition context of a Region is the nearest containing StateMachine.
        [Region operation (query); params: none; returns: "Classifier"; stub - metamodel metadata only
        ]
        """
        raise NotImplementedError

class RemoveStructuralFeatureValueAction(WriteStructuralFeatureAction):
    """A RemoveStructuralFeatureValueAction is a WriteStructuralFeatureAction that removes values from a StructuralFeature."""
    _PKG = "Actions"
    _DECL = {
    # Specifies whether to remove duplicates of the value in nonunique StructuralFeatures.
    'isRemoveDuplicates': _Ref('isRemoveDuplicates', bool),
    # An InputPin that provides the position of an existing value to remove in ordered, nonunique stru
    # ctural features. The type of the removeAt InputPin is UnlimitedNatural, but the value cannot be 
    # zero or unlimited.
    'removeAt': _Ref('removeAt', "InputPin", composite=True, subsets=("input",), assoc="A_removeAt_removeStructuralFeatureValueAction"),
    }
    _UNIONS = {
        "input": ("removeAt",),
        "ownedElement": ("removeAt",),
    }
    CONSTRAINTS = (
        ("removeAt_and_value",
         "if structuralFeature.isOrdered and not structuralFeature.isUnique and not isRemoveDuplic"
         "ates then value = null and removeAt <> null and removeAt.type = UnlimitedNatural and rem"
         "oveAt.is(1,1) else removeAt = null and value <> null endif"
        ),
    )

class RemoveVariableValueAction(WriteVariableAction):
    """A RemoveVariableValueAction is a WriteVariableAction that removes values from a Variables."""
    _PKG = "Actions"
    _DECL = {
    # Specifies whether to remove duplicates of the value in nonunique Variables.
    'isRemoveDuplicates': _Ref('isRemoveDuplicates', bool),
    # An InputPin that provides the position of an existing value to remove in ordered, nonunique Vari
    # ables. The type of the removeAt InputPin is UnlimitedNatural, but the value cannot be zero or un
    # limited.
    'removeAt': _Ref('removeAt', "InputPin", composite=True, subsets=("input",), assoc="A_removeAt_removeVariableValueAction"),
    }
    _UNIONS = {
        "input": ("removeAt",),
        "ownedElement": ("removeAt",),
    }
    CONSTRAINTS = (
        ("removeAt_and_value",
         "if variable.isOrdered and not variable.isUnique and not isRemoveDuplicates then value = "
         "null and removeAt <> null and removeAt.type = UnlimitedNatural and removeAt.is(1,1) else"
         " removeAt = null and value <> null endif"
        ),
    )

class ReplyAction(Action):
    """A ReplyAction is an Action that accepts a set of reply values and a value containing return information produced by a previous AcceptCallAction. The ReplyAction returns the values to the caller of the previous call, completing execution of the call."""
    _PKG = "Actions"
    _DECL = {
    # The Trigger specifying the Operation whose call is being replied to.
    'replyToCall': _Ref('replyToCall', "Trigger", assoc="A_replyToCall_replyAction"),
    # A list of InputPins providing the values for the output (inout, out, and return) Parameters of t
    # he Operation. These values are returned to the caller.
    'replyValue': _Ref('replyValue', "InputPin", composite=True, multi=True, lo=0, hi='*', subsets=("input",), assoc="A_replyValue_replyAction"),
    # An InputPin that holds the return information value produced by an earlier AcceptCallAction.
    'returnInformation': _Ref('returnInformation', "InputPin", composite=True, subsets=("input",), assoc="A_returnInformation_replyAction"),
    }
    _UNIONS = {
        "input": ("replyValue", "returnInformation",),
        "ownedElement": ("replyValue", "returnInformation",),
    }
    CONSTRAINTS = (
        ("pins_match_parameter",
         "let parameter:OrderedSet(Parameter) = replyToCall.event.oclAsType(CallEvent).operation.o"
         "utputParameters() in replyValue->size()=parameter->size() and Sequence{1..replyValue->si"
         "ze()}->forAll(i | replyValue->at(i).type.conformsTo(parameter->at(i).type) and replyValu"
         "e->at(i).isOrdered=parameter->at(i).isOrdered and replyValue->at(i).compatibleWith(param"
         "eter->at(i)))"
        ),
        ("event_on_reply_to_call_trigger",
         "replyToCall.event.oclIsKindOf(CallEvent)"
        ),
    )

class SendObjectAction(InvocationAction):
    """A SendObjectAction is an InvocationAction that transmits an input object to the target object, which is handled as a request message by the target object. The requestor continues execution immediately after the object is sent out and cannot receive reply values."""
    _PKG = "Actions"
    _DECL = {
    # The request object, which is transmitted to the target object. The object may be copied in trans
    # mission, so identity might not be preserved.
    'request': _Ref('request', "InputPin", composite=True, redefines=("argument",), assoc="A_request_sendObjectAction"),
    # The target object to which the object is sent.
    'target': _Ref('target', "InputPin", composite=True, subsets=("input",), assoc="A_target_sendObjectAction"),
    }
    _UNIONS = {
        "input": ("target",),
        "ownedElement": ("target",),
    }
    CONSTRAINTS = (
        ("type_target_pin",
         "onPort<>null implies target.type.oclAsType(Classifier).allFeatures()->includes(onPort)"
        ),
    )

class SendSignalAction(InvocationAction):
    """A SendSignalAction is an InvocationAction that creates a Signal instance and transmits it to the target object. Values from the argument InputPins are used to provide values for the attributes of the Signal. The requestor continues execution immediately after the Signal instance is sent out and cannot receive reply values."""
    _PKG = "Actions"
    _DECL = {
    # The Signal whose instance is transmitted to the target.
    'signal': _Ref('signal', "Signal", assoc="A_signal_sendSignalAction"),
    # The InputPin that provides the target object to which the Signal instance is sent.
    'target': _Ref('target', "InputPin", composite=True, subsets=("input",), assoc="A_target_sendSignalAction"),
    }
    _UNIONS = {
        "input": ("target",),
        "ownedElement": ("target",),
    }
    CONSTRAINTS = (
        ("type_ordering_multiplicity",
         "let attribute: OrderedSet(Property) = signal.allAttributes() in Sequence{1..argument->si"
         "ze()}->forAll(i | argument->at(i).type.conformsTo(attribute->at(i).type) and argument->a"
         "t(i).isOrdered = attribute->at(i).isOrdered and argument->at(i).compatibleWith(attribute"
         "->at(i)))"
        ),
        ("number_order",
         "argument->size()=signal.allAttributes()->size()"
        ),
        ("type_target_pin",
         "not onPort->isEmpty() implies target.type.oclAsType(Classifier).allFeatures()->includes("
         "onPort)"
        ),
    )

class SequenceNode(StructuredActivityNode):
    """A SequenceNode is a StructuredActivityNode that executes a sequence of ExecutableNodes in order."""
    _PKG = "Actions"
    _DECL = {
    # The ordered set of ExecutableNodes to be sequenced.
    'executableNode': _Ref('executableNode', "ExecutableNode", composite=True, multi=True, lo=0, hi='*', redefines=("node",), assoc="A_executableNode_sequenceNode"),
    }

class Signal(Classifier):
    """A Signal is a specification of a kind of communication between objects in which a reaction is asynchronously triggered in the receiver without a reply."""
    _PKG = "SimpleClassifiers"
    _DECL = {
    # The attributes owned by the Signal.
    'ownedAttribute': _Ref('ownedAttribute', "Property", composite=True, multi=True, lo=0, hi='*', subsets=("attribute", "ownedMember",), assoc="A_ownedAttribute_owningSignal"),
    }
    _UNIONS = {
        "attribute": ("ownedAttribute",),
        "feature": ("ownedAttribute",),
        "member": ("ownedAttribute",),
        "ownedElement": ("ownedAttribute",),
        "ownedMember": ("ownedAttribute",),
        "redefinableElement": ("ownedAttribute",),
    }

class SignalEvent(MessageEvent):
    """A SignalEvent represents the receipt of an asynchronous Signal instance."""
    _PKG = "CommonBehavior"
    _DECL = {
    # The specific Signal that is associated with this SignalEvent.
    'signal': _Ref('signal', "Signal", assoc="A_signal_signalEvent"),
    }

class Slot(Element):
    """A Slot designates that an entity modeled by an InstanceSpecification has a value or values for a specific StructuralFeature."""
    _PKG = "Classification"
    _DECL = {
    # The StructuralFeature that specifies the values that may be held by the Slot.
    'definingFeature': _Ref('definingFeature', "StructuralFeature", assoc="A_definingFeature_slot"),
    # The InstanceSpecification that owns this Slot.
    'owningInstance': _Ref('owningInstance', "InstanceSpecification", subsets=("owner",), assoc="A_slot_owningInstance"),
    # The value or values held by the Slot.
    'value': _Ref('value', "ValueSpecification", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_value_owningSlot"),
    }
    _UNIONS = {
        "ownedElement": ("value",),
        "owner": ("owningInstance",),
    }

class StartClassifierBehaviorAction(Action):
    """A StartClassifierBehaviorAction is an Action that starts the classifierBehavior of the input object."""
    _PKG = "Actions"
    _DECL = {
    # The InputPin that holds the object whose classifierBehavior is to be started.
    'object': _Ref('object', "InputPin", composite=True, subsets=("input",), assoc="A_object_startClassifierBehaviorAction"),
    }
    _UNIONS = {
        "input": ("object",),
        "ownedElement": ("object",),
    }
    CONSTRAINTS = (
        ("multiplicity",
         "object.is(1,1)"
        ),
        ("type_has_classifier",
         "object.type->notEmpty() implies (object.type.oclIsKindOf(BehavioredClassifier) and objec"
         "t.type.oclAsType(BehavioredClassifier).classifierBehavior<>null)"
        ),
    )

class StartObjectBehaviorAction(CallAction):
    """A StartObjectBehaviorAction is an InvocationAction that starts the execution either of a directly instantiated Behavior or of the classifierBehavior of an object. Argument values may be supplied for the input Parameters of the Behavior. If the Behavior is invoked synchronously, then output values may be obtained for output Parameters."""
    _PKG = "Actions"
    _DECL = {
    # An InputPin that holds the object that is either a Behavior to be started or has a classifierBeh
    # avior to be started.
    'object': _Ref('object', "InputPin", composite=True, subsets=("input",), assoc="A_object_startObjectBehaviorAction"),
    }
    _UNIONS = {
        "input": ("object",),
        "ownedElement": ("object",),
    }
    CONSTRAINTS = (
        ("multiplicity_of_object",
         "object.is(1,1)"
        ),
        ("type_of_object",
         "self.behavior()<>null"
        ),
        ("no_onport",
         "onPort->isEmpty()"
        ),
    )
    def outputParameters(self) -> "Parameter":
        """
        Return the inout, out and return ownedParameters of the Behavior being called.
        [StartObjectBehaviorAction operation (query); params: none; returns: "Parameter"; stub - metam
        odel metadata only]
        """
        raise NotImplementedError
    def inputParameters(self) -> "Parameter":
        """
        Return the in and inout ownedParameters of the Behavior being called.
        [StartObjectBehaviorAction operation (query); params: none; returns: "Parameter"; stub - metam
        odel metadata only]
        """
        raise NotImplementedError
    def behavior(self) -> "Behavior":
        """
        If the type of the object InputPin is a Behavior, then that Behavior. Otherwise, if the type o
        f the object InputPin is a BehavioredClassifier, then the classifierBehavior of that Behaviore
        dClassifier.
        [StartObjectBehaviorAction operation (query); params: none; returns: "Behavior"; stub - metamo
        del metadata only]
        """
        raise NotImplementedError

class StateInvariant(InteractionFragment):
    """A StateInvariant is a runtime constraint on the participants of the Interaction. It may be used to specify a variety of different kinds of Constraints, such as values of Attributes or Variables, internal or external States, and so on. A StateInvariant is an InteractionFragment and it is placed on a Lifeline."""
    _PKG = "Interactions"
    _DECL = {
    # References the Lifeline on which the StateInvariant appears.
    'covered': _Ref('covered', "Lifeline", redefines=("covered",), assoc="A_covered_stateInvariant"),
    # A Constraint that should hold at runtime for this StateInvariant.
    'invariant': _Ref('invariant', "Constraint", composite=True, subsets=("ownedElement",), assoc="A_invariant_stateInvariant"),
    }
    _UNIONS = {
        "ownedElement": ("invariant",),
    }

class Stereotype(Class):
    """A stereotype defines how an existing metaclass may be extended, and enables the use of platform or domain specific terminology or notation in place of, or in addition to, the ones used for the extended metaclass."""
    _PKG = "Packages"
    _DECL = {
    # Stereotype can change the graphical appearance of the extended model element by using attached i
    # cons. When this association is not null, it references the location of the icon content to be di
    # splayed within diagrams presenting the extended model elements.
    'icon': _Ref('icon', "Image", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_icon_stereotype"),
    # The profile that directly or indirectly contains this stereotype.
    'profile': _Ref('profile', "Profile", derived=True, readonly=True, assoc="A_profile_stereotype"),
    }
    _UNIONS = {
        "ownedElement": ("icon",),
    }
    CONSTRAINTS = (
        ("binaryAssociationsOnly",
         "ownedAttribute.association->forAll(memberEnd->size()=2)"
        ),
        ("generalize",
         "allParents()->forAll(oclIsKindOf(Stereotype)) and Classifier.allInstances()->forAll(c | "
         "c.allParents()->exists(oclIsKindOf(Stereotype)) implies c.oclIsKindOf(Stereotype))"
        ),
        ("name_not_clash",
         "(no specification serialized)"
        ),
        ("associationEndOwnership",
         "ownedAttribute ->select(association->notEmpty() and not association.oclIsKindOf(Extensio"
         "n) and not type.oclIsKindOf(Stereotype)) ->forAll(opposite.owner = association)"
        ),
        ("base_property_upper_bound",
         "(no specification serialized)"
        ),
        ("base_property_multiplicity_single_extension",
         "(no specification serialized)"
        ),
        ("base_property_multiplicity_multiple_extension",
         "(no specification serialized)"
        ),
    )
    def containingProfile(self) -> "Profile":
        """
        The query containingProfile returns the closest profile directly or indirectly containing this
         stereotype.
        [Stereotype operation (query); params: none; returns: "Profile"; stub - metamodel metadata onl
        y]
        """
        raise NotImplementedError
    def profile(self) -> "Profile":
        """
        A stereotype must be contained, directly or indirectly, in a profile.
        [Stereotype operation (query); params: none; returns: "Profile"; stub - metamodel metadata onl
        y]
        """
        raise NotImplementedError

class StringExpression(Expression, TemplateableElement):
    """A StringExpression is an Expression that specifies a String value that is derived by concatenating a sequence of operands with String values or a sequence of subExpressions, some of which might be template parameters."""
    _PKG = "Values"
    _DECL = {
    # The StringExpression of which this StringExpression is a subExpression.
    'owningExpression': _Ref('owningExpression', "StringExpression", subsets=("owner",), assoc="A_subExpression_owningExpression"),
    # The StringExpressions that constitute this StringExpression.
    'subExpression': _Ref('subExpression', "StringExpression", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_subExpression_owningExpression"),
    }
    _UNIONS = {
        "ownedElement": ("subExpression",),
        "owner": ("owningExpression",),
    }
    CONSTRAINTS = (
        ("operands",
         "operand->forAll (oclIsKindOf (LiteralString))"
        ),
        ("subexpressions",
         "if subExpression->notEmpty() then operand->isEmpty() else operand->notEmpty() endif"
        ),
    )
    def stringValue(self) -> str:
        """
        The query stringValue() returns the String resulting from concatenating, in order, all the com
        ponent String values of all the operands or subExpressions that are part of the StringExpressi
        on.
        [StringExpression operation (query); params: none; returns: str; stub - metamodel metadata onl
        y]
        """
        raise NotImplementedError

class Substitution(Realization):
    """A substitution is a relationship between two classifiers signifying that the substituting classifier complies with the contract specified by the contract classifier. This implies that instances of the substituting classifier are runtime substitutable where instances of the contract classifier are expected."""
    _PKG = "Classification"
    _DECL = {
    # The contract with which the substituting classifier complies.
    'contract': _Ref('contract', "Classifier", subsets=("supplier",), assoc="A_contract_substitution"),
    # Instances of the substituting classifier are runtime substitutable where instances of the contra
    # ct classifier are expected.
    'substitutingClassifier': _Ref('substitutingClassifier', "Classifier", subsets=("client", "owner",), assoc="A_substitution_substitutingClassifier"),
    }
    _UNIONS = {
        "owner": ("substitutingClassifier",),
        "relatedElement": ("contract", "substitutingClassifier",),
        "source": ("substitutingClassifier",),
        "target": ("contract",),
    }

class TemplateBinding(DirectedRelationship):
    """A TemplateBinding is a DirectedRelationship between a TemplateableElement and a template. A TemplateBinding specifies the TemplateParameterSubstitutions of actual parameters for the formal parameters of the template."""
    _PKG = "CommonStructure"
    _DECL = {
    # The TemplateableElement that is bound by this TemplateBinding.
    'boundElement': _Ref('boundElement', "TemplateableElement", subsets=("source", "owner",), assoc="A_templateBinding_boundElement"),
    # The TemplateParameterSubstitutions owned by this TemplateBinding.
    'parameterSubstitution': _Ref('parameterSubstitution', "TemplateParameterSubstitution", composite=True, multi=True, lo=0, hi='*', subsets=("ownedElement",), assoc="A_parameterSubstitution_templateBinding"),
    # The TemplateSignature for the template that is the target of this TemplateBinding.
    'signature': _Ref('signature', "TemplateSignature", subsets=("target",), assoc="A_signature_templateBinding"),
    }
    _UNIONS = {
        "ownedElement": ("parameterSubstitution",),
        "owner": ("boundElement",),
        "relatedElement": ("boundElement", "signature",),
        "source": ("boundElement",),
        "target": ("signature",),
    }
    CONSTRAINTS = (
        ("parameter_substitution_formal",
         "parameterSubstitution->forAll(b | signature.parameter->includes(b.formal))"
        ),
        ("one_parameter_substitution",
         "signature.parameter->forAll(p | parameterSubstitution->select(b | b.formal = p)->size() "
         "<= 1)"
        ),
    )

class TemplateParameterSubstitution(Element):
    """A TemplateParameterSubstitution relates the actual parameter to a formal TemplateParameter as part of a template binding."""
    _PKG = "CommonStructure"
    _DECL = {
    # The ParameterableElement that is the actual parameter for this TemplateParameterSubstitution.
    'actual': _Ref('actual', "ParameterableElement", assoc="A_actual_templateParameterSubstitution"),
    # The formal TemplateParameter that is associated with this TemplateParameterSubstitution.
    'formal': _Ref('formal', "TemplateParameter", assoc="A_formal_templateParameterSubstitution"),
    # The ParameterableElement that is owned by this TemplateParameterSubstitution as its actual param
    # eter.
    'ownedActual': _Ref('ownedActual', "ParameterableElement", composite=True, subsets=("ownedElement", "actual",), assoc="A_ownedActual_owningTemplateParameterSubstitution"),
    # The TemplateBinding that owns this TemplateParameterSubstitution.
    'templateBinding': _Ref('templateBinding', "TemplateBinding", subsets=("owner",), assoc="A_parameterSubstitution_templateBinding"),
    }
    _UNIONS = {
        "ownedElement": ("ownedActual",),
        "owner": ("templateBinding",),
    }
    CONSTRAINTS = (
        ("must_be_compatible",
         "actual->forAll(a | a.isCompatibleWith(formal.parameteredElement))"
        ),
    )

class TestIdentityAction(Action):
    """A TestIdentityAction is an Action that tests if two values are identical objects."""
    _PKG = "Actions"
    _DECL = {
    # The InputPin on which the first input object is placed.
    'first': _Ref('first', "InputPin", composite=True, subsets=("input",), assoc="A_first_testIdentityAction"),
    # The OutputPin whose Boolean value indicates whether the two input objects are identical.
    'result': _Ref('result', "OutputPin", composite=True, subsets=("output",), assoc="A_result_testIdentityAction"),
    # The OutputPin on which the second input object is placed.
    'second': _Ref('second', "InputPin", composite=True, subsets=("input",), assoc="A_second_testIdentityAction"),
    }
    _UNIONS = {
        "input": ("first", "second",),
        "output": ("result",),
        "ownedElement": ("first", "result", "second",),
    }
    CONSTRAINTS = (
        ("multiplicity",
         "first.is(1,1) and second.is(1,1)"
        ),
        ("no_type",
         "first.type= null and second.type = null"
        ),
        ("result_is_boolean",
         "result.type=Boolean"
        ),
    )

class TimeConstraint(IntervalConstraint):
    """A TimeConstraint is a Constraint that refers to a TimeInterval."""
    _PKG = "Values"
    _DECL = {
    # The value of firstEvent is related to the constrainedElement. If firstEvent is true, then the co
    # rresponding observation event is the first time instant the execution enters the constrainedElem
    # ent. If firstEvent is false, then the corresponding observation event is the last time instant t
    # he execution is within the constrainedElement.
    'firstEvent': _Ref('firstEvent', bool),
    # TheTimeInterval constraining the duration.
    'specification': _Ref('specification', "TimeInterval", composite=True, redefines=("specification",), assoc="A_specification_timeConstraint"),
    }
    CONSTRAINTS = (
        ("has_one_constrainedElement",
         "constrainedElement->size() = 1"
        ),
    )

class TimeEvent(Event):
    """A TimeEvent is an Event that occurs at a specific point in time."""
    _PKG = "CommonBehavior"
    _DECL = {
    # Specifies whether the TimeEvent is specified as an absolute or relative time.
    'isRelative': _Ref('isRelative', bool),
    # Specifies the time of the TimeEvent.
    'when': _Ref('when', "TimeExpression", composite=True, subsets=("ownedElement",), assoc="A_when_timeEvent"),
    }
    _UNIONS = {
        "ownedElement": ("when",),
    }
    CONSTRAINTS = (
        ("when_non_negative",
         "when.integerValue() >= 0"
        ),
    )

class TimeExpression(ValueSpecification):
    """A TimeExpression is a ValueSpecification that represents a time value."""
    _PKG = "Values"
    _DECL = {
    # A ValueSpecification that evaluates to the value of the TimeExpression.
    'expr': _Ref('expr', "ValueSpecification", composite=True, subsets=("ownedElement",), assoc="A_expr_timeExpression"),
    # Refers to the Observations that are involved in the computation of the TimeExpression value.
    'observation': _Ref('observation', "Observation", multi=True, lo=0, hi='*', assoc="A_observation_timeExpression"),
    }
    _UNIONS = {
        "ownedElement": ("expr",),
    }
    CONSTRAINTS = (
        ("no_expr_requires_observation",
         "expr = null implies (observation->size() = 1 and observation->forAll(oclIsKindOf(TimeObs"
         "ervation)))"
        ),
    )

class TimeInterval(Interval):
    """A TimeInterval defines the range between two TimeExpressions."""
    _PKG = "Values"
    _DECL = {
    # Refers to the TimeExpression denoting the maximum value of the range.
    'max': _Ref('max', "TimeExpression", redefines=("max",), assoc="A_max_timeInterval"),
    # Refers to the TimeExpression denoting the minimum value of the range.
    'min': _Ref('min', "TimeExpression", redefines=("min",), assoc="A_min_timeInterval"),
    }

class TimeObservation(Observation):
    """A TimeObservation is a reference to a time instant during an execution. It points out the NamedElement in the model to observe and whether the observation is when this NamedElement is entered or when it is exited."""
    _PKG = "Values"
    _DECL = {
    # The TimeObservation is determined by the entering or exiting of the event Element during executi
    # on.
    'event': _Ref('event', "NamedElement", assoc="A_event_timeObservation"),
    # The value of firstEvent is related to the event. If firstEvent is true, then the corresponding o
    # bservation event is the first time instant the execution enters the event Element. If firstEvent
    #  is false, then the corresponding observation event is the time instant the execution exits the 
    # event Element.
    'firstEvent': _Ref('firstEvent', bool),
    }

class Trigger(NamedElement):
    """A Trigger specifies a specific point at which an Event occurrence may trigger an effect in a Behavior. A Trigger may be qualified by the Port on which the Event occurred."""
    _PKG = "CommonBehavior"
    _DECL = {
    # The Event that detected by the Trigger.
    'event': _Ref('event', "Event", assoc="A_event_trigger"),
    # A optional Port of through which the given effect is detected.
    'port': _Ref('port', "Port", multi=True, lo=0, hi='*', assoc="A_port_trigger"),
    }
    CONSTRAINTS = (
        ("trigger_with_ports",
         "port->notEmpty() implies event.oclIsKindOf(MessageEvent)"
        ),
    )

class UnmarshallAction(Action):
    """An UnmarshallAction is an Action that retrieves the values of the StructuralFeatures of an object and places them on OutputPins."""
    _PKG = "Actions"
    _DECL = {
    # The InputPin that gives the object to be unmarshalled.
    'object': _Ref('object', "InputPin", composite=True, subsets=("input",), assoc="A_object_unmarshallAction"),
    # The OutputPins on which are placed the values of the StructuralFeatures of the input object.
    'result': _Ref('result', "OutputPin", composite=True, multi=True, lo=0, hi='*', subsets=("output",), assoc="A_result_unmarshallAction"),
    # The type of the object to be unmarshalled.
    'unmarshallType': _Ref('unmarshallType', "Classifier", assoc="A_unmarshallType_unmarshallAction"),
    }
    _UNIONS = {
        "input": ("object",),
        "output": ("result",),
        "ownedElement": ("object", "result",),
    }
    CONSTRAINTS = (
        ("structural_feature",
         "unmarshallType.allAttributes()->size() >= 1"
        ),
        ("number_of_result",
         "unmarshallType.allAttributes()->size() = result->size()"
        ),
        ("type_ordering_and_multiplicity",
         "let attribute:OrderedSet(Property) = unmarshallType.allAttributes() in Sequence{1..resul"
         "t->size()}->forAll(i | attribute->at(i).type.conformsTo(result->at(i).type) and attribut"
         "e->at(i).isOrdered=result->at(i).isOrdered and attribute->at(i).compatibleWith(result->a"
         "t(i)))"
        ),
        ("multiplicity_of_object",
         "object.is(1,1)"
        ),
        ("object_type",
         "object.type.conformsTo(unmarshallType)"
        ),
    )

class Usage(Dependency):
    """A Usage is a Dependency in which the client Element requires the supplier Element (or set of Elements) for its full implementation or operation."""
    _PKG = "CommonStructure"

class UseCase(BehavioredClassifier):
    """A UseCase specifies a set of actions performed by its subjects, which yields an observable result that is of value for one or more Actors or other stakeholders of each subject."""
    _PKG = "UseCases"
    _DECL = {
    # The Extend relationships owned by this UseCase.
    'extend': _Ref('extend', "Extend", composite=True, multi=True, lo=0, hi='*', subsets=("directedRelationship", "ownedMember",), assoc="A_extend_extension"),
    # The ExtensionPoints owned by this UseCase.
    'extensionPoint': _Ref('extensionPoint', "ExtensionPoint", composite=True, multi=True, lo=0, hi='*', subsets=("ownedMember",), assoc="A_extensionPoint_useCase"),
    # The Include relationships owned by this UseCase.
    'include': _Ref('include', "Include", composite=True, multi=True, lo=0, hi='*', subsets=("directedRelationship", "ownedMember",), assoc="A_include_includingCase"),
    # The subjects to which this UseCase applies. Each subject or its parts realize all the UseCases t
    # hat apply to it.
    'subject': _Ref('subject', "Classifier", multi=True, lo=0, hi='*', assoc="A_subject_useCase"),
    }
    _UNIONS = {
        "directedRelationship": ("extend", "include",),
        "member": ("extend", "extensionPoint", "include",),
        "ownedElement": ("extend", "extensionPoint", "include",),
        "ownedMember": ("extend", "extensionPoint", "include",),
        "relationship": ("extend", "include",),
    }
    CONSTRAINTS = (
        ("binary_associations",
         "Association.allInstances()->forAll(a | a.memberEnd.type->includes(self) implies a.member"
         "End->size() = 2)"
        ),
        ("no_association_to_use_case",
         "Association.allInstances()->forAll(a | a.memberEnd.type->includes(self) implies ( let us"
         "ecases: Set(UseCase) = a.memberEnd.type->select(oclIsKindOf(UseCase))->collect(oclAsType"
         "(UseCase))->asSet() in usecases->size() > 1 implies usecases->collect(subject)->size() >"
         " 1 ) )"
        ),
        ("cannot_include_self",
         "not allIncludedUseCases()->includes(self)"
        ),
        ("must_have_name",
         "name -> notEmpty ()"
        ),
    )
    def allIncludedUseCases(self) -> "UseCase":
        """
        The query allIncludedUseCases() returns the transitive closure of all UseCases (directly or in
        directly) included by this UseCase.
        [UseCase operation (query); params: none; returns: "UseCase"; stub - metamodel metadata only]
        """
        raise NotImplementedError

class ValuePin(InputPin):
    """A ValuePin is an InputPin that provides a value by evaluating a ValueSpecification."""
    _PKG = "Actions"
    _DECL = {
    # The ValueSpecification that is evaluated to obtain the value that the ValuePin will provide.
    'value': _Ref('value', "ValueSpecification", composite=True, subsets=("ownedElement",), assoc="A_value_valuePin"),
    }
    _UNIONS = {
        "ownedElement": ("value",),
    }
    CONSTRAINTS = (
        ("no_incoming_edges",
         "incoming->isEmpty()"
        ),
        ("compatible_type",
         "value.type.conformsTo(type)"
        ),
    )

class ValueSpecificationAction(Action):
    """A ValueSpecificationAction is an Action that evaluates a ValueSpecification and provides a result."""
    _PKG = "Actions"
    _DECL = {
    # The OutputPin on which the result value is placed.
    'result': _Ref('result', "OutputPin", composite=True, subsets=("output",), assoc="A_result_valueSpecificationAction"),
    # The ValueSpecification to be evaluated.
    'value': _Ref('value', "ValueSpecification", composite=True, subsets=("ownedElement",), assoc="A_value_valueSpecificationAction"),
    }
    _UNIONS = {
        "output": ("result",),
        "ownedElement": ("result", "value",),
    }
    CONSTRAINTS = (
        ("multiplicity",
         "result.is(1,1)"
        ),
        ("compatible_type",
         "value.type.conformsTo(result.type)"
        ),
    )

class Variable(ConnectableElement, MultiplicityElement):
    """A Variable is a ConnectableElement that may store values during the execution of an Activity. Reading and writing the values of a Variable provides an alternative means for passing data than the use of ObjectFlows. A Variable may be owned directly by an Activity, in which case it is accessible from anywhere within that activity, or it may be owned by a StructuredActivityNode, in which case it is only accessible within that node."""
    _PKG = "Activities"
    _DECL = {
    # An Activity that owns the Variable.
    'activityScope': _Ref('activityScope', "Activity", subsets=("namespace",), assoc="A_variable_activityScope"),
    # A StructuredActivityNode that owns the Variable.
    'scope': _Ref('scope', "StructuredActivityNode", subsets=("namespace",), assoc="A_variable_scope"),
    }
    _UNIONS = {
        "memberNamespace": ("activityScope", "scope",),
        "namespace": ("activityScope", "scope",),
        "owner": ("activityScope", "scope",),
    }
    def isAccessibleBy(self, a: "Action" = None) -> bool:
        """
        A Variable is accessible by Actions within its scope (the Activity or StructuredActivityNode t
        hat owns it).
        [Variable operation (query); params: a: "Action"; returns: bool; stub - metamodel metadata onl
        y]
        """
        raise NotImplementedError

# ---------------------------------------------------------------------------
# post-import assembly
# ---------------------------------------------------------------------------
_CLASSES = [Element, Relationship, DirectedRelationship, ParameterableElement, NamedElement, PackageableElement, Dependency, Abstraction, RedefinableElement, ActivityNode, ExecutableNode, Action, AcceptEventAction, AcceptCallAction, InteractionFragment, ExecutionSpecification, ActionExecutionSpecification, TypedElement, ObjectNode, MultiplicityElement, Pin, InputPin, ActionInputPin, Namespace, Type, TemplateableElement, Classifier, BehavioredClassifier, StructuredClassifier, EncapsulatedClassifier, Class, Behavior, Activity, ActivityEdge, ControlNode, FinalNode, ActivityFinalNode, ActivityGroup, ActivityParameterNode, ActivityPartition, Actor, StructuralFeatureAction, WriteStructuralFeatureAction, AddStructuralFeatureValueAction, VariableAction, WriteVariableAction, AddVariableValueAction, Event, MessageEvent, AnyReceiveEvent, DeployedArtifact, Artifact, Association, AssociationClass, BehaviorExecutionSpecification, Feature, BehavioralFeature, InvocationAction, BroadcastSignalAction, CallAction, CallBehaviorAction, CallEvent, CallOperationAction, CentralBufferNode, ChangeEvent, TemplateParameter, ClassifierTemplateParameter, Clause, ClearAssociationAction, ClearStructuralFeatureAction, ClearVariableAction, Collaboration, CollaborationUse, CombinedFragment, Comment, CommunicationPath, Component, Realization, ComponentRealization, StructuredActivityNode, ConditionalNode, ConnectableElement, ConnectableElementTemplateParameter, Vertex, ConnectionPointReference, Connector, ConnectorEnd, ConsiderIgnoreFragment, Constraint, Continuation, ControlFlow, LinkAction, WriteLinkAction, CreateLinkAction, CreateLinkObjectAction, CreateObjectAction, DataStoreNode, DataType, DecisionNode, Deployment, DeploymentSpecification, DeploymentTarget, DestroyLinkAction, DestroyObjectAction, MessageEnd, OccurrenceSpecification, MessageOccurrenceSpecification, DestructionOccurrenceSpecification, Node, Device, ValueSpecification, Duration, IntervalConstraint, DurationConstraint, Interval, DurationInterval, Observation, DurationObservation, ElementImport, Enumeration, InstanceSpecification, EnumerationLiteral, ExceptionHandler, ExecutionEnvironment, ExecutionOccurrenceSpecification, ExpansionNode, ExpansionRegion, Expression, Extend, Extension, StructuralFeature, Property, ExtensionEnd, ExtensionPoint, State, FinalState, FlowFinalNode, ForkNode, OpaqueBehavior, FunctionBehavior, Gate, GeneralOrdering, Generalization, GeneralizationSet, Image, Include, InformationFlow, InformationItem, InitialNode, InstanceValue, Interaction, InteractionConstraint, InteractionOperand, InteractionUse, Interface, InterfaceRealization, InterruptibleActivityRegion, JoinNode, Lifeline, LinkEndData, LinkEndCreationData, LinkEndDestructionData, LiteralSpecification, LiteralBoolean, LiteralInteger, LiteralNull, LiteralReal, LiteralString, LiteralUnlimitedNatural, LoopNode, Manifestation, MergeNode, Message, Package, Model, ObjectFlow, OpaqueAction, OpaqueExpression, Operation, OperationTemplateParameter, OutputPin, PackageImport, PackageMerge, Parameter, ParameterSet, PartDecomposition, Port, PrimitiveType, Profile, ProfileApplication, ProtocolConformance, StateMachine, ProtocolStateMachine, Transition, ProtocolTransition, Pseudostate, QualifierValue, RaiseExceptionAction, ReadExtentAction, ReadIsClassifiedObjectAction, ReadLinkAction, ReadLinkObjectEndAction, ReadLinkObjectEndQualifierAction, ReadSelfAction, ReadStructuralFeatureAction, ReadVariableAction, Reception, ReclassifyObjectAction, TemplateSignature, RedefinableTemplateSignature, ReduceAction, Region, RemoveStructuralFeatureValueAction, RemoveVariableValueAction, ReplyAction, SendObjectAction, SendSignalAction, SequenceNode, Signal, SignalEvent, Slot, StartClassifierBehaviorAction, StartObjectBehaviorAction, StateInvariant, Stereotype, StringExpression, Substitution, TemplateBinding, TemplateParameterSubstitution, TestIdentityAction, TimeConstraint, TimeEvent, TimeExpression, TimeInterval, TimeObservation, Trigger, UnmarshallAction, Usage, UseCase, ValuePin, ValueSpecificationAction, Variable]
_OPPOSITES = {
    ("Activity", "edge"): ("ActivityEdge", "activity"),
    ("Activity", "group"): ("ActivityGroup", "inActivity"),
    ("Activity", "node"): ("ActivityNode", "activity"),
    ("Activity", "structuredNode"): ("StructuredActivityNode", "activity"),
    ("Activity", "variable"): ("Variable", "activityScope"),
    ("ActivityEdge", "activity"): ("Activity", "edge"),
    ("ActivityEdge", "inGroup"): ("ActivityGroup", "containedEdge"),
    ("ActivityEdge", "inPartition"): ("ActivityPartition", "edge"),
    ("ActivityEdge", "inStructuredNode"): ("StructuredActivityNode", "edge"),
    ("ActivityEdge", "interrupts"): ("InterruptibleActivityRegion", "interruptingEdge"),
    ("ActivityEdge", "source"): ("ActivityNode", "outgoing"),
    ("ActivityEdge", "target"): ("ActivityNode", "incoming"),
    ("ActivityGroup", "containedEdge"): ("ActivityEdge", "inGroup"),
    ("ActivityGroup", "containedNode"): ("ActivityNode", "inGroup"),
    ("ActivityGroup", "inActivity"): ("Activity", "group"),
    ("ActivityGroup", "subgroup"): ("ActivityGroup", "superGroup"),
    ("ActivityGroup", "superGroup"): ("ActivityGroup", "subgroup"),
    ("ActivityNode", "activity"): ("Activity", "node"),
    ("ActivityNode", "inGroup"): ("ActivityGroup", "containedNode"),
    ("ActivityNode", "inInterruptibleRegion"): ("InterruptibleActivityRegion", "node"),
    ("ActivityNode", "inPartition"): ("ActivityPartition", "node"),
    ("ActivityNode", "inStructuredNode"): ("StructuredActivityNode", "node"),
    ("ActivityNode", "incoming"): ("ActivityEdge", "target"),
    ("ActivityNode", "outgoing"): ("ActivityEdge", "source"),
    ("ActivityPartition", "edge"): ("ActivityEdge", "inPartition"),
    ("ActivityPartition", "node"): ("ActivityNode", "inPartition"),
    ("ActivityPartition", "subpartition"): ("ActivityPartition", "superPartition"),
    ("ActivityPartition", "superPartition"): ("ActivityPartition", "subpartition"),
    ("Association", "memberEnd"): ("Property", "association"),
    ("Association", "ownedEnd"): ("Property", "owningAssociation"),
    ("Behavior", "specification"): ("BehavioralFeature", "method"),
    ("BehavioralFeature", "method"): ("Behavior", "specification"),
    ("BehavioredClassifier", "interfaceRealization"): ("InterfaceRealization", "implementingClassifier"),
    ("Class", "extension"): ("Extension", "metaclass"),
    ("Class", "ownedAttribute"): ("Property", "class_"),
    ("Class", "ownedOperation"): ("Operation", "class_"),
    ("Classifier", "feature"): ("Feature", "featuringClassifier"),
    ("Classifier", "generalization"): ("Generalization", "specific"),
    ("Classifier", "ownedTemplateSignature"): ("RedefinableTemplateSignature", "classifier"),
    ("Classifier", "powertypeExtent"): ("GeneralizationSet", "powertype"),
    ("Classifier", "substitution"): ("Substitution", "substitutingClassifier"),
    ("Classifier", "templateParameter"): ("ClassifierTemplateParameter", "parameteredElement"),
    ("Classifier", "useCase"): ("UseCase", "subject"),
    ("ClassifierTemplateParameter", "parameteredElement"): ("Classifier", "templateParameter"),
    ("Clause", "predecessorClause"): ("Clause", "successorClause"),
    ("Clause", "successorClause"): ("Clause", "predecessorClause"),
    ("Component", "realization"): ("ComponentRealization", "abstraction"),
    ("ComponentRealization", "abstraction"): ("Component", "realization"),
    ("ConnectableElement", "end"): ("ConnectorEnd", "role"),
    ("ConnectableElement", "templateParameter"): ("ConnectableElementTemplateParameter", "parameteredElement"),
    ("ConnectableElementTemplateParameter", "parameteredElement"): ("ConnectableElement", "templateParameter"),
    ("ConnectionPointReference", "state"): ("State", "connection"),
    ("ConnectorEnd", "role"): ("ConnectableElement", "end"),
    ("Constraint", "context"): ("Namespace", "ownedRule"),
    ("DataType", "ownedAttribute"): ("Property", "datatype"),
    ("DataType", "ownedOperation"): ("Operation", "datatype"),
    ("Dependency", "client"): ("NamedElement", "clientDependency"),
    ("Deployment", "configuration"): ("DeploymentSpecification", "deployment"),
    ("Deployment", "location"): ("DeploymentTarget", "deployment"),
    ("DeploymentSpecification", "deployment"): ("Deployment", "configuration"),
    ("DeploymentTarget", "deployment"): ("Deployment", "location"),
    ("Element", "ownedElement"): ("Element", "owner"),
    ("Element", "owner"): ("Element", "ownedElement"),
    ("ElementImport", "importingNamespace"): ("Namespace", "elementImport"),
    ("Enumeration", "ownedLiteral"): ("EnumerationLiteral", "enumeration"),
    ("EnumerationLiteral", "enumeration"): ("Enumeration", "ownedLiteral"),
    ("ExceptionHandler", "protectedNode"): ("ExecutableNode", "handler"),
    ("ExecutableNode", "handler"): ("ExceptionHandler", "protectedNode"),
    ("ExpansionNode", "regionAsInput"): ("ExpansionRegion", "inputElement"),
    ("ExpansionNode", "regionAsOutput"): ("ExpansionRegion", "outputElement"),
    ("ExpansionRegion", "inputElement"): ("ExpansionNode", "regionAsInput"),
    ("ExpansionRegion", "outputElement"): ("ExpansionNode", "regionAsOutput"),
    ("Extend", "extension"): ("UseCase", "extend"),
    ("Extension", "metaclass"): ("Class", "extension"),
    ("ExtensionPoint", "useCase"): ("UseCase", "extensionPoint"),
    ("Feature", "featuringClassifier"): ("Classifier", "feature"),
    ("GeneralOrdering", "after"): ("OccurrenceSpecification", "toBefore"),
    ("GeneralOrdering", "before"): ("OccurrenceSpecification", "toAfter"),
    ("Generalization", "generalizationSet"): ("GeneralizationSet", "generalization"),
    ("Generalization", "specific"): ("Classifier", "generalization"),
    ("GeneralizationSet", "generalization"): ("Generalization", "generalizationSet"),
    ("GeneralizationSet", "powertype"): ("Classifier", "powertypeExtent"),
    ("Include", "includingCase"): ("UseCase", "include"),
    ("InstanceSpecification", "slot"): ("Slot", "owningInstance"),
    ("Interaction", "fragment"): ("InteractionFragment", "enclosingInteraction"),
    ("Interaction", "lifeline"): ("Lifeline", "interaction"),
    ("Interaction", "message"): ("Message", "interaction"),
    ("InteractionFragment", "covered"): ("Lifeline", "coveredBy"),
    ("InteractionFragment", "enclosingInteraction"): ("Interaction", "fragment"),
    ("InteractionFragment", "enclosingOperand"): ("InteractionOperand", "fragment"),
    ("InteractionOperand", "fragment"): ("InteractionFragment", "enclosingOperand"),
    ("Interface", "ownedAttribute"): ("Property", "interface"),
    ("Interface", "ownedOperation"): ("Operation", "interface"),
    ("InterfaceRealization", "implementingClassifier"): ("BehavioredClassifier", "interfaceRealization"),
    ("InterruptibleActivityRegion", "interruptingEdge"): ("ActivityEdge", "interrupts"),
    ("InterruptibleActivityRegion", "node"): ("ActivityNode", "inInterruptibleRegion"),
    ("Lifeline", "coveredBy"): ("InteractionFragment", "covered"),
    ("Lifeline", "interaction"): ("Interaction", "lifeline"),
    ("Message", "interaction"): ("Interaction", "message"),
    ("NamedElement", "clientDependency"): ("Dependency", "client"),
    ("NamedElement", "namespace"): ("Namespace", "ownedMember"),
    ("Namespace", "elementImport"): ("ElementImport", "importingNamespace"),
    ("Namespace", "ownedMember"): ("NamedElement", "namespace"),
    ("Namespace", "ownedRule"): ("Constraint", "context"),
    ("Namespace", "packageImport"): ("PackageImport", "importingNamespace"),
    ("OccurrenceSpecification", "toAfter"): ("GeneralOrdering", "before"),
    ("OccurrenceSpecification", "toBefore"): ("GeneralOrdering", "after"),
    ("Operation", "class"): ("Class", "ownedOperation"),
    ("Operation", "datatype"): ("DataType", "ownedOperation"),
    ("Operation", "interface"): ("Interface", "ownedOperation"),
    ("Operation", "ownedParameter"): ("Parameter", "operation"),
    ("Operation", "templateParameter"): ("OperationTemplateParameter", "parameteredElement"),
    ("OperationTemplateParameter", "parameteredElement"): ("Operation", "templateParameter"),
    ("Package", "nestedPackage"): ("Package", "nestingPackage"),
    ("Package", "nestingPackage"): ("Package", "nestedPackage"),
    ("Package", "ownedType"): ("Type", "package"),
    ("Package", "packageMerge"): ("PackageMerge", "receivingPackage"),
    ("Package", "profileApplication"): ("ProfileApplication", "applyingPackage"),
    ("PackageImport", "importingNamespace"): ("Namespace", "packageImport"),
    ("PackageMerge", "receivingPackage"): ("Package", "packageMerge"),
    ("Parameter", "operation"): ("Operation", "ownedParameter"),
    ("Parameter", "parameterSet"): ("ParameterSet", "parameter"),
    ("ParameterSet", "parameter"): ("Parameter", "parameterSet"),
    ("ParameterableElement", "owningTemplateParameter"): ("TemplateParameter", "ownedParameteredElement"),
    ("ParameterableElement", "templateParameter"): ("TemplateParameter", "parameteredElement"),
    ("ProfileApplication", "applyingPackage"): ("Package", "profileApplication"),
    ("Property", "association"): ("Association", "memberEnd"),
    ("Property", "associationEnd"): ("Property", "qualifier"),
    ("Property", "class"): ("Class", "ownedAttribute"),
    ("Property", "datatype"): ("DataType", "ownedAttribute"),
    ("Property", "interface"): ("Interface", "ownedAttribute"),
    ("Property", "owningAssociation"): ("Association", "ownedEnd"),
    ("Property", "qualifier"): ("Property", "associationEnd"),
    ("ProtocolConformance", "specificMachine"): ("ProtocolStateMachine", "conformance"),
    ("ProtocolStateMachine", "conformance"): ("ProtocolConformance", "specificMachine"),
    ("Pseudostate", "state"): ("State", "connectionPoint"),
    ("Pseudostate", "stateMachine"): ("StateMachine", "connectionPoint"),
    ("RedefinableTemplateSignature", "classifier"): ("Classifier", "ownedTemplateSignature"),
    ("Region", "state"): ("State", "region"),
    ("Region", "stateMachine"): ("StateMachine", "region"),
    ("Region", "subvertex"): ("Vertex", "container"),
    ("Region", "transition"): ("Transition", "container"),
    ("Slot", "owningInstance"): ("InstanceSpecification", "slot"),
    ("State", "connection"): ("ConnectionPointReference", "state"),
    ("State", "connectionPoint"): ("Pseudostate", "state"),
    ("State", "region"): ("Region", "state"),
    ("State", "submachine"): ("StateMachine", "submachineState"),
    ("StateMachine", "connectionPoint"): ("Pseudostate", "stateMachine"),
    ("StateMachine", "region"): ("Region", "stateMachine"),
    ("StateMachine", "submachineState"): ("State", "submachine"),
    ("StringExpression", "owningExpression"): ("StringExpression", "subExpression"),
    ("StringExpression", "subExpression"): ("StringExpression", "owningExpression"),
    ("StructuredActivityNode", "activity"): ("Activity", "structuredNode"),
    ("StructuredActivityNode", "edge"): ("ActivityEdge", "inStructuredNode"),
    ("StructuredActivityNode", "node"): ("ActivityNode", "inStructuredNode"),
    ("StructuredActivityNode", "variable"): ("Variable", "scope"),
    ("Substitution", "substitutingClassifier"): ("Classifier", "substitution"),
    ("TemplateBinding", "boundElement"): ("TemplateableElement", "templateBinding"),
    ("TemplateBinding", "parameterSubstitution"): ("TemplateParameterSubstitution", "templateBinding"),
    ("TemplateParameter", "ownedParameteredElement"): ("ParameterableElement", "owningTemplateParameter"),
    ("TemplateParameter", "parameteredElement"): ("ParameterableElement", "templateParameter"),
    ("TemplateParameter", "signature"): ("TemplateSignature", "ownedParameter"),
    ("TemplateParameterSubstitution", "templateBinding"): ("TemplateBinding", "parameterSubstitution"),
    ("TemplateSignature", "ownedParameter"): ("TemplateParameter", "signature"),
    ("TemplateSignature", "template"): ("TemplateableElement", "ownedTemplateSignature"),
    ("TemplateableElement", "ownedTemplateSignature"): ("TemplateSignature", "template"),
    ("TemplateableElement", "templateBinding"): ("TemplateBinding", "boundElement"),
    ("Transition", "container"): ("Region", "transition"),
    ("Transition", "source"): ("Vertex", "outgoing"),
    ("Transition", "target"): ("Vertex", "incoming"),
    ("Type", "package"): ("Package", "ownedType"),
    ("UseCase", "extend"): ("Extend", "extension"),
    ("UseCase", "extensionPoint"): ("ExtensionPoint", "useCase"),
    ("UseCase", "include"): ("Include", "includingCase"),
    ("UseCase", "subject"): ("Classifier", "useCase"),
    ("Variable", "activityScope"): ("Activity", "variable"),
    ("Variable", "scope"): ("StructuredActivityNode", "variable"),
    ("Vertex", "container"): ("Region", "subvertex"),
    ("Vertex", "incoming"): ("Transition", "target"),
    ("Vertex", "outgoing"): ("Transition", "source"),
}
_ABSTRACT_NAMES = {"Element", "Relationship", "DirectedRelationship", "ParameterableElement", "NamedElement", "PackageableElement", "RedefinableElement", "ActivityNode", "ExecutableNode", "Action", "InteractionFragment", "ExecutionSpecification", "TypedElement", "ObjectNode", "MultiplicityElement", "Pin", "Namespace", "Type", "TemplateableElement", "Classifier", "BehavioredClassifier", "StructuredClassifier", "EncapsulatedClassifier", "Behavior", "ActivityEdge", "ControlNode", "FinalNode", "ActivityGroup", "StructuralFeatureAction", "WriteStructuralFeatureAction", "VariableAction", "WriteVariableAction", "Event", "MessageEvent", "DeployedArtifact", "Feature", "BehavioralFeature", "InvocationAction", "CallAction", "ConnectableElement", "Vertex", "LinkAction", "WriteLinkAction", "DeploymentTarget", "MessageEnd", "ValueSpecification", "Observation", "StructuralFeature", "LiteralSpecification"}

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

_ENUMS = {"AggregationKind": AggregationKind, "CallConcurrencyKind": CallConcurrencyKind, "ConnectorKind": ConnectorKind, "ExpansionKind": ExpansionKind, "InteractionOperatorKind": InteractionOperatorKind, "MessageKind": MessageKind, "MessageSort": MessageSort, "ObjectNodeOrderingKind": ObjectNodeOrderingKind, "ParameterDirectionKind": ParameterDirectionKind, "ParameterEffectKind": ParameterEffectKind, "PseudostateKind": PseudostateKind, "TransitionKind": TransitionKind, "VisibilityKind": VisibilityKind}

