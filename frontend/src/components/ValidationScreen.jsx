import React, { useState, useEffect } from 'react';
import './ValidationScreen.css';
import BullseyeTarget from './BullseyeTarget';

/**
 * Validation screen as per RealEye whitepaper:
 * - Desktop: 3 validation targets
 * - Targets "swirl and explode" when gaze detected
 * - Threshold: 150px (desktop) or 100px (smartphone) from target center
 * - Timeout: 5 seconds - if not detected, show "Try Again"
 */
function ValidationScreen({ calibrationData, onComplete, onFailed }) {
  const [validationPoints] = useState(generateValidationPoints());
  const [currentPoint, setCurrentPoint] = useState(0);
  const [gazePosition, setGazePosition] = useState(null);
  const [isValidating, setIsValidating] = useState(false);
  const [isSwirling, setIsSwirling] = useState(false);
  const [isExploding, setIsExploding] = useState(false);
  const [timeoutId, setTimeoutId] = useState(null);

  const VALIDATION_THRESHOLD = 150; // pixels for desktop (100 for smartphone)
  const VALIDATION_TIMEOUT = 5000; // 5 seconds
  const SWIRL_DURATION = 1000; // 1 second swirl before explosion

  function generateValidationPoints() {
    const w = window.innerWidth;
    const h = window.innerHeight;

    // 3 validation points for desktop (4 for smartphone)
    return [
      { x: w * 0.25, y: h * 0.25 },
      { x: w * 0.5, y: h * 0.5 },
      { x: w * 0.75, y: h * 0.75 }
    ];
  }

  useEffect(() => {
    if (isValidating && !isSwirling && !isExploding) {
      // Simulate gaze tracking - in production, this would use actual gaze data
      const interval = setInterval(() => {
        // For demo purposes, simulate gaze moving toward target over time
        const point = validationPoints[currentPoint];

        // Simulate gaze (in real implementation, this comes from eye tracker)
        // For now, just auto-trigger after 2 seconds for demo
        const simulatedGaze = { x: point.x, y: point.y };
        setGazePosition(simulatedGaze);

        const distance = calculateDistance(simulatedGaze, point);

        if (distance < VALIDATION_THRESHOLD) {
          // Success - start swirl animation
          clearInterval(interval);
          triggerSwirlAndExplode();
        }
      }, 100);

      // Set timeout for failure
      const timeout = setTimeout(() => {
        clearInterval(interval);
        // Failed - gaze not detected on target within 5 seconds
        alert('Validation failed. Please try again and look directly at the targets.');
        onFailed();
      }, VALIDATION_TIMEOUT);

      setTimeoutId(timeout);

      return () => {
        clearInterval(interval);
        clearTimeout(timeout);
      };
    }
  }, [isValidating, currentPoint, isSwirling, isExploding]);

  const calculateDistance = (p1, p2) => {
    if (!p1 || !p2) return Infinity;
    const dx = p1.x - p2.x;
    const dy = p1.y - p2.y;
    return Math.sqrt(dx * dx + dy * dy);
  };

  const triggerSwirlAndExplode = () => {
    // Start swirl animation
    setIsSwirling(true);

    // After 1 second of swirling, trigger explosion
    setTimeout(() => {
      setIsSwirling(false);
      setIsExploding(true);

      // After explosion animation (0.5s), move to next target
      setTimeout(() => {
        setIsExploding(false);
        handlePointValidated();
      }, 500);
    }, SWIRL_DURATION);
  };

  const handlePointValidated = () => {
    if (currentPoint < validationPoints.length - 1) {
      setCurrentPoint(currentPoint + 1);
      setGazePosition(null);
    } else {
      // All points validated
      onComplete();
    }
  };

  const startValidation = () => {
    setIsValidating(true);
  };

  const currentValidationPoint = validationPoints[currentPoint];

  return (
    <div className="validation-screen">
      <div className="validation-header">
        <h2>Validation</h2>
        <p>Look at each target until it explodes</p>
      </div>

      {!isValidating ? (
        <div className="validation-start">
          <button className="button-primary" onClick={startValidation}>
            Start Validation
          </button>
        </div>
      ) : (
        <>
          {!isExploding && (
            <div
              className={`validation-target-container ${isSwirling ? 'swirling' : ''}`}
              style={{
                left: `${currentValidationPoint.x}px`,
                top: `${currentValidationPoint.y}px`
              }}
            >
              <BullseyeTarget
                x={0}
                y={0}
                color="white"
                backgroundColor="#898989"
              />
            </div>
          )}

          {isExploding && (
            <div
              className="explosion-container"
              style={{
                left: `${currentValidationPoint.x}px`,
                top: `${currentValidationPoint.y}px`
              }}
            >
              <div className="explosion"></div>
            </div>
          )}

          <div className="validation-progress">
            Point {currentPoint + 1} / {validationPoints.length}
          </div>
        </>
      )}
    </div>
  );
}

export default ValidationScreen;
