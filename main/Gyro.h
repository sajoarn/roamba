#ifndef GYRO_H
#define GYRO_H

#include <Arduino.h>
//#include <Wire.h> 
#include "MPU6050.h"

class Gyro {
  private:
    // The MPU object and timing variable are hidden inside the class
    MPU6050 mpu;
    unsigned long lastTime = 0;

  public:
    // Yaw is public so your main file can still read it easily
    float yaw = 0;

    // Empty constructor
    Gyro();

    // Keeping your exact original function names
    void initGyro();
    void updateYaw();
    void resetYaw();
};

#endif