#include <stdio.h>
#include <string.h>

#include "Arduino.h"

#include "MotorController.h"
#include "Ultrasonic.h"
#include "Gyro.h"
#include "Rotation.h"
#include "ServoController.h"

MotorController motor;
Ultrasonic ultrasonic;
Gyro gyro;
ServoController servo;

struct VehicleData {
    // Ultrasonic Data
    uint16_t frontDistance;
    bool obstacleDetected;

    uint8_t speed = 0;
    
    // Future Raspberry Pi OpenCV Data
    int targetSteeringAngle; 
    bool stopSignDetected;   
};

VehicleData robotData; // Create our mailbox

// System configuration
const uint16_t CRITICAL_DISTANCE_CM = 25; 
int durationMs = 1000; // Default duration for forward/backward commands

unsigned long lastSonarTime = 0;
unsigned long lastPiTime = 0;
const uint8_t SONAR_INTERVAL = 100;

bool debugMode = false; // TESTING WITHOUT PI
// ==========================================
// 2. DATA COLLECTION FUNCTIONS
// ==========================================

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
                case 'G': 
                    robotData.targetSteeringAngle = 0; 
                    robotData.speed = 100;
                    Serial.print("DONE");
                    break; // General steering command
                case 'S': 
                    robotData.targetSteeringAngle = 0; 
                    robotData.speed = 0;
                    break;
            } //"L:30" means turn left 30 degrees, "R:15" means turn right 15 degrees, Wont move unless angle is larger then absolute value of 10 degrees
        }
    }
}

// ==========================================
// 3. VEHICLE DECISION LOGIC
// ==========================================

void Navigation() {

    if (robotData.obstacleDetected) {
        motor.moveBackward(robotData.speed,durationMs);
        motor.stopMotors(); // Updated
        servo.surveySurroundings(); // Updated
        return; // Exit immediately to prevent Pi commands from overriding safety
    }

    // PRIORITY 3: Navigation and Lane Tracking
    if (robotData.targetSteeringAngle < 0) {
        // Steer Left
        rotateLeftDegrees(robotData.targetSteeringAngle, gyro,  motor, ultrasonic); // blocking
        robotData.targetSteeringAngle = 0; // Reset after steering
       // motor.rotateLeftRaw(100); // Updated
    } 
    else if (robotData.targetSteeringAngle > 0) {
        // Steer Right
        rotateRightDegrees(robotData.targetSteeringAngle, gyro,  motor, ultrasonic); // blocking
        robotData.targetSteeringAngle = 0; // Reset after steering
       // motor.rotateRightRaw(100); // Updated
    } 
    else {
        motor.moveForward(robotData.speed,durationMs); // Updated
    }
}
unsigned long lastDebugTime = 0;
int debugSequence = 0;
void simulateDebugCommands() {
    // Only change the command every 2000 milliseconds (2 seconds)
    if (millis() - lastDebugTime > 2000) {
        lastDebugTime = millis();
        
        // Cycle to the next step in the sequence
        debugSequence++;
        if (debugSequence > 3) {
            debugSequence = 0; // Loop back to the start
        }
        switch(debugSequence) {
            case 0:
                robotData.targetSteeringAngle = 0;
                break;
            case 1:
                robotData.targetSteeringAngle = -45;
                break;
            case 2:
                robotData.targetSteeringAngle = 0;
                break;
            case 3:
                robotData.targetSteeringAngle = 45;
                break;
        }
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
    servo.init();
    // Set default safe values
    robotData.obstacleDetected = false;
    robotData.targetSteeringAngle = 0;
    robotData.stopSignDetected = false;
    
    Serial.println("R.O.A.M. B.A. System Boot: Online and ready.");
}

void loop() {
  
    updateUltrasonicData(); 

    // 2. Decide where our steering instructions are coming from
    if (debugMode) {
        // Run our ghost Pi simulator
        simulateDebugCommands(); 
    } else {
        // Listen to the real Pi over the USB cable
        updateRaspberryPiData(); 
    }

    Navigation(); 
}