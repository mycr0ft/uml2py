"""Stereotype classes generated from OMG profile XMI files.

Sources: StandardProfile.xmi (UML 2.5.1 Standard Profile) and sysml.xmi
(SysML v1 profile, URI https://www.omg.org/spec/SysML/20240101).

Contents: 89 stereotype classes, 52 tagged values,
143 profile constraints (metadata). Each stereotype folds its
base metaclasses (Python inheritance) with stereotype generalizations;
base_* extension ends are consumed, and extension required/optional
data is carried in _EXTENSIONS.
"""
from __future__ import annotations
import enum as _enum

from gen import uml25 as U
from gen.uml25 import _Ref  # noqa: F401

class ControlValueKind(_enum.Enum):
    disable = "disable"
    enable = "enable"

class FeatureDirectionKind(_enum.Enum):
    provided = "provided"
    providedRequired = "providedRequired"
    required = "required"

class FlowDirectionKind(_enum.Enum):
    in_ = "in"
    inout = "inout"
    out = "out"

class VerdictKind(_enum.Enum):
    error = "error"
    fail = "fail"
    inconclusive = "inconclusive"
    pass_ = "pass"

# ---- profile: StandardProfile ----

class Auxiliary(U.Class):
    _STEREO = "StandardProfile::StandardProfile::Auxiliary"
    _BASE_METACLASSES = ("Class")

class BuildComponent(U.Component):
    _STEREO = "StandardProfile::StandardProfile::BuildComponent"
    _BASE_METACLASSES = ("Component")

class Call(U.Usage):
    _STEREO = "StandardProfile::StandardProfile::Call"
    _BASE_METACLASSES = ("Usage")

class Create(U.Usage, U.BehavioralFeature):
    _STEREO = "StandardProfile::StandardProfile::Create"
    _BASE_METACLASSES = ("BehavioralFeature", "Usage")

class Derive(U.Abstraction):
    _STEREO = "StandardProfile::StandardProfile::Derive"
    _BASE_METACLASSES = ("Abstraction")

class Destroy(U.BehavioralFeature):
    _STEREO = "StandardProfile::StandardProfile::Destroy"
    _BASE_METACLASSES = ("BehavioralFeature")

class File(U.Artifact):
    _STEREO = "StandardProfile::StandardProfile::File"
    _BASE_METACLASSES = ("Artifact")

class Document(File, U.Artifact):
    _STEREO = "StandardProfile::StandardProfile::Document"
    _BASE_METACLASSES = ("Artifact")

class Entity(U.Component):
    _STEREO = "StandardProfile::StandardProfile::Entity"
    _BASE_METACLASSES = ("Component")

class Executable(File, U.Artifact):
    _STEREO = "StandardProfile::StandardProfile::Executable"
    _BASE_METACLASSES = ("Artifact")

class Focus(U.Class):
    _STEREO = "StandardProfile::StandardProfile::Focus"
    _BASE_METACLASSES = ("Class")

class Framework(U.Package):
    _STEREO = "StandardProfile::StandardProfile::Framework"
    _BASE_METACLASSES = ("Package")

class Implement(U.Component):
    _STEREO = "StandardProfile::StandardProfile::Implement"
    _BASE_METACLASSES = ("Component")

class ImplementationClass(U.Class):
    _STEREO = "StandardProfile::StandardProfile::ImplementationClass"
    _BASE_METACLASSES = ("Class")

class Instantiate(U.Usage):
    _STEREO = "StandardProfile::StandardProfile::Instantiate"
    _BASE_METACLASSES = ("Usage")

class Library(File, U.Artifact):
    _STEREO = "StandardProfile::StandardProfile::Library"
    _BASE_METACLASSES = ("Artifact")

class Metaclass(U.Class):
    _STEREO = "StandardProfile::StandardProfile::Metaclass"
    _BASE_METACLASSES = ("Class")

class Metamodel(U.Model):
    _STEREO = "StandardProfile::StandardProfile::Metamodel"
    _BASE_METACLASSES = ("Model")

class ModelLibrary(U.Package):
    _STEREO = "StandardProfile::StandardProfile::ModelLibrary"
    _BASE_METACLASSES = ("Package")

class Process(U.Component):
    _STEREO = "StandardProfile::StandardProfile::Process"
    _BASE_METACLASSES = ("Component")

class Realization(U.Classifier):
    _STEREO = "StandardProfile::StandardProfile::Realization"
    _BASE_METACLASSES = ("Classifier")

class Refine(U.Abstraction):
    _STEREO = "StandardProfile::StandardProfile::Refine"
    _BASE_METACLASSES = ("Abstraction")

class Responsibility(U.Usage):
    _STEREO = "StandardProfile::StandardProfile::Responsibility"
    _BASE_METACLASSES = ("Usage")

class Script(File, U.Artifact):
    _STEREO = "StandardProfile::StandardProfile::Script"
    _BASE_METACLASSES = ("Artifact")

class Send(U.Usage):
    _STEREO = "StandardProfile::StandardProfile::Send"
    _BASE_METACLASSES = ("Usage")

class Service(U.Component):
    _STEREO = "StandardProfile::StandardProfile::Service"
    _BASE_METACLASSES = ("Component")

class Source(File, U.Artifact):
    _STEREO = "StandardProfile::StandardProfile::Source"
    _BASE_METACLASSES = ("Artifact")

class Specification(U.Classifier):
    _STEREO = "StandardProfile::StandardProfile::Specification"
    _BASE_METACLASSES = ("Classifier")

class Subsystem(U.Component):
    _STEREO = "StandardProfile::StandardProfile::Subsystem"
    _BASE_METACLASSES = ("Component")

class SystemModel(U.Model):
    _STEREO = "StandardProfile::StandardProfile::SystemModel"
    _BASE_METACLASSES = ("Model")

class Trace(U.Abstraction):
    _STEREO = "StandardProfile::StandardProfile::Trace"
    _BASE_METACLASSES = ("Abstraction")

class Type(U.Class):
    _STEREO = "StandardProfile::StandardProfile::Type"
    _BASE_METACLASSES = ("Class")

class Utility(U.Class):
    _STEREO = "StandardProfile::StandardProfile::Utility"
    _BASE_METACLASSES = ("Class")

# ---- profile: SysML ----

class AbstractRequirement(U.NamedElement):
    """An AbstractRequirement establishes the attributes and relationships essential to any potential kind of requirement. Any intended requirement kind should subclass AbstractRequirement. The only normative stereotype based on AbstractRequirement is the Requirement stereotype, described in Requirement. Examples of additional non-normative stereotypes based on AbstractRequirement are included in Building Non-Normative Extensions for Property-Based Requirments ."""
    _STEREO = "SysML::Requirements::AbstractRequirement"
    _BASE_METACLASSES = ("NamedElement")
    _ABSTRACT = True
    _DECL = {
    # Derived from all requirements that are the client of a <<deriveReqt>> relationship for which thi
    # s requirement is a supplier.
    'derived': _Ref('derived', None, multi=True, lo=0, hi='*', derived=True),
    # Derived from all requirements that are the supplier of a <<deriveReqt>> relationship for which t
    # his requirement is a client.
    'derivedFrom': _Ref('derivedFrom', None, multi=True, lo=0, hi='*', derived=True),
    # The unique id of the requirement.
    'id': _Ref('id', str),
    # This is a derived property that lists the master requirement for this slave requirement. The mas
    # ter attribute is derived from the supplier of the Copy dependency that has this requirement as t
    # he slave.
    'master': _Ref('master', None, multi=True, lo=0, hi='*', derived=True),
    # Derived from all elements that are the client of a <<refine>> relationship for which this requir
    # ement is a supplier.
    'refinedBy': _Ref('refinedBy', U.NamedElement, multi=True, lo=0, hi='*', derived=True),
    # Derived from all elements that are the client of a <<satisfy>> relationship for which this requi
    # rement is a supplier.
    'satisfiedBy': _Ref('satisfiedBy', U.NamedElement, multi=True, lo=0, hi='*', derived=True),
    # The textual representation or a reference to the textual representation of the requirement.
    'text': _Ref('text', str),
    # Derived from all elements that are the client of a <<trace>> relationship for which this require
    # ment is a supplier.
    'tracedTo': _Ref('tracedTo', U.NamedElement, multi=True, lo=0, hi='*', derived=True),
    # Derived from all elements that are the client of a <<verify>> relationship for which this requir
    # ement is a supplier.
    'verifiedBy': _Ref('verifiedBy', U.NamedElement, multi=True, lo=0, hi='*', derived=True),
    }

