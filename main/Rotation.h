#ifndef ROTATION_H
#define ROTATION_H

#include <Arduino.h>
#include "Gyro.h"
#include "MotorControl.h"
#include "Ultrasonic.h"

// Standard procedural functions that accept the hardware objects they need to manipulate
void rotateLeftDegrees(float targetDeg, Gyro& gyro, MotorController& motors, Ultrasonic& sensor);
void rotateRightDegrees(float targetDeg, Gyro& gyro, MotorController& motors, Ultrasonic& sensor);

#endif