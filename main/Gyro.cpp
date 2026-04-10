#include "Gyro.h"

MPU6050 mpu;
float yaw = 0;
unsigned long lastTime = 0;

void initGyro() {
    Wire.begin();
    mpu.initialize();
    delay(1000);
    lastTime = micros();
}

void resetYaw() {
    yaw = 0;
    lastTime = micros();
}

void updateYaw() {
    unsigned long now = micros();
    float dt = (now - lastTime) / 1000000.0;
    lastTime = now;

    int16_t gx, gy, gz;
    mpu.getRotation(&gx, &gy, &gz);

    float gyroZ = gz / 131.0;
    yaw += gyroZ * dt;
}