class AcceptChangeStructuralFeatureEventAction(U.AcceptEventAction):
    """Accept change structural feature event actions handle change structural feature events (see DirectedFeature). The actions have exactly two output pins. The first output pin holds the values of the structural feature just after the values changed, while the second pin holds the values just before the values changed. The action only accepts events for structural features on the blocks owning the behavior containing the action, or on the behavior itself, if the behavior is not owned by a block."""
    _STEREO = "SysML::Ports&Flows::AcceptChangeStructuralFeatureEventAction"
    _BASE_METACLASSES = ("AcceptEventAction")
    CONSTRAINTS = (
        ("1_one_trigger",
         "(no specification serialized)"
        ),
        ("2_two_resultpins",
         "(no specification serialized)"
        ),
        ("3_context_owns_structuralfeature",
         "(no specification serialized)"
        ),
        ("4_can_access_structuralfeature",
         "(no specification serialized)"
        ),
        ("5_uml_constraint_removed",
         "(no specification serialized)"
        ),
    )

class ElementPropertyPath(U.Element):
    """The ElementPropertyPath stereotype based on UML Element enables elements to identify other elements by a multi-level path of properties accessible from a context block. The context block is described in specializations of ElementPropertyPath."""
    _STEREO = "SysML::Blocks::ElementPropertyPath"
    _BASE_METACLASSES = ("Element")
    _ABSTRACT = True
    _DECL = {
    # A series of properties that identifies elements in the context of a block described in specializ
    # ations of ElementPropertyPath. The ordering of properties is from a property of the context bloc
    # k, through a property of each intermediate block that types the preceding property, ending in a 
    # property with a type that owns or inherits the fully nested property. The fully nested property 
    # is not included in the propertyPath list, but is given by the element to which the ElementProper
    # tyPath is applied in a way described in specializations of ElementPropertyPath. The same propert
    # y might appear more than once because a block can own a property with the same or specialized bl
    # ock as a type.
    'propertyPath': _Ref('propertyPath', U.Property, multi=True, lo=1, hi='*'),
    }
    CONSTRAINTS = (
        ("1_path_consistency",
         "(no specification serialized)"
        ),
    )

class AddFlowPropertyValueOnNestedPortAction(U.AddStructuralFeatureValueAction, ElementPropertyPath):
    """This enables values added to a flow property to propagate out through a specified behavioral port of an object executing the action, rather than all behavior ports exposing the flow property. It also enables values added to a flow property to propagate into objects. Values flowing out of an object are added to an out or inout flow property of the executing object. In this case, the applied stereotype specifies a (possibly nested) behavioral port at the end of a (possibly multi-level) path of behavioral ports from a block that supports the flow property. Values flowing into an object are added to an in or inout flow property of that object, specifying a (possibly nested) port of that object."""
    _STEREO = "SysML::Ports&Flows::AddFlowPropertyValueOnNestedPortAction"
    _BASE_METACLASSES = ("AddStructuralFeatureValueAction")
    _DECL = {
    # Gives a series of ports that end in one supporting the flow property to which a value is being a
    # dded. The ordering of ports is from a port of the object of the stereotyped action, through a po
    # rt of each intermediate block that types the preceding port, ending in a port with a type that o
    # wns or inherits the flow property. The same port might appear more than once because a block can
    #  own a port with the same block as a type, or another block that has the same property.
    'onNestedPort': _Ref('onNestedPort', U.Port, multi=True, lo=1, hi='*'),
    }
    CONSTRAINTS = (
        ("1_feature_flowproperty",
         "(no specification serialized)"
        ),
        ("2_onnestedport_first_owned_by_target_type",
         "(no specification serialized)"
        ),
        ("3_path_consistency",
         "(no specification serialized)"
        ),
        ("4_onnestedport_last_type_owns_invocation_onPort",
         "(no specification serialized)"
        ),
    )

class AdjunctProperty(U.Property):
    """The AdjunctProperty stereotype can be applied to properties to constrain their values to the values of connectors typed by association blocks, call actions, object nodes, variables, or parameters, interaction uses, and submachine states. The values of connectors typed by association blocks are the instances of the association block typing a connector in the block having the stereotyped property. The values of call actions are the executions of behaviors invoked by the behavior having the call action and the stereotyped property (see Notation for more about this use of the stereotype). The values of object nodes are the values of tokens in the object nodes of the behavior having the stereotyp...[truncated]"""
    _STEREO = "SysML::Blocks::AdjunctProperty"
    _BASE_METACLASSES = ("Property")
    _DECL = {
    # Gives the element that determines the values of the property.
    'principal': _Ref('principal', U.Element),
    }
    CONSTRAINTS = (
        ("10_multiplicity_same_or_less_restrictive",
         "(no specification serialized)"
        ),
        ("11_submachine_and_interactionuse_composite_and _compatible_type",
         "(no specification serialized)"
        ),
        ("1_principal_kind",
         "(no specification serialized)"
        ),
        ("2_same_name",
         "(no specification serialized)"
        ),
        ("3_connector_and_callaction_composite",
         "(no specification serialized)"
        ),
        ("4_same_owner",
         "(no specification serialized)"
        ),
        ("5_compatible_type",
         "(no specification serialized)"
        ),
        ("6_connector_principal_associationblock",
         "(no specification serialized)"
        ),
        ("7_adjunctproperty_connectorproperty_consistent",
         "(no specification serialized)"
        ),
        ("8_callAction_composite_and_consistent_type",
         "(no specification serialized)"
        ),
        ("9_objectnode_multiplicity",
         "(no specification serialized)"
        ),
    )

class DirectedRelationshipPropertyPath(U.DirectedRelationship):
    """The DirectedRelationshipPropertyPath stereotype based on UML DirectedRelationship enables directed relationships to identify their sources and targets by a multi-level path of properties accessible from context blocks for the sources and targets. Context blocks are typically the owner of the first property in the path of properties, but can be specializations of the owner to limit the scope of the relationship."""
    _STEREO = "SysML::Blocks::DirectedRelationshipPropertyPath"
    _BASE_METACLASSES = ("DirectedRelationship")
    _ABSTRACT = True
    _DECL = {
    # Gives the context for sourcePropertyPath to begin from.
    'sourceContext': _Ref('sourceContext', U.Classifier),
    # A series of properties that identifies the source of the directed relationship in the context of
    #  the block specified by the sourceContext property. The ordering of properties is from a propert
    # y of the sourceContext block, through a property of each intermediate block that types the prece
    # ding property, ending in a property with a type that owns or inherits the source of the directed
    #  relationship. The source is not included in the propertyPath list. The same property might appe
    # ar more than once because a block can own a property with the same or specialized block as a typ
    # e.
    'sourcePropertyPath': _Ref('sourcePropertyPath', U.Property, multi=True, lo=0, hi='*'),
    # Gives the context for targetPropertyPath to begin from.
    'targetContext': _Ref('targetContext', U.Classifier),
    # A series of properties that identifies the target of the directed relationship in the context of
    #  the block specified by the targetContext property. The ordering of properties is from a propert
    # y of the targetContext block, through a property of each intermediate block that types the prece
    # ding property, ending in a property with a type that owns or inherits the target of the directed
    #  relationship. The target is not included in the propertyPath list. The same property might appe
    # ar more than once because a block can own a property with the same or specialized block as a typ
    # e.
    'targetPropertyPath': _Ref('targetPropertyPath', U.Property, multi=True, lo=0, hi='*'),
    }
    CONSTRAINTS = (
        ("1_sourcecontext_iif_property",
         "(no specification serialized)"
        ),
        ("2_targetcontext_iif_property",
         "(no specification serialized)"
        ),
        ("3_sourcepropertypath_implies_property",
         "(no specification serialized)"
        ),
        ("4_targetpropertypath_implies_property",
         "(no specification serialized)"
        ),
        ("5_sourcecontext_owns_sourcepath_first",
         "(no specification serialized)"
        ),
        ("6_targetcontext_owns_targetpath_first",
         "(no specification serialized)"
        ),
        ("7_path_and_owners_consistency",
         "(no specification serialized)"
        ),
        ("8_sourcepath_last_type_owns_source",
         "(no specification serialized)"
        ),
        ("9_targetpath_last_type_owns_target",
         "(no specification serialized)"
        ),
    )

class Allocate(U.Abstraction, DirectedRelationshipPropertyPath):
    """<p> Allocate is a dependency based on UML::Abstraction. It is a mechanism for associating elements of different types, or in different hierarchies, at an abstract level. Allocate is used for assessing user model consistency and directing future design activity. It is expected that an <<allocate>> relationship between model elements is a precursor to a more concrete relationship between the elements, their properties, operations, attributes, or sub-classes. Allocate is a stereotype of a UML4SysML::Abstraction that is permissible between any two NamedElements. It is depicted as a dependency with the "allocate" keyword attached to it. Allocate is directional in that one NamedElement is the "fro...[truncated]"""
    _STEREO = "SysML::Allocations::Allocate"
    _BASE_METACLASSES = ("Abstraction")
    CONSTRAINTS = (
        ("2_binary",
         "(no specification serialized)"
        ),
    )

