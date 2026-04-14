from MotorModule import Motor
from LaneDetectionModule import getLaneCurve
import WebcamModule
import serial

##################################################
#motor = Motor(2,3,4,17,22,27) ##likely need to replace this with serial connection: Motor('/dev/ttyUSB0', 9600)
##################################################
arduino = serial.Serial(port='COM3', baudrate=115200, timeout=1); # Establish connection to Arduino
def main():
 
    img = WebcamModule.getImg()
    curveVal= getLaneCurve(img,1)
 
    sen = 1.3  # SENSITIVITY
    maxVAl= 0.3 # MAX SPEED
    if curveVal>maxVAl:curveVal = maxVAl
    if curveVal<-maxVAl: curveVal =-maxVAl
    #print(curveVal)
    if curveVal>0:
        sen =1.7
        cmd = "R"
        if curveVal<0.05: curveVal=0
    else:
        cmd = "L"
        if curveVal>-0.08: curveVal=0
    arduino.write(f"{cmd}{abs(curveVal):.2f}\n".encode('utf-8'))  # Send command to Arduino
    #motor.move(0.20,-curveVal*sen,0.05)
    #cv2.waitKey(1)
     

if __name__ == '__main__':
    while True:
        main()