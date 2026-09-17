"""UAF stereotype classes generated from the OMG profile XMI.

256 stereotypes, 112 tagged values, 259 constraints
(metadata). Stereotypes fold their base metaclasses (Python inheritance)
with stereotype generalizations; base_* extension ends are consumed;
extension required/optional data is in _EXTENSIONS.
"""
from __future__ import annotations

import enum as _enum

from gen import uml25 as U
import gen.sysml as sysml
from gen.uml25 import _Ref  # noqa: F401

_URI = 'https://www.omg.org/spec/UAF/20211201/UAF'

class ActualMeasurementKind(_enum.Enum):
    Actual = "Actual"
    Required = "Required"
    Estimate = "Estimate"

class ActualMilestoneKind(_enum.Enum):
    InService = "InService"
    Deployed = "Deployed"
    NoLongerUsed = "NoLongerUsed"
    OutOfService = "OutOfService"
    Other = "Other"

class CapabilityKind(_enum.Enum):
    Strategic = "Strategic"
    Operational = "Operational"
    Service = "Service"
    Resource = "Resource"
    Personnel = "Personnel"
    Security = "Security"
    Other = "Other"

class ChallengeKind(_enum.Enum):
    Strategic = "Strategic"
    Enterprise = "Enterprise"
    Mission = "Mission"
    Business = "Business"
    Other = "Other"

class DriverKind(_enum.Enum):
    Strategic = "Strategic"
    Operational = "Operational"
    Service = "Service"
    Resource = "Resource"
    Personnel = "Personnel"
    Security = "Security"
    Project = "Project"
    Standard = "Standard"
    Other = "Other"
    Architecture_Principle = "Architecture Principle"

class EnvironmentKind(_enum.Enum):
    TerrainType = "TerrainType"
    WeatherConditions = "WeatherConditions"
    LightConditions = "LightConditions"
    CBRNEnvironment = "CBRNEnvironment"
    SituationType = "SituationType"

class GeoPoliticalExtentTypeKind(_enum.Enum):
    GeoFeatureType = "GeoFeatureType"
    RegionOfCountryType = "RegionOfCountryType"
    CountryType = "CountryType"
    RegionOfWorldType = "RegionOfWorldType"
    FacilityType = "FacilityType"
    SiteType = "SiteType"
    InstallationType = "InstallationType"
    OtherType = "OtherType"

class InformationKind(_enum.Enum):
    Information = "Information"
    DomainInformation = "DomainInformation"
    PositionReferenceFrame = "PositionReferenceFrame"
    PedigreeInformation = "PedigreeInformation"
    Data = "Data"

class InformationModelKind(_enum.Enum):
    Conceptual = "Conceptual"
    Logical = "Logical"
    Physical = "Physical"

class LocationKind(_enum.Enum):
    SolidVolume = "SolidVolume"
    Surface = "Surface"
    Line = "Line"
    Point = "Point"
    GeoStationaryPoint = "GeoStationaryPoint"
    PlanarSurface = "PlanarSurface"
    PolygonArea = "PolygonArea"
    RectangularArea = "RectangularArea"
    ElipticalArea = "ElipticalArea"
    CircularArea = "CircularArea"
    Other = "Other"

class LocationTypeKind(_enum.Enum):
    OtherType = "OtherType"
    SolidVolumeType = "SolidVolumeType"
    SurfaceType = "SurfaceType"
    LineType = "LineType"
    PointType = "PointType"
    GeoStationaryPointType = "GeoStationaryPointType"
    PlanarSurfaceType = "PlanarSurfaceType"
    PolygonAreaType = "PolygonAreaType"
    RectangularAreaType = "RectangularAreaType"
    ElipticalAreaType = "ElipticalAreaType"
    CircularAreaType = "CircularAreaType"

class OperationalExchangeKind(_enum.Enum):
    MaterielExchange = "MaterielExchange"
    OrganizationalExchange = "OrganizationalExchange"
    EnergyExchange = "EnergyExchange"
    InformationExchange = "InformationExchange"
    ConfigurationExchange = "ConfigurationExchange"
    GeoPoliticalExtentExchange = "GeoPoliticalExtentExchange"

class ProjectKind(_enum.Enum):
    Programme = "Programme"
    Portfolio = "Portfolio"
    Project = "Project"
    PersonnelDevelopment = "PersonnelDevelopment"

class ResourceExchangeKind(_enum.Enum):
    ResourceCommunication = "ResourceCommunication"
    ResourceMovement = "ResourceMovement"
    ResourceEnergyFlow = "ResourceEnergyFlow"
    GeoPoliticalExtentExchange = "GeoPoliticalExtentExchange"

class ResponsibleRoleKind(_enum.Enum):
    Manager = "Manager"
    ResponsibleOwner = "ResponsibleOwner"

class RoleKind(_enum.Enum):
    Part = "Part"
    Component = "Component"
    UsedConfiguration = "UsedConfiguration"
    HumanResource = "HumanResource"
    Platform = "Platform"
    System = "System"
    SubOrganization = "SubOrganization"
    PostRole = "PostRole"
    ResponsibilityRole = "ResponsibilityRole"
    Equipment = "Equipment"
    SubSystemPart = "SubSystemPart"
    UsedPhysicalArchitecture = "UsedPhysicalArchitecture"
    HostedSoftware = "HostedSoftware"
    ArtifactComponent = "ArtifactComponent"
    NaturalResourceComponent = "NaturalResourceComponent"
    Other = "Other"

class RuleKind(_enum.Enum):
    StructuralAssertion = "StructuralAssertion"
    ActionAssertion = "ActionAssertion"
    Derivation = "Derivation"
    Contract = "Contract"
    Constraint = "Constraint"
    Guidance = "Guidance"
    SecurityPolicy = "SecurityPolicy"
    Caveat = "Caveat"

class ServiceExchangeKind(_enum.Enum):
    MaterielExchange = "MaterielExchange"
    OrganizationalExchange = "OrganizationalExchange"
    EnergyExchange = "EnergyExchange"
    InformationExchange = "InformationExchange"
    ConfigurationExchange = "ConfigurationExchange"

class ValueItemKind(_enum.Enum):
    Time = "Time"
    Cost = "Cost"
    Quality = "Quality"
    Revenue = "Revenue"
    Benefit = "Benefit"
    KPI = "KPI"
    Loss = "Loss"
    Other = "Other"

class WholeLifeConfigurationKind(_enum.Enum):
    Service = "Service"
    ResourcePerformer = "ResourcePerformer"
    OrganizationalResource = "OrganizationalResource"


class UAFElement(U.Element):
    """Abstract super type for all of the UAF elements. It provides a way for all of the UAF elements to have a common set of properties."""
    _STEREO = "UAF::Summary and Overview::UAFElement"
    _BASE_METACLASSES = ("Element",)
    _ABSTRACT = True
    _DECL = {
    # Captures Unique identifier for the element.
    'URI_': _Ref('URI_', str),
    # Relates a UAFElement to the Standard that the UAFElement is conforming to.
    'conformsTo': _Ref('conformsTo', 'Standard', multi=True, lo=0, hi='*'),
    }

class Achiever(U.InstanceSpecification, UAFElement):
    """An ActualResource, ActualProject or ActualStrategicPhase that can deliver a desired effect."""
    _STEREO = "UAF::States::Achiever"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = True

class MeasurableElement(UAFElement, U.Element):
    """Abstract grouping for elements that can be measured by applying MeasurementSets to them."""
    _STEREO = "UAF::Parameters::MeasurableElement"
    _BASE_METACLASSES = ("Element",)
    _ABSTRACT = True
    _DECL = {
    # Relates the MeasurableElement to the ActualMeasurementSet that provides its ActualMeasurements.
    'actualMeasurementSet': _Ref('actualMeasurementSet', 'ActualMeasurementSet', multi=True, lo=0, hi='*'),
    # Relates the MeasurableElement to the MeasurementSet that provides its Measurements by which it c
    # an be measured.
    'measurementSet': _Ref('measurementSet', 'MeasurementSet', multi=True, lo=0, hi='*'),
    }

class Achieves(U.Dependency, MeasurableElement):
    """A dependency relationship that exists between an ActualState (e.g., observed/measured during testing) of an element that attempts to achieve a desired effect and an Achiever."""
    _STEREO = "UAF::States::Achieves"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("Achieves.client",
         "Value for the client metaproperty must be stereotyped by the specialization of «Achiever"
         "»."
        ),
        ("Achieves.supplier",
         "Value for the supplier metaproperty must be stereotyped by the specialization of «Actual"
         "State»."
        ),
    )

class AffectableElement(UAFElement, U.Element):
    """An abstract grouping of elements that can be affected by Risk."""
    _STEREO = "UAF::Parameters::AffectableElement"
    _BASE_METACLASSES = ("Element",)
    _ABSTRACT = True

class Activity(U.Activity, MeasurableElement, AffectableElement):
    """An abstract element that represents a behavior or process (i.e. a Function or OperationalActivity) that can be performed by a Performer."""
    _STEREO = "UAF::Processes::Activity"
    _BASE_METACLASSES = ("Activity",)
    _ABSTRACT = True
    _DECL = {
    # The environment under which an activity is performed.
    'activityPerformableUnderCondition': _Ref('activityPerformableUnderCondition', 'ActualCondition', multi=True, lo=0, hi='*'),
    }

class ActualState(UAFElement, U.Element):
    """Abstract element that applies temporal extent to a set of elements realized as Instance Specifications."""
    _STEREO = "UAF::Taxonomy::ActualState"
    _BASE_METACLASSES = ("Element",)
    _ABSTRACT = True
    _DECL = {
    # End time for all "actual" elements.
    'endDate': _Ref('endDate', 'ISO8601DateTime'),
    # Start time for all "actual" elements.
    'startDate': _Ref('startDate', 'ISO8601DateTime'),
    }

class ActualPropertySet(U.InstanceSpecification, ActualState):
    """A set or collection of Actual properties."""
    _STEREO = "UAF::Parameters::ActualPropertySet"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ActualPropertySet.classifier",
         "Value for the classifier metaproperty must be stereotyped by the specialization of «Prop"
         "ertySet»."
        ),
    )

class ActualCondition(ActualPropertySet, U.InstanceSpecification):
    """An actual situation with respect to circumstances under which an OperationalActivity, Function or ServiceFunction can be performed."""
    _STEREO = "UAF::Parameters::ActualCondition"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ActualCondition.classifier",
         "Value for the classifier metaproperty has to be stereotyped «Condition» or its specializ"
         "ations."
        ),
    )

class ActualEffect(ActualPropertySet, U.InstanceSpecification):
    """A real world phenomenon that follows and is caused by some previous phenomenon."""
    _STEREO = "UAF::States::ActualEffect"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False
    _DECL = {
    # Condition under which the Effect can be achieved.
    'enablingCondition': _Ref('enablingCondition', 'ActualCondition', multi=True, lo=0, hi='*'),
    }
    CONSTRAINTS = (
        ("ActualEffect.classifier",
         "Value for the classifier metaproperty must be stereotyped by «Effect» or its specializat"
         "ions."
        ),
    )

class ActualStrategicPhase(Achiever, ActualPropertySet, U.InstanceSpecification):
    """A phase of an actual enterprise, mission, ValueStream or EnduringTask endeavor."""
    _STEREO = "UAF::Processes::ActualStrategicPhase"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = True
    CONSTRAINTS = (
        ("ActualStrategicPhase.classifier",
         "Value for the classifier metaproperty must be stereotyped by «StrategicPhase» or its spe"
         "cializations."
        ),
        ("ActualStrategicPhase.start/endDate",
         "Must fall within the start and end dates of the enclosing ActualStrategicPhase having th"
         "is ActualStrategicPhase set as a value for a slot."
        ),
    )

class ActualEnduringTask(ActualStrategicPhase, U.InstanceSpecification):
    """An actual undertaking recognized by an enterprise as being essential to achieving its goals - i.e. a strategic specification of what the enterprise does."""
    _STEREO = "UAF::Processes::ActualEnduringTask"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False

class ActualEnterprisePhase(ActualStrategicPhase, U.InstanceSpecification):
    """A time period within which a set of Capabilities are deployed."""
    _STEREO = "UAF::Processes::ActualEnterprisePhase"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False
    _DECL = {
    # Relates the ActualEnterprisePhase to the ActualEnduringTasks that are intended to be implemented
    #  during that phase.
    'statementTask': _Ref('statementTask', 'ActualEnduringTask', multi=True, lo=0, hi='*'),
    }

class ActualEnvironment(ActualCondition, U.InstanceSpecification):
    """Actual circumstances of an Environment."""
    _STEREO = "UAF::Parameters::ActualEnvironment"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ActualEnvironment.classifier",
         "Value for the classifier metaproperty has to be stereotyped «Environment» or its special"
         "izations."
        ),
    )

class ActualLocation(ActualCondition, U.InstanceSpecification):
    """A physical location, for example using text to provide an address, Geo-coordinates, etc."""
    _STEREO = "UAF::Parameters::ActualLocation"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False
    _DECL = {
    # String describing the address of the ActualLocation, i.e. "1600 Pennsylvania avenue", "The White
    #  House"
    'address': _Ref('address', str),
    # String describing a location kind that is not in the LocationKind enumerated list
    'customKind': _Ref('customKind', str),
    # Enumerated value describing the kind of ActualLocation.
    'locationKind': _Ref('locationKind', LocationKind),
    # Boolean that indicates if the ActualLocation address is embedded in the ActualLocation name. By 
    # default = false.
    'locationNamedByAddress': _Ref('locationNamedByAddress', bool),
    }
    CONSTRAINTS = (
        ("ActualLocation.classifier",
         "Classifier metaproperty value must be stereotyped «Location» or its specializations."
        ),
    )

class ActualMeasurement(ActualState, U.Slot):
    """An actual value that is applied to a Measurement."""
    _STEREO = "UAF::Parameters::ActualMeasurement"
    _BASE_METACLASSES = ("Slot",)
    _ABSTRACT = False
    _DECL = {
    # Enumerated value describing the intent of the ActualMeasurement.
    'intention': _Ref('intention', ActualMeasurementKind),
    }
    CONSTRAINTS = (
        ("ActualMeasurement.definingFeature",
         "Value for the definingFeature metaproperty must be stereotyped «Measurement» or its spec"
         "ializations."
        ),
        ("ActualMeasurement.owningInstance",
         "Value for the owningInstance metaproperty must be stereotyped «ActualPropertySet» or its"
         " specializations."
        ),
    )

class ActualMeasurementSet(ActualPropertySet, U.InstanceSpecification):
    """A set of ActualMeasurements."""
    _STEREO = "UAF::Parameters::ActualMeasurementSet"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False
    _DECL = {
    # Relates the ActualMeasurementSet to the elements that are being measured.
    'appliesFor': _Ref('appliesFor', 'MeasurableElement', multi=True, lo=0, hi='*'),
    }
    CONSTRAINTS = (
        ("ActualMeasurementSet.classifier",
         "Classifier metaproperty value must be stereotyped «MeasurementSet» or its specialization"
         "s."
        ),
        ("ActualMeasurementSet.slot",
         "Value for the slot metaproperty must be stereotyped «ActualMeasurement» or its specializ"
         "ations."
        ),
    )

class Stakeholder(UAFElement, U.Element):
    """An individual organizational resource, or a type of organizational resource (both internal and external to the enterprise) who has an interest in, or is affected by, outcomes or intermediate effects generated or influenced by the enterprise."""
    _STEREO = "UAF::Summary and Overview::Stakeholder"
    _BASE_METACLASSES = ("Element",)
    _ABSTRACT = True
    _DECL = {
    # Relates a Stakeholder to a Concern.
    'stakeholderConcern': _Ref('stakeholderConcern', 'Concern', multi=True, lo=0, hi='*'),
    }

class SubjectOfResourceConstraint(UAFElement, U.Element):
    """An abstract grouping of elements that can be the subject of a ResourceConstraint."""
    _STEREO = "UAF::Constraints::SubjectOfResourceConstraint"
    _BASE_METACLASSES = ("Element",)
    _ABSTRACT = True

class CapableElement(UAFElement, U.Element):
    """An abstract type that represents a structural element that can exhibit capabilities."""
    _STEREO = "UAF::Processes::CapableElement"
    _BASE_METACLASSES = ("Element",)
    _ABSTRACT = True

class ActualResource(ActualPropertySet, Achiever, U.InstanceSpecification, SubjectOfResourceConstraint, CapableElement):
    """An instance of a ResourcePerformer in the real world."""
    _STEREO = "UAF::Taxonomy::ActualResource"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False
    _DECL = {
    # Relates the ActualResource to the ActualStates of an environment or location describing its situ
    # ation
    'actualCondition': _Ref('actualCondition', 'ActualCondition', multi=True, lo=0, hi='*'),
    # Relates an ActualResource to the ActualProjectMilestones. It is used to describe aspects of the 
    # lifecycle of an ActualResource.
    'milestone': _Ref('milestone', 'ActualProjectMilestone', multi=True, lo=0, hi='*'),
    }
    CONSTRAINTS = (
        ("ActualResource.classifier",
         "Classifier metaproperty value must be stereotyped by a specialization of «ResourcePerfor"
         "mer»."
        ),
    )

class ActualOrganizationalResource(ActualResource, U.InstanceSpecification, Stakeholder):
    """Abstract element for an ActualOrganization, ActualPerson or ActualPost."""
    _STEREO = "UAF::Taxonomy::ActualOrganizationalResource"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = True

class ActualResponsibleResource(ActualOrganizationalResource, U.InstanceSpecification):
    """An abstract grouping of responsible OrganizationalResources."""
    _STEREO = "UAF::Taxonomy::ActualResponsibleResource"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = True

class ActualOrganization(ActualResponsibleResource, U.InstanceSpecification):
    """An actual formal or informal organizational unit, e.g. "Driving and Vehicle Licensing Agency", "UAF team Alpha"."""
    _STEREO = "UAF::Taxonomy::ActualOrganization"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False
    _DECL = {
    # Standards that were ratified by this ActualOrganization.
    'ratifiedStandards': _Ref('ratifiedStandards', 'Standard', multi=True, lo=0, hi='*'),
    # Service office code or symbol
    'serviceType': _Ref('serviceType', str),
    # String providing a simplified means of identifying an ActualOrganization, i.e. SoftWareGroup cou
    # ld use SWG as the shortName.
    'shortName': _Ref('shortName', str),
    }
    CONSTRAINTS = (
        ("ActualOrganization.classifier",
         "Classifier metaproperty value must be stereotyped «Organization» or its specializations."
        ),
        ("ActualOrganization.slot",
         "Slot metaproperty value must be stereotyped «ActualOrganizationRole» or its specializati"
         "ons."
        ),
    )

class ActualResourceRole(U.Slot, UAFElement):
    """An instance of a ResourcePerformer."""
    _STEREO = "UAF::Structure::ActualResourceRole"
    _BASE_METACLASSES = ("Slot",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ActualResourceRole.definingFeature",
         "Value for definingFeature metaproperty has to be stereotyped «ResourceRole» or its speci"
         "alizations."
        ),
        ("ActualResourceRole.owningInstance",
         "Value for owningInstance metaproperty has to be stereotyped «ActualResource» or its spec"
         "ializations."
        ),
    )

class ActualOrganizationRole(ActualResourceRole, U.Slot):
    """An ActualOrganizationalResource that is applied to a ResourceRole."""
    _STEREO = "UAF::Structure::ActualOrganizationRole"
    _BASE_METACLASSES = ("Slot",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ActualOrganizationRole.owningInstance",
         "Value for owningInstance metaproperty has to be stereotyped «ActualOrganization» or its "
         "specializations."
        ),
    )

class ActualOutcome(ActualEffect, U.InstanceSpecification):
    """Something that happens or is produced as the final consequence or product and is related to one of the goals for the business or enterprise. Outcome is a special kind of effect, one that is usually at the end of a chain of effects, i.e. an "end effect"."""
    _STEREO = "UAF::States::ActualOutcome"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False