class AllocateActivityPartition(U.ActivityPartition):
    """AllocateActivityPartition is used to depict an <<allocate>> relationship on an Activity diagram. The AllocateActivityPartition is a standard UML::ActivityPartition, with modified constraints as stated below."""
    _STEREO = "SysML::Allocations::AllocateActivityPartition"
    _BASE_METACLASSES = ("ActivityPartition")
    CONSTRAINTS = (
        ("1_actions_on_client_ends",
         "(no specification serialized)"
        ),
        ("2_not_uml_semantics",
         "(no specification serialized)"
        ),
    )

class BindingConnector(U.Connector):
    """A Binding Connector is a connector which specifies that the properties at both ends of the connector have equal values. If the properties at the ends of a binding connector are typed by a ValueType, the connector specifies that the instances of the properties shall hold equal values, recursively through any nested properties within the connected properties. If the properties at the ends of a binding connector are typed by a Block, the connector specifies that the instances of the properties shall refer to the same block instance. As with any connector owned by a SysML Block, the ends of a binding connector may be nested within a multi-level path of properties accessible from the owning block...[truncated]"""
    _STEREO = "SysML::Blocks::BindingConnector"
    _BASE_METACLASSES = ("Connector")
    CONSTRAINTS = (
        ("1_compatible_types",
         "(no specification serialized)"
        ),
    )

class Block(U.Class):
    """<p> A Block is a modular unit that describes the structure of a system or element. It may include both structural and behavioral features, such as properties and operations, which represent the state of the system and behavior that the system may exhibit. Some of these properties may hold parts of a system, which can also be described by blocks that type the properties. Properties without types do not restrict the instances that can be values of the properties, as if they had the most general type possible. A block may include a structure of connectors between its properties to indicate how its parts or other properties relate to one another. </p><p> SysML blocks provide a general-purpose ca...[truncated]"""
    _STEREO = "SysML::Blocks::Block"
    _BASE_METACLASSES = ("Class")
    _DECL = {
    # If true, then the block is treated as a black box; a part typed by this black box can only be co
    # nnected via its ports or directly to its outer boundary. If false, or if a value is not present,
    #  then connections can be established to elements of its internal structure via deep-nested conne
    # ctor ends.
    'isEncapsulated': _Ref('isEncapsulated', bool),
    }
    CONSTRAINTS = (
        ("1_associations_binary",
         "(no specification serialized)"
        ),
        ("2_connectors_binary",
         "(no specification serialized)"
        ),
        ("5_uml_connector_constraint_removed",
         "(no specification serialized)"
        ),
        ("6_valueproperties_composite",
         "(no specification serialized)"
        ),
        ("7_composition_acyclic",
         "(no specification serialized)"
        ),
        ("8_specializations_are_blocks",
         "(no specification serialized)"
        ),
        ("9_valueproperties_composite",
         "(no specification serialized)"
        ),
    )

class EndPathMultiplicity(U.Property):
    """The EndPathMultiplicity stereotype can be applied to properties that are related by redefinition to properties that have BoundReference applied. The lower and upper properties of the stereotype give the minimum and maximum number of values, respectively, of the property at the bound end of the related bound reference, for each object reached by navigation along its binding path."""
    _STEREO = "SysML::Blocks::EndPathMultiplicity"
    _BASE_METACLASSES = ("Property")
    _DECL = {
    # Gives the minimum number of values of the property at the end of the related bindingPath, for ea
    # ch object reached by navigation along the bindingPath from an instance of the block owning the p
    # roperty to which EndPathMultiplicity is applied
    'lower': _Ref('lower', int),
    # Gives the maximum number of values of the property at the end of the related bindingPath, for ea
    # ch object reached by navigation along the bindingPath from an instance of the block owning the p
    # roperty to which EndPathMultiplicity is applied.
    'upper': _Ref('upper', U.UnlimitedNatural),
    }
    CONSTRAINTS = (
        ("1_redefinition",
         "(no specification serialized)"
        ),
        ("2_non_negative",
         "(no specification serialized)"
        ),
    )

class BoundReference(EndPathMultiplicity, U.Property):
    """<p> The BoundReference stereotype can be applied to properties that have binding connectors, to highlight their usage as constraining other properties. The bound end of the stereotype is a connector end of one of the binding connectors, path of the bound end, if it is a nested connector end. </p><p> The type of stereotyped property constrains the type of the values of the bound properties. The multiplicity of the stereotyped property constrains the number of values of the bound properties, which is the total number of values reached by navigation through property paths of nested connector ends, if any. The multiplicities at the end of path can be constrained, because bound references are end...[truncated]"""
    _STEREO = "SysML::Blocks::BoundReference"
    _BASE_METACLASSES = ("Property")
    _DECL = {
    # Gives the propertyPath of the NestedConnectorEnd applied, if any, to the boundEnd, appended to t
    # he role of the boundEnd.
    'bindingPath': _Ref('bindingPath', U.Property, multi=True, lo=1, hi='*', derived=True),
    # Gives a connector end of a binding connector opposite to the end linked to the stereotyped prope
    # rty, or linked to a property that generalizes the stereotyped one through redefinition.
    'boundEnd': _Ref('boundEnd', U.ConnectorEnd),
    }
    CONSTRAINTS = (
        ("1_bindingconnector_end",
         "(no specification serialized)"
        ),
        ("2_opposite_bindingconnector_end",
         "(no specification serialized)"
        ),
        ("3_navigable",
         "(no specification serialized)"
        ),
        ("4_propertypath_consistency",
         "(no specification serialized)"
        ),
        ("5_reference_or_valueproperty",
         "(no specification serialized)"
        ),
        ("6_ordered_nonunique",
         "(no specification serialized)"
        ),
        ("7_cannot_redefine_boundreference",
         "(no specification serialized)"
        ),
        ("8_notbounded_to_itslef",
         "(no specification serialized)"
        ),
    )

class ChangeStructuralFeatureEvent(U.ChangeEvent):
    """A ChangeStructuralFeatureEvent models changes in values of structural features."""
    _STEREO = "SysML::Ports&Flows::ChangeStructuralFeatureEvent"
    _BASE_METACLASSES = ("ChangeEvent")
    _DECL = {
    # The event models occurrences of changes to values of this structural feature.
    'structuralFeature': _Ref('structuralFeature', U.StructuralFeature),
    }
    CONSTRAINTS = (
        ("1_not_static",
         "(no specification serialized)"
        ),
        ("2_one_featuringclassifier",
         "(no specification serialized)"
        ),
    )

class ClassifierBehaviorProperty(U.Property):
    """The ClassifierBehaviorProperty stereotype can be applied to properties to constrain their values to be the executions of classifier behaviors. The value of properties with ClassifierBehaviorProperty applied are the executions of classifier behaviors invoked by instantiation of the block that owns the stereotyped property or one of its specializations."""
    _STEREO = "SysML::Blocks::ClassifierBehaviorProperty"
    _BASE_METACLASSES = ("Property")
    CONSTRAINTS = (
        ("1_owner_classifierbehavior",
         "(no specification serialized)"
        ),
        ("2_composite",
         "(no specification serialized)"
        ),
        ("3_typed_by_classifierbehavior",
         "(no specification serialized)"
        ),
    )

class Conform(U.Generalization):
    """A Conform relationship is a dependency between a view and a viewpoint. The view conforms to the specified rules and conventions detailed in the viewpoint. Conform is a specialization of the UML dependency, and as with other dependencies the arrow direction points from the (client/source) to the (supplier/target)."""
    _STEREO = "SysML::ModelElements::Conform"
    _BASE_METACLASSES = ("Generalization")
    CONSTRAINTS = (
        ("1_general_is_viewpoint",
         "(no specification serialized)"
        ),
        ("2_specific_is_view",
         "(no specification serialized)"
        ),
    )

class ConnectorProperty(U.Property):
    """<p> Connectors can be typed by association classes that are stereotyped by Block (association blocks, see ParticipantProperty in subclause ParticipantProperty). These connectors specify instances of the association block created within the instances of the block that owns the connector. The values of a connector property are instances of the association block created due to the connector referred to by the connector property. </p><p> A connector property can optionally be shown in an internal block diagram with a dotted line from the connector line to a rectangle notating the connector property. The keyword <<connector>> before a property name indicates the property is stereotyped by Connect...[truncated]"""
    _STEREO = "SysML::Blocks::ConnectorProperty"
    _BASE_METACLASSES = ("Property")
    _DECL = {
    # A connector of the block owning the property on which the stereotype is applied.
    'connector': _Ref('connector', U.Connector),
    }
    CONSTRAINTS = (
        ("1_block_property",
         "(no specification serialized)"
        ),
        ("2_owned_or_inherited",
         "(no specification serialized)"
        ),
        ("3_composite",
         "(no specification serialized)"
        ),
        ("4_typed_by_associationblock",
         "(no specification serialized)"
        ),
        ("5_same_name",
         "(no specification serialized)"
        ),
    )

