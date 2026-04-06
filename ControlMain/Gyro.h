#ifndef GYRO_H
#define GYRO_H

#include <Arduino.h>
#include <MPU6050.h>

extern MPU6050 mpu;
extern float yaw;

void initGyro();
void updateYaw();
void resetYaw();

#endif
