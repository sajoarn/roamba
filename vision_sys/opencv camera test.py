import cv2
import numpy as np
import matplotlib

cap = cv2.VideoCapture(r"C:\Users\hussa\Documents\school\vid1.mp4") ##add the file path of the video here or replace with 0 for the camera

if not cap.isOpened():
    raise IOError("Can't open video capture")

while True:
    ret, frame = cap.read()

    print(ret)

    if not ret:
        print("End of video or failed to read frame")
        break

    frame = cv2.resize(frame, dsize=(0,0), fx=0.5, fy=0.5)

    cv2.imshow("Webcam", frame)

    key = cv2.waitKey(10)
    if key == 27:  # esc key
        break

cap.release()
cv2.destroyAllWindows()