class ConstraintBlock(Block, U.Class):
    """<p> A constraint block is a block that packages the statement of a constraint so it may be applied in a reusable way to constrain properties of other blocks. A constraint block typically defines one or more constraint parameters, which are bound to properties of other blocks in a surrounding context where the constraint is used. Binding connectors, as defined in Blocks are used to bind each parameter of the constraint block to a property in the surrounding context. All properties of a constraint block are constraint parameters, with the exception of constraint properties that hold internally nested usages of constraint blocks. </p><p> A constraint property is a property of any block that is ...[truncated]"""
    _STEREO = "SysML::ConstraintBlocks::ConstraintBlock"
    _BASE_METACLASSES = ("Class")
    CONSTRAINTS = (
        ("1_constraintparameters_only",
         "(no specification serialized)"
        ),
        ("2_specializations_are_constraintblocks",
         "(no specification serialized)"
        ),
        ("3_composite",
         "(no specification serialized)"
        ),
    )

class Rate(U.Parameter, U.ObjectNode, U.ActivityEdge):
    """When the <<rate>> stereotype is applied to an activity edge, it specifies the expected value of the number of objects and values that traverse the edge per time interval, that is, the expected value rate at which they leave the source node and arrive at the target node. It does not refer to the rate at which a value changes over time. When the stereotype is applied to a parameter, the parameter shall be streaming, and the stereotype gives the number of objects or values that flow in or out of the parameter per time interval while the behavior or operation is executing. Streaming is a characteristic of UML behavior parameters that supports the input and output of items while a behavior is exe...[truncated]"""
    _STEREO = "SysML::Activities::Rate"
    _BASE_METACLASSES = ("ActivityEdge", "ObjectNode", "Parameter")
    _DECL = {
    # Value of the rate
    'rate': _Ref('rate', U.InstanceSpecification),
    }
    CONSTRAINTS = (
        ("1_streaming",
         "(no specification serialized)"
        ),
        ("2_edges_rates",
         "(no specification serialized)"
        ),
    )

class Continuous(Rate):
    """<p> Continuous rate is a special case of rate of flow (see Rate) where the increment of time between items approaches zero. It is intended to represent continuous flows that may correspond to water flowing through a pipe, a time continuous signal, or continuous energy flow. It is independent from UML streaming, see Rate. A streaming parameter may or may not apply to continuous flow, and a continuous flow may or may not apply to streaming parameters. </p><p> UML places no restriction on the rate at which tokens flow. In particular, the time between tokens can approach as close to zero as needed, for example to simulate continuous flow. There is also no restriction in UML on the kind of values...[truncated]"""
    _STEREO = "SysML::Activities::Continuous"
    _BASE_METACLASSES = ()

class ControlOperator(U.Behavior):
    """<p> A control operator is a behavior that is intended to represent an arbitrarily complex logical operator that can be used to enable and disable other actions. When the <<controlOperator>> stereotype is applied to behaviors, the behavior takes control values as inputs or provides them as outputs, that is, it treats control as data (see ControlValue). When the <<controlOperator>> stereotype is not applied, the behavior may not have a parameter typed by ControlValue. The <<controlOperator>> stereotype also applies to operations with the same semantics. </p><p> The control value inputs do not enable or disable the control operator execution based on their value, they only enable based on their...[truncated]"""
    _STEREO = "SysML::Activities::ControlOperator"
    _BASE_METACLASSES = ("Behavior", "Operation")
    CONSTRAINTS = (
        ("1_one_parameter_controlvalue",
         "(no specification serialized)"
        ),
        ("2_controloperator_operation_method",
         "(no specification serialized)"
        ),
    )

class Trace(U.Abstraction, DirectedRelationshipPropertyPath):
    """The Trace stereotype specializes UML4SysML Trace and DirectedRelationshipPropertyPath to enable traces to identify their sources and targets by a multi-level path of accessible properties from context blocks for the sources and targets."""
    _STEREO = "SysML::Requirements::Trace"
    _BASE_METACLASSES = ("Abstraction")
    CONSTRAINTS = (
        ("2_binary",
         "(no specification serialized)"
        ),
    )

class Copy(Trace, U.Abstraction):
    """<p> A Copy relationship is a dependency between a supplier requirement and a client requirement that specifies that the text of the client requirement is a read-only copy of the text of the supplier requirement. </p><p> A Copy dependency created between two requirements maintains a master/slave relationship between the two elements for the purpose of requirements re-use in different contexts. When a Copy dependency exists between two requirements, the requirement text of the client requirement is a read-only copy of the requirement text of the requirement at the supplier end of the dependency. </p>"""
    _STEREO = "SysML::Requirements::Copy"
    _BASE_METACLASSES = ("Abstraction")
    CONSTRAINTS = (
        ("1_source_and_taget_are_requirements",
         "(no specification serialized)"
        ),
        ("2_same_text",
         "(no specification serialized)"
        ),
    )

class DeriveReqt(Trace, U.Abstraction):
    """A DeriveReqt relationship is a dependency between two requirements in which a client requirement can be derived from the supplier requirement. For example, a system requirement may be derived from a business need, or lower-level requirements may be derived from a system requirement. As with other dependencies, the arrow direction points from the derived (client) requirement to the (supplier) requirement from which it is derived."""
    _STEREO = "SysML::Requirements::DeriveReqt"
    _BASE_METACLASSES = ("Abstraction")
    CONSTRAINTS = (
        ("1_supplier_is_requirement",
         "(no specification serialized)"
        ),
        ("2_client_is_requirement",
         "(no specification serialized)"
        ),
    )

class DirectedFeature(U.Feature):
    """<p> A DirectedFeature indicates whether the feature is supported by the owning block (provided) for other connected blocks to use, or is to be supported by a connected block for the owning block to use (required), or both (providedRequired). A providedRequired feature specifies a symmetric dependency between two connected blocks whereby a block's internal use of such a feature is delegated to the connected block with the corresponding feature and conversely that block's internal use of the feature is delegated to the other connected block. </p><p> The owning block for features on types of proxy ports is the type of the block usage the proxy port is standing in for, which might be an internal...[truncated]"""
    _STEREO = "SysML::Ports&Flows::DirectedFeature"
    _BASE_METACLASSES = ("Feature")
    _DECL = {
    # Specifies whether the feature is supported by the owning block (featureDirection="provided"), or
    #  is to be supported by other blocks for the owning block to use (featureDirection="required"), o
    # r both (featureDirection="providedrequired").
    'featureDirection': _Ref('featureDirection', None),
    }
    CONSTRAINTS = (
        ("1_behavioralfeature_or_not_flowproperty",
         "(no specification serialized)"
        ),
        ("2_method_if_provided",
         "(no specification serialized)"
        ),
    )

class Discrete(Rate):
    """Discrete rate is a special case of rate of flow (see Rate) where the increment of time between items is a non-zero. Examples include the production of assemblies in a factory and signals set at periodic time intervals."""
    _STEREO = "SysML::Activities::Discrete"
    _BASE_METACLASSES = ()
    CONSTRAINTS = (
        ("1_not_continuous",
         "(no specification serialized)"
        ),
    )

class DistributedProperty(U.Property):
    """DistributedProperty is a stereotype of Property used to apply a probability distribution to the values of the property. Specific distributions should be defined as subclasses of the DistributedProperty stereotype with the operands of the distributions represented by properties of those stereotype subclasses. A sample set of probability distributions that could be applied to value properties is given in Distribution Extensions."""
    _STEREO = "SysML::Blocks::DistributedProperty"
    _BASE_METACLASSES = ("Property")
    CONSTRAINTS = (
        ("1_block_or_valuetype",
         "(no specification serialized)"
        ),
    )

class ElementGroup(U.Comment):
    """<p> The ElementGroup stereotype provides a lightweight mechanism for grouping various and possibly heterogeneous model elements by extending the capability of comments to refer to multiple annotated elements. For example, it can group elements that are associated with a particular release of the model, have a certain risk level, or are associated with a legacy design. The semantics of ElementGroup is modeler-defined. In particular, the body text is not restricted. It can describe the grouped elements as well as elements or values related to the grouped elements. </p><p> Element groups are named using the name property. The criterion for membership in an element group is specified by the body...[truncated]"""
    _STEREO = "SysML::ModelElements::ElementGroup"
    _BASE_METACLASSES = ("Comment")
    _DECL = {
    # Specifies the rationale for being member of the group. Adding an element to the group asserts th
    # at the criterion applies to this element. Derived from Comment::body.
    'criterion': _Ref('criterion', str, derived=True),
    # Set specifying the members of the group. Derived from Comment::annotatedElement.
    'member': _Ref('member', U.Element, multi=True, lo=0, hi='*', derived=True),
    # Name of the element group.
    'name': _Ref('name', str),
    # Organize member according to an arbitrary order.
    'orderedMember': _Ref('orderedMember', U.Element, multi=True, lo=0, hi='*'),
    # Number of members in the group.
    'size': _Ref('size', int, derived=True),
    }

