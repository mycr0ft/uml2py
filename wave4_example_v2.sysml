package Wave4 {
  part def BaseBlock {
    battr;
    attribute dattr : Kilogram subsets battr;
    part wheels : BaseBlock;
    ref part spare : BaseBlock redefines wheels;
  }
  action def Proc {
    action a1 {
      in x;
      out item result : Kilogram;
      language "OCL" /* x = y + 1; */
    }
    action a2 {
      in item inputValue;
      out item spare;
    }
    action a3 {
      in item sink;
    }
    decide dn;
    merge mn {
      in ref inputObject1;
      in ref inputObject2;
      out ref outputObject1 = (inputObject1, inputObject2);
    }
    action coa {
      in paramIn;
      in target : T2;
      out paramReturn = target.op;
    }
    action ssa {
      in target : T2;
      send Sig to target;
    }
    action aea {
      accept : Sig;
    }
    succession flow of1 of Kilogram from a1.result to a2.inputValue;
    succession flow of2 of Kilogram from a1.result to mn.inputObject1;
    succession flow of3 from a2.spare to mn.inputObject2;
    succession flow of4 from mn.outputObject1 to a3.sink;
    succession cf1 first a1 if { return : ScalarValues::Boolean; language "OCL2.0" /* x > 0 */ }.result then a2;
    succession cf2 first a1 then dn;
    succession cf3 first dn if { return : ScalarValues::Boolean; language "SysMLv1" /* else */ }.result then a3;
  }
  item def Sig;
  part def T2 {
    perform action op;
  }
  state def GuardedSM {
    state s1;
    state s2;
    transition tg1 first s1 if true then s2;
  }
}
