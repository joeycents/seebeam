"""
Accuracy Measurement Module
Implements validation and accuracy testing as per RealEye whitepaper
"""
import numpy as np
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class AccuracyResult:
    """
    Results from accuracy measurement
    """
    mean_error: float  # Mean error in pixels
    median_error: float  # Median error in pixels
    std_error: float  # Standard deviation
    min_error: float
    max_error: float
    errors_per_target: List[float]  # Error for each target
    success_rate: float  # Percentage of targets meeting threshold


class AccuracyTester:
    """
    Tests gaze estimation accuracy using grid-based validation
    """

    def __init__(self, screen_width: int = 1920, screen_height: int = 1080):
        """
        Initialize accuracy tester

        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

    def generate_13_point_grid(self) -> List[Tuple[float, float]]:
        """
        Generate 13-point validation grid for desktop

        Returns:
            List of (x, y) coordinates in pixels
        """
        w = self.screen_width
        h = self.screen_height

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

        # Bottom row (3 points)
        y3 = h - margin_y
        for i in [0, 2, 4]:
            x = margin_x + (w - 2 * margin_x) * i / 4
            positions.append((x, y3))

        return positions

    def generate_49_point_grid(self) -> List[Tuple[float, float]]:
        """
        Generate 49-point validation grid (7×7) for full-screen accuracy

        Returns:
            List of (x, y) coordinates in pixels
        """
        w = self.screen_width
        h = self.screen_height

        margin_x = w * 0.05
        margin_y = h * 0.05

        positions = []

        for row in range(7):
            y = margin_y + (h - 2 * margin_y) * row / 6
            for col in range(7):
                x = margin_x + (w - 2 * margin_x) * col / 6
                positions.append((x, y))

        return positions

    def generate_mobile_13_grid(self) -> List[Tuple[float, float]]:
        """
        Generate 13-point mobile validation grid

        Returns:
            List of (x, y) coordinates in pixels
        """
        # Mobile uses similar pattern to desktop but optimized for smaller screen
        return self.generate_13_point_grid()

    def generate_mobile_21_grid(self) -> List[Tuple[float, float]]:
        """
        Generate 21-point mobile validation grid (3×7)

        Returns:
            List of (x, y) coordinates in pixels
        """
        w = self.screen_width
        h = self.screen_height

        margin_x = w * 0.1
        margin_y = h * 0.05

        positions = []

        for row in range(7):
            y = margin_y + (h - 2 * margin_y) * row / 6
            for col in range(3):
                x = margin_x + (w - 2 * margin_x) * col / 2
                positions.append((x, y))

        return positions

    def calculate_accuracy_closest_fixation(self,
                                           target_pos: Tuple[float, float],
                                           fixations: List[Tuple[float, float]]) -> float:
        """
        Calculate accuracy using closest fixation method (best performing per paper)

        Args:
            target_pos: Target position (x, y) in pixels
            fixations: List of fixation positions (x, y) in pixels

        Returns:
            Distance to closest fixation in pixels
        """
        if not fixations:
            return float('inf')

        distances = [
            np.sqrt((f[0] - target_pos[0])**2 + (f[1] - target_pos[1])**2)
            for f in fixations
        ]

        return min(distances)

    def calculate_accuracy_mean_fixation(self,
                                        target_pos: Tuple[float, float],
                                        fixations: List[Tuple[float, float]]) -> float:
        """
        Calculate accuracy using mean of all fixations

        Args:
            target_pos: Target position (x, y) in pixels
            fixations: List of fixation positions (x, y) in pixels

        Returns:
            Distance from target to mean fixation position in pixels
        """
        if not fixations:
            return float('inf')

        mean_x = np.mean([f[0] for f in fixations])
        mean_y = np.mean([f[1] for f in fixations])

        distance = np.sqrt(
            (mean_x - target_pos[0])**2 +
            (mean_y - target_pos[1])**2
        )

        return distance

    def test_accuracy(self,
                     grid_points: List[Tuple[float, float]],
                     fixations_per_target: List[List[Tuple[float, float]]],
                     method: str = "closest") -> AccuracyResult:
        """
        Test accuracy across a grid of targets

        Args:
            grid_points: List of target positions
            fixations_per_target: List of fixations for each target
            method: "closest" or "mean"

        Returns:
            AccuracyResult object with detailed metrics
        """
        if len(grid_points) != len(fixations_per_target):
            raise ValueError("Number of targets must match number of fixation lists")

        errors = []

        for target, fixations in zip(grid_points, fixations_per_target):
            if method == "closest":
                error = self.calculate_accuracy_closest_fixation(target, fixations)
            elif method == "mean":
                error = self.calculate_accuracy_mean_fixation(target, fixations)
            else:
                raise ValueError(f"Unknown method: {method}")

            errors.append(error)

        # Filter out infinite errors (no fixations)
        valid_errors = [e for e in errors if e != float('inf')]

        if len(valid_errors) == 0:
            return AccuracyResult(
                mean_error=float('inf'),
                median_error=float('inf'),
                std_error=0,
                min_error=float('inf'),
                max_error=float('inf'),
                errors_per_target=errors,
                success_rate=0.0
            )

        # Calculate statistics
        mean_error = np.mean(valid_errors)
        median_error = np.median(valid_errors)
        std_error = np.std(valid_errors)
        min_error = np.min(valid_errors)
        max_error = np.max(valid_errors)

        # Success rate (within 200px threshold - common standard)
        threshold = 200.0
        success_count = sum(1 for e in valid_errors if e <= threshold)
        success_rate = (success_count / len(valid_errors)) * 100

        return AccuracyResult(
            mean_error=mean_error,
            median_error=median_error,
            std_error=std_error,
            min_error=min_error,
            max_error=max_error,
            errors_per_target=errors,
            success_rate=success_rate
        )

    def exclude_saccadic_latency(self,
                                 fixations: List[Tuple[float, float, float]],
                                 target_onset_time: float,
                                 latency_ms: float = 200) -> List[Tuple[float, float]]:
        """
        Exclude fixations within saccadic latency period

        Args:
            fixations: List of (x, y, timestamp) tuples
            target_onset_time: Time when target appeared (ms)
            latency_ms: Saccadic latency to exclude (ms)

        Returns:
            Filtered list of (x, y) fixations
        """
        filtered = [
            (f[0], f[1]) for f in fixations
            if f[2] > target_onset_time + latency_ms
        ]
        return filtered

    def convert_percentage_to_pixels(self, gaze_pct: Tuple[float, float]) -> Tuple[float, float]:
        """
        Convert gaze coordinates from percentage to pixels

        Args:
            gaze_pct: Gaze position as (x%, y%)

        Returns:
            Gaze position as (x_px, y_px)
        """
        x_px = (gaze_pct[0] / 100.0) * self.screen_width
        y_px = (gaze_pct[1] / 100.0) * self.screen_height
        return (x_px, y_px)

    def generate_accuracy_report(self, result: AccuracyResult) -> str:
        """
        Generate human-readable accuracy report

        Args:
            result: AccuracyResult object

        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 60)
        report.append("ACCURACY TEST RESULTS")
        report.append("=" * 60)
        report.append(f"Mean Error:     {result.mean_error:.2f} pixels")
        report.append(f"Median Error:   {result.median_error:.2f} pixels")
        report.append(f"Std Deviation:  {result.std_error:.2f} pixels")
        report.append(f"Min Error:      {result.min_error:.2f} pixels")
        report.append(f"Max Error:      {result.max_error:.2f} pixels")
        report.append(f"Success Rate:   {result.success_rate:.1f}%")
        report.append(f"Targets Tested: {len(result.errors_per_target)}")
        report.append("=" * 60)

        # Compare to RealEye benchmarks
        report.append("\nComparison to RealEye Whitepaper Benchmarks:")
        report.append("  Desktop Calibration Target:  ~106px")
        report.append("  Desktop Full-screen Target:  ~123px")
        report.append("  Mobile Calibration Target:   ~56px")
        report.append("  Mobile Full-screen Target:   ~70px")

        return "\n".join(report)
