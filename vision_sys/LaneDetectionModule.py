"""
@file LaneDetectionModule.py
@brief Lane detection module for autonomous robot navigation.
@details Performs image processing to detect lane curves using thresholding,
         perspective warping, and histogram analysis. Provides smoothed curve
         values through moving average filtering.
"""

import cv2
import numpy as np
import utils

# ============================================================================
# Global Configuration Variables
# ============================================================================

DEBUG_VIDEO_FILE = '../resources/vids/single_lane.mp4'

## List to store raw curve values for smoothing via moving average
curve_list = []

## Number of frames to average for curve smoothing
AVERAGE_WINDOW_SIZE = 10

# ============================================================================
# Function Definitions
# ============================================================================

def getLaneCurve(img, display=2):
    """
    @brief Detect lane curve from camera image.
    @details Performs image thresholding, perspective warping, and histogram
             analysis to determine the lateral offset of the lane. Applies
             moving average smoothing for stable steering values.
    
    @param img (numpy.ndarray) - Input image from camera (BGR format)
    @param display (int) - Display mode:
                          0 = no display
                          1 = display result only
                          2 = display complete pipeline (default)
    
    @return int - Smoothed curve value in pixels
                 Negative = curve left, Positive = curve right
    """
    utils.initializeTrackbars([102, 80, 20, 214])

    imgCopy = img.copy()
    imgResult = img.copy()

    # Step 1: Threshold the image to isolate lane markings
    imgThres = utils.thresholding(img)

    # Step 2: Apply perspective warping for bird's-eye view
    hT, wT, c = img.shape
    points = utils.valTrackbars()
    imgWarp = utils.warpImg(imgThres, points, wT, hT)
    imgWarpPoints = utils.drawPoints(imgCopy, points)

    # Step 3: Find lane center using histogram analysis
    # midPoint analyzes bottom quarter of image for immediate lane position
    midPoint, imgHist = utils.getHistogram(imgWarp, display=True, minPer=0.5, region=4)
    # curveAvgPoint analyzes full bottom of image for broader lane trend
    curveAvgPoint, imgHist = utils.getHistogram(imgWarp, display=True, minPer=0.9)
    curveRaw = curveAvgPoint - midPoint

    # Step 4: Apply moving average to smooth steering transitions
    curve_list.append(curveRaw)
    if len(curve_list) > AVERAGE_WINDOW_SIZE:
        curve_list.pop(0)
    curve = int(sum(curve_list) / len(curve_list))

    # Step 5: Visualize lane detection results
    if display != 0:
        imgInvWarp = utils.warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT//3, 0:wT] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 450
        
        # Display curve value
        cv2.putText(imgResult, str(curve), (wT//2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        
        # Draw lane center line
        cv2.line(imgResult, (wT//2, midY), (wT//2 + (curve * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)
        
        # Draw lane width indicators
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
                     (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
    
    # Display results based on display mode
    if display == 2:
        imgStacked = utils.stackImages(0.7, ([img, imgWarpPoints, imgWarp],
                                             [imgHist, imgLaneColor, imgResult]))
        cv2.imshow('ImageStack', imgStacked)
    elif display == 1:
        cv2.imshow('Result', imgResult)

    return curve

# ============================================================================
# Main Test Program
# ============================================================================

if __name__ == '__main__':
    # Open video file or camera
    # Note: Replace "test.jpeg" with 0 for live camera feed
    cap = cv2.VideoCapture(DEBUG_VIDEO_FILE)

    # Initialize trackbars for perspective warping calibration
    initialTrackBarVals = [102, 80, 20, 214]
    utils.initializeTrackbars(initialTrackBarVals)

    frame_counter = 0

    # Verify video/camera is available
    if not cap.isOpened():
        raise IOError("Can't open video capture")

    # Main processing loop
    while True:
        frame_counter += 1
        
        # Reset video to beginning if at end
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frame_counter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frame_counter = 0

        # Read frame from video/camera
        ret, img = cap.read()

        if not ret:
            print("End of video or failed to read frame")
            break

        # Resize for faster processing
        img = cv2.resize(img, dsize=(0, 0), fx=0.75, fy=0.5)

        # Detect lane curve
        curve = getLaneCurve(img, display=2)
        print(curve)

        # Exit on ESC key
        key = cv2.waitKey(10)
        if key == 27:
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
