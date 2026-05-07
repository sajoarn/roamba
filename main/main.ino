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
#define SONAR_INTERVAL_MS 100
#define SERIAL_BAUD 115200
#define ROBOT_SPEED 50
#define SERIAL_TIMEOUT_MS 10

/***********************************************
 *  Typedefs
 ***********************************************/
enum Directions_t {
    LEFT,
    SHARP_LEFT,
    RIGHT,
    SHARP_RIGHT,
    FORWARD,
    STOP,
    NO_CMD
};

/***********************************************
 *  Singleton Instances
 ***********************************************/
MotorController motor;
Ultrasonic ultrasonic;
Gyro gyro;
ServoController servo;
Directions_t steeringCmd; // Create our mailbox

// ==========================================
// DATA COLLECTION FUNCTIONS
// ==========================================

void updateUltrasonicData() {
    // Poll the sensor on a set frequency
    if (ultrasonic.obstacleDetected()) {
        steeringCmd = STOP;
    }
}

void updateRaspberryPiData() {
    String rxData;
    char cmd;
    while(Serial.available() > 0) {
        // Flush out the serial RX buffer, and use last command
        // (This is fragile! What if the buffer doesn't contain a newline?)
        rxData = Serial.readStringUntil('\n');
        cmd = rxData.charAt(0);
        switch(cmd) {
            case 'L': 
                steeringCmd = LEFT;
                break;
            case 'A':
                steeringCmd = SHARP_LEFT;
                break;
            case 'R':
                steeringCmd = RIGHT;
                break;
            case 'C':
                steeringCmd = SHARP_RIGHT;
                break;
            case 'F':
                steeringCmd = FORWARD;
                break;
            case 'S':
            // If command is invalid, stop movement
                steeringCmd = STOP;
                break;
            default:
                steeringCmd = NO_CMD;
                break;
        }
    }
}

// ==========================================
// VEHICLE DECISION LOGIC
// ==========================================

void Navigation() {
    switch (steeringCmd) {
        case LEFT:
            motor.rotateLeftRaw(ROBOT_SPEED, ROBOT_SPEED);
            roambaPrintTime();
            Serial.println("Motors Left...");
            break;
        case SHARP_LEFT:
            motor.rotateLeftRaw(ROBOT_SPEED, ROBOT_SPEED * 2);
            roambaPrintTime();
            Serial.println("Motors Sharp Left...");
            break;
        case RIGHT:
            motor.rotateRightRaw(ROBOT_SPEED, ROBOT_SPEED);
            roambaPrintTime();
            Serial.println("Motors Right...");
            break;
        case SHARP_RIGHT:
            motor.rotateRightRaw(ROBOT_SPEED, ROBOT_SPEED * 2);
            roambaPrintTime();
            Serial.println("Motors Sharp Right...");
            break;
        case FORWARD:
            motor.moveForwardRaw(ROBOT_SPEED); // Updated
            roambaPrintTime();
            Serial.println("Motors forward...");
            break;
        case STOP:
            motor.stopMotors();
            break;
        case NO_CMD:
        default:
            // Do nothing if no command
            break;
    }
    steeringCmd = NO_CMD;
}

// ==========================================
// MAIN EXECUTABLE
// ==========================================

void setup() {
    Serial.begin(SERIAL_BAUD);
    Serial.setTimeout(SERIAL_TIMEOUT_MS);
    roambaPrintTime();
    Serial.println("Initializing...");
    // Initialize all hardware securely using the new names
    motor.initMotors();
    ultrasonic.initUltrasonic();
    gyro.initGyro();
    servo.init();
    steeringCmd = NO_CMD;
    
    roambaPrintTime();
    Serial.println("R.O.A.M. B.A. System Boot: Online and ready.");
}

void loop() {
    // 1. Get any commands from serial
    updateRaspberryPiData(); 

    // 2. Get Sensor Data
    // (This will override any serial command)
    updateUltrasonicData(); 

    // 3. Act on steering commands
    Navigation(); 
    Serial.flush(); // Empty out any outgoing serial prints
}