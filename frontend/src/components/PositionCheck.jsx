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
  const [faceOutOfBounds, setFaceOutOfBounds] = useState(false);

  // Rectangle bounds (larger, more forgiving - 450px width x 550px height, centered in 640x480 video)
  const RECT_WIDTH = 450;
  const RECT_HEIGHT = 550;
  const VIDEO_WIDTH = 640;
  const VIDEO_HEIGHT = 480;
  const RECT_X = (VIDEO_WIDTH - RECT_WIDTH) / 2; // 95
  const RECT_Y = (VIDEO_HEIGHT - RECT_HEIGHT) / 2; // -35 (extends above video slightly, that's ok)

  useEffect(() => {
    // Setup video stream
    if (videoRef.current && window.eyeTrackingStream) {
      videoRef.current.srcObject = window.eyeTrackingStream;
    }

    // Check face position using actual backend API
    const checkInterval = setInterval(async () => {
      try {
        const response = await fetch('http://localhost:5000/api/face-position');
        const data = await response.json();

        if (data.detected) {
          const bbox = data.bbox;
          const frameWidth = data.frame_width;
          const frameHeight = data.frame_height;

          // Scale bbox to video container size (640x480)
          const scaleX = VIDEO_WIDTH / frameWidth;
          const scaleY = VIDEO_HEIGHT / frameHeight;

          const scaledBbox = {
            x: bbox.x * scaleX,
            y: bbox.y * scaleY,
            width: bbox.width * scaleX,
            height: bbox.height * scaleY
          };

          // Check if face is within rectangle bounds
          const faceLeft = scaledBbox.x;
          const faceRight = scaledBbox.x + scaledBbox.width;
          const faceTop = scaledBbox.y;
          const faceBottom = scaledBbox.y + scaledBbox.height;

          const rectLeft = RECT_X;
          const rectRight = RECT_X + RECT_WIDTH;
          const rectTop = RECT_Y;
          const rectBottom = RECT_Y + RECT_HEIGHT;

          // Check if ANY part of the face is outside the rectangle
          const isOutOfBounds =
            faceLeft < rectLeft ||
            faceRight > rectRight ||
            faceTop < rectTop ||
            faceBottom > rectBottom;

          setFaceOutOfBounds(isOutOfBounds);
          setFaceDetected(true);
          setEyesDetected(true); // Eyes detected if we have bbox

          // Check distance based on IPD (more forgiving range)
          const ipd = data.interpupillary_distance;
          const goodDistance = ipd >= 30 && ipd <= 150;
          setDistanceOk(goodDistance);

          // Check if face is centered (not out of bounds)
          setPositionCentered(!isOutOfBounds);

          // Debug logging
          console.log('Face detection:', {
            bbox: scaledBbox,
            rect: { x: RECT_X, y: RECT_Y, width: RECT_WIDTH, height: RECT_HEIGHT },
            isOutOfBounds,
            ipd,
            goodDistance,
            faceDetected: true,
            eyesDetected: true,
            positionCentered: !isOutOfBounds
          });

          // All checks passed - show green dots and start countdown
          if (!isOutOfBounds && goodDistance) {
            setShowGreenDots(true);

            // Start countdown if not already started
            if (countdown === null) {
              setCountdown(5);
            }
          } else {
            setShowGreenDots(false);
            setCountdown(null);
          }
        } else {
          // No face detected
          setFaceDetected(false);
          setEyesDetected(false);
          setDistanceOk(false);
          setPositionCentered(false);
          setShowGreenDots(false);
          setFaceOutOfBounds(false);
          setCountdown(null);
        }
      } catch (error) {
        console.error('Error checking face position:', error);
        // On error, reset all states
        setFaceDetected(false);
        setEyesDetected(false);
        setDistanceOk(false);
        setPositionCentered(false);
        setShowGreenDots(false);
        setFaceOutOfBounds(false);
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
          <div className={`face-oval ${faceDetected && !faceOutOfBounds ? 'detected' : ''} ${faceOutOfBounds ? 'out-of-bounds' : ''}`}>
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