class ActualPerson(ActualResponsibleResource, U.InstanceSpecification):
    """An individual human being."""
    _STEREO = "UAF::Taxonomy::ActualPerson"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ActualPerson.classifier",
         "Value for the classifier metaproperty has to be stereotyped «Person» or its specializati"
         "ons."
        ),
    )

class ActualPost(ActualResponsibleResource, U.InstanceSpecification):
    """An actual, specific post, an instance of a Post "type" - e.g., "President of the United States of America." where the Post would be president."""
    _STEREO = "UAF::Taxonomy::ActualPost"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ActualPost.classifier",
         "Classifier metaproperty value must be stereotyped «Post» or its specializations."
        ),
    )

class ActualProject(ActualOrganizationalResource, Achiever, U.InstanceSpecification):
    """A time-limited planned endeavor executed by an ActualOrganization responsible for developing, deploying or decommissioning ResourcePerformers in accordance with ActualProjectMilestones."""
    _STEREO = "UAF::Roadmap::ActualProject"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False
    _DECL = {
    # Relates the ActualProjectMilestones to the relevant ActualProject.
    'ownedMilestone': _Ref('ownedMilestone', 'ActualProjectMilestone', multi=True, lo=0, hi='*', derived=True),
    # Enumerated value describing the kind of ActualProject.
    'projectKind': _Ref('projectKind', ProjectKind),
    }
    CONSTRAINTS = (
        ("ActualProject.classifier",
         "Value for the classifier metaproperty must be stereotyped «Project» or its specializatio"
         "ns."
        ),
        ("ActualProject.slot",
         "Value for the slot metaproperty must be stereotyped «ActualProjectRole», «ActualProjectM"
         "ilestoneRole», or their specializations."
        ),
    )

class ActualProjectMilestone(ActualPropertySet, U.InstanceSpecification):
    """An event with a start date in a ActualProject from which progress is measured."""
    _STEREO = "UAF::Roadmap::ActualProjectMilestone"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False
    _DECL = {
    # Relates an ActualProjectMilestone to the ActualResources that are affected by the milestone. It 
    # is used to describe aspects of the lifecycle of an ActualResource.
    'actualResource': _Ref('actualResource', 'ActualResource', multi=True, lo=0, hi='*'),
    # End time for this ActualProjectMilestone.
    'endDate': _Ref('endDate', 'ISO8601DateTime'),
    # Enumerated value describing the kind of ActualProjectMilestone.
    'kind': _Ref('kind', ActualMilestoneKind),
    'versionReleased': _Ref('versionReleased', 'VersionedElement', multi=True, lo=0, hi='*'),
    'versionWithdrawn': _Ref('versionWithdrawn', 'VersionedElement', multi=True, lo=0, hi='*'),
    }
    CONSTRAINTS = (
        ("ActualProjectMilestone.classifier",
         "Value for the classifier metaproperty must be stereotyped «ProjectMilestone» or its spec"
         "ializations."
        ),
    )

class ActualProjectMilestoneRole(ActualState, U.Slot):
    """An ActualProjectMilestone that is applied to a ProjectMilestoneRole."""
    _STEREO = "UAF::Roadmap::ActualProjectMilestoneRole"
    _BASE_METACLASSES = ("Slot",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ActualProjectMilestoneRole.definingFeature",
         "Value for the definingFeature metaproperty has to be stereotyped «ProjectMilestoneRole» "
         "or its specializations."
        ),
        ("ActualProjectMilestoneRole.owningInstance",
         "Value for the owningInstance metaproperty has to be stereotyped «ActualProject» or its s"
         "pecializations."
        ),
        ("ActualProjectMilestoneRole.value.instance",
         "Value for the value.instance metaproperty has to be stereotyped «ActualProjectMilestone»"
         " or its specializations."
        ),
    )

class ActualProjectRole(ActualState, U.Slot):
    """An ActualProject that is applied to a ProjectRole."""
    _STEREO = "UAF::Roadmap::ActualProjectRole"
    _BASE_METACLASSES = ("Slot",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ActualProjectRole.definingFeature",
         "Value for the definingFeature metaproperty has to be stereotyped «ProjectRole» or its sp"
         "ecializations."
        ),
        ("ActualProjectRole.owningInstance",
         "Value for the owningInstance metaproperty has to be stereotyped «ActualProject» or its s"
         "pecializations."
        ),
        ("ActualProjectRole.value.instance",
         "Value for the value.instance metaproperty has to be stereotyped «ActualProject» or its s"
         "pecializations."
        ),
    )

class ActualResourceRelationship(sysml.ItemFlow, U.InformationFlow, UAFElement):
    """An abstract element that details the ActualOrganizationalResources that are able to carry out an ActualResponsibility."""
    _STEREO = "UAF::Connectivity::ActualResourceRelationship"
    _BASE_METACLASSES = ("InformationFlow",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ActualResourceRelationship.informationSource",
         "Value for informationSource metaproperty must be stereotyped «ActualResource» or its spe"
         "cializations."
        ),
        ("ActualResourceRelationship.realizes",
         "Value for realizes metaproperty must be stereotyped «ResourceExchange» or its specializa"
         "tions."
        ),
        ("ActualResourceRelationship.informationTarget",
         "Value for informationTarget metaproperty must be stereotyped «ActualResource» or its spe"
         "cializations."
        ),
    )

class ActualResponsibility(ActualOrganizationalResource, U.InstanceSpecification):
    """The duty required of a Person or Organization."""
    _STEREO = "UAF::Taxonomy::ActualResponsibility"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ActualResponsibility.classifier",
         "Classifier metaproperty value must be stereotyped «Responsibility» or its specialization"
         "s."
        ),
    )

class ActualRisk(ActualPropertySet, U.InstanceSpecification):
    """An instance of a Risk. A value holder for Risk Measurements."""
    _STEREO = "UAF::Parameters::ActualRisk"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False
    _DECL = {
    # Enables association of an ActualRisk to an actual organizational role that is responsible for ex
    # ecuting the actual mitigation.
    'actualRiskOwner': _Ref('actualRiskOwner', 'ActualResponsibleResource'),
    # Asserts that an ActualRisk is applicable to an ActualResource.
    'affectedActualResource': _Ref('affectedActualResource', 'ActualResource'),
    }
    CONSTRAINTS = (
        ("ActualRisk.classifier",
         "Value for the classifier metaproperty must be stereotyped by «Risk» or its specializatio"
         "ns."
        ),
    )

class ActualService(ActualMeasurementSet, U.InstanceSpecification, CapableElement):
    """An instance of a Service."""
    _STEREO = "UAF::Constraints::ActualService"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ActualService.classifier",
         "Value for the classifier metaproperty must be stereotyped by «Service» or its specializa"
         "tions."
        ),
    )

class Affects(U.Dependency, MeasurableElement):
    """A dependency that asserts that a Risk is applicable to an Asset."""
    _STEREO = "UAF::Parameters::Affects"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("Affects.client",
         "Value for the client metaproperty must be stereotyped «Risk» or its specializations."
        ),
        ("Affects.supplier",
         "Value for the supplier metaproperty must be stereotyped «AffectableElement» or its speci"
         "alizations."
        ),
    )

class AffectsInContext(U.Dependency, MeasurableElement):
    """A dependency that asserts that a Risk is applicable to an AssetRole in the specific context or configuration."""
    _STEREO = "UAF::Parameters::AffectsInContext"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("AffectsInContext.client",
         "Value for the client metaproperty must be stereotyped «Risk» or its specializations."
        ),
        ("AffectsInContext.supplier",
         "Value for the supplier metaproperty must be stereotyped «AssetRole» or its specializatio"
         "ns."
        ),
    )

class Alias(MeasurableElement, U.Comment):
    """A metamodel Artifact used to define an alternative name for an element."""
    _STEREO = "UAF::Information::Alias"
    _BASE_METACLASSES = ("Comment",)
    _ABSTRACT = False
    _DECL = {
    # Someone or something that uses this alternative name.
    'nameOwner': _Ref('nameOwner', str, multi=True, lo=0, hi='*'),
    }
    CONSTRAINTS = (
        ("Alias.annotatedElement",
         "Value for the annotatedElement metaproperty must be stereotyped by the specialization of"
         " «UAFElement»."
        ),
    )

class ArbitraryConnector(U.Dependency, MeasurableElement):
    """Represents a visual indication of a connection used in high level operational concept diagrams."""
    _STEREO = "UAF::Taxonomy::ArbitraryConnector"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ArbitraryConnector.client",
         "The value for client metaproperty has to be stereotyped «ConceptRole» or its specializat"
         "ions."
        ),
        ("ArbitraryConnector.supplier",
         "The value for supplier metaproperty has to be stereotyped «ConceptRole» or its specializ"
         "ations."
        ),
    )

class ArchitecturalDescription(U.Package, MeasurableElement):
    """An Architecture Description is a work product used to express the Architecture of some System Of Interest. It provides executive-level summary information about the architecture description in a consistent form to allow quick reference and comparison between architecture descriptions -- It includes assumptions, constraints, and limitations that may affect high-level decisions relating to an architecture-based work program."""
    _STEREO = "UAF::Summary and Overview::ArchitecturalDescription"
    _BASE_METACLASSES = ("Package",)
    _ABSTRACT = False
    _DECL = {
    # Someone or something that has the authority to approve the ArchitecturalDescription.
    'approvalAuthority': _Ref('approvalAuthority', str, multi=True, lo=0, hi='*'),
    # Someone responsible for the creation of ArchitecturalDescription.
    'architect': _Ref('architect', str, multi=True, lo=0, hi='*'),
    # Indicates the type of framework used.
    'architectureFramework': _Ref('architectureFramework', str),
    # Any assumptions, constraints, and limitations contained in the ArchitecturalDescription, includi
    # ng those affecting deployment, communications performance, information assurance environments, e
    # tc.
    'assumptionAndConstraint': _Ref('assumptionAndConstraint', str, multi=True, lo=0, hi='*'),
    # The organization responsible for creating the ArchitecturalDescription.
    'creatingOrganization': _Ref('creatingOrganization', str, multi=True, lo=0, hi='*'),
    # Date that the ArchitecturalDescription was completed.
    'dateCompleted': _Ref('dateCompleted', str),
    # Name of the documented methodology that will be or has been used in describing the architecture.
    'methodologyUsed': _Ref('methodologyUsed', str, multi=True, lo=0, hi='*'),
    # Explains the need for the Architecture, what it will demonstrate, the types of analyses that wil
    # l be applied to it, who is expected to perform the analyses, what decisions are expected to be m
    # ade on the basis of each form of analysis, who is expected to make those decisions, and what act
    # ions are expected to result.
    'purpose': _Ref('purpose', str, multi=True, lo=0, hi='*'),
    # States the recommendations that have been developed based on the architecture effort. Examples i
    # nclude recommended system implementations, and opportunities for technology insertion.
    'recommendations': _Ref('recommendations', str, multi=True, lo=0, hi='*'),
    # State of the architecture description in terms of its development, baselining, activity (e.g. ac
    # tive or inactive), or some other factor of importance.
    'status': _Ref('status', str, multi=True, lo=0, hi='*'),
    # Summarizes the findings that have been developed so far. This may be updated several times durin
    # g the development of the ArchitecturalDescription.
    'summaryOfFindings': _Ref('summaryOfFindings', str, multi=True, lo=0, hi='*'),
    # Indicates whether the ArchitecturalDescription represents an Architecture that exists or will ex
    # ist in the future.
    'toBe': _Ref('toBe', bool),
    # Identifies any tools used to develop the ArchitecturalDescription as well as file names and form
    # ats if appropriate.
    'toolsUsed': _Ref('toolsUsed', str, multi=True, lo=0, hi='*'),
    # Identifier that indicates the particular edition or revision of the architecture description.
    'version': _Ref('version', str, multi=True, lo=0, hi='*'),
    # Indicates which views are used in the ArchitecturalDescription.
    'view': _Ref('view', 'View', multi=True, lo=0, hi='*'),
    # The architecture viewpoints used when developing the architecture description.
    'viewpoint': _Ref('viewpoint', 'Viewpoint', multi=True, lo=0, hi='*'),
    }

class ArchitecturalReference(U.Dependency, MeasurableElement):
    """A dependency relationship that specifies that one architectural description refers to another."""
    _STEREO = "UAF::Traceability::ArchitecturalReference"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ArchitecturalReference.client",
         "Value for the client metaproperty must be stereotyped «ArchitecturalDescription» or its "
         "specializations."
        ),
        ("ArchitecturalReference.supplier",
         "Value for the supplier metaproperty must be stereotyped «ArchitecturalDescription» or it"
         "s specializations."
        ),
    )

class Architecture(U.Class, UAFElement):
    """An abstract type that represents a generic architecture. Subtypes are OperationalArchitecture, Service Architecture, and ResourceArchitecture."""
    _STEREO = "UAF::Summary and Overview::Architecture"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = True
    _DECL = {
    # The description of an Architecture.
    'describedBy': _Ref('describedBy', 'ArchitecturalDescription', multi=True, lo=0, hi='*'),
    }

class Metadata(MeasurableElement, U.Comment):
    """A comment that can be applied to any element in the architecture. The attributes associated with this element details the relationship between the element and its related dublinCoreElement, metaDataScheme, category and name. This allows the element to be referenced using the Semantic Web."""
    _STEREO = "UAF::Information::Metadata"
    _BASE_METACLASSES = ("Comment",)
    _ABSTRACT = False
    _DECL = {
    # Defines the category of a Metadata element example: http://purl.org/dc/terms/abstract.
    'category': _Ref('category', str),
    # A metadata category that is a DublinCore tag.
    'dublinCoreElement': _Ref('dublinCoreElement', str),
    # A representation scheme that defines a set of Metadata.
    'metaDataScheme': _Ref('metaDataScheme', str),
    # The name of the Metadata.
    'name': _Ref('name', str),
    }
    CONSTRAINTS = (
        ("Metadata.annotatedElement",
         "Value for the annotatedElement metaproperty must be stereotyped by a specialization of «"
         "UAFElement»."
        ),
    )

class ArchitectureMetadata(Metadata, U.Comment):
    """Information associated with an ArchitecturalDescription, that supplements the standard set of tags used to summarize the Architecture. It states things like what methodology was used, notation, etc."""
    _STEREO = "UAF::Information::ArchitectureMetadata"
    _BASE_METACLASSES = ("Comment",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ArchitectureMetadata.annotatedElement",
         "Value for the annotatedElement metaproperty must be stereotyped «ArchitecturalDescriptio"
         "n» or its specializations."
        ),
    )

class ConceptItem(UAFElement, U.Element):
    """An abstract type which represents some part played by an asset or location in a HighLevelOperationalConcept."""
    _STEREO = "UAF::Taxonomy::ConceptItem"
    _BASE_METACLASSES = ("Element",)
    _ABSTRACT = True

class PropertySet(UAFElement, U.Element):
    """An abstract grouping of architectural elements that can own Measurements."""
    _STEREO = "UAF::Parameters::PropertySet"
    _BASE_METACLASSES = ("Element",)
    _ABSTRACT = True

class LocationHolder(UAFElement, U.Element):
    """Abstract grouping used to define elements that are allowed to be associated with a Location."""
    _STEREO = "UAF::Parameters::LocationHolder"
    _BASE_METACLASSES = ("Element",)
    _ABSTRACT = True
    _DECL = {
    # Relates a LocationHolder (i.e. OperationalPerformer, OperationalRole, ResourceRole etc.) to its 
    # ActualLocation.
    'physicalLocation': _Ref('physicalLocation', 'ActualLocation', multi=True, lo=0, hi='*'),
    # Relates a LocationHolder (i.e. OperationalPerformer, OperationalRole, ResourceRole etc.) to the 
    # Environment in which it is required to perform/be used.
    'requiredEnvironment': _Ref('requiredEnvironment', 'ActualEnvironment', multi=True, lo=0, hi='*'),
    }

class SubjectOfSecurityConstraint(UAFElement, U.Element):
    """An abstract grouping of elements that can be the subject of a SecurityConstraint."""
    _STEREO = "UAF::Constraints::SubjectOfSecurityConstraint"
    _BASE_METACLASSES = ("Element",)
    _ABSTRACT = True

class Asset(sysml.Block, U.Class, ConceptItem, PropertySet, LocationHolder, SubjectOfSecurityConstraint, AffectableElement):
    """An abstract element that indicates the types of elements that can be affected by Risk. Asset as applied to Security views is an abstract element that indicates the types of elements that can be considered as a subject for security analysis."""
    _STEREO = "UAF::Taxonomy::Asset"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = True
    _DECL = {
    # Enables association of an Asset to the set of security related measurements (MeasurementSet).
    'categoryCategorizesAsset': _Ref('categoryCategorizesAsset', 'MeasurementSet'),
    }

class AssetRole(MeasurableElement, SubjectOfSecurityConstraint, U.Element):
    """An abstract element that indicates the types of elements that can be affected by Risk in the particular context. AssetRole as applied to Security views, is an abstract element that indicates the type of elements that can be considered as a subject for security analysis in the particular context."""
    _STEREO = "UAF::Structure::AssetRole"
    _BASE_METACLASSES = ("Element",)
    _ABSTRACT = True

class Desirer(UAFElement, U.Element):
    """Abstract element used to group architecture elements that might desire a particular effect."""
    _STEREO = "UAF::States::Desirer"
    _BASE_METACLASSES = ("Element",)
    _ABSTRACT = True

class PhaseableElement(UAFElement, U.Element):
    """An abstract element that indicates the types of elements that can be assigned to a specific ActualStrategicPhase."""
    _STEREO = "UAF::Taxonomy::PhaseableElement"
    _BASE_METACLASSES = ("Element",)
    _ABSTRACT = True

class SubjectOfStrategicConstraint(UAFElement, U.Element):
    """An abstract grouping of elements that can be the subject of a StrategicConstraint."""
    _STEREO = "UAF::Constraints::SubjectOfStrategicConstraint"
    _BASE_METACLASSES = ("Element",)
    _ABSTRACT = True

class Capability(sysml.Block, U.Class, PropertySet, Desirer, PhaseableElement, AffectableElement, SubjectOfStrategicConstraint):
    """An enterprise's ability to Achieve a desired effect realized through a combination of ways and means (e.g. CapabilityConfigurations) along with specified measures."""
    _STEREO = "UAF::Taxonomy::Capability"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False
    _DECL = {
    # Identification of a special kind of Capability that is different from one of the predefined enum
    # erated kinds.
    'customKind': _Ref('customKind', str),
    # Selection of the enumerated kind for this element.
    'kind': _Ref('kind', CapabilityKind),
    }

class ResourceAsset(Asset, U.Class):
    """An abstract element used to group the elements of ResourcePerformer and ResourceInformation allowing them to own ResourceInformationRoles"""
    _STEREO = "UAF::Taxonomy::ResourceAsset"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = True

class Resource(PropertySet):
    """Abstract element grouping for all elements that can be conveyed by an Exchange."""
    _STEREO = "UAF::Connectivity::Resource"
    _BASE_METACLASSES = ()
    _ABSTRACT = True

class ResourceExchangeItem(Resource):
    """An abstract grouping for elements that defines the types of elements that can be exchanged between ResourcePerformers and conveyed by a ResourceExchange."""
    _STEREO = "UAF::Connectivity::ResourceExchangeItem"
    _BASE_METACLASSES = ()
    _ABSTRACT = True
    _DECL = {
    # Function using the ResourceExchangeItem internally.
    'function': _Ref('function', 'Function', multi=True, lo=0, hi='*', derived=True),
    }

class VersionedElement(U.Class, UAFElement):
    """An abstract grouping of ResourcePerformer and Service that allows VersionOfConfiguration to be related to ActualProjectMilestones."""
    _STEREO = "UAF::Roadmap::VersionedElement"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = True
    _DECL = {
    # Relates a VersionedElement to the ActualProjectMilestone. It indicates the ActualProjectMileston
    # e at which the VersionedElement is released.
    'versionReleasedAtMilestone': _Ref('versionReleasedAtMilestone', 'ActualProjectMilestone', multi=True, lo=0, hi='*'),
    # Relates a VersionedElement to the ActualProjectMilestone. It indicates the ActualProjectMileston
    # e at which the VersionedElement is withdrawn.
    'versionWithdrawnAtMilestone': _Ref('versionWithdrawnAtMilestone', 'ActualProjectMilestone', multi=True, lo=0, hi='*'),
    }

