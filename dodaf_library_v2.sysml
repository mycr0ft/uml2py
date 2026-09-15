package <'DoDAF Class Library'> {
  /* v1 stereotype applied: StandardProfileL2::ModelLibrary */
  attribute def SecurityAttributes {
    doc /* W3C XML Schema for the Intelligence Community Metadata Standard for Information Security Marking (IC-ISM), which is part of the IC standards for Information Assurance. */
    /* v1 stereotype applied: updm::MeasurementSet */
    attribute classification : ClassificationType;
    attribute dateOfExemptedSource : String;
    attribute typeOfExemptedSource : String;
    attribute nonICmarkings : String;
    attribute declassException : String;
    attribute declassEvent : String;
    attribute declassDate : String;
    attribute derivedFrom : String;
    attribute classifiedBy : String;
    attribute FGIsourceProtected : String;
    attribute FGIsourceOpen : String;
    attribute DisseminationControls : String;
    attribute DeclassManualReview : String;
    attribute ownerProducer : String;
    attribute classificationReason : String;
    attribute SCIControls : String;
    attribute SARIdentifier : String;
    attribute releasableTo : String;
  }
  attribute def CommunicationsLinkProperties {
    doc /* Properties detailing aspects of Resource Interfaces. */
    /* v1 stereotype applied: updm::MeasurementSet */
    attribute capacity : String;
    attribute infrastructureTechnology : String;
  }
  enum def ClassificationType {
    C;
    CTS;
    <'CTS-B'>;
    <'CTS-BALK'>;
    CTSA;
    NC;
    NCA;
    NR;
    NS;
    <'NS-A'>;
    <'NS-S'>;
    NSAT;
    NU;
    R;
    S;
    TS;
    U;
  }
  attribute def InformationAssuranceProperties {
    doc /* Properties indicating the assurance of a piece of information. */
    /* v1 stereotype applied: updm::MeasurementSet */
    attribute accessControl[*] : String;
    attribute availability[*] : String;
    attribute confidentiality[*] : String;
    attribute disseminationControl[*] : String;
    attribute integrity[*] : String;
    attribute nonRepudiationConsumer[*] : String;
    attribute nonRepudiationProducer[*] : String;
  }
  attribute def InformationElementProperties {
    doc /* Predefined additional DoDAF properties for InformationElement. */
    /* v1 stereotype applied: updm::MeasurementSet */
    attribute accuracy[*] : String;
    attribute language[*] : String;
    attribute scope[*] : String;
    attribute content[*] : String;
  }
  attribute def DataElementProperties {
    doc /* Properties detailing the aspects of a DataElement. */
    /* v1 stereotype applied: updm::MeasurementSet */
    attribute accuracy : String;
    attribute scope : String;
    attribute content : String;
    attribute formatType : String;
    attribute mediaType : String;
    attribute unitOfMeasurement : String;
  }
  connection def <'packagedElement-7'> {
    end ownedEnd : SecurityAttributes;
    end classification : ClassificationType;
  }
  attribute def ExchangeProperties {
    doc /* Properties detailing aspects of exchange for Operational Exchange and/or Resource Interaction. */
    /* v1 stereotype applied: updm::MeasurementSet */
    attribute accountability[*] : String;
    attribute interoperabilityLevelAchievable[*] : String;
    attribute classification[*] : String;
    attribute classificationCaveat[*] : String;
    attribute criticality[*] : String;
    attribute periodicity[*] : String;
    attribute protectionDuration[*] : String;
    attribute protectionSuspenseCalendarDate[*] : String;
    attribute protectionTypeName[*] : String;
    attribute timeliness[*] : String;
    attribute transactionType[*] : String;
    attribute protectionDurationCode[*] : String;
    attribute releasability[*] : String;
    attribute size[*] : String;
    attribute throughput[*] : String;
  }
  attribute def OperationalActivityProperties {
    doc /* Properties detailing aspects OperationalActivities. */
    /* v1 stereotype applied: updm::MeasurementSet */
    attribute cost : String;
  }
}
