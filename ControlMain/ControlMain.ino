#include "MotorControl.h"
#include "Ultrasonic.h"
#include "Gyro.h"
#include "Rotation.h"

String inputString = "";
bool stringComplete = false;

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

void setup() {
    Serial.begin(115200);

    initMotors();
    initUltrasonic();
    initGyro();
}

void loop() {
    if (stringComplete) {
        processCommand(inputString);
        inputString = "";
        stringComplete = false;
    }

    if (obstacleDetected()) {
        stopMotors();
    }
}