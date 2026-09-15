package VehicleExample {
  part def Wheel;
  part def Vehicle {
    part wheels[1..4] : Wheel;
    attribute mass : Kilogram;
    attribute paint : VehicleColor;
  }
  attribute def Kilogram;
  enum def VehicleColor {
    red;
    green;
    blue;
  }
  part def Car :> Vehicle;
  requirement CarIsVehicle {
    doc /* A car shall be a specialization of vehicle. */
    doc /* derived from R-1 */
    /* v1 id: R-1 */
  }
  satisfy CarSatisfiesR1 : CarIsVehicle by Car;
}
