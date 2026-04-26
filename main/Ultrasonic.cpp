#include "Ultrasonic.h"
#include "Utils.h"

// Empty constructor because pins are set in the header
Ultrasonic::Ultrasonic() {
}

void Ultrasonic::initUltrasonic() {
    pinMode(TRIG, OUTPUT);
    pinMode(ECHO, INPUT);
}

long Ultrasonic::readUltrasonicCm() {
    digitalWrite(TRIG, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG, LOW);

    unsigned long duration = pulseIn(ECHO, HIGH, 25000UL);
    if (duration == 0) return -1;

    long distanceCm = duration / 58;
    if (distanceCm > 400) distanceCm = 400;
    return distanceCm;
}

bool Ultrasonic::obstacleDetected() {
    long d = readUltrasonicCm();
    if (d != -1 && d <= 20) {
        roambaPrintTime();
        Serial.print("Obstacle detected at ");
        Serial.print(d);
        Serial.print("\r\n");
        return true;
    }
    return false;
}