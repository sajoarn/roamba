#include <stdio.h>
#include <string.h>

#include "Arduino.h"
#include "DeviceDriverSet_xxx0.h"

#include "MotorController.h"
#include "Ultrasonic.h"
#include "Gyro.h"
#include "Rotation.h"


MotorController motor;
Ultrasonic ultrasonic;
Gyro gyro;
DeviceDriverSet_Servo AppServo;

// ==========================================
// 1. THE CENTRAL MAILBOX (Global Data)
// ==========================================
// This structure holds ALL the data your robot needs to make a decision.
// To add new OpenCV data later, you just add a new variable right here.

struct VehicleData {
    // Ultrasonic Data
    uint16_t frontDistance;
    bool obstacleDetected;
    
    // Future Raspberry Pi OpenCV Data
    int targetSteeringAngle; 
    bool stopSignDetected;   
};

VehicleData robotData; // Create our mailbox

// System configuration
const uint16_t CRITICAL_DISTANCE_CM = 20; 
const uint8_t CRUISE_SPEED = 150;
int durationMs = 1000; // Default duration for forward/backward commands

unsigned long lastSonarTime = 0;
unsigned long lastPiTime = 0;

// ==========================================
// 2. DATA COLLECTION FUNCTIONS
// ==========================================

void serialEvent() {
    while (Serial.available()) {
        char c = (char)Serial.read();
        if (c == '\n') {
            stringComplete = true;
            return;
        }
        inputString += c;
    }
}

void processCommand(String cmd) {
    cmd.trim();
    if (cmd.length() == 0) return;

    Serial.print("CMD: ");
    Serial.println(cmd);

    if (cmd.indexOf(':') != -1) {
        char action = cmd.charAt(0);
        float value = cmd.substring(2).toFloat();

        switch (action) {
            case 'L': rotateLeftDegrees(value); break;
            case 'R': rotateRightDegrees(value); break;
            case 'F': forwardUntilBlocked(speedCar, (unsigned long)value); break;
            case 'B': reverseUntilBlocked(speedCar, (unsigned long)value); break;
        }
    } else {
        if (cmd == "S") stopMotors();
    }
}

void updateUltrasonicData() {
    // Only check the sensor every 50 milliseconds
    if (millis() - lastSonarTime >= SONAR_INTERVAL) {
        lastSonarTime = millis();
        // Updated to use the new 'ultrasonic' name
        robotData.obstacleDetected = ultrasonic.obstacleDetected();
    }
}

void updateRaspberryPiData() {
if (Serial.available() > 0) {
        String incomingData = Serial.readStringUntil('\n');
        incomingData.trim();
        if (incomingData.length() == 0) return;
        if (incomingData.indexOf(':') != -1) {
            char action = incomingData.charAt(0);
            float value = incomingData.substring(2).toFloat();

            switch (action) {
                case 'L': robotData.targetSteeringAngle = -value; break; // Left is negative
                case 'R': robotData.targetSteeringAngle = value; break;  // Right is positive
                case 'S': robotData.stopSignDetected = (value > 0); break;
            }
        }
    }
}

// ==========================================
// 3. VEHICLE DECISION LOGIC
// ==========================================

void Navigation() {

    if (robotData.obstacleDetected) {
        motor.moveBackward(CRUISE_SPEED,durationMs);
        motor.stopMotors(); // Updated
        Serial.println("ALERT: Physical obstacle boundary breached.");
        return; // Exit immediately to prevent Pi commands from overriding safety
    }

    // PRIORITY 3: Navigation and Lane Tracking
    if (robotData.targetSteeringAngle < -10) {
        // Steer Left
        rotateRightDegrees(robotData.targetSteeringAngle, gyro,  motor, ultrasonic)
        robotData.targetSteeringAngle = 0; // Reset after steering
       // motor.rotateLeftRaw(100); // Updated
    } 
    else if (robotData.targetSteeringAngle > 10) {
        // Steer Right
        rotateLeftDegrees(robotData.targetSteeringAngle, gyro,  motor, ultrasonic)
        robotData.targetSteeringAngle = 0; // Reset after steering
       // motor.rotateRightRaw(100); // Updated
    } 
    else {
        motor.moveForward(CRUISE_SPEED,durationMs); // Updated
    }
}

// ==========================================
// 4. MAIN EXECUTABLE
// ==========================================

void setup() {
    Serial.begin(115200);
    // Initialize all hardware securely using the new names
    motor.initMotors();
    ultrasonic.initUltrasonic();
    gyro.initGyro();
    
    // Set default safe values
    robotData.obstacleDetected = false;
    robotData.targetSteeringAngle = 0;
    robotData.stopSignDetected = false;
    
    Serial.println("R.O.A.M. B.A. System Boot: Online and ready.");
}

void loop() {
    // The main loop is now just a clean, easy to read checklist.
    // It gathers all data first, then makes a decision.
    updateUltrasonicData();
    //updateRaspberryPiData();
    Navigation();
}