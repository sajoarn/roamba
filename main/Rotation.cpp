#include "Rotation.h"

void rotateLeftDegrees(float targetDeg, Gyro& gyro, MotorController& motors, Ultrasonic& sensor) {
    int speedCar = 100; // Local variable for this specific maneuver
    
    Serial.print("Rotating LEFT ");
    Serial.print(targetDeg);
    Serial.println(" degrees");

    gyro.resetYaw();
    motors.rotateLeftRaw(speedCar);

    while (gyro.yaw < targetDeg) {
        gyro.updateYaw();
        if (sensor.obstacleDetected()) {
            motors.stopMotors();
            return;
        }
    }

    motors.stopMotors();
    Serial.println("Left rotation complete.");
}

void rotateRightDegrees(float targetDeg, Gyro& gyro, MotorController& motors, Ultrasonic& sensor) {
    int speedCar = 100;
    
    Serial.print("Rotating RIGHT ");
    Serial.print(targetDeg);
    Serial.println(" degrees");

    gyro.resetYaw();
    motors.rotateRightRaw(speedCar);

    while (gyro.yaw > -targetDeg) {
        gyro.updateYaw();
        if (sensor.obstacleDetected()) {
            motors.stopMotors();
            return;
        }
    }

    motors.stopMotors();
    Serial.println("Right rotation complete.");
}