"""BPMN 2.0.2 metamodel classes generated from the OMG CMOF XMI.

137 classes, 471 attributes (including synthesized
association back-refs), 193 associations, 9 enumerations, 28 literals (metadata).
Source: https://www.omg.org/spec/BPMN/20100501/BPMN20.cmof
(OMG BPMN 2.0.2). CMOF dialect: superClass attributes, memberEnd
name-pairs, href-typed primitives. The CMOF carries no OCL - BPMN
constraints are normative prose in the spec. Reuses gen.uml25's
_Ref/_RefList descriptors (their wiring hooks are UML-scoped and
no-op here); BPMN classes are deliberately NOT UML Elements.
"""
from __future__ import annotations

import enum as _enum

from gen.uml25 import _Ref  # noqa: F401  (descriptor machinery)


class _MOFBase:
    """Common base of all BPMN classes (mirrors gen.uml25._Element
    mechanics: _vals storage, _union reads, add() helper - without
    UML composite-ownership wiring)."""
    _DECL: dict = {}
    _UNIONS: dict = {}
    _ABSTRACT = False

    def __init__(self, **kw):
        if type(self)._ABSTRACT:
            raise TypeError(
                f'{type(self).__name__} is abstract in the BPMN 2.0.2'
                f' metamodel; instantiate a concrete subclass.')
        self._vals = {}
        self._owner = None
        self._namespace = None
        self._wiring = False
        for k, v in kw.items():
            if k not in self._props:
                raise TypeError(
                f'{type(self).__name__} has no property {k!r}')
            setattr(self, k, v)

    def _union(self, name):
        """Derived-union read: values of properties that subset it."""
        out, seen = [], set()
        for cls in type(self).__mro__:
            for contrib in getattr(cls, '_UNIONS', {}).get(name, ()):
                d = self._props.get(contrib)
                if d is None or d.union:
                    continue
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
        for v in values:
            lst.append(v)

    def __repr__(self):
        n = self._vals.get('name')
        if isinstance(n, str) and n:
            return f'<{type(self).__name__} {n!r}>'
        return f'<{type(self).__name__} #{id(self):x}>'

class AdHocOrdering(_enum.Enum):
    Parallel = "Parallel"
    Sequential = "Sequential"

class AssociationDirection(_enum.Enum):
    None_ = "None"
    One = "One"
    Both = "Both"

class ChoreographyLoopType(_enum.Enum):
    None_ = "None"
    Standard = "Standard"
    MultiInstanceSequential = "MultiInstanceSequential"
    MultiInstanceParallel = "MultiInstanceParallel"

class EventBasedGatewayType(_enum.Enum):
    Parallel = "Parallel"
    Exclusive = "Exclusive"

class GatewayDirection(_enum.Enum):
    Unspecified = "Unspecified"
    Converging = "Converging"
    Diverging = "Diverging"
    Mixed = "Mixed"

class ItemKind(_enum.Enum):
    Physical = "Physical"
    Information = "Information"

class MultiInstanceBehavior(_enum.Enum):
    None_ = "None"
    One = "One"
    All = "All"
    Complex = "Complex"

class ProcessType(_enum.Enum):
    None_ = "None"
    Public = "Public"
    Private = "Private"

class RelationshipDirection(_enum.Enum):
    None_ = "None"
    Forward = "Forward"
    Backward = "Backward"
    Both = "Both"


class BaseElement(_MOFBase):
    _ABSTRACT = True
    # association end of A_partitionElement_lane (opposite of Lane.partitionElement)
    # association end of A_sourceRef_outgoing_association (opposite of Association.sourceRef)
    # association end of A_targetRef_incoming_association (opposite of Association.targetRef)
    _DECL = {
    'id': _Ref('id', str),
    'extensionDefinitions': _Ref('extensionDefinitions', "ExtensionDefinition", multi=True, lo=0, hi='*', assoc="A_extensionDefinitions_baseElement"),
    'extensionValues': _Ref('extensionValues', "ExtensionAttributeValue", multi=True, lo=0, hi='*', composite=True, assoc="A_extensionValues_baseElement"),
    'documentation': _Ref('documentation', "Documentation", multi=True, lo=0, hi='*', composite=True, assoc="A_documentation_baseElement"),
    'lane': _Ref('lane', "Lane", assoc="A_partitionElement_lane"),
    'outgoing': _Ref('outgoing', "Association", multi=True, lo=0, hi='*', assoc="A_sourceRef_outgoing_association"),
    'incoming': _Ref('incoming', "Association", multi=True, lo=0, hi='*', assoc="A_targetRef_incoming_association"),
    }
    _OPPS = {
        'extensionDefinitions': ('baseElement',),
        'extensionValues': ('baseElement',),
        'documentation': ('baseElement',),
        'lane': ('partitionElement', 'partitionElementRef'),
        'outgoing': ('sourceRef',),
        'incoming': ('targetRef',),
    }

class FlowElement(BaseElement):
    _ABSTRACT = True
    # association end of A_flowElements_container (opposite of FlowElementsContainer.flowElements)
    _DECL = {
    'name': _Ref('name', str),
    'auditing': _Ref('auditing', "Auditing", composite=True, assoc="A_auditing_flowElement"),
    'monitoring': _Ref('monitoring', "Monitoring", composite=True, assoc="A_monitoring_flowElement"),
    'categoryValueRef': _Ref('categoryValueRef', "CategoryValue", multi=True, lo=0, hi='*', assoc="A_categorizedFlowElements_categoryValueRef"),
    'container': _Ref('container', "FlowElementsContainer", assoc="A_flowElements_container"),
    }
    _OPPS = {
        'auditing': ('flowElement',),
        'monitoring': ('flowElement',),
        'categoryValueRef': ('categorizedFlowElements',),
        'container': ('flowElements',),
    }

class FlowNode(FlowElement):
    _ABSTRACT = True
    _DECL = {
    'outgoing': _Ref('outgoing', "SequenceFlow", multi=True, lo=0, hi='*', assoc="A_sourceRef_outgoing_flow"),
    'incoming': _Ref('incoming', "SequenceFlow", multi=True, lo=0, hi='*', assoc="A_targetRef_incoming_flow"),
    'lanes': _Ref('lanes', "Lane", multi=True, lo=0, hi='*', derived=True, assoc="A_flowNodeRefs_lanes"),
    }
    _OPPS = {
        'outgoing': ('sourceRef',),
        'incoming': ('targetRef',),
        'lanes': ('flowNodeRefs',),
    }

class Activity(FlowNode):
    _ABSTRACT = True
    # default: 'false'
    # default: '1'
    # default: '1'
    # association end of A_activityRef_compensateEventDefinition (opposite of CompensateEventDefinition.activityRef)
    _DECL = {
    'isForCompensation': _Ref('isForCompensation', bool),
    'loopCharacteristics': _Ref('loopCharacteristics', "LoopCharacteristics", composite=True, assoc="A_loopCharacteristics_activity"),
    'resources': _Ref('resources', "ResourceRole", multi=True, lo=0, hi='*', composite=True, assoc="A_resources_activity"),
    'default': _Ref('default', "SequenceFlow", assoc="A_default_activity"),
    'properties': _Ref('properties', "Property", multi=True, lo=0, hi='*', composite=True, assoc="A_properties_activity"),
    'ioSpecification': _Ref('ioSpecification', "InputOutputSpecification", composite=True, assoc="A_ioSpecification_activity"),
    'boundaryEventRefs': _Ref('boundaryEventRefs', "BoundaryEvent", multi=True, lo=0, hi='*', assoc="A_boundaryEventRefs_attachedToRef"),
    'dataInputAssociations': _Ref('dataInputAssociations', "DataInputAssociation", multi=True, lo=0, hi='*', composite=True, assoc="A_dataInputAssociations_activity"),
    'dataOutputAssociations': _Ref('dataOutputAssociations', "DataOutputAssociation", multi=True, lo=0, hi='*', composite=True, assoc="A_dataOutputAssociations_activity"),
    'startQuantity': _Ref('startQuantity', int),
    'completionQuantity': _Ref('completionQuantity', int),
    'compensateEventDefinition': _Ref('compensateEventDefinition', "CompensateEventDefinition", multi=True, lo=0, hi='*', assoc="A_activityRef_compensateEventDefinition"),
    }
    _OPPS = {
        'loopCharacteristics': ('activity',),
        'resources': ('activity',),
        'default': ('activity',),
        'properties': ('activity',),
        'ioSpecification': ('activity',),
        'boundaryEventRefs': ('attachedToRef',),
        'dataInputAssociations': ('activity',),
        'dataOutputAssociations': ('activity',),
        'compensateEventDefinition': ('activityRef',),
    }

class FlowElementsContainer(BaseElement):
    _ABSTRACT = True
    _DECL = {
    'flowElements': _Ref('flowElements', "FlowElement", multi=True, lo=0, hi='*', composite=True, assoc="A_flowElements_container"),
    'laneSets': _Ref('laneSets', "LaneSet", multi=True, lo=0, hi='*', composite=True, assoc="A_laneSets_flowElementsContainer"),
    }
    _OPPS = {
        'flowElements': ('container',),
        'laneSets': ('flowElementsContainer',),
    }

class SubProcess(Activity, FlowElementsContainer):
    _ABSTRACT = False
    # default: 'false'
    _DECL = {
    'triggeredByEvent': _Ref('triggeredByEvent', bool),
    'artifacts': _Ref('artifacts', "Artifact", multi=True, lo=0, hi='*', composite=True, assoc="A_artifacts_subProcess"),
    }
    _OPPS = {
        'artifacts': ('subProcess',),
    }

class AdHocSubProcess(SubProcess):
    _ABSTRACT = False
    # default: 'true'
    _DECL = {
    'completionCondition': _Ref('completionCondition', "Expression", composite=True, assoc="A_completionCondition_adHocSubProcess"),
    'ordering': _Ref('ordering', "AdHocOrdering"),
    'cancelRemainingInstances': _Ref('cancelRemainingInstances', bool),
    }
    _OPPS = {
        'completionCondition': ('adHocSubProcess',),
    }

class Artifact(BaseElement):
    _ABSTRACT = True
    # association end of A_artifacts_process (opposite of Process.artifacts)
    # association end of A_artifacts_collaboration (opposite of Collaboration.artifacts)
    # association end of A_artifacts_subChoreography (opposite of SubChoreography.artifacts)
    # association end of A_artifacts_subProcess (opposite of SubProcess.artifacts)
    _DECL = {
    'process': _Ref('process', "Process", assoc="A_artifacts_process"),
    'collaboration': _Ref('collaboration', "Collaboration", assoc="A_artifacts_collaboration"),
    'subChoreography': _Ref('subChoreography', "SubChoreography", assoc="A_artifacts_subChoreography"),
    'subProcess': _Ref('subProcess', "SubProcess", assoc="A_artifacts_subProcess"),
    }
    _OPPS = {
        'process': ('artifacts',),
        'collaboration': ('artifacts',),
        'subChoreography': ('artifacts',),
        'subProcess': ('artifacts',),
    }

class Assignment(BaseElement):
    _ABSTRACT = False
    # association end of A_assignment_dataAssociation (opposite of DataAssociation.assignment)
    _DECL = {
    'from': _Ref('from', "Expression", composite=True, assoc="A_from_assignment"),
    'to': _Ref('to', "Expression", composite=True, assoc="A_to_assignment"),
    'dataAssociation': _Ref('dataAssociation', "DataAssociation", assoc="A_assignment_dataAssociation"),
    }
    _OPPS = {
        'from': ('assignment',),
        'to': ('assignment',),
        'dataAssociation': ('assignment',),
    }

class Association(Artifact):
    _ABSTRACT = False
    _DECL = {
    'associationDirection': _Ref('associationDirection', "AssociationDirection"),
    'sourceRef': _Ref('sourceRef', "BaseElement", assoc="A_sourceRef_outgoing_association"),
    'targetRef': _Ref('targetRef', "BaseElement", assoc="A_targetRef_incoming_association"),
    }
    _OPPS = {
        'sourceRef': ('outgoing',),
        'targetRef': ('incoming',),
    }

class Auditing(BaseElement):
    _ABSTRACT = False
    # association end of A_auditing_process (opposite of Process.auditing)
    # association end of A_auditing_flowElement (opposite of FlowElement.auditing)
    _DECL = {
    'process': _Ref('process', "Process", assoc="A_auditing_process"),
    'flowElement': _Ref('flowElement', "FlowElement", assoc="A_auditing_flowElement"),
    }
    _OPPS = {
        'process': ('auditing',),
        'flowElement': ('auditing',),
    }

class InteractionNode(_MOFBase):
    _ABSTRACT = True
    # association end of A_targetRef_messageFlow (opposite of MessageFlow.targetRef)
    _DECL = {
    'incomingConversationLinks': _Ref('incomingConversationLinks', "ConversationLink", multi=True, lo=0, hi='*', derived=True, assoc="A_targetRef_incomingConversationLinks"),
    'outgoingConversationLinks': _Ref('outgoingConversationLinks', "ConversationLink", multi=True, lo=0, hi='*', derived=True, assoc="A_sourceRef_outgoingConversationLinks"),
    'messageFlow': _Ref('messageFlow', "MessageFlow", multi=True, lo=0, hi='*', assoc="A_targetRef_messageFlow"),
    }
    _OPPS = {
        'incomingConversationLinks': ('targetRef',),
        'outgoingConversationLinks': ('sourceRef',),
        'messageFlow': ('targetRef', 'sourceRef'),
    }

class Event(FlowNode, InteractionNode):
    _ABSTRACT = True
    _DECL = {
    'properties': _Ref('properties', "Property", multi=True, lo=0, hi='*', composite=True, assoc="A_properties_event"),
    }
    _OPPS = {
        'properties': ('event',),
    }

class CatchEvent(Event):
    _ABSTRACT = True
    _DECL = {
    'parallelMultiple': _Ref('parallelMultiple', bool),
    'outputSet': _Ref('outputSet', "OutputSet", composite=True, assoc="A_outputSet_catchEvent"),
    'eventDefinitionRefs': _Ref('eventDefinitionRefs', "EventDefinition", multi=True, lo=0, hi='*', assoc="A_eventDefinitionRefs_catchEvent"),
    'dataOutputAssociation': _Ref('dataOutputAssociation', "DataOutputAssociation", multi=True, lo=0, hi='*', composite=True, assoc="A_dataOutputAssociation_catchEvent"),
    'dataOutputs': _Ref('dataOutputs', "DataOutput", multi=True, lo=0, hi='*', composite=True, assoc="A_dataOutputs_catchEvent"),
    'eventDefinitions': _Ref('eventDefinitions', "EventDefinition", multi=True, lo=0, hi='*', composite=True, assoc="A_eventDefinitions_catchEvent"),
    }
    _OPPS = {
        'outputSet': ('catchEvent',),
        'eventDefinitionRefs': ('catchEvent',),
        'dataOutputAssociation': ('catchEvent',),
        'dataOutputs': ('catchEvent',),
        'eventDefinitions': ('catchEvent',),
    }

class BoundaryEvent(CatchEvent):
    _ABSTRACT = False
    # default: 'true'
    _DECL = {
    'cancelActivity': _Ref('cancelActivity', bool),
    'attachedToRef': _Ref('attachedToRef', "Activity", assoc="A_boundaryEventRefs_attachedToRef"),
    }
    _OPPS = {
        'attachedToRef': ('boundaryEventRefs',),
    }

class Task(Activity, InteractionNode):
    _ABSTRACT = False

class BusinessRuleTask(Task):
    _ABSTRACT = False
    _DECL = {
    'implementation': _Ref('implementation', str),
    }

class CallActivity(Activity):
    _ABSTRACT = False
    _DECL = {
    'calledElementRef': _Ref('calledElementRef', "CallableElement", assoc="A_calledElementRef_callActivity"),
    }
    _OPPS = {
        'calledElementRef': ('callActivity',),
    }

class ChoreographyActivity(FlowNode):
    _ABSTRACT = True
    # default: 'None'
    _DECL = {
    'participantRefs': _Ref('participantRefs', "Participant", multi=True, lo=2, hi='*', assoc="A_participantRefs_choreographyActivity"),
    'initiatingParticipantRef': _Ref('initiatingParticipantRef', "Participant", assoc="A_initiatingParticipantRef_choreographyActivity"),
    'correlationKeys': _Ref('correlationKeys', "CorrelationKey", multi=True, lo=0, hi='*', composite=True, assoc="A_correlationKeys_choreographyActivity"),
    'loopType': _Ref('loopType', "ChoreographyLoopType"),
    }
    _OPPS = {
        'participantRefs': ('choreographyActivity',),
        'initiatingParticipantRef': ('choreographyActivity',),
        'correlationKeys': ('choreographyActivity',),
    }

class CallChoreography(ChoreographyActivity):
    _ABSTRACT = False
    _DECL = {
    'calledChoreographyRef': _Ref('calledChoreographyRef', "Choreography", assoc="A_calledChoreographyRef_callChoreographyActivity"),
    'participantAssociations': _Ref('participantAssociations', "ParticipantAssociation", multi=True, lo=0, hi='*', composite=True, assoc="A_participantAssociations_callChoreographyActivity"),
    }
    _OPPS = {
        'calledChoreographyRef': ('callChoreographyActivity',),
        'participantAssociations': ('callChoreographyActivity',),
    }

class ConversationNode(InteractionNode, BaseElement):
    _ABSTRACT = True
    # association end of A_innerConversationNodeRef_conversationAssociation (opposite of ConversationAssociation.innerConversationNodeRef)
    # association end of A_conversationNodes_subConversation (opposite of SubConversation.conversationNodes)
    # association end of A_conversations_collaboration (opposite of Collaboration.conversations)
    _DECL = {
    'name': _Ref('name', str),
    'participantRefs': _Ref('participantRefs', "Participant", multi=True, lo=2, hi='*', assoc="A_participantRefs_conversationNode"),
    'messageFlowRefs': _Ref('messageFlowRefs', "MessageFlow", multi=True, lo=0, hi='*', assoc="A_messageFlowRefs_communication"),
    'correlationKeys': _Ref('correlationKeys', "CorrelationKey", multi=True, lo=0, hi='*', composite=True, assoc="A_correlationKeys_conversationNode"),
    'conversationAssociation': _Ref('conversationAssociation', "ConversationAssociation", multi=True, lo=0, hi='*', assoc="A_innerConversationNodeRef_conversationAssociation"),
    'subConversation': _Ref('subConversation', "SubConversation", assoc="A_conversationNodes_subConversation"),
    'collaboration': _Ref('collaboration', "Collaboration", assoc="A_conversations_collaboration"),
    }
    _OPPS = {
        'participantRefs': ('conversationNode',),
        'messageFlowRefs': ('communication',),
        'correlationKeys': ('conversationNode',),
        'conversationAssociation': ('innerConversationNodeRef', 'outerConversationNodeRef'),
        'subConversation': ('conversationNodes',),
        'collaboration': ('conversations',),
    }

class CallConversation(ConversationNode):
    _ABSTRACT = False
    _DECL = {
    'calledCollaborationRef': _Ref('calledCollaborationRef', "Collaboration", assoc="A_calledCollaborationRef_callConversation"),
    'participantAssociations': _Ref('participantAssociations', "ParticipantAssociation", multi=True, lo=0, hi='*', composite=True, assoc="A_participantAssociations_callConversation"),
    }
    _OPPS = {
        'calledCollaborationRef': ('callConversation',),
        'participantAssociations': ('callConversation',),
    }

class RootElement(BaseElement):
    _ABSTRACT = True
    # association end of A_rootElements_definition (opposite of Definitions.rootElements)
    _DECL = {
    'definition': _Ref('definition', "Definitions", assoc="A_rootElements_definition"),
    }
    _OPPS = {
        'definition': ('rootElements',),
    }

class CallableElement(RootElement):
    _ABSTRACT = True
    # association end of A_calledElementRef_callActivity (opposite of CallActivity.calledElementRef)
    _DECL = {
    'name': _Ref('name', str),
    'ioSpecification': _Ref('ioSpecification', "InputOutputSpecification", composite=True, assoc="A_ioSpecification_callableElement"),
    'supportedInterfaceRefs': _Ref('supportedInterfaceRefs', "Interface", multi=True, lo=0, hi='*', assoc="A_supportedInterfaceRefs_callableElements"),
    'ioBinding': _Ref('ioBinding', "InputOutputBinding", multi=True, lo=0, hi='*', composite=True, assoc="A_ioBinding_callableElement"),
    'callActivity': _Ref('callActivity', "CallActivity", multi=True, lo=0, hi='*', assoc="A_calledElementRef_callActivity"),
    }
    _OPPS = {
        'ioSpecification': ('callableElement',),
        'supportedInterfaceRefs': ('callableElements',),
        'ioBinding': ('callableElement',),
        'callActivity': ('calledElementRef',),
    }

class EventDefinition(RootElement):
    _ABSTRACT = True
    # association end of A_eventDefinitionRefs_throwEvent (opposite of ThrowEvent.eventDefinitionRefs)
    # association end of A_eventDefinitionRefs_catchEvent (opposite of CatchEvent.eventDefinitionRefs)
    # association end of A_noneBehaviorEventRef_multiInstanceLoopCharacteristics (opposite of MultiInstanceLoopCharacteristics.noneBehaviorEventRef)
    _DECL = {
    'throwEvent': _Ref('throwEvent', "ThrowEvent", multi=True, lo=0, hi='*', assoc="A_eventDefinitionRefs_throwEvent"),
    'catchEvent': _Ref('catchEvent', "CatchEvent", multi=True, lo=0, hi='*', assoc="A_eventDefinitionRefs_catchEvent"),
    'multiInstanceLoopCharacteristics': _Ref('multiInstanceLoopCharacteristics', "MultiInstanceLoopCharacteristics", multi=True, lo=0, hi='*', assoc="A_noneBehaviorEventRef_multiInstanceLoopCharacteristics"),
    }
    _OPPS = {
        'throwEvent': ('eventDefinitionRefs', 'eventDefinitions'),
        'catchEvent': ('eventDefinitionRefs', 'eventDefinitions'),
        'multiInstanceLoopCharacteristics': ('noneBehaviorEventRef', 'oneBehaviorEventRef'),
    }

class CancelEventDefinition(EventDefinition):
    _ABSTRACT = False

class Category(RootElement):
    _ABSTRACT = False
    _DECL = {
    'categoryValue': _Ref('categoryValue', "CategoryValue", multi=True, lo=0, hi='*', composite=True, assoc="A_categoryValue_category"),
    'name': _Ref('name', str),
    }
    _OPPS = {
        'categoryValue': ('category',),
    }

class CategoryValue(BaseElement):
    _ABSTRACT = False
    # association end of A_categoryValueRef_categoryValueRef (opposite of Group.categoryValueRef)
    # association end of A_categoryValue_category (opposite of Category.categoryValue)
    _DECL = {
    'categorizedFlowElements': _Ref('categorizedFlowElements', "FlowElement", multi=True, lo=0, hi='*', derived=True, assoc="A_categorizedFlowElements_categoryValueRef"),
    'value': _Ref('value', str),
    'categoryValueRef': _Ref('categoryValueRef', "Group", multi=True, lo=0, hi='*', assoc="A_categoryValueRef_categoryValueRef"),
    'category': _Ref('category', "Category", assoc="A_categoryValue_category"),
    }
    _OPPS = {
        'categorizedFlowElements': ('categoryValueRef',),
        'categoryValueRef': ('categoryValueRef',),
        'category': ('categoryValue',),
    }