class SubjectOfForecast(U.Class, UAFElement):
    """An abstract grouping of elements that can be the subject of a Forecast."""
    _STEREO = "UAF::Roadmap::SubjectOfForecast"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = True

class OperationalExchangeItem(Resource):
    """An abstract grouping for elements that defines the types of elements that can be exchanged between OperationalPerformers and conveyed by an OperationalExchange."""
    _STEREO = "UAF::Connectivity::OperationalExchangeItem"
    _BASE_METACLASSES = ()
    _ABSTRACT = True
    _DECL = {
    # A collection of OperationalActivities that consume and/or produce the OperationalExchangeItem in
    # ternally.
    'activity': _Ref('activity', 'OperationalActivity', multi=True, lo=0, hi='*', derived=True),
    }

class ServiceExchangeItem(Resource):
    """An abstract grouping for elements that defines the types of elements that can be exchanged between Services and conveyed by a ServiceExchange."""
    _STEREO = "UAF::Connectivity::ServiceExchangeItem"
    _BASE_METACLASSES = ()
    _ABSTRACT = True

class StrategicExchangeItem(Resource, U.Element):
    """An abstract grouping for elements that defines the types of elements that can be exchanged between ActualStrategicPhases and conveyed by a StrategicExchange."""
    _STEREO = "UAF::Connectivity::StrategicExchangeItem"
    _BASE_METACLASSES = ("Element",)
    _ABSTRACT = True

class ResourcePerformer(ResourceAsset, VersionedElement, SubjectOfForecast, U.Class, ResourceExchangeItem, OperationalExchangeItem, ServiceExchangeItem, StrategicExchangeItem, SubjectOfResourceConstraint, CapableElement, Desirer):
    """An abstract grouping of elements that can perform Functions."""
    _STEREO = "UAF::Taxonomy::ResourcePerformer"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = True
    _DECL = {
    # Indicates if the ResourcePerformer is StandardConfiguration, default=false.
    'isStandardConfiguration': _Ref('isStandardConfiguration', bool),
    # Relates ResourcePerformer to ProjectMilestones that affect it.
    'milestone': _Ref('milestone', 'ProjectMilestone', multi=True, lo=0, hi='*'),
    }
    CONSTRAINTS = (
        ("ResourcePerformer.ownedOperation",
         "Values for the ownedOperation metaproperty must be stereotyped «ResourceMethod» or its s"
         "pecializations."
        ),
        ("ResourcePerformer.ownedPort",
         "Values for the ownedPort metaproperty must be stereotyped «ResourcePort» or its speciali"
         "zations."
        ),
        ("ResourcePerformer.isCapableOfPerforming",
         "Is capable of performing only «Function» elements or its specializations."
        ),
    )

class ResourceArchitecture(ResourcePerformer, Architecture, U.Class):
    """An element used to denote a model of the Architecture, described from the ResourcePerformer perspective."""
    _STEREO = "UAF::Taxonomy::ResourceArchitecture"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class CapabilityConfiguration(ResourceArchitecture, U.Class):
    """A composite structure representing the physical and human resources (and their interactions) in an enterprise, assembled to meet a capability."""
    _STEREO = "UAF::Taxonomy::CapabilityConfiguration"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False
    _DECL = {
    # Represents the doctrinal line of development of the Capability.
    'doctrine': _Ref('doctrine', 'StandardOperationalActivity', multi=True, lo=0, hi='*'),
    }

class CapabilityRole(U.Property, MeasurableElement, Desirer):
    """Property of a Capability typed by another Capability, enabling whole-part relationships and structures."""
    _STEREO = "UAF::Structure::CapabilityRole"
    _BASE_METACLASSES = ("Property",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("CapabilityRole.class",
         "Value for class metaproperty must be stereotyped «Capability» or its specializations."
        ),
        ("CapabilityRole.type",
         "Value for type metaproperty must be stereotyped «Capability» or its specializations."
        ),
    )

class MotivationalElement(sysml.Block, U.Class, PropertySet):
    """An abstract kind of element in the model that provides the reason or reasons one has for acting or behaving in a particular way"""
    _STEREO = "UAF::Motivation::MotivationalElement"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = True
    _DECL = {
    # Numerical identifier for tracking and sorting Motivational Elements.
    'ID': _Ref('ID', str),
    # Description of a Motivational Element.
    'Text': _Ref('Text', str),
    }

class Challenge(MotivationalElement, U.Class):
    """An existing or potential difficulty, circumstance, or obstacle which will require effort and determination from an enterprise to overcome in achieving its goals."""
    _STEREO = "UAF::Motivation::Challenge"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False
    _DECL = {
    # Selection of the enumerated kind for this element.
    'kind': _Ref('kind', ChallengeKind),
    }

class Exchange(sysml.ItemFlow, U.InformationFlow, MeasurableElement, SubjectOfSecurityConstraint):
    """Abstract grouping for OperationalExchanges and ResourceExchanges that exchange Resources."""
    _STEREO = "UAF::Connectivity::Exchange"
    _BASE_METACLASSES = ("InformationFlow",)
    _ABSTRACT = True

class ResourceExchange(Exchange, U.InformationFlow):
    """Asserts that a flow can exist between ResourcePerformers (i.e. flows of data, people, materiel, or energy)."""
    _STEREO = "UAF::Connectivity::ResourceExchange"
    _BASE_METACLASSES = ("InformationFlow",)
    _ABSTRACT = False
    _DECL = {
    # Captures the kind of ResourceExchange.
    'exchangeKind': _Ref('exchangeKind', ResourceExchangeKind, derived=True),
    }
    CONSTRAINTS = (
        ("ResourceExchange.conveyed",
         "In case of ResourceExchange.exchangeKind: = ResourceCommunication, the conveyed element "
         "must be stereotyped «DataElement» or its specializations, = ResourceMovement, the convey"
         "ed element must be stereotyped by the specialization of «PhysicalResource», = ResourceEn"
         "ergyFlow, the conveyed element must be stereotyped «NaturalResource» or its specializati"
         "ons, = GeoPoliticalExtentExchange, the conveyed element must be stereotyped «GeoPolitica"
         "lExtentType» or its specializations."
        ),
        ("ResourceInteraction.realizingActivityEdge",
         "Value for the realizingActivityEdge metaproperty must be stereotyped by the specializati"
         "on of «FunctionEdge»."
        ),
        ("ResourceInteraction.realizingConnector",
         "Value for the realizingConnector metaproperty must be stereotyped «ResourceConnector» or"
         " its specializations."
        ),
        ("ResourceInteraction.informationSource",
         "Value for the informationSource metaproperty must be stereotyped by the specialization o"
         "f «ResourcePerformer»."
        ),
        ("ResourceInteraction.informationTarget",
         "Value for the informationTarget metaproperty must be stereotyped by the specialization o"
         "f «ResourcePerformer»."
        ),
        ("ResourceInteraction.realizingMessage",
         "Value for the realizingMessage metaproperty must be stereotyped «ResourceMessage» or its"
         " specializations."
        ),
    )

class Command(ResourceExchange, U.InformationFlow):
    """A type of ResourceExchange that asserts that one OrganizationalResource commands another."""
    _STEREO = "UAF::Connectivity::Command"
    _BASE_METACLASSES = ("InformationFlow",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("Command.informationSource",
         "Value for the informationSource metaproperty must be stereotyped by the specialization o"
         "f «OrganizationalResource»."
        ),
        ("Command.informationTarget",
         "Value for the informationTarget metaproperty must be stereotyped by the specialization o"
         "f «OrganizationalResource»."
        ),
        ("Command.conveyed",
         "Value for the conveyed metaproperty must be stereotyped «ResourceInformation» or its spe"
         "cializations."
        ),
    )

class ComparesTo(sysml.Trace, U.Abstraction, MeasurableElement):
    """An abstraction relationship relating the effect that is achieved with the originally expected DesiredEffect. Providing a means of comparison, between the expectation of the desirer and the actual result."""
    _STEREO = "UAF::Traceability::ComparesTo"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ComparesTo.client",
         "Value for the client metaproperty must be stereotyped by any of specializations of «Actu"
         "alState»."
        ),
        ("ComparesTo.supplier",
         "Value for the supplier metaproperty must be stereotyped by any of specializations of «Ac"
         "tualState»."
        ),
    )

class Competence(SubjectOfForecast, sysml.Block, U.Class, PropertySet):
    """A specific set of abilities defined by knowledge, skills and aptitude."""
    _STEREO = "UAF::Constraints::Competence"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class CompetenceForRole(sysml.Allocate, U.Abstraction, MeasurableElement):
    """An abstraction relationship used to associate an organizational role with a specific set of required competencies."""
    _STEREO = "UAF::Constraints::CompetenceForRole"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("CompetenceForRole.client",
         "Value for the client metaproperty must be stereotyped «ResourceRole» or its specializati"
         "ons."
        ),
        ("CompetenceForRole.supplier",
         "Value for the supplier metaproperty must be stereotyped «Competence» or its specializati"
         "ons."
        ),
    )

class CompetenceToConduct(sysml.Allocate, U.Abstraction, MeasurableElement):
    """An abstraction relationship used to associate a Function with a specific set of Competencies needed to conduct the Function."""
    _STEREO = "UAF::Processes::CompetenceToConduct"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("CompetenceToConduct.client",
         "Value for the client metaproperty must be stereotyped «Function» or its specializations."
        ),
        ("CompetenceToConduct.supplier",
         "Value for the supplier metaproperty must be stereotyped «Competence» or its specializati"
         "ons."
        ),
    )

class ConceptRole(U.Property, MeasurableElement):
    """Usage of a ConceptItem in the context of a HighLevelOperationalConcept."""
    _STEREO = "UAF::Taxonomy::ConceptRole"
    _BASE_METACLASSES = ("Property",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ConceptRole.type",
         "Value for the type metaproperty must be stereotyped by a specialization of «ConceptItem»"
         "."
        ),
        ("ConceptRole.class",
         "Value for the class metaproperty must be stereotyped «HighLevelOperationalConcept» or it"
         "s specializations."
        ),
    )

class Concern(sysml.Block, U.Class, PropertySet, PhaseableElement):
    """A matter of relevance or importance to a stakeholder regarding an entity of interest."""
    _STEREO = "UAF::Summary and Overview::Concern"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class Condition(sysml.ValueType, U.DataType, PropertySet):
    """A type that defines the Location, Environment and/or GeoPoliticalExtent."""
    _STEREO = "UAF::Parameters::Condition"
    _BASE_METACLASSES = ("DataType",)
    _ABSTRACT = False

class Control(ResourceExchange, U.InformationFlow):
    """A type of ResourceExchange that asserts that one PhysicalResource controls another PhysicalResource (i.e. the driver of a vehicle controlling the vehicle speed or direction)."""
    _STEREO = "UAF::Connectivity::Control"
    _BASE_METACLASSES = ("InformationFlow",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("Control.conveyed",
         "Value for the conveyed metaproperty must be stereotyped «ResourceInformation» or its spe"
         "cializations."
        ),
        ("Control.informationTarget",
         "Value for the informationTarget metaproperty must be stereotyped by the specialization o"
         "f «PhysicalResource» or its specializations."
        ),
        ("Control.informationSource",
         "Value for the informationSource metaproperty must be stereotyped by the specialization o"
         "f «PhysicalResource»."
        ),
    )

class Creates(U.Dependency, MeasurableElement):
    """A dependency relationship denoting that an ActualStrategicPhase brings into existence a StrategicAsset."""
    _STEREO = "UAF::Processes::Creates"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("Creates.client",
         "Value for the client metaproperty must be stereotyped «ActualOutcome» or its specializat"
         "ions, or any of specializations of «ActualStrategicPhase»."
        ),
        ("Creates.supplier",
         "Value for the supplier metaproperty must be stereotyped by any of specializations of «St"
         "rategicAsset»."
        ),
    )

class Definition(MeasurableElement, U.Comment):
    """A comment containing a description of an element in the architecture."""
    _STEREO = "UAF::Information::Definition"
    _BASE_METACLASSES = ("Comment",)
    _ABSTRACT = False
    _DECL = {
    # The original or current person (architect) responsible for the Definition.
    'author': _Ref('author', str, multi=True, lo=0, hi='*'),
    }
    CONSTRAINTS = (
        ("Definition.annotatedElement",
         "Value for the annotatedElement metaproperty must be stereotyped by the specialization of"
         " «UAFElement»."
        ),
    )

class Desires(U.Dependency, MeasurableElement):
    """A dependency relationship relating the Desirer (a Capability or OrganizationalResource) to an ActualState."""
    _STEREO = "UAF::States::Desires"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("Desires.client",
         "Value for the client metaproperty must be stereotyped a specialization of «Desirer»."
        ),
        ("Desires.supplier",
         "Value for the supplier metaproperty must be stereotyped a specialization of «ActualState"
         "»."
        ),
    )

class Driver(MotivationalElement, U.Class):
    """A factor which will have a significant impact on the activities, and goals of an enterprise"""
    _STEREO = "UAF::Motivation::Driver"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False
    _DECL = {
    # Selection of the enumerated kind for this element.
    'kind': _Ref('kind', DriverKind),
    }

class Effect(MotivationalElement, U.Class):
    """A kind of phenomenon that follows and is caused by some previous phenomenon that could lead to downstream effects or to one or more desired outcomes"""
    _STEREO = "UAF::States::Effect"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class Enables(U.Dependency, MeasurableElement):
    """A dependency relationship denoting that an Opportunity provides the means for achieving an EnterpriseGoal or Objective."""
    _STEREO = "UAF::Motivation::Enables"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("Enables.client",
         "Value for the client metaproperty must be stereotyped «Opportunity»."
        ),
        ("Enables.supplier",
         "Value for the supplier metaproperty must be stereotyped «EnterpriseGoal» or its speciali"
         "zations."
        ),
    )

class SecurityControl(sysml.Requirement, U.Class, MeasurableElement):
    """The management, operational, and technical control (i.e., safeguard or countermeasure) prescribed for an information system to protect the confidentiality, integrity, and availability of the system and its information [NIST SP 800-53]."""
    _STEREO = "UAF::Motivation::SecurityControl"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False
    _DECL = {
    # Relates an actual mitigation (an ActualResource for mitigating a Risk) to a SecurityControl.
    'mitigatingActualResource': _Ref('mitigatingActualResource', 'ActualResource', multi=True, lo=0, hi='*'),
    }

class EnhancedSecurityControl(SecurityControl, U.Class):
    """Statement of security capability to: (i) build in additional but related, functionality to a basic control; and/or (ii)increase the strength of a basic control."""
    _STEREO = "UAF::Motivation::EnhancedSecurityControl"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class Enhances(sysml.DeriveReqt, U.Abstraction, MeasurableElement):
    """A dependency relationship relating the EnhancedSecurityControl to a SecurityControl."""
    _STEREO = "UAF::Motivation::Enhances"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("Enhances.client",
         "Value for the client metaproperty must be stereotyped «EnhancedSecurityControl» or its s"
         "pecializations."
        ),
        ("Enhances.supplier",
         "Value for the supplier metaproperty must be stereotyped «SecurityControl» or its special"
         "izations."
        ),
    )

class EnterpriseGoal(sysml.Requirement, U.Class, PropertySet, PhaseableElement, AffectableElement):
    """A statement about a state or condition of the enterprise to be brought about or sustained through appropriate Means. An EnterpriseGoal amplifies an EnterpriseVision that is, it indicates what must be satisfied on a continuing basis to effectively attain the EnterpriseVision. http://www.omg.org/spec/BMM/1.3/"""
    _STEREO = "UAF::Taxonomy::EnterpriseGoal"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False
    _DECL = {
    # An advantage or profit gained from achieving the EnterpriseGoal.
    'benefit': _Ref('benefit', 'ValueItem', multi=True, lo=0, hi='*'),
    }

class EnterpriseMission(ActualEnterprisePhase, U.InstanceSpecification):
    """Mission captures at a high level what you will do to realize your vision"""
    _STEREO = "UAF::Processes::EnterpriseMission"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False

class EnterpriseObjective(EnterpriseGoal, U.Class):
    """A statement of an attainable, time-targeted, and measurable target that the enterprise seeks to meet in order to achieve its Goals. http://www.omg.org/spec/BMM/1.3/"""
    _STEREO = "UAF::Taxonomy::EnterpriseObjective"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class EnterpriseVision(sysml.Block, U.Class, PropertySet, PhaseableElement):
    """A Vision describes the future state of the enterprise, without regard to how it is to be achieved. http://www.omg.org/spec/BMM/1.3/"""
    _STEREO = "UAF::Taxonomy::EnterpriseVision"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False
    _DECL = {
    # A description of the Vision.
    'statement': _Ref('statement', 'VisionStatement', multi=True, lo=0, hi='*', derived=True),
    }

class Environment(Condition, U.DataType):
    """A definition of the environmental factors in which something exists or functions. The definition of an Environment element can be further defined using EnvironmentKind."""
    _STEREO = "UAF::Parameters::Environment"
    _BASE_METACLASSES = ("DataType",)
    _ABSTRACT = False
    _DECL = {
    # Captures the kind of Environment.
    'kind': _Ref('kind', EnvironmentKind),
    }

class EnvironmentProperty(U.Property, MeasurableElement):
    """A property of an Environment that is typed by a Condition. The kinds of Condition that can be represented are Location, GeoPoliticalExtentType and Environment."""
    _STEREO = "UAF::Parameters::EnvironmentProperty"
    _BASE_METACLASSES = ("Property",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("EnvironmentalProperty.class",
         "Value for the class metaproperty must be stereotyped «Environment» or its specialization"
         "s."
        ),
        ("EnvironmentalProperty.type",
         "Value for the type property must be stereotyped «Condition» or its specializations."
        ),
    )

class EvokedBy(U.Dependency, MeasurableElement):
    """A dependency relationship denoting that a Risk is drawn out by an Opportunity."""
    _STEREO = "UAF::Traceability::EvokedBy"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("EvokedBy.client",
         "Value for the client metaproperty must be stereotyped «Risk» or its specializations."
        ),
        ("EvokedBy.supplier",
         "Value for the supplier metaproperty must be stereotyped «Opportunity» or its specializat"
         "ions."
        ),
    )

class Exhibits(sysml.Allocate, U.Abstraction, MeasurableElement):
    """An abstraction relationship that exists between a CapableElement and a Capability that it meets under specific environmental conditions."""
    _STEREO = "UAF::Traceability::Exhibits"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    _DECL = {
    # Defines the environmental conditions constraining the way that a Capability is exhibited.
    'environmentalConditions': _Ref('environmentalConditions', 'Environment', multi=True, lo=0, hi='*'),
    }
    CONSTRAINTS = (
        ("Exhibits.client",
         "Value for the client metaproperty must be stereotyped a specialization of «CapableElemen"
         "t»."
        ),
        ("Exhibits.supplier",
         "Value for the supplier metaproperty must be stereotyped «Capability»."
        ),
    )

class FieldedCapability(ActualResource, U.InstanceSpecification):
    """An actual, fully-realized capability. A FieldedCapability is typed by a CapabilityConfiguration."""
    _STEREO = "UAF::Taxonomy::FieldedCapability"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("FieldedCapability.classifier",
         "Value for the classifier metaproperty must be stereotyped «CapabilityConfiguration» or i"
         "ts specializations."
        ),
    )

class FillsPost(sysml.Allocate, U.Abstraction, MeasurableElement):
    """A dependency relationship that asserts that an ActualPerson fills an ActualPost."""
    _STEREO = "UAF::Connectivity::FillsPost"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    _DECL = {
    # End date of an ActualPerson filling an ActualPost.
    'endDate': _Ref('endDate', 'ISO8601DateTime'),
    # Start date of an ActualPerson filling an ActualPost.
    'startDate': _Ref('startDate', 'ISO8601DateTime'),
    }
    CONSTRAINTS = (
        ("FillsPost.client",
         "Value for the client metaproperty must be stereotyped by «ActualPerson» or its specializ"
         "ations."
        ),
        ("FillsPost.supplier",
         "Value for the supplier metaproperty must be stereotyped by «ActualPost» or its specializ"
         "ations."
        ),
    )

