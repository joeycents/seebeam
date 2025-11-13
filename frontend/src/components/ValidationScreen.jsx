import React, { useState, useEffect } from 'react';
import './ValidationScreen.css';

function ValidationScreen({ calibrationData, onComplete, onFailed }) {
  const [validationPoints] = useState(generateValidationPoints());
  const [currentPoint, setCurrentPoint] = useState(0);
  const [gazePosition, setGazePosition] = useState(null);
  const [isValidating, setIsValidating] = useState(false);

  const VALIDATION_THRESHOLD = 150; // pixels for desktop
  const VALIDATION_TIMEOUT = 5000; // 5 seconds

  function generateValidationPoints() {
    const w = window.innerWidth;
    const h = window.innerHeight;

    // 3 validation points for desktop
    return [
      { x: w * 0.25, y: h * 0.25 },
      { x: w * 0.5, y: h * 0.5 },
      { x: w * 0.75, y: h * 0.75 }
    ];
  }

  useEffect(() => {
    if (isValidating) {
      // Simulate gaze tracking
      const interval = setInterval(() => {
        const point = validationPoints[currentPoint];
        const distance = calculateDistance(gazePosition, point);

        if (distance < VALIDATION_THRESHOLD) {
          // Success - explode and move to next
          handlePointValidated();
        }
      }, 100);

      const timeout = setTimeout(() => {
        // Failed - gaze not detected on target
        onFailed();
      }, VALIDATION_TIMEOUT);

      return () => {
        clearInterval(interval);
        clearTimeout(timeout);
      };
    }
  }, [isValidating, currentPoint, gazePosition]);

  const calculateDistance = (p1, p2) => {
    if (!p1 || !p2) return Infinity;
    const dx = p1.x - p2.x;
    const dy = p1.y - p2.y;
    return Math.sqrt(dx * dx + dy * dy);
  };

  const handlePointValidated = () => {
    if (currentPoint < validationPoints.length - 1) {
      setCurrentPoint(currentPoint + 1);
    } else {
      // All points validated
      onComplete();
    }
  };

  const startValidation = () => {
    setIsValidating(true);
  };

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
          <div className="validation-point"
            style={{
              left: `${validationPoints[currentPoint].x}px`,
              top: `${validationPoints[currentPoint].y}px`
            }}
          >
            <div className="validation-target">
              <div className="swirl-animation"></div>
            </div>
          </div>

          <div className="validation-progress">
            {currentPoint + 1} / {validationPoints.length}
          </div>
        </>
      )}
    </div>
  );
}

export default ValidationScreen;
