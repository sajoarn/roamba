#include "Ultrasonic.h"

void initUltrasonic() {
    pinMode(Pins::TRIG, OUTPUT);
    pinMode(Pins::ECHO, INPUT);
}

long readUltrasonicCm() {
    digitalWrite(Pins::TRIG, LOW);
    delayMicroseconds(2);
    digitalWrite(Pins::TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(Pins::TRIG, LOW);

    unsigned long duration = pulseIn(Pins::ECHO, HIGH, 25000UL);
    if (duration == 0) return -1;

    long distanceCm = duration / 58;
    if (distanceCm > 400) distanceCm = 400;
    return distanceCm;
}

bool obstacleDetected() {
    long d = readUltrasonicCm();
    if (d != -1 && d <= 20) {
        Serial.print("Obstacle detected at ");
        Serial.print(d);
        return true;
    }
    return false;
}