class Expose(U.Dependency):
    """The expose relationship relates a view to one or more model elements. Each model element is an access point to initiate the query. The view and the model elements related to the view are passed to the constructor when it is invoked. The method describes how the exposed elements are navigated to extract the desired information."""
    _STEREO = "SysML::ModelElements::Expose"
    _BASE_METACLASSES = ("Dependency")
    CONSTRAINTS = (
        ("1_client_is_view",
         "(no specification serialized)"
        ),
    )

class FlowPort(U.Port):
    """A FlowPort is an interaction point through which input and/or output of items such as data, material, or energy may flow. This enables the owning block to declare which items it may exchange with its environment and the interaction points through which the exchange is made. We distinguish between atomic flow port and a nonatomic flow port. Atomic flow ports relay items that are classified by a single Block, ValueType, DataType, or Signal classifier. A nonatomic flow port relays items of several types as specified by a FlowSpecification. Flow ports and associated flow specifications define "what can flow" between the block and its environment, whereas item flows specify "what does flow" in a ...[truncated]"""
    _STEREO = "SysML::DeprecatedElements::FlowPort"
    _BASE_METACLASSES = ("Port")
    _DECL = {
    # Indicates the direction in which an atomic flow port relays its items. If the direction is set t
    # o "in," then the items are relayed from an external connector via the flow port into the flow po
    # rt's owner (or one of its parts). If the direction is set to "out," then the items are relayed f
    # rom the flow port's owner, via the flow port, through an external connector attached to the flow
    #  port. If the direction is set to "inout," then items can flow both ways. By default, the value 
    # is inout.
    'direction': _Ref('direction', None),
    # This is a derived attribute (derived from the flow port's type). For a flow port typed by a flow
    #  specification the value of this attribute is False, otherwise the value is True.
    'isAtomic': _Ref('isAtomic', bool, derived=True),
    }

class FlowProperty(U.Property):
    """<p> A FlowProperty signifies a single kind of flow element that can flow to/from its owning instance that is specified by the block defining that flow property. A flow propertys values are either received from or transmitted to another instance. An "in" flow property value cannot be modified by the owning instance of that flow property, or by parts of that instance. An "out" flow property can only be modified by the owning instance of that flow property, or by parts of that instance. An "inout" flow property can be used as an "in" flow property or an "out" flow property, and there is no restriction regarding the way it can be modified. </p><p> Flow due to flow properties can only occur when ...[truncated]"""
    _STEREO = "SysML::Ports&Flows::FlowProperty"
    _BASE_METACLASSES = ("Property")
    _DECL = {
    # Specifies if the property value is received from an external block (direction="in"), transmitted
    #  to an external Block (direction="out") or both (direction="inout").
    'direction': _Ref('direction', None),
    }
    CONSTRAINTS = (
        ("1_restricted_types",
         "(no specification serialized)"
        ),
    )

class FlowSpecification(U.Interface):
    """A FlowSpecification specifies inputs and outputs as a set of flow properties. A flow specification is used by flow ports to specify what items can flow via the port."""
    _STEREO = "SysML::DeprecatedElements::FlowSpecification"
    _BASE_METACLASSES = ("Interface")

class FullPort(U.Port):
    """Full ports specify a separate element of the system from the owning block or its internal parts. They might have their own internal parts and behaviors to support interaction with the owning block, its internal parts, or external blocks. They cannot be behavioral ports, or linked to internal parts by binding connectors, because these constructs imply identity with the owning block or internal parts. However, full ports can be linked to non-full ports by binding connectors, because this does not necessarily imply identity with other parts of the system."""
    _STEREO = "SysML::Ports&Flows::FullPort"
    _BASE_METACLASSES = ("Port")
    CONSTRAINTS = (
        ("1_not_proxy",
         "(no specification serialized)"
        ),
        ("2_not_bound_to_fullport",
         "(no specification serialized)"
        ),
        ("3_not_behavioral",
         "(no specification serialized)"
        ),
    )

class InterfaceBlock(Block):
    """Interface blocks are blocks that cannot have internal parts or behaviors, including classifier behaviors or methods, but otherwise have the same capabilities as blocks. In particular, they can have operations, receptions and properties (like UML interfaces), as well as ports. They can type any kind of property, but are mandatory as types of proxy ports, and can type ports to any level of nesting."""
    _STEREO = "SysML::Ports&Flows::InterfaceBlock"
    _BASE_METACLASSES = ()
    CONSTRAINTS = (
        ("1_no_behavior",
         "(no specification serialized)"
        ),
        ("2_no_part",
         "(no specification serialized)"
        ),
        ("3_interfaceblock_typed_ports",
         "(no specification serialized)"
        ),
        ("4_isconjugated_not_used",
         "(no specification serialized)"
        ),
    )

class InvocationOnNestedPortAction(U.InvocationAction, ElementPropertyPath):
    """This extends the capabilities of UMLs onPort property of InvocationAction to support nested ports. It identifies a nested port by a multi-level path of ports from the block that executes the action. Like UMLs onPort property, this extends invocation actions to send invocations out of ports of objects executing the actions, or to ports of those objects or other objects. Invocations intended to go out of the object executing the action shall be sent to the executing object on a proxy port. Invocations intended to go directly to a target object are sent to that object on a port of that object."""
    _STEREO = "SysML::Ports&Flows::InvocationOnNestedPortAction"
    _BASE_METACLASSES = ("InvocationAction")
    _DECL = {
    # Gives a series of ports that identifies the port receiving the invocation in the context of the 
    # target object of the invocation. The ordering of ports is from a port of the target object, thro
    # ugh a port of each intermediate block that types the preceding port, ending in a port with a typ
    # e that owns or inherits the port given by the onPort property of the invocation action. The onPo
    # rt port is not included in the onNestedPort list. The same port might appear more than once beca
    # use a block can own a port with the same block as a type, or another block that has the same pro
    # perty.
    'onNestedPort': _Ref('onNestedPort', U.Port, multi=True, lo=1, hi='*'),
    }
    CONSTRAINTS = (
        ("1_onPort_defined",
         "(no specification serialized)"
        ),
        ("2_onnestedport_first_owned_by_target_type",
         "(no specification serialized)"
        ),
        ("3_path_consistency",
         "(no specification serialized)"
        ),
        ("4_onnestedport_last_type_owns_invocation_onPort",
         "(no specification serialized)"
        ),
    )

class ItemFlow(U.InformationFlow):
    """<p> An ItemFlow describes the flow of items across a connector or an association. It may constrain the item exchange between blocks, block usages, or ports as specified by their flow properties. For example, a pump connected to a tank: the pump has an "out" flow property of type Liquid and the tank has an "in" FlowProperty of type Liquid. To signify that only water flows between the pump and the tank, we can specify an ItemFlow of type Water on the connector. </p><p> One can label an ItemFlow with the classifiers of the items that may be conveyed. For example: a label Water would imply that instances of Water might be transmitted over this ItemFlow. In addition, if the item flow identifies a...[truncated]"""
    _STEREO = "SysML::Ports&Flows::ItemFlow"
    _BASE_METACLASSES = ("InformationFlow")
    _DECL = {
    # An optional property that relates the flowing item to the instances of the connectors enclosing 
    # block. This property is applicable only for item flows realized by connectors. The itemProperty 
    # attribute has no values if the item flow is realized by an Association.
    'itemProperty': _Ref('itemProperty', U.Property),
    }
    CONSTRAINTS = (
        ("1_source_and_target_linked",
         "(no specification serialized)"
        ),
        ("2_type_restricted",
         "(no specification serialized)"
        ),
        ("3_itemproperty_common_owner",
         "(no specification serialized)"
        ),
        ("4_association_xor_itemproperty",
         "(no specification serialized)"
        ),
        ("5_same_type",
         "(no specification serialized)"
        ),
        ("6_same_name",
         "(no specification serialized)"
        ),
    )

