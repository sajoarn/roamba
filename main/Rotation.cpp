#include "Rotation.h"
#include "Utils.h"

void rotateLeftDegrees(float targetDeg, Gyro& gyro, MotorController& motors, Ultrasonic& sensor) {
    int speedCar = 100; // Local variable for this specific maneuver
    
    roambaPrintTime();
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
    roambaPrintTime();
    Serial.println("Left rotation complete.");
}

void rotateRightDegrees(float targetDeg, Gyro& gyro, MotorController& motors, Ultrasonic& sensor) {
    int speedCar = 100;

    roambaPrintTime();
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
    roambaPrintTime();
    Serial.println("Right rotation complete.");
}