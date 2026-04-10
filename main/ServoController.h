#ifndef SERVO_CONTROLLER_H
#define SERVO_CONTROLLER_H

#include <Arduino.h>
#include <Servo.h>

class ServoController {
  private:
    Servo servo;
    
    uint8_t pinZ = 10; 

  public:
    ServoController();

    void init(int startAngle = 90);
    void controlAngle(int angle);
    void surveySurroundings();
};

#endif