#include "Rotation.h"
#include "Utils.h"

#define ROTATION_SPEED_LEFT 100
#define ROTATION_SPEED_RIGHT 100

/**
 * @brief Rotate the robot left by a specific number of degrees.
 *
 * Uses gyro feedback to determine when the left rotation has reached
 * the requested yaw offset. The function exits early if the ultrasonic
 * sensor detects an obstacle during rotation.
 *
 * @param targetDeg Desired left rotation in degrees.
 * @param gyro Reference to the gyroscope object for yaw tracking.
 * @param motors Reference to the motor controller for issuing drive commands.
 * @param sensor Reference to the ultrasonic sensor for obstacle detection.
 */
void rotateLeftDegrees(float targetDeg, Gyro& gyro, MotorController& motors, Ultrasonic& sensor) {
    roambaPrintTime();
    Serial.print("Rotating LEFT ");
    Serial.print(targetDeg);
    Serial.println(" degrees");

    motors.rotateLeftRaw(ROTATION_SPEED_LEFT, ROTATION_SPEED_LEFT);
    gyro.resetYaw();

    while (gyro.yaw < targetDeg) {
        gyro.updateYaw();
        if (sensor.obstacleDetected()) {
            motors.stopMotors();
            Serial.print("DONE");
            return;
        }
    }

    motors.stopMotors();
    roambaPrintTime();
    Serial.println("Left rotation complete.");
}

/**
 * @brief Rotate the robot right by a specific number of degrees.
 *
 * Right turns produce negative yaw readings from the gyroscope. The loop
 * continues until the absolute target is reached or an obstacle is detected.
 *
 * @param targetDeg Desired right rotation in degrees.
 * @param gyro Reference to the gyroscope object for yaw tracking.
 * @param motors Reference to the motor controller for issuing drive commands.
 * @param sensor Reference to the ultrasonic sensor for obstacle detection.
 */
void rotateRightDegrees(float targetDeg, Gyro& gyro, MotorController& motors, Ultrasonic& sensor) {
    roambaPrintTime();
    Serial.print("Rotating RIGHT ");
    Serial.print(targetDeg);
    Serial.println(" degrees");

    gyro.resetYaw();
    motors.rotateRightRaw(ROTATION_SPEED_RIGHT, ROTATION_SPEED_RIGHT);

    while (gyro.yaw > -targetDeg) {
        gyro.updateYaw();
        if (sensor.obstacleDetected()) {
            motors.stopMotors();
            Serial.print("DONE");
            return;
        }
    }

    motors.stopMotors();
    roambaPrintTime();
    Serial.println("Right rotation complete.");
}