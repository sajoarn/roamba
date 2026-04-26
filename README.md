# ROAMBA - Robotic Observation and Autonomous Mobility Boundary Analyzer

## Overview

ROAMBA is an autonomous robot system designed for lane detection and navigation. The project integrates computer vision on a Raspberry Pi with Arduino-based motor control and sensor systems to create a self-driving robot that can follow lanes while avoiding obstacles.

## System Architecture

The system consists of two main components:

1. **Vision System (Python/Raspberry Pi)**: Handles camera input, lane detection, and WiFi connectivity
2. **Control System (Arduino)**: Manages motors, sensors, and executes navigation commands

### Communication
The Raspberry Pi and Arduino communicate via serial connection (USB). The vision system sends steering commands to the Arduino, which executes them while monitoring sensors for safety.

## Hardware Components

- **Arduino Board**: Main controller for motors and sensors
- **Raspberry Pi**: Runs computer vision algorithms
- **Camera**: Captures video feed for lane detection
- **Motors**: Drive the robot's movement
- **Ultrasonic Sensor**: Detects obstacles
- **Gyroscope**: Measures rotation for precise steering
- **Servo**: Used for surveying surroundings

## Software Components

### Arduino Side (`main/` directory)

#### Core Files:
- **`main.ino`**: Main Arduino program that orchestrates all robot functions
- **`MotorController.h/.cpp`**: Handles motor control for forward/backward movement and steering
- **`Ultrasonic.h/.cpp`**: Manages ultrasonic sensor for obstacle detection
- **`Gyro.h/.cpp`**: Interfaces with gyroscope for rotation measurements
- **`Rotation.h/.cpp`**: Implements precise rotational movements
- **`ServoController.h/.cpp`**: Controls servo motors for environmental scanning

#### How It Works:
The Arduino code runs in a continuous loop:
1. **Sensor Updates**: Regularly checks ultrasonic sensor for obstacles
2. **Command Reception**: Listens for serial commands from Raspberry Pi
3. **Decision Logic**: Prioritizes safety (obstacle avoidance) over navigation commands
4. **Execution**: Controls motors and servos based on current state

**Command Protocol:**
- `L:value` - Turn left by specified degrees
- `R:value` - Turn right by specified degrees
- `G:value` - Move forward (general command)
- `S:value` - Stop

### Vision System (`vision_sys/` directory)

#### Core Files:
- **`MainRobotLane.py`**: Main Python script that coordinates the vision system
- **`LaneDetectionModule.py`**: Contains lane detection algorithms using OpenCV
- **`WebcamModule.py`**: Handles camera input and video processing
- **`ColorPickerScript.py`**: Utility for color calibration
- **`requirements.txt`**: Python dependencies

#### How It Works:
1. **WiFi Connection**: Connects to robot's WiFi network for camera streaming
2. **Camera Initialization**: Sets up webcam or video stream
3. **Lane Detection Loop**:
   - Captures frames from camera
   - Processes images to detect lane curves
   - Calculates steering angles based on lane position
   - Sends commands to Arduino via serial

**Lane Detection Process:**
- Image preprocessing and filtering
- Edge detection to find lane markings
- Curve calculation (pixels from center line)
- Conversion to steering degrees
- Sensitivity and speed adjustments

## Setup and Installation

### Arduino Setup
1. Open `main/main.ino` in Arduino IDE
2. Install required libraries (ArduinoJson, etc.)
3. Upload to Arduino board
4. Connect sensors and motors according to pin definitions

### Raspberry Pi Setup
1. Install Python dependencies:
   ```bash
   cd vision_sys
   pip install -r requirements.txt
   ```
2. Ensure OpenCV is properly installed
3. Connect camera to Raspberry Pi
4. Run the main script:
   ```bash
   python MainRobotLane.py
   ```

### Hardware Connections
- Arduino ↔ Raspberry Pi: USB serial connection
- Camera → Raspberry Pi
- Motors, sensors → Arduino (see pin definitions in code)

## Usage

1. **Power on** both Arduino and Raspberry Pi
2. **Connect to WiFi** (robot broadcasts its own network)
3. **Run the vision system** on Raspberry Pi
4. **Monitor serial output** for debugging
5. Robot will automatically start lane following

### Debug Mode
Set `debug_mode = True` in `MainRobotLane.py` to use local video files instead of live camera feed.

## Dependencies

### Python
- OpenCV
- NumPy
- Serial
- Subprocess
- Platform
- Time

### Arduino
- ArduinoJson
- Standard Arduino libraries

## Safety Features

- **Obstacle Detection**: Currently uses ultrasonic sensor to stop robot when obstacles are detected. Camera-based obstacle detection is planned as a secondary goal to complement ultrasonic sensing.
- **Priority System**: Safety overrides navigation commands
- **Servo Survey**: Robot can scan surroundings when stopped
- **Speed Limiting**: Maximum turn values prevent excessive maneuvers

## Troubleshooting

- **Serial Connection Issues**: Check COM port in `MainRobotLane.py`
- **WiFi Connection**: Ensure robot's WiFi network is available
- **Camera Issues**: Verify camera is properly connected and configured
- **Lane Detection**: Adjust sensitivity values in vision code for different lighting conditions

### QT Font Errors
- The latest version of OpenCV for Python does not include fonts when installed via pip. -To manually copy over fonts:
1. Run your venv activate script
2. Find your venv path
3. Create a folder in your OpenCV site package to hold the fonts:
```sh
mkdir /home/$USER_NAME/$ROAMBA_REPO_PATH/.venv/lib/python3.13/site-packages/cv2/qt/fonts
```
4. Copy over the fonts to this new directory:
```sh
cp /usr/share/fonts/truetype/dejavu/*.ttf /home/$USER_NAME/$ROAMBA_REPO_PATH/.venv/lib/python3.13/site-packages/cv2/qt/fonts
```

## Future Enhancements

- Camera-based obstacle detection (secondary goal) to complement ultrasonic sensing
- Integration with additional sensors (GPS, LIDAR)
- Advanced computer vision features (traffic sign recognition)
- Machine learning-based navigation
- Remote monitoring interface
