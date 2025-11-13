"""
Face and Eye Detection Module
Uses MediaPipe Face Mesh for landmark detection
"""
import cv2
import numpy as np
import mediapipe as mp
from typing import Optional, Dict, List, Tuple


class FaceDetector:
    """
    Detects faces and extracts eye landmarks using MediaPipe Face Mesh
    """

    # MediaPipe landmark indices for eyes
    LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]  # Key landmarks
    RIGHT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
    LEFT_IRIS_INDICES = [468, 469, 470, 471, 472]
    RIGHT_IRIS_INDICES = [473, 474, 475, 476, 477]

    def __init__(self, min_detection_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5):
        """
        Initialize MediaPipe Face Mesh

        Args:
            min_detection_confidence: Minimum confidence for face detection
            min_tracking_confidence: Minimum confidence for landmark tracking
        """
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,  # Enable iris tracking
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def detect(self, frame: np.ndarray) -> Optional[Dict]:
        """
        Detect face and extract landmarks

        Args:
            frame: Input frame (BGR format)

        Returns:
            Dictionary containing face data or None if no face detected
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process frame
        results = self.face_mesh.process(rgb_frame)

        if not results.multi_face_landmarks:
            return None

        # Get first face (we only track one face)
        face_landmarks = results.multi_face_landmarks[0]

        # Extract relevant landmarks
        h, w = frame.shape[:2]

        face_data = {
            'landmarks': face_landmarks,
            'left_eye': self._extract_eye_landmarks(face_landmarks, self.LEFT_EYE_INDICES, w, h),
            'right_eye': self._extract_eye_landmarks(face_landmarks, self.RIGHT_EYE_INDICES, w, h),
            'left_iris': self._extract_eye_landmarks(face_landmarks, self.LEFT_IRIS_INDICES, w, h),
            'right_iris': self._extract_eye_landmarks(face_landmarks, self.RIGHT_IRIS_INDICES, w, h),
            'frame_width': w,
            'frame_height': h
        }

        # Calculate derived features
        face_data['left_pupil'] = self._calculate_pupil_center(face_data['left_iris'])
        face_data['right_pupil'] = self._calculate_pupil_center(face_data['right_iris'])
        face_data['interpupillary_distance'] = self._calculate_ipd(
            face_data['left_pupil'],
            face_data['right_pupil']
        )

        return face_data

    def _extract_eye_landmarks(self, face_landmarks, indices: List[int],
                               width: int, height: int) -> List[Tuple[float, float]]:
        """
        Extract specific landmark points and convert to pixel coordinates
        """
        landmarks = []
        for idx in indices:
            landmark = face_landmarks.landmark[idx]
            x = landmark.x * width
            y = landmark.y * height
            landmarks.append((x, y))
        return landmarks

    def _calculate_pupil_center(self, iris_landmarks: List[Tuple[float, float]]) -> Tuple[float, float]:
        """
        Calculate pupil center from iris landmarks
        """
        if not iris_landmarks:
            return (0, 0)

        x_coords = [p[0] for p in iris_landmarks]
        y_coords = [p[1] for p in iris_landmarks]

        center_x = np.mean(x_coords)
        center_y = np.mean(y_coords)

        return (center_x, center_y)

    def _calculate_ipd(self, left_pupil: Tuple[float, float],
                       right_pupil: Tuple[float, float]) -> float:
        """
        Calculate inter-pupillary distance
        """
        dx = right_pupil[0] - left_pupil[0]
        dy = right_pupil[1] - left_pupil[1]
        return np.sqrt(dx**2 + dy**2)

    def draw_landmarks(self, frame: np.ndarray, face_data: Dict) -> np.ndarray:
        """
        Draw face landmarks on frame for visualization

        Args:
            frame: Input frame
            face_data: Face data from detect()

        Returns:
            Annotated frame
        """
        annotated_frame = frame.copy()

        # Draw pupils
        left_pupil = face_data['left_pupil']
        right_pupil = face_data['right_pupil']

        cv2.circle(annotated_frame, (int(left_pupil[0]), int(left_pupil[1])),
                   5, (0, 255, 0), -1)
        cv2.circle(annotated_frame, (int(right_pupil[0]), int(right_pupil[1])),
                   5, (0, 255, 0), -1)

        # Draw eye contours
        for eye_landmarks in [face_data['left_eye'], face_data['right_eye']]:
            points = np.array(eye_landmarks, dtype=np.int32)
            cv2.polylines(annotated_frame, [points], True, (255, 0, 0), 1)

        # Draw iris
        for iris_landmarks in [face_data['left_iris'], face_data['right_iris']]:
            points = np.array(iris_landmarks, dtype=np.int32)
            cv2.polylines(annotated_frame, [points], True, (0, 255, 255), 1)

        return annotated_frame

    def __del__(self):
        """
        Cleanup MediaPipe resources
        """
        if hasattr(self, 'face_mesh'):
            self.face_mesh.close()