class NestedConnectorEnd(U.ConnectorEnd, ElementPropertyPath):
    """The NestedConnectorEnd stereotype of UML ConnectorEnd extends a UML ConnectorEnd so that the connected property may be identified by a multi-level path of accessible properties from the block that owns the connector. The propertyPath inherited from ElementPropertyPath gives a series of properties that identifies the connected property in the context of the block that owns the connector. The ordering of properties is from a property of the block that owns the connector, through a property of each intermediate block that types the preceding property, ending in a property with a type that owns or inherits the property that is the role of the connector end (the property that the connector graphi...[truncated]"""
    _STEREO = "SysML::Blocks::NestedConnectorEnd"
    _BASE_METACLASSES = ("ConnectorEnd")
    CONSTRAINTS = (
        ("1_propertypath_first_owned_by_connector_owner",
         "(no specification serialized)"
        ),
        ("2_propertypath_last_type_owns_role",
         "(no specification serialized)"
        ),
    )

class NoBuffer(U.ObjectNode):
    """When the <<nobuffer>> stereotype is applied to object nodes, tokens arriving at the node are discarded if they are refused by outgoing edges, or refused by actions for object nodes that are input pins. This is typically used with fast or continuously flowing data values, to prevent buffer overrun, or to model transient values, such as electrical signals. For object nodes that are the target of continuous flows, <<nobuffer>> and <<overwrite>> have the same effect. The stereotype does not override UML token offering semantics; it just indicates what happens to the token when it is accepted. When the stereotype is not applied, the semantics are as in UML."""
    _STEREO = "SysML::Activities::NoBuffer"
    _BASE_METACLASSES = ("ObjectNode")
    CONSTRAINTS = (
        ("1_not_overwrite",
         "(no specification serialized)"
        ),
    )

class Optional(U.Parameter):
    """When the <<optional>> stereotype is applied to parameters, the lower multiplicity shall be equal to zero. This means the parameter is not required to have a value for the activity or any behavior to begin or end execution. Otherwise, the lower multiplicity shall be greater than zero, which is called "required." The absence of this stereotype indicates a constraint, see below."""
    _STEREO = "SysML::Activities::Optional"
    _BASE_METACLASSES = ("Parameter")
    CONSTRAINTS = (
        ("1_lower_is_0",
         "(no specification serialized)"
        ),
    )

class Overwrite(U.ObjectNode):
    """When the <<overwrite>> stereotype is applied to object nodes, a token arriving at a full object node removes one that is already there before being added (a full object node has as many tokens as allowed by its upper bound). This is typically used on an input pin with an upper bound of 1 to ensure that stale data is overridden at an input pin. For upper bounds greater than one, the token removed is the one that has been in the object node the longest. For FIFO ordering, this is the token that is next to be selected, for LIFO it is the token that would be last to be selected. Tokens arriving at a full object node with the Overwrite stereotype applied take up their positions in the ordering as...[truncated]"""
    _STEREO = "SysML::Activities::Overwrite"
    _BASE_METACLASSES = ("ObjectNode")
    CONSTRAINTS = (
        ("1_not_nobuffer",
         "(no specification serialized)"
        ),
    )

class ParticipantProperty(U.Property):
    """<p> The Block stereotype extends Class, so it can be applied to any specialization of Class, including Association Classes. These are informally called "association blocks." An association block can own properties and connectors, like any other block. Each instance of an association block can link together instances of the end classifiers of the association. </p><p> To refer to linked objects and values of an instance of an association block, it is necessary for the modeler to specify which (participant) properties of the association block identify the instances being linked at which end of the association. The value of a participant property on an instance (link) of the association block is...[truncated]"""
    _STEREO = "SysML::Blocks::ParticipantProperty"
    _BASE_METACLASSES = ("Property")
    _DECL = {
    # A member end of the association block owning the property on which the stereotype is applied.
    'end': _Ref('end', U.Property),
    }
    CONSTRAINTS = (
        ("1_associationblock",
         "(no specification serialized)"
        ),
        ("2_memberend",
         "(no specification serialized)"
        ),
        ("3_aggregationkind_none",
         "(no specification serialized)"
        ),
        ("4_end_owner",
         "(no specification serialized)"
        ),
        ("5_same_type",
         "(no specification serialized)"
        ),
        ("6_multiplicity_1",
         "(no specification serialized)"
        ),
    )

class Probability(U.ActivityEdge, U.ParameterSet):
    """When the <<probability>> stereotype is applied to edges coming out of decision nodes and object nodes, it provides an expression for the probability that the edge will be traversed. These shall be between zero and one inclusive, and add up to one for edges with same source at the time the probabilities are used. When the <<probability>> stereotype is applied to output parameter sets, it gives the probability the parameter set will be given values at runtime. These shall be between zero and one inclusive, and add up to one for output parameter sets of the same behavior at the time the probabilities are used."""
    _STEREO = "SysML::Activities::Probability"
    _BASE_METACLASSES = ("ActivityEdge", "ParameterSet")
    _DECL = {
    # Value of the probability
    'probability': _Ref('probability', U.ValueSpecification),
    }
    CONSTRAINTS = (
        ("1_source_decisionnode_or_objectnode",
         "(no specification serialized)"
        ),
        ("2_all_outgoing_edges",
         "(no specification serialized)"
        ),
        ("3_all_parametersets",
         "(no specification serialized)"
        ),
        ("4_all_outputparameter_in_parametersets",
         "(no specification serialized)"
        ),
    )

class Problem(U.Comment):
    """A Problem documents a deficiency, limitation, or failure of one or more model elements to satisfy a requirement or need, or other undesired outcome. It may be used to capture problems identified during analysis, design, verification, or manufacture and associate the problem with the relevant model elements. Problem is a stereotype of comment and may be attached to any other model element in the same manner as a comment."""
    _STEREO = "SysML::ModelElements::Problem"
    _BASE_METACLASSES = ("Comment")

class PropertySpecificType(U.Classifier):
    """<p> The PropertySpecificType stereotype can be applied to classifiers that type exactly one property and that are owned by the owner of that property. Classifiers with this stereotype applied shall be generalized by at most one other classifier. </p><p> Instances of a property-specific type are exactly those that are values of the property it types, in all instances of the property owner. Values are (de)classified under property-specific types as they are (removed from) added to the property they type: <ul> <li>quantityKind : InstanceSpecification [0..1]<br/>A kind of quantity, represented by an InstanceSpecification classified by a kind of SysML QuantityKind, that may be stated by means</li...[truncated]"""
    _STEREO = "SysML::Blocks::PropertySpecificType"
    _BASE_METACLASSES = ("Classifier")
    CONSTRAINTS = (
        ("1_only_one_property",
         "(no specification serialized)"
        ),
    )

class ProxyPort(U.Port):
    """<p> Proxy ports identify features of the owning block or its internal parts that are available to external blocks through external connectors to the ports. They do not specify a separate element of the system from the owning block or internal parts. Actions on features of a proxy port have the same effect as if they were acting on features of the owning block or internal parts the port stands in for, and changes to features of the owning block or internal parts that the proxy port makes available to external blocks are visible to those blocks via connectors to the port. (This applies to provided features; for required features, see DirectedFeature.) Proxy ports do not specify their own behav...[truncated]"""
    _STEREO = "SysML::Ports&Flows::ProxyPort"
    _BASE_METACLASSES = ("Port")
    CONSTRAINTS = (
        ("1_not_fullport",
         "(no specification serialized)"
        ),
        ("2_interfaceblock",
         "(no specification serialized)"
        ),
        ("3_subports_are_proxyports",
         "(no specification serialized)"
        ),
    )

class Rationale(U.Comment):
    """A Rationale documents the justification for decisions and the requirements, design, and other decisions. A Rationale can be attached to any model element including relationships. It allows the user, for example, to specify a rationale that may reference more detailed documentation such as a trade study or analysis report. Rationale is a stereotype of comment and may be attached to any other model element in the same manner as a comment."""
    _STEREO = "SysML::ModelElements::Rationale"
    _BASE_METACLASSES = ("Comment")

class Refine(U.Abstraction, DirectedRelationshipPropertyPath):
    """The Refine stereotype specializes UML4SysML Refine and DirectedRelationshipPropertyPath to enable refinements to identify their sources and targets by a multi-level path of accessible properties from context blocks for the sources and targets."""
    _STEREO = "SysML::Requirements::Refine"
    _BASE_METACLASSES = ("Abstraction")
    CONSTRAINTS = (
        ("2_binary",
         "(no specification serialized)"
        ),
    )

