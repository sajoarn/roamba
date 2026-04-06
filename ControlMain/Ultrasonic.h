#ifndef ULTRASONIC_H
#define ULTRASONIC_H

#include <Arduino.h>

namespace Pins {
    const uint8_t TRIG = 13;
    const uint8_t ECHO = 12;
}

void initUltrasonic();
long readUltrasonicCm();
bool obstacleDetected();

#endif