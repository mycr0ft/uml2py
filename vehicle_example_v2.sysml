package VehicleExample {
  /* v1 packageImport of 'Common' elided: target grammar reader has no import */
  package Common;
  part def Wheel;
  part def Vehicle {
    part wheels[1..4] : Wheel;
    attribute mass : Kilogram;
    attribute paint : VehicleColor;
    port pwr : PowerIf;
    port aux;
    part frontAxle : Axle;
    part rearAxle : Axle;
    attribute rawA : Kilogram;
    attribute rawB : Kilogram;
    ref occurrence legacy : LegacyPart;
    perform action totalMass {
      in extra : Kilogram;
      out result;
    }
    connection axleLink connect frontAxle to rearAxle;
    binding massBind bind rawA = rawB;
  }
  part def Axle;
  attribute def Kilogram;
  enum def VehicleColor {
    red;
    green;
    blue;
  }
  port def PowerIf;
  occurrence def LegacyPart;
  item def MoveCommand;
  part def Operator;
  state def OpMode {
    state on;
    state off;
    transition t1 first on then off;
  }
  action def Generate {
    in demand;
  }
  use case def OperateVehicle {
    include use case : StartEngine;
  }
  use case def StartEngine;
  part def Car {
    ref part spareWheel : Wheel;
  }
  requirement <'R-1'> CarIsVehicle {
    doc /* A car shall be a specialization of vehicle. */
  }
  requirement DerivedReq;
  connection def WheelToAxle {
    end wheelEnd : Wheel;
    end axleEnd : Axle;
  }
  verification def CheckMass {
    objective obj_CheckMass {
      verify CarIsVehicle;
    }
    return verdict : VerificationCases::VerdictKind;
  }
  connection : DerivationConnections::Derivation connect DerivedReq to CarIsVehicle;
  metadata def RefineData { attribute isRefine : Boolean; }
  dependency refineTag from Vehicle to CarIsVehicle {
    @RefineData { isRefine = true; }
  }
  dependency refinesVeh from Vehicle to CarIsVehicle;
  dependency usesLegacy from Vehicle to LegacyPart;
  allocation def {
    end :>> source : Wheel;
    end :>> target : Wheel;
    allocate source.wheels to target.spareWheel;
  }
}