class Collaboration(RootElement):
    _ABSTRACT = False
    # association end of A_definitionalCollaborationRef_process (opposite of Process.definitionalCollaborationRef)
    # association end of A_calledCollaborationRef_callConversation (opposite of CallConversation.calledCollaborationRef)
    _DECL = {
    'name': _Ref('name', str),
    'isClosed': _Ref('isClosed', bool),
    'choreographyRef': _Ref('choreographyRef', "Choreography", multi=True, lo=0, hi='*', assoc="A_choreographyRef_collaboration"),
    'artifacts': _Ref('artifacts', "Artifact", multi=True, lo=0, hi='*', composite=True, assoc="A_artifacts_collaboration"),
    'participantAssociations': _Ref('participantAssociations', "ParticipantAssociation", multi=True, lo=0, hi='*', composite=True, assoc="A_participantAssociations_collaboration"),
    'messageFlowAssociations': _Ref('messageFlowAssociations', "MessageFlowAssociation", multi=True, lo=0, hi='*', composite=True, assoc="A_messageFlowAssociations_collaboration"),
    'conversationAssociations': _Ref('conversationAssociations', "ConversationAssociation", composite=True, assoc="A_conversationAssociations_converstaionAssociations"),
    'participants': _Ref('participants', "Participant", multi=True, lo=0, hi='*', composite=True, assoc="A_participants_collaboration"),
    'messageFlows': _Ref('messageFlows', "MessageFlow", multi=True, lo=0, hi='*', composite=True, assoc="A_messageFlows_collaboration"),
    'correlationKeys': _Ref('correlationKeys', "CorrelationKey", multi=True, lo=0, hi='*', composite=True, assoc="A_correlationKeys_collaboration"),
    'conversations': _Ref('conversations', "ConversationNode", multi=True, lo=0, hi='*', composite=True, assoc="A_conversations_collaboration"),
    'conversationLinks': _Ref('conversationLinks', "ConversationLink", multi=True, lo=0, hi='*', composite=True, assoc="A_conversationLinks_collaboration"),
    'process': _Ref('process', "Process", multi=True, lo=0, hi='*', assoc="A_definitionalCollaborationRef_process"),
    'callConversation': _Ref('callConversation', "CallConversation", multi=True, lo=0, hi='*', assoc="A_calledCollaborationRef_callConversation"),
    }
    _OPPS = {
        'choreographyRef': ('collaboration',),
        'artifacts': ('collaboration',),
        'participantAssociations': ('collaboration',),
        'messageFlowAssociations': ('collaboration',),
        'conversationAssociations': ('converstaionAssociations',),
        'participants': ('collaboration',),
        'messageFlows': ('collaboration',),
        'correlationKeys': ('collaboration',),
        'conversations': ('collaboration',),
        'conversationLinks': ('collaboration',),
        'process': ('definitionalCollaborationRef',),
        'callConversation': ('calledCollaborationRef',),
    }

class Choreography(FlowElementsContainer, Collaboration):
    _ABSTRACT = False
    # association end of A_choreographyRef_collaboration (opposite of Collaboration.choreographyRef)
    # association end of A_calledChoreographyRef_callChoreographyActivity (opposite of CallChoreography.calledChoreographyRef)
    _DECL = {
    'collaboration': _Ref('collaboration', "Collaboration", multi=True, lo=0, hi='*', assoc="A_choreographyRef_collaboration"),
    'callChoreographyActivity': _Ref('callChoreographyActivity', "CallChoreography", multi=True, lo=0, hi='*', assoc="A_calledChoreographyRef_callChoreographyActivity"),
    }
    _OPPS = {
        'collaboration': ('choreographyRef',),
        'callChoreographyActivity': ('calledChoreographyRef',),
    }

class ChoreographyTask(ChoreographyActivity):
    _ABSTRACT = False
    _DECL = {
    'messageFlowRef': _Ref('messageFlowRef', "MessageFlow", multi=True, lo=1, hi='2', assoc="A_messageFlowRef_choreographyTask"),
    }
    _OPPS = {
        'messageFlowRef': ('choreographyTask',),
    }

class CompensateEventDefinition(EventDefinition):
    _ABSTRACT = False
    _DECL = {
    'waitForCompletion': _Ref('waitForCompletion', bool),
    'activityRef': _Ref('activityRef', "Activity", assoc="A_activityRef_compensateEventDefinition"),
    }
    _OPPS = {
        'activityRef': ('compensateEventDefinition',),
    }

class ComplexBehaviorDefinition(BaseElement):
    _ABSTRACT = False
    # association end of A_complexBehaviorDefinition_multiInstanceLoopCharacteristics (opposite of MultiInstanceLoopCharacteristics.complexBehaviorDefinition)
    _DECL = {
    'condition': _Ref('condition', "FormalExpression", composite=True, assoc="A_condition_complexBehaviorDefinition"),
    'event': _Ref('event', "ImplicitThrowEvent", composite=True, assoc="A_event_complexBehaviorDefinition"),
    'multiInstanceLoopCharacteristics': _Ref('multiInstanceLoopCharacteristics', "MultiInstanceLoopCharacteristics", assoc="A_complexBehaviorDefinition_multiInstanceLoopCharacteristics"),
    }
    _OPPS = {
        'condition': ('complexBehaviorDefinition',),
        'event': ('complexBehaviorDefinition',),
        'multiInstanceLoopCharacteristics': ('complexBehaviorDefinition',),
    }

class Gateway(FlowNode):
    _ABSTRACT = True
    # default: 'unspecified'
    _DECL = {
    'gatewayDirection': _Ref('gatewayDirection', "GatewayDirection"),
    }

class ComplexGateway(Gateway):
    _ABSTRACT = False
    _DECL = {
    'activationCondition': _Ref('activationCondition', "Expression", composite=True, assoc="A_activationCondition_complexGateway"),
    'default': _Ref('default', "SequenceFlow", assoc="A_default_complexGateway"),
    }
    _OPPS = {
        'activationCondition': ('complexGateway',),
        'default': ('complexGateway',),
    }

class ConditionalEventDefinition(EventDefinition):
    _ABSTRACT = False
    _DECL = {
    'condition': _Ref('condition', "Expression", composite=True, assoc="A_condition_conditionalEventDefinition"),
    }
    _OPPS = {
        'condition': ('conditionalEventDefinition',),
    }

class Conversation(ConversationNode):
    _ABSTRACT = False

class ConversationAssociation(BaseElement):
    _ABSTRACT = False
    # association end of A_conversationAssociations_converstaionAssociations (opposite of Collaboration.conversationAssociations)
    _DECL = {
    'innerConversationNodeRef': _Ref('innerConversationNodeRef', "ConversationNode", assoc="A_innerConversationNodeRef_conversationAssociation"),
    'outerConversationNodeRef': _Ref('outerConversationNodeRef', "ConversationNode", assoc="A_outerConversationNodeRef_conversationAssociation"),
    'converstaionAssociations': _Ref('converstaionAssociations', "Collaboration", assoc="A_conversationAssociations_converstaionAssociations"),
    }
    _OPPS = {
        'innerConversationNodeRef': ('conversationAssociation',),
        'outerConversationNodeRef': ('conversationAssociation',),
        'converstaionAssociations': ('conversationAssociations',),
    }

class ConversationLink(BaseElement):
    _ABSTRACT = False
    # association end of A_conversationLinks_collaboration (opposite of Collaboration.conversationLinks)
    _DECL = {
    'sourceRef': _Ref('sourceRef', "InteractionNode", assoc="A_sourceRef_outgoingConversationLinks"),
    'targetRef': _Ref('targetRef', "InteractionNode", assoc="A_targetRef_incomingConversationLinks"),
    'name': _Ref('name', str),
    'collaboration': _Ref('collaboration', "Collaboration", assoc="A_conversationLinks_collaboration"),
    }
    _OPPS = {
        'sourceRef': ('outgoingConversationLinks',),
        'targetRef': ('incomingConversationLinks',),
        'collaboration': ('conversationLinks',),
    }

class CorrelationKey(BaseElement):
    _ABSTRACT = False
    # association end of A_correlationKeys_collaboration (opposite of Collaboration.correlationKeys)
    # association end of A_correlationKeys_conversationNode (opposite of ConversationNode.correlationKeys)
    # association end of A_correlationKeyRef_correlationSubscription (opposite of CorrelationSubscription.correlationKeyRef)
    # association end of A_correlationKeys_choreographyActivity (opposite of ChoreographyActivity.correlationKeys)
    _DECL = {
    'correlationPropertyRef': _Ref('correlationPropertyRef', "CorrelationProperty", multi=True, lo=0, hi='*', assoc="A_correlationPropertyRef_correlationKey"),
    'name': _Ref('name', str),
    'collaboration': _Ref('collaboration', "Collaboration", assoc="A_correlationKeys_collaboration"),
    'conversationNode': _Ref('conversationNode', "ConversationNode", assoc="A_correlationKeys_conversationNode"),
    'correlationSubscription': _Ref('correlationSubscription', "CorrelationSubscription", multi=True, lo=0, hi='*', assoc="A_correlationKeyRef_correlationSubscription"),
    'choreographyActivity': _Ref('choreographyActivity', "ChoreographyActivity", assoc="A_correlationKeys_choreographyActivity"),
    }
    _OPPS = {
        'correlationPropertyRef': ('correlationKey',),
        'collaboration': ('correlationKeys',),
        'conversationNode': ('correlationKeys',),
        'correlationSubscription': ('correlationKeyRef',),
        'choreographyActivity': ('correlationKeys',),
    }

class CorrelationProperty(RootElement):
    _ABSTRACT = False
    # association end of A_correlationPropertyRef_correlationKey (opposite of CorrelationKey.correlationPropertyRef)
    # association end of A_correlationPropertyRef_correlationPropertyBinding (opposite of CorrelationPropertyBinding.correlationPropertyRef)
    _DECL = {
    'correlationPropertyRetrievalExpression': _Ref('correlationPropertyRetrievalExpression', "CorrelationPropertyRetrievalExpression", multi=True, lo=0, hi='*', composite=True, assoc="A_correlationPropertyRetrievalExpression_correlationproperty"),
    'name': _Ref('name', str),
    'type': _Ref('type', "ItemDefinition", assoc="A_type_correlationProperty"),
    'correlationKey': _Ref('correlationKey', "CorrelationKey", multi=True, lo=0, hi='*', assoc="A_correlationPropertyRef_correlationKey"),
    'correlationPropertyBinding': _Ref('correlationPropertyBinding', "CorrelationPropertyBinding", multi=True, lo=0, hi='*', assoc="A_correlationPropertyRef_correlationPropertyBinding"),
    }
    _OPPS = {
        'correlationPropertyRetrievalExpression': ('correlationproperty',),
        'type': ('correlationProperty',),
        'correlationKey': ('correlationPropertyRef',),
        'correlationPropertyBinding': ('correlationPropertyRef',),
    }

class CorrelationPropertyBinding(BaseElement):
    _ABSTRACT = False
    # association end of A_correlationPropertyBinding_correlationSubscription (opposite of CorrelationSubscription.correlationPropertyBinding)
    _DECL = {
    'dataPath': _Ref('dataPath', "FormalExpression", composite=True, assoc="A_dataPath_correlationPropertyBinding"),
    'correlationPropertyRef': _Ref('correlationPropertyRef', "CorrelationProperty", assoc="A_correlationPropertyRef_correlationPropertyBinding"),
    'correlationSubscription': _Ref('correlationSubscription', "CorrelationSubscription", assoc="A_correlationPropertyBinding_correlationSubscription"),
    }
    _OPPS = {
        'dataPath': ('correlationPropertyBinding',),
        'correlationPropertyRef': ('correlationPropertyBinding',),
        'correlationSubscription': ('correlationPropertyBinding',),
    }

class CorrelationPropertyRetrievalExpression(BaseElement):
    _ABSTRACT = False
    # association end of A_correlationPropertyRetrievalExpression_correlationproperty (opposite of CorrelationProperty.correlationPropertyRetrievalExpression)
    _DECL = {
    'messagePath': _Ref('messagePath', "FormalExpression", composite=True, assoc="A_messagePath_correlationset"),
    'messageRef': _Ref('messageRef', "Message", assoc="A_messageRef_correlationPropertyRetrievalExpression"),
    'correlationproperty': _Ref('correlationproperty', "CorrelationProperty", assoc="A_correlationPropertyRetrievalExpression_correlationproperty"),
    }
    _OPPS = {
        'messagePath': ('correlationset',),
        'messageRef': ('correlationPropertyRetrievalExpression',),
        'correlationproperty': ('correlationPropertyRetrievalExpression',),
    }

class CorrelationSubscription(BaseElement):
    _ABSTRACT = False
    # association end of A_correlationSubscriptions_process (opposite of Process.correlationSubscriptions)
    _DECL = {
    'correlationKeyRef': _Ref('correlationKeyRef', "CorrelationKey", assoc="A_correlationKeyRef_correlationSubscription"),
    'correlationPropertyBinding': _Ref('correlationPropertyBinding', "CorrelationPropertyBinding", multi=True, lo=0, hi='*', composite=True, assoc="A_correlationPropertyBinding_correlationSubscription"),
    'process': _Ref('process', "Process", assoc="A_correlationSubscriptions_process"),
    }
    _OPPS = {
        'correlationKeyRef': ('correlationSubscription',),
        'correlationPropertyBinding': ('correlationSubscription',),
        'process': ('correlationSubscriptions',),
    }

class DataAssociation(BaseElement):
    _ABSTRACT = False
    _DECL = {
    'transformation': _Ref('transformation', "FormalExpression", composite=True, assoc="A_transformation_dataAssociation"),
    'assignment': _Ref('assignment', "Assignment", multi=True, lo=0, hi='*', composite=True, assoc="A_assignment_dataAssociation"),
    'targetRef': _Ref('targetRef', "ItemAwareElement", assoc="A_targetRef_dataAssociation"),
    'sourceRef': _Ref('sourceRef', "ItemAwareElement", multi=True, lo=0, hi='*', assoc="A_sourceRef_dataAssociation"),
    }
    _OPPS = {
        'transformation': ('dataAssociation',),
        'assignment': ('dataAssociation',),
        'targetRef': ('dataAssociation',),
        'sourceRef': ('dataAssociation',),
    }

class ItemAwareElement(BaseElement):
    _ABSTRACT = False
    # association end of A_sourceRef_dataAssociation (opposite of DataAssociation.sourceRef)
    # association end of A_loopDataInputRef_multiInstanceLoopCharacteristics (opposite of MultiInstanceLoopCharacteristics.loopDataInputRef)
    _DECL = {
    'itemSubjectRef': _Ref('itemSubjectRef', "ItemDefinition", assoc="A_itemSubjectRef_itemAwareElement"),
    'dataState': _Ref('dataState', "DataState", composite=True, assoc="A_dataState_itemAwareElement"),
    'dataAssociation': _Ref('dataAssociation', "DataAssociation", multi=True, lo=0, hi='*', assoc="A_sourceRef_dataAssociation"),
    'multiInstanceLoopCharacteristics': _Ref('multiInstanceLoopCharacteristics', "MultiInstanceLoopCharacteristics", assoc="A_loopDataInputRef_multiInstanceLoopCharacteristics"),
    }
    _OPPS = {
        'itemSubjectRef': ('itemAwareElement',),
        'dataState': ('itemAwareElement',),
        'dataAssociation': ('sourceRef', 'targetRef'),
        'multiInstanceLoopCharacteristics': ('loopDataInputRef', 'loopDataOutputRef'),
    }

class DataInput(ItemAwareElement):
    _ABSTRACT = False
    # default: 'false'
    # association end of A_dataInputs_throwEvent (opposite of ThrowEvent.dataInputs)
    # association end of A_dataInputs_inputOutputSpecification (opposite of InputOutputSpecification.dataInputs)
    # association end of A_inputDataItem_multiInstanceLoopCharacteristics (opposite of MultiInstanceLoopCharacteristics.inputDataItem)
    _DECL = {
    'name': _Ref('name', str),
    'isCollection': _Ref('isCollection', bool),
    'inputSetRefs': _Ref('inputSetRefs', "InputSet", multi=True, lo=0, hi='*', derived=True, assoc="A_dataInputRefs_inputSetRefs"),
    'inputSetWithOptional': _Ref('inputSetWithOptional', "InputSet", multi=True, lo=0, hi='*', derived=True, assoc="A_optionalInputRefs_inputSetWithOptional"),
    'inputSetWithWhileExecuting': _Ref('inputSetWithWhileExecuting', "InputSet", multi=True, lo=0, hi='*', derived=True, assoc="A_whileExecutingInputRefs_inputSetWithWhileExecuting"),
    'throwEvent': _Ref('throwEvent', "ThrowEvent", assoc="A_dataInputs_throwEvent"),
    'inputOutputSpecification': _Ref('inputOutputSpecification', "InputOutputSpecification", assoc="A_dataInputs_inputOutputSpecification"),
    'multiInstanceLoopCharacteristics': _Ref('multiInstanceLoopCharacteristics', "MultiInstanceLoopCharacteristics", assoc="A_inputDataItem_multiInstanceLoopCharacteristics"),
    }
    _OPPS = {
        'inputSetRefs': ('dataInputRefs',),
        'inputSetWithOptional': ('optionalInputRefs',),
        'inputSetWithWhileExecuting': ('whileExecutingInputRefs',),
        'throwEvent': ('dataInputs',),
        'inputOutputSpecification': ('dataInputs',),
        'multiInstanceLoopCharacteristics': ('inputDataItem',),
    }

class DataInputAssociation(DataAssociation):
    _ABSTRACT = False
    # association end of A_dataInputAssociation_throwEvent (opposite of ThrowEvent.dataInputAssociation)
    # association end of A_dataInputAssociations_activity (opposite of Activity.dataInputAssociations)
    _DECL = {
    'throwEvent': _Ref('throwEvent', "ThrowEvent", assoc="A_dataInputAssociation_throwEvent"),
    'activity': _Ref('activity', "Activity", assoc="A_dataInputAssociations_activity"),
    }
    _OPPS = {
        'throwEvent': ('dataInputAssociation',),
        'activity': ('dataInputAssociations',),
    }

class DataObject(FlowElement, ItemAwareElement):
    _ABSTRACT = False
    # default: 'false'
    # association end of A_dataObjectRef_dataObject (opposite of DataObjectReference.dataObjectRef)
    _DECL = {
    'isCollection': _Ref('isCollection', bool),
    'dataObject': _Ref('dataObject', "DataObjectReference", multi=True, lo=0, hi='*', assoc="A_dataObjectRef_dataObject"),
    }
    _OPPS = {
        'dataObject': ('dataObjectRef',),
    }

class DataObjectReference(ItemAwareElement, FlowElement):
    _ABSTRACT = False
    _DECL = {
    'dataObjectRef': _Ref('dataObjectRef', "DataObject", assoc="A_dataObjectRef_dataObject"),
    }
    _OPPS = {
        'dataObjectRef': ('dataObject',),
    }

class DataOutput(ItemAwareElement):
    _ABSTRACT = False
    # default: 'false'
    # association end of A_dataOutputs_catchEvent (opposite of CatchEvent.dataOutputs)
    # association end of A_dataOutputs_inputOutputSpecification (opposite of InputOutputSpecification.dataOutputs)
    # association end of A_outputDataItem_multiInstanceLoopCharacteristics (opposite of MultiInstanceLoopCharacteristics.outputDataItem)
    _DECL = {
    'name': _Ref('name', str),
    'isCollection': _Ref('isCollection', bool),
    'outputSetRefs': _Ref('outputSetRefs', "OutputSet", multi=True, lo=0, hi='*', derived=True, assoc="A_dataOutputRefs_outputSetRefs"),
    'outputSetWithOptional': _Ref('outputSetWithOptional', "OutputSet", multi=True, lo=0, hi='*', derived=True, assoc="A_outputSetWithOptional_optionalOutputRefs"),
    'outputSetWithWhileExecuting': _Ref('outputSetWithWhileExecuting', "OutputSet", multi=True, lo=0, hi='*', derived=True, assoc="A_outputSetWithWhileExecuting_whileExecutingOutputRefs"),
    'catchEvent': _Ref('catchEvent', "CatchEvent", assoc="A_dataOutputs_catchEvent"),
    'inputOutputSpecification': _Ref('inputOutputSpecification', "InputOutputSpecification", assoc="A_dataOutputs_inputOutputSpecification"),
    'multiInstanceLoopCharacteristics': _Ref('multiInstanceLoopCharacteristics', "MultiInstanceLoopCharacteristics", assoc="A_outputDataItem_multiInstanceLoopCharacteristics"),
    }
    _OPPS = {
        'outputSetRefs': ('dataOutputRefs',),
        'outputSetWithOptional': ('optionalOutputRefs',),
        'outputSetWithWhileExecuting': ('whileExecutingOutputRefs',),
        'catchEvent': ('dataOutputs',),
        'inputOutputSpecification': ('dataOutputs',),
        'multiInstanceLoopCharacteristics': ('outputDataItem',),
    }

class DataOutputAssociation(DataAssociation):
    _ABSTRACT = False
    # association end of A_dataOutputAssociation_catchEvent (opposite of CatchEvent.dataOutputAssociation)
    # association end of A_dataOutputAssociations_activity (opposite of Activity.dataOutputAssociations)
    _DECL = {
    'catchEvent': _Ref('catchEvent', "CatchEvent", assoc="A_dataOutputAssociation_catchEvent"),
    'activity': _Ref('activity', "Activity", assoc="A_dataOutputAssociations_activity"),
    }
    _OPPS = {
        'catchEvent': ('dataOutputAssociation',),
        'activity': ('dataOutputAssociations',),
    }

class DataState(BaseElement):
    _ABSTRACT = False
    # association end of A_dataState_itemAwareElement (opposite of ItemAwareElement.dataState)
    _DECL = {
    'name': _Ref('name', str),
    'itemAwareElement': _Ref('itemAwareElement', "ItemAwareElement", assoc="A_dataState_itemAwareElement"),
    }
    _OPPS = {
        'itemAwareElement': ('dataState',),
    }

class DataStore(RootElement, ItemAwareElement):
    _ABSTRACT = False
    # default: 'true'
    # association end of A_dataStoreRef_dataStoreReference (opposite of DataStoreReference.dataStoreRef)
    _DECL = {
    'name': _Ref('name', str),
    'capacity': _Ref('capacity', int),
    'isUnlimited': _Ref('isUnlimited', bool),
    'dataStoreReference': _Ref('dataStoreReference', "DataStoreReference", multi=True, lo=0, hi='*', assoc="A_dataStoreRef_dataStoreReference"),
    }
    _OPPS = {
        'dataStoreReference': ('dataStoreRef',),
    }

class DataStoreReference(ItemAwareElement, FlowElement):
    _ABSTRACT = False
    _DECL = {
    'dataStoreRef': _Ref('dataStoreRef', "DataStore", assoc="A_dataStoreRef_dataStoreReference"),
    }
    _OPPS = {
        'dataStoreRef': ('dataStoreReference',),
    }

class Definitions(BaseElement):
    _ABSTRACT = False
    # default: 'http://www.w3.org/1999/XPath'
    # default: 'http://www.w3.org/2001/XMLSchema'
    _DECL = {
    'name': _Ref('name', str),
    'targetNamespace': _Ref('targetNamespace', str),
    'expressionLanguage': _Ref('expressionLanguage', str),
    'typeLanguage': _Ref('typeLanguage', str),
    'imports': _Ref('imports', "Import", multi=True, lo=0, hi='*', composite=True, assoc="A_imports_definition"),
    'extensions': _Ref('extensions', "Extension", multi=True, lo=0, hi='*', composite=True, assoc="A_extensions_definitions"),
    'relationships': _Ref('relationships', "Relationship", multi=True, lo=0, hi='*', composite=True, assoc="A_relationships_definition"),
    'rootElements': _Ref('rootElements', "RootElement", multi=True, lo=0, hi='*', composite=True, assoc="A_rootElements_definition"),
    'diagrams': _Ref('diagrams', 'BPMNDI.BPMNDiagram', multi=True, lo=0, hi='*', composite=True, assoc="A_diagrams_definitions"),
    'exporter': _Ref('exporter', str),
    'exporterVersion': _Ref('exporterVersion', str),
    }
    _OPPS = {
        'imports': ('definition',),
        'extensions': ('definitions',),
        'relationships': ('definition',),
        'rootElements': ('definition',),
        'diagrams': ('definitions',),
    }

class Documentation(BaseElement):
    _ABSTRACT = False
    # default: 'text/plain'
    # association end of A_documentation_baseElement (opposite of BaseElement.documentation)
    _DECL = {
    'text': _Ref('text', str),
    'textFormat': _Ref('textFormat', str),
    'baseElement': _Ref('baseElement', "BaseElement", assoc="A_documentation_baseElement"),
    }
    _OPPS = {
        'baseElement': ('documentation',),
    }

