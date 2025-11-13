"""
RealEye Eye-Tracking System - Main Entry Point
"""
import cv2
import numpy as np
from core.video_capture import WebcamCapture
from core.face_detection import FaceDetector
from models.gaze_estimator import GazeEstimator
from models.fixation_detector import FixationDetector
from calibration.virtual_chinrest import VirtualChinrest


def main():
    """
    Main application entry point
    """
    print("=== RealEye Eye-Tracking System ===")
    print("Initializing components...")

    # Initialize components
    webcam = WebcamCapture(resolution=(1920, 1080), fps=30)
    face_detector = FaceDetector()
    gaze_estimator = GazeEstimator()
    fixation_detector = FixationDetector()
    chinrest = VirtualChinrest()

    print("✓ Components initialized")
    print("\nStarting video capture...")
    print("Press 'q' to quit, 'c' to calibrate")

    calibrated = False

    try:
        while True:
            # Capture frame
            frame = webcam.get_frame()
            if frame is None:
                break

            # Detect face and landmarks
            face_data = face_detector.detect(frame)

            if face_data is not None:
                # Draw face landmarks
                annotated_frame = face_detector.draw_landmarks(frame, face_data)

                if calibrated:
                    # Estimate gaze
                    gaze_point = gaze_estimator.predict(face_data)

                    # Check head position
                    position_status = chinrest.check_position(face_data)

                    if position_status == "OK":
                        # Draw gaze point
                        gaze_x = int(gaze_point[0] * frame.shape[1] / 100)
                        gaze_y = int(gaze_point[1] * frame.shape[0] / 100)
                        cv2.circle(annotated_frame, (gaze_x, gaze_y), 10, (0, 255, 0), -1)
                        cv2.putText(annotated_frame, "Tracking", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    else:
                        cv2.putText(annotated_frame, "RECALIBRATE", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    cv2.putText(annotated_frame, "Press 'c' to calibrate", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            else:
                annotated_frame = frame
                cv2.putText(annotated_frame, "No face detected", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Display frame
            cv2.imshow('RealEye Eye Tracking', annotated_frame)

            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c'):
                print("\n=== Starting Calibration ===")
                print("This will open the web interface for calibration")
                print("Please use the browser-based calibration")
                calibrated = True  # Temporary - will be replaced with actual calibration

    finally:
        webcam.release()
        cv2.destroyAllWindows()
        print("\nShutdown complete")


if __name__ == "__main__":
    main()
