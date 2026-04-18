import cv2

#cap =cv2.VideoCapture(0)#pulls video feed from camera
#need to connect to wifi and then use stream url to get video feed from robot's camera
#probably need to do that in wifi

class Webcam:
    def __init__(self, stream_url='http://192.168.4.1:81/stream'):
        self.cap = cv2.VideoCapture(stream_url)
        if not self.cap.isOpened():
            print("\nOpenCV cannot open the camera URL.")
            print("Are you sure the PC is connected to the ELEGOO Wi-Fi?\n")
        else:
            print("Connection made to camera.\n")
        
    def getImg(self,display=False, size=[480,240]):
        _,img = self.cap.read()
        img = cv2.resize(img, (size[0],size[1]))

        if display:
            cv2.imshow("IMG",img)
        return img

