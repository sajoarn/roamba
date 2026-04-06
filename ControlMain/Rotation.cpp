#include "Rotation.h"
#include "Gyro.h"
#include "MotorControl.h"
#include "Ultrasonic.h"

void rotateLeftDegrees(float targetDeg) {
    Serial.print("Rotating LEFT ");
    Serial.print(targetDeg);
    Serial.println(" degrees");

    resetYaw();
    rotateLeftRaw(speedCar);

    while (yaw < targetDeg) {
        updateYaw();
        if (obstacleDetected()) {
            stopMotors();
            return;
        }
    }

    stopMotors();
    Serial.println("Left rotation complete.");
}

void rotateRightDegrees(float targetDeg) {
    Serial.print("Rotating RIGHT ");
    Serial.print(targetDeg);
    Serial.println(" degrees");

    resetYaw();
    rotateRightRaw(speedCar);

    while (yaw > -targetDeg) {
        updateYaw();
        if (obstacleDetected()) {
            stopMotors();
            return;
        }
    }

    stopMotors();
    Serial.println("Right rotation complete.");
}