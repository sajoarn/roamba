#ifndef MOTOR_CONTROL_H
#define MOTOR_CONTROL_H

#include <Arduino.h>

class MotorController {
  private:
    // In-class initialization: Setting the "factory defaults"
    uint8_t PWMA = 5;
    uint8_t PWMB = 6;
    uint8_t AIN = 7;
    uint8_t BIN = 8;
    uint8_t STBY = 3;
    int speedCar = 100;

  public:
    // We can tell the compiler to just use a standard, empty constructor
    MotorController(); 

    void initMotors();
    void stopMotors();
    void rotateLeftRaw(int speed);
    void rotateRightRaw(int speed);
    void moveForward(int speed, unsigned long durationMs);
    void moveBackward(int speed, unsigned long durationMs);
};

#endif