class Forecast(U.Dependency, MeasurableElement):
    """A dependency relationship that specifies a transition from one Resource Performer, Standard, Competence to another future one. It is related to an ActualStrategicPhase to give it a temporal context."""
    _STEREO = "UAF::Roadmap::Forecast"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    _DECL = {
    # Relates the SubjectOfForecast to the ActualStrategicPhase in which the SubjectOfForecast is expe
    # cted to be provided.
    'forecastPeriod': _Ref('forecastPeriod', 'ActualStrategicPhase'),
    }
    CONSTRAINTS = (
        ("Forecast.supplier",
         "Value for the supplier property must be stereotyped by the specialization of «SubjectOfF"
         "orecast»."
        ),
        ("Forecast.client",
         "Value for the client metaproperty must be stereotyped by the specialization of «SubjectO"
         "fForecast»."
        ),
        ("Forecast.pair",
         "Values for the client and supplier metaproperties must be stereotyped by the same specia"
         "lization of «SubjectOfForecast» (e.g. «Software» to «Software», «Standard» to «Standard»"
         ", etc)."
        ),
    )

class Function(Activity, U.Activity, SubjectOfResourceConstraint):
    """An Activity which is specified in the context to the ResourcePerformer (human or machine) that IsCapableToPerform it."""
    _STEREO = "UAF::Processes::Function"
    _BASE_METACLASSES = ("Activity",)
    _ABSTRACT = False
    _DECL = {
    # ResourceExchangeItems consumed and produced internally within a Function.
    'affectedResource': _Ref('affectedResource', 'ResourceExchangeItem', multi=True, lo=0, hi='*', derived=True),
    }
    CONSTRAINTS = (
        ("Function.ownedParameter",
         "The values for the ownedParameter metaproperty must be stereotyped «ResourceParameter» o"
         "r its specializations."
        ),
    )

class FunctionAction(U.CallBehaviorAction, MeasurableElement):
    """A call of a Function indicating that the Function is performed by a ResourceRole in a specific context."""
    _STEREO = "UAF::Processes::FunctionAction"
    _BASE_METACLASSES = ("CallBehaviorAction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("FunctionAction.activity",
         "Value for the activity metaproperty must be stereotyped «Function» or its specialization"
         "s."
        ),
        ("FunctionAction.behavior",
         "Value for the behavior metaproperty must be stereotyped «Function» or its specialization"
         "s."
        ),
    )

class FunctionEdge(U.ActivityEdge, MeasurableElement):
    """Abstract grouping for FunctionControlFlow and FunctionObjectFlow."""
    _STEREO = "UAF::Processes::FunctionEdge"
    _BASE_METACLASSES = ("ActivityEdge",)
    _ABSTRACT = True
    CONSTRAINTS = (
        ("FunctionEdge.owner",
         "«FunctionEdge» must be owned directly or indirectly by «Function» or its specializations"
         "."
        ),
    )

class FunctionControlFlow(U.ControlFlow, FunctionEdge):
    """An ActivityEdge that shows the flow of control between FunctionActions."""
    _STEREO = "UAF::Processes::FunctionControlFlow"
    _BASE_METACLASSES = ("ControlFlow",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("FunctionControlFlow.source",
         "Value for the source metaproperty must be stereotyped «FunctionAction» or its specializa"
         "tions."
        ),
        ("FunctionControlFlow.target",
         "Value for the target metaproperty must be stereotyped «FunctionAction» or its specializa"
         "tions."
        ),
    )

class FunctionObjectFlow(U.ObjectFlow, FunctionEdge):
    """An ActivityEdge that shows the flow of Resources (objects/data) between FunctionActions."""
    _STEREO = "UAF::Processes::FunctionObjectFlow"
    _BASE_METACLASSES = ("ObjectFlow",)
    _ABSTRACT = False

class GeoPoliticalExtentType(Condition, U.DataType, ResourceExchangeItem, OperationalExchangeItem, StrategicExchangeItem):
    """A type of geospatial extent whose boundaries are defined by declaration or agreement by political parties."""
    _STEREO = "UAF::Parameters::GeoPoliticalExtentType"
    _BASE_METACLASSES = ("DataType",)
    _ABSTRACT = False
    _DECL = {
    # Captures the kind of GeopoliticalExtentType if the GeoPoliticalExtentTypeKind has been set to "O
    # therType".
    'customKind': _Ref('customKind', str),
    # Captures the kind of GeopoliticalExtentType.
    'kind': _Ref('kind', GeoPoliticalExtentTypeKind),
    }

class GovernedBy(sysml.Allocate, U.Abstraction, MeasurableElement):
    """An abstraction relationship that exists between the ServiceContract and the Service that it governs."""
    _STEREO = "UAF::Traceability::GovernedBy"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("GovernedBy.client",
         "Value for the client metaproperty must be stereotyped «Service» or its specializations."
        ),
        ("GovernedBy.supplier",
         "Value for the supplier metaproperty must be stereotyped «ServiceContract» or its special"
         "izations."
        ),
    )

class HighLevelOperationalConcept(sysml.Block, U.Class, PropertySet):
    """Describes the Resources and Locations required to meet an operational scenario from an integrated systems point of view. It is used to communicate overall quantitative and qualitative system characteristics to stakeholders."""
    _STEREO = "UAF::Taxonomy::HighLevelOperationalConcept"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class ISO8601DateTime(U.LiteralString, UAFElement):
    """A date and time specified in the ISO8601 date-time format including timezone designator (TZD): YYYY-MM-DDThh:mm:ssTZD."""
    _STEREO = "UAF::Taxonomy::ISO8601DateTime"
    _BASE_METACLASSES = ("LiteralString",)
    _ABSTRACT = False

class ImpactedBy(U.Abstraction, MeasurableElement):
    """A dependency relationship denoting that a Capability is affected by an Opportunity."""
    _STEREO = "UAF::Motivation::ImpactedBy"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ImpactedBy.supplier",
         "In case of value for ImpactedBy.client is stereotyped: a. by any of specializations of «"
         "Architecture», values for the supplier metaproperty must be stereotyped «Challenge» or i"
         "ts specializations, b. by any of specializations of «ActualStrategicPhase», values for t"
         "he supplier metaproperty must be stereotyped «Challenge» or its specializations, c. «Ope"
         "rationalActivity» or its specializations, values for the supplier metaproperty must be s"
         "tereotyped «Challenge» or its specializations, d. «Capability» or its specializations, v"
         "alues for the supplier metaproperty must be stereotyped «Opportunity» or its specializat"
         "ions, e. «ActualOutcome» or its specializations, values for the supplier metaproperty mu"
         "st be stereotyped «EnterpriseGoal» or its specializations."
        ),
        ("ImpactedBy.client",
         "In case of value for ImpactedBy.supplier is stereotyped: a. «Challenge» or its specializ"
         "ations, values for the client metaproperty must be stereotyped by any of specializations"
         " of «Architecture» or «ActualStrategicPhase», or «OperationalActivity» or its specializa"
         "tions, b. «Opportunity» or its specializations, values for the client metaproperty must "
         "be stereotyped «Capability» or its specializations, c. «EnterpriseGoal» or its specializ"
         "ations, values for the client metaproperty must be stereotyped «ActualOutcome» or its sp"
         "ecializations."
        ),
    )

class Implements(sysml.Allocate, U.Abstraction, MeasurableElement):
    """An abstraction relationship that defines how an element in the upper layer of abstraction is implemented by a semantically equivalent element (for example tracing the Functions to the OperationalActivities) in the lower level of abstraction."""
    _STEREO = "UAF::Traceability::Implements"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("Implements.client",
         "In case of value for Implements.supplier is stereotyped: a. by any of specializations of"
         " «OperationalAgent», values for the client metaproperty must be stereotyped by any of sp"
         "ecializations of «ResourcePerformer», b. «OperationalActivity» or its specializations, v"
         "alues for the client metaproperty must be stereotyped «Function» or its specializations,"
         " c. «ServiceFunction» or its specializations, values for the client metaproperty must be"
         " stereotyped «Function» or its specializations, d. «ServiceInterface» or its specializat"
         "ions, values for the client metaproperty must be stereotyped «ResourceInterface» or its "
         "specializations, e. «OperationalInterface» or its specializations, values for the client"
         " metaproperty must be stereotyped «ResourceInterface» or its specializations, f. «Operat"
         "ionalConnector» or its specializations, values for the client metaproperty must be stere"
         "otyped «ResourceConnector» or its specializations, g. «OperationalExchange» or its speci"
         "alizations, values for the client metaproperty must be stereotyped «ResourceExchange» or"
         " its specializations, g. «OperationalRole» or its specializations, values for the client"
         " metaproperty must be stereotyped «ResourceRole» or its specializations, h. «ResourceCon"
         "nector» or its specializations, values for the client metaproperty must be stereotyped «"
         "ResourceConnector» or its specializations, i. «OperationalInformation» or its specializa"
         "tions, values for the client metaproperty must be stereotyped «ResourceInformation» or i"
         "ts specializations. j. by any of specializations of «ActualStrategicPhase», values for t"
         "he client metaproperty must be stereotyped by any of specializations of «Architecture» o"
         "r «OperationalActivity». k. «Service» or its specializations, values for the supplier me"
         "taproperty must be stereotyped «ResourceService» or its specializations. l. «StrategicIn"
         "formation» or its specializations, values for the client metaproperty must be stereotype"
         "d «OperationalInformation» or its specializations."
        ),
        ("Implements.supplier",
         "In case of value for Implements.client is stereotyped: a. by any of specializations of «"
         "ResourcePerformer», values for the supplier metaproperty must be stereotyped by any of s"
         "pecializations of «OperationalAgent», b. «Function» or its specializations, values for t"
         "he supplier metaproperty must be stereotyped «OperationalActivity», «ServiceFunction» or"
         " their specializations, c. «ResourceInterface» or its specializations, values for the su"
         "pplier metaproperty must be stereotyped «ServiceInterface», «OperationalInterface», or t"
         "heir specializations, d. «ResourceConnector» or its specializations, values for the supp"
         "lier metaproperty must be stereotyped «OperationalConnector», «ResourceConnector» or the"
         "ir specializations, e. «ResourceExchange» or its specializations, values for the supplie"
         "r metaproperty must be stereotyped «OperationalExchange» or its specializations, f. «Res"
         "ourceRole» or its specializations, values for the supplier metaproperty must be stereoty"
         "ped «OperationalRole» or its specializations, g. «OperationalActivity» or its specializa"
         "tions, values for the supplier metaproperty must be stereotyped «ActualStrategicPhase» o"
         "r its specializations, h. «ResourceInformation» or its specializations, values for the s"
         "upplier metaproperty must be stereotyped «OperationalInformation» or its specializations"
         ". i. by any of specializations of «Architecture», values for the supplier metaproperty m"
         "ust be stereotyped by any of specializations of «ActualStrategicPhase». j. «ResourceServ"
         "ice» or its specializations, values for the supplier metaproperty must be stereotyped «S"
         "ervice» or its specializations. k. «OperationalInformation» or its specializations, valu"
         "es for the supplier metaproperty must be stereotyped «StrategicInformation» or its speci"
         "alizations. l. «ServiceInterface» or its specializations, values for the supplier metapr"
         "operty must be stereotyped «OperationalInterface» or its specializations."
        ),
    )

class Information(MeasurableElement, U.Comment):
    """A comment that describes the state of an item of interest in any medium or form -- and is communicated or received."""
    _STEREO = "UAF::Information::Information"
    _BASE_METACLASSES = ("Comment",)
    _ABSTRACT = False
    _DECL = {
    # Captures the kind of information.
    'informationKind': _Ref('informationKind', InformationKind),
    }
    CONSTRAINTS = (
        ("Information.annotatedElement",
         "Value for the annotatedElement metaproperty must be stereotyped by a specialization of «"
         "UAFElement»."
        ),
    )

class SubjectOfOperationalConstraint(UAFElement, U.Element):
    """An abstract grouping of elements that can be the subject of an OperationalConstraint."""
    _STEREO = "UAF::Constraints::SubjectOfOperationalConstraint"
    _BASE_METACLASSES = ("Element",)
    _ABSTRACT = True

class InformationModel(U.Package, SubjectOfOperationalConstraint, SubjectOfResourceConstraint):
    """A structural specification of information types, showing relationships between them. The type of information captured in the InformationModel is described using the enumeration InformationModelKind (Conceptual, Logical, and Physical)."""
    _STEREO = "UAF::Information::InformationModel"
    _BASE_METACLASSES = ("Package",)
    _ABSTRACT = False
    _DECL = {
    # Captures the kind of DataModel being represented, Conceptual, Logical or Physical.
    'kind': _Ref('kind', InformationModelKind),
    }

class IsCapableToPerform(sysml.Allocate, U.Abstraction, MeasurableElement):
    """An Abstraction relationship defining the traceability between the structural elements to the Activities that they can perform."""
    _STEREO = "UAF::Processes::IsCapableToPerform"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("IsCapableOfPerforming.client",
         "In case of value for IsCapableToPerform.supplier is stereotyped: a. «OperationalActivity"
         "» or its specializations, values for the client metaproperty must be stereotyped by any "
         "of specializations of «OperationalAgent», b. «ServiceFunction» or its specializations, v"
         "alues for the client metaproperty must be stereotyped «Service» or its specializations, "
         "c. «Function» or its specializations, except for «ProjectActivity», values for the clien"
         "t metaproperty must be stereotyped by any of specializations of «ResourcePerformer», d. "
         "«ProjectActivity» or its specializations, values for the client metaproperty must be ste"
         "reotyped by any of specializations of «Project»."
        ),
        ("IsCapableOfPerforming.supplier",
         "In case of value for IsCapableToPerform.client is stereotyped: a. by a specialization of"
         " «OperationalAgent», values for the supplier metaproperty must be stereotyped «Operation"
         "alActivity» or its specializations, b. «Service» or its specializations, values for the "
         "supplier metaproperty must be stereotyped «ServiceFunction» or its specializations, c. b"
         "y a specialization of «ResourcePerformer», values for the supplier metaproperty must be "
         "stereotyped «Function» or its specializations, except for «ProjectActivity», d. by a spe"
         "cialization of «Project», values for the supplier metaproperty must be stereotyped «Proj"
         "ectActivity» or its specializations."
        ),
    )

class OperationalAsset(Asset, U.Class):
    """An abstract element used to group the elements of OperationalAgent and OperationalInformation allowing them to own OperationalInformationRoles."""
    _STEREO = "UAF::Taxonomy::OperationalAsset"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = True

class OperationalAgent(OperationalAsset, U.Class, SubjectOfOperationalConstraint, CapableElement, Desirer):
    """An abstract type grouping OperationalArchitecture and OperationalPerformer."""
    _STEREO = "UAF::Structure::OperationalAgent"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = True
    CONSTRAINTS = (
        ("OperationalAgent.ownedPort",
         "Values for the ownedPort metaproperty must be stereotyped «OperationalPort» or its speci"
         "alizations."
        ),
        ("OperationalAgent.ownedOperation",
         "Values for the ownedOperation metaproperty must be stereotyped «OperationalMethod» or it"
         "s specializations."
        ),
        ("OperationalAgent.isCapableOfPerforming",
         "Is capable of performing only «OperationalActivity» elements or its specializations."
        ),
    )

class OperationalPerformer(OperationalAgent, U.Class):
    """A logical agent that IsCapableToPerform OperationalActivities which produce, consume and process Resources."""
    _STEREO = "UAF::Structure::OperationalPerformer"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class KnownResource(OperationalPerformer, ResourcePerformer, U.Class):
    """Asserts that a known ResourcePerformer constrains the implementation of the OperationalPerformer that plays the role in the OperationalArchitecture."""
    _STEREO = "UAF::Structure::KnownResource"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class Location(Condition, U.DataType, ConceptItem):
    """A specification of the generic area in which a LocationHolder is required to be located."""
    _STEREO = "UAF::Parameters::Location"
    _BASE_METACLASSES = ("DataType",)
    _ABSTRACT = False
    _DECL = {
    # Captures the kind of Location if the LocationTypeKind has been set to "OtherType".
    'customKind': _Ref('customKind', str),
    # Captures the kind of Location.
    'kind': _Ref('kind', LocationTypeKind),
    }

class MapsToCapability(sysml.Allocate, U.Abstraction, MeasurableElement):
    """An Abstraction relationship denoting that an Activity contributes to providing a Capability."""
    _STEREO = "UAF::Traceability::MapsToCapability"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("MapsToCapability.client",
         "Value for the client metaproperty must be stereotyped a specialization of «Activity»."
        ),
        ("MapsToCapability.supplier",
         "Value for the supplier metaproperty must be stereotyped «Capability»."
        ),
    )

class MapsToGoal(sysml.Refine, MeasurableElement, U.Element):
    """A dependency relationship denoting that some StrategicInformation contributes to achieving an EnterpriseGoal or Objective."""
    _STEREO = "UAF::Information::MapsToGoal"
    _BASE_METACLASSES = ("Element",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("MapsToGoal.client",
         "Value for the client metaproperty must be stereotyped «StrategicInformation»."
        ),
        ("MapsToGoal.supplier",
         "Value for the supplier metaproperty must be stereotyped «EnterpriseGoal» or its speciali"
         "zations."
        ),
    )

class Measurement(U.Property, MeasurableElement):
    """A property of an element representing something in the physical world, expressed in amounts of a unit of measure."""
    _STEREO = "UAF::Parameters::Measurement"
    _BASE_METACLASSES = ("Property",)
    _ABSTRACT = False
    _DECL = {
    # Relates the Measurement to the Condition (which provides the environementalContext) under which 
    # the Measurement is expected to be taken.
    'environmentalContext': _Ref('environmentalContext', 'ActualCondition'),
    }
    CONSTRAINTS = (
        ("Measurement.class",
         "Value for the class metaproperty must be stereotyped by the specialization of «PropertyS"
         "et»."
        ),
    )

class MeasurementSet(sysml.ValueType, U.DataType, PropertySet):
    """A collection of Measurements."""
    _STEREO = "UAF::Parameters::MeasurementSet"
    _BASE_METACLASSES = ("DataType",)
    _ABSTRACT = False
    _DECL = {
    # Relates the MeasurementSet to the MeasurableElement that it is applicable to.
    'appliesFor': _Ref('appliesFor', 'MeasurableElement', multi=True, lo=0, hi='*'),
    }

class Sequence(U.Dependency, MeasurableElement):
    """A dependency relationship that asserts one Individual's temporal extent is completely before the temporal extent of another."""
    _STEREO = "UAF::Traceability::Sequence"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("Sequence.client",
         "Value for the client metaproperty must be stereotyped by any of specializations of «Actu"
         "alState»."
        ),
        ("Sequence.supplier",
         "Value for the supplier metaproperty must be stereotyped by any of specializations of «Ac"
         "tualState»."
        ),
    )

class MilestoneDependency(Sequence, U.Dependency):
    """A dependency relationship between two ActualProjectMilestones that denotes one ActualProjectMilestone follows from another."""
    _STEREO = "UAF::Connectivity::MilestoneDependency"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("MilestoneDependency.client",
         "Value for the client metaproperty must be stereotyped «ActualProjectMilestone» or its sp"
         "ecializations."
        ),
        ("MilestoneDependency.supplier",
         "Value for the supplier metaproperty must be stereotyped «ActualProjectMilestone» or its "
         "specializations."
        ),
    )

class Mitigates(U.Dependency, MeasurableElement):
    """A dependency relating a Security Control to a Risk. Mitigation is established to manage risk and could be represented as an overall strategy or through techniques (mitigation configurations) and procedures (SecurityProcesses)."""
    _STEREO = "UAF::Parameters::Mitigates"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("Mitigates.client",
         "Value for the client metaproperty must be stereotyped «SecurityControl» or its specializ"
         "ations."
        ),
        ("Mitigates.supplier",
         "Value for the supplier metaproperty must be stereotyped «Risk» or its specializations."
        ),
    )

