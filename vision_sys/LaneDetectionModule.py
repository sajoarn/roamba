import cv2
import numpy as np
import utlis

curveList=[]
avgVal=10

def getLaneCurve(img, display=2): #0=no display, 1=display result, 2=display complete pipeline

    imgCopy=img.copy()
    imgResult=img.copy()
    initialTrackBarVals=[57,185,10,285]
    utlis.initializeTrackbars(initialTrackBarVals)
    ##STEP1 to find the lane
    imgThres= utlis.thresholding(img)

    ##STEP2: finding warpature of the lane
    hT,wT,c=img.shape
    points=utlis.valTrackbars()
    imgWarp=utlis.warpImg(imgThres,points,wT,hT)
    imgWarpPoints=utlis.drawPoints(imgCopy, points)

    ##STEP3: trying to determine the center of the path, even when note straight
    midPoint,imgHist= utlis.getHistogram(imgWarp, display=True,minPer=0.5,region=4) #the region being 4 means it just looks at the bottom fourth of the image
    curveAvgPoint,imgHist= utlis.getHistogram(imgWarp, display=True,minPer=0.9)
    #print(basePoint-midPoint)
    curveRaw=curveAvgPoint-midPoint

    ##step 4: help create a smoother transition and result when looking at the path
    curveList.append(curveRaw)
    if len(curveList)>avgVal:
        curveList.pop(0)
    curve=int(sum(curveList)/len(curveList))

    ##STEP 5: display
    if display != 0:
       imgInvWarp = utlis.warpImg(imgWarp, points, wT, hT,inv = True)
       imgInvWarp = cv2.cvtColor(imgInvWarp,cv2.COLOR_GRAY2BGR)
       imgInvWarp[0:hT//3,0:wT] = 0,0,0
       imgLaneColor = np.zeros_like(img)
       imgLaneColor[:] = 0, 255, 0
       imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
       imgResult = cv2.addWeighted(imgResult,1,imgLaneColor,1,0)
       midY = 450
       cv2.putText(imgResult,str(curve),(wT//2-80,85),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),3)
       cv2.line(imgResult,(wT//2,midY),(wT//2+(curve*3),midY),(255,0,255),5)
       cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY-25), (wT // 2 + (curve * 3), midY+25), (0, 255, 0), 5)
       for x in range(-30, 30):
           w = wT // 20
           cv2.line(imgResult, (w * x + int(curve//50 ), midY-10),
                    (w * x + int(curve//50 ), midY+10), (0, 0, 255), 2)
       #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
       #cv2.putText(imgResult, 'FPS '+str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230,50,50), 3);
    #show how images should be stacked, 2 for all, 1 for just result
    if display == 2:
       imgStacked = utlis.stackImages(0.7,([img,imgWarpPoints,imgWarp],
                                         [imgHist,imgLaneColor,imgResult]))
       cv2.imshow('ImageStack',imgStacked)
    elif display == 1:
       cv2.imshow('Resutlt',imgResult)

    #normalization of values
    #curve=curve/100
    #if curve>1:
    #    curve=1
    #if curve<-1:
    #    curve=-1    
    # cv2.imshow('Thres', imgThres) ##grayscale of the lane
    # cv2.imshow('Warp', imgWarp) ##"birds eye" view of the lane
    # cv2.imshow('Warp Points', imgWarpPoints) #adding dots to the image to tell
    # cv2.imshow('Histogram', imgHist)   #display histogram
    return curve




###MAIN EXE
if __name__=='__main__':

    ##add the file path of the video here or replace with 0 for the camera
    cap = cv2.VideoCapture("vid1.mp4") 

    #the next two lines is to help with cropping the video to find the lane from a "birds eye view"
    initialTrackBarVals=[102,80,20,214]
    utlis.initializeTrackbars(initialTrackBarVals)

    frameCounter=0

    #error checking if video/camera isnt working
    if not cap.isOpened():
        raise IOError("Can't open video capture")

    

    while True:

        frameCounter +=1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) ==frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
            frameCounter=0


        ret, img = cap.read()

        #print(ret)

        if not ret:
            print("End of video or failed to read frame")
            break

        img = cv2.resize(img, dsize=(0,0), fx=0.75, fy=0.5)

        curve=getLaneCurve(img,display=2)
        print(curve)

        #cv2.imshow("Webcam", img)

        key = cv2.waitKey(10)
        if key == 27:  # esc key
            break

    cap.release()
    cv2.destroyAllWindows()