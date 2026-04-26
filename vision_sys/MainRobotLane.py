"""
@file MainRobotLane.py
@brief Main control script for ELEGOO robot with lane detection.
@details Handles WiFi connection, camera streaming, and lane detection
         to autonomously navigate the robot. Commands are sent to the 
         Arduino microcontroller via serial communication.
"""

from LaneDetectionModule import getLaneCurve
import WebcamModule
import serial
import subprocess
import platform
import time

# ============================================================================
# Global Configuration Variables
# ============================================================================

## WiFi SSID for robot connection
ROBOT_WIFI_NAME = "ELEGOO-B89958BA2010"

## Debug mode flag - Set to True to use local video file instead of camera stream
debug_mode = False

## Arduino serial port configuration
ARDUINO_PORT = '/dev/ttyUSB0'
ARDUINO_BAUDRATE = 115200

## Lane detection sensitivity multiplier
SENSITIVITY = 0.1

## Maximum speed value for motor control
MAX_SPEED = 10

## Scale factor to convert pixels to degrees (100 pixels = 13.75 degrees)
CURVE_SCALE_FACTOR = 0.1375

## Network initialization delay (seconds)
NETWORK_INIT_DELAY = 5

## Arduino connection initialization delay (seconds)
ARDUINO_INIT_DELAY = 2

## Curve threshold for determining turn direction (degrees)
CURVE_THRESHOLD = 0.5

# ============================================================================
# Function Definitions
# ============================================================================

def connect_to_wifi(ssid, password=None):
    """
    @brief Connect to WiFi network based on the operating system.
    @details Handles WiFi connection for Windows (using netsh) and 
             Linux/Raspberry Pi (using nmcli). Waits for network IP 
             assignment before returning.
    
    @param ssid (str) - WiFi network SSID to connect to
    @param password (str, optional) - WiFi password (required for Linux)
    
    @return bool - True if connection successful, False otherwise
    """
    current_os = platform.system()
    print(f"Detected OS: {current_os}. Attempting to connect to {ssid}...")
    connection_successful = False
    if current_os == "Windows":
        # WINDOWS CONNECTION
        try:
            # The command: netsh wlan connect name="SSID"
            cmd = f'netsh wlan connect name="{ssid}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if "completed successfully" in result.stdout:
                print(f"Windows: Command sent to connect to {ssid}.")
                connection_successful = True
            else:
                print(f"Windows: Warning - {result.stdout.strip()}")
                
        except Exception as e:
            print(f"Windows Error: {e}")

    elif current_os == "Linux":
        # LINUX / RASPBERRY PI CONNECTION
        # Linux is much better at this. We use the 'nmcli' (NetworkManager) command.
        try:
            cmd = ["nmcli", "device", "wifi", "connect", ssid]
            if password:
                cmd.extend(["password", password])
                
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Linux: Successfully connected to {ssid}.")
                connection_successful = True
            else:
                print(f"Linux Error: {result.stderr.strip()}")
                
        except Exception as e:
            print(f"Linux Error: {e}")
            
    else:
        print(f"Unsupported Operating System: {current_os}")

    print("Waiting 5 seconds for network IP assignment...")
    time.sleep(NETWORK_INIT_DELAY)
    print("Ready to connect to camera stream!")

    return connection_successful


def main():
    """
    @brief Main control loop for autonomous lane detection.
    @details Initializes WiFi connection, Arduino serial communication, and 
             camera stream. Continuously detects lane curves and sends motor 
             control commands to the Arduino based on lane position.
    
    @note Requires prior WiFi connection setup and Arduino initialization
    @return None
    """

    # Connect to WiFi before starting the main loop
    connection_made = connect_to_wifi(ROBOT_WIFI_NAME)
    if not connection_made:
        print("Failed to connect to WiFi.")
        return
    
    # Establish connection to Arduino
    arduino = serial.Serial(port=ARDUINO_PORT, baudrate=ARDUINO_BAUDRATE, timeout=1)
    time.sleep(ARDUINO_INIT_DELAY)
    
    # Initialize webcam module
    webcam = WebcamModule.Webcam(debug=debug_mode)

    # Send start command to robot
    arduino.write(f"G:0\n".encode('utf-8'))
    
    # Main control loop
    while True:
        # Get current frame from camera
        img = webcam.getImg(display=True)
        # Detect lane curve (in pixels)
        # Negative = left turn, Positive = right turn
        curve_pixel = getLaneCurve(img,display=0)
        curve_degrees = curve_pixel * CURVE_SCALE_FACTOR # 100 pixels should equal 13.75

        # Calculate turn value with sensitivity
        turn_val = abs(curve_degrees) * SENSITIVITY

        # Limit turn value to maximum speed
        if turn_val > MAX_SPEED:
            turn_val = MAX_SPEED

        if curve_degrees > CURVE_THRESHOLD:  
            cmd = "R" # Right turn
        elif curve_degrees < -CURVE_THRESHOLD:
            cmd = "L"  # Left turn
        else:
            cmd = "G"  # Go straight
            turn_val = 0

        # Format and send command to Arduino
        send_command = f"{cmd}:{abs(turn_val):.2f}\n"
        arduino.write(send_command.encode('utf-8'))

        # Live update print in one line so terminal doesn't get filled with prints
        print(f"Curve in degrees:\t{curve_degrees:.2f}\tCommand: {cmd}", end="\r")
     
if __name__ == '__main__':
    main()
