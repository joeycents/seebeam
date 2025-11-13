"""
Calibration Module
Handles the multi-point calibration process
"""
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class DeviceType(Enum):
    """Device type for calibration"""
    DESKTOP = "desktop"
    MOBILE = "mobile"


@dataclass
class CalibrationPoint:
    """
    Represents a calibration target point
    """
    target_x: float  # Target X coordinate (pixels)
    target_y: float  # Target Y coordinate (pixels)
    background_color: str  # Background color (#RRGGBB)
    target_color: str  # Target color (white/black)
    sequence_number: int  # Countdown number (39→1)


@dataclass
class CalibrationSample:
    """
    Represents a calibration data sample
    """
    target_x: float
    target_y: float
    features: np.ndarray  # Feature vector from face data
    timestamp: float
    background_color: str


class Calibrator:
    """
    Manages calibration process for eye tracking
    """

    # Target specifications from whitepaper
    TARGET_TOTAL_DIAMETER = 72  # CSS pixels
    TARGET_INNER_DIAMETER = 24  # CSS pixels (clickable)

    # Background colors for desktop calibration
    BG_DARK_GREY = "#393939"
    BG_MEDIUM_GREY = "#898989"
    BG_LIGHT_GREY = "#CECECE"

    def __init__(self, device_type: DeviceType = DeviceType.DESKTOP,
                 screen_width: int = 1920, screen_height: int = 1080):
        """
        Initialize calibrator

        Args:
            device_type: Desktop or mobile device
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self.device_type = device_type
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.calibration_points = []
        self.calibration_samples = []

        # Generate calibration grid
        self._generate_calibration_points()

    def _generate_calibration_points(self):
        """
        Generate calibration points based on device type
        """
        if self.device_type == DeviceType.DESKTOP:
            self._generate_desktop_points()
        else:
            self._generate_mobile_points()

    def _generate_desktop_points(self):
        """
        Generate 39-point desktop calibration grid (13 positions × 3 backgrounds)
        """
        # Generate 13-point grid
        base_positions = self._generate_13_point_grid()

        sequence_num = 39

        # Phase 1: Dark grey background, white targets
        for pos in base_positions:
            self.calibration_points.append(CalibrationPoint(
                target_x=pos[0],
                target_y=pos[1],
                background_color=self.BG_DARK_GREY,
                target_color="white",
                sequence_number=sequence_num
            ))
            sequence_num -= 1

        # Phase 2: Medium grey background, white targets
        for pos in base_positions:
            self.calibration_points.append(CalibrationPoint(
                target_x=pos[0],
                target_y=pos[1],
                background_color=self.BG_MEDIUM_GREY,
                target_color="white",
                sequence_number=sequence_num
            ))
            sequence_num -= 1

        # Phase 3: Light grey background, black targets
        for pos in base_positions:
            self.calibration_points.append(CalibrationPoint(
                target_x=pos[0],
                target_y=pos[1],
                background_color=self.BG_LIGHT_GREY,
                target_color="black",
                sequence_number=sequence_num
            ))
            sequence_num -= 1

        print(f"Generated {len(self.calibration_points)} desktop calibration points")

    def _generate_mobile_points(self):
        """
        Generate 27-point mobile calibration grid (9 positions × 3 backgrounds)
        """
        # Generate 9-point grid for mobile
        base_positions = self._generate_9_point_grid()

        sequence_num = 27

        # Same background progression as desktop
        for bg_color, target_color in [
            (self.BG_DARK_GREY, "white"),
            (self.BG_MEDIUM_GREY, "white"),
            (self.BG_LIGHT_GREY, "black")
        ]:
            for pos in base_positions:
                self.calibration_points.append(CalibrationPoint(
                    target_x=pos[0],
                    target_y=pos[1],
                    background_color=bg_color,
                    target_color=target_color,
                    sequence_number=sequence_num
                ))
                sequence_num -= 1

        print(f"Generated {len(self.calibration_points)} mobile calibration points")

    def _generate_13_point_grid(self) -> List[Tuple[float, float]]:
        """
        Generate 13-point grid positions

        Grid layout:
        X  X  X  X  X
        X  X  X  X  X
        X  X  X
        """
        w = self.screen_width
        h = self.screen_height

        # Margins from edge
        margin_x = w * 0.1
        margin_y = h * 0.1

        positions = []

        # Top row (5 points)
        y1 = margin_y
        for i in range(5):
            x = margin_x + (w - 2 * margin_x) * i / 4
            positions.append((x, y1))

        # Middle row (5 points)
        y2 = h / 2
        for i in range(5):
            x = margin_x + (w - 2 * margin_x) * i / 4
            positions.append((x, y2))

        # Bottom row (3 points - left, center, right)
        y3 = h - margin_y
        for i in [0, 2, 4]:
            x = margin_x + (w - 2 * margin_x) * i / 4
            positions.append((x, y3))

        return positions

    def _generate_9_point_grid(self) -> List[Tuple[float, float]]:
        """
        Generate 9-point grid (3×3) for mobile
        """
        w = self.screen_width
        h = self.screen_height

        margin_x = w * 0.1
        margin_y = h * 0.1

        positions = []

        for row in range(3):
            y = margin_y + (h - 2 * margin_y) * row / 2
            for col in range(3):
                x = margin_x + (w - 2 * margin_x) * col / 2
                positions.append((x, y))

        return positions

    def add_sample(self, point_index: int, features: np.ndarray, timestamp: float):
        """
        Add a calibration sample for a specific point

        Args:
            point_index: Index of calibration point
            features: Feature vector extracted from face data
            timestamp: Timestamp in milliseconds
        """
        if point_index < 0 or point_index >= len(self.calibration_points):
            raise ValueError(f"Invalid point index: {point_index}")

        cal_point = self.calibration_points[point_index]

        sample = CalibrationSample(
            target_x=cal_point.target_x,
            target_y=cal_point.target_y,
            features=features,
            timestamp=timestamp,
            background_color=cal_point.background_color
        )

        self.calibration_samples.append(sample)

    def get_training_data(self) -> Tuple[List[np.ndarray], List[Tuple[float, float]]]:
        """
        Get training data for gaze estimation model

        Returns:
            Tuple of (features_list, targets_list)
        """
        if len(self.calibration_samples) == 0:
            raise ValueError("No calibration samples collected")

        features = [s.features for s in self.calibration_samples]
        targets = [(s.target_x, s.target_y) for s in self.calibration_samples]

        return features, targets

    def get_validation_points(self, count: int = 3) -> List[Tuple[float, float]]:
        """
        Generate validation points for accuracy check

        Args:
            count: Number of validation points (3 for desktop, 4 for mobile)

        Returns:
            List of (x, y) validation point coordinates
        """
        if self.device_type == DeviceType.MOBILE and count == 3:
            count = 4  # Mobile uses 4 validation points

        w = self.screen_width
        h = self.screen_height

        validation_points = []

        if count == 3:
            # Desktop: top-left, center, bottom-right
            validation_points = [
                (w * 0.25, h * 0.25),
                (w * 0.5, h * 0.5),
                (w * 0.75, h * 0.75)
            ]
        elif count == 4:
            # Mobile: 4 corners (with margin)
            margin_x = w * 0.2
            margin_y = h * 0.2
            validation_points = [
                (margin_x, margin_y),
                (w - margin_x, margin_y),
                (margin_x, h - margin_y),
                (w - margin_x, h - margin_y)
            ]

        return validation_points

    def get_validation_threshold(self) -> float:
        """
        Get validation threshold based on device type

        Returns:
            Maximum allowed distance in pixels
        """
        if self.device_type == DeviceType.DESKTOP:
            return 150.0  # pixels
        else:
            return 100.0  # pixels

    def reset(self):
        """
        Reset calibration data
        """
        self.calibration_samples = []
        print("Calibration data reset")

    def get_progress(self) -> Dict:
        """
        Get calibration progress information

        Returns:
            Dictionary with progress information
        """
        return {
            'total_points': len(self.calibration_points),
            'completed_samples': len(self.calibration_samples),
            'progress_pct': (len(self.calibration_samples) / len(self.calibration_points) * 100)
                           if len(self.calibration_points) > 0 else 0
        }
