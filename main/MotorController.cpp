#include "MotorControl.h"
#include "Ultrasonic.h"

MotorController::MotorController() {
    // Nothing to do here.
}

void MotorController::initMotors() {
    // This will automatically use PWMA = 5, PWMB = 6, etc.
    pinMode(PWMA, OUTPUT);
    pinMode(PWMB, OUTPUT);
    pinMode(AIN, OUTPUT);
    pinMode(BIN, OUTPUT);
    pinMode(STBY, OUTPUT);
    digitalWrite(STBY, HIGH);
}

void MotorController::stopMotors() {
    analogWrite(PWMA, 0);
    analogWrite(PWMB, 0);
}

void MotorController::rotateLeftRaw(int speed) {
    int speedRotation = speed + 100;
    digitalWrite(AIN, HIGH);
    digitalWrite(BIN, HIGH);
    analogWrite(PWMA, speedRotation);
    analogWrite(PWMB, speed);
}

void MotorController::rotateRightRaw(int speed) {
    int speedRotation = speed + 100;
    digitalWrite(AIN, HIGH);
    digitalWrite(BIN, HIGH);
    analogWrite(PWMA, speed);
    analogWrite(PWMB, speedRotation);
}

void MotorController::moveForward(int speed, unsigned long durationMs) {
    unsigned long start = millis();

    while (millis() - start < durationMs) {
        digitalWrite(AIN, HIGH);
        digitalWrite(BIN, HIGH);
        analogWrite(PWMA, speed);
        analogWrite(PWMB, speed);
    }
    stopMotors();
}

void MotorController::moveBackward(int speed, unsigned long durationMs) {
    unsigned long start = millis();

    while (millis() - start < durationMs) {
        digitalWrite(AIN, LOW);
        digitalWrite(BIN, LOW);
        analogWrite(PWMA, speed);
        analogWrite(PWMB, speed);
    }
    stopMotors();
}