class ThrowEvent(Event):
    _ABSTRACT = True
    _DECL = {
    'inputSet': _Ref('inputSet', "InputSet", composite=True, assoc="A_inputSet_throwEvent"),
    'eventDefinitionRefs': _Ref('eventDefinitionRefs', "EventDefinition", multi=True, lo=0, hi='*', assoc="A_eventDefinitionRefs_throwEvent"),
    'dataInputAssociation': _Ref('dataInputAssociation', "DataInputAssociation", multi=True, lo=0, hi='*', composite=True, assoc="A_dataInputAssociation_throwEvent"),
    'dataInputs': _Ref('dataInputs', "DataInput", multi=True, lo=0, hi='*', composite=True, assoc="A_dataInputs_throwEvent"),
    'eventDefinitions': _Ref('eventDefinitions', "EventDefinition", multi=True, lo=0, hi='*', composite=True, assoc="A_eventDefinitions_throwEvent"),
    }
    _OPPS = {
        'inputSet': ('throwEvent',),
        'eventDefinitionRefs': ('throwEvent',),
        'dataInputAssociation': ('throwEvent',),
        'dataInputs': ('throwEvent',),
        'eventDefinitions': ('throwEvent',),
    }

class EndEvent(ThrowEvent):
    _ABSTRACT = False

class EndPoint(RootElement):
    _ABSTRACT = False
    # association end of A_endPointRefs_participant (opposite of Participant.endPointRefs)
    _DECL = {
    'participant': _Ref('participant', "Participant", multi=True, lo=0, hi='*', assoc="A_endPointRefs_participant"),
    }
    _OPPS = {
        'participant': ('endPointRefs',),
    }

class Error(RootElement):
    _ABSTRACT = False
    # association end of A_errorRefs_operation (opposite of Operation.errorRefs)
    # association end of A_errorRef_errorEventDefinition (opposite of ErrorEventDefinition.errorRef)
    _DECL = {
    'structureRef': _Ref('structureRef', "ItemDefinition", assoc="A_structureRef_error"),
    'name': _Ref('name', str),
    'errorCode': _Ref('errorCode', str),
    'operation': _Ref('operation', "Operation", multi=True, lo=0, hi='*', assoc="A_errorRefs_operation"),
    'errorEventDefinition': _Ref('errorEventDefinition', "ErrorEventDefinition", multi=True, lo=0, hi='*', assoc="A_errorRef_errorEventDefinition"),
    }
    _OPPS = {
        'structureRef': ('error',),
        'operation': ('errorRefs',),
        'errorEventDefinition': ('errorRef',),
    }

class ErrorEventDefinition(EventDefinition):
    _ABSTRACT = False
    _DECL = {
    'errorRef': _Ref('errorRef', "Error", assoc="A_errorRef_errorEventDefinition"),
    }
    _OPPS = {
        'errorRef': ('errorEventDefinition',),
    }

class Escalation(_MOFBase):
    _ABSTRACT = False
    # association end of A_escalationRef_escalationEventDefinition (opposite of EscalationEventDefinition.escalationRef)
    _DECL = {
    'structureRef': _Ref('structureRef', "ItemDefinition", assoc="A_structureRef_escalation"),
    'name': _Ref('name', str),
    'escalationCode': _Ref('escalationCode', str),
    'escalationEventDefinition': _Ref('escalationEventDefinition', "EscalationEventDefinition", multi=True, lo=0, hi='*', assoc="A_escalationRef_escalationEventDefinition"),
    }
    _OPPS = {
        'structureRef': ('escalation',),
        'escalationEventDefinition': ('escalationRef',),
    }

class EscalationEventDefinition(EventDefinition):
    _ABSTRACT = False
    _DECL = {
    'escalationRef': _Ref('escalationRef', "Escalation", assoc="A_escalationRef_escalationEventDefinition"),
    }
    _OPPS = {
        'escalationRef': ('escalationEventDefinition',),
    }

class EventBasedGateway(Gateway):
    _ABSTRACT = False
    # default: 'false'
    _DECL = {
    'instantiate': _Ref('instantiate', bool),
    'eventGatewayType': _Ref('eventGatewayType', "EventBasedGatewayType"),
    }

class ExclusiveGateway(Gateway):
    _ABSTRACT = False
    _DECL = {
    'default': _Ref('default', "SequenceFlow", assoc="A_default_exclusiveGateway"),
    }
    _OPPS = {
        'default': ('exclusiveGateway',),
    }

class Expression(BaseElement):
    _ABSTRACT = False
    # association end of A_activationCondition_complexGateway (opposite of ComplexGateway.activationCondition)
    # association end of A_condition_conditionalEventDefinition (opposite of ConditionalEventDefinition.condition)
    # association end of A_timeDate_timerEventDefinition (opposite of TimerEventDefinition.timeDate)
    # association end of A_from_assignment (opposite of Assignment.from)
    # association end of A_conditionExpression_sequenceFlow (opposite of SequenceFlow.conditionExpression)
    # association end of A_expression_resourceAssignmentExpression (opposite of ResourceAssignmentExpression.expression)
    # association end of A_expression_resourceParameterBinding (opposite of ResourceParameterBinding.expression)
    # association end of A_completionCondition_multiInstanceLoopCharacteristics (opposite of MultiInstanceLoopCharacteristics.completionCondition)
    # association end of A_loopCondition_standardLoopCharacteristics (opposite of StandardLoopCharacteristics.loopCondition)
    # association end of A_completionCondition_adHocSubProcess (opposite of AdHocSubProcess.completionCondition)
    _DECL = {
    'complexGateway': _Ref('complexGateway', "ComplexGateway", assoc="A_activationCondition_complexGateway"),
    'conditionalEventDefinition': _Ref('conditionalEventDefinition', "ConditionalEventDefinition", assoc="A_condition_conditionalEventDefinition"),
    'timerEventDefinition': _Ref('timerEventDefinition', "TimerEventDefinition", assoc="A_timeDate_timerEventDefinition"),
    'assignment': _Ref('assignment', "Assignment", assoc="A_from_assignment"),
    'sequenceFlow': _Ref('sequenceFlow', "SequenceFlow", assoc="A_conditionExpression_sequenceFlow"),
    'resourceAssignmentExpression': _Ref('resourceAssignmentExpression', "ResourceAssignmentExpression", assoc="A_expression_resourceAssignmentExpression"),
    'resourceParameterBinding': _Ref('resourceParameterBinding', "ResourceParameterBinding", assoc="A_expression_resourceParameterBinding"),
    'multiInstanceLoopCharacteristics': _Ref('multiInstanceLoopCharacteristics', "MultiInstanceLoopCharacteristics", assoc="A_completionCondition_multiInstanceLoopCharacteristics"),
    'standardLoopCharacteristics': _Ref('standardLoopCharacteristics', "StandardLoopCharacteristics", assoc="A_loopCondition_standardLoopCharacteristics"),
    'adHocSubProcess': _Ref('adHocSubProcess', "AdHocSubProcess", assoc="A_completionCondition_adHocSubProcess"),
    }
    _OPPS = {
        'complexGateway': ('activationCondition',),
        'conditionalEventDefinition': ('condition',),
        'timerEventDefinition': ('timeDate', 'timeCycle', 'timeDuration'),
        'assignment': ('from', 'to'),
        'sequenceFlow': ('conditionExpression',),
        'resourceAssignmentExpression': ('expression',),
        'resourceParameterBinding': ('expression',),
        'multiInstanceLoopCharacteristics': ('completionCondition', 'loopCardinality'),
        'standardLoopCharacteristics': ('loopCondition', 'loopMaximum'),
        'adHocSubProcess': ('completionCondition',),
    }

class Extension(_MOFBase):
    _ABSTRACT = False
    # default: 'false'
    # association end of A_extensions_definitions (opposite of Definitions.extensions)
    _DECL = {
    'mustUnderstand': _Ref('mustUnderstand', bool),
    'definition': _Ref('definition', "ExtensionDefinition", composite=True, assoc="A_definition_extension"),
    'definitions': _Ref('definitions', "Definitions", assoc="A_extensions_definitions"),
    }
    _OPPS = {
        'definition': ('extension',),
        'definitions': ('extensions',),
    }

class ExtensionAttributeDefinition(_MOFBase):
    _ABSTRACT = False
    # default: 'false'
    # association end of A_extensionAttributeDefinition_extensionAttributeValue (opposite of ExtensionAttributeValue.extensionAttributeDefinition)
    _DECL = {
    'name': _Ref('name', str),
    'type': _Ref('type', str),
    'isReference': _Ref('isReference', bool),
    'extensionDefinition': _Ref('extensionDefinition', "ExtensionDefinition", assoc="A_extensionAttributeDefinitions_extensionDefinition"),
    'extensionAttributeValue': _Ref('extensionAttributeValue', "ExtensionAttributeValue", multi=True, lo=0, hi='*', assoc="A_extensionAttributeDefinition_extensionAttributeValue"),
    }
    _OPPS = {
        'extensionDefinition': ('extensionAttributeDefinitions',),
        'extensionAttributeValue': ('extensionAttributeDefinition',),
    }

class ExtensionAttributeValue(_MOFBase):
    _ABSTRACT = False
    # association end of A_extensionValues_baseElement (opposite of BaseElement.extensionValues)
    _DECL = {
    'valueRef': _Ref('valueRef', 'xml.dom.Element', assoc="A_valueRef_extensionAttributeValue"),
    'value': _Ref('value', 'xml.dom.Element', composite=True, assoc="A_value_extensionAttributeValue"),
    'extensionAttributeDefinition': _Ref('extensionAttributeDefinition', "ExtensionAttributeDefinition", assoc="A_extensionAttributeDefinition_extensionAttributeValue"),
    'baseElement': _Ref('baseElement', "BaseElement", assoc="A_extensionValues_baseElement"),
    }
    _OPPS = {
        'valueRef': ('extensionAttributeValue',),
        'value': ('extensionAttributeValue',),
        'extensionAttributeDefinition': ('extensionAttributeValue',),
        'baseElement': ('extensionValues',),
    }

class ExtensionDefinition(_MOFBase):
    _ABSTRACT = False
    # association end of A_extensionDefinitions_baseElement (opposite of BaseElement.extensionDefinitions)
    # association end of A_definition_extension (opposite of Extension.definition)
    _DECL = {
    'name': _Ref('name', str),
    'extensionAttributeDefinitions': _Ref('extensionAttributeDefinitions', "ExtensionAttributeDefinition", multi=True, lo=0, hi='*', composite=True, assoc="A_extensionAttributeDefinitions_extensionDefinition"),
    'baseElement': _Ref('baseElement', "BaseElement", multi=True, lo=0, hi='*', assoc="A_extensionDefinitions_baseElement"),
    'extension': _Ref('extension', "Extension", assoc="A_definition_extension"),
    }
    _OPPS = {
        'extensionAttributeDefinitions': ('extensionDefinition',),
        'baseElement': ('extensionDefinitions',),
        'extension': ('definition',),
    }

class FormalExpression(Expression):
    _ABSTRACT = False
    # association end of A_transformation_dataAssociation (opposite of DataAssociation.transformation)
    # association end of A_messagePath_correlationset (opposite of CorrelationPropertyRetrievalExpression.messagePath)
    # association end of A_dataPath_correlationPropertyBinding (opposite of CorrelationPropertyBinding.dataPath)
    # association end of A_condition_complexBehaviorDefinition (opposite of ComplexBehaviorDefinition.condition)
    _DECL = {
    'language': _Ref('language', str),
    'body': _Ref('body', 'xml.dom.Element'),
    'evaluatesToTypeRef': _Ref('evaluatesToTypeRef', "ItemDefinition", assoc="A_evaluatesToTypeRef_formalExpression"),
    'dataAssociation': _Ref('dataAssociation', "DataAssociation", assoc="A_transformation_dataAssociation"),
    'correlationset': _Ref('correlationset', "CorrelationPropertyRetrievalExpression", assoc="A_messagePath_correlationset"),
    'correlationPropertyBinding': _Ref('correlationPropertyBinding', "CorrelationPropertyBinding", assoc="A_dataPath_correlationPropertyBinding"),
    'complexBehaviorDefinition': _Ref('complexBehaviorDefinition', "ComplexBehaviorDefinition", assoc="A_condition_complexBehaviorDefinition"),
    }
    _OPPS = {
        'evaluatesToTypeRef': ('formalExpression',),
        'dataAssociation': ('transformation',),
        'correlationset': ('messagePath',),
        'correlationPropertyBinding': ('dataPath',),
        'complexBehaviorDefinition': ('condition',),
    }

class GlobalTask(CallableElement):
    _ABSTRACT = False
    _DECL = {
    'resources': _Ref('resources', "ResourceRole", multi=True, lo=0, hi='*', composite=True, assoc="A_resources_globalTask"),
    }
    _OPPS = {
        'resources': ('globalTask',),
    }

class GlobalBusinessRuleTask(GlobalTask):
    _ABSTRACT = False
    _DECL = {
    'implementation': _Ref('implementation', str),
    }

class GlobalChoreographyTask(Choreography):
    _ABSTRACT = False
    _DECL = {
    'initiatingParticipantRef': _Ref('initiatingParticipantRef', "Participant", assoc="A_initiatingParticipantRef_globalChoreographyTask"),
    }
    _OPPS = {
        'initiatingParticipantRef': ('globalChoreographyTask',),
    }

class GlobalConversation(Collaboration):
    _ABSTRACT = False

class GlobalManualTask(GlobalTask):
    _ABSTRACT = False

class GlobalScriptTask(GlobalTask):
    _ABSTRACT = False
    _DECL = {
    'scriptLanguage': _Ref('scriptLanguage', str),
    'script': _Ref('script', str),
    }

class GlobalUserTask(GlobalTask):
    _ABSTRACT = False
    _DECL = {
    'implementation': _Ref('implementation', str),
    'renderings': _Ref('renderings', "Rendering", multi=True, lo=0, hi='*', composite=True, assoc="A_renderings_globalUserTask"),
    }
    _OPPS = {
        'renderings': ('globalUserTask',),
    }

class Group(Artifact):
    _ABSTRACT = False
    _DECL = {
    'categoryValueRef': _Ref('categoryValueRef', "CategoryValue", assoc="A_categoryValueRef_categoryValueRef"),
    }
    _OPPS = {
        'categoryValueRef': ('categoryValueRef',),
    }

class ResourceRole(BaseElement):
    _ABSTRACT = False
    # association end of A_resources_globalTask (opposite of GlobalTask.resources)
    # association end of A_resources_process (opposite of Process.resources)
    # association end of A_resources_activity (opposite of Activity.resources)
    _DECL = {
    'resourceRef': _Ref('resourceRef', "Resource", assoc="A_resourceRef_activityResource"),
    'resourceParameterBindings': _Ref('resourceParameterBindings', "ResourceParameterBinding", multi=True, lo=0, hi='*', composite=True, assoc="A_resourceParameterBindings_activityResource"),
    'resourceAssignmentExpression': _Ref('resourceAssignmentExpression', "ResourceAssignmentExpression", composite=True, assoc="A_resourceAssignmentExpression_activityResource"),
    'name': _Ref('name', str),
    'globalTask': _Ref('globalTask', "GlobalTask", assoc="A_resources_globalTask"),
    'process': _Ref('process', "Process", assoc="A_resources_process"),
    'activity': _Ref('activity', "Activity", assoc="A_resources_activity"),
    }
    _OPPS = {
        'resourceRef': ('activityResource',),
        'resourceParameterBindings': ('activityResource',),
        'resourceAssignmentExpression': ('activityResource',),
        'globalTask': ('resources',),
        'process': ('resources',),
        'activity': ('resources',),
    }

class Performer(ResourceRole):
    _ABSTRACT = False

class HumanPerformer(Performer):
    _ABSTRACT = False

class ImplicitThrowEvent(ThrowEvent):
    _ABSTRACT = False
    # association end of A_event_complexBehaviorDefinition (opposite of ComplexBehaviorDefinition.event)
    _DECL = {
    'complexBehaviorDefinition': _Ref('complexBehaviorDefinition', "ComplexBehaviorDefinition", assoc="A_event_complexBehaviorDefinition"),
    }
    _OPPS = {
        'complexBehaviorDefinition': ('event',),
    }

class Import(_MOFBase):
    _ABSTRACT = False
    # association end of A_import_itemDefinition (opposite of ItemDefinition.import)
    # association end of A_imports_definition (opposite of Definitions.imports)
    _DECL = {
    'importType': _Ref('importType', str),
    'location': _Ref('location', str),
    'namespace': _Ref('namespace', str),
    'itemDefinition': _Ref('itemDefinition', "ItemDefinition", multi=True, lo=0, hi='*', assoc="A_import_itemDefinition"),
    'definition': _Ref('definition', "Definitions", assoc="A_imports_definition"),
    }
    _OPPS = {
        'itemDefinition': ('import',),
        'definition': ('imports',),
    }

class InclusiveGateway(Gateway):
    _ABSTRACT = False
    _DECL = {
    'default': _Ref('default', "SequenceFlow", assoc="A_default_inclusiveGateway"),
    }
    _OPPS = {
        'default': ('inclusiveGateway',),
    }

class InputOutputBinding(_MOFBase):
    _ABSTRACT = False
    # association end of A_ioBinding_callableElement (opposite of CallableElement.ioBinding)
    _DECL = {
    'inputDataRef': _Ref('inputDataRef', "InputSet", assoc="A_inputDataRef_inputOutputBinding"),
    'outputDataRef': _Ref('outputDataRef', "OutputSet", assoc="A_outputDataRef_inputOutputBinding"),
    'operationRef': _Ref('operationRef', "Operation", assoc="A_operationRef_ioBinding"),
    'callableElement': _Ref('callableElement', "CallableElement", assoc="A_ioBinding_callableElement"),
    }
    _OPPS = {
        'inputDataRef': ('inputOutputBinding',),
        'outputDataRef': ('inputOutputBinding',),
        'operationRef': ('ioBinding',),
        'callableElement': ('ioBinding',),
    }

class InputOutputSpecification(BaseElement):
    _ABSTRACT = False
    # association end of A_ioSpecification_callableElement (opposite of CallableElement.ioSpecification)
    # association end of A_ioSpecification_activity (opposite of Activity.ioSpecification)
    _DECL = {
    'inputSets': _Ref('inputSets', "InputSet", multi=True, lo=0, hi='*', composite=True, assoc="A_inputSets_inputOutputSpecification"),
    'outputSets': _Ref('outputSets', "OutputSet", multi=True, lo=0, hi='*', composite=True, assoc="A_outputSets_inputOutputSpecification"),
    'dataInputs': _Ref('dataInputs', "DataInput", multi=True, lo=0, hi='*', composite=True, assoc="A_dataInputs_inputOutputSpecification"),
    'dataOutputs': _Ref('dataOutputs', "DataOutput", multi=True, lo=0, hi='*', composite=True, assoc="A_dataOutputs_inputOutputSpecification"),
    'callableElement': _Ref('callableElement', "CallableElement", assoc="A_ioSpecification_callableElement"),
    'activity': _Ref('activity', "Activity", assoc="A_ioSpecification_activity"),
    }
    _OPPS = {
        'inputSets': ('inputOutputSpecification',),
        'outputSets': ('inputOutputSpecification',),
        'dataInputs': ('inputOutputSpecification',),
        'dataOutputs': ('inputOutputSpecification',),
        'callableElement': ('ioSpecification',),
        'activity': ('ioSpecification',),
    }

class InputSet(BaseElement):
    _ABSTRACT = False
    # association end of A_inputSet_throwEvent (opposite of ThrowEvent.inputSet)
    # association end of A_inputSets_inputOutputSpecification (opposite of InputOutputSpecification.inputSets)
    # association end of A_inputDataRef_inputOutputBinding (opposite of InputOutputBinding.inputDataRef)
    _DECL = {
    'name': _Ref('name', str),
    'dataInputRefs': _Ref('dataInputRefs', "DataInput", multi=True, lo=0, hi='*', assoc="A_dataInputRefs_inputSetRefs"),
    'optionalInputRefs': _Ref('optionalInputRefs', "DataInput", multi=True, lo=0, hi='*', assoc="A_optionalInputRefs_inputSetWithOptional"),
    'whileExecutingInputRefs': _Ref('whileExecutingInputRefs', "DataInput", multi=True, lo=0, hi='*', assoc="A_whileExecutingInputRefs_inputSetWithWhileExecuting"),
    'outputSetRefs': _Ref('outputSetRefs', "OutputSet", multi=True, lo=0, hi='*', assoc="A_inputSetRefs_outputSetRefs"),
    'throwEvent': _Ref('throwEvent', "ThrowEvent", assoc="A_inputSet_throwEvent"),
    'inputOutputSpecification': _Ref('inputOutputSpecification', "InputOutputSpecification", assoc="A_inputSets_inputOutputSpecification"),
    'inputOutputBinding': _Ref('inputOutputBinding', "InputOutputBinding", multi=True, lo=0, hi='*', assoc="A_inputDataRef_inputOutputBinding"),
    }
    _OPPS = {
        'dataInputRefs': ('inputSetRefs',),
        'optionalInputRefs': ('inputSetWithOptional',),
        'whileExecutingInputRefs': ('inputSetWithWhileExecuting',),
        'outputSetRefs': ('inputSetRefs',),
        'throwEvent': ('inputSet',),
        'inputOutputSpecification': ('inputSets',),
        'inputOutputBinding': ('inputDataRef',),
    }

class Interface(RootElement):
    _ABSTRACT = False
    # association end of A_supportedInterfaceRefs_callableElements (opposite of CallableElement.supportedInterfaceRefs)
    # association end of A_interfaceRefs_participant (opposite of Participant.interfaceRefs)
    _DECL = {
    'name': _Ref('name', str),
    'operations': _Ref('operations', "Operation", multi=True, lo=0, hi='*', composite=True, assoc="A_operations_interface"),
    'implementationRef': _Ref('implementationRef', 'xml.dom.Element'),
    'callableElements': _Ref('callableElements', "CallableElement", multi=True, lo=0, hi='*', assoc="A_supportedInterfaceRefs_callableElements"),
    'participant': _Ref('participant', "Participant", multi=True, lo=0, hi='*', assoc="A_interfaceRefs_participant"),
    }
    _OPPS = {
        'operations': ('interface',),
        'callableElements': ('supportedInterfaceRefs',),
        'participant': ('interfaceRefs',),
    }

class IntermediateCatchEvent(CatchEvent):
    _ABSTRACT = False

class IntermediateThrowEvent(ThrowEvent):
    _ABSTRACT = False

class ItemDefinition(RootElement):
    _ABSTRACT = False
    # default: 'false'
    # association end of A_structureRef_signal (opposite of Signal.structureRef)
    # association end of A_structureRef_escalation (opposite of Escalation.structureRef)
    # association end of A_itemSubjectRef_itemAwareElement (opposite of ItemAwareElement.itemSubjectRef)
    # association end of A_structureRef_error (opposite of Error.structureRef)
    # association end of A_evaluatesToTypeRef_formalExpression (opposite of FormalExpression.evaluatesToTypeRef)
    # association end of A_type_correlationProperty (opposite of CorrelationProperty.type)
    # association end of A_type_resourceParameter (opposite of ResourceParameter.type)
    # association end of A_itemRef_message (opposite of Message.itemRef)
    _DECL = {
    'itemKind': _Ref('itemKind', "ItemKind"),
    'structureRef': _Ref('structureRef', 'xml.dom.Element'),
    'isCollection': _Ref('isCollection', bool),
    'import': _Ref('import', "Import", assoc="A_import_itemDefinition"),
    'signal': _Ref('signal', "Signal", multi=True, lo=0, hi='*', assoc="A_structureRef_signal"),
    'escalation': _Ref('escalation', "Escalation", multi=True, lo=0, hi='*', assoc="A_structureRef_escalation"),
    'itemAwareElement': _Ref('itemAwareElement', "ItemAwareElement", multi=True, lo=0, hi='*', assoc="A_itemSubjectRef_itemAwareElement"),
    'error': _Ref('error', "Error", multi=True, lo=0, hi='*', assoc="A_structureRef_error"),
    'formalExpression': _Ref('formalExpression', "FormalExpression", multi=True, lo=0, hi='*', assoc="A_evaluatesToTypeRef_formalExpression"),
    'correlationProperty': _Ref('correlationProperty', "CorrelationProperty", multi=True, lo=0, hi='*', assoc="A_type_correlationProperty"),
    'resourceParameter': _Ref('resourceParameter', "ResourceParameter", multi=True, lo=0, hi='*', assoc="A_type_resourceParameter"),
    'message': _Ref('message', "Message", multi=True, lo=0, hi='*', assoc="A_itemRef_message"),
    }
    _OPPS = {
        'import': ('itemDefinition',),
        'signal': ('structureRef',),
        'escalation': ('structureRef',),
        'itemAwareElement': ('itemSubjectRef',),
        'error': ('structureRef',),
        'formalExpression': ('evaluatesToTypeRef',),
        'correlationProperty': ('type',),
        'resourceParameter': ('type',),
        'message': ('itemRef',),
    }

