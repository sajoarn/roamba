import cv2
import numpy as np
#import utlis
# connnect to robot and then robot wifi
stream_url = 'http://192.168.4.1:81/stream'
cap = cv2.VideoCapture(stream_url)

if __name__ == '__main__':
    #cap = cv2.VideoCapture(r"C:\Users\hussa\Downloads\vid1.mp4")
    #stream_url = 'http://192.168.4.1:81/stream'
    cap = cv2.VideoCapture(stream_url)
    print("Connection made\n")
    while True:
        _, img = cap.read() # GET THE IMAGE
        img = cv2.resize(img,(640,480)) # RESIZE
        #getLaneCurve(img)
        cv2.waitKey(1)

        