"""
@file MainRobotLane.py
@brief Main control script for ELEGOO robot with lane detection.
@details Handles WiFi connection, camera streaming, and lane detection
         to autonomously navigate the robot. Commands are sent to the 
         Arduino microcontroller via serial communication.
"""

from LaneDetectionModule import getLaneCurve, initCompVision
import WebcamModule
import serial
import subprocess
import platform
import time
import threading
import queue

# Thread coordination objects.
_stop_event = threading.Event()
_log_queue = queue.Queue()

# Initialize logging queue and worker thread to handle all print output.
# This thread is joined during shutdown so queued messages are flushed.
def log_worker():
    while True:
        message = _log_queue.get()
        if message is None:
            _log_queue.task_done()
            break
        print(message, flush=True)
        _log_queue.task_done()

_log_thread = threading.Thread(target=log_worker)
_log_thread.start()


def log(message):
    _log_queue.put(message)


def shutdown_logging(timeout=1.0):
    """Flush any backlogged log messages and stop the log worker thread."""
    _log_queue.put(None)
    _log_queue.join()
    _log_thread.join(timeout=timeout)

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

## Scale factor to convert pixels to degrees (100 pixels = 13.75 degrees)
CURVE_SCALE_FACTOR = 0.1375

## Network initialization delay (seconds)
NETWORK_INIT_DELAY = 5

## Arduino connection initialization delay (seconds)
ARDUINO_INIT_DELAY = 2

## Curve threshold for determining turn direction (degrees)
CURVE_THRESHOLD_LOW = 0.1
CURVE_THRESHOLD_HIGH = 2

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
    log(f"Detected OS: {current_os}. Attempting to connect to {ssid}...")
    connection_successful = False
    if current_os == "Windows":
        # WINDOWS CONNECTION
        try:
            # The command: netsh wlan connect name="SSID"
            cmd = f'netsh wlan connect name="{ssid}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if "completed successfully" in result.stdout:
                log(f"Windows: Command sent to connect to {ssid}.")
                connection_successful = True
            else:
                log(f"Windows: Warning - {result.stdout.strip()}")
                
        except Exception as e:
            log(f"Windows Error: {e}")

    elif current_os == "Linux":
        # LINUX / RASPBERRY PI CONNECTION
        # Linux is much better at this. We use the 'nmcli' (NetworkManager) command.
        try:
            cmd = ["nmcli", "device", "wifi", "connect", ssid]
            if password:
                cmd.extend(["password", password])
                
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                log(f"Linux: Successfully connected to {ssid}.")
                connection_successful = True
            else:
                log(f"Linux Error: {result.stderr.strip()}")
                
        except Exception as e:
            log(f"Linux Error: {e}")
            
    else:
        log(f"Unsupported Operating System: {current_os}")

    log("Waiting 5 seconds for network IP assignment...")
    time.sleep(NETWORK_INIT_DELAY)
    log("Ready to connect to camera stream!")

    return connection_successful


def read_arduino_data(arduino):
    """
    @brief Continuously read and print data from Arduino serial connection.
    @details Runs in a separate thread to monitor incoming serial data.
    
    @param arduino Serial object for Arduino communication.
    """
    while not _stop_event.is_set():
        if arduino.in_waiting > 0:
            received_data = arduino.readline().decode('utf-8').strip()
            log(f"Arduino: {received_data}")
        time.sleep(0.01)  # Small delay to avoid high CPU usage

def determine_curve(webcam):
    """Determine the curve of the current frame"""
    # Get current frame from camera
    img = webcam.getImg(display=True)
    # Detect lane curve (in pixels)
    # Negative = left turn, Positive = right turn
    curve_pixel = getLaneCurve(img,display=0)
    curve_degrees = curve_pixel * CURVE_SCALE_FACTOR # 100 pixels should equal 13.75

    if curve_degrees > CURVE_THRESHOLD_LOW and curve_degrees < CURVE_THRESHOLD_HIGH:  
        cmd = "R" # Right turn
    elif curve_degrees > CURVE_THRESHOLD_HIGH:
        cmd = "C" # Sharp right turn clockwise
    elif curve_degrees < -CURVE_THRESHOLD_LOW and curve_degrees > -CURVE_THRESHOLD_HIGH:
        cmd = "L"  # Left turn
    elif curve_degrees < -CURVE_THRESHOLD_HIGH:
        cmd = "A" # Sharp left turn anti-clockwise
    else:
        cmd = "F"  # Go forward

    return cmd, curve_degrees

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
    # connection_made = connect_to_wifi(ROBOT_WIFI_NAME)
    # if not connection_made:
    #     print("Failed to connect to WiFi.")
    #     # FIXME: comment out return. Workaround to allow continue running since
    #     # nmcli does not work running over ssh
    #     return
    
    # Establish connection to Arduino
    arduino = serial.Serial(port=ARDUINO_PORT, baudrate=ARDUINO_BAUDRATE, timeout=1)
    time.sleep(ARDUINO_INIT_DELAY)
    
    # Start thread for reading Arduino serial data
    arduino_thread = threading.Thread(target=read_arduino_data, args=(arduino,))
    arduino_thread.start()
    
    # Initialize webcam module and start Webcam thread
    webcam = WebcamModule.Webcam(debug=debug_mode)
    webcam.start()

    # Initialize Computer vision module
    initCompVision()
    determine_curve(webcam) # Pull up first frame

    
    # Wait for user input to start the control loop
    log("Ready to start autonomous navigation. Press Enter to begin...")
    input()
    # Read webcam once to clear stale buffer
    determine_curve(webcam)

    # Track runtime elapsed in seconds from main() start
    start_time = time.perf_counter()
    
    try:
        # Main control loop
        while True:
            cmd, curve_degrees = determine_curve(webcam)

            # Format and send command to Arduino
            send_command = f"{cmd}\n"
            arduino.write(send_command.encode('utf-8'))

            elapsed_seconds = time.perf_counter() - start_time

            # Live update print in one line so terminal doesn't get filled with prints
            log(f"RPi: [{elapsed_seconds:.8f}s] Curve in degrees:\t{curve_degrees:.2f}\tCommand: {cmd}")
    except KeyboardInterrupt:
        log("KeyboardInterrupt received, shutting down...")
    except Exception as exc:
        log(f"Exception occurred: {exc}")
    finally:
        _stop_event.set()
        log("Stopping...")
        try:
            arduino.write(f"S\n".encode('utf-8'))
        except Exception:
            pass
        if arduino_thread is not None:
            arduino_thread.join(timeout=1.0)
        # if webcam.thread is not None:
        #     webcam.stop()
        #     webcam.thread.join(timeout=1.0)
        shutdown_logging(timeout=1.0)
    
if __name__ == '__main__':
    main()
