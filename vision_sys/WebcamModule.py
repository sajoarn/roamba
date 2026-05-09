"""
@file WebcamModule.py
@brief Webcam/camera stream interface for robot vision system.
@details Provides a wrapper class for OpenCV video capture that supports
         both live camera streams via HTTP and local video files for testing.
         Includes error handling and frame dropping recovery.
"""

import cv2
import numpy as np
import threading
import time

# ============================================================================
# Global Configuration Variables
# ============================================================================

## Default camera stream URL for ELEGOO robot
DEFAULT_STREAM_URL = 'http://192.168.4.1:81/stream'

## Default debug video file path for offline testing
DEBUG_VIDEO_FILE = '../resources/vids/single_lane.mp4'

## Default frame width
DEFAULT_FRAME_WIDTH = 800

## Default frame height
DEFAULT_FRAME_HEIGHT = 600


class Webcam:
    """
    @class Webcam
    @brief Interface for accessing camera stream or video file.
    @details Wraps OpenCV VideoCapture for either live camera feeds via HTTP
             or local video files for testing. Handles connection errors and
             automatic frame rewinding in debug mode.
    """

    def __init__(self, stream_url=DEFAULT_STREAM_URL, debug=False):
        """
        @brief Initialize webcam/camera stream connection.
        @details Attempts to open either a live camera stream or a debug video file.
                 Prints connection status and warns if connection fails.
        
        @param stream_url (str) - HTTP URL for live camera stream (default: robot camera)
        @param debug (bool) - If True, use local video file instead of camera stream
        
        @return None
        """
        self.stopped = False
        self.thread = threading.Thread(target=self.update, args=())
        cv2.CAP_PROP_BUFFERSIZE = 1 # Only store a single frame so we don't get camera lag
        if debug:
            self.stream = cv2.VideoCapture(DEBUG_VIDEO_FILE)
            self.debug_mode = True
            print(f"Debug mode enabled: Using local video file '{DEBUG_VIDEO_FILE}' instead of camera stream.")
        else:
            self.stream = cv2.VideoCapture(stream_url)
            self.debug_mode = False
        
        if not self.stream.isOpened():
            print("\n[ERROR] OpenCV cannot open the camera URL.")
            print("Are you sure the PC is connected to the ELEGOO Wi-Fi?\n")
        else:
            print("Connection made to camera.\n")

    def start(self):
        """Start thread"""
        self.thread.start()
        return self
    
    def update(self):
        """Continuously update webcam's frame buffer"""
        while True:
            if self.stopped: return
            # Get at least one frame
            (grabbed, frame) = self.stream.read()
            self.grabbed = grabbed
            self.frame = frame
            # Now empty frame buffer
            # while (grabbed):
            #     (grabbed, frame) = self.stream.read()
            #     if grabbed:
            #         # Every loop, only save last frame if read was successful
            #         self.grabbed = grabbed
            #         self.frame = frame
            # if self.grabbed:
                # cv2.imshow("IMG", frame)
                # cv2.waitKey(1)
            # sleep to give up context for other threads
            # Assuming 60 fps
            time.sleep(0.01)
    def read(self):
        """Get the most recent frame"""
        return self.grabbed, self.frame
    def stop(self):
        """Exit thread gracefully"""
        self.stopped = True
        self.stream.release()
        cv2.destroyAllWindows()
        
    def getImg(self, display=False, size=None):
        """
        @brief Retrieve and process a frame from camera/video stream.
        @details Reads the next frame from the video source. If in debug mode
                 and frame read fails, automatically rewinds video to start.
                 Handles dropped frames gracefully by returning black image.
        
        @param display (bool) - If True, display frame in OpenCV window
        @param size (list) - [width, height] for frame resizing
                            (default: [480, 240])
        
        @return numpy.ndarray - Frame image in BGR format, resized to specified dimensions
                                Returns black image if frame read fails
        """
        if size is None:
            size = [DEFAULT_FRAME_WIDTH, DEFAULT_FRAME_HEIGHT]
        
        # ret, img = self.stream.read()
        ret, img = self.read()

        # In debug mode, rewind video if frame read fails
        if self.debug_mode and not ret:
            # Rewind to beginning of video
            self.stream.set(cv2.CAP_PROP_POS_FRAMES, 0)
            # Read the first frame again
            ret, img = self.stream.read()

        # Handle frame drop by returning blank image
        if not ret or img is None:
            print("WARNING: Camera feed dropped a frame! Waiting for voltage to stabilize...")
            # Return blank black image to prevent errors in downstream processing
            return np.zeros((size[1], size[0], 3), dtype=np.uint8)

        # Shrink frame to reduce processing time
        img = cv2.resize(img, (size[0], size[1]), fx=0.5, fy=0.5)

        if display and img is not None:
            cv2.imshow("IMG", img)
            # cv2.waitKey(1)
        
        return img