import cv2
import numpy as np
import utlis

def getLaneCurve(img):

    imgCopy=img.copy()

    ##STEP1 to find the lane
    imgThres= utlis.thresholding(img)

    ##STEP2: finding warpature of the lane
    h,w,c=img.shape
    points=utlis.valTrackbars()
    imgWarp=utlis.warpImg(imgThres,points,w,h)
    imgWarpPoints=utlis.drawPoints(imgCopy, points)

    ##STEP3
    basePoint,imgHist= utlis.getHistogram(imgWarp, display=True)

    
    cv2.imshow('Thres', imgThres) ##grayscale of the lane
    cv2.imshow('Warp', imgWarp) ##"birds eye" view of the lane
    cv2.imshow('Warp Points', imgWarpPoints) #adding dots to the image to tell
    cv2.imshow('Histogram', imgHist)   #display histogram


    return None




###MAIN EXE
if __name__=='__main__':

    cap = cv2.VideoCapture(r"C:\Users\hussa\OneDrive\Desktop\Personal\Grad School\Purdue\ECE 568-Embedded Systems\Project\vid1.mp4") ##add the file path of the video here or replace with 0 for the camera

    #the next two lines is to help with cropping the video to find the lane from a "birds eye view"
    initialTrackBarVals=[102,80,20,214]
    utlis.initializeTrackbars(initialTrackBarVals)

    frameCounter=0

    if not cap.isOpened():
        raise IOError("Can't open video capture")

    while True:

        frameCounter +=1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) ==frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
            frameCounter=0


        ret, img = cap.read()

        print(ret)

        if not ret:
            print("End of video or failed to read frame")
            break

        img = cv2.resize(img, dsize=(0,0), fx=0.75, fy=0.5)

        getLaneCurve(img)

        cv2.imshow("Webcam", img)

        key = cv2.waitKey(10)
        if key == 27:  # esc key
            break

    cap.release()
    cv2.destroyAllWindows()