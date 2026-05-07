"""
@file ColorPickerScript.py
@brief Interactive HSV color picker using OpenCV trackbars.

This script reads frames from a video source, converts each frame to HSV,
creates a mask based on user-controlled HSV thresholds, and displays the
original, mask, and resulting filtered image side by side.
"""

import cv2
import numpy as np


# ============================================================================
# Global Configuration Variables
# ============================================================================

# Constants for video capture settings
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CAMERA_SOURCE = '../resources/vids/single_lane.mp4'  # Path to video file or 0 for camera
WINDOW_NAME = 'HSV'
DISPLAY_WINDOW = 'Horizontal Stacking'

# ============================================================================
# Function Definitions
# ============================================================================

def empty(_value):
    """
    @brief Callback placeholder for OpenCV trackbars.

    @param _value Current trackbar position (unused).
    """
    pass


def create_hsv_trackbars(window_name: str) -> None:
    """
    @brief Create HSV range trackbars in a named OpenCV window.

    @param window_name Name of the OpenCV window.
    """
    cv2.namedWindow(window_name)
    cv2.resizeWindow(window_name, 640, 240)
    cv2.createTrackbar("HUE Min", window_name, 0, 179, empty)
    cv2.createTrackbar("HUE Max", window_name, 179, 179, empty)
    cv2.createTrackbar("SAT Min", window_name, 0, 255, empty)
    cv2.createTrackbar("SAT Max", window_name, 255, 255, empty)
    cv2.createTrackbar("VALUE Min", window_name, 0, 255, empty)
    cv2.createTrackbar("VALUE Max", window_name, 255, 255, empty)


def get_hsv_bounds(window_name: str) -> tuple[np.ndarray, np.ndarray]:
    """
    @brief Read current HSV bounds from the trackbars.

    @param window_name Name of the OpenCV window holding the trackbars.
    @return A tuple containing lower and upper HSV bound arrays.
    """
    h_min = cv2.getTrackbarPos("HUE Min", window_name)
    h_max = cv2.getTrackbarPos("HUE Max", window_name)
    s_min = cv2.getTrackbarPos("SAT Min", window_name)
    s_max = cv2.getTrackbarPos("SAT Max", window_name)
    v_min = cv2.getTrackbarPos("VALUE Min", window_name)
    v_max = cv2.getTrackbarPos("VALUE Max", window_name)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    return lower, upper


def main() -> None:
    """
    @brief Main loop for the HSV color picker.
    """
    # Initialize video capture
    cap = cv2.VideoCapture(CAMERA_SOURCE)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not cap.isOpened():
        raise RuntimeError(f"Unable to open video source: {CAMERA_SOURCE}")

    # Create trackbars for HSV adjustment
    create_hsv_trackbars(WINDOW_NAME)

    frame_counter = 0
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    while True:
        frame_counter += 1
        # Loop video if it reaches the end
        if frame_count > 0 and frame_counter >= frame_count:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frame_counter = 0

        success, img = cap.read()
        if not success or img is None:
            break

        # Convert to HSV color space
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Get current HSV bounds from trackbars
        lower, upper = get_hsv_bounds(WINDOW_NAME)

        # Create mask based on HSV range
        mask = cv2.inRange(img_hsv, lower, upper)
        result = cv2.bitwise_and(img, img, mask=mask)

        # Convert mask to BGR for stacking
        mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        h_stack = np.hstack([img, mask_bgr, result])

        # Display the stacked images
        cv2.imshow(DISPLAY_WINDOW, h_stack)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