class Requirement(U.Class, AbstractRequirement):
    """<p> A requirement specifies a capability or condition that must (or should) be satisfied. A requirement may specify a function that a system must perform or a performance condition that a system must satisfy. Requirements are used to establish a contract between the customer (or other stakeholder) and those responsible for designing and implementing the system. </p><p> A requirement is a stereotype of both Class and Abstract Requirement. Compound requirements can be created by using the nesting capability of the class definition mechanism. The default interpretation of a compound requirement, unless stated differently by the compound requirement itself, is that all its subrequirements shall ...[truncated]"""
    _STEREO = "SysML::Requirements::Requirement"
    _BASE_METACLASSES = ("Class")
    CONSTRAINTS = (
        ("1_no_operation",
         "(no specification serialized)"
        ),
        ("2_no_attribute",
         "(no specification serialized)"
        ),
        ("3_no_association",
         "(no specification serialized)"
        ),
        ("4_no_generalization",
         "(no specification serialized)"
        ),
        ("5_nestedclassifiers_are_requirements",
         "(no specification serialized)"
        ),
        ("6_not_a_type",
         "(no specification serialized)"
        ),
    )

class Satisfy(Trace, U.Abstraction):
    """A Satisfy relationship is a dependency between a requirement and a model element that fulfills the requirement. As with other dependencies, the arrow direction points from the satisfying (client) model element to the (supplier) requirement that is satisfied."""
    _STEREO = "SysML::Requirements::Satisfy"
    _BASE_METACLASSES = ("Abstraction")
    CONSTRAINTS = (
        ("1_supplier_is_requirement",
         "(no specification serialized)"
        ),
    )

class Stakeholder(U.Classifier):
    """A stakeholder represents a role, group, or individual who has concerns that will be addressed by the View of the model."""
    _STEREO = "SysML::ModelElements::Stakeholder"
    _BASE_METACLASSES = ("Classifier")
    _DECL = {
    'concern': _Ref('concern', str, multi=True, lo=0, hi='*', derived=True),
    'concernList': _Ref('concernList', U.Comment, multi=True, lo=0, hi='*'),
    }
    CONSTRAINTS = (
        ("1_not_association",
         "(no specification serialized)"
        ),
    )

class TestCase(U.Behavior):
    """A test case is a method for verifying a requirement is satisfied."""
    _STEREO = "SysML::Requirements::TestCase"
    _BASE_METACLASSES = ("Behavior", "Operation")
    CONSTRAINTS = (
        ("1_return_verdictkind",
         "(no specification serialized)"
        ),
    )

class TriggerOnNestedPort(U.Trigger, ElementPropertyPath):
    """This extends trigger to support nested ports. It identifies a nested port by a multi-level path of ports from the object receiving the triggering events. It is not applicable to full ports."""
    _STEREO = "SysML::Ports&Flows::TriggerOnNestedPort"
    _BASE_METACLASSES = ("Trigger")
    _DECL = {
    # Gives a series of ports that identifies a port on which the event is occurring, in the context o
    # f a block in which the trigger is used. The ordering of ports is from a port of the receiving ob
    # ject, through a port of each intermediate block that types the preceding port, ending in a prope
    # rty with a type that owns or inherits the port given by the port property of the trigger. The po
    # rt property is not included in the onNestedPort list. The same port might appear more than once 
    # because a block can own a port with the same block as a type, or another block that has the same
    #  property.
    'onNestedPort': _Ref('onNestedPort', U.Port, multi=True, lo=1, hi='*'),
    }
    CONSTRAINTS = (
        ("1_single_proxyport",
         "(no specification serialized)"
        ),
        ("2_no_fullport",
         "(no specification serialized)"
        ),
        ("3_onnestedport_first_owned_by_context",
         "(no specification serialized)"
        ),
        ("4_path_consistency",
         "(no specification serialized)"
        ),
        ("5_onnestedport_last_type_owns_trigger_port",
         "(no specification serialized)"
        ),
    )

class ValueType(U.DataType):
    """<p> A ValueType defines types of values that may be used to express information about a system, but cannot be identified as the target of any reference. Since a value cannot be identified except by means of the value itself, each such value within a model is independent of any other, unless other forms of constraints are imposed. </p><p> Value types may be used to type properties, operation parameters, or potentially other elements within SysML. SysML defines ValueType as a stereotype of UML DataType to establish a more neutral term for system values that may never be given a concrete data representation. For example, the SysML "Real" ValueType expresses the mathematical concept of a real nu...[truncated]"""
    _STEREO = "SysML::Blocks::ValueType"
    _BASE_METACLASSES = ("DataType")
    _DECL = {
    # <p> A kind of quantity, represented by an InstanceSpecification classified by a kind of SysML Qu
    # antityKind, that may be stated by means of units. A value type may optionally specify a quantity
    #  kind without any unit. Such a value type may be used to type a value specification to represent
    #  it in an abstract form independent of any specific units. </p><p> Value types may be used to ty
    # pe properties, operation parameters, or potentially other elements within SysML. SysML defines V
    # alueType as a stereotype of UML DataType to establish a more neutral term for system values that
    #  may never be given a concrete data representation. For example, the SysML "Real" ValueType expr
    # esses the mathematical concept of a real number, but does not impose any restrictions on the pre
    # cision or scale of a fixed or floating-point representation that expresses this concept. More sp
    # ecific value types can define the concrete data representations that a digital computer can proc
    # ess, such as conventional Float, Integer, or String types. </p><p> SysML ValueType adds an abili
    # ty to carry a unit of measure and quantity kind associated with the value. A quantity kind is a 
    # kind of quantity that may be stated in terms of defined units, but does not restrict the selecti
    # on of a unit to state the value. A unit is a particular value in terms of which a quantity of th
    # e same quantity kind may be expressed. A SysML ValueType and its quantityKind establishes, via U
    # ML typing, the associative relationship between a particular "quantity" [VIM3-1.1] (modeled as a
    #  SysML value property typed by a ValueType) and a "kind of quantity" [VIM3-1.2] (the ValueType::
    # quantityKind of the SysML value propertys type). This UML/SysML associative relationship reflect
    # s the terminological distinction made in VIM3 between the concepts of "quantity" [VIM3-1.1] and 
    # "kind-of-quantity" [VIM3- 1.2] that "cannot be in a generic or partitive hierarchical relation t
    # o each other" [Dybkaer-2010]. </p><p> A SysML ValueType may define its own properties and/or ope
    # rations, just as for a UML DataType. See 8.3.2.4, Block for property classifications that SysML 
    # defines for either a Block or ValueType. </p>
    'quantityKind': _Ref('quantityKind', U.InstanceSpecification),
    # A unit, represented by an InstanceSpecification classified by a kind of SysML Unit, in terms of 
    # which the magnitudes of other quantities that have the same quantity kind can be stated.
    'unit': _Ref('unit', U.InstanceSpecification),
    }
    CONSTRAINTS = (
        ("1_specializations_are_valuetypes",
         "(no specification serialized)"
        ),
        ("2_unit",
         "(no specification serialized)"
        ),
        ("3_quantitykind",
         "(no specification serialized)"
        ),
    )

class Verify(Trace, U.Abstraction):
    """A Verify relationship is a dependency between a requirement and a test case or other model element that can determine whether a system fulfills the requirement. As with other dependencies, the arrow direction points from the (client) element to the (supplier) requirement."""
    _STEREO = "SysML::Requirements::Verify"
    _BASE_METACLASSES = ("Abstraction")
    CONSTRAINTS = (
        ("1_supplier_is_requirement",
         "(no specification serialized)"
        ),
    )

class View(U.Class):
    """<p> A View is a model element that represents a real world artifact that can be presented to stakeholders. The view is the result of querying one or more models that are defined by a viewpoint method. The view shall conform to the viewpoint in terms of the viewpoint stakeholders, concerns, method, language, and presentation requirements. </p><p> It is sometimes desirable to construct views from other views, and to establish an order for presenting the views. Views may include one or more views as properties, each of which conforms to their viewpoint. The order of the referenced views is reflected in the property order. </p><p> The information may be presented to the stakeholder in any format...[truncated]"""
    _STEREO = "SysML::ModelElements::View"
    _BASE_METACLASSES = ("Class")
    _DECL = {
    # The list of stakeholders is derived from the viewpoint the view conforms to.
    'stakeholder': _Ref('stakeholder', None, multi=True, lo=0, hi='*', derived=True),
    # The viewpoint for this View is derived from the conform relationship.
    'viewpoint': _Ref('viewpoint', None, derived=True),
    }
    CONSTRAINTS = (
        ("1_single_viewpoint",
         "(no specification serialized)"
        ),
        ("2_viewpoint_derived_from_conform",
         "(no specification serialized)"
        ),
        ("3_stakeholder_derived_from_conform",
         "(no specification serialized)"
        ),
    )

