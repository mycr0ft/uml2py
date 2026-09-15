package Wave3 {
  metadata def PortData { attribute isFullPort : Boolean; }
  part def Controller {
    part fullPort : MotorIf {@PortData {isFullPort = true;}}
    port proxyPort;
    /* v1 ProxyPort has no normative mapping (7.8.7 Table 30; SYSML2_-329) */
    out attribute torque : Kilogram;
    in flowIn;
    inout ref occurrence flowRef : Axle;
  }
  constraint def Adder {
    in attribute a : Kilogram;
    in attribute b : Kilogram;
    in attribute c : Kilogram;
    constraint sumCheck {
      language "OCL2.0"
      /* c == a + b */
    }
  }
  part def Block1 {
    attribute massValue : Kilogram;
  }
  part inst1 : Block1 {
    redefines massValue = "Hello InstanceSpecification";
  }
  part def Holder {
    ref part pv : Block1 = inst1;
  }
  part def Block2;
  connection def AssocD {
    end e1 : Block1;
    end e2 : Block2;
  }
  part inst2 : Block2;
  connection link1 : AssocD connect inst1 to inst2;
  /* v1 Interaction 'Comm' elided: Interaction -> Interaction (7.7.8.3.6; 2 Lifeline -> PartUsage, 1 Message -> Flow) but the target grammar reader has no interaction element */
  /* v1 StateInvariant 'inv1' elided: mapped to v2 Invariant (7.7.8.3.17) but the target grammar reader has no invariant element */
  /* v1 InteractionUse 'useBase' elided: mapped to v2 Step (7.7.8.3.9) but the target grammar reader has no step element */
  action exec1;
}
