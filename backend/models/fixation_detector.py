"""
Fixation Detection using I-VT (Velocity-Threshold Identification) Filter
Implements the algorithm described in the RealEye whitepaper
"""
import numpy as np
from scipy.ndimage import median_filter
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import deque


@dataclass
class GazePoint:
    """
    Represents a single gaze point measurement
    """
    x: float  # X coordinate (percentage)
    y: float  # Y coordinate (percentage)
    timestamp: float  # Timestamp in milliseconds
    confidence: float = 1.0


@dataclass
class Fixation:
    """
    Represents a detected fixation
    """
    x: float  # Median X coordinate
    y: float  # Median Y coordinate
    duration: float  # Duration in milliseconds
    start_time: float  # Start timestamp
    end_time: float  # End timestamp
    points: List[GazePoint]  # Raw gaze points in fixation
    fixation_id: str  # Unique ID


class FixationDetector:
    """
    Detects fixations using I-VT algorithm with configurable parameters
    """

    def __init__(self,
                 min_duration: float = 100,  # ms
                 max_duration: float = 3000,  # ms
                 noise_window: float = 200,  # ms
                 velocity_threshold: float = 150,  # %/s
                 max_saccade_duration: float = 150,  # ms
                 fps: float = 30):
        """
        Initialize fixation detector

        Args:
            min_duration: Minimum fixation duration (ms)
            max_duration: Maximum fixation duration (ms)
            noise_window: Moving median filter window size (ms)
            velocity_threshold: Velocity threshold for fixation vs saccade (%/s)
            max_saccade_duration: Maximum saccade duration (ms)
            fps: Frame rate for velocity calculation
        """
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.noise_window = noise_window
        self.velocity_threshold = velocity_threshold
        self.max_saccade_duration = max_saccade_duration
        self.fps = fps
        self.frame_time = 1000.0 / fps  # ms per frame

        # State for streaming detection
        self.gaze_buffer = deque(maxlen=int(max_duration / self.frame_time))
        self.current_fixation = []
        self.fixations = []
        self.fixation_counter = 0

    def apply_noise_reduction(self, gaze_points: List[GazePoint]) -> List[Tuple[float, float]]:
        """
        Apply moving median filter to reduce noise

        Args:
            gaze_points: List of raw gaze points

        Returns:
            List of filtered (x, y) coordinates
        """
        if len(gaze_points) < 3:
            return [(p.x, p.y) for p in gaze_points]

        # Calculate window size in samples
        window_samples = max(3, int(self.noise_window / self.frame_time))
        if window_samples % 2 == 0:  # Must be odd for median filter
            window_samples += 1

        # Extract coordinates
        x_coords = np.array([p.x for p in gaze_points])
        y_coords = np.array([p.y for p in gaze_points])

        # Apply median filter
        x_filtered = median_filter(x_coords, size=window_samples, mode='nearest')
        y_filtered = median_filter(y_coords, size=window_samples, mode='nearest')

        return list(zip(x_filtered, y_filtered))

    def calculate_velocity(self, p1: Tuple[float, float],
                          p2: Tuple[float, float],
                          dt: float) -> float:
        """
        Calculate gaze velocity in %/s

        Args:
            p1: First point (x, y)
            p2: Second point (x, y)
            dt: Time difference in milliseconds

        Returns:
            Velocity in %/s (percentage of screen per second)
        """
        if dt <= 0:
            return 0.0

        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        distance = np.sqrt(dx**2 + dy**2)

        # Convert to per second
        velocity = (distance / dt) * 1000.0

        return velocity

    def detect_fixations(self, gaze_stream: List[GazePoint]) -> List[Fixation]:
        """
        Detect fixations in a stream of gaze points using I-VT algorithm

        Args:
            gaze_stream: List of gaze points

        Returns:
            List of detected fixations
        """
        if len(gaze_stream) < 2:
            return []

        # Apply noise reduction
        filtered = self.apply_noise_reduction(gaze_stream)

        fixations = []
        current_fixation_indices = []

        # Process each point
        for i in range(1, len(filtered)):
            # Calculate velocity
            dt = self.frame_time  # Assume constant frame rate
            velocity = self.calculate_velocity(filtered[i-1], filtered[i], dt)

            if velocity < self.velocity_threshold:
                # Part of fixation
                if len(current_fixation_indices) == 0:
                    current_fixation_indices.append(i-1)
                current_fixation_indices.append(i)
            else:
                # Saccade detected - end current fixation
                if len(current_fixation_indices) > 0:
                    fixation = self._create_fixation(
                        gaze_stream,
                        filtered,
                        current_fixation_indices
                    )
                    if fixation is not None:
                        fixations.append(fixation)
                    current_fixation_indices = []

        # Process final fixation if exists
        if len(current_fixation_indices) > 0:
            fixation = self._create_fixation(
                gaze_stream,
                filtered,
                current_fixation_indices
            )
            if fixation is not None:
                fixations.append(fixation)

        return fixations

    def _create_fixation(self,
                        original_points: List[GazePoint],
                        filtered_points: List[Tuple[float, float]],
                        indices: List[int]) -> Optional[Fixation]:
        """
        Create a fixation object from point indices

        Args:
            original_points: Original gaze points
            filtered_points: Filtered coordinates
            indices: Indices of points in the fixation

        Returns:
            Fixation object or None if duration constraints not met
        """
        if len(indices) == 0:
            return None

        # Calculate duration
        duration = len(indices) * self.frame_time

        # Check duration constraints
        if duration < self.min_duration or duration > self.max_duration:
            return None

        # Get fixation points
        fixation_coords = [filtered_points[i] for i in indices]
        fixation_originals = [original_points[i] for i in indices]

        # Calculate median position
        x_median = np.median([p[0] for p in fixation_coords])
        y_median = np.median([p[1] for p in fixation_coords])

        # Get timestamps
        start_time = fixation_originals[0].timestamp
        end_time = fixation_originals[-1].timestamp

        # Generate unique ID
        self.fixation_counter += 1
        fixation_id = f"fix_{self.fixation_counter:04d}"

        return Fixation(
            x=float(x_median),
            y=float(y_median),
            duration=duration,
            start_time=start_time,
            end_time=end_time,
            points=fixation_originals,
            fixation_id=fixation_id
        )

    def add_gaze_point(self, gaze_point: GazePoint) -> Optional[Fixation]:
        """
        Add a gaze point for streaming fixation detection

        Args:
            gaze_point: New gaze point

        Returns:
            Completed fixation if detected, None otherwise
        """
        self.gaze_buffer.append(gaze_point)

        if len(self.gaze_buffer) < 2:
            return None

        # Detect fixations in current buffer
        fixations = self.detect_fixations(list(self.gaze_buffer))

        # Return most recent completed fixation
        if len(fixations) > 0:
            return fixations[-1]

        return None

    def reset(self):
        """
        Reset detector state
        """
        self.gaze_buffer.clear()
        self.current_fixation = []
        self.fixations = []
        self.fixation_counter = 0

    def exclude_saccadic_latency(self, fixations: List[Fixation],
                                 target_onset_time: float,
                                 latency_ms: float = 200) -> List[Fixation]:
        """
        Exclude fixations that occur within saccadic latency period

        Args:
            fixations: List of fixations
            target_onset_time: Time when target appeared (ms)
            latency_ms: Saccadic latency to exclude (ms)

        Returns:
            Filtered list of fixations
        """
        return [f for f in fixations
                if f.start_time > target_onset_time + latency_ms]

    def get_statistics(self) -> Dict:
        """
        Get statistics about detected fixations

        Returns:
            Dictionary with fixation statistics
        """
        if len(self.fixations) == 0:
            return {
                'count': 0,
                'mean_duration': 0,
                'total_duration': 0
            }

        durations = [f.duration for f in self.fixations]

        return {
            'count': len(self.fixations),
            'mean_duration': np.mean(durations),
            'median_duration': np.median(durations),
            'total_duration': np.sum(durations),
            'min_duration': np.min(durations),
            'max_duration': np.max(durations)
        }
