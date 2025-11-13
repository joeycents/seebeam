"""
Virtual Chinrest Module
Handles head movement detection and compensation
"""
import numpy as np
from typing import Dict, Optional, Tuple


class VirtualChinrest:
    """
    Detects head movements and compensates for them in gaze estimation
    """

    def __init__(self,
                 position_threshold: float = 30.0,  # pixels
                 size_threshold: float = 20.0):      # pixels
        """
        Initialize virtual chinrest

        Args:
            position_threshold: Maximum allowed head position change (pixels)
            size_threshold: Maximum allowed face size change (pixels)
        """
        self.position_threshold = position_threshold
        self.size_threshold = size_threshold

        # Baseline measurements from calibration
        self.baseline_ipd = None
        self.baseline_left_pupil = None
        self.baseline_right_pupil = None
        self.baseline_face_center = None
        self.baseline_face_size = None

        self.is_initialized = False

    def initialize(self, face_data: Dict):
        """
        Set baseline measurements during calibration

        Args:
            face_data: Face data dictionary from FaceDetector
        """
        self.baseline_ipd = face_data['interpupillary_distance']
        self.baseline_left_pupil = face_data['left_pupil']
        self.baseline_right_pupil = face_data['right_pupil']

        # Calculate face center as midpoint between pupils
        self.baseline_face_center = (
            (self.baseline_left_pupil[0] + self.baseline_right_pupil[0]) / 2,
            (self.baseline_left_pupil[1] + self.baseline_right_pupil[1]) / 2
        )

        # Use IPD as proxy for face size
        self.baseline_face_size = self.baseline_ipd

        self.is_initialized = True

        print(f"Virtual chinrest initialized:")
        print(f"  Baseline IPD: {self.baseline_ipd:.2f}px")
        print(f"  Face center: ({self.baseline_face_center[0]:.1f}, {self.baseline_face_center[1]:.1f})")

    def check_position(self, face_data: Dict) -> str:
        """
        Check if user's head has moved significantly from baseline

        Args:
            face_data: Current face data

        Returns:
            "OK" if position is good, "RECALIBRATE" if movement detected
        """
        if not self.is_initialized:
            return "NOT_INITIALIZED"

        # Calculate current face center
        current_left = face_data['left_pupil']
        current_right = face_data['right_pupil']
        current_center = (
            (current_left[0] + current_right[0]) / 2,
            (current_left[1] + current_right[1]) / 2
        )

        # Calculate position difference
        position_diff = np.sqrt(
            (current_center[0] - self.baseline_face_center[0])**2 +
            (current_center[1] - self.baseline_face_center[1])**2
        )

        # Calculate size difference (using IPD as proxy)
        current_ipd = face_data['interpupillary_distance']
        size_diff = abs(current_ipd - self.baseline_face_size)

        # Check thresholds
        if position_diff > self.position_threshold:
            return "RECALIBRATE"

        if size_diff > self.size_threshold:
            return "RECALIBRATE"

        return "OK"

    def adjust_gaze(self,
                    raw_gaze: Tuple[float, float],
                    face_data: Dict) -> Tuple[float, float]:
        """
        Compensate for minor head movements in gaze estimation

        Args:
            raw_gaze: Raw gaze prediction (x%, y%)
            face_data: Current face data

        Returns:
            Adjusted gaze coordinates (x%, y%)
        """
        if not self.is_initialized:
            return raw_gaze

        # Calculate current face center
        current_left = face_data['left_pupil']
        current_right = face_data['right_pupil']
        current_center = (
            (current_left[0] + current_right[0]) / 2,
            (current_left[1] + current_right[1]) / 2
        )

        # Calculate position delta
        delta_x = current_center[0] - self.baseline_face_center[0]
        delta_y = current_center[1] - self.baseline_face_center[1]

        # Calculate size ratio
        current_ipd = face_data['interpupillary_distance']
        size_ratio = current_ipd / self.baseline_face_size if self.baseline_face_size > 0 else 1.0

        # Convert position delta to screen percentage
        # This is a simplified compensation - more sophisticated approaches could be used
        frame_width = face_data['frame_width']
        frame_height = face_data['frame_height']

        delta_x_pct = (delta_x / frame_width) * 100
        delta_y_pct = (delta_y / frame_height) * 100

        # Apply compensation with dampening factor
        dampening = 0.5  # Adjust this based on empirical testing

        corrected_x = raw_gaze[0] - (delta_x_pct * dampening)
        corrected_y = raw_gaze[1] - (delta_y_pct * dampening)

        # Apply size compensation (closer = gaze shifts more)
        size_adjustment = (size_ratio - 1.0) * 5.0  # Scale factor
        corrected_x -= size_adjustment * np.sign(corrected_x - 50)
        corrected_y -= size_adjustment * np.sign(corrected_y - 50)

        # Clamp to valid range
        corrected_x = max(0.0, min(100.0, corrected_x))
        corrected_y = max(0.0, min(100.0, corrected_y))

        return (corrected_x, corrected_y)

    def get_movement_metrics(self, face_data: Dict) -> Dict:
        """
        Get detailed movement metrics

        Args:
            face_data: Current face data

        Returns:
            Dictionary with movement information
        """
        if not self.is_initialized:
            return {'initialized': False}

        # Calculate current measurements
        current_left = face_data['left_pupil']
        current_right = face_data['right_pupil']
        current_center = (
            (current_left[0] + current_right[0]) / 2,
            (current_left[1] + current_right[1]) / 2
        )
        current_ipd = face_data['interpupillary_distance']

        # Calculate differences
        position_diff = np.sqrt(
            (current_center[0] - self.baseline_face_center[0])**2 +
            (current_center[1] - self.baseline_face_center[1])**2
        )
        size_diff = abs(current_ipd - self.baseline_face_size)

        return {
            'initialized': True,
            'position_diff': position_diff,
            'position_threshold': self.position_threshold,
            'position_ok': position_diff <= self.position_threshold,
            'size_diff': size_diff,
            'size_threshold': self.size_threshold,
            'size_ok': size_diff <= self.size_threshold,
            'overall_status': self.check_position(face_data)
        }

    def reset(self):
        """
        Reset chinrest to uninitialized state
        """
        self.baseline_ipd = None
        self.baseline_left_pupil = None
        self.baseline_right_pupil = None
        self.baseline_face_center = None
        self.baseline_face_size = None
        self.is_initialized = False

        print("Virtual chinrest reset")
