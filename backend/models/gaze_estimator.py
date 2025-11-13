"""
Gaze Estimation Model
Uses linear regression (Ridge) to predict gaze coordinates from eye features
"""
import numpy as np
from sklearn.linear_model import Ridge
from typing import Optional, Tuple, List, Dict
import pickle
import os


class GazeEstimator:
    """
    Predicts gaze position on screen using linear regression
    """

    def __init__(self, alpha: float = 1.0):
        """
        Initialize gaze estimator

        Args:
            alpha: Ridge regression regularization parameter
        """
        self.model_x = Ridge(alpha=alpha)
        self.model_y = Ridge(alpha=alpha)
        self.is_trained = False
        self.screen_width = 1920
        self.screen_height = 1080

    def train(self, features: List[np.ndarray], targets: List[Tuple[float, float]]):
        """
        Train gaze estimation models

        Args:
            features: List of feature vectors from calibration
            targets: List of (x, y) target coordinates in pixels
        """
        if len(features) == 0 or len(targets) == 0:
            raise ValueError("Training data cannot be empty")

        if len(features) != len(targets):
            raise ValueError("Features and targets must have same length")

        # Convert to numpy arrays
        X = np.array(features)
        y_x = np.array([t[0] for t in targets])
        y_y = np.array([t[1] for t in targets])

        # Train separate models for X and Y coordinates
        print(f"Training gaze models on {len(features)} samples...")
        self.model_x.fit(X, y_x)
        self.model_y.fit(X, y_y)

        self.is_trained = True

        # Calculate training accuracy
        pred_x = self.model_x.predict(X)
        pred_y = self.model_y.predict(X)

        errors = []
        for i in range(len(targets)):
            error = np.sqrt((pred_x[i] - y_x[i])**2 + (pred_y[i] - y_y[i])**2)
            errors.append(error)

        mean_error = np.mean(errors)
        print(f"✓ Training complete. Mean calibration error: {mean_error:.2f} pixels")

    def predict(self, face_data: Dict) -> Tuple[float, float]:
        """
        Predict gaze position from face data

        Args:
            face_data: Face data dictionary from FaceDetector

        Returns:
            (gaze_x, gaze_y) as percentage of screen (0-100)
        """
        if not self.is_trained:
            # Return center of screen if not trained
            return (50.0, 50.0)

        # Import here to avoid circular dependency
        from core.feature_extraction import FeatureExtractor

        extractor = FeatureExtractor()
        features = extractor.extract_features(face_data)

        # Predict coordinates in pixels
        gaze_x_px = self.model_x.predict([features])[0]
        gaze_y_px = self.model_y.predict([features])[0]

        # Convert to percentage
        gaze_x_pct = (gaze_x_px / self.screen_width) * 100
        gaze_y_pct = (gaze_y_px / self.screen_height) * 100

        # Clamp to valid range
        gaze_x_pct = max(0.0, min(100.0, gaze_x_pct))
        gaze_y_pct = max(0.0, min(100.0, gaze_y_pct))

        return (gaze_x_pct, gaze_y_pct)

    def set_screen_dimensions(self, width: int, height: int):
        """
        Set screen dimensions for coordinate conversion

        Args:
            width: Screen width in pixels
            height: Screen height in pixels
        """
        self.screen_width = width
        self.screen_height = height

    def save_model(self, filepath: str):
        """
        Save trained model to file

        Args:
            filepath: Path to save model
        """
        if not self.is_trained:
            raise RuntimeError("Cannot save untrained model")

        model_data = {
            'model_x': self.model_x,
            'model_y': self.model_y,
            'screen_width': self.screen_width,
            'screen_height': self.screen_height
        }

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)

        print(f"✓ Model saved to {filepath}")

    def load_model(self, filepath: str):
        """
        Load trained model from file

        Args:
            filepath: Path to model file
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")

        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)

        self.model_x = model_data['model_x']
        self.model_y = model_data['model_y']
        self.screen_width = model_data['screen_width']
        self.screen_height = model_data['screen_height']
        self.is_trained = True

        print(f"✓ Model loaded from {filepath}")

    def get_model_info(self) -> Dict:
        """
        Get information about trained model

        Returns:
            Dictionary with model information
        """
        if not self.is_trained:
            return {'trained': False}

        return {
            'trained': True,
            'screen_width': self.screen_width,
            'screen_height': self.screen_height,
            'num_features': len(self.model_x.coef_),
            'x_coef_sum': np.sum(np.abs(self.model_x.coef_)),
            'y_coef_sum': np.sum(np.abs(self.model_y.coef_))
        }
