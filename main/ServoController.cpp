#include "ServoController.h"

// Empty constructor because the pin is set in the header
ServoController::ServoController() {
}

void ServoController::init(int startAngle) {
    // Attach the servo with Elegoo's specific min/max pulse widths to protect the gears
    // 500: 0 degrees | 2400: 180 degrees
    servo.attach(pinZ, 500, 2400);
    
    servo.write(startAngle); 
}

void ServoController::controlAngle(int angle) {
    // Safety check: Constrain the angle between 0 and 180 to prevent mechanical binding
    if (angle < 0) {
        angle = 0;
    } else if (angle > 180) {
        angle = 180;
    }

    // Command the servo to move
    servo.write(angle);
}

void ServoController::surveySurroundings() {

    for (int angle = 90; angle >= 45; angle -= 5) {
        controlAngle(angle);
        delay(100); 
    }

    for (int angle = 45; angle <= 135; angle += 5) {
        controlAngle(angle);
        delay(100); 
    }

    for (int angle = 135; angle >= 90; angle -= 5) {
        controlAngle(angle);
        delay(100);
    }

}