class MotivatedBy(U.Dependency, MeasurableElement):
    """A dependency relationship denoting the reason or reasons one has for acting or behaving in a particular way"""
    _STEREO = "UAF::Motivation::MotivatedBy"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("MotivatedBy.supplier",
         "In case of value for ImpactedBy.client is stereotyped: a. «Opportunity» or its specializ"
         "ations, values for the supplier metaproperty must be stereotyped «Challenge» or its spec"
         "ializations, b. «EnterpriseGoal» or its specializations, values for the supplier metapro"
         "perty must be stereotyped «Driver» or its specializations."
        ),
        ("MotivatedBy.client",
         "In case of value for ImpactedBy.supplier is stereotyped: a. «Challenge» or its specializ"
         "ations, values for the client metaproperty must be stereotyped «Opportunity» or its spec"
         "ializations, b. «Driver» or its specializations, values for the client metaproperty must"
         " be stereotyped «EnterpriseGoal» or its specializations."
        ),
    )

class PhysicalResource(ResourcePerformer, U.Class):
    """An abstract grouping that defines physical resources (i.e. OrganizationalResource, ResourceArtifact and NaturalResource)."""
    _STEREO = "UAF::Taxonomy::PhysicalResource"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = True

class NaturalResource(PhysicalResource, U.Class):
    """Type of physical resource that occurs in nature such as oil, water, gas or coal."""
    _STEREO = "UAF::Taxonomy::NaturalResource"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class OperationalActivity(Activity, U.Activity, SubjectOfOperationalConstraint):
    """An Activity that captures a logical process, specified independently of how the process is carried out."""
    _STEREO = "UAF::Processes::OperationalActivity"
    _BASE_METACLASSES = ("Activity",)
    _ABSTRACT = False
    _DECL = {
    # A collection of OperationalExchangeItems consumed and produced internally within the Operational
    # Activity.
    'affectedResource': _Ref('affectedResource', 'OperationalExchangeItem', multi=True, lo=0, hi='*', derived=True),
    }
    CONSTRAINTS = (
        ("OperationalActivity.ownedParameter",
         "The values for the ownedParameter metaproperty must be stereotyped «OperationalParameter"
         "» or its specializations."
        ),
    )

class OperationalActivityAction(U.CallBehaviorAction, MeasurableElement):
    """A call of an OperationalActivity in the context of another OperationalActivity."""
    _STEREO = "UAF::Processes::OperationalActivityAction"
    _BASE_METACLASSES = ("CallBehaviorAction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("OperationalActivityAction.behavior",
         "Value for activity metaproperty must be stereotyped «OperationalActivity» or its special"
         "izations."
        ),
        ("OperationalActivityAction.activity",
         "Value for the activity metaproperty must be stereotyped «OperationalActivity» or its spe"
         "cializations."
        ),
    )

class OperationalActivityEdge(U.ActivityEdge, MeasurableElement):
    """Abstract grouping for OperationalControlFlow and OperationalObjectFlow."""
    _STEREO = "UAF::Processes::OperationalActivityEdge"
    _BASE_METACLASSES = ("ActivityEdge",)
    _ABSTRACT = True
    CONSTRAINTS = (
        ("OperationalActivityEdge.owner",
         "«OperationalActivityEdge» must be owned directly or indirectly by «OperationalActivity» "
         "or its specializations."
        ),
    )

class OperationalArchitecture(OperationalAgent, Architecture, U.Class):
    """An element used to denote a model of the Architecture, described from the Operational perspective."""
    _STEREO = "UAF::Structure::OperationalArchitecture"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class OperationalConnector(U.Connector, AssetRole):
    """A Connector that goes between OperationalRoles representing a need to exchange Resources. It can carry a number of OperationalExchanges."""
    _STEREO = "UAF::Connectivity::OperationalConnector"
    _BASE_METACLASSES = ("Connector",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("OperationalConnector.end",
         "The value for the role metaproperty for the owned ConnectorEnd must be stereotype «Opera"
         "tionalRole»/«OperationalPort» or its specializations."
        ),
    )

class Rule(U.Constraint, MeasurableElement):
    """An abstract grouping for all types of constraint (i.e. an OperationalConstraint could detail the rules of accountancy best practice)."""
    _STEREO = "UAF::Constraints::Rule"
    _BASE_METACLASSES = ("Constraint",)
    _ABSTRACT = True
    _DECL = {
    # Captures the kind of Rule that is being described.
    'ruleKind': _Ref('ruleKind', RuleKind),
    }

class OperationalConstraint(Rule, U.Constraint):
    """A Rule governing an operational architecture element i.e. OperationalPerformer, OperationalActivity, OperationalInformation etc."""
    _STEREO = "UAF::Constraints::OperationalConstraint"
    _BASE_METACLASSES = ("Constraint",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("OperationalConstraint.constrainedElement",
         "Value for the constrainedElement metaproperty must be stereotyped by any specialization "
         "of «SubjectOfOperationalConstraint»."
        ),
    )

class OperationalControlFlow(U.ControlFlow, OperationalActivityEdge):
    """An ActivityEdge that shows the flow of control between OperationalActivityActions."""
    _STEREO = "UAF::Processes::OperationalControlFlow"
    _BASE_METACLASSES = ("ControlFlow",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("OperationalControlFlow.target",
         "Value for the target metaproperty must be stereotyped «OperationalActivityAction» or its"
         " specializations."
        ),
        ("OperationalControlFlow.source",
         "Value for the source metaproperty must be stereotyped «OperationalActivityAction» or its"
         " specializations."
        ),
    )

class OperationalExchange(Exchange, U.InformationFlow, SubjectOfOperationalConstraint):
    """Asserts that a flow can exist between OperationalPerformers (i.e. flows of information, people, materiel, or energy)."""
    _STEREO = "UAF::Connectivity::OperationalExchange"
    _BASE_METACLASSES = ("InformationFlow",)
    _ABSTRACT = False
    _DECL = {
    # Captures the kind of Resource being exchanged.
    'exchangeKind': _Ref('exchangeKind', OperationalExchangeKind, derived=True),
    # Captures the directional arbitrary level of trust related to an OperationalExchange between two 
    # OperationalPerformers.
    'trustLevel': _Ref('trustLevel', float),
    }
    CONSTRAINTS = (
        ("OperationalExchange.realizingConnector",
         "Value for realizingConnector metaproperty has to be stereotyped «OperationalConnector» o"
         "r its specializations."
        ),
        ("OperationalExchange.realizingActivityEdge",
         "Value for realizingActivityEdge metaproperty has to be stereotyped by any specialization"
         " of «OperationalActivityEdge»."
        ),
        ("OperationalExchange.informationSource",
         "Value for informationSource metaproperty has to be stereotyped «OperationalPerformer» or"
         " its specializations."
        ),
        ("OperationalExchange.informationTarget",
         "Value for informationTarget metaproperty has to be stereotyped «OperationalPerformer» or"
         " its specializations."
        ),
        ("OperationalExchange.realizingMessage",
         "Value for realizingMessage metaproperty has to be stereotyped «OperationalMessage» or it"
         "s specializations."
        ),
        ("OperationalExchange.conveyed",
         "In case of OperationalExchange.operationalExchangeKind: = InformationExchange, the conve"
         "yed element must be stereotyped «OperationalInformation» or its specializations, = Mater"
         "ielExchange, the conveyed element must be stereotyped «ResourceArtifact» or its speciali"
         "zations, = EnergyExchange, the conveyed element must be stereotyped «NaturalResource» or"
         " its specializations, = OrganizationalExchange, the conveyed element must be stereotyped"
         " «OrganizationalResource» or its specializations, = ConfigurationExchange, the conveyed "
         "element must be stereotyped «CapabilityConfiguration» or its specializations, or = GeoPo"
         "liticalExtentExchange, the conveyed element must be stereotyped «GeoPoliticalExtentType»"
         " or its specializations."
        ),
    )

class OperationalInformation(OperationalAsset, U.Class, OperationalExchangeItem, ServiceExchangeItem, SubjectOfOperationalConstraint):
    """An item of information that flows between OperationalPerformers and is produced and consumed by the OperationalActivities that the OperationalPerformers are capable to perform (see IsCapableToPerform)."""
    _STEREO = "UAF::Information::OperationalInformation"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("InformationElement.owner",
         "Values for the owner metaproperty must be stereotyped «DataModel» or its specializations"
         "."
        ),
    )

class OperationalInformationRole(U.Property, AssetRole):
    """A usage of OperationalInformation that exists in the context of an OperationalAsset. It also allows the representation of the whole-part aggregation of OperationalInformation elements."""
    _STEREO = "UAF::Structure::OperationalInformationRole"
    _BASE_METACLASSES = ("Property",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("OperationalInformationRole.type",
         "Value for the type metaproperty must be stereotyped «OperationalInformation» or its spec"
         "ializations."
        ),
        ("OperationalInformationRole.class",
         "Value for the class metaproperty must be stereotyped by the specialization of «Operation"
         "alAsset»."
        ),
    )

class OperationalInterface(sysml.InterfaceBlock, U.Class, PropertySet):
    """A declaration that specifies a contract between the OperationalPerformer it is related to, and any other OperationalPerformers it can interact with."""
    _STEREO = "UAF::Connectivity::OperationalInterface"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("OperationalInterface.ownedOperation",
         "Values for the ownedOperation metaproperty must be stereotyped «OperationalMethod» or it"
         "s specializations."
        ),
    )

class OperationalMessage(U.Message, MeasurableElement):
    """Message for use in an operational interaction scenario which carries any of the subtypes of OperationalExchange."""
    _STEREO = "UAF::Sequences::OperationalMessage"
    _BASE_METACLASSES = ("Message",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("OperationalMessage.receiveEvent.event.operation",
         "Values for the receiveEvent.event.operation metaproperty must be stereotyped with «Opera"
         "tionalMethod» or its specializations."
        ),
    )

class OperationalMethod(U.Operation, MeasurableElement):
    """A behavioral feature of an OperationalAgent whose behavior is specified in an OperationalActivity."""
    _STEREO = "UAF::Structure::OperationalMethod"
    _BASE_METACLASSES = ("Operation",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("OperationalMethod.ownedParameter",
         "The values for the ownedParameter metaproperty must be stereotyped «OperationalParameter"
         "» or its specializations."
        ),
        ("OperationalMethod.method",
         "Value for the method metaproperty must be stereotyped «OperationalActivity» or its speci"
         "alizations."
        ),
    )

class OperationalMitigation(OperationalArchitecture, U.Class):
    """A set of OperationalPerformers intended to address against specific operational risks."""
    _STEREO = "UAF::Taxonomy::OperationalMitigation"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class OperationalObjectFlow(U.ObjectFlow, OperationalActivityEdge):
    """An ActivityEdge that shows the flow of Resources (objects/information) between OperationalActivityActions."""
    _STEREO = "UAF::Processes::OperationalObjectFlow"
    _BASE_METACLASSES = ("ObjectFlow",)
    _ABSTRACT = False

class OperationalParameter(U.Parameter, MeasurableElement):
    """An element that represents inputs and outputs of an OperationalActivity. It is typed by an OperationalExchangeItem."""
    _STEREO = "UAF::Structure::OperationalParameter"
    _BASE_METACLASSES = ("Parameter",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("OperationalParameter.type",
         "Value for the type metaproperty must be stereotyped by specialization of «OperationalExc"
         "hangeItem»."
        ),
    )

class OperationalPort(sysml.ProxyPort, U.Port, MeasurableElement):
    """An interaction point for an OperationalAgent through which it can interact with the outside environment and which is defined by an OperationalInterface."""
    _STEREO = "UAF::Structure::OperationalPort"
    _BASE_METACLASSES = ("Port",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("OperationalPort.class",
         "Value for class metaproperty must be stereotyped «OperationalAgent» or its specializatio"
         "ns."
        ),
        ("OperationalPort.type",
         "Value for type metaproperty must be stereotyped «OperationalInterface» or its specializa"
         "tions."
        ),
    )

class OperationalRole(U.Property, AssetRole, MeasurableElement, LocationHolder):
    """Usage of a OperationalPerformer or OperationalArchitecture in the context of another OperationalPerformer or OperationalArchitecture. Creates a whole-part relationship."""
    _STEREO = "UAF::Structure::OperationalRole"
    _BASE_METACLASSES = ("Property",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("OperationalRole.type",
         "Value for type metaproperty must be stereotyped by a specialization of «OperationalAgent"
         "»."
        ),
        ("OperationalRole.class",
         "Value for class metaproperty must be stereotyped by a specialization of «OperationalAgen"
         "t»."
        ),
    )

class OperationalSignal(U.Signal, OperationalExchangeItem, SubjectOfOperationalConstraint):
    """An OperationalSignal is a specification of a kind of communication between operational performers in which a reaction is asynchronously triggered in the receiver without a reply."""
    _STEREO = "UAF::Connectivity::OperationalSignal"
    _BASE_METACLASSES = ("Signal",)
    _ABSTRACT = False

class OperationalSignalProperty(U.Property, MeasurableElement):
    """A property of an OperationalSignal typed by OperationalExchangeItem. It enables OperationalExchangeItem e.g. OperationalInformation to be passed as arguments of the OperationalSignal."""
    _STEREO = "UAF::Connectivity::OperationalSignalProperty"
    _BASE_METACLASSES = ("Property",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("OperationalSignalProperty.class",
         "Value for class metaproperty must be stereotyped «OperationalSignal» or its specializati"
         "ons."
        ),
        ("OperationalSignalProperty.type",
         "Value for type metaproperty must be stereotyped by a specialization of «OperationalExcha"
         "ngeItem»."
        ),
    )

class OperationalStateDescription(U.StateMachine, MeasurableElement):
    """A state machine describing the behavior of a OperationalPerformer, depicting how the OperationalPerformer responds to various events and the actions."""
    _STEREO = "UAF::States::OperationalStateDescription"
    _BASE_METACLASSES = ("StateMachine",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("OperationalStateDescription.owner",
         "Values for the owner metaproperty must be stereotyped with specializations of «Operation"
         "alAgent» ."
        ),
    )

class Opportunity(MotivationalElement, U.Class, PhaseableElement, AffectableElement):
    """An existing or potential favorable circumstance or combination of circumstances which can be advantageous for addressing enterprise Challenges."""
    _STEREO = "UAF::Motivation::Opportunity"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class OrganizationalResource(PhysicalResource, U.Class, Stakeholder):
    """An abstract element grouping for Organization, Person, Post and Responsibility."""
    _STEREO = "UAF::Taxonomy::OrganizationalResource"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = True

class Organization(OrganizationalResource, U.Class):
    """A group of OrganizationalResources (Persons, Posts, Organizations and Responsibilities) associated for a particular purpose."""
    _STEREO = "UAF::Taxonomy::Organization"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class OrganizationInPhase(sysml.Allocate, U.Abstraction, MeasurableElement):
    """An abstraction relationship relating an ActualOrganization to an ActualStrategicPhase to denote that the ActualOrganization plays a role or is a stakeholder in an ActualStrategicPhase."""
    _STEREO = "UAF::Traceability::OrganizationInPhase"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("OrganizationInEnterprise.supplier",
         "Value for the supplier metaproperty must be stereotyped by any of specializations of «Ac"
         "tualStrategicPhase»."
        ),
        ("OrganizationInEnterprise.client",
         "Value for the client metaproperty must be stereotyped «ActualOrganization» or its specia"
         "lizations."
        ),
    )

class OwnsProcess(sysml.Allocate, U.Abstraction, MeasurableElement):
    """A dependency relationship denoting that an ActualOrganizationResource owns an OperationalActivity."""
    _STEREO = "UAF::Traceability::OwnsProcess"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("OwnsProcess.supplier",
         "Value for the supplier metaproperty must be stereotyped «OperationalActivity» or its spe"
         "cializations."
        ),
        ("OwnsProcess.client",
         "Value for the client metaproperty must be stereotyped «ActualOrganizationalResource» or "
         "its specializations."
        ),
    )

class OwnsRisk(sysml.Allocate, U.Abstraction, MeasurableElement):
    """An abstraction relating a Risk to an organizational resource that is responsible for executing the risk mitigation."""
    _STEREO = "UAF::Parameters::OwnsRisk"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("OwnsRisk.client",
         "Value for the client metaproperty must be stereotyped «OrganizationalResource» or its sp"
         "ecializations."
        ),
        ("OwnsRisk.supplier",
         "Value for the supplier metaproperty must be stereotyped «Risk» or its specializations."
        ),
    )

class OwnsRiskInContext(sysml.Allocate, U.Abstraction, MeasurableElement):
    """An abstraction relating a Risk to an organizational role that is responsible for executing the risk mitigation in the specific context or configuration."""
    _STEREO = "UAF::Parameters::OwnsRiskInContext"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("OwnsRiskInContext.client",
         "Value for the client metaproperty must be stereotyped «ResourceRole» or its specializati"
         "ons."
        ),
        ("OwnsRiskInContext.supplier",
         "Value for the supplier metaproperty must be stereotyped «Risk» or its specializations."
        ),
    )

class OwnsValue(sysml.Allocate, U.Abstraction, MeasurableElement):
    """An abstraction relationship denoting that an ActualOrganizationalResource owns a ValueItem"""
    _STEREO = "UAF::Taxonomy::OwnsValue"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("OwnsValue.client",
         "Value for the client metaproperty must be stereotyped by any of specializations of «Actu"
         "alOrganizationalResource»."
        ),
        ("OwnsValue.supplier",
         "Value for the supplier metaproperty must be stereotyped «ValueItem» or its specializatio"
         "ns."
        ),
    )

class PerformsInContext(sysml.Allocate, U.Abstraction, MeasurableElement):
    """An abstraction relationship that relates an OperationalAction to a OperationalRole, or a FunctionAction to a ResourceRole. It indicates that the action can be carried out by the role when used in a specific context or configuration."""
    _STEREO = "UAF::Processes::PerformsInContext"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("PerformsInContext.client",
         "In case of value for PerformsInContext.supplier is stereotyped: a. «OperationalActivityA"
         "ction» or its specializations, values for the client metaproperty must be stereotyped «O"
         "perationalRole» or its specializations, b. «ServiceFunctionAction» or its specialization"
         "s, values for the client metaproperty must be stereotyped «ServiceRole» or its specializ"
         "ations, c. «FunctionAction» or its specializations, except for «ProjectActivityAction», "
         "values for the client metaproperty must be stereotyped «ResourceRole» or its specializat"
         "ions. d. «ProjectActivityAction» or its specializations, values for the client metaprope"
         "rty must be stereotyped «ProjectRole» or its specializations."
        ),
        ("PerformsInContext.supplier",
         "In case of value for PerformsInContext.client is stereotyped: a. «OperationalRole» or it"
         "s specializations, values for the supplier metaproperty must be stereotyped «Operational"
         "ActivityAction» or its specializations, b. «ServiceRole» or its specializations, values "
         "for the supplier metaproperty must be stereotyped «ServiceFunctionAction» or its special"
         "izations, c. «ResourceRole» or its specializations, values for the supplier metaproperty"
         " must be stereotyped «FunctionAction» or its specializations."
        ),
    )

class Person(OrganizationalResource, U.Class):
    """A type of a human being used to define the characteristics that need to be described for ActualPersons (e.g. properties such as address, telephone number, nationality, etc)."""
    _STEREO = "UAF::Taxonomy::Person"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class Phases(U.Abstraction, MeasurableElement):
    """An abstraction relationship that exists between a PhaseableElement and an ActualStrategicPhase that it is assigned to."""
    _STEREO = "UAF::Summary and Overview::Phases"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("Phases.client",
         "Value for the client metaproperty must be stereotyped by any of specializations of «Actu"
         "alStrategicPhase»."
        ),
        ("Phases.supplier",
         "Value for the supplier metaproperty must be stereotyped by any of specializations of «Ph"
         "aseableElement»."
        ),
    )

