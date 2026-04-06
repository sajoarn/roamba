#ifndef MOTOR_CONTROL_H
#define MOTOR_CONTROL_H

#include <Arduino.h>

// Motor pins
#define PWMA 5
#define PWMB 6
#define AIN 7
#define BIN 8
#define STBY 3

extern int speedCar;

// Motor API
void initMotors();
void stopMotors();
void rotateLeftRaw(int speed);
void rotateRightRaw(int speed);
void forwardUntilBlocked(int speed, unsigned long durationMs);
void reverseUntilBlocked(int speed, unsigned long durationMs);

#endif