class Viewpoint(U.Class):
    """A Viewpoint is a specification of the conventions and rules for constructing and using a view for the purpose of addressing a set of stakeholder concerns. The languages and methods for specifying a view may reference languages and methods in another viewpoint. They specify the elements expected to be represented in the view, and may be formally or informally defined. For example, the security viewpoint may require the security requirements, security functional and physical architecture, and security test cases."""
    _STEREO = "SysML::ModelElements::Viewpoint"
    _BASE_METACLASSES = ("Class")
    _DECL = {
    # The interest of the stakeholders displayed as the body of the comments from concernList.
    'concern': _Ref('concern', str, multi=True, lo=0, hi='*', derived=True),
    # The interests of the stakeholders addressed by this viewpoint.
    'concernList': _Ref('concernList', U.Comment, multi=True, lo=0, hi='*'),
    # The languages used to express the models that represent content which is represented by the view
    # . The language specification such as its metamodel, profile, or other language specification is 
    # referred to by its URI.
    'language': _Ref('language', str, multi=True, lo=0, hi='*'),
    # The behavior is derived from the method of the operation with the Create stereotype.
    'method': _Ref('method', U.Behavior, multi=True, lo=0, hi='*', derived=True),
    # The specifications prescribed for formatting and styling the view.
    'presentation': _Ref('presentation', str, multi=True, lo=0, hi='*'),
    # The purpose addresses the stakeholder concerns.
    'purpose': _Ref('purpose', str),
    # Set of stakeholders whose concerns are to be addressed by the viewpoint.
    'stakeholder': _Ref('stakeholder', None, multi=True, lo=0, hi='*'),
    }
    CONSTRAINTS = (
        ("1_method_derived_from_create_operations",
         "(no specification serialized)"
        ),
        ("2_create_view_operation",
         "(no specification serialized)"
        ),
    )

class _InterfaceBlock(InterfaceBlock, U.Class):
    """The ~InterfaceBlock stereotype (shall be pronounced: "conjugated interface block") is a specialization of InterfaceBlock that has the same features as its original InterfaceBlock except that its DirectedFeatures and FlowProperties are reversed (conjugated), for example, in flow properties are conjugated as out flow properties and provided features are conjugated as required features. Conjugation is specified by a constraint giving the features of ~InterfaceBlocks according to those of their original InterfaceBlocks (see the Constraints subsection below). It is expected that tools conforming to this specification automatically create features of ~InterfaceBlocks."""
    _STEREO = "SysML::Ports&Flows::~InterfaceBlock"
    _BASE_METACLASSES = ("Class")
    _DECL = {
    # The InterfaceBlock that this is a conjugation of.
    'original': _Ref('original', None),
    }
    CONSTRAINTS = (
        ("enforced_name",
         "(no specification serialized)"
        ),
        ("inverted_features",
         "(no specification serialized)"
        ),
    )

# ---------------------------------------------------------------------------
# extension metadata: stereotype -> ((metaclass, required), ...)
# ---------------------------------------------------------------------------
_EXTENSIONS = {
    "Auxiliary": (("Class", False),),
    "BuildComponent": (("Component", False),),
    "Call": (("Usage", False),),
    "Create": (("BehavioralFeature", False), ("Usage", False),),
    "Derive": (("Abstraction", False),),
    "Destroy": (("BehavioralFeature", False),),
    "Document": (("Artifact", False),),
    "Entity": (("Component", False),),
    "Executable": (("Artifact", False),),
    "File": (("Artifact", False),),
    "Focus": (("Class", False),),
    "Framework": (("Package", False),),
    "Implement": (("Component", False),),
    "ImplementationClass": (("Class", False),),
    "Instantiate": (("Usage", False),),
    "Library": (("Artifact", False),),
    "Metaclass": (("Class", False),),
    "Metamodel": (("Model", False),),
    "ModelLibrary": (("Package", False),),
    "Process": (("Component", False),),
    "Realization": (("Classifier", False),),
    "Refine": (("Abstraction", False),),
    "Responsibility": (("Usage", False),),
    "Script": (("Artifact", False),),
    "Send": (("Usage", False),),
    "Service": (("Component", False),),
    "Source": (("Artifact", False),),
    "Specification": (("Classifier", False),),
    "Subsystem": (("Component", False),),
    "SystemModel": (("Model", False),),
    "Trace": (("Abstraction", False),),
    "Type": (("Class", False),),
    "Utility": (("Class", False),),
    "AbstractRequirement": (("NamedElement", False),),
    "AcceptChangeStructuralFeatureEventAction": (("AcceptEventAction", False),),
    "AddFlowPropertyValueOnNestedPortAction": (("AddStructuralFeatureValueAction", False),),
    "AdjunctProperty": (("Property", False),),
    "Allocate": (("Abstraction", False),),
    "AllocateActivityPartition": (("ActivityPartition", False),),
    "BindingConnector": (("Connector", False),),
    "Block": (("Class", False),),
    "BoundReference": (("Property", False),),
    "ChangeStructuralFeatureEvent": (("ChangeEvent", False),),
    "ClassifierBehaviorProperty": (("Property", False),),
    "Conform": (("Generalization", False),),
    "ConnectorProperty": (("Property", False),),
    "ConstraintBlock": (("Class", False),),
    "ControlOperator": (("Behavior", False), ("Operation", False),),
    "Copy": (("Abstraction", False),),
    "DeriveReqt": (("Abstraction", False),),
    "DirectedFeature": (("Feature", False),),
    "DirectedRelationshipPropertyPath": (("DirectedRelationship", False),),
    "DistributedProperty": (("Property", False),),
    "ElementGroup": (("Comment", False),),
    "ElementPropertyPath": (("Element", False),),
    "EndPathMultiplicity": (("Property", False),),
    "Expose": (("Dependency", False),),
    "FlowPort": (("Port", False),),
    "FlowProperty": (("Property", False),),
    "FlowSpecification": (("Interface", False),),
    "FullPort": (("Port", False),),
    "InvocationOnNestedPortAction": (("InvocationAction", False),),
    "ItemFlow": (("InformationFlow", False),),
    "NestedConnectorEnd": (("ConnectorEnd", False),),
    "NoBuffer": (("ObjectNode", False),),
    "Optional": (("Parameter", False),),
    "Overwrite": (("ObjectNode", False),),
    "ParticipantProperty": (("Property", False),),
    "Probability": (("ActivityEdge", False), ("ParameterSet", False),),
    "Problem": (("Comment", False),),
    "PropertySpecificType": (("Classifier", False),),
    "ProxyPort": (("Port", False),),
    "Rate": (("ActivityEdge", False), ("ObjectNode", False), ("Parameter", False),),
    "Rationale": (("Comment", False),),
    "Refine": (("Abstraction", False),),
    "Requirement": (("Class", False),),
    "Satisfy": (("Abstraction", False),),
    "Stakeholder": (("Classifier", False),),
    "TestCase": (("Behavior", False), ("Operation", False),),
    "Trace": (("Abstraction", False),),
    "TriggerOnNestedPort": (("Trigger", False),),
    "ValueType": (("DataType", False),),
    "Verify": (("Abstraction", False),),
    "View": (("Class", False),),
    "Viewpoint": (("Class", False),),
    "_InterfaceBlock": (("Class", False),),
}
# ---------------------------------------------------------------------------
# post-import assembly (mirror of uml25._finish for profile classes)
# ---------------------------------------------------------------------------
_STEREOTYPES = [Auxiliary, BuildComponent, Call, Create, Derive, Destroy, File, Document, Entity, Executable, Focus, Framework, Implement, ImplementationClass, Instantiate, Library, Metaclass, Metamodel, ModelLibrary, Process, Realization, Refine, Responsibility, Script, Send, Service, Source, Specification, Subsystem, SystemModel, Trace, Type, Utility, AbstractRequirement, AcceptChangeStructuralFeatureEventAction, ElementPropertyPath, AddFlowPropertyValueOnNestedPortAction, AdjunctProperty, DirectedRelationshipPropertyPath, Allocate, AllocateActivityPartition, BindingConnector, Block, EndPathMultiplicity, BoundReference, ChangeStructuralFeatureEvent, ClassifierBehaviorProperty, Conform, ConnectorProperty, ConstraintBlock, Rate, Continuous, ControlOperator, Trace, Copy, DeriveReqt, DirectedFeature, Discrete, DistributedProperty, ElementGroup, Expose, FlowPort, FlowProperty, FlowSpecification, FullPort, InterfaceBlock, InvocationOnNestedPortAction, ItemFlow, NestedConnectorEnd, NoBuffer, Optional, Overwrite, ParticipantProperty, Probability, Problem, PropertySpecificType, ProxyPort, Rationale, Refine, Requirement, Satisfy, Stakeholder, TestCase, TriggerOnNestedPort, ValueType, Verify, View, Viewpoint, _InterfaceBlock]

def _finish():
    for c in _STEREOTYPES:
        decl = c.__dict__.get('_DECL')
        if not decl:
            continue
        for d in decl.values():
            d.owner_cls = c.__name__
        for n, d in decl.items():
            setattr(c, n, d)
_finish()

