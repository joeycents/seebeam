import React, { useState, useEffect, useRef } from 'react';
import './PositionCheck.css';

/**
 * Pre-calibration position check screen
 * Ensures user is properly positioned before calibration begins:
 * - Face detected
 * - Appropriate distance from screen
 * - Head centered
 * - Eyes visible
 *
 * Shows green dots when position is good (Virtual Chinrest concept)
 */
function PositionCheck({ onPositionConfirmed }) {
  const videoRef = useRef(null);
  const [faceDetected, setFaceDetected] = useState(false);
  const [eyesDetected, setEyesDetected] = useState(false);
  const [distanceOk, setDistanceOk] = useState(false);
  const [positionCentered, setPositionCentered] = useState(false);
  const [showGreenDots, setShowGreenDots] = useState(false);
  const [countdown, setCountdown] = useState(null);

  useEffect(() => {
    // Setup video stream
    if (videoRef.current && window.eyeTrackingStream) {
      videoRef.current.srcObject = window.eyeTrackingStream;
    }

    // Simulate face detection checks
    // In production, this would use actual MediaPipe face detection
    const checkInterval = setInterval(() => {
      // Simulate detection (in real implementation, check actual face landmarks)
      const mockFaceDetected = true; // Would check MediaPipe
      const mockEyesDetected = true; // Would check eye landmarks
      const mockDistance = true; // Would check face size/IPD
      const mockCentered = true; // Would check face position

      setFaceDetected(mockFaceDetected);
      setEyesDetected(mockEyesDetected);
      setDistanceOk(mockDistance);
      setPositionCentered(mockCentered);

      // All checks passed - show green dots and start countdown
      if (mockFaceDetected && mockEyesDetected && mockDistance && mockCentered) {
        setShowGreenDots(true);

        // Start countdown if not already started
        if (countdown === null) {
          setCountdown(5);
        }
      } else {
        setShowGreenDots(false);
        setCountdown(null);
      }
    }, 100);

    return () => clearInterval(checkInterval);
  }, [countdown]);

  // Countdown timer
  useEffect(() => {
    if (countdown !== null && countdown > 0) {
      const timer = setTimeout(() => {
        setCountdown(countdown - 1);
      }, 1000);
      return () => clearTimeout(timer);
    } else if (countdown === 0) {
      // Position held for 5 seconds - proceed to calibration
      onPositionConfirmed();
    }
  }, [countdown, onPositionConfirmed]);

  const allChecksPassed = faceDetected && eyesDetected && distanceOk && positionCentered;

  return (
    <div className="position-check">
      <div className="position-header">
        <h2>Position Your Face</h2>
        <p>Adjust your position until all indicators are green</p>
      </div>

      <div className="video-container">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="position-video"
        />

        {/* Face outline guide */}
        <div className="face-guide">
          <div className={`face-oval ${faceDetected ? 'detected' : ''}`}>
            {/* Eye position indicators (green dots) */}
            {showGreenDots && (
              <>
                <div className="eye-indicator left"></div>
                <div className="eye-indicator right"></div>
              </>
            )}
          </div>
        </div>

        {/* Countdown overlay */}
        {countdown !== null && countdown > 0 && (
          <div className="countdown-overlay">
            <div className="countdown-circle">
              <span className="countdown-number">{countdown}</span>
            </div>
            <p>Hold steady...</p>
          </div>
        )}
      </div>

      <div className="position-checklist">
        <div className={`check-item ${faceDetected ? 'passed' : ''}`}>
          <span className="check-icon">{faceDetected ? '✓' : '○'}</span>
          <span className="check-label">Face detected</span>
        </div>

        <div className={`check-item ${eyesDetected ? 'passed' : ''}`}>
          <span className="check-icon">{eyesDetected ? '✓' : '○'}</span>
          <span className="check-label">Both eyes visible</span>
        </div>

        <div className={`check-item ${distanceOk ? 'passed' : ''}`}>
          <span className="check-icon">{distanceOk ? '✓' : '○'}</span>
          <span className="check-label">Distance from screen OK</span>
        </div>

        <div className={`check-item ${positionCentered ? 'passed' : ''}`}>
          <span className="check-icon">{positionCentered ? '✓' : '○'}</span>
          <span className="check-label">Head centered</span>
        </div>
      </div>

      <div className="position-instructions">
        <h3>Tips for best results:</h3>
        <ul>
          <li>Sit 50-70cm from the screen</li>
          <li>Keep your head still and centered</li>
          <li>Ensure good lighting on your face</li>
          <li>Remove or adjust glasses if needed</li>
          <li>Look directly at the camera</li>
        </ul>
      </div>

      {!allChecksPassed && (
        <div className="position-warning">
          <p>⚠️ Adjust your position to meet all requirements</p>
        </div>
      )}
    </div>
  );
}

export default PositionCheck;
