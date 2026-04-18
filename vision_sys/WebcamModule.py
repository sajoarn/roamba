import cv2
import numpy as np

class Webcam:
    def __init__(self, stream_url='http://192.168.4.1:81/stream',debug=False):
        if debug:
            self.cap = cv2.VideoCapture('vid1.mp4')
            self.debug_mode = True
            print("Debug mode enabled: Using local video file 'vid1.mp4' instead of camera stream.")
        else:
            self.cap = cv2.VideoCapture(stream_url)
            self.debug_mode = False
        if not self.cap.isOpened():
            print("\n[ERROR] OpenCV cannot open the camera URL.")
            print("Are you sure the PC is connected to the ELEGOO Wi-Fi?\n")
        else:
            print("Connection made to camera.\n")
        
    def getImg(self, display=False, size=[480,240]):
        ret, img = self.cap.read()

        if self.debug_mode and not ret:
            # Rewind the video back to frame 0
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            # Read the first frame again
            ret, img = self.cap.read()

        if not ret or img is None:
            print("WARNING: Camera feed dropped a frame! Waiting for voltage to stabilize...")
            # Return a blank black image so cv2.resize doesn't explode
            return np.zeros((size[1], size[0], 3), dtype=np.uint8)

        img = cv2.resize(img, (size[0], size[1]))

        if display:
            cv2.imshow("IMG", img)
            cv2.waitKey(1)
        return img