//#include <hardwareSerial.h>
#include <stdio.h>
#include <string.h>
#include "DeviceDriverSet_xxx0.h"

#include "ArduinoJson-v6.11.1.h" //ArduinoJson
#include "MPU6050_getdata.h"

/*Hardware device object list*/
MPU6050_getdata AppMPU6050getdata;
DeviceDriverSet_RBGLED AppRBG_LED;
DeviceDriverSet_Key AppKey;
DeviceDriverSet_ITR20001 AppITR20001;
DeviceDriverSet_Voltage AppVoltage;

DeviceDriverSet_Motor AppMotor;
DeviceDriverSet_ULTRASONIC AppULTRASONIC;
DeviceDriverSet_Servo AppServo;
DeviceDriverSet_IRrecv AppIRrecv;
// Define pin constants
const int LED_PIN = 13;
const int BUTTON_PIN = 2;

void setup() {
    // Initialize serial communication
    Serial.begin(9600);
    
    // Initialize pins, sensors, and other hardware
    pinMode(LED_BUILTIN, OUTPUT);
    
    Serial.println("Setup complete");
}

void loop() {
    // Main program logic

}