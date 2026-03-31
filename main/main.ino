#include <stdio.h>
#include <string.h>
#include "Arduino.h"
#include "DeviceDriverSet_xxx0.h"

DeviceDriverSet_Motor AppMotor;
DeviceDriverSet_ULTRASONIC AppULTRASONIC;
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

unsigned long lastSonarTime = 0;
unsigned long lastPiTime = 0;

// ==========================================
// 2. DATA COLLECTION FUNCTIONS
// ==========================================

void updateUltrasonicData() {
    // Only check the sensor every 50 milliseconds
    if (millis() - lastSonarTime >= 50) {
        lastSonarTime = millis();
        
        robotData.frontDistance = AppULTRASONIC.DeviceDriverSet_ULTRASONIC_Get();
        
        if (robotData.frontDistance > 0 && robotData.frontDistance < CRITICAL_DISTANCE_CM) {
            robotData.obstacleDetected = true;
        } else {
            robotData.obstacleDetected = false;
        }
    }
}

void updateRaspberryPiData() {
// check on rasberry pi data
}

// ==========================================
// 3. VEHICLE DECISION LOGIC
// ==========================================

void Navigation() {
    // 1. Safety always comes first: Check the ultrasonic flag
    if (robotData.obstacleDetected) {
        // Stop immediately
        AppMotor.DeviceDriverSet_Motor_control(direction_void, 0, direction_void, 0, false);
        Serial.println("ALERT: Obstacle Detected! Halting.");
        
        // (Insert backup or turn around code here)
        return; // Exit the function immediately so we do not process Pi commands
    }
    
    // 2. If the path is clear, follow the Raspberry Pi instructions
    // (This code will run once we actually have the Pi sending data)
    /*
    if (robotData.stopSignDetected) {
        AppMotor.DeviceDriverSet_Motor_control(direction_void, 0, direction_void, 0, false);
    } else {
        // Drive forward using the Pi's steering angle
        AppMotor.DeviceDriverSet_Motor_control(direction_just, CRUISE_SPEED, direction_just, CRUISE_SPEED, true);
    }
    */
}

// ==========================================
// 4. MAIN EXECUTABLE
// ==========================================

void setup() {
    Serial.begin(115200);
    AppMotor.DeviceDriverSet_Motor_Init();
    AppULTRASONIC.DeviceDriverSet_ULTRASONIC_Init();
   // AppServo.DeviceDriverSet_Servo_Init(90); 
    
    // Set default safe values in the mailbox
    robotData.obstacleDetected = false;
    robotData.targetSteeringAngle = 0;
    robotData.stopSignDetected = false;
    
    Serial.println("System Boot: Ready.");
}

void loop() {
    // The main loop is now just a clean, easy to read checklist.
    // It gathers all data first, then makes a decision.
    
    updateUltrasonicData();
    updateRaspberryPiData();
    Navigation();
}