class Post(OrganizationalResource, U.Class):
    """A type of job title or position that a person can fill (e.g. Lawyer, Solution Architect, Machine Operator or Chief Executive Officer)."""
    _STEREO = "UAF::Taxonomy::Post"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class PresentedBy(U.Dependency, MeasurableElement):
    """A dependency relationship denoting that a Challenge must be overcome for addressing a Driver."""
    _STEREO = "UAF::Motivation::PresentedBy"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("PresentedBy.client",
         "Value for the client metaproperty must be stereotyped «Challenge» or its specializations"
         "."
        ),
        ("PresentedBy.supplier",
         "Value for the supplier metaproperty must be stereotyped «Driver» or its specializations."
        ),
    )

class ProblemDomain(OperationalRole, U.Property):
    """A property associated with an OperationalArchitecture, used to specify the scope of the problem."""
    _STEREO = "UAF::Structure::ProblemDomain"
    _BASE_METACLASSES = ("Property",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ProblemDomain.class",
         "Value for the class metaproperty must be stereotyped «OperationalArchitecture» or its sp"
         "ecializations."
        ),
        ("ProblemDomain.type",
         "Value for the type metaproperty must be stereotyped «OperationalPerformer» or its specia"
         "lizations."
        ),
    )

class Project(OrganizationalResource, sysml.Block, U.Class):
    """A type that represents a planned endeavor executed by an ActualOrganization responsible for developing, deploying or decommissioning ResourcePerformers in accordance with ActualProjectMilestones."""
    _STEREO = "UAF::Taxonomy::Project"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class ProjectActivity(Function, U.Activity):
    """An activity carried out during a project."""
    _STEREO = "UAF::Processes::ProjectActivity"
    _BASE_METACLASSES = ("Activity",)
    _ABSTRACT = False

class ProjectActivityAction(FunctionAction, U.CallBehaviorAction):
    """The ProjectActivityAction is defined as a call behavior action that invokes the activity that needs to be preformed."""
    _STEREO = "UAF::Processes::ProjectActivityAction"
    _BASE_METACLASSES = ("CallBehaviorAction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ProjectActivityAction.activity",
         "Value for the activity metaproperty must be stereotyped «ProjectActivity» or its special"
         "izations."
        ),
        ("FunctionAction.behavior",
         "Value for the behavior metaproperty must be stereotyped «ProjectActivity» or its special"
         "izations."
        ),
    )

class ProjectMilestone(sysml.Block, U.Class, PropertySet):
    """A type of event in a Project by which progress is measured."""
    _STEREO = "UAF::Taxonomy::ProjectMilestone"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False
    _DECL = {
    # Relates a ProjectMilestone to the Resources that can be affected by the milestone. It is used to
    #  describe aspects of the lifecycle of a Resource.
    'resource': _Ref('resource', 'ResourcePerformer', multi=True, lo=0, hi='*'),
    }
    CONSTRAINTS = (
        ("ProjectMilestone.ownedAttribute",
         "All of the «ProjectThemes», owned by a «ProjectMilestone», must be typed by the same «St"
         "atusIndicators» or its specializations."
        ),
    )

class ProjectMilestoneRole(U.Property, MeasurableElement):
    """The role played by a ProjectMilestone in the context of a Project."""
    _STEREO = "UAF::Structure::ProjectMilestoneRole"
    _BASE_METACLASSES = ("Property",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ProjectMilestoneRole.class",
         "Value for the class metaproperty must be stereotyped «Project» or its specializations."
        ),
        ("ProjectMilestoneRole.type",
         "Value for the type metaproperty must be stereotyped «ProjectMilestone» or its specializa"
         "tions."
        ),
    )

class ResourceRole(U.Property, AssetRole, LocationHolder, SubjectOfResourceConstraint, MeasurableElement):
    """Usage of a ResourcePerformer in the context of another ResourcePerformer. Creates a whole-part relationship."""
    _STEREO = "UAF::Structure::ResourceRole"
    _BASE_METACLASSES = ("Property",)
    _ABSTRACT = False
    _DECL = {
    # Captures the kind of role a Resource can play.
    'roleKind': _Ref('roleKind', RoleKind),
    }
    CONSTRAINTS = (
        ("ResourceRole.class",
         "Value for the class metaproperty must be stereotyped by the specialization of «ResourceP"
         "erformer»."
        ),
        ("ResouceRole.type",
         "Value for the type metaproperty must be stereotyped by the specialization of «ResourcePe"
         "rformer»."
        ),
    )

class ProjectRole(ResourceRole, U.Property):
    """Usage of a Project in the context of another Project. Creates a whole-part relationship."""
    _STEREO = "UAF::Structure::ProjectRole"
    _BASE_METACLASSES = ("Property",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ProjectRole.class",
         "Value for the class metaproperty must be stereotyped «Project» or its specializations."
        ),
        ("ProjectRole.type",
         "Value for the type metaproperty must be stereotyped «Project» or its specializations."
        ),
    )

class ProjectSequence(Sequence, U.Dependency):
    """A dependency relationship between two ActualProjects that denotes one ActualProject cannot start before the previous ActualProject is finished."""
    _STEREO = "UAF::Connectivity::ProjectSequence"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ProjectSequence.client",
         "Value for the client metaproperty must be stereotyped «ActualProject» or its specializat"
         "ions."
        ),
        ("ProjectSequence.supplier",
         "Value for the supplier metaproperty must be stereotyped «ActualProject» or its specializ"
         "ations."
        ),
    )

class ProjectStatus(U.Slot, UAFElement):
    """The status (i.e. level of progress) of a ProjectTheme for an ActualProject at the time of the ActualProjectMilestone."""
    _STEREO = "UAF::Structure::ProjectStatus"
    _BASE_METACLASSES = ("Slot",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ProjectStatus.definingFeature",
         "Value for the DefiningFeature metaproperty must be stereotyped «ProjectTheme» or its spe"
         "cializations."
        ),
    )

class ProjectTheme(U.Property, MeasurableElement):
    """A property of a ProjectMilestone that captures an aspect by which the progress of ActualProjects may be measured."""
    _STEREO = "UAF::Structure::ProjectTheme"
    _BASE_METACLASSES = ("Property",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ProjecTheme.type",
         "Value for the type metaproperty must be stereotyped «StatusIndicators» or its specializa"
         "tions."
        ),
        ("ProjecTheme.class",
         "Value for the class metaproperty must be stereotyped «ProjectMilestone» or its specializ"
         "ations."
        ),
    )

class Protects(U.Dependency, MeasurableElement):
    """A dependency that asserts that a SecurityControl is required to protect an Asset."""
    _STEREO = "UAF::Motivation::Protects"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("Protects.client",
         "Value for the client metaproperty must be stereotyped «SecurityControl» or its specializ"
         "ations."
        ),
        ("Protects.supplier",
         "Value for the supplier metaproperty must be stereotyped bu the specialization of «Asset»"
         "."
        ),
    )

class ProtectsInContext(U.Dependency, MeasurableElement):
    """A dependency relationship that relates a SecurityControlAction to a OperationalRole, or a ResourceRole. It indicates that SecurityControl is required to protect an Asset in a specific context or configuration."""
    _STEREO = "UAF::Motivation::ProtectsInContext"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ProtectsInContext.client",
         "Value for the client metaproperty must be stereotyped «SecurityControl» or its specializ"
         "ations."
        ),
        ("ProtectsInContext.supplier",
         "Value for the supplier metaproperty must be stereotyped «AssetRole» or its specializatio"
         "ns."
        ),
    )

class Standard(SubjectOfForecast, sysml.Block, U.Class, PropertySet):
    """A ratified and peer-reviewed specification that is used to guide or constrain the architecture. A Standard may be applied to any element in the architecture."""
    _STEREO = "UAF::Taxonomy::Standard"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False
    _DECL = {
    # The date when this version of the Standard was published.
    'mandatedDate': _Ref('mandatedDate', 'ISO8601DateTime'),
    # Relates a Standard to the ActualOrganization that ratified the Standard.
    'ratifiedBy': _Ref('ratifiedBy', 'ActualOrganization', multi=True, lo=0, hi='*'),
    # The date when this version of the Standard was retired.
    'retiredDate': _Ref('retiredDate', 'ISO8601DateTime'),
    }

class Protocol(Standard, U.Class):
    """A Standard for communication over a network. Protocols may be composite, represented as a ProtocolStack made up of ProtocolLayers."""
    _STEREO = "UAF::Taxonomy::Protocol"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class ProtocolImplementation(UAFElement, U.Element):
    """An abstract grouping of architectural elements that can implement Protocols."""
    _STEREO = "UAF::Traceability::ProtocolImplementation"
    _BASE_METACLASSES = ("Element",)
    _ABSTRACT = True
    _DECL = {
    # Relates the ResourceConnector and ResourcePort to the Protocols that they can implement.
    'implements': _Ref('implements', 'Protocol', multi=True, lo=0, hi='*'),
    }

class ProtocolLayer(U.Property, MeasurableElement):
    """Usage of a Protocol in the context of another Protocol. Creates a whole-part relationship."""
    _STEREO = "UAF::Structure::ProtocolLayer"
    _BASE_METACLASSES = ("Property",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ProtocolLayer.class",
         "Value for the class metaproperty must be stereotyped «Protocol» or its specializations."
        ),
        ("ProtocolLayer.type",
         "Value for the type metaproperty must be stereotyped «Protocol» or its specializations."
        ),
    )

class ProtocolStack(Protocol, U.Class):
    """A sub-type of Protocol that contains the ProtocolLayers, defining a complete stack."""
    _STEREO = "UAF::Taxonomy::ProtocolStack"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class ProvidedServiceLevel(ActualService, U.InstanceSpecification):
    """A sub type of ActualService that details a specific service level delivered by the provider."""
    _STEREO = "UAF::Constraints::ProvidedServiceLevel"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False

class ProvidesCompetence(U.Dependency, MeasurableElement):
    """A dependency relationship that asserts that an ActualOrganizationalResource provides a specific set of Competencies."""
    _STEREO = "UAF::Constraints::ProvidesCompetence"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ProvidesCompetence.client",
         "Value for the client metaproperty must be stereotyped by a specialization of «ActualOrga"
         "nizationalResource»."
        ),
        ("ProvidesCompetence.supplier",
         "Value for the supplier metaproperty must be stereotyped «Competence» or its specializati"
         "ons."
        ),
    )

class RequiredServiceLevel(ActualService, U.InstanceSpecification):
    """A sub type of ActualService that details a specific service level required of the provider."""
    _STEREO = "UAF::Constraints::RequiredServiceLevel"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False

class RequiresCompetence(sysml.Allocate, U.Abstraction, MeasurableElement):
    """An abstraction relationship that asserts that an ActualOrganizationalResource is required to have a specific set of Competencies."""
    _STEREO = "UAF::Constraints::RequiresCompetence"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("RequiresCompetence.client",
         "Value for the client metaproperty must be stereotyped a specialization of «Organizationa"
         "lResource»."
        ),
        ("RequiresCompetence.supplier",
         "Value for the supplier metaproperty must be stereotyped «Competence» or its specializati"
         "ons."
        ),
    )

class ResourceArtifact(PhysicalResource, U.Class):
    """A type of man-made object that contains no human beings (i.e. satellite, radio, petrol, gasoline, etc.)."""
    _STEREO = "UAF::Taxonomy::ResourceArtifact"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class ResourceConnector(U.Connector, AssetRole, ProtocolImplementation):
    """A channel for exchange between two ResourceRoles."""
    _STEREO = "UAF::Connectivity::ResourceConnector"
    _BASE_METACLASSES = ("Connector",)
    _ABSTRACT = False
    _DECL = {
    # Relates a ResourceConector to the extremes of the Environment in which it is required to be made
    #  available.
    'boundaryCondition': _Ref('boundaryCondition', 'Environment', multi=True, lo=0, hi='*'),
    }
    CONSTRAINTS = (
        ("ResourceConnector.end",
         "The value for the role metaproperty for the owned ConnectorEnd must be stereotype «Resou"
         "rcePort», «ResourceRole» or their specializations."
        ),
    )

class ResourceConstraint(Rule, U.Constraint):
    """A rule governing the structural or functional aspects of an implementation."""
    _STEREO = "UAF::Constraints::ResourceConstraint"
    _BASE_METACLASSES = ("Constraint",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ResourceConstraint.constrainedElement",
         "Value for the constrainedElement metaproperty must be stereotyped by the specialization "
         "of «SubjectOfResourceConstraint»."
        ),
    )

class ResourceInformation(ResourceAsset, U.Class, ResourceExchangeItem, SubjectOfResourceConstraint):
    """A formalized representation of information that is managed by or exchanged between systems."""
    _STEREO = "UAF::Information::ResourceInformation"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ResourceInformation.owner",
         "Values for the owner metaproperty must be stereotyped «InformationModel» or its speciali"
         "zations."
        ),
    )

class ResourceInformationRole(AssetRole, U.Element):
    """A usage of ResourceInformation that exists in the context of a ResourceAsset. It also allows the representation of the whole-part aggregation of ResourceInformation elements."""
    _STEREO = "UAF::Structure::ResourceInformationRole"
    _BASE_METACLASSES = ("Element",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ResourceInformationRole.class",
         "Value for the class metaproperty must be stereotyped by the specialization of «ResourceA"
         "sset»."
        ),
        ("ResourceInformationRole.type",
         "Value for the type metaproperty must be stereotyped «ResourceInformation» or its special"
         "izations."
        ),
    )

class ResourceInterface(sysml.InterfaceBlock, U.Class, PropertySet):
    """A declaration that specifies a contract between the ResourcePerformers it is related to and any other ResourcePerformers it can interact with. It is also intended to be an implementation of a specification of an Interface in the Business and/or Service layer."""
    _STEREO = "UAF::Connectivity::ResourceInterface"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ResourceInterface.ownedOperation",
         "Values for ownedOperation metaproperty must be stereotyped «ResourceMethod» or its speci"
         "alizations."
        ),
    )

class ResourceMessage(U.Message, MeasurableElement):
    """Message for use in a Resource Event-Trace which carries any of the subtypes of ResourceExchange."""
    _STEREO = "UAF::Sequences::ResourceMessage"
    _BASE_METACLASSES = ("Message",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ResourceMessage.receiveEvent.event.operation",
         "Values for the receiveEvent.event.operation metaproperty must be stereotyped with «Resou"
         "rceMethod» or its specializations."
        ),
    )

class ResourceMethod(U.Operation, MeasurableElement):
    """A behavioral feature of a ResourcePerformer whose behavior is specified in a Function."""
    _STEREO = "UAF::Structure::ResourceMethod"
    _BASE_METACLASSES = ("Operation",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ResourceMethod.method",
         "Value for the method metaproperty must be stereotyped «Function» or its specializations."
        ),
        ("ResourceMethod.ownedParameter",
         "The values for the ownedParameter metaproperty must be stereotyped «ResourceParameter»."
        ),
    )

class ResourceMitigation(ResourceArchitecture, U.Class):
    """A set of ResourcePerformers intended to address against specific risks."""
    _STEREO = "UAF::Taxonomy::ResourceMitigation"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class ResourceParameter(U.Parameter, MeasurableElement):
    """An element that represents inputs and outputs of a Function. It is typed by a ResourceInteractionItem."""
    _STEREO = "UAF::Structure::ResourceParameter"
    _BASE_METACLASSES = ("Parameter",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ResourceParameter.type",
         "Value for the type metaproperty must be stereotyped with a specialization of «ResourceIn"
         "teractionItem»."
        ),
    )

class ResourcePort(sysml.ProxyPort, U.Port, MeasurableElement, ProtocolImplementation):
    """An interaction point for a ResourcePerformer through which it can interact with the outside environment and which is defined by a ResourceInterface."""
    _STEREO = "UAF::Structure::ResourcePort"
    _BASE_METACLASSES = ("Port",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ResoucePort.type",
         "Value for the type metaproperty must be stereotyped «ResourceInterface» or its specializ"
         "ations."
        ),
        ("ResourcePort.class",
         "Value for the class metaproperty must be stereotyped by the specialization of «ResourceP"
         "erformer»."
        ),
    )

class ResourceService(ResourcePerformer, U.Class):
    """A services that a ResourcePerformer provides to support higher level Services or OperationalActivities. Employee provisioning, backup and recovery, storage, self-service help desk are examples of ResourceServices."""
    _STEREO = "UAF::Taxonomy::ResourceService"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class ResourceServiceInterface(ResourceInterface, U.Class):
    """A contract that defines the ResourceMethods and ResourceSignal receptions that the ResourceServices realize."""
    _STEREO = "UAF::Connectivity::ResourceServiceInterface"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class ResourceSignal(U.Signal, ResourceExchangeItem):
    """A ResourceSignal is a specification of a kind of communication between resources (ResourcePerformers) in which a reaction is asynchronously triggered in the receiver without a reply."""
    _STEREO = "UAF::Connectivity::ResourceSignal"
    _BASE_METACLASSES = ("Signal",)
    _ABSTRACT = False

class ResourceSignalProperty(U.Property, MeasurableElement):
    """A property of an ResourceSignal typed by ResourceExchangeItem. It enables ResourceExchangeItem e.g. ResourceInformation to be passed as arguments of the ResourceSignal."""
    _STEREO = "UAF::Connectivity::ResourceSignalProperty"
    _BASE_METACLASSES = ("Property",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ResourceSignalProperty.class",
         "Value for class metaproperty must be stereotyped «ResourceSignal» or its specializations"
         "."
        ),
        ("ResourceSignalProperty.type",
         "Value for type metaproperty must be stereotyped by a specialization of «ResourceExchange"
         "Item»."
        ),
    )

class ResourceStateDescription(U.StateMachine, MeasurableElement):
    """A state machine describing the behavior of a ResourcePerformer, depicting how the ResourcePerformer responds to various events and the actions."""
    _STEREO = "UAF::States::ResourceStateDescription"
    _BASE_METACLASSES = ("StateMachine",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ResourceStateDescription.owner",
         "Values for the owner metaproperty must be stereotyped with the specialization of «Resour"
         "cePerformer»."
        ),
    )

class Responsibility(OrganizationalResource, U.Class):
    """The type of duty required of a Person or Organization."""
    _STEREO = "UAF::Taxonomy::Responsibility"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class ResponsibleFor(sysml.Allocate, U.Abstraction, MeasurableElement):
    """An abstraction relationship between an ActualResponsibleResource and an ActualResponsibility or ActualProject. It defines the duties that the ActualResponsibleResource is ResponsibleFor."""
    _STEREO = "UAF::Traceability::ResponsibleFor"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    _DECL = {
    # End date of an ActualResponsibleResource being ResponsibleFor and ActualProject or ActualRespons
    # ibility.
    'endDate': _Ref('endDate', 'ISO8601DateTime'),
    # Captures the kind of role (Manager or ResponsibleOwner) responsible for the ActualProject or Act
    # ualResponsibility.
    'responsibleRoleKind': _Ref('responsibleRoleKind', ResponsibleRoleKind),
    # Start date of an ActualResponsibleResource being ResponsibleFor and ActualProject or ActualRespo
    # nsibility.
    'startDate': _Ref('startDate', 'ISO8601DateTime'),
    }
    CONSTRAINTS = (
        ("ResponsibleFor.client",
         "Value for the client metaproperty must be stereotyped by the specialization of «ActualRe"
         "sponsibleResource»."
        ),
        ("ResponsibleFor.supplier",
         "Value for the supplier metaproperty must be stereotyped «ActualProject», «ActualResponsi"
         "bility», «ActualProjectMilestone» or their specializations."
        ),
    )

class Risk(sysml.Block, U.Constraint, PropertySet):
    """A type that represents a situation involving exposure to danger of AffectableElements (e.g. Assets, Processes, Capabilities, Opportunities, or Enterprise Goals) where the effects of such exposure can be characterized in terms of the likelihood of occurrence of a given threat and the potential adverse consequences of that threat's occurrence."""
    _STEREO = "UAF::Parameters::Risk"
    _BASE_METACLASSES = ("Constraint",)
    _ABSTRACT = False