class Lane(BaseElement):
    _ABSTRACT = False
    # association end of A_lanes_laneSet (opposite of LaneSet.lanes)
    _DECL = {
    'name': _Ref('name', str),
    'childLaneSet': _Ref('childLaneSet', "LaneSet", composite=True, assoc="A_childLaneSet_parentLane"),
    'partitionElementRef': _Ref('partitionElementRef', "BaseElement", assoc="A_partitionElementRef_lane"),
    'flowNodeRefs': _Ref('flowNodeRefs', "FlowNode", multi=True, lo=0, hi='*', assoc="A_flowNodeRefs_lanes"),
    'partitionElement': _Ref('partitionElement', "BaseElement", composite=True, assoc="A_partitionElement_lane"),
    'laneSet': _Ref('laneSet', "LaneSet", assoc="A_lanes_laneSet"),
    }
    _OPPS = {
        'childLaneSet': ('parentLane',),
        'partitionElementRef': ('lane',),
        'flowNodeRefs': ('lanes',),
        'partitionElement': ('lane',),
        'laneSet': ('lanes',),
    }

class LaneSet(BaseElement):
    _ABSTRACT = False
    # association end of A_childLaneSet_parentLane (opposite of Lane.childLaneSet)
    # association end of A_laneSets_flowElementsContainer (opposite of FlowElementsContainer.laneSets)
    _DECL = {
    'lanes': _Ref('lanes', "Lane", multi=True, lo=0, hi='*', composite=True, assoc="A_lanes_laneSet"),
    'name': _Ref('name', str),
    'parentLane': _Ref('parentLane', "Lane", assoc="A_childLaneSet_parentLane"),
    'flowElementsContainer': _Ref('flowElementsContainer', "FlowElementsContainer", assoc="A_laneSets_flowElementsContainer"),
    }
    _OPPS = {
        'lanes': ('laneSet',),
        'parentLane': ('childLaneSet',),
        'flowElementsContainer': ('laneSets',),
    }

class LinkEventDefinition(EventDefinition):
    _ABSTRACT = False
    _DECL = {
    'name': _Ref('name', str),
    'target': _Ref('target', "LinkEventDefinition", assoc="A_target_source"),
    'source': _Ref('source', "LinkEventDefinition", multi=True, lo=0, hi='*', assoc="A_target_source"),
    }
    _OPPS = {
        'target': ('source',),
        'source': ('target',),
    }

class LoopCharacteristics(BaseElement):
    _ABSTRACT = True
    # association end of A_loopCharacteristics_activity (opposite of Activity.loopCharacteristics)
    _DECL = {
    'activity': _Ref('activity', "Activity", assoc="A_loopCharacteristics_activity"),
    }
    _OPPS = {
        'activity': ('loopCharacteristics',),
    }

class ManualTask(Task):
    _ABSTRACT = False

class Message(RootElement):
    _ABSTRACT = False
    # association end of A_inMessageRef_operation (opposite of Operation.inMessageRef)
    # association end of A_messageRef_messageEventDefinition (opposite of MessageEventDefinition.messageRef)
    # association end of A_messageRef_correlationPropertyRetrievalExpression (opposite of CorrelationPropertyRetrievalExpression.messageRef)
    # association end of A_messageRef_messageFlow (opposite of MessageFlow.messageRef)
    # association end of A_messageRef_sendTask (opposite of SendTask.messageRef)
    # association end of A_messageRef_receiveTask (opposite of ReceiveTask.messageRef)
    _DECL = {
    'name': _Ref('name', str),
    'itemRef': _Ref('itemRef', "ItemDefinition", assoc="A_itemRef_message"),
    'operation': _Ref('operation', "Operation", multi=True, lo=0, hi='*', assoc="A_inMessageRef_operation"),
    'messageEventDefinition': _Ref('messageEventDefinition', "MessageEventDefinition", multi=True, lo=0, hi='*', assoc="A_messageRef_messageEventDefinition"),
    'correlationPropertyRetrievalExpression': _Ref('correlationPropertyRetrievalExpression', "CorrelationPropertyRetrievalExpression", multi=True, lo=0, hi='*', assoc="A_messageRef_correlationPropertyRetrievalExpression"),
    'messageFlow': _Ref('messageFlow', "MessageFlow", multi=True, lo=0, hi='*', assoc="A_messageRef_messageFlow"),
    'sendTask': _Ref('sendTask', "SendTask", multi=True, lo=0, hi='*', assoc="A_messageRef_sendTask"),
    'receiveTask': _Ref('receiveTask', "ReceiveTask", multi=True, lo=0, hi='*', assoc="A_messageRef_receiveTask"),
    }
    _OPPS = {
        'itemRef': ('message',),
        'operation': ('inMessageRef', 'outMessageRef'),
        'messageEventDefinition': ('messageRef',),
        'correlationPropertyRetrievalExpression': ('messageRef',),
        'messageFlow': ('messageRef',),
        'sendTask': ('messageRef',),
        'receiveTask': ('messageRef',),
    }

class MessageEventDefinition(EventDefinition):
    _ABSTRACT = False
    _DECL = {
    'messageRef': _Ref('messageRef', "Message", assoc="A_messageRef_messageEventDefinition"),
    'operationRef': _Ref('operationRef', "Operation", assoc="A_operationRef_messageEventDefinition"),
    }
    _OPPS = {
        'messageRef': ('messageEventDefinition',),
        'operationRef': ('messageEventDefinition',),
    }

class MessageFlow(BaseElement):
    _ABSTRACT = False
    # association end of A_messageFlowRefs_communication (opposite of ConversationNode.messageFlowRefs)
    # association end of A_innerMessageFlowRef_messageFlowAssociation (opposite of MessageFlowAssociation.innerMessageFlowRef)
    # association end of A_messageFlows_collaboration (opposite of Collaboration.messageFlows)
    # association end of A_messageFlowRef_choreographyTask (opposite of ChoreographyTask.messageFlowRef)
    _DECL = {
    'name': _Ref('name', str),
    'sourceRef': _Ref('sourceRef', "InteractionNode", assoc="A_sourceRef_messageFlow"),
    'targetRef': _Ref('targetRef', "InteractionNode", assoc="A_targetRef_messageFlow"),
    'messageRef': _Ref('messageRef', "Message", assoc="A_messageRef_messageFlow"),
    'communication': _Ref('communication', "ConversationNode", multi=True, lo=0, hi='*', assoc="A_messageFlowRefs_communication"),
    'messageFlowAssociation': _Ref('messageFlowAssociation', "MessageFlowAssociation", multi=True, lo=0, hi='*', assoc="A_innerMessageFlowRef_messageFlowAssociation"),
    'collaboration': _Ref('collaboration', "Collaboration", assoc="A_messageFlows_collaboration"),
    'choreographyTask': _Ref('choreographyTask', "ChoreographyTask", assoc="A_messageFlowRef_choreographyTask"),
    }
    _OPPS = {
        'sourceRef': ('messageFlow',),
        'targetRef': ('messageFlow',),
        'messageRef': ('messageFlow',),
        'communication': ('messageFlowRefs',),
        'messageFlowAssociation': ('innerMessageFlowRef', 'outerMessageFlowRef'),
        'collaboration': ('messageFlows',),
        'choreographyTask': ('messageFlowRef',),
    }

class MessageFlowAssociation(BaseElement):
    _ABSTRACT = False
    # association end of A_messageFlowAssociations_collaboration (opposite of Collaboration.messageFlowAssociations)
    _DECL = {
    'innerMessageFlowRef': _Ref('innerMessageFlowRef', "MessageFlow", assoc="A_innerMessageFlowRef_messageFlowAssociation"),
    'outerMessageFlowRef': _Ref('outerMessageFlowRef', "MessageFlow", assoc="A_outerMessageFlowRef_messageFlowAssociation"),
    'collaboration': _Ref('collaboration', "Collaboration", assoc="A_messageFlowAssociations_collaboration"),
    }
    _OPPS = {
        'innerMessageFlowRef': ('messageFlowAssociation',),
        'outerMessageFlowRef': ('messageFlowAssociation',),
        'collaboration': ('messageFlowAssociations',),
    }

class Monitoring(BaseElement):
    _ABSTRACT = False
    # association end of A_monitoring_process (opposite of Process.monitoring)
    # association end of A_monitoring_flowElement (opposite of FlowElement.monitoring)
    _DECL = {
    'process': _Ref('process', "Process", assoc="A_monitoring_process"),
    'flowElement': _Ref('flowElement', "FlowElement", assoc="A_monitoring_flowElement"),
    }
    _OPPS = {
        'process': ('monitoring',),
        'flowElement': ('monitoring',),
    }

class MultiInstanceLoopCharacteristics(LoopCharacteristics):
    _ABSTRACT = False
    # default: 'false'
    # default: 'All'
    _DECL = {
    'isSequential': _Ref('isSequential', bool),
    'behavior': _Ref('behavior', "MultiInstanceBehavior"),
    'loopCardinality': _Ref('loopCardinality', "Expression", composite=True, assoc="A_loopCardinality_multiInstanceLoopCharacteristics"),
    'loopDataInputRef': _Ref('loopDataInputRef', "ItemAwareElement", assoc="A_loopDataInputRef_multiInstanceLoopCharacteristics"),
    'loopDataOutputRef': _Ref('loopDataOutputRef', "ItemAwareElement", assoc="A_loopDataOutputRef_multiInstanceLoopCharacteristics"),
    'inputDataItem': _Ref('inputDataItem', "DataInput", composite=True, assoc="A_inputDataItem_multiInstanceLoopCharacteristics"),
    'outputDataItem': _Ref('outputDataItem', "DataOutput", composite=True, assoc="A_outputDataItem_multiInstanceLoopCharacteristics"),
    'completionCondition': _Ref('completionCondition', "Expression", composite=True, assoc="A_completionCondition_multiInstanceLoopCharacteristics"),
    'complexBehaviorDefinition': _Ref('complexBehaviorDefinition', "ComplexBehaviorDefinition", multi=True, lo=0, hi='*', composite=True, assoc="A_complexBehaviorDefinition_multiInstanceLoopCharacteristics"),
    'oneBehaviorEventRef': _Ref('oneBehaviorEventRef', "EventDefinition", assoc="A_oneBehaviorEventRef_multiInstanceLoopCharacteristics"),
    'noneBehaviorEventRef': _Ref('noneBehaviorEventRef', "EventDefinition", assoc="A_noneBehaviorEventRef_multiInstanceLoopCharacteristics"),
    }
    _OPPS = {
        'loopCardinality': ('multiInstanceLoopCharacteristics',),
        'loopDataInputRef': ('multiInstanceLoopCharacteristics',),
        'loopDataOutputRef': ('multiInstanceLoopCharacteristics',),
        'inputDataItem': ('multiInstanceLoopCharacteristics',),
        'outputDataItem': ('multiInstanceLoopCharacteristics',),
        'completionCondition': ('multiInstanceLoopCharacteristics',),
        'complexBehaviorDefinition': ('multiInstanceLoopCharacteristics',),
        'oneBehaviorEventRef': ('multiInstanceLoopCharacteristics',),
        'noneBehaviorEventRef': ('multiInstanceLoopCharacteristics',),
    }

class Operation(BaseElement):
    _ABSTRACT = False
    # association end of A_operations_interface (opposite of Interface.operations)
    # association end of A_operationRef_messageEventDefinition (opposite of MessageEventDefinition.operationRef)
    # association end of A_operationRef_ioBinding (opposite of InputOutputBinding.operationRef)
    # association end of A_operationRef_serviceTask (opposite of ServiceTask.operationRef)
    # association end of A_operationRef_receiveTask (opposite of ReceiveTask.operationRef)
    # association end of A_operationRef_sendTask (opposite of SendTask.operationRef)
    _DECL = {
    'name': _Ref('name', str),
    'inMessageRef': _Ref('inMessageRef', "Message", assoc="A_inMessageRef_operation"),
    'outMessageRef': _Ref('outMessageRef', "Message", assoc="A_outMessageRef_operation"),
    'errorRefs': _Ref('errorRefs', "Error", multi=True, lo=0, hi='*', assoc="A_errorRefs_operation"),
    'implementationRef': _Ref('implementationRef', 'xml.dom.Element'),
    'interface': _Ref('interface', "Interface", assoc="A_operations_interface"),
    'messageEventDefinition': _Ref('messageEventDefinition', "MessageEventDefinition", multi=True, lo=0, hi='*', assoc="A_operationRef_messageEventDefinition"),
    'ioBinding': _Ref('ioBinding', "InputOutputBinding", multi=True, lo=0, hi='*', assoc="A_operationRef_ioBinding"),
    'serviceTask': _Ref('serviceTask', "ServiceTask", multi=True, lo=0, hi='*', assoc="A_operationRef_serviceTask"),
    'receiveTask': _Ref('receiveTask', "ReceiveTask", multi=True, lo=0, hi='*', assoc="A_operationRef_receiveTask"),
    'sendTask': _Ref('sendTask', "SendTask", multi=True, lo=0, hi='*', assoc="A_operationRef_sendTask"),
    }
    _OPPS = {
        'inMessageRef': ('operation',),
        'outMessageRef': ('operation',),
        'errorRefs': ('operation',),
        'interface': ('operations',),
        'messageEventDefinition': ('operationRef',),
        'ioBinding': ('operationRef',),
        'serviceTask': ('operationRef',),
        'receiveTask': ('operationRef',),
        'sendTask': ('operationRef',),
    }

class OutputSet(BaseElement):
    _ABSTRACT = False
    # association end of A_outputSet_catchEvent (opposite of CatchEvent.outputSet)
    # association end of A_outputSets_inputOutputSpecification (opposite of InputOutputSpecification.outputSets)
    # association end of A_outputDataRef_inputOutputBinding (opposite of InputOutputBinding.outputDataRef)
    _DECL = {
    'dataOutputRefs': _Ref('dataOutputRefs', "DataOutput", multi=True, lo=0, hi='*', assoc="A_dataOutputRefs_outputSetRefs"),
    'name': _Ref('name', str),
    'inputSetRefs': _Ref('inputSetRefs', "InputSet", multi=True, lo=0, hi='*', assoc="A_inputSetRefs_outputSetRefs"),
    'optionalOutputRefs': _Ref('optionalOutputRefs', "DataOutput", multi=True, lo=0, hi='*', assoc="A_outputSetWithOptional_optionalOutputRefs"),
    'whileExecutingOutputRefs': _Ref('whileExecutingOutputRefs', "DataOutput", multi=True, lo=0, hi='*', assoc="A_outputSetWithWhileExecuting_whileExecutingOutputRefs"),
    'catchEvent': _Ref('catchEvent', "CatchEvent", assoc="A_outputSet_catchEvent"),
    'inputOutputSpecification': _Ref('inputOutputSpecification', "InputOutputSpecification", assoc="A_outputSets_inputOutputSpecification"),
    'inputOutputBinding': _Ref('inputOutputBinding', "InputOutputBinding", multi=True, lo=0, hi='*', assoc="A_outputDataRef_inputOutputBinding"),
    }
    _OPPS = {
        'dataOutputRefs': ('outputSetRefs',),
        'inputSetRefs': ('outputSetRefs',),
        'optionalOutputRefs': ('outputSetWithOptional',),
        'whileExecutingOutputRefs': ('outputSetWithWhileExecuting',),
        'catchEvent': ('outputSet',),
        'inputOutputSpecification': ('outputSets',),
        'inputOutputBinding': ('outputDataRef',),
    }

class ParallelGateway(Gateway):
    _ABSTRACT = False

class Participant(InteractionNode, BaseElement):
    _ABSTRACT = False
    # association end of A_participantRefs_conversationNode (opposite of ConversationNode.participantRefs)
    # association end of A_innerParticipantRef_participantAssociation (opposite of ParticipantAssociation.innerParticipantRef)
    # association end of A_partnerEntityRef_participantRef (opposite of PartnerEntity.participantRef)
    # association end of A_partnerRoleRef_participantRef (opposite of PartnerRole.participantRef)
    # association end of A_participants_collaboration (opposite of Collaboration.participants)
    # association end of A_initiatingParticipantRef_choreographyActivity (opposite of ChoreographyActivity.initiatingParticipantRef)
    # association end of A_initiatingParticipantRef_globalChoreographyTask (opposite of GlobalChoreographyTask.initiatingParticipantRef)
    _DECL = {
    'name': _Ref('name', str),
    'interfaceRefs': _Ref('interfaceRefs', "Interface", multi=True, lo=0, hi='*', assoc="A_interfaceRefs_participant"),
    'participantMultiplicity': _Ref('participantMultiplicity', "ParticipantMultiplicity", composite=True, assoc="A_participantMultiplicity_participant"),
    'endPointRefs': _Ref('endPointRefs', "EndPoint", multi=True, lo=0, hi='*', assoc="A_endPointRefs_participant"),
    'processRef': _Ref('processRef', "Process", assoc="A_processRef_participant"),
    'conversationNode': _Ref('conversationNode', "ConversationNode", multi=True, lo=0, hi='*', assoc="A_participantRefs_conversationNode"),
    'participantAssociation': _Ref('participantAssociation', "ParticipantAssociation", multi=True, lo=0, hi='*', assoc="A_innerParticipantRef_participantAssociation"),
    'partnerEntityRef': _Ref('partnerEntityRef', "PartnerEntity", multi=True, lo=0, hi='*', assoc="A_partnerEntityRef_participantRef"),
    'partnerRoleRef': _Ref('partnerRoleRef', "PartnerRole", multi=True, lo=0, hi='*', assoc="A_partnerRoleRef_participantRef"),
    'collaboration': _Ref('collaboration', "Collaboration", assoc="A_participants_collaboration"),
    'choreographyActivity': _Ref('choreographyActivity', "ChoreographyActivity", multi=True, lo=0, hi='*', assoc="A_initiatingParticipantRef_choreographyActivity"),
    'globalChoreographyTask': _Ref('globalChoreographyTask', "GlobalChoreographyTask", multi=True, lo=0, hi='*', assoc="A_initiatingParticipantRef_globalChoreographyTask"),
    }
    _OPPS = {
        'interfaceRefs': ('participant',),
        'participantMultiplicity': ('participant',),
        'endPointRefs': ('participant',),
        'processRef': ('participant',),
        'conversationNode': ('participantRefs',),
        'participantAssociation': ('innerParticipantRef', 'outerParticipantRef'),
        'partnerEntityRef': ('participantRef',),
        'partnerRoleRef': ('participantRef',),
        'collaboration': ('participants',),
        'choreographyActivity': ('initiatingParticipantRef', 'participantRefs'),
        'globalChoreographyTask': ('initiatingParticipantRef',),
    }

class ParticipantAssociation(BaseElement):
    _ABSTRACT = False
    # association end of A_participantAssociations_callConversation (opposite of CallConversation.participantAssociations)
    # association end of A_participantAssociations_collaboration (opposite of Collaboration.participantAssociations)
    # association end of A_participantAssociations_callChoreographyActivity (opposite of CallChoreography.participantAssociations)
    _DECL = {
    'innerParticipantRef': _Ref('innerParticipantRef', "Participant", assoc="A_innerParticipantRef_participantAssociation"),
    'outerParticipantRef': _Ref('outerParticipantRef', "Participant", assoc="A_outerParticipantRef_participantAssociation"),
    'callConversation': _Ref('callConversation', "CallConversation", assoc="A_participantAssociations_callConversation"),
    'collaboration': _Ref('collaboration', "Collaboration", assoc="A_participantAssociations_collaboration"),
    'callChoreographyActivity': _Ref('callChoreographyActivity', "CallChoreography", assoc="A_participantAssociations_callChoreographyActivity"),
    }
    _OPPS = {
        'innerParticipantRef': ('participantAssociation',),
        'outerParticipantRef': ('participantAssociation',),
        'callConversation': ('participantAssociations',),
        'collaboration': ('participantAssociations',),
        'callChoreographyActivity': ('participantAssociations',),
    }

class ParticipantMultiplicity(_MOFBase):
    _ABSTRACT = False
    # default: '0'
    # default: '1'
    # association end of A_participantMultiplicity_participant (opposite of Participant.participantMultiplicity)
    _DECL = {
    'minimum': _Ref('minimum', int),
    'maximum': _Ref('maximum', int),
    'participant': _Ref('participant', "Participant", assoc="A_participantMultiplicity_participant"),
    }
    _OPPS = {
        'participant': ('participantMultiplicity',),
    }

class PartnerEntity(RootElement):
    _ABSTRACT = False
    _DECL = {
    'name': _Ref('name', str),
    'participantRef': _Ref('participantRef', "Participant", multi=True, lo=0, hi='*', assoc="A_partnerEntityRef_participantRef"),
    }
    _OPPS = {
        'participantRef': ('partnerEntityRef',),
    }

class PartnerRole(RootElement):
    _ABSTRACT = False
    _DECL = {
    'name': _Ref('name', str),
    'participantRef': _Ref('participantRef', "Participant", multi=True, lo=0, hi='*', assoc="A_partnerRoleRef_participantRef"),
    }
    _OPPS = {
        'participantRef': ('partnerRoleRef',),
    }

class PotentialOwner(HumanPerformer):
    _ABSTRACT = False

class Process(FlowElementsContainer, CallableElement):
    _ABSTRACT = False
    # association end of A_supports_process (opposite of Process.supports)
    # association end of A_processRef_participant (opposite of Participant.processRef)
    _DECL = {
    'processType': _Ref('processType', "ProcessType"),
    'isClosed': _Ref('isClosed', bool),
    'auditing': _Ref('auditing', "Auditing", composite=True, assoc="A_auditing_process"),
    'monitoring': _Ref('monitoring', "Monitoring", composite=True, assoc="A_monitoring_process"),
    'properties': _Ref('properties', "Property", multi=True, lo=0, hi='*', composite=True, assoc="A_properties_process"),
    'supports': _Ref('supports', "Process", multi=True, lo=0, hi='*', assoc="A_supports_process"),
    'definitionalCollaborationRef': _Ref('definitionalCollaborationRef', "Collaboration", assoc="A_definitionalCollaborationRef_process"),
    'isExecutable': _Ref('isExecutable', bool),
    'resources': _Ref('resources', "ResourceRole", multi=True, lo=0, hi='*', composite=True, assoc="A_resources_process"),
    'artifacts': _Ref('artifacts', "Artifact", multi=True, lo=0, hi='*', composite=True, assoc="A_artifacts_process"),
    'correlationSubscriptions': _Ref('correlationSubscriptions', "CorrelationSubscription", multi=True, lo=0, hi='*', composite=True, assoc="A_correlationSubscriptions_process"),
    'process': _Ref('process', "Process", multi=True, lo=0, hi='*', assoc="A_supports_process"),
    'participant': _Ref('participant', "Participant", multi=True, lo=0, hi='*', assoc="A_processRef_participant"),
    }
    _OPPS = {
        'auditing': ('process',),
        'monitoring': ('process',),
        'properties': ('process',),
        'supports': ('process',),
        'definitionalCollaborationRef': ('process',),
        'resources': ('process',),
        'artifacts': ('process',),
        'correlationSubscriptions': ('process',),
        'process': ('supports',),
        'participant': ('processRef',),
    }

class Property(ItemAwareElement):
    _ABSTRACT = False
    # association end of A_properties_process (opposite of Process.properties)
    # association end of A_properties_event (opposite of Event.properties)
    # association end of A_properties_activity (opposite of Activity.properties)
    _DECL = {
    'name': _Ref('name', str),
    'process': _Ref('process', "Process", assoc="A_properties_process"),
    'event': _Ref('event', "Event", assoc="A_properties_event"),
    'activity': _Ref('activity', "Activity", assoc="A_properties_activity"),
    }
    _OPPS = {
        'process': ('properties',),
        'event': ('properties',),
        'activity': ('properties',),
    }

