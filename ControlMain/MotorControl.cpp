#include "MotorControl.h"
#include "Ultrasonic.h"

int speedCar = 100;

void initMotors() {
    pinMode(PWMA, OUTPUT);
    pinMode(PWMB, OUTPUT);
    pinMode(AIN, OUTPUT);
    pinMode(BIN, OUTPUT);
    pinMode(STBY, OUTPUT);
    digitalWrite(STBY, HIGH);
}

void stopMotors() {
    analogWrite(PWMA, 0);
    analogWrite(PWMB, 0);
}

void rotateLeftRaw(int speed) {
    int speedRotation = speed + 100;
    digitalWrite(AIN, HIGH);
    digitalWrite(BIN, HIGH);
    analogWrite(PWMA, speedRotation);
    analogWrite(PWMB, speed);
}

void rotateRightRaw(int speed) {
    int speedRotation = speed + 100;
    digitalWrite(AIN, HIGH);
    digitalWrite(BIN, HIGH);
    analogWrite(PWMA, speed);
    analogWrite(PWMB, speedRotation);
}

void forwardUntilBlocked(int speed, unsigned long durationMs) {
    unsigned long start = millis();

    while (millis() - start < durationMs) {
        if (obstacleDetected()) {
            stopMotors();
            Serial.println("Stopped FORWARD due to obstacle");
            return;
        }
        digitalWrite(AIN, HIGH);
        digitalWrite(BIN, HIGH);
        analogWrite(PWMA, speed);
        analogWrite(PWMB, speed);
    }
    stopMotors();
}

void reverseUntilBlocked(int speed, unsigned long durationMs) {
    unsigned long start = millis();

    while (millis() - start < durationMs) {
        if (obstacleDetected()) {
            stopMotors();
            Serial.println("Stopped REVERSE due to obstacle");
            return;
        }
        digitalWrite(AIN, LOW);
        digitalWrite(BIN, LOW);
        analogWrite(PWMA, speed);
        analogWrite(PWMB, speed);
    }
    stopMotors();
}