class SameAs(U.Dependency, MeasurableElement):
    """A dependency relationship that asserts that two elements refer to the same real-world thing."""
    _STEREO = "UAF::Information::SameAs"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("SameAs.client",
         "Values for the client metaproperty must be stereotyped by the specialization of «UAFElem"
         "ent»."
        ),
        ("SameAs.supplier",
         "Values for the supplier metaproperty must be stereotyped by the specialization of «UAFEl"
         "ement»."
        ),
    )

class SecurityConstraint(Rule, U.Constraint):
    """A type of rule that captures a formal statement to define security laws, regulations, guidances, and policy."""
    _STEREO = "UAF::Constraints::SecurityConstraint"
    _BASE_METACLASSES = ("Constraint",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("Security.constrainedElement",
         "Value for the constrainedElement metaproperty must be stereotyped by the specialization "
         "of «SubjectOfSecurityConstraint»."
        ),
    )

class SecurityControlFamily(SecurityControl, U.Class):
    """An element that organizes security controls into a family. Each Security Control Family contains security controls related to the general security topic of the family."""
    _STEREO = "UAF::Motivation::SecurityControlFamily"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class SecurityEnclave(ResourceArchitecture, U.Class):
    """Collection of information systems connected by one or more internal networks under the control of a single authority and security policy. The systems may be structured by physical proximity or by function, independent of location."""
    _STEREO = "UAF::Taxonomy::SecurityEnclave"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class SecurityProcess(OperationalActivity, Function, U.Activity, SubjectOfSecurityConstraint):
    """The security-related procedure that satisfies the security control requirement."""
    _STEREO = "UAF::Processes::SecurityProcess"
    _BASE_METACLASSES = ("Activity",)
    _ABSTRACT = False

class SecurityProcessAction(OperationalActivityAction, FunctionAction, U.CallBehaviorAction):
    """A call of a SecurityProcess in the context of another SecurityProcess."""
    _STEREO = "UAF::Processes::SecurityProcessAction"
    _BASE_METACLASSES = ("CallBehaviorAction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("SecurityProcessAction.behavior",
         "Value for behavior metaproperty must be stereotyped «SecurityProcess» or its specializat"
         "ions."
        ),
    )

class SecurityRisk(Risk, U.Class):
    """The level of impact on enterprise operations, assets, or individuals resulting from the operation of an information system given the potential impact of a threat and the likelihood of that threat occurring [NIST SP 800-65]."""
    _STEREO = "UAF::Constraints::SecurityRisk"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class Service(Asset, VersionedElement, sysml.Block, U.Class, PropertySet, CapableElement):
    """A mechanism to enable access to one or more capabilities, where the access is provided using a prescribed service interface and is exercised consistent with service constraints and policies."""
    _STEREO = "UAF::Taxonomy::Service"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class ServiceArchitecture(Service, Architecture, U.Class):
    """An element used to denote a model of the Architecture, described from the Services perspective."""
    _STEREO = "UAF::Taxonomy::ServiceArchitecture"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class ServiceConnector(U.Connector, AssetRole):
    """A channel for exchange between two Services. Where one acts as the consumer of the other."""
    _STEREO = "UAF::Connectivity::ServiceConnector"
    _BASE_METACLASSES = ("Connector",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ServiceConnector.end",
         "The value for the role metaproperty for the owned ConnectorEnd must be stereotyped «Serv"
         "icePort», «ServiceRole» or their specializations."
        ),
    )

class ServiceContract(Rule, U.Constraint):
    """A constraint governing the use of one or more Services."""
    _STEREO = "UAF::Constraints::ServiceContract"
    _BASE_METACLASSES = ("Constraint",)
    _ABSTRACT = False
    _DECL = {
    # OperationalExchanges constrained to be carried out by the Service GovernedBy this ServiceContrac
    # t.
    'constrainedExchanges': _Ref('constrainedExchanges', 'OperationalExchange', multi=True, lo=0, hi='*', derived=True),
    }
    CONSTRAINTS = (
        ("ServiceContract.constrainedElement",
         "Values for constrainedElement metaproperty must be stereotyped «OperationalConnector» or"
         " its specializations."
        ),
    )

class ServiceFunctionEdge(U.ActivityEdge, MeasurableElement):
    """Abstract grouping for ServiceControlFlow and ServiceObjectFlow."""
    _STEREO = "UAF::Processes::ServiceFunctionEdge"
    _BASE_METACLASSES = ("ActivityEdge",)
    _ABSTRACT = True
    CONSTRAINTS = (
        ("ServiceFunctionEdge.owner",
         "«ServiceFunctionEdge» must be owned directly or indirectly by «ServiceFunction» or its s"
         "pecializations."
        ),
    )

class ServiceControlFlow(U.ControlFlow, ServiceFunctionEdge):
    """An ActivityEdge that shows the flow of control between ServiceFunctionActions."""
    _STEREO = "UAF::Processes::ServiceControlFlow"
    _BASE_METACLASSES = ("ControlFlow",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ServiceControlFlow.source",
         "Value for the source metaproperty must be stereotyped «ServiceFunctionAction» or its spe"
         "cializations."
        ),
        ("ServiceControlFlow.target",
         "Value for the target metaproperty must be stereotyped «ServiceFunctionAction» or its spe"
         "cializations."
        ),
    )

class ServiceExchange(Exchange, U.InformationFlow):
    """Asserts that a flow can exist between Services (i.e. flows of information, people, materiel, or energy)."""
    _STEREO = "UAF::Connectivity::ServiceExchange"
    _BASE_METACLASSES = ("InformationFlow",)
    _ABSTRACT = False
    _DECL = {
    # Captures the kind of Resource being exchanged.
    'exchangeKind': _Ref('exchangeKind', ServiceExchangeKind, derived=True),
    }
    CONSTRAINTS = (
        ("ServiceExchange.conveyed",
         "Value for conveyed metaproperty has to be stereotyped by any of specializations of «Serv"
         "iceExchangeItem»."
        ),
        ("ServiceExchange.informationSource",
         "Value for informationSource metaproperty has to be stereotyped «Service» or its speciali"
         "zations."
        ),
        ("ServiceExchange.informationTarget",
         "Value for informationTarget metaproperty has to be stereotyped «Service» or its speciali"
         "zations."
        ),
        ("ServiceExchange.realizingActivityEdge",
         "Value for the realizingActivityEdge metaproperty must be stereotyped by the specializati"
         "on of «ServiceFunctionEdge»."
        ),
        ("ServiceExchange.realizingConnector",
         "Value for the realizingConnector metaproperty must be stereotyped «ServiceConnector» or "
         "its specializations."
        ),
        ("ServiceExchange.realizingMessage",
         "Value for the realizingMessage metaproperty must be stereotyped «ServiceMessage» or its "
         "specializations."
        ),
    )

class ServiceFunction(Activity, U.Activity):
    """An Activity that describes the abstract behavior of Services, regardless of the actual implementation."""
    _STEREO = "UAF::Processes::ServiceFunction"
    _BASE_METACLASSES = ("Activity",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ServiceFunction.ownedParameter",
         "The values for the ownedParameter metaproperty must be stereotyped «ServiceParameter»."
        ),
    )

class ServiceFunctionAction(U.CallBehaviorAction, MeasurableElement):
    """A call of a ServiceFunction in the context of another ServiceFunction."""
    _STEREO = "UAF::Processes::ServiceFunctionAction"
    _BASE_METACLASSES = ("CallBehaviorAction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ServiceFunctionAction.behavior",
         "Value for the activity metaproperty must be stereotyped «ServiceFunction» or its special"
         "izations."
        ),
        ("ServiceFunctionAction.activity",
         "Value for the behavior metaproperty must be stereotyped «ServiceFunction» or its special"
         "izations."
        ),
    )

class ServiceInterface(sysml.InterfaceBlock, U.Class, PropertySet):
    """A contract that defines the ServiceMethods and ServiceSignals that the Service realizes."""
    _STEREO = "UAF::Connectivity::ServiceInterface"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ServiceInterface.ownedOperation",
         "Values for the ownedOperation metaproperty must be stereotyped «ServiceMethod» or its sp"
         "ecializations."
        ),
    )

class ServiceMessage(U.Message, MeasurableElement):
    """Message for use in a services interaction scenario which carries any of the subtypes of ServiceExchange."""
    _STEREO = "UAF::Sequences::ServiceMessage"
    _BASE_METACLASSES = ("Message",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ServiceMessage.receiveEvent.event.operation",
         "Values for the receiveEvent.event.operation metaproperty must be stereotyped with «Servi"
         "ceMethod» or its specializations."
        ),
    )

class ServiceMethod(U.Operation, MeasurableElement):
    """A behavioral feature of a Service whose behavior is specified in a ServiceFunction."""
    _STEREO = "UAF::Structure::ServiceMethod"
    _BASE_METACLASSES = ("Operation",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ServiceMethod.ownedParameter",
         "The values for the ownedParameter metaproperty must be stereotyped «ServiceParameter» or"
         " its specializations."
        ),
        ("ServiceMethod.method",
         "Value for the method metaproperty must be stereotyped «ServiceFunction» or its specializ"
         "ations."
        ),
        ("ServiceMethod.owner",
         "The values for the owner metaproperty must be stereotyped «Service» or its specializatio"
         "ns."
        ),
    )

class ServiceObjectFlow(U.ObjectFlow, ServiceFunctionEdge):
    """An ActivityEdge that shows the flow of Resources (objects/information) between ServiceFunctionActions."""
    _STEREO = "UAF::Processes::ServiceObjectFlow"
    _BASE_METACLASSES = ("ObjectFlow",)
    _ABSTRACT = False

class ServiceParameter(U.Parameter, MeasurableElement):
    """An element that represents inputs and outputs of a ServiceFunction, represents inputs and outputs of a Service."""
    _STEREO = "UAF::Structure::ServiceParameter"
    _BASE_METACLASSES = ("Parameter",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ServiceParameter.type",
         "The values for the type metaproperty must be stereotyped a specialization of «ServiceExc"
         "hangeItem»."
        ),
    )

class ServicePolicy(Rule, U.Constraint):
    """A constraint governing the use of one or more Services."""
    _STEREO = "UAF::Constraints::ServicePolicy"
    _BASE_METACLASSES = ("Constraint",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ServicePolicy.constrainedElement",
         "Values for constrainedElement metaproperty must be stereotyped «Service» or its speciali"
         "zations."
        ),
    )

class ServicePort(sysml.ProxyPort, U.Port, MeasurableElement):
    """An interaction point for a Service through which it can interact with the outside environment and which is defined by a ServiceInterface."""
    _STEREO = "UAF::Structure::ServicePort"
    _BASE_METACLASSES = ("Port",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ServicePort.type",
         "Value for the type metaproperty must be stereotyped «ServiceInterface» or its specializa"
         "tions."
        ),
        ("ServicePort.class",
         "Value for the class metaproperty must be stereotyped «Service» or its specializations."
        ),
    )

class ServiceRole(U.Property, AssetRole, MeasurableElement):
    """Usage of a Service in the context of another Service. Creates a whole-part relationship."""
    _STEREO = "UAF::Structure::ServiceRole"
    _BASE_METACLASSES = ("Property",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ServiceRole.type",
         "Value for the type metaproperty must be stereotyped «Service» or its specializations."
        ),
        ("ServiceRole.class",
         "Value for the class metaproperty must be stereotyped «Service» or its specializations."
        ),
    )

class ServiceSignal(U.Signal, ServiceExchangeItem):
    """A specification of a kind of communication between Services in which a reaction is asynchronously triggered in the receiver without a reply."""
    _STEREO = "UAF::Connectivity::ServiceSignal"
    _BASE_METACLASSES = ("Signal",)
    _ABSTRACT = False

class ServiceSignalProperty(U.Property, MeasurableElement):
    """A property of a ServiceSignal typed by ServiceExchangeItem. It enables ServiceExchangeItem e.g. OperationalInformation to be passed as arguments of the ServiceSignal."""
    _STEREO = "UAF::Connectivity::ServiceSignalProperty"
    _BASE_METACLASSES = ("Property",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ServiceSignalProperty.class",
         "Value for class metaproperty must be stereotyped «ServiceSignal» or its specializations."
        ),
        ("ServiceSignalProperty.type",
         "Value for type metaproperty must be stereotyped by the specialization of «ServiceExchang"
         "eItem»."
        ),
    )

class ServiceStateDescription(U.StateMachine, MeasurableElement):
    """A state machine describing the behavior of a Service, depicting how the Service responds to various events and the actions."""
    _STEREO = "UAF::States::ServiceStateDescription"
    _BASE_METACLASSES = ("StateMachine",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("ServiceStateMachine.owner",
         "Values for the owner metaproperty must be stereotyped «Service» or its specializations."
        ),
    )

class Software(ResourceArtifact, U.Class):
    """A sub-type of ResourceArtifact that specifies an executable computer program."""
    _STEREO = "UAF::Taxonomy::Software"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class StandardOperationalActivity(OperationalActivity, U.Activity):
    """A sub-type of OperationalActivity that is a standard operating procedure."""
    _STEREO = "UAF::Processes::StandardOperationalActivity"
    _BASE_METACLASSES = ("Activity",)
    _ABSTRACT = False

class StatusIndicators(U.Enumeration, sysml.ValueType, MeasurableElement):
    """An enumerated type that specifies a status for a ProjectTheme."""
    _STEREO = "UAF::Structure::StatusIndicators"
    _BASE_METACLASSES = ("Enumeration",)
    _ABSTRACT = False

class StrategicAsset(Asset, U.Class):
    """An abstract element that indicates the types of strategic elements that can be affected by Risk."""
    _STEREO = "UAF::Taxonomy::StrategicAsset"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = True

class StrategicConstraint(Rule, U.Constraint):
    """A Rule governing a Capability."""
    _STEREO = "UAF::Constraints::StrategicConstraint"
    _BASE_METACLASSES = ("Constraint",)
    _ABSTRACT = False

class StrategicExchange(Exchange, U.InformationFlow):
    """Asserts that a flow can exist between ActualStrategicPhases (i.e. flows of information, people, materiel, or energy)."""
    _STEREO = "UAF::Connectivity::StrategicExchange"
    _BASE_METACLASSES = ("InformationFlow",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("StrategicExchange.conveyed",
         "Value for conveyed metaproperty has to be stereotyped by any of specializations of «Stra"
         "tegicExchangeItem»."
        ),
        ("StrategicExchange.informationSource",
         "Value for informationSource metaproperty has to be stereotyped by any of specializations"
         " of «ActualStrategicPhase»."
        ),
        ("StrategicExchange.informationTarget",
         "Value for informationTarget metaproperty has to be stereotyped by any of specializations"
         " of «ActualStrategicPhase»."
        ),
    )

class StrategicInformation(StrategicAsset, U.Class, StrategicExchangeItem):
    """Knowledge communicated or received concerning a particular fact or circumstance that is strategic in nature that is important or essential in relation to a plan of action"""
    _STEREO = "UAF::Information::StrategicInformation"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("StrategicInformation.owner",
         "Values for the owner metaproperty must be stereotyped «DataModel» or its specializations"
         "."
        ),
    )

class StrategicPhase(sysml.Block, U.Class, PropertySet):
    """A type of a current or future phase of the enterprise, mission, ValueStream, or EnduringTask."""
    _STEREO = "UAF::Taxonomy::StrategicPhase"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class StructuralPart(U.Property, MeasurableElement):
    """Usage of a StrategicPhase in the context of another StrategicPhase. It asserts that one StrategicPhase is a spatial part of another. Creates a whole-part relationship that represents the structure of the StrategicPhase."""
    _STEREO = "UAF::Structure::StructuralPart"
    _BASE_METACLASSES = ("Property",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("StructuralPart.class",
         "Value for class metaproperty must be stereotyped «StrategicPhase» or its specializations"
         "."
        ),
        ("StructuralPart.type",
         "Value for type metaproperty must be stereotyped «StrategicPhase» or its specializations."
        ),
    )

class Supports(sysml.Allocate, U.Abstraction, MeasurableElement):
    """A abstraction relationship that asserts that a service in someway contributes or assists in the execution of an OperationalActivity."""
    _STEREO = "UAF::Traceability::Supports"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("Supports.client",
         "Value for the client metaproperty must be stereotyped «Service» or its specializations."
        ),
        ("Supports.supplier",
         "Value for the supplier metaproperty must be stereotyped «OperationalActivity» or its spe"
         "cializations."
        ),
    )

class System(ResourceArchitecture, U.Class):
    """An integrated set of elements, subsystems, or assemblies that accomplish a defined objective. These elements include products (hardware, software, firmware), processes, people, information, techniques, facilities, services, and other support elements (INCOSE SE Handbook V4, 2015)."""
    _STEREO = "UAF::Taxonomy::System"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class Technology(ResourceArtifact, U.Class):
    """A sub type of ResourceArtifact that indicates a technology domain, i.e. nuclear, mechanical, electronic, mobile telephony etc."""
    _STEREO = "UAF::Roadmap::Technology"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class TemporalPart(U.Property, MeasurableElement):
    """Usage of a StrategicPhase in the context of another StrategicPhase. It asserts that one StrategicPhase is a spatial part of another. Creates a whole-part relationship that represents the temporal structure of the StrategicPhase."""
    _STEREO = "UAF::Structure::TemporalPart"
    _BASE_METACLASSES = ("Property",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("TemporalPart.class",
         "Value for class metaproperty must be stereotyped «EnterprisePhase» or its specialization"
         "s."
        ),
        ("TemporalPart.type",
         "Value for type metaproperty must be stereotyped «EnterprisePhase» or its specializations"
         "."
        ),
    )

class ValueItem(StrategicAsset, MeasurementSet, U.DataType):
    """An ideal, custom, or institution that an enterprise promotes or agrees with. It may be positive or negative, depending on point of view."""
    _STEREO = "UAF::Taxonomy::ValueItem"
    _BASE_METACLASSES = ("DataType",)
    _ABSTRACT = False
    _DECL = {
    # Captures the kind of ValueItem if the ValueItemKind has been set to "Other".
    'customKind': _Ref('customKind', str),
    # Captures the kind of ValueItem.
    'kind': _Ref('kind', ValueItemKind),
    }

class ValueStream(ActualStrategicPhase, U.InstanceSpecification):
    """An end-to-end collection of activities that create a result for a customer, who may be the ultimate customer or an internal end-user of the value stream. Value stream nested within another value stream may represent Value Stream Stage - a distinct, identifiable phase or step within a value stream [The Business Architecture Metamodel Guide, 2020]."""
    _STEREO = "UAF::Processes::ValueStream"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False

class VersionOfConfiguration(U.Property, MeasurableElement):
    """A property of a WholeLifeConfiguration, used in version control of a VersionedElement. It asserts that a VersionedElement is a version of a WholeLifeConfiguration."""
    _STEREO = "UAF::Roadmap::VersionOfConfiguration"
    _BASE_METACLASSES = ("Property",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("VersionOfConfiguration.class",
         "Value for the class metaproperty must be stereotyped «WholeLifeConfiguration» or its spe"
         "cializations."
        ),
        ("VersionOfConfiguration.type",
         "Value for the type metaproperty must be stereotyped by the specialization of «VersionedE"
         "lement»."
        ),
    )

class VersionSuccession(U.Dependency, MeasurableElement):
    """A dependency relationship between two VersionOfConfigurations that denotes that one VersionOfConfiguration follows from another."""
    _STEREO = "UAF::Roadmap::VersionSuccession"
    _BASE_METACLASSES = ("Dependency",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("VersionSuccession.client",
         "Value for the client metaproperty must be stereotyped «VersionOfConfiguration» or its sp"
         "ecializations."
        ),
        ("VersionSuccession.supplier",
         "Value for the supplier metaproperty must be stereotyped «VersionOfConfiguration» or its "
         "specializations."
        ),
    )

class View(sysml.View, U.Class, PropertySet):
    """An information item, governed by an architecture viewpoint, comprising part of an architecture description that communicates some aspect of an architecture."""
    _STEREO = "UAF::Summary and Overview::View"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False
    _DECL = {
    # Relates the View to the Viewpoint that the View conforms to.
    'viewpoint': _Ref('viewpoint', 'Viewpoint'),
    }