class ReceiveTask(Task):
    _ABSTRACT = False
    # default: 'false'
    _DECL = {
    'implementation': _Ref('implementation', str),
    'instantiate': _Ref('instantiate', bool),
    'operationRef': _Ref('operationRef', "Operation", assoc="A_operationRef_receiveTask"),
    'messageRef': _Ref('messageRef', "Message", assoc="A_messageRef_receiveTask"),
    }
    _OPPS = {
        'operationRef': ('receiveTask',),
        'messageRef': ('receiveTask',),
    }

class Relationship(BaseElement):
    _ABSTRACT = False
    # association end of A_relationships_definition (opposite of Definitions.relationships)
    _DECL = {
    'type': _Ref('type', str),
    'direction': _Ref('direction', "RelationshipDirection"),
    'sources': _Ref('sources', 'xml.dom.Element', multi=True, lo=0, hi='*', assoc="A_sources_relationship"),
    'targets': _Ref('targets', 'xml.dom.Element', multi=True, lo=0, hi='*', assoc="A_targets_relationship"),
    'definition': _Ref('definition', "Definitions", assoc="A_relationships_definition"),
    }
    _OPPS = {
        'sources': ('relationship',),
        'targets': ('relationship',),
        'definition': ('relationships',),
    }

class Rendering(BaseElement):
    _ABSTRACT = False
    # association end of A_renderings_usertask (opposite of UserTask.renderings)
    # association end of A_renderings_globalUserTask (opposite of GlobalUserTask.renderings)
    _DECL = {
    'usertask': _Ref('usertask', "UserTask", assoc="A_renderings_usertask"),
    'globalUserTask': _Ref('globalUserTask', "GlobalUserTask", assoc="A_renderings_globalUserTask"),
    }
    _OPPS = {
        'usertask': ('renderings',),
        'globalUserTask': ('renderings',),
    }

class Resource(RootElement):
    _ABSTRACT = False
    # association end of A_resourceRef_activityResource (opposite of ResourceRole.resourceRef)
    _DECL = {
    'name': _Ref('name', str),
    'resourceParameters': _Ref('resourceParameters', "ResourceParameter", multi=True, lo=0, hi='*', composite=True, assoc="A_resourceParameters_resource"),
    'activityResource': _Ref('activityResource', "ResourceRole", multi=True, lo=0, hi='*', assoc="A_resourceRef_activityResource"),
    }
    _OPPS = {
        'resourceParameters': ('resource',),
        'activityResource': ('resourceRef',),
    }

class ResourceAssignmentExpression(_MOFBase):
    _ABSTRACT = False
    # association end of A_resourceAssignmentExpression_activityResource (opposite of ResourceRole.resourceAssignmentExpression)
    _DECL = {
    'expression': _Ref('expression', "Expression", composite=True, assoc="A_expression_resourceAssignmentExpression"),
    'activityResource': _Ref('activityResource', "ResourceRole", assoc="A_resourceAssignmentExpression_activityResource"),
    }
    _OPPS = {
        'expression': ('resourceAssignmentExpression',),
        'activityResource': ('resourceAssignmentExpression',),
    }

class ResourceParameter(BaseElement):
    _ABSTRACT = False
    # association end of A_resourceParameters_resource (opposite of Resource.resourceParameters)
    # association end of A_parameterRef_resourceParameterBinding (opposite of ResourceParameterBinding.parameterRef)
    _DECL = {
    'name': _Ref('name', str),
    'isRequired': _Ref('isRequired', bool),
    'type': _Ref('type', "ItemDefinition", assoc="A_type_resourceParameter"),
    'resource': _Ref('resource', "Resource", assoc="A_resourceParameters_resource"),
    'resourceParameterBinding': _Ref('resourceParameterBinding', "ResourceParameterBinding", multi=True, lo=0, hi='*', assoc="A_parameterRef_resourceParameterBinding"),
    }
    _OPPS = {
        'type': ('resourceParameter',),
        'resource': ('resourceParameters',),
        'resourceParameterBinding': ('parameterRef',),
    }

class ResourceParameterBinding(_MOFBase):
    _ABSTRACT = False
    # association end of A_resourceParameterBindings_activityResource (opposite of ResourceRole.resourceParameterBindings)
    _DECL = {
    'expression': _Ref('expression', "Expression", composite=True, assoc="A_expression_resourceParameterBinding"),
    'parameterRef': _Ref('parameterRef', "ResourceParameter", assoc="A_parameterRef_resourceParameterBinding"),
    'activityResource': _Ref('activityResource', "ResourceRole", assoc="A_resourceParameterBindings_activityResource"),
    }
    _OPPS = {
        'expression': ('resourceParameterBinding',),
        'parameterRef': ('resourceParameterBinding',),
        'activityResource': ('resourceParameterBindings',),
    }

class ScriptTask(Task):
    _ABSTRACT = False
    _DECL = {
    'scriptFormat': _Ref('scriptFormat', str),
    'script': _Ref('script', str),
    }

class SendTask(Task):
    _ABSTRACT = False
    _DECL = {
    'implementation': _Ref('implementation', str),
    'operationRef': _Ref('operationRef', "Operation", assoc="A_operationRef_sendTask"),
    'messageRef': _Ref('messageRef', "Message", assoc="A_messageRef_sendTask"),
    }
    _OPPS = {
        'operationRef': ('sendTask',),
        'messageRef': ('sendTask',),
    }

class SequenceFlow(FlowElement):
    _ABSTRACT = False
    # association end of A_default_inclusiveGateway (opposite of InclusiveGateway.default)
    # association end of A_default_exclusiveGateway (opposite of ExclusiveGateway.default)
    # association end of A_default_complexGateway (opposite of ComplexGateway.default)
    # association end of A_default_activity (opposite of Activity.default)
    _DECL = {
    'isImmediate': _Ref('isImmediate', bool),
    'conditionExpression': _Ref('conditionExpression', "Expression", composite=True, assoc="A_conditionExpression_sequenceFlow"),
    'sourceRef': _Ref('sourceRef', "FlowNode", assoc="A_sourceRef_outgoing_flow"),
    'targetRef': _Ref('targetRef', "FlowNode", assoc="A_targetRef_incoming_flow"),
    'inclusiveGateway': _Ref('inclusiveGateway', "InclusiveGateway", multi=True, lo=0, hi='*', assoc="A_default_inclusiveGateway"),
    'exclusiveGateway': _Ref('exclusiveGateway', "ExclusiveGateway", multi=True, lo=0, hi='*', assoc="A_default_exclusiveGateway"),
    'complexGateway': _Ref('complexGateway', "ComplexGateway", multi=True, lo=0, hi='*', assoc="A_default_complexGateway"),
    'activity': _Ref('activity', "Activity", assoc="A_default_activity"),
    }
    _OPPS = {
        'conditionExpression': ('sequenceFlow',),
        'sourceRef': ('outgoing',),
        'targetRef': ('incoming',),
        'inclusiveGateway': ('default',),
        'exclusiveGateway': ('default',),
        'complexGateway': ('default',),
        'activity': ('default',),
    }

class ServiceTask(Task):
    _ABSTRACT = False
    _DECL = {
    'implementation': _Ref('implementation', str),
    'operationRef': _Ref('operationRef', "Operation", assoc="A_operationRef_serviceTask"),
    }
    _OPPS = {
        'operationRef': ('serviceTask',),
    }

class Signal(RootElement):
    _ABSTRACT = False
    # association end of A_signalRef_signalEventDefinition (opposite of SignalEventDefinition.signalRef)
    _DECL = {
    'structureRef': _Ref('structureRef', "ItemDefinition", assoc="A_structureRef_signal"),
    'name': _Ref('name', str),
    'signalEventDefinition': _Ref('signalEventDefinition', "SignalEventDefinition", multi=True, lo=0, hi='*', assoc="A_signalRef_signalEventDefinition"),
    }
    _OPPS = {
        'structureRef': ('signal',),
        'signalEventDefinition': ('signalRef',),
    }

class SignalEventDefinition(EventDefinition):
    _ABSTRACT = False
    _DECL = {
    'signalRef': _Ref('signalRef', "Signal", assoc="A_signalRef_signalEventDefinition"),
    }
    _OPPS = {
        'signalRef': ('signalEventDefinition',),
    }

class StandardLoopCharacteristics(LoopCharacteristics):
    _ABSTRACT = False
    # default: 'false'
    _DECL = {
    'testBefore': _Ref('testBefore', bool),
    'loopCondition': _Ref('loopCondition', "Expression", composite=True, assoc="A_loopCondition_standardLoopCharacteristics"),
    'loopMaximum': _Ref('loopMaximum', "Expression", composite=True, assoc="A_loopMaximum_standardLoopCharacteristics"),
    }
    _OPPS = {
        'loopCondition': ('standardLoopCharacteristics',),
        'loopMaximum': ('standardLoopCharacteristics',),
    }

class StartEvent(CatchEvent):
    _ABSTRACT = False
    # default: 'true'
    _DECL = {
    'isInterrupting': _Ref('isInterrupting', bool),
    }

class SubChoreography(ChoreographyActivity, FlowElementsContainer):
    _ABSTRACT = False
    _DECL = {
    'artifacts': _Ref('artifacts', "Artifact", multi=True, lo=0, hi='*', composite=True, assoc="A_artifacts_subChoreography"),
    }
    _OPPS = {
        'artifacts': ('subChoreography',),
    }

class SubConversation(ConversationNode):
    _ABSTRACT = False
    _DECL = {
    'conversationNodes': _Ref('conversationNodes', "ConversationNode", multi=True, lo=0, hi='*', composite=True, assoc="A_conversationNodes_subConversation"),
    }
    _OPPS = {
        'conversationNodes': ('subConversation',),
    }

class TerminateEventDefinition(EventDefinition):
    _ABSTRACT = False

class TextAnnotation(Artifact):
    _ABSTRACT = False
    # default: 'text/plain'
    _DECL = {
    'text': _Ref('text', str),
    'textFormat': _Ref('textFormat', str),
    }

class TimerEventDefinition(EventDefinition):
    _ABSTRACT = False
    _DECL = {
    'timeDate': _Ref('timeDate', "Expression", composite=True, assoc="A_timeDate_timerEventDefinition"),
    'timeCycle': _Ref('timeCycle', "Expression", composite=True, assoc="A_timeCycle_timerEventDefinition"),
    'timeDuration': _Ref('timeDuration', "Expression", composite=True, assoc="A_timeDuration_timerEventDefinition"),
    }
    _OPPS = {
        'timeDate': ('timerEventDefinition',),
        'timeCycle': ('timerEventDefinition',),
        'timeDuration': ('timerEventDefinition',),
    }

class Transaction(SubProcess):
    _ABSTRACT = False
    _DECL = {
    'protocol': _Ref('protocol', str),
    'method': _Ref('method', str),
    }

class UserTask(Task):
    _ABSTRACT = False
    _DECL = {
    'renderings': _Ref('renderings', "Rendering", multi=True, lo=0, hi='*', composite=True, assoc="A_renderings_usertask"),
    'implementation': _Ref('implementation', str),
    }
    _OPPS = {
        'renderings': ('usertask',),
    }

