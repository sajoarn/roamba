#include "MotorController.h"
#include "Ultrasonic.h"

MotorController::MotorController() {
    // Nothing to do here.
}

void MotorController::initMotors() {
    pinMode(PWMA, OUTPUT);
    pinMode(PWMB, OUTPUT);
    pinMode(A_IN, OUTPUT);
    pinMode(B_IN, OUTPUT);
    pinMode(STBY, OUTPUT);
    digitalWrite(STBY, HIGH);
}

void MotorController::stopMotors() {
    analogWrite(PWMA, 0);
    analogWrite(PWMB, 0);
}

void MotorController::rotateLeftRaw(int speed, int rate) {
    int speedRotation = speed + rate;
    digitalWrite(A_IN, HIGH);
    digitalWrite(B_IN, HIGH);
    analogWrite(PWMA, speedRotation);
    analogWrite(PWMB, speed);
}

void MotorController::rotateRightRaw(int speed, int rate) {
    int speedRotation = speed + rate;
    digitalWrite(A_IN, HIGH);
    digitalWrite(B_IN, HIGH);
    analogWrite(PWMA, speed);
    analogWrite(PWMB, speedRotation);
}

void MotorController::moveForwardRaw(int speed) {
    digitalWrite(A_IN, HIGH);
    digitalWrite(B_IN, HIGH);
    analogWrite(PWMA, speed);
    analogWrite(PWMB, speed);
}

void MotorController::moveForward(int speed, unsigned long durationMs) {
    unsigned long start = millis();

    while (millis() - start < durationMs) {
        digitalWrite(A_IN, HIGH);
        digitalWrite(B_IN, HIGH);
        analogWrite(PWMA, speed);
        analogWrite(PWMB, speed);
    }
    stopMotors();
}

void MotorController::moveBackward(int speed, unsigned long durationMs) {
    unsigned long start = millis();

    while (millis() - start < durationMs) {
        digitalWrite(A_IN, LOW);
        digitalWrite(B_IN, LOW);
        analogWrite(PWMA, speed);
        analogWrite(PWMB, speed);
    }
    stopMotors();
}