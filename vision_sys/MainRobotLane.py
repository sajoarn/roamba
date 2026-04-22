from LaneDetectionModule import getLaneCurve
import WebcamModule
import serial
import subprocess
import platform
import time

def connect_to_wifi(ssid, password=None):
    current_os = platform.system()
    print(f"Detected OS: {current_os}. Attempting to connect to {ssid}...")
    connection_successful=False;
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
    time.sleep(5)
    print("Ready to connect to camera stream!")

    return connection_successful

ROBOT_WIFI_NAME = "ELEGOO-B89958BA2010";
debug_mode = False # Set to True to use local video file instead of camera stream for testing
def main():

    connection_made = connect_to_wifi(ROBOT_WIFI_NAME) # Connect to WiFi before starting the main loop
    if not connection_made:
        print("Failed to connect to WiFi.")
        return
    
    arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=1); # Establish connection to Arduino
    time.sleep(2) # Wait for the connection to initialize
    webcam = WebcamModule.Webcam(debug=debug_mode) # Initialize webcam module

    arduino.write(f"G:0\n".encode('utf-8')) # car starts
    #print('Robot Go\n')
    while True:
        #print('Lane detection\n')
        img = webcam.getImg()
        curvePixel= getLaneCurve(img,1) # curve in pixels, the higher the value the sharper the turn. Negative is left, positive is right
        curveDegrees = curvePixel * 0.1375 # 100 pixels should equal 13.75

        sen = 1.3  # SENSITIVITY
        maxVAl= 0.5 # MAX SPEED

        turnVal = abs(curveDegrees) * sen

        if turnVal>maxVAl:
            turnVal = maxVAl

        
        if curveDegrees > 0.5:  
            cmd = "R"
        elif curveDegrees < -0.5:
            cmd = "L"
        else:
            cmd = "G"
            turnVal = 0

        sendCommand = f"{cmd}:{abs(turnVal):.2f}\n"
        print(sendCommand)
        arduino.write(sendCommand.encode('utf-8'))  # Send command to Arduino
     
if __name__ == '__main__':
    main()
