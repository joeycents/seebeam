"""
WebRTC Video Capture Module
Handles webcam access and frame extraction
"""
import cv2
import numpy as np
from typing import Optional, Tuple


class WebcamCapture:
    """
    Handles webcam video capture with configurable resolution and FPS
    """

    def __init__(self, resolution: Tuple[int, int] = (1920, 1080), fps: int = 30):
        """
        Initialize webcam capture

        Args:
            resolution: Desired (width, height) resolution
            fps: Target frames per second
        """
        self.resolution = resolution
        self.fps = fps
        self.cap = None
        self.frame_count = 0
        self._initialize_camera()

    def _initialize_camera(self):
        """
        Initialize camera with specified settings
        """
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            raise RuntimeError("Failed to open webcam")

        # Set resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])

        # Set FPS
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)

        # Get actual settings (may differ from requested)
        actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        actual_fps = int(self.cap.get(cv2.CAP_PROP_FPS))

        print(f"Camera initialized:")
        print(f"  Resolution: {actual_width}x{actual_height} (requested: {self.resolution[0]}x{self.resolution[1]})")
        print(f"  FPS: {actual_fps} (requested: {self.fps})")

    def get_frame(self) -> Optional[np.ndarray]:
        """
        Capture a single frame from webcam

        Returns:
            Frame as numpy array (BGR format) or None if failed
        """
        if self.cap is None or not self.cap.isOpened():
            return None

        ret, frame = self.cap.read()

        if ret:
            self.frame_count += 1
            return frame

        return None

    def get_frame_with_timestamp(self) -> Optional[Tuple[np.ndarray, float]]:
        """
        Capture frame with timestamp

        Returns:
            Tuple of (frame, timestamp_ms) or None if failed
        """
        frame = self.get_frame()
        if frame is not None:
            timestamp = self.cap.get(cv2.CAP_PROP_POS_MSEC)
            return frame, timestamp
        return None

    def release(self):
        """
        Release webcam resources
        """
        if self.cap is not None:
            self.cap.release()
            print(f"Camera released. Total frames captured: {self.frame_count}")

    def __del__(self):
        """
        Destructor to ensure camera is released
        """
        self.release()
