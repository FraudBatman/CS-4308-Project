// SCL v 1.0 File: arduino_ex1.c, Sat Apr 21 14:21:11 2018

/*
  ReadAnalogVoltage
  Reads an analog input from pin 0, converts it to voltage, and prints the result to the serial monitor.

  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This Sysplm program is derived from an example code, which is in the public domain. Sysplm version J. Garrido Sept. 2017
*/
#include "sysplm.h"
#define SERIAL_SPEED 9600
#define TTL_VOLTAGE 5
// forward declarations
// the setup routine runs once when you press reset:
void  setup(  );
// global declarations
const byte  A0 = 0;
// uint8_t pins_arduino.h
/**
description
  the setup routine runs once when you press reset:
  */
void  setup(  ) {
// initialize serial communication at 9600 bits per second:
    Serial.begin(SERIAL_SPEED);
}  // end function setup
/**
  description
      the loop routine runs over and over again forever:
      */
//
void  loop(  ) {
// read the input on analog pin 0:
    int  sensorValue;
    float  voltage;
    // read from pin A0
// Convert the analog reading (which goes from 0 - 1023)
    sensorValue = analogRead(A0);
// to a voltage (0 - 5V):
    voltage = (sensorValue) * (( (TTL_VOLTAGE)/(1023.0)) );
// print out the value you read:
    Serial.println(voltage);
    return 0;
}  // end function loop