class Viewpoint(sysml.Viewpoint, U.Class, PropertySet):
    """Conventions for the creation, interpretation and use of an architecture view to frame one or more concerns that governs the creation of views."""
    _STEREO = "UAF::Summary and Overview::Viewpoint"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False
    _DECL = {
    # Relates the Viewpoint to the Concerns that the Viewpoint addresses.
    'concern': _Ref('concern', 'Concern', multi=True, lo=0, hi='*'),
    # The languages used to express the Viewpoint.
    'language': _Ref('language', str, multi=True, lo=0, hi='*'),
    # The methods employed in the development of the Viewpoint.
    'method': _Ref('method', str, multi=True, lo=0, hi='*'),
    # The purpose of the Viewpoint.
    'purpose': _Ref('purpose', str),
    # Relates the Viewpoint to the Stakeholders whose Concerns are being addressed by the Viewpoint.
    'stakeholder': _Ref('stakeholder', 'Stakeholder', multi=True, lo=0, hi='*'),
    }

class VisionStatement(MeasurableElement, U.Comment):
    """A type of comment that describes the future state of the enterprise, without regard to how it is to be achieved. http://www.omg.org/spec/BMM/1.3/"""
    _STEREO = "UAF::Taxonomy::VisionStatement"
    _BASE_METACLASSES = ("Comment",)
    _ABSTRACT = False
    CONSTRAINTS = (
        ("VisionStatement.ownedAttribute",
         "Values for annotatedElement metaproperty must be stereotyped «EnterpriseVision» or its s"
         "pecializations."
        ),
    )

class WholeLifeConfiguration(sysml.Block, U.Class, PropertySet):
    """A set of VersionedElements, e.g. Services for a service provider or ResourcePerformers deployed for implementation."""
    _STEREO = "UAF::Roadmap::WholeLifeConfiguration"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False
    _DECL = {
    # Captures the kind of WholeLifeConfiguration.
    'kind': _Ref('kind', WholeLifeConfigurationKind),
    }

class WholeLifeEnterprise(ActualEnterprisePhase, U.InstanceSpecification):
    """A WholeLifeEnterprise is a purposeful endeavor of any size involving people, organizations and supporting systems. It is made up of TemporalParts and StructuralParts."""
    _STEREO = "UAF::Taxonomy::WholeLifeEnterprise"
    _BASE_METACLASSES = ("InstanceSpecification",)
    _ABSTRACT = False

# ---------------------------------------------------------------------------
# post-import assembly (mirror of uml25._finish for stereotype classes)
# ---------------------------------------------------------------------------
_STEREOTYPES = [UAFElement, Achiever, MeasurableElement, Achieves, AffectableElement, Activity, ActualState, ActualPropertySet, ActualCondition, ActualEffect, ActualStrategicPhase, ActualEnduringTask, ActualEnterprisePhase, ActualEnvironment, ActualLocation, ActualMeasurement, ActualMeasurementSet, Stakeholder, SubjectOfResourceConstraint, CapableElement, ActualResource, ActualOrganizationalResource, ActualResponsibleResource, ActualOrganization, ActualResourceRole, ActualOrganizationRole, ActualOutcome, ActualPerson, ActualPost, ActualProject, ActualProjectMilestone, ActualProjectMilestoneRole, ActualProjectRole, ActualResourceRelationship, ActualResponsibility, ActualRisk, ActualService, Affects, AffectsInContext, Alias, ArbitraryConnector, ArchitecturalDescription, ArchitecturalReference, Architecture, Metadata, ArchitectureMetadata, ConceptItem, PropertySet, LocationHolder, SubjectOfSecurityConstraint, Asset, AssetRole, Desirer, PhaseableElement, SubjectOfStrategicConstraint, Capability, ResourceAsset, Resource, ResourceExchangeItem, VersionedElement, SubjectOfForecast, OperationalExchangeItem, ServiceExchangeItem, StrategicExchangeItem, ResourcePerformer, ResourceArchitecture, CapabilityConfiguration, CapabilityRole, MotivationalElement, Challenge, Exchange, ResourceExchange, Command, ComparesTo, Competence, CompetenceForRole, CompetenceToConduct, ConceptRole, Concern, Condition, Control, Creates, Definition, Desires, Driver, Effect, Enables, SecurityControl, EnhancedSecurityControl, Enhances, EnterpriseGoal, EnterpriseMission, EnterpriseObjective, EnterpriseVision, Environment, EnvironmentProperty, EvokedBy, Exhibits, FieldedCapability, FillsPost, Forecast, Function, FunctionAction, FunctionEdge, FunctionControlFlow, FunctionObjectFlow, GeoPoliticalExtentType, GovernedBy, HighLevelOperationalConcept, ISO8601DateTime, ImpactedBy, Implements, Information, SubjectOfOperationalConstraint, InformationModel, IsCapableToPerform, OperationalAsset, OperationalAgent, OperationalPerformer, KnownResource, Location, MapsToCapability, MapsToGoal, Measurement, MeasurementSet, Sequence, MilestoneDependency, Mitigates, MotivatedBy, PhysicalResource, NaturalResource, OperationalActivity, OperationalActivityAction, OperationalActivityEdge, OperationalArchitecture, OperationalConnector, Rule, OperationalConstraint, OperationalControlFlow, OperationalExchange, OperationalInformation, OperationalInformationRole, OperationalInterface, OperationalMessage, OperationalMethod, OperationalMitigation, OperationalObjectFlow, OperationalParameter, OperationalPort, OperationalRole, OperationalSignal, OperationalSignalProperty, OperationalStateDescription, Opportunity, OrganizationalResource, Organization, OrganizationInPhase, OwnsProcess, OwnsRisk, OwnsRiskInContext, OwnsValue, PerformsInContext, Person, Phases, Post, PresentedBy, ProblemDomain, Project, ProjectActivity, ProjectActivityAction, ProjectMilestone, ProjectMilestoneRole, ResourceRole, ProjectRole, ProjectSequence, ProjectStatus, ProjectTheme, Protects, ProtectsInContext, Standard, Protocol, ProtocolImplementation, ProtocolLayer, ProtocolStack, ProvidedServiceLevel, ProvidesCompetence, RequiredServiceLevel, RequiresCompetence, ResourceArtifact, ResourceConnector, ResourceConstraint, ResourceInformation, ResourceInformationRole, ResourceInterface, ResourceMessage, ResourceMethod, ResourceMitigation, ResourceParameter, ResourcePort, ResourceService, ResourceServiceInterface, ResourceSignal, ResourceSignalProperty, ResourceStateDescription, Responsibility, ResponsibleFor, Risk, SameAs, SecurityConstraint, SecurityControlFamily, SecurityEnclave, SecurityProcess, SecurityProcessAction, SecurityRisk, Service, ServiceArchitecture, ServiceConnector, ServiceContract, ServiceFunctionEdge, ServiceControlFlow, ServiceExchange, ServiceFunction, ServiceFunctionAction, ServiceInterface, ServiceMessage, ServiceMethod, ServiceObjectFlow, ServiceParameter, ServicePolicy, ServicePort, ServiceRole, ServiceSignal, ServiceSignalProperty, ServiceStateDescription, Software, StandardOperationalActivity, StatusIndicators, StrategicAsset, StrategicConstraint, StrategicExchange, StrategicInformation, StrategicPhase, StructuralPart, Supports, System, Technology, TemporalPart, ValueItem, ValueStream, VersionOfConfiguration, VersionSuccession, View, Viewpoint, VisionStatement, WholeLifeConfiguration, WholeLifeEnterprise]
_EXTENSIONS = {
    "Achiever": (("InstanceSpecification", True),),
    "Achieves": (("Dependency", True),),
    "Activity": (("Activity", True),),
    "ActualCondition": (("InstanceSpecification", True),),
    "ActualEffect": (("InstanceSpecification", True),),
    "ActualEnduringTask": (("InstanceSpecification", True),),
    "ActualEnterprisePhase": (("InstanceSpecification", True),),
    "ActualEnvironment": (("InstanceSpecification", True),),
    "ActualLocation": (("InstanceSpecification", True),),
    "ActualMeasurement": (("Slot", True),),
    "ActualMeasurementSet": (("InstanceSpecification", True),),
    "ActualOrganization": (("InstanceSpecification", True),),
    "ActualOrganizationRole": (("Slot", True),),
    "ActualOrganizationalResource": (("InstanceSpecification", True),),
    "ActualOutcome": (("InstanceSpecification", True),),
    "ActualPerson": (("InstanceSpecification", True),),
    "ActualPost": (("InstanceSpecification", True),),
    "ActualProject": (("InstanceSpecification", True),),
    "ActualProjectMilestone": (("InstanceSpecification", True),),
    "ActualProjectMilestoneRole": (("Slot", True),),
    "ActualProjectRole": (("Slot", True),),
    "ActualPropertySet": (("InstanceSpecification", True),),
    "ActualResource": (("InstanceSpecification", True),),
    "ActualResourceRelationship": (("InformationFlow", True),),
    "ActualResourceRole": (("Slot", True),),
    "ActualResponsibility": (("InstanceSpecification", True),),
    "ActualResponsibleResource": (("InstanceSpecification", True),),
    "ActualRisk": (("InstanceSpecification", True),),
    "ActualService": (("InstanceSpecification", True),),
    "ActualState": (("Element", True),),
    "ActualStrategicPhase": (("InstanceSpecification", True),),
    "AffectableElement": (("Element", True),),
    "Affects": (("Dependency", True),),
    "AffectsInContext": (("Dependency", True),),
    "Alias": (("Comment", True),),
    "ArbitraryConnector": (("Dependency", True),),
    "ArchitecturalDescription": (("Package", True),),
    "ArchitecturalReference": (("Dependency", True),),
    "Architecture": (("Class", True),),
    "ArchitectureMetadata": (("Comment", True),),
    "Asset": (("Class", True),),
    "AssetRole": (("Element", True),),
    "Capability": (("Class", True),),
    "CapabilityConfiguration": (("Class", True),),
    "CapabilityRole": (("Property", True),),
    "CapableElement": (("Element", True),),
    "Challenge": (("Class", True),),
    "Command": (("InformationFlow", True),),
    "ComparesTo": (("Abstraction", True),),
    "Competence": (("Class", True),),
    "CompetenceForRole": (("Abstraction", True),),
    "CompetenceToConduct": (("Abstraction", True),),
    "ConceptItem": (("Element", True),),
    "ConceptRole": (("Property", True),),
    "Concern": (("Class", True),),
    "Condition": (("DataType", True),),
    "Control": (("InformationFlow", True),),
    "Creates": (("Dependency", True),),
    "Definition": (("Comment", True),),
    "Desirer": (("Element", True),),
    "Desires": (("Dependency", True),),
    "Driver": (("Class", True),),
    "Effect": (("Class", True),),
    "Enables": (("Dependency", True),),
    "EnhancedSecurityControl": (("Class", True),),
    "Enhances": (("Abstraction", True),),
    "EnterpriseGoal": (("Class", True),),
    "EnterpriseMission": (("InstanceSpecification", True),),
    "EnterpriseObjective": (("Class", True),),
    "EnterpriseVision": (("Class", True),),
    "Environment": (("DataType", True),),
    "EnvironmentProperty": (("Property", True),),
    "EvokedBy": (("Dependency", True),),
    "Exchange": (("InformationFlow", True),),
    "Exhibits": (("Abstraction", True),),
    "FieldedCapability": (("InstanceSpecification", True),),
    "FillsPost": (("Abstraction", True),),
    "Forecast": (("Dependency", True),),
    "Function": (("Activity", True),),
    "FunctionAction": (("CallBehaviorAction", True),),
    "FunctionControlFlow": (("ControlFlow", True),),
    "FunctionEdge": (("ActivityEdge", True),),
    "FunctionObjectFlow": (("ObjectFlow", True),),
    "GeoPoliticalExtentType": (("DataType", True),),
    "GovernedBy": (("Abstraction", True),),
    "HighLevelOperationalConcept": (("Class", True),),
    "ISO8601DateTime": (("LiteralString", True),),
    "ImpactedBy": (("Abstraction", True),),
    "Implements": (("Abstraction", True),),
    "Information": (("Comment", True),),
    "InformationModel": (("Package", True),),
    "IsCapableToPerform": (("Abstraction", True),),
    "KnownResource": (("Class", True),),
    "Location": (("DataType", True),),
    "LocationHolder": (("Element", True),),
    "MapsToCapability": (("Abstraction", True),),
    "MapsToGoal": (("Element", True),),
    "MeasurableElement": (("Element", True),),
    "Measurement": (("Property", True),),
    "MeasurementSet": (("DataType", True),),
    "Metadata": (("Comment", True),),
    "MilestoneDependency": (("Dependency", True),),
    "Mitigates": (("Dependency", True),),
    "MotivatedBy": (("Dependency", True),),
    "MotivationalElement": (("Class", True),),
    "NaturalResource": (("Class", True),),
    "OperationalActivity": (("Activity", True),),
    "OperationalActivityAction": (("CallBehaviorAction", True),),
    "OperationalActivityEdge": (("ActivityEdge", True),),
    "OperationalAgent": (("Class", True),),
    "OperationalArchitecture": (("Class", True),),
    "OperationalAsset": (("Class", True),),
    "OperationalConnector": (("Connector", True),),
    "OperationalConstraint": (("Constraint", True),),
    "OperationalControlFlow": (("ControlFlow", True),),
    "OperationalExchange": (("InformationFlow", True),),
    "OperationalInformation": (("Class", True),),
    "OperationalInformationRole": (("Property", True),),
    "OperationalInterface": (("Class", True),),
    "OperationalMessage": (("Message", True),),
    "OperationalMethod": (("Operation", True),),
    "OperationalMitigation": (("Class", True),),
    "OperationalObjectFlow": (("ObjectFlow", True),),
    "OperationalParameter": (("Parameter", True),),
    "OperationalPerformer": (("Class", True),),
    "OperationalPort": (("Port", True),),
    "OperationalRole": (("Property", True),),
    "OperationalSignal": (("Signal", True),),
    "OperationalSignalProperty": (("Property", True),),
    "OperationalStateDescription": (("StateMachine", True),),
    "Opportunity": (("Class", True),),
    "Organization": (("Class", True),),
    "OrganizationInPhase": (("Abstraction", True),),
    "OrganizationalResource": (("Class", True),),
    "OwnsProcess": (("Abstraction", True),),
    "OwnsRisk": (("Abstraction", True),),
    "OwnsRiskInContext": (("Abstraction", True),),
    "OwnsValue": (("Abstraction", True),),
    "PerformsInContext": (("Abstraction", True),),
    "Person": (("Class", True),),
    "PhaseableElement": (("Element", True),),
    "Phases": (("Abstraction", True),),
    "PhysicalResource": (("Class", True),),
    "Post": (("Class", True),),
    "PresentedBy": (("Dependency", True),),
    "ProblemDomain": (("Property", True),),
    "Project": (("Class", True),),
    "ProjectActivity": (("Activity", True),),
    "ProjectActivityAction": (("CallBehaviorAction", True),),
    "ProjectMilestone": (("Class", True),),
    "ProjectMilestoneRole": (("Property", True),),
    "ProjectRole": (("Property", True),),
    "ProjectSequence": (("Dependency", True),),
    "ProjectStatus": (("Slot", True),),
    "ProjectTheme": (("Property", True),),
    "PropertySet": (("Element", True),),
    "Protects": (("Dependency", True),),
    "ProtectsInContext": (("Dependency", True),),
    "Protocol": (("Class", True),),
    "ProtocolImplementation": (("Element", True),),
    "ProtocolLayer": (("Property", True),),
    "ProtocolStack": (("Class", True),),
    "ProvidedServiceLevel": (("InstanceSpecification", True),),
    "ProvidesCompetence": (("Dependency", True),),
    "RequiredServiceLevel": (("InstanceSpecification", True),),
    "RequiresCompetence": (("Abstraction", True),),
    "ResourceArchitecture": (("Class", True),),
    "ResourceArtifact": (("Class", True),),
    "ResourceAsset": (("Class", True),),
    "ResourceConnector": (("Connector", True),),
    "ResourceConstraint": (("Constraint", True),),
    "ResourceExchange": (("InformationFlow", True),),
    "ResourceInformation": (("Class", True),),
    "ResourceInformationRole": (("Element", True),),
    "ResourceInterface": (("Class", True),),
    "ResourceMessage": (("Message", True),),
    "ResourceMethod": (("Operation", True),),
    "ResourceMitigation": (("Class", True),),
    "ResourceParameter": (("Parameter", True),),
    "ResourcePerformer": (("Class", True),),
    "ResourcePort": (("Port", True),),
    "ResourceRole": (("Property", True),),
    "ResourceService": (("Class", True),),
    "ResourceServiceInterface": (("Class", True),),
    "ResourceSignal": (("Signal", True),),
    "ResourceSignalProperty": (("Property", True),),
    "ResourceStateDescription": (("StateMachine", True),),
    "Responsibility": (("Class", True),),
    "ResponsibleFor": (("Abstraction", True),),
    "Risk": (("Constraint", True),),
    "Rule": (("Constraint", True),),
    "SameAs": (("Dependency", True),),
    "SecurityConstraint": (("Constraint", True),),
    "SecurityControl": (("Class", True),),
    "SecurityControlFamily": (("Class", True),),
    "SecurityEnclave": (("Class", True),),
    "SecurityProcess": (("Activity", True),),
    "SecurityProcessAction": (("CallBehaviorAction", True),),
    "SecurityRisk": (("Class", True),),
    "Sequence": (("Dependency", True),),
    "Service": (("Class", True),),
    "ServiceArchitecture": (("Class", True),),
    "ServiceConnector": (("Connector", True),),
    "ServiceContract": (("Constraint", True),),
    "ServiceControlFlow": (("ControlFlow", True),),
    "ServiceExchange": (("InformationFlow", True),),
    "ServiceFunction": (("Activity", True),),
    "ServiceFunctionAction": (("CallBehaviorAction", True),),
    "ServiceFunctionEdge": (("ActivityEdge", True),),
    "ServiceInterface": (("Class", True),),
    "ServiceMessage": (("Message", True),),
    "ServiceMethod": (("Operation", True),),
    "ServiceObjectFlow": (("ObjectFlow", True),),
    "ServiceParameter": (("Parameter", True),),
    "ServicePolicy": (("Constraint", True),),
    "ServicePort": (("Port", True),),
    "ServiceRole": (("Property", True),),
    "ServiceSignal": (("Signal", True),),
    "ServiceSignalProperty": (("Property", True),),
    "ServiceStateDescription": (("StateMachine", True),),
    "Software": (("Class", True),),
    "Stakeholder": (("Element", True),),
    "Standard": (("Class", True),),
    "StandardOperationalActivity": (("Activity", True),),
    "StatusIndicators": (("Enumeration", True),),
    "StrategicAsset": (("Class", True),),
    "StrategicConstraint": (("Constraint", True),),
    "StrategicExchange": (("InformationFlow", True),),
    "StrategicExchangeItem": (("Element", True),),
    "StrategicInformation": (("Class", True),),
    "StrategicPhase": (("Class", True),),
    "StructuralPart": (("Property", True),),
    "SubjectOfForecast": (("Class", True),),
    "SubjectOfOperationalConstraint": (("Element", True),),
    "SubjectOfResourceConstraint": (("Element", True),),
    "SubjectOfSecurityConstraint": (("Element", True),),
    "SubjectOfStrategicConstraint": (("Element", True),),
    "Supports": (("Abstraction", True),),
    "System": (("Class", True),),
    "Technology": (("Class", True),),
    "TemporalPart": (("Property", True),),
    "UAFElement": (("Element", True),),
    "ValueItem": (("DataType", True),),
    "ValueStream": (("InstanceSpecification", True),),
    "VersionOfConfiguration": (("Property", True),),
    "VersionSuccession": (("Dependency", True),),
    "VersionedElement": (("Class", True),),
    "View": (("Class", True),),
    "Viewpoint": (("Class", True),),
    "VisionStatement": (("Comment", True),),
    "WholeLifeConfiguration": (("Class", True),),
    "WholeLifeEnterprise": (("InstanceSpecification", True),),
}

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

