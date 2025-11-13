"""
Feature Extraction Module
Extracts relevant features from face/eye landmarks for gaze estimation
"""
import numpy as np
from typing import Dict, List


class FeatureExtractor:
    """
    Extracts features from detected face/eye landmarks for ML models
    """

    def __init__(self):
        """
        Initialize feature extractor
        """
        self.feature_names = []

    def extract_features(self, face_data: Dict) -> np.ndarray:
        """
        Extract feature vector from face data

        Features include:
        - Normalized pupil positions
        - Eye corner positions
        - Inter-pupillary distance
        - Eye aspect ratios
        - Iris diameters
        - Relative pupil positions within eyes

        Args:
            face_data: Face data dictionary from FaceDetector

        Returns:
            Feature vector as numpy array
        """
        features = []

        # Frame dimensions for normalization
        w = face_data['frame_width']
        h = face_data['frame_height']

        # 1. Normalized pupil positions
        left_pupil = face_data['left_pupil']
        right_pupil = face_data['right_pupil']

        features.extend([
            left_pupil[0] / w,   # Left pupil X (normalized)
            left_pupil[1] / h,   # Left pupil Y (normalized)
            right_pupil[0] / w,  # Right pupil X (normalized)
            right_pupil[1] / h   # Right pupil Y (normalized)
        ])

        # 2. Inter-pupillary distance (normalized)
        ipd = face_data['interpupillary_distance']
        features.append(ipd / w)

        # 3. Eye corner positions (normalized)
        left_eye = face_data['left_eye']
        right_eye = face_data['right_eye']

        if len(left_eye) >= 2:
            # Inner and outer corners of left eye
            features.extend([
                left_eye[0][0] / w,  # Left eye inner corner X
                left_eye[0][1] / h,  # Left eye inner corner Y
                left_eye[3][0] / w,  # Left eye outer corner X
                left_eye[3][1] / h   # Left eye outer corner Y
            ])
        else:
            features.extend([0, 0, 0, 0])

        if len(right_eye) >= 2:
            # Inner and outer corners of right eye
            features.extend([
                right_eye[0][0] / w,  # Right eye inner corner X
                right_eye[0][1] / h,  # Right eye inner corner Y
                right_eye[3][0] / w,  # Right eye outer corner X
                right_eye[3][1] / h   # Right eye outer corner Y
            ])
        else:
            features.extend([0, 0, 0, 0])

        # 4. Eye aspect ratios (measure of eye openness)
        left_ear = self._calculate_eye_aspect_ratio(left_eye)
        right_ear = self._calculate_eye_aspect_ratio(right_eye)
        features.extend([left_ear, right_ear])

        # 5. Iris diameters (normalized)
        left_iris_diameter = self._calculate_iris_diameter(face_data['left_iris'])
        right_iris_diameter = self._calculate_iris_diameter(face_data['right_iris'])
        features.extend([left_iris_diameter / w, right_iris_diameter / w])

        # 6. Relative pupil position within eye (gaze direction indicator)
        left_relative = self._calculate_relative_pupil_position(
            left_pupil, left_eye
        )
        right_relative = self._calculate_relative_pupil_position(
            right_pupil, right_eye
        )
        features.extend([left_relative[0], left_relative[1],
                        right_relative[0], right_relative[1]])

        # 7. Pupil distance from eye center
        left_offset = self._calculate_pupil_offset(left_pupil, left_eye)
        right_offset = self._calculate_pupil_offset(right_pupil, right_eye)
        features.extend([left_offset / w, right_offset / w])

        return np.array(features, dtype=np.float32)

    def _calculate_eye_aspect_ratio(self, eye_landmarks: List) -> float:
        """
        Calculate Eye Aspect Ratio (EAR) - measure of eye openness
        """
        if len(eye_landmarks) < 6:
            return 0.0

        # Vertical distances
        v1 = np.linalg.norm(np.array(eye_landmarks[1]) - np.array(eye_landmarks[5]))
        v2 = np.linalg.norm(np.array(eye_landmarks[2]) - np.array(eye_landmarks[4]))

        # Horizontal distance
        h = np.linalg.norm(np.array(eye_landmarks[0]) - np.array(eye_landmarks[3]))

        if h == 0:
            return 0.0

        ear = (v1 + v2) / (2.0 * h)
        return ear

    def _calculate_iris_diameter(self, iris_landmarks: List) -> float:
        """
        Calculate iris diameter from iris landmarks
        """
        if len(iris_landmarks) < 2:
            return 0.0

        x_coords = [p[0] for p in iris_landmarks]
        y_coords = [p[1] for p in iris_landmarks]

        width = max(x_coords) - min(x_coords)
        height = max(y_coords) - min(y_coords)

        # Average diameter
        diameter = (width + height) / 2.0
        return diameter

    def _calculate_relative_pupil_position(self, pupil: tuple,
                                          eye_landmarks: List) -> tuple:
        """
        Calculate pupil position relative to eye bounding box
        Returns (x, y) in range [0, 1]
        """
        if len(eye_landmarks) < 2:
            return (0.5, 0.5)

        x_coords = [p[0] for p in eye_landmarks]
        y_coords = [p[1] for p in eye_landmarks]

        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)

        if max_x - min_x == 0 or max_y - min_y == 0:
            return (0.5, 0.5)

        rel_x = (pupil[0] - min_x) / (max_x - min_x)
        rel_y = (pupil[1] - min_y) / (max_y - min_y)

        # Clamp to [0, 1]
        rel_x = max(0.0, min(1.0, rel_x))
        rel_y = max(0.0, min(1.0, rel_y))

        return (rel_x, rel_y)

    def _calculate_pupil_offset(self, pupil: tuple, eye_landmarks: List) -> float:
        """
        Calculate distance of pupil from eye center
        """
        if len(eye_landmarks) < 2:
            return 0.0

        # Calculate eye center
        x_coords = [p[0] for p in eye_landmarks]
        y_coords = [p[1] for p in eye_landmarks]

        center_x = np.mean(x_coords)
        center_y = np.mean(y_coords)

        # Distance from center
        dx = pupil[0] - center_x
        dy = pupil[1] - center_y
        distance = np.sqrt(dx**2 + dy**2)

        return distance

    def get_feature_dimension(self) -> int:
        """
        Get total number of features
        """
        # Based on extract_features implementation:
        # 4 (pupil pos) + 1 (IPD) + 8 (eye corners) + 2 (EAR) +
        # 2 (iris diameter) + 4 (relative pupil) + 2 (pupil offset)
        return 23
