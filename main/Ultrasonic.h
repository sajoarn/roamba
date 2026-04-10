#ifndef ULTRASONIC_H
#define ULTRASONIC_H

#include <Arduino.h>

class Ultrasonic {
  private:
    // In-class initialization for your default pins
    uint8_t TRIG = 13;
    uint8_t ECHO = 12;

  public:
    // Empty constructor
    Ultrasonic();

    // Keeping your exact original function names
    void initUltrasonic();
    long readUltrasonicCm();
    bool obstacleDetected();
};

#endif