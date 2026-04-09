# R.O.A.M-B.A
The Robotic Observation and Autonomous Mobility Boundary Analyzer (R.O.A.M-B.A) is a group project for Purdue University ECE 568 Embedded Systems. The system uses a off-the-shelf robot kit that comes complete with an Arduino Uno R3 and all sensors and servos needed to drive the robot[1]. Additionally, we use a Raspberry Pi 4 hooked to the kit's webcam for visual recognition of path and obstacles.

[1] https://us.elegoo.com/products/elegoo-smart-robot-car-kit-v-4-0
[2] https://www.raspberrypi.com/products/raspberry-pi-4-model-b/

# Getting Started
## Arduino
1. Install [Arduino IDE v2.3.8](https://github.com/arduino/arduino-ide/releases/tag/2.3.8)
2. Update IDE to include Arduino AVR Boards (core) which includes the build tools needed for the Uno R3
3. Using the IDE library manager, add libraries:
    - IRremote
    - FastLED
    - MPU6050 by Electronic Cats
4. Sketch -> Verify/Compile
5. Upload (check button)

## Raspberry Pi
1. Setup python virtual environment:
```py
python -m venv .venv
```
2. Run venv:
```py
source .venv/bin/activate
```
3. Clone repo onto raspberry pi
4. From cloned repo, install necessary files
```py
pip install -r ./roamba/vision_sys/requirements.txt
```

## Debug Web Server
This puts out commands that can be read by ControlMain.ino
1. pip install flask pyserial