_SYNTH = {
    "package": {"name": 'BPMN20', "uri": 'http://www.omg.org/spec/BPMN/20100524/MODEL-XMI'},
    "tags": (
        ('org.omg.xmi.nsPrefix', 'bpmn', '_0'),
        ('org.omg.xmi.nsURI', 'http://www.omg.org/spec/BPMN/20100524/MODEL-XMI', '_0'),
    ),
    "hrefs": {
        "BPMNDI.BPMNDiagram": "BPMNDI.cmof#BPMNDiagram",
        "Boolean": "http://schema.omg.org/spec/MOF/2.0/cmof.xml#Boolean",
        "Element": "http://schema.omg.org/spec/MOF/2.0/cmof.xml#Element",
        "Integer": "http://schema.omg.org/spec/MOF/2.0/cmof.xml#Integer",
        "String": "http://schema.omg.org/spec/MOF/2.0/cmof.xml#String",
    },
    "ends": {
        "A_activationCondition_complexGateway": ('complexGateway', 'ComplexGateway', '0', None, None, False),
        "A_activityRef_compensateEventDefinition": ('compensateEventDefinition', 'CompensateEventDefinition', '0', '*', None, False),
        "A_artifacts_collaboration": ('collaboration', 'Collaboration', '0', None, None, False),
        "A_artifacts_process": ('process', 'Process', '0', None, 'public', False),
        "A_artifacts_subChoreography": ('subChoreography', 'SubChoreography', '0', None, 'public', False),
        "A_artifacts_subProcess": ('subProcess', 'SubProcess', '0', None, 'public', False),
        "A_assignment_dataAssociation": ('dataAssociation', 'DataAssociation', None, None, None, False),
        "A_auditing_flowElement": ('flowElement', 'FlowElement', '0', None, None, False),
        "A_auditing_process": ('process', 'Process', '0', None, None, False),
        "A_calledChoreographyRef_callChoreographyActivity": ('callChoreographyActivity', 'CallChoreography', '0', '*', None, False),
        "A_calledCollaborationRef_callConversation": ('callConversation', 'CallConversation', '0', '*', None, False),
        "A_calledElementRef_callActivity": ('callActivity', 'CallActivity', '0', '*', None, False),
        "A_categoryValueRef_categoryValueRef": ('categoryValueRef', 'Group', '0', '*', None, False),
        "A_categoryValue_category": ('category', 'Category', None, None, None, False),
        "A_childLaneSet_parentLane": ('parentLane', 'Lane', '0', None, None, False),
        "A_choreographyRef_collaboration": ('collaboration', 'Collaboration', '0', '*', None, False),
        "A_completionCondition_adHocSubProcess": ('adHocSubProcess', 'AdHocSubProcess', '0', None, None, False),
        "A_completionCondition_multiInstanceLoopCharacteristics": ('multiInstanceLoopCharacteristics', 'MultiInstanceLoopCharacteristics', '0', None, None, False),
        "A_complexBehaviorDefinition_multiInstanceLoopCharacteristics": ('multiInstanceLoopCharacteristics', 'MultiInstanceLoopCharacteristics', None, None, None, False),
        "A_conditionExpression_sequenceFlow": ('sequenceFlow', 'SequenceFlow', '0', None, None, False),
        "A_condition_complexBehaviorDefinition": ('complexBehaviorDefinition', 'ComplexBehaviorDefinition', '0', None, None, False),
        "A_condition_conditionalEventDefinition": ('conditionalEventDefinition', 'ConditionalEventDefinition', '0', None, None, False),
        "A_conversationAssociations_converstaionAssociations": ('converstaionAssociations', 'Collaboration', None, None, None, False),
        "A_conversationLinks_collaboration": ('collaboration', 'Collaboration', None, None, 'public', False),
        "A_conversationNodes_subConversation": ('subConversation', 'SubConversation', '0', None, 'public', False),
        "A_conversations_collaboration": ('collaboration', 'Collaboration', '0', None, 'public', False),
        "A_correlationKeyRef_correlationSubscription": ('correlationSubscription', 'CorrelationSubscription', '0', '*', None, False),
        "A_correlationKeys_choreographyActivity": ('choreographyActivity', 'ChoreographyActivity', '0', None, 'public', False),
        "A_correlationKeys_collaboration": ('collaboration', 'Collaboration', '0', None, 'public', False),
        "A_correlationKeys_conversationNode": ('conversationNode', 'ConversationNode', '0', None, 'public', False),
        "A_correlationPropertyBinding_correlationSubscription": ('correlationSubscription', 'CorrelationSubscription', '0', None, None, False),
        "A_correlationPropertyRef_correlationKey": ('correlationKey', 'CorrelationKey', '0', '*', None, False),
        "A_correlationPropertyRef_correlationPropertyBinding": ('correlationPropertyBinding', 'CorrelationPropertyBinding', '0', '*', None, False),
        "A_correlationPropertyRetrievalExpression_correlationproperty": ('correlationproperty', 'CorrelationProperty', None, None, None, False),
        "A_correlationSubscriptions_process": ('process', 'Process', None, None, 'public', False),
        "A_dataInputAssociation_throwEvent": ('throwEvent', 'ThrowEvent', '0', None, None, False),
        "A_dataInputAssociations_activity": ('activity', 'Activity', '0', None, None, False),
        "A_dataInputs_inputOutputSpecification": ('inputOutputSpecification', 'InputOutputSpecification', None, None, None, False),
        "A_dataInputs_throwEvent": ('throwEvent', 'ThrowEvent', '0', None, None, False),
        "A_dataObjectRef_dataObject": ('dataObject', 'DataObjectReference', '0', '*', 'public', False),
        "A_dataOutputAssociation_catchEvent": ('catchEvent', 'CatchEvent', '0', None, None, False),
        "A_dataOutputAssociations_activity": ('activity', 'Activity', '0', None, None, False),
        "A_dataOutputs_catchEvent": ('catchEvent', 'CatchEvent', '0', None, None, False),
        "A_dataOutputs_inputOutputSpecification": ('inputOutputSpecification', 'InputOutputSpecification', None, None, None, False),
        "A_dataPath_correlationPropertyBinding": ('correlationPropertyBinding', 'CorrelationPropertyBinding', '0', None, None, False),
        "A_dataState_itemAwareElement": ('itemAwareElement', 'ItemAwareElement', None, None, None, False),
        "A_dataStoreRef_dataStoreReference": ('dataStoreReference', 'DataStoreReference', '0', '*', None, False),
        "A_default_activity": ('activity', 'Activity', None, None, None, False),
        "A_default_complexGateway": ('complexGateway', 'ComplexGateway', '0', '*', None, False),
        "A_default_exclusiveGateway": ('exclusiveGateway', 'ExclusiveGateway', '0', '*', None, False),
        "A_default_inclusiveGateway": ('inclusiveGateway', 'InclusiveGateway', '0', '*', None, False),
        "A_definition_extension": ('extension', 'Extension', None, None, None, False),
        "A_definitionalCollaborationRef_process": ('process', 'Process', '0', '*', None, False),
        "A_diagrams_definitions": ('definitions', 'Definitions', None, None, 'public', False),
        "A_documentation_baseElement": ('baseElement', 'BaseElement', None, None, None, False),
        "A_endPointRefs_participant": ('participant', 'Participant', '0', '*', None, False),
        "A_errorRef_errorEventDefinition": ('errorEventDefinition', 'ErrorEventDefinition', '0', '*', None, False),
        "A_errorRefs_operation": ('operation', 'Operation', '0', '*', None, False),
        "A_escalationRef_escalationEventDefinition": ('escalationEventDefinition', 'EscalationEventDefinition', '0', '*', None, False),
        "A_evaluatesToTypeRef_formalExpression": ('formalExpression', 'FormalExpression', '0', '*', None, False),
        "A_eventDefinitionRefs_catchEvent": ('catchEvent', 'CatchEvent', '0', '*', None, False),
        "A_eventDefinitionRefs_throwEvent": ('throwEvent', 'ThrowEvent', '0', '*', None, False),
        "A_eventDefinitions_catchEvent": ('catchEvent', 'CatchEvent', '0', None, None, False),
        "A_eventDefinitions_throwEvent": ('throwEvent', 'ThrowEvent', '0', None, None, False),
        "A_event_complexBehaviorDefinition": ('complexBehaviorDefinition', 'ComplexBehaviorDefinition', None, None, None, False),
        "A_expression_resourceAssignmentExpression": ('resourceAssignmentExpression', 'ResourceAssignmentExpression', '0', None, None, False),
        "A_expression_resourceParameterBinding": ('resourceParameterBinding', 'ResourceParameterBinding', '0', None, None, False),
        "A_extensionAttributeDefinition_extensionAttributeValue": ('extensionAttributeValue', 'ExtensionAttributeValue', '0', '*', None, False),
        "A_extensionDefinitions_baseElement": ('baseElement', 'BaseElement', '0', '*', None, False),
        "A_extensionValues_baseElement": ('baseElement', 'BaseElement', None, None, None, False),
        "A_extensions_definitions": ('definitions', 'Definitions', None, None, None, False),
        "A_flowElements_container": ('container', 'FlowElementsContainer', None, None, None, False),
        "A_from_assignment": ('assignment', 'Assignment', '0', None, 'public', False),
        "A_import_itemDefinition": ('itemDefinition', 'ItemDefinition', '0', '*', None, False),
        "A_imports_definition": ('definition', 'Definitions', None, None, None, False),
        "A_inMessageRef_operation": ('operation', 'Operation', '0', '*', None, False),
        "A_initiatingParticipantRef_choreographyActivity": ('choreographyActivity', 'ChoreographyActivity', '0', '*', None, False),
        "A_initiatingParticipantRef_globalChoreographyTask": ('globalChoreographyTask', 'GlobalChoreographyTask', '0', '*', None, False),
        "A_innerConversationNodeRef_conversationAssociation": ('conversationAssociation', 'ConversationAssociation', '0', '*', 'public', False),
        "A_innerMessageFlowRef_messageFlowAssociation": ('messageFlowAssociation', 'MessageFlowAssociation', '0', '*', None, False),
        "A_innerParticipantRef_participantAssociation": ('participantAssociation', 'ParticipantAssociation', '0', '*', None, False),
        "A_inputDataItem_multiInstanceLoopCharacteristics": ('multiInstanceLoopCharacteristics', 'MultiInstanceLoopCharacteristics', '0', None, None, False),
        "A_inputDataRef_inputOutputBinding": ('inputOutputBinding', 'InputOutputBinding', '0', '*', None, False),
        "A_inputSet_throwEvent": ('throwEvent', 'ThrowEvent', '0', None, None, False),
        "A_inputSets_inputOutputSpecification": ('inputOutputSpecification', 'InputOutputSpecification', None, None, None, False),
        "A_interfaceRefs_participant": ('participant', 'Participant', '0', '*', None, False),
        "A_ioBinding_callableElement": ('callableElement', 'CallableElement', '0', None, None, False),
        "A_ioSpecification_activity": ('activity', 'Activity', '0', None, None, False),
        "A_ioSpecification_callableElement": ('callableElement', 'CallableElement', '0', None, None, False),
        "A_itemRef_message": ('message', 'Message', '0', '*', 'public', False),
        "A_itemSubjectRef_itemAwareElement": ('itemAwareElement', 'ItemAwareElement', '0', '*', None, False),
        "A_laneSets_flowElementsContainer": ('flowElementsContainer', 'FlowElementsContainer', '0', None, 'public', False),
        "A_lanes_laneSet": ('laneSet', 'LaneSet', None, None, None, False),
        "A_loopCardinality_multiInstanceLoopCharacteristics": ('multiInstanceLoopCharacteristics', 'MultiInstanceLoopCharacteristics', '0', None, None, False),
        "A_loopCharacteristics_activity": ('activity', 'Activity', '0', None, None, False),
        "A_loopCondition_standardLoopCharacteristics": ('standardLoopCharacteristics', 'StandardLoopCharacteristics', '0', None, None, False),
        "A_loopDataInputRef_multiInstanceLoopCharacteristics": ('multiInstanceLoopCharacteristics', 'MultiInstanceLoopCharacteristics', '0', None, None, False),
        "A_loopDataOutputRef_multiInstanceLoopCharacteristics": ('multiInstanceLoopCharacteristics', 'MultiInstanceLoopCharacteristics', '0', None, None, False),
        "A_loopMaximum_standardLoopCharacteristics": ('standardLoopCharacteristics', 'StandardLoopCharacteristics', '0', None, None, False),
        "A_messageFlowAssociations_collaboration": ('collaboration', 'Collaboration', None, None, None, False),
        "A_messageFlowRef_choreographyTask": ('choreographyTask', 'ChoreographyTask', '0', None, 'public', False),
        "A_messageFlowRefs_communication": ('communication', 'ConversationNode', '0', '*', None, False),
        "A_messageFlows_collaboration": ('collaboration', 'Collaboration', None, None, 'public', False),
        "A_messagePath_correlationset": ('correlationset', 'CorrelationPropertyRetrievalExpression', '0', None, None, False),
        "A_messageRef_correlationPropertyRetrievalExpression": ('correlationPropertyRetrievalExpression', 'CorrelationPropertyRetrievalExpression', '0', '*', None, False),
        "A_messageRef_messageEventDefinition": ('messageEventDefinition', 'MessageEventDefinition', '0', '*', None, False),
        "A_messageRef_messageFlow": ('messageFlow', 'MessageFlow', '0', '*', None, False),
        "A_messageRef_receiveTask": ('receiveTask', 'ReceiveTask', '0', '*', None, False),
        "A_messageRef_sendTask": ('sendTask', 'SendTask', '0', '*', None, False),
        "A_monitoring_flowElement": ('flowElement', 'FlowElement', '0', None, None, False),
        "A_monitoring_process": ('process', 'Process', '0', None, None, False),
        "A_noneBehaviorEventRef_multiInstanceLoopCharacteristics": ('multiInstanceLoopCharacteristics', 'MultiInstanceLoopCharacteristics', '0', '*', None, False),
        "A_oneBehaviorEventRef_multiInstanceLoopCharacteristics": ('multiInstanceLoopCharacteristics', 'MultiInstanceLoopCharacteristics', '0', '*', None, False),
        "A_operationRef_ioBinding": ('ioBinding', 'InputOutputBinding', '0', '*', None, False),
        "A_operationRef_messageEventDefinition": ('messageEventDefinition', 'MessageEventDefinition', '0', '*', None, False),
        "A_operationRef_receiveTask": ('receiveTask', 'ReceiveTask', '0', '*', None, False),
        "A_operationRef_sendTask": ('sendTask', 'SendTask', '0', '*', None, False),
        "A_operationRef_serviceTask": ('serviceTask', 'ServiceTask', '0', '*', None, False),
        "A_operations_interface": ('interface', 'Interface', None, None, None, False),
        "A_outMessageRef_operation": ('operation', 'Operation', '0', '*', None, False),
        "A_outerConversationNodeRef_conversationAssociation": ('conversationAssociation', 'ConversationAssociation', '0', '*', 'public', False),
        "A_outerMessageFlowRef_messageFlowAssociation": ('messageFlowAssociation', 'MessageFlowAssociation', '0', '*', None, False),
        "A_outerParticipantRef_participantAssociation": ('participantAssociation', 'ParticipantAssociation', '0', '*', None, False),
        "A_outputDataItem_multiInstanceLoopCharacteristics": ('multiInstanceLoopCharacteristics', 'MultiInstanceLoopCharacteristics', '0', None, None, False),
        "A_outputDataRef_inputOutputBinding": ('inputOutputBinding', 'InputOutputBinding', '0', '*', None, False),
        "A_outputSet_catchEvent": ('catchEvent', 'CatchEvent', '0', None, None, False),
        "A_outputSets_inputOutputSpecification": ('inputOutputSpecification', 'InputOutputSpecification', None, None, None, False),
        "A_parameterRef_resourceParameterBinding": ('resourceParameterBinding', 'ResourceParameterBinding', '0', '*', None, False),
        "A_participantAssociations_callChoreographyActivity": ('callChoreographyActivity', 'CallChoreography', '0', None, None, False),
        "A_participantAssociations_callConversation": ('callConversation', 'CallConversation', '0', None, None, False),
        "A_participantAssociations_collaboration": ('collaboration', 'Collaboration', '0', None, None, False),
        "A_participantMultiplicity_participant": ('participant', 'Participant', None, None, None, False),
        "A_participantRefs_choreographyActivity": ('choreographyActivity', 'ChoreographyActivity', '0', '*', None, False),
        "A_participantRefs_conversationNode": ('conversationNode', 'ConversationNode', '0', '*', None, False),
        "A_participants_collaboration": ('collaboration', 'Collaboration', None, None, 'public', False),
        "A_partitionElementRef_lane": ('lane', 'Lane', '0', '*', None, False),
        "A_partitionElement_lane": ('lane', 'Lane', '0', None, None, False),
        "A_partnerEntityRef_participantRef": ('partnerEntityRef', 'PartnerEntity', '0', '*', None, True),
        "A_partnerRoleRef_participantRef": ('partnerRoleRef', 'PartnerRole', '0', '*', None, True),
        "A_processRef_participant": ('participant', 'Participant', '0', '*', None, False),
        "A_properties_activity": ('activity', 'Activity', '0', None, None, False),
        "A_properties_event": ('event', 'Event', '0', None, 'public', False),
        "A_properties_process": ('process', 'Process', '0', None, None, False),
        "A_relationships_definition": ('definition', 'Definitions', None, None, None, False),
        "A_renderings_globalUserTask": ('globalUserTask', 'GlobalUserTask', '0', None, None, False),
        "A_renderings_usertask": ('usertask', 'UserTask', '0', None, None, False),
        "A_resourceAssignmentExpression_activityResource": ('activityResource', 'ResourceRole', None, None, None, False),
        "A_resourceParameterBindings_activityResource": ('activityResource', 'ResourceRole', None, None, None, False),
        "A_resourceParameters_resource": ('resource', 'Resource', None, None, None, False),
        "A_resourceRef_activityResource": ('activityResource', 'ResourceRole', '0', '*', None, False),
        "A_resources_activity": ('activity', 'Activity', '0', None, None, False),
        "A_resources_globalTask": ('globalTask', 'GlobalTask', '0', None, None, False),
        "A_resources_process": ('process', 'Process', '0', None, 'public', False),
        "A_rootElements_definition": ('definition', 'Definitions', '0', None, None, False),
        "A_signalRef_signalEventDefinition": ('signalEventDefinition', 'SignalEventDefinition', '0', '*', None, False),
        "A_sourceRef_dataAssociation": ('dataAssociation', 'DataAssociation', '0', '*', None, False),
        "A_sourceRef_messageFlow": ('messageFlow', 'MessageFlow', '0', '*', None, False),
        "A_sourceRef_outgoing_association": ('outgoing', 'Association', '0', '*', None, False),
        "A_sources_relationship": ('relationship', 'Relationship', '0', '*', None, False),
        "A_structureRef_error": ('error', 'Error', '0', '*', None, False),
        "A_structureRef_escalation": ('escalation', 'Escalation', '0', '*', None, False),
        "A_structureRef_signal": ('signal', 'Signal', '0', '*', None, False),
        "A_supportedInterfaceRefs_callableElements": ('callableElements', 'CallableElement', '0', '*', None, False),
        "A_supports_process": ('process', 'Process', '0', '*', None, False),
        "A_targetRef_dataAssociation": ('dataAssociation', 'DataAssociation', '0', '*', None, False),
        "A_targetRef_incoming_association": ('incoming', 'Association', '0', '*', None, False),
        "A_targetRef_messageFlow": ('messageFlow', 'MessageFlow', '0', '*', None, False),
        "A_targets_relationship": ('relationship', 'Relationship', '0', '*', None, False),
        "A_timeCycle_timerEventDefinition": ('timerEventDefinition', 'TimerEventDefinition', '0', None, None, False),
        "A_timeDate_timerEventDefinition": ('timerEventDefinition', 'TimerEventDefinition', '0', None, None, False),
        "A_timeDuration_timerEventDefinition": ('timerEventDefinition', 'TimerEventDefinition', '0', None, 'public', False),
        "A_to_assignment": ('assignment', 'Assignment', '0', None, 'public', False),
        "A_transformation_dataAssociation": ('dataAssociation', 'DataAssociation', '0', None, None, False),
        "A_type_correlationProperty": ('correlationProperty', 'CorrelationProperty', '0', '*', 'public', False),
        "A_type_resourceParameter": ('resourceParameter', 'ResourceParameter', '0', '*', 'public', False),
        "A_valueRef_extensionAttributeValue": ('extensionAttributeValue', 'ExtensionAttributeValue', '0', '*', None, False),
        "A_value_extensionAttributeValue": ('extensionAttributeValue', 'ExtensionAttributeValue', None, None, None, False),
    },
    "props": {
        "Activity.boundaryEventRefs": ('0', '*', None, None, None),
        "Activity.completionQuantity": (None, None, None, None, '1'),
        "Activity.dataInputAssociations": ('0', '*', None, None, None),
        "Activity.dataOutputAssociations": ('0', '*', None, None, None),
        "Activity.default": ('0', None, None, None, None),
        "Activity.ioSpecification": ('0', None, None, None, None),
        "Activity.isForCompensation": (None, None, None, None, 'false'),
        "Activity.loopCharacteristics": ('0', None, None, None, None),
        "Activity.properties": ('0', '*', None, None, None),
        "Activity.resources": ('0', '*', None, None, None),
        "Activity.startQuantity": (None, None, None, None, '1'),
        "AdHocSubProcess.cancelRemainingInstances": (None, None, None, None, 'true'),
        "AdHocSubProcess.completionCondition": (None, None, None, None, None),
        "AdHocSubProcess.ordering": (None, None, None, None, None),
        "Assignment.from": (None, None, 'public', None, None),
        "Assignment.to": (None, None, 'public', None, None),
        "Association.associationDirection": (None, None, None, None, None),
        "Association.sourceRef": (None, None, None, None, None),
        "Association.targetRef": (None, None, None, None, None),
        "BaseElement.documentation": ('0', '*', None, None, None),
        "BaseElement.extensionDefinitions": ('0', '*', None, None, None),
        "BaseElement.extensionValues": ('0', '*', None, None, None),
        "BaseElement.id": (None, None, None, None, None),
        "BoundaryEvent.attachedToRef": (None, None, None, None, None),
        "BoundaryEvent.cancelActivity": (None, None, None, None, 'true'),
        "BusinessRuleTask.implementation": (None, None, 'public', None, None),
        "CallActivity.calledElementRef": ('0', None, None, None, None),
        "CallChoreography.calledChoreographyRef": ('0', None, None, None, None),
        "CallChoreography.participantAssociations": ('0', '*', None, None, None),
        "CallConversation.calledCollaborationRef": ('0', None, None, None, None),
        "CallConversation.participantAssociations": ('0', '*', None, None, None),
        "CallableElement.ioBinding": ('0', '*', None, None, None),
        "CallableElement.ioSpecification": ('0', None, None, None, None),
        "CallableElement.name": (None, None, None, None, None),
        "CallableElement.supportedInterfaceRefs": ('0', '*', None, None, None),
        "CatchEvent.dataOutputAssociation": ('0', '*', None, None, None),
        "CatchEvent.dataOutputs": ('0', '*', None, None, None),
        "CatchEvent.eventDefinitionRefs": ('0', '*', None, None, None),
        "CatchEvent.eventDefinitions": ('0', '*', None, None, None),
        "CatchEvent.outputSet": ('0', None, None, None, None),
        "CatchEvent.parallelMultiple": (None, None, None, None, None),
        "Category.categoryValue": ('0', '*', None, None, None),
        "Category.name": (None, None, 'public', None, None),
        "CategoryValue.categorizedFlowElements": ('0', '*', None, None, None),
        "CategoryValue.value": (None, None, None, None, None),
        "ChoreographyActivity.correlationKeys": ('0', '*', 'public', None, None),
        "ChoreographyActivity.initiatingParticipantRef": (None, None, None, None, None),
        "ChoreographyActivity.loopType": (None, None, 'public', None, 'None'),
        "ChoreographyActivity.participantRefs": ('2', '*', None, None, None),
        "ChoreographyTask.messageFlowRef": (None, '2', None, None, None),
        "Collaboration.artifacts": ('0', '*', None, None, None),
        "Collaboration.choreographyRef": ('0', '*', None, None, None),
        "Collaboration.conversationAssociations": (None, None, None, None, None),
        "Collaboration.conversationLinks": ('0', '*', 'public', None, None),
        "Collaboration.conversations": ('0', '*', 'public', None, None),
        "Collaboration.correlationKeys": ('0', '*', None, None, None),
        "Collaboration.isClosed": (None, None, None, None, None),
        "Collaboration.messageFlowAssociations": ('0', '*', None, None, None),
        "Collaboration.messageFlows": ('0', '*', 'public', None, None),
        "Collaboration.name": (None, None, None, None, None),
        "Collaboration.participantAssociations": ('0', '*', None, None, None),
        "Collaboration.participants": ('0', '*', 'public', None, None),
        "CompensateEventDefinition.activityRef": ('0', None, None, None, None),
        "CompensateEventDefinition.waitForCompletion": (None, None, None, None, None),
        "ComplexBehaviorDefinition.condition": (None, None, None, None, None),
        "ComplexBehaviorDefinition.event": ('0', None, None, None, None),
        "ComplexGateway.activationCondition": ('0', None, None, None, None),
        "ComplexGateway.default": ('0', None, None, None, None),
        "ConditionalEventDefinition.condition": (None, None, None, None, None),
        "ConversationAssociation.innerConversationNodeRef": (None, None, 'public', None, None),
        "ConversationAssociation.outerConversationNodeRef": (None, None, 'public', None, None),
        "ConversationLink.name": ('0', None, 'public', None, None),
        "ConversationLink.sourceRef": (None, None, 'public', None, None),
        "ConversationLink.targetRef": (None, None, 'public', None, None),
        "ConversationNode.correlationKeys": ('0', '*', None, None, None),
        "ConversationNode.messageFlowRefs": ('0', '*', None, None, None),
        "ConversationNode.name": (None, None, None, None, None),
        "ConversationNode.participantRefs": ('2', '*', None, None, None),
        "CorrelationKey.correlationPropertyRef": ('0', '*', None, None, None),
        "CorrelationKey.name": (None, None, 'public', None, None),
        "CorrelationProperty.correlationPropertyRetrievalExpression": (None, '*', None, None, None),
        "CorrelationProperty.name": (None, None, 'public', None, None),
        "CorrelationProperty.type": ('0', None, 'public', None, None),
        "CorrelationPropertyBinding.correlationPropertyRef": (None, None, None, None, None),
        "CorrelationPropertyBinding.dataPath": (None, None, None, None, None),
        "CorrelationPropertyRetrievalExpression.messagePath": (None, None, None, None, None),
        "CorrelationPropertyRetrievalExpression.messageRef": (None, None, None, None, None),
        "CorrelationSubscription.correlationKeyRef": (None, None, None, None, None),
        "CorrelationSubscription.correlationPropertyBinding": ('0', '*', None, None, None),
        "DataAssociation.assignment": ('0', '*', None, None, None),
        "DataAssociation.sourceRef": ('0', '*', None, None, None),
        "DataAssociation.targetRef": (None, None, None, None, None),
        "DataAssociation.transformation": ('0', None, None, None, None),
        "DataInput.inputSetRefs": (None, '*', None, None, None),
        "DataInput.inputSetWithOptional": ('0', '*', None, None, None),
        "DataInput.inputSetWithWhileExecuting": ('0', '*', None, None, None),
        "DataInput.isCollection": (None, None, None, None, 'false'),
        "DataInput.name": ('0', None, None, None, None),
        "DataObject.isCollection": (None, None, None, None, 'false'),
        "DataObjectReference.dataObjectRef": (None, None, 'public', None, None),
        "DataOutput.isCollection": (None, None, None, None, 'false'),
        "DataOutput.name": ('0', None, None, None, None),
        "DataOutput.outputSetRefs": (None, '*', None, None, None),
        "DataOutput.outputSetWithOptional": ('0', '*', None, None, None),
        "DataOutput.outputSetWithWhileExecuting": ('0', '*', None, None, None),
        "DataState.name": (None, None, None, None, None),
        "DataStore.capacity": (None, None, None, None, None),
        "DataStore.isUnlimited": (None, None, None, None, 'true'),
        "DataStore.name": (None, None, None, None, None),
        "DataStoreReference.dataStoreRef": ('0', None, None, None, None),
        "Definitions.diagrams": ('0', '*', 'public', None, None),
        "Definitions.exporter": (None, None, 'public', None, None),
        "Definitions.exporterVersion": (None, None, 'public', None, None),
        "Definitions.expressionLanguage": (None, None, 'public', None, 'http://www.w3.org/1999/XPath'),
        "Definitions.extensions": ('0', '*', 'public', None, None),
        "Definitions.imports": ('0', '*', 'public', None, None),
        "Definitions.name": (None, None, 'public', None, None),
        "Definitions.relationships": ('0', '*', 'public', None, None),
        "Definitions.rootElements": ('0', '*', 'public', None, None),
        "Definitions.targetNamespace": (None, None, 'public', None, None),
        "Definitions.typeLanguage": (None, None, 'public', None, 'http://www.w3.org/2001/XMLSchema'),
        "Documentation.text": (None, None, None, None, None),
        "Documentation.textFormat": (None, None, 'public', None, 'text/plain'),
        "Error.errorCode": (None, None, 'public', None, None),
        "Error.name": (None, None, 'public', None, None),
        "Error.structureRef": ('0', None, None, None, None),
        "ErrorEventDefinition.errorRef": ('0', None, None, None, None),
        "Escalation.escalationCode": (None, None, 'public', None, None),
        "Escalation.name": (None, None, 'public', None, None),
        "Escalation.structureRef": ('0', None, None, None, None),
        "EscalationEventDefinition.escalationRef": ('0', None, None, None, None),
        "Event.properties": ('0', '*', 'public', None, None),
        "EventBasedGateway.eventGatewayType": (None, None, None, None, None),
        "EventBasedGateway.instantiate": (None, None, None, None, 'false'),
        "ExclusiveGateway.default": ('0', None, None, None, None),
        "Extension.definition": (None, None, None, None, None),
        "Extension.mustUnderstand": (None, None, None, None, 'false'),
        "ExtensionAttributeDefinition.extensionDefinition": (None, None, None, None, None),
        "ExtensionAttributeDefinition.isReference": (None, None, None, None, 'false'),
        "ExtensionAttributeDefinition.name": (None, None, None, None, None),
        "ExtensionAttributeDefinition.type": (None, None, None, None, None),
        "ExtensionAttributeValue.extensionAttributeDefinition": (None, None, None, None, None),
        "ExtensionAttributeValue.value": ('0', None, None, None, None),
        "ExtensionAttributeValue.valueRef": ('0', None, None, None, None),
        "ExtensionDefinition.extensionAttributeDefinitions": ('0', '*', None, None, None),
        "ExtensionDefinition.name": (None, None, None, None, None),
        "FlowElement.auditing": ('0', None, None, None, None),
        "FlowElement.categoryValueRef": ('0', '*', None, None, None),
        "FlowElement.monitoring": ('0', None, None, None, None),
        "FlowElement.name": (None, None, None, None, None),
        "FlowElementsContainer.flowElements": ('0', '*', None, None, None),
        "FlowElementsContainer.laneSets": ('0', '*', 'public', None, None),
        "FlowNode.incoming": ('0', '*', None, None, None),
        "FlowNode.lanes": ('0', '*', None, None, None),
        "FlowNode.outgoing": ('0', '*', None, 'true', None),
        "FormalExpression.body": (None, None, None, None, None),
        "FormalExpression.evaluatesToTypeRef": (None, None, None, None, None),
        "FormalExpression.language": (None, None, None, None, None),
        "Gateway.gatewayDirection": (None, None, None, None, 'unspecified'),
        "GlobalBusinessRuleTask.implementation": (None, None, 'public', None, None),
        "GlobalChoreographyTask.initiatingParticipantRef": (None, None, None, None, None),
        "GlobalScriptTask.script": (None, None, None, None, None),
        "GlobalScriptTask.scriptLanguage": (None, None, None, None, None),
        "GlobalTask.resources": ('0', '*', None, None, None),
        "GlobalUserTask.implementation": (None, None, None, None, None),
        "GlobalUserTask.renderings": ('0', '*', None, None, None),
        "Group.categoryValueRef": ('0', None, None, None, None),
        "Import.importType": (None, None, 'public', None, None),
        "Import.location": (None, None, 'public', None, None),
        "Import.namespace": (None, None, 'public', None, None),
        "InclusiveGateway.default": ('0', None, None, None, None),
        "InputOutputBinding.inputDataRef": (None, None, None, None, None),
        "InputOutputBinding.operationRef": (None, None, None, None, None),
        "InputOutputBinding.outputDataRef": (None, None, None, None, None),
        "InputOutputSpecification.dataInputs": ('0', '*', None, None, None),
        "InputOutputSpecification.dataOutputs": ('0', '*', None, None, None),
        "InputOutputSpecification.inputSets": (None, '*', None, None, None),
        "InputOutputSpecification.outputSets": (None, '*', None, None, None),
        "InputSet.dataInputRefs": ('0', '*', None, None, None),
        "InputSet.name": (None, None, None, None, None),
        "InputSet.optionalInputRefs": ('0', '*', None, None, None),
        "InputSet.outputSetRefs": ('0', '*', None, None, None),
        "InputSet.whileExecutingInputRefs": ('0', '*', None, None, None),
        "InteractionNode.incomingConversationLinks": ('0', '*', 'public', None, None),
        "InteractionNode.outgoingConversationLinks": ('0', '*', 'public', None, None),
        "Interface.implementationRef": ('0', None, 'public', None, None),
        "Interface.name": (None, None, None, None, None),
        "Interface.operations": (None, '*', None, None, None),
        "ItemAwareElement.dataState": ('0', None, None, None, None),
        "ItemAwareElement.itemSubjectRef": ('0', None, None, None, None),
        "ItemDefinition.import": ('0', None, None, None, None),
        "ItemDefinition.isCollection": (None, None, None, None, 'false'),
        "ItemDefinition.itemKind": (None, None, None, None, None),
        "ItemDefinition.structureRef": (None, None, None, None, None),
        "Lane.childLaneSet": ('0', None, None, None, None),
        "Lane.flowNodeRefs": ('0', '*', None, None, None),
        "Lane.name": (None, None, None, None, None),
        "Lane.partitionElement": ('0', None, None, None, None),
        "Lane.partitionElementRef": ('0', None, None, None, None),
        "LaneSet.lanes": ('0', '*', None, None, None),
        "LaneSet.name": ('0', None, 'public', None, None),
        "LinkEventDefinition.name": (None, None, None, None, None),
        "LinkEventDefinition.source": ('0', '*', 'public', None, None),
        "LinkEventDefinition.target": ('0', None, 'public', None, None),
        "Message.itemRef": ('0', None, 'public', None, None),
        "Message.name": (None, None, None, None, None),
        "MessageEventDefinition.messageRef": ('0', None, None, None, None),
        "MessageEventDefinition.operationRef": ('0', None, None, None, None),
        "MessageFlow.messageRef": ('0', None, None, None, None),
        "MessageFlow.name": (None, None, None, None, None),
        "MessageFlow.sourceRef": (None, None, None, None, None),
        "MessageFlow.targetRef": (None, None, None, None, None),
        "MessageFlowAssociation.innerMessageFlowRef": (None, None, None, None, None),
        "MessageFlowAssociation.outerMessageFlowRef": (None, None, None, None, None),
        "MultiInstanceLoopCharacteristics.behavior": (None, None, None, None, 'All'),
        "MultiInstanceLoopCharacteristics.completionCondition": ('0', None, None, None, None),
        "MultiInstanceLoopCharacteristics.complexBehaviorDefinition": ('0', '*', None, None, None),
        "MultiInstanceLoopCharacteristics.inputDataItem": ('0', None, None, None, None),
        "MultiInstanceLoopCharacteristics.isSequential": (None, None, None, None, 'false'),
        "MultiInstanceLoopCharacteristics.loopCardinality": ('0', None, None, None, None),
        "MultiInstanceLoopCharacteristics.loopDataInputRef": ('0', None, None, None, None),
        "MultiInstanceLoopCharacteristics.loopDataOutputRef": ('0', None, None, None, None),
        "MultiInstanceLoopCharacteristics.noneBehaviorEventRef": ('0', None, None, None, None),
        "MultiInstanceLoopCharacteristics.oneBehaviorEventRef": ('0', None, None, None, None),
        "MultiInstanceLoopCharacteristics.outputDataItem": ('0', None, None, None, None),
        "Operation.errorRefs": ('0', '*', None, None, None),
        "Operation.implementationRef": ('0', None, 'public', None, None),
        "Operation.inMessageRef": (None, None, None, None, None),
        "Operation.name": (None, None, None, None, None),
        "Operation.outMessageRef": ('0', None, None, None, None),
        "OutputSet.dataOutputRefs": ('0', '*', None, None, None),
        "OutputSet.inputSetRefs": ('0', '*', None, None, None),
        "OutputSet.name": (None, None, None, None, None),
        "OutputSet.optionalOutputRefs": ('0', '*', None, None, None),
        "OutputSet.whileExecutingOutputRefs": ('0', '*', None, None, None),
        "Participant.endPointRefs": ('0', '*', None, None, None),
        "Participant.interfaceRefs": ('0', '*', None, None, None),
        "Participant.name": (None, None, None, None, None),
        "Participant.participantMultiplicity": ('0', None, None, None, None),
        "Participant.processRef": ('0', None, None, None, None),
        "ParticipantAssociation.innerParticipantRef": (None, None, None, None, None),
        "ParticipantAssociation.outerParticipantRef": (None, None, None, None, None),
        "ParticipantMultiplicity.maximum": ('0', None, None, None, '1'),
        "ParticipantMultiplicity.minimum": (None, None, None, None, '0'),
        "PartnerEntity.name": (None, None, None, None, None),
        "PartnerEntity.participantRef": ('0', '*', None, None, None),
        "PartnerRole.name": (None, None, None, None, None),
        "PartnerRole.participantRef": ('0', '*', None, None, None),
        "Process.artifacts": ('0', '*', 'public', None, None),
        "Process.auditing": ('0', None, None, None, None),
        "Process.correlationSubscriptions": ('0', '*', 'public', None, None),
        "Process.definitionalCollaborationRef": ('0', None, None, None, None),
        "Process.isClosed": (None, None, None, None, None),
        "Process.isExecutable": (None, None, 'public', None, None),
        "Process.monitoring": ('0', None, None, None, None),
        "Process.processType": (None, None, None, None, None),
        "Process.properties": ('0', '*', None, None, None),
        "Process.resources": ('0', '*', 'public', None, None),
        "Process.supports": ('0', '*', None, None, None),
        "Property.name": (None, None, None, None, None),
        "ReceiveTask.implementation": (None, None, None, None, None),
        "ReceiveTask.instantiate": (None, None, None, None, 'false'),
        "ReceiveTask.messageRef": ('0', None, None, None, None),
        "ReceiveTask.operationRef": ('0', None, None, None, None),
        "Relationship.direction": (None, None, None, None, None),
        "Relationship.sources": (None, '*', None, None, None),
        "Relationship.targets": (None, '*', None, None, None),
        "Relationship.type": (None, None, None, None, None),
        "Resource.name": (None, None, None, None, None),
        "Resource.resourceParameters": ('0', '*', None, None, None),
        "ResourceAssignmentExpression.expression": (None, None, None, None, None),
        "ResourceParameter.isRequired": (None, None, None, None, None),
        "ResourceParameter.name": (None, None, None, None, None),
        "ResourceParameter.type": ('0', None, 'public', None, None),
        "ResourceParameterBinding.expression": (None, None, None, None, None),
        "ResourceParameterBinding.parameterRef": (None, None, None, None, None),
        "ResourceRole.name": (None, None, 'public', None, None),
        "ResourceRole.resourceAssignmentExpression": ('0', None, None, None, None),
        "ResourceRole.resourceParameterBindings": ('0', '*', None, None, None),
        "ResourceRole.resourceRef": ('0', None, None, None, None),
        "ScriptTask.script": (None, None, None, None, None),
        "ScriptTask.scriptFormat": (None, None, 'public', None, None),
        "SendTask.implementation": (None, None, None, None, None),
        "SendTask.messageRef": ('0', None, None, None, None),
        "SendTask.operationRef": ('0', None, None, None, None),
        "SequenceFlow.conditionExpression": ('0', None, None, None, None),
        "SequenceFlow.isImmediate": ('0', None, None, None, None),
        "SequenceFlow.sourceRef": (None, None, None, None, None),
        "SequenceFlow.targetRef": (None, None, None, None, None),
        "ServiceTask.implementation": (None, None, None, None, None),
        "ServiceTask.operationRef": ('0', None, None, None, None),
        "Signal.name": (None, None, None, None, None),
        "Signal.structureRef": ('0', None, None, None, None),
        "SignalEventDefinition.signalRef": ('0', None, None, None, None),
        "StandardLoopCharacteristics.loopCondition": ('0', None, None, None, None),
        "StandardLoopCharacteristics.loopMaximum": ('0', None, None, None, None),
        "StandardLoopCharacteristics.testBefore": (None, None, None, None, 'false'),
        "StartEvent.isInterrupting": (None, None, None, None, 'true'),
        "SubChoreography.artifacts": ('0', '*', 'public', None, None),
        "SubConversation.conversationNodes": ('0', '*', 'public', None, None),
        "SubProcess.artifacts": ('0', '*', 'public', None, None),
        "SubProcess.triggeredByEvent": (None, None, None, None, 'false'),
        "TextAnnotation.text": (None, None, None, None, None),
        "TextAnnotation.textFormat": (None, None, 'public', None, 'text/plain'),
        "ThrowEvent.dataInputAssociation": ('0', '*', None, None, None),
        "ThrowEvent.dataInputs": ('0', '*', None, None, None),
        "ThrowEvent.eventDefinitionRefs": ('0', '*', None, None, None),
        "ThrowEvent.eventDefinitions": ('0', '*', None, None, None),
        "ThrowEvent.inputSet": ('0', None, None, None, None),
        "TimerEventDefinition.timeCycle": ('0', None, None, None, None),
        "TimerEventDefinition.timeDate": ('0', None, None, None, None),
        "TimerEventDefinition.timeDuration": ('0', None, 'public', None, None),
        "Transaction.method": (None, None, None, None, None),
        "Transaction.protocol": ('0', None, None, None, None),
        "UserTask.implementation": (None, None, None, None, None),
        "UserTask.renderings": ('0', '*', None, None, None),
    },
    "synth_attrs": {
        "Activity.compensateEventDefinition": 'A_activityRef_compensateEventDefinition',
        "Artifact.collaboration": 'A_artifacts_collaboration',
        "Artifact.process": 'A_artifacts_process',
        "Artifact.subChoreography": 'A_artifacts_subChoreography',
        "Artifact.subProcess": 'A_artifacts_subProcess',
        "Assignment.dataAssociation": 'A_assignment_dataAssociation',
        "Auditing.flowElement": 'A_auditing_flowElement',
        "Auditing.process": 'A_auditing_process',
        "BaseElement.incoming": 'A_targetRef_incoming_association',
        "BaseElement.lane": 'A_partitionElement_lane',
        "BaseElement.outgoing": 'A_sourceRef_outgoing_association',
        "CallableElement.callActivity": 'A_calledElementRef_callActivity',
        "CategoryValue.category": 'A_categoryValue_category',
        "CategoryValue.categoryValueRef": 'A_categoryValueRef_categoryValueRef',
        "Choreography.callChoreographyActivity": 'A_calledChoreographyRef_callChoreographyActivity',
        "Choreography.collaboration": 'A_choreographyRef_collaboration',
        "Collaboration.callConversation": 'A_calledCollaborationRef_callConversation',
        "Collaboration.process": 'A_definitionalCollaborationRef_process',
        "ComplexBehaviorDefinition.multiInstanceLoopCharacteristics": 'A_complexBehaviorDefinition_multiInstanceLoopCharacteristics',
        "ConversationAssociation.converstaionAssociations": 'A_conversationAssociations_converstaionAssociations',
        "ConversationLink.collaboration": 'A_conversationLinks_collaboration',
        "ConversationNode.collaboration": 'A_conversations_collaboration',
        "ConversationNode.conversationAssociation": 'A_innerConversationNodeRef_conversationAssociation',
        "ConversationNode.subConversation": 'A_conversationNodes_subConversation',
        "CorrelationKey.choreographyActivity": 'A_correlationKeys_choreographyActivity',
        "CorrelationKey.collaboration": 'A_correlationKeys_collaboration',
        "CorrelationKey.conversationNode": 'A_correlationKeys_conversationNode',
        "CorrelationKey.correlationSubscription": 'A_correlationKeyRef_correlationSubscription',
        "CorrelationProperty.correlationKey": 'A_correlationPropertyRef_correlationKey',
        "CorrelationProperty.correlationPropertyBinding": 'A_correlationPropertyRef_correlationPropertyBinding',
        "CorrelationPropertyBinding.correlationSubscription": 'A_correlationPropertyBinding_correlationSubscription',
        "CorrelationPropertyRetrievalExpression.correlationproperty": 'A_correlationPropertyRetrievalExpression_correlationproperty',
        "CorrelationSubscription.process": 'A_correlationSubscriptions_process',
        "DataInput.inputOutputSpecification": 'A_dataInputs_inputOutputSpecification',
        "DataInput.multiInstanceLoopCharacteristics": 'A_inputDataItem_multiInstanceLoopCharacteristics',
        "DataInput.throwEvent": 'A_dataInputs_throwEvent',
        "DataInputAssociation.activity": 'A_dataInputAssociations_activity',
        "DataInputAssociation.throwEvent": 'A_dataInputAssociation_throwEvent',
        "DataObject.dataObject": 'A_dataObjectRef_dataObject',
        "DataOutput.catchEvent": 'A_dataOutputs_catchEvent',
        "DataOutput.inputOutputSpecification": 'A_dataOutputs_inputOutputSpecification',
        "DataOutput.multiInstanceLoopCharacteristics": 'A_outputDataItem_multiInstanceLoopCharacteristics',
        "DataOutputAssociation.activity": 'A_dataOutputAssociations_activity',
        "DataOutputAssociation.catchEvent": 'A_dataOutputAssociation_catchEvent',
        "DataState.itemAwareElement": 'A_dataState_itemAwareElement',
        "DataStore.dataStoreReference": 'A_dataStoreRef_dataStoreReference',
        "Documentation.baseElement": 'A_documentation_baseElement',
        "EndPoint.participant": 'A_endPointRefs_participant',
        "Error.errorEventDefinition": 'A_errorRef_errorEventDefinition',
        "Error.operation": 'A_errorRefs_operation',
        "Escalation.escalationEventDefinition": 'A_escalationRef_escalationEventDefinition',
        "EventDefinition.catchEvent": 'A_eventDefinitionRefs_catchEvent',
        "EventDefinition.multiInstanceLoopCharacteristics": 'A_noneBehaviorEventRef_multiInstanceLoopCharacteristics',
        "EventDefinition.throwEvent": 'A_eventDefinitionRefs_throwEvent',
        "Expression.adHocSubProcess": 'A_completionCondition_adHocSubProcess',
        "Expression.assignment": 'A_from_assignment',
        "Expression.complexGateway": 'A_activationCondition_complexGateway',
        "Expression.conditionalEventDefinition": 'A_condition_conditionalEventDefinition',
        "Expression.multiInstanceLoopCharacteristics": 'A_completionCondition_multiInstanceLoopCharacteristics',
        "Expression.resourceAssignmentExpression": 'A_expression_resourceAssignmentExpression',
        "Expression.resourceParameterBinding": 'A_expression_resourceParameterBinding',
        "Expression.sequenceFlow": 'A_conditionExpression_sequenceFlow',
        "Expression.standardLoopCharacteristics": 'A_loopCondition_standardLoopCharacteristics',
        "Expression.timerEventDefinition": 'A_timeDate_timerEventDefinition',
        "Extension.definitions": 'A_extensions_definitions',
        "ExtensionAttributeDefinition.extensionAttributeValue": 'A_extensionAttributeDefinition_extensionAttributeValue',
        "ExtensionAttributeValue.baseElement": 'A_extensionValues_baseElement',
        "ExtensionDefinition.baseElement": 'A_extensionDefinitions_baseElement',
        "ExtensionDefinition.extension": 'A_definition_extension',
        "FlowElement.container": 'A_flowElements_container',
        "FormalExpression.complexBehaviorDefinition": 'A_condition_complexBehaviorDefinition',
        "FormalExpression.correlationPropertyBinding": 'A_dataPath_correlationPropertyBinding',
        "FormalExpression.correlationset": 'A_messagePath_correlationset',
        "FormalExpression.dataAssociation": 'A_transformation_dataAssociation',
        "ImplicitThrowEvent.complexBehaviorDefinition": 'A_event_complexBehaviorDefinition',
        "Import.definition": 'A_imports_definition',
        "Import.itemDefinition": 'A_import_itemDefinition',
        "InputOutputBinding.callableElement": 'A_ioBinding_callableElement',
        "InputOutputSpecification.activity": 'A_ioSpecification_activity',
        "InputOutputSpecification.callableElement": 'A_ioSpecification_callableElement',
        "InputSet.inputOutputBinding": 'A_inputDataRef_inputOutputBinding',
        "InputSet.inputOutputSpecification": 'A_inputSets_inputOutputSpecification',
        "InputSet.throwEvent": 'A_inputSet_throwEvent',
        "InteractionNode.messageFlow": 'A_targetRef_messageFlow',
        "Interface.callableElements": 'A_supportedInterfaceRefs_callableElements',
        "Interface.participant": 'A_interfaceRefs_participant',
        "ItemAwareElement.dataAssociation": 'A_sourceRef_dataAssociation',
        "ItemAwareElement.multiInstanceLoopCharacteristics": 'A_loopDataInputRef_multiInstanceLoopCharacteristics',
        "ItemDefinition.correlationProperty": 'A_type_correlationProperty',
        "ItemDefinition.error": 'A_structureRef_error',
        "ItemDefinition.escalation": 'A_structureRef_escalation',
        "ItemDefinition.formalExpression": 'A_evaluatesToTypeRef_formalExpression',
        "ItemDefinition.itemAwareElement": 'A_itemSubjectRef_itemAwareElement',
        "ItemDefinition.message": 'A_itemRef_message',
        "ItemDefinition.resourceParameter": 'A_type_resourceParameter',
        "ItemDefinition.signal": 'A_structureRef_signal',
        "Lane.laneSet": 'A_lanes_laneSet',
        "LaneSet.flowElementsContainer": 'A_laneSets_flowElementsContainer',
        "LaneSet.parentLane": 'A_childLaneSet_parentLane',
        "LoopCharacteristics.activity": 'A_loopCharacteristics_activity',
        "Message.correlationPropertyRetrievalExpression": 'A_messageRef_correlationPropertyRetrievalExpression',
        "Message.messageEventDefinition": 'A_messageRef_messageEventDefinition',
        "Message.messageFlow": 'A_messageRef_messageFlow',
        "Message.operation": 'A_inMessageRef_operation',
        "Message.receiveTask": 'A_messageRef_receiveTask',
        "Message.sendTask": 'A_messageRef_sendTask',
        "MessageFlow.choreographyTask": 'A_messageFlowRef_choreographyTask',
        "MessageFlow.collaboration": 'A_messageFlows_collaboration',
        "MessageFlow.communication": 'A_messageFlowRefs_communication',
        "MessageFlow.messageFlowAssociation": 'A_innerMessageFlowRef_messageFlowAssociation',
        "MessageFlowAssociation.collaboration": 'A_messageFlowAssociations_collaboration',
        "Monitoring.flowElement": 'A_monitoring_flowElement',
        "Monitoring.process": 'A_monitoring_process',
        "Operation.interface": 'A_operations_interface',
        "Operation.ioBinding": 'A_operationRef_ioBinding',
        "Operation.messageEventDefinition": 'A_operationRef_messageEventDefinition',
        "Operation.receiveTask": 'A_operationRef_receiveTask',
        "Operation.sendTask": 'A_operationRef_sendTask',
        "Operation.serviceTask": 'A_operationRef_serviceTask',
        "OutputSet.catchEvent": 'A_outputSet_catchEvent',
        "OutputSet.inputOutputBinding": 'A_outputDataRef_inputOutputBinding',
        "OutputSet.inputOutputSpecification": 'A_outputSets_inputOutputSpecification',
        "Participant.choreographyActivity": 'A_initiatingParticipantRef_choreographyActivity',
        "Participant.collaboration": 'A_participants_collaboration',
        "Participant.conversationNode": 'A_participantRefs_conversationNode',
        "Participant.globalChoreographyTask": 'A_initiatingParticipantRef_globalChoreographyTask',
        "Participant.participantAssociation": 'A_innerParticipantRef_participantAssociation',
        "Participant.partnerEntityRef": 'A_partnerEntityRef_participantRef',
        "Participant.partnerRoleRef": 'A_partnerRoleRef_participantRef',
        "ParticipantAssociation.callChoreographyActivity": 'A_participantAssociations_callChoreographyActivity',
        "ParticipantAssociation.callConversation": 'A_participantAssociations_callConversation',
        "ParticipantAssociation.collaboration": 'A_participantAssociations_collaboration',
        "ParticipantMultiplicity.participant": 'A_participantMultiplicity_participant',
        "Process.participant": 'A_processRef_participant',
        "Process.process": 'A_supports_process',
        "Property.activity": 'A_properties_activity',
        "Property.event": 'A_properties_event',
        "Property.process": 'A_properties_process',
        "Relationship.definition": 'A_relationships_definition',
        "Rendering.globalUserTask": 'A_renderings_globalUserTask',
        "Rendering.usertask": 'A_renderings_usertask',
        "Resource.activityResource": 'A_resourceRef_activityResource',
        "ResourceAssignmentExpression.activityResource": 'A_resourceAssignmentExpression_activityResource',
        "ResourceParameter.resource": 'A_resourceParameters_resource',
        "ResourceParameter.resourceParameterBinding": 'A_parameterRef_resourceParameterBinding',
        "ResourceParameterBinding.activityResource": 'A_resourceParameterBindings_activityResource',
        "ResourceRole.activity": 'A_resources_activity',
        "ResourceRole.globalTask": 'A_resources_globalTask',
        "ResourceRole.process": 'A_resources_process',
        "RootElement.definition": 'A_rootElements_definition',
        "SequenceFlow.activity": 'A_default_activity',
        "SequenceFlow.complexGateway": 'A_default_complexGateway',
        "SequenceFlow.exclusiveGateway": 'A_default_exclusiveGateway',
        "SequenceFlow.inclusiveGateway": 'A_default_inclusiveGateway',
        "Signal.signalEventDefinition": 'A_signalRef_signalEventDefinition',
    },
}

# ---------------------------------------------------------------------------
# association table (raw CMOF memberEnd name-pairs per A_* association);
# file order - the writer emits members in this order
# ---------------------------------------------------------------------------
_ASSOCIATIONS = {
    "A_errorRefs_operation": ("Operation-errorRefs", "A_errorRefs_operation-operation"),
    "A_inMessageRef_operation": ("Operation-inMessageRef", "A_inMessageRef_operation-operation"),
    "A_outMessageRef_operation": ("Operation-outMessageRef", "A_outMessageRef_operation-operation"),
    "A_operations_interface": ("Interface-operations", "A_operations_interface-interface"),
    "A_definitionalCollaborationRef_process": ("Process-definitionalCollaborationRef", "A_definitionalCollaborationRef_process-process"),
    "A_partitionElement_lane": ("Lane-partitionElement", "A_partitionElement_lane-lane"),
    "A_flowNodeRefs_lanes": ("Lane-flowNodeRefs", "FlowNode-lanes"),
    "A_partitionElementRef_lane": ("Lane-partitionElementRef", "A_partitionElementRef_lane-lane"),
    "A_auditing_process": ("Process-auditing", "A_auditing_process-process"),
    "A_monitoring_process": ("Process-monitoring", "A_monitoring_process-process"),
    "A_properties_process": ("Process-properties", "A_properties_process-process"),
    "A_lanes_laneSet": ("LaneSet-lanes", "A_lanes_laneSet-laneSet"),
    "A_childLaneSet_parentLane": ("Lane-childLaneSet", "A_childLaneSet_parentLane-parentLane"),
    "A_resources_globalTask": ("GlobalTask-resources", "A_resources_globalTask-globalTask"),
    "A_supports_process": ("Process-supports", "A_supports_process-process"),
    "A_resources_process": ("Process-resources", "A_resources_process-process"),
    "A_artifacts_process": ("Process-artifacts", "A_artifacts_process-process"),
    "A_correlationSubscriptions_process": ("Process-correlationSubscriptions", "A_correlationSubscriptions_process-process"),
    "A_renderings_usertask": ("UserTask-renderings", "A_renderings_usertask-usertask"),
    "A_renderings_globalUserTask": ("GlobalUserTask-renderings", "A_renderings_globalUserTask-globalUserTask"),
    "A_activationCondition_complexGateway": ("ComplexGateway-activationCondition", "A_activationCondition_complexGateway-complexGateway"),
    "A_default_inclusiveGateway": ("InclusiveGateway-default", "A_default_inclusiveGateway-inclusiveGateway"),
    "A_default_exclusiveGateway": ("ExclusiveGateway-default", "A_default_exclusiveGateway-exclusiveGateway"),
    "A_default_complexGateway": ("ComplexGateway-default", "A_default_complexGateway-complexGateway"),
    "A_valueRef_extensionAttributeValue": ("ExtensionAttributeValue-valueRef", "A_valueRef_extensionAttributeValue-extensionAttributeValue"),
    "A_value_extensionAttributeValue": ("ExtensionAttributeValue-value", "A_value_extensionAttributeValue-extensionAttributeValue"),
    "A_extensionDefinitions_baseElement": ("BaseElement-extensionDefinitions", "A_extensionDefinitions_baseElement-baseElement"),
    "A_definition_extension": ("Extension-definition", "A_definition_extension-extension"),
    "A_extensionAttributeDefinitions_extensionDefinition": ("ExtensionDefinition-extensionAttributeDefinitions", "ExtensionAttributeDefinition-extensionDefinition"),
    "A_extensionValues_baseElement": ("BaseElement-extensionValues", "A_extensionValues_baseElement-baseElement"),
    "A_extensionAttributeDefinition_extensionAttributeValue": ("ExtensionAttributeValue-extensionAttributeDefinition", "A_extensionAttributeDefinition_extensionAttributeValue-extensionAttributeValue"),
    "A_documentation_baseElement": ("BaseElement-documentation", "A_documentation_baseElement-baseElement"),
    "A_sources_relationship": ("Relationship-sources", "A_sources_relationship-relationship"),
    "A_targets_relationship": ("Relationship-targets", "A_targets_relationship-relationship"),
    "A_dataInputAssociation_throwEvent": ("ThrowEvent-dataInputAssociation", "A_dataInputAssociation_throwEvent-throwEvent"),
    "A_dataOutputAssociation_catchEvent": ("CatchEvent-dataOutputAssociation", "A_dataOutputAssociation_catchEvent-catchEvent"),
    "A_activityRef_compensateEventDefinition": ("CompensateEventDefinition-activityRef", "A_activityRef_compensateEventDefinition-compensateEventDefinition"),
    "A_inputSet_throwEvent": ("ThrowEvent-inputSet", "A_inputSet_throwEvent-throwEvent"),
    "A_structureRef_signal": ("Signal-structureRef", "A_structureRef_signal-signal"),
    "A_messageRef_messageEventDefinition": ("MessageEventDefinition-messageRef", "A_messageRef_messageEventDefinition-messageEventDefinition"),
    "A_outputSet_catchEvent": ("CatchEvent-outputSet", "A_outputSet_catchEvent-catchEvent"),
    "A_structureRef_escalation": ("Escalation-structureRef", "A_structureRef_escalation-escalation"),
    "A_eventDefinitionRefs_throwEvent": ("ThrowEvent-eventDefinitionRefs", "A_eventDefinitionRefs_throwEvent-throwEvent"),
    "A_eventDefinitionRefs_catchEvent": ("CatchEvent-eventDefinitionRefs", "A_eventDefinitionRefs_catchEvent-catchEvent"),
    "A_errorRef_errorEventDefinition": ("ErrorEventDefinition-errorRef", "A_errorRef_errorEventDefinition-errorEventDefinition"),
    "A_escalationRef_escalationEventDefinition": ("EscalationEventDefinition-escalationRef", "A_escalationRef_escalationEventDefinition-escalationEventDefinition"),
    "A_signalRef_signalEventDefinition": ("SignalEventDefinition-signalRef", "A_signalRef_signalEventDefinition-signalEventDefinition"),
    "A_eventDefinitions_throwEvent": ("ThrowEvent-eventDefinitions", "A_eventDefinitions_throwEvent-throwEvent"),
    "A_eventDefinitions_catchEvent": ("CatchEvent-eventDefinitions", "A_eventDefinitions_catchEvent-catchEvent"),
    "A_dataInputs_throwEvent": ("ThrowEvent-dataInputs", "A_dataInputs_throwEvent-throwEvent"),
    "A_dataOutputs_catchEvent": ("CatchEvent-dataOutputs", "A_dataOutputs_catchEvent-catchEvent"),
    "A_operationRef_messageEventDefinition": ("MessageEventDefinition-operationRef", "A_operationRef_messageEventDefinition-messageEventDefinition"),
    "A_condition_conditionalEventDefinition": ("ConditionalEventDefinition-condition", "A_condition_conditionalEventDefinition-conditionalEventDefinition"),
    "A_timeDate_timerEventDefinition": ("TimerEventDefinition-timeDate", "A_timeDate_timerEventDefinition-timerEventDefinition"),
    "A_timeCycle_timerEventDefinition": ("TimerEventDefinition-timeCycle", "A_timeCycle_timerEventDefinition-timerEventDefinition"),
    "A_target_source": ("LinkEventDefinition-target", "LinkEventDefinition-source"),
    "A_properties_event": ("Event-properties", "A_properties_event-event"),
    "A_timeDuration_timerEventDefinition": ("TimerEventDefinition-timeDuration", "A_timeDuration_timerEventDefinition-timerEventDefinition"),
    "A_dataState_itemAwareElement": ("ItemAwareElement-dataState", "A_dataState_itemAwareElement-itemAwareElement"),
    "A_operationRef_ioBinding": ("InputOutputBinding-operationRef", "A_operationRef_ioBinding-ioBinding"),
    "A_sourceRef_dataAssociation": ("DataAssociation-sourceRef", "A_sourceRef_dataAssociation-dataAssociation"),
    "A_targetRef_dataAssociation": ("DataAssociation-targetRef", "A_targetRef_dataAssociation-dataAssociation"),
    "A_transformation_dataAssociation": ("DataAssociation-transformation", "A_transformation_dataAssociation-dataAssociation"),
    "A_dataInputRefs_inputSetRefs": ("InputSet-dataInputRefs", "DataInput-inputSetRefs"),
    "A_dataOutputRefs_outputSetRefs": ("OutputSet-dataOutputRefs", "DataOutput-outputSetRefs"),
    "A_inputSets_inputOutputSpecification": ("InputOutputSpecification-inputSets", "A_inputSets_inputOutputSpecification-inputOutputSpecification"),
    "A_outputSets_inputOutputSpecification": ("InputOutputSpecification-outputSets", "A_outputSets_inputOutputSpecification-inputOutputSpecification"),
    "A_dataInputs_inputOutputSpecification": ("InputOutputSpecification-dataInputs", "A_dataInputs_inputOutputSpecification-inputOutputSpecification"),
    "A_dataOutputs_inputOutputSpecification": ("InputOutputSpecification-dataOutputs", "A_dataOutputs_inputOutputSpecification-inputOutputSpecification"),
    "A_inputSetRefs_outputSetRefs": ("OutputSet-inputSetRefs", "InputSet-outputSetRefs"),
    "A_inputDataRef_inputOutputBinding": ("InputOutputBinding-inputDataRef", "A_inputDataRef_inputOutputBinding-inputOutputBinding"),
    "A_outputDataRef_inputOutputBinding": ("InputOutputBinding-outputDataRef", "A_outputDataRef_inputOutputBinding-inputOutputBinding"),
    "A_whileExecutingInputRefs_inputSetWithWhileExecuting": ("InputSet-whileExecutingInputRefs", "DataInput-inputSetWithWhileExecuting"),
    "A_optionalInputRefs_inputSetWithOptional": ("InputSet-optionalInputRefs", "DataInput-inputSetWithOptional"),
    "A_outputSetWithOptional_optionalOutputRefs": ("DataOutput-outputSetWithOptional", "OutputSet-optionalOutputRefs"),
    "A_outputSetWithWhileExecuting_whileExecutingOutputRefs": ("DataOutput-outputSetWithWhileExecuting", "OutputSet-whileExecutingOutputRefs"),
    "A_assignment_dataAssociation": ("DataAssociation-assignment", "A_assignment_dataAssociation-dataAssociation"),
    "A_dataStoreRef_dataStoreReference": ("DataStoreReference-dataStoreRef", "A_dataStoreRef_dataStoreReference-dataStoreReference"),
    "A_itemSubjectRef_itemAwareElement": ("ItemAwareElement-itemSubjectRef", "A_itemSubjectRef_itemAwareElement-itemAwareElement"),
    "A_from_assignment": ("Assignment-from", "A_from_assignment-assignment"),
    "A_to_assignment": ("Assignment-to", "A_to_assignment-assignment"),
    "A_dataObjectRef_dataObject": ("DataObjectReference-dataObjectRef", "A_dataObjectRef_dataObject-dataObject"),
    "A_calledCollaborationRef_callConversation": ("CallConversation-calledCollaborationRef", "A_calledCollaborationRef_callConversation-callConversation"),
    "A_participantRefs_conversationNode": ("ConversationNode-participantRefs", "A_participantRefs_conversationNode-conversationNode"),
    "A_messageFlowRefs_communication": ("ConversationNode-messageFlowRefs", "A_messageFlowRefs_communication-communication"),
    "A_participantAssociations_callConversation": ("CallConversation-participantAssociations", "A_participantAssociations_callConversation-callConversation"),
    "A_correlationKeys_collaboration": ("Collaboration-correlationKeys", "A_correlationKeys_collaboration-collaboration"),
    "A_correlationKeys_conversationNode": ("ConversationNode-correlationKeys", "A_correlationKeys_conversationNode-conversationNode"),
    "A_innerConversationNodeRef_conversationAssociation": ("ConversationAssociation-innerConversationNodeRef", "A_innerConversationNodeRef_conversationAssociation-conversationAssociation"),
    "A_outerConversationNodeRef_conversationAssociation": ("ConversationAssociation-outerConversationNodeRef", "A_outerConversationNodeRef_conversationAssociation-conversationAssociation"),
    "A_conversationNodes_subConversation": ("SubConversation-conversationNodes", "A_conversationNodes_subConversation-subConversation"),
    "A_sourceRef_outgoingConversationLinks": ("ConversationLink-sourceRef", "InteractionNode-outgoingConversationLinks"),
    "A_targetRef_incomingConversationLinks": ("ConversationLink-targetRef", "InteractionNode-incomingConversationLinks"),
    "A_correlationPropertyRef_correlationKey": ("CorrelationKey-correlationPropertyRef", "A_correlationPropertyRef_correlationKey-correlationKey"),
    "A_supportedInterfaceRefs_callableElements": ("CallableElement-supportedInterfaceRefs", "A_supportedInterfaceRefs_callableElements-callableElements"),
    "A_ioBinding_callableElement": ("CallableElement-ioBinding", "A_ioBinding_callableElement-callableElement"),
    "A_ioSpecification_callableElement": ("CallableElement-ioSpecification", "A_ioSpecification_callableElement-callableElement"),
    "A_messagePath_correlationset": ("CorrelationPropertyRetrievalExpression-messagePath", "A_messagePath_correlationset-correlationset"),
    "A_structureRef_error": ("Error-structureRef", "A_structureRef_error-error"),
    "A_evaluatesToTypeRef_formalExpression": ("FormalExpression-evaluatesToTypeRef", "A_evaluatesToTypeRef_formalExpression-formalExpression"),
    "A_conditionExpression_sequenceFlow": ("SequenceFlow-conditionExpression", "A_conditionExpression_sequenceFlow-sequenceFlow"),
    "A_flowElements_container": ("FlowElementsContainer-flowElements", "A_flowElements_container-container"),
    "A_sourceRef_outgoing_flow": ("SequenceFlow-sourceRef", "FlowNode-outgoing"),
    "A_targetRef_incoming_flow": ("SequenceFlow-targetRef", "FlowNode-incoming"),
    "A_correlationPropertyRetrievalExpression_correlationproperty": ("CorrelationProperty-correlationPropertyRetrievalExpression", "A_correlationPropertyRetrievalExpression_correlationproperty-correlationproperty"),
    "A_messageRef_correlationPropertyRetrievalExpression": ("CorrelationPropertyRetrievalExpression-messageRef", "A_messageRef_correlationPropertyRetrievalExpression-correlationPropertyRetrievalExpression"),
    "A_dataPath_correlationPropertyBinding": ("CorrelationPropertyBinding-dataPath", "A_dataPath_correlationPropertyBinding-correlationPropertyBinding"),
    "A_correlationPropertyRef_correlationPropertyBinding": ("CorrelationPropertyBinding-correlationPropertyRef", "A_correlationPropertyRef_correlationPropertyBinding-correlationPropertyBinding"),
    "A_resourceParameters_resource": ("Resource-resourceParameters", "A_resourceParameters_resource-resource"),
    "A_import_itemDefinition": ("ItemDefinition-import", "A_import_itemDefinition-itemDefinition"),
    "A_correlationKeyRef_correlationSubscription": ("CorrelationSubscription-correlationKeyRef", "A_correlationKeyRef_correlationSubscription-correlationSubscription"),
    "A_correlationPropertyBinding_correlationSubscription": ("CorrelationSubscription-correlationPropertyBinding", "A_correlationPropertyBinding_correlationSubscription-correlationSubscription"),
    "A_auditing_flowElement": ("FlowElement-auditing", "A_auditing_flowElement-flowElement"),
    "A_monitoring_flowElement": ("FlowElement-monitoring", "A_monitoring_flowElement-flowElement"),
    "A_type_correlationProperty": ("CorrelationProperty-type", "A_type_correlationProperty-correlationProperty"),
    "A_type_resourceParameter": ("ResourceParameter-type", "A_type_resourceParameter-resourceParameter"),
    "A_itemRef_message": ("Message-itemRef", "A_itemRef_message-message"),
    "A_laneSets_flowElementsContainer": ("FlowElementsContainer-laneSets", "A_laneSets_flowElementsContainer-flowElementsContainer"),
    "A_messageFlowAssociations_collaboration": ("Collaboration-messageFlowAssociations", "A_messageFlowAssociations_collaboration-collaboration"),
    "A_participantAssociations_collaboration": ("Collaboration-participantAssociations", "A_participantAssociations_collaboration-collaboration"),
    "A_artifacts_collaboration": ("Collaboration-artifacts", "A_artifacts_collaboration-collaboration"),
    "A_conversationAssociations_converstaionAssociations": ("Collaboration-conversationAssociations", "A_conversationAssociations_converstaionAssociations-converstaionAssociations"),
    "A_choreographyRef_collaboration": ("Collaboration-choreographyRef", "A_choreographyRef_collaboration-collaboration"),
    "A_innerParticipantRef_participantAssociation": ("ParticipantAssociation-innerParticipantRef", "A_innerParticipantRef_participantAssociation-participantAssociation"),
    "A_outerParticipantRef_participantAssociation": ("ParticipantAssociation-outerParticipantRef", "A_outerParticipantRef_participantAssociation-participantAssociation"),
    "A_endPointRefs_participant": ("Participant-endPointRefs", "A_endPointRefs_participant-participant"),
    "A_participantMultiplicity_participant": ("Participant-participantMultiplicity", "A_participantMultiplicity_participant-participant"),
    "A_interfaceRefs_participant": ("Participant-interfaceRefs", "A_interfaceRefs_participant-participant"),
    "A_partnerEntityRef_participantRef": ("A_partnerEntityRef_participantRef-partnerEntityRef", "PartnerEntity-participantRef"),
    "A_partnerRoleRef_participantRef": ("A_partnerRoleRef_participantRef-partnerRoleRef", "PartnerRole-participantRef"),
    "A_processRef_participant": ("Participant-processRef", "A_processRef_participant-participant"),
    "A_innerMessageFlowRef_messageFlowAssociation": ("MessageFlowAssociation-innerMessageFlowRef", "A_innerMessageFlowRef_messageFlowAssociation-messageFlowAssociation"),
    "A_outerMessageFlowRef_messageFlowAssociation": ("MessageFlowAssociation-outerMessageFlowRef", "A_outerMessageFlowRef_messageFlowAssociation-messageFlowAssociation"),
    "A_targetRef_messageFlow": ("MessageFlow-targetRef", "A_targetRef_messageFlow-messageFlow"),
    "A_messageRef_messageFlow": ("MessageFlow-messageRef", "A_messageRef_messageFlow-messageFlow"),
    "A_sourceRef_messageFlow": ("MessageFlow-sourceRef", "A_sourceRef_messageFlow-messageFlow"),
    "A_participants_collaboration": ("Collaboration-participants", "A_participants_collaboration-collaboration"),
    "A_messageFlows_collaboration": ("Collaboration-messageFlows", "A_messageFlows_collaboration-collaboration"),
    "A_conversations_collaboration": ("Collaboration-conversations", "A_conversations_collaboration-collaboration"),
    "A_conversationLinks_collaboration": ("Collaboration-conversationLinks", "A_conversationLinks_collaboration-collaboration"),
    "A_participantAssociations_callChoreographyActivity": ("CallChoreography-participantAssociations", "A_participantAssociations_callChoreographyActivity-callChoreographyActivity"),
    "A_calledChoreographyRef_callChoreographyActivity": ("CallChoreography-calledChoreographyRef", "A_calledChoreographyRef_callChoreographyActivity-callChoreographyActivity"),
    "A_messageFlowRef_choreographyTask": ("ChoreographyTask-messageFlowRef", "A_messageFlowRef_choreographyTask-choreographyTask"),
    "A_initiatingParticipantRef_choreographyActivity": ("ChoreographyActivity-initiatingParticipantRef", "A_initiatingParticipantRef_choreographyActivity-choreographyActivity"),
    "A_participantRefs_choreographyActivity": ("ChoreographyActivity-participantRefs", "A_participantRefs_choreographyActivity-choreographyActivity"),
    "A_artifacts_subChoreography": ("SubChoreography-artifacts", "A_artifacts_subChoreography-subChoreography"),
    "A_correlationKeys_choreographyActivity": ("ChoreographyActivity-correlationKeys", "A_correlationKeys_choreographyActivity-choreographyActivity"),
    "A_initiatingParticipantRef_globalChoreographyTask": ("GlobalChoreographyTask-initiatingParticipantRef", "A_initiatingParticipantRef_globalChoreographyTask-globalChoreographyTask"),
    "A_sourceRef_outgoing_association": ("Association-sourceRef", "A_sourceRef_outgoing_association-outgoing"),
    "A_targetRef_incoming_association": ("Association-targetRef", "A_targetRef_incoming_association-incoming"),
    "A_categoryValueRef_categoryValueRef": ("Group-categoryValueRef", "A_categoryValueRef_categoryValueRef-categoryValueRef"),
    "A_categoryValue_category": ("Category-categoryValue", "A_categoryValue_category-category"),
    "A_categorizedFlowElements_categoryValueRef": ("CategoryValue-categorizedFlowElements", "FlowElement-categoryValueRef"),
    "A_event_complexBehaviorDefinition": ("ComplexBehaviorDefinition-event", "A_event_complexBehaviorDefinition-complexBehaviorDefinition"),
    "A_expression_resourceAssignmentExpression": ("ResourceAssignmentExpression-expression", "A_expression_resourceAssignmentExpression-resourceAssignmentExpression"),
    "A_expression_resourceParameterBinding": ("ResourceParameterBinding-expression", "A_expression_resourceParameterBinding-resourceParameterBinding"),
    "A_noneBehaviorEventRef_multiInstanceLoopCharacteristics": ("MultiInstanceLoopCharacteristics-noneBehaviorEventRef", "A_noneBehaviorEventRef_multiInstanceLoopCharacteristics-multiInstanceLoopCharacteristics"),
    "A_oneBehaviorEventRef_multiInstanceLoopCharacteristics": ("MultiInstanceLoopCharacteristics-oneBehaviorEventRef", "A_oneBehaviorEventRef_multiInstanceLoopCharacteristics-multiInstanceLoopCharacteristics"),
    "A_completionCondition_multiInstanceLoopCharacteristics": ("MultiInstanceLoopCharacteristics-completionCondition", "A_completionCondition_multiInstanceLoopCharacteristics-multiInstanceLoopCharacteristics"),
    "A_condition_complexBehaviorDefinition": ("ComplexBehaviorDefinition-condition", "A_condition_complexBehaviorDefinition-complexBehaviorDefinition"),
    "A_resourceRef_activityResource": ("ResourceRole-resourceRef", "A_resourceRef_activityResource-activityResource"),
    "A_messageRef_sendTask": ("SendTask-messageRef", "A_messageRef_sendTask-sendTask"),
    "A_messageRef_receiveTask": ("ReceiveTask-messageRef", "A_messageRef_receiveTask-receiveTask"),
    "A_operationRef_serviceTask": ("ServiceTask-operationRef", "A_operationRef_serviceTask-serviceTask"),
    "A_calledElementRef_callActivity": ("CallActivity-calledElementRef", "A_calledElementRef_callActivity-callActivity"),
    "A_loopCardinality_multiInstanceLoopCharacteristics": ("MultiInstanceLoopCharacteristics-loopCardinality", "A_loopCardinality_multiInstanceLoopCharacteristics-multiInstanceLoopCharacteristics"),
    "A_properties_activity": ("Activity-properties", "A_properties_activity-activity"),
    "A_resources_activity": ("Activity-resources", "A_resources_activity-activity"),
    "A_loopCondition_standardLoopCharacteristics": ("StandardLoopCharacteristics-loopCondition", "A_loopCondition_standardLoopCharacteristics-standardLoopCharacteristics"),
    "A_loopCharacteristics_activity": ("Activity-loopCharacteristics", "A_loopCharacteristics_activity-activity"),
    "A_ioSpecification_activity": ("Activity-ioSpecification", "A_ioSpecification_activity-activity"),
    "A_completionCondition_adHocSubProcess": ("AdHocSubProcess-completionCondition", "A_completionCondition_adHocSubProcess-adHocSubProcess"),
    "A_operationRef_receiveTask": ("ReceiveTask-operationRef", "A_operationRef_receiveTask-receiveTask"),
    "A_operationRef_sendTask": ("SendTask-operationRef", "A_operationRef_sendTask-sendTask"),
    "A_complexBehaviorDefinition_multiInstanceLoopCharacteristics": ("MultiInstanceLoopCharacteristics-complexBehaviorDefinition", "A_complexBehaviorDefinition_multiInstanceLoopCharacteristics-multiInstanceLoopCharacteristics"),
    "A_resourceParameterBindings_activityResource": ("ResourceRole-resourceParameterBindings", "A_resourceParameterBindings_activityResource-activityResource"),
    "A_resourceAssignmentExpression_activityResource": ("ResourceRole-resourceAssignmentExpression", "A_resourceAssignmentExpression_activityResource-activityResource"),
    "A_loopMaximum_standardLoopCharacteristics": ("StandardLoopCharacteristics-loopMaximum", "A_loopMaximum_standardLoopCharacteristics-standardLoopCharacteristics"),
    "A_dataInputAssociations_activity": ("Activity-dataInputAssociations", "A_dataInputAssociations_activity-activity"),
    "A_dataOutputAssociations_activity": ("Activity-dataOutputAssociations", "A_dataOutputAssociations_activity-activity"),
    "A_parameterRef_resourceParameterBinding": ("ResourceParameterBinding-parameterRef", "A_parameterRef_resourceParameterBinding-resourceParameterBinding"),
    "A_loopDataInputRef_multiInstanceLoopCharacteristics": ("MultiInstanceLoopCharacteristics-loopDataInputRef", "A_loopDataInputRef_multiInstanceLoopCharacteristics-multiInstanceLoopCharacteristics"),
    "A_loopDataOutputRef_multiInstanceLoopCharacteristics": ("MultiInstanceLoopCharacteristics-loopDataOutputRef", "A_loopDataOutputRef_multiInstanceLoopCharacteristics-multiInstanceLoopCharacteristics"),
    "A_inputDataItem_multiInstanceLoopCharacteristics": ("MultiInstanceLoopCharacteristics-inputDataItem", "A_inputDataItem_multiInstanceLoopCharacteristics-multiInstanceLoopCharacteristics"),
    "A_outputDataItem_multiInstanceLoopCharacteristics": ("MultiInstanceLoopCharacteristics-outputDataItem", "A_outputDataItem_multiInstanceLoopCharacteristics-multiInstanceLoopCharacteristics"),
    "A_boundaryEventRefs_attachedToRef": ("Activity-boundaryEventRefs", "BoundaryEvent-attachedToRef"),
    "A_default_activity": ("Activity-default", "A_default_activity-activity"),
    "A_artifacts_subProcess": ("SubProcess-artifacts", "A_artifacts_subProcess-subProcess"),
    "A_diagrams_definitions": ("Definitions-diagrams", "A_diagrams_definitions-definitions"),
    "A_imports_definition": ("Definitions-imports", "A_imports_definition-definition"),
    "A_extensions_definitions": ("Definitions-extensions", "A_extensions_definitions-definitions"),
    "A_relationships_definition": ("Definitions-relationships", "A_relationships_definition-definition"),
    "A_rootElements_definition": ("Definitions-rootElements", "A_rootElements_definition-definition"),
}

_CLASSES = [BaseElement, FlowElement, FlowNode, Activity, FlowElementsContainer, SubProcess, AdHocSubProcess, Artifact, Assignment, Association, Auditing, InteractionNode, Event, CatchEvent, BoundaryEvent, Task, BusinessRuleTask, CallActivity, ChoreographyActivity, CallChoreography, ConversationNode, CallConversation, RootElement, CallableElement, EventDefinition, CancelEventDefinition, Category, CategoryValue, Collaboration, Choreography, ChoreographyTask, CompensateEventDefinition, ComplexBehaviorDefinition, Gateway, ComplexGateway, ConditionalEventDefinition, Conversation, ConversationAssociation, ConversationLink, CorrelationKey, CorrelationProperty, CorrelationPropertyBinding, CorrelationPropertyRetrievalExpression, CorrelationSubscription, DataAssociation, ItemAwareElement, DataInput, DataInputAssociation, DataObject, DataObjectReference, DataOutput, DataOutputAssociation, DataState, DataStore, DataStoreReference, Definitions, Documentation, ThrowEvent, EndEvent, EndPoint, Error, ErrorEventDefinition, Escalation, EscalationEventDefinition, EventBasedGateway, ExclusiveGateway, Expression, Extension, ExtensionAttributeDefinition, ExtensionAttributeValue, ExtensionDefinition, FormalExpression, GlobalTask, GlobalBusinessRuleTask, GlobalChoreographyTask, GlobalConversation, GlobalManualTask, GlobalScriptTask, GlobalUserTask, Group, ResourceRole, Performer, HumanPerformer, ImplicitThrowEvent, Import, InclusiveGateway, InputOutputBinding, InputOutputSpecification, InputSet, Interface, IntermediateCatchEvent, IntermediateThrowEvent, ItemDefinition, Lane, LaneSet, LinkEventDefinition, LoopCharacteristics, ManualTask, Message, MessageEventDefinition, MessageFlow, MessageFlowAssociation, Monitoring, MultiInstanceLoopCharacteristics, Operation, OutputSet, ParallelGateway, Participant, ParticipantAssociation, ParticipantMultiplicity, PartnerEntity, PartnerRole, PotentialOwner, Process, Property, ReceiveTask, Relationship, Rendering, Resource, ResourceAssignmentExpression, ResourceParameter, ResourceParameterBinding, ScriptTask, SendTask, SequenceFlow, ServiceTask, Signal, SignalEventDefinition, StandardLoopCharacteristics, StartEvent, SubChoreography, SubConversation, TerminateEventDefinition, TextAnnotation, TimerEventDefinition, Transaction, UserTask]

def _finish():
    for c in _CLASSES:
        props = {}
        for k in reversed(c.__mro__):
            for n, d in getattr(k, '_DECL', {}).items():
                props[n] = d
        c._props = props
    for c in _CLASSES:
        decl = c.__dict__.get('_DECL')
        if not decl:
            continue
        for d in decl.values():
            d.owner_cls = c.__name__
            for o in c.__dict__.get('_OPPS', {}).get(d.name, ()):
                if d.opp is None:
                    d.opp = o
        for n, d in decl.items():
            setattr(c, n, d)
_finish()


def class_of(name):
    """Look up a generated BPMN class by metamodel name."""
    for c in _CLASSES:
        if c.__name__ == name:
            return c
    raise KeyError(name)

