// Standard Libs
#include <stdio.h>
#include <string.h>

// External Libs
#include "Arduino.h"
#include "Ultrasonic.h"
#include "Gyro.h"
#include "Rotation.h"
#include "ServoController.h"

// Custom Sources
#include "MotorController.h"
#include "Utils.h"

/***********************************************
 *  Defines
 ***********************************************/
#define DEBUG_CMD_DURATION_MS 2000
#define MOVEMENT_DURATION_MS 100
#define SONAR_INTERVAL_MS 100
#define SERIAL_BAUD 115200
#define ROBOT_SPEED 100

// #define DEBUG_MODE // Comment out to disable Debug Mode

/***********************************************
 *  Typedefs
 ***********************************************/
struct VehicleData {
    // Ultrasonic Data
    bool obstacleDetected = false;
    uint8_t speed = 0;
    
    // Future Raspberry Pi OpenCV Data
    int targetSteeringAngle; 
    bool stopSignDetected;   
};

/***********************************************
 *  Singleton Instances
 ***********************************************/
MotorController motor;
Ultrasonic ultrasonic;
Gyro gyro;
ServoController servo;
VehicleData robotData; // Create our mailbox


// ==========================================
// DATA COLLECTION FUNCTIONS
// ==========================================

void updateUltrasonicData() {
    static unsigned long prevSonarTime = 0;
    // Poll the sensor on a set frequency
    if (millis() - prevSonarTime >= SONAR_INTERVAL_MS) {
        prevSonarTime = millis();
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
                    robotData.speed = ROBOT_SPEED;
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
// VEHICLE DECISION LOGIC
// ==========================================

void Navigation() {

    if (robotData.obstacleDetected) {
        // motor.moveBackward(robotData.speed, MOVEMENT_DURATION_MS);
        motor.stopMotors(); // Updated
        // servo.surveySurroundings(); // Updated
        return; // Exit immediately to prevent Pi commands from overriding safety
    }

    // PRIORITY 3: Navigation and Lane Tracking
    if (robotData.targetSteeringAngle < 0) {
        // Steer Left
        // rotateLeftDegrees(robotData.targetSteeringAngle, gyro,  motor, ultrasonic); // blocking
        motor.rotateLeftRaw(ROBOT_SPEED);
        robotData.targetSteeringAngle = 0; // Reset after steering
    } 
    else if (robotData.targetSteeringAngle > 0) {
        // Steer Right
        // rotateRightDegrees(robotData.targetSteeringAngle, gyro,  motor, ultrasonic); // blocking
        motor.rotateRightRaw(ROBOT_SPEED);
        robotData.targetSteeringAngle = 0; // Reset after steering
    } 
    else {
        motor.moveForward(robotData.speed, MOVEMENT_DURATION_MS); // Updated
    }
}

void simulateDebugCommands() {
    // Static so variables persist between function calls
    static unsigned long lastDebugTime = 0;
    static int debugSequence = 0;
    // Only change the command every few seconds
    if (millis() - lastDebugTime > DEBUG_CMD_DURATION_MS) {
        lastDebugTime = millis();
        
        // Cycle to the next step in the sequence
        debugSequence++;
        if (debugSequence > 3) {
            debugSequence = 0; // Loop back to the start
        }
        roambaPrintTime();
        Serial.print("Debug sequence ");
        Serial.println(debugSequence);

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
// MAIN EXECUTABLE
// ==========================================

void setup() {
    Serial.begin(SERIAL_BAUD);
    roambaPrintTime();
    Serial.println("Initializing...");
    // Initialize all hardware securely using the new names
    motor.initMotors();
    ultrasonic.initUltrasonic();
    gyro.initGyro();
    servo.init();
    // Set default safe values
    robotData.obstacleDetected = false;
    robotData.targetSteeringAngle = 0;
    robotData.stopSignDetected = false;
    
    roambaPrintTime();
    Serial.println("R.O.A.M. B.A. System Boot: Online and ready.");
}

void loop() {
    // 1. Get Sensor Data
    updateUltrasonicData(); 

    // 2. Decide where our steering instructions are coming from
#ifdef DEBUG_MODE
    simulateDebugCommands(); 
#else
    updateRaspberryPiData(); 
#endif

    // 3. Act on steering commands
    Navigation(); 
}