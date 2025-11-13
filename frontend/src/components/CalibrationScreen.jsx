import React, { useState, useEffect, useRef } from 'react';
import './CalibrationScreen.css';
import BullseyeTarget from './BullseyeTarget';

function CalibrationScreen({ onComplete }) {
  const [currentPoint, setCurrentPoint] = useState(0);
  const [calibrationPoints, setCalibrationPoints] = useState([]);
  const [collectedData, setCollectedData] = useState([]);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  // Generate calibration points (39 for desktop)
  useEffect(() => {
    const points = generateCalibrationPoints();
    setCalibrationPoints(points);
  }, []);

  // Setup video stream
  useEffect(() => {
    if (videoRef.current && window.eyeTrackingStream) {
      videoRef.current.srcObject = window.eyeTrackingStream;
    }
  }, []);

  const generateCalibrationPoints = () => {
    const w = window.innerWidth;
    const h = window.innerHeight;
    const margin = { x: w * 0.1, y: h * 0.1 };

    const basePositions = generate13PointGrid(w, h, margin);
    const points = [];
    let sequenceNum = 39;

    // Phase 1: Dark grey background
    basePositions.forEach(pos => {
      points.push({
        x: pos.x,
        y: pos.y,
        background: '#393939',
        targetColor: 'white',
        sequence: sequenceNum--
      });
    });

    // Phase 2: Medium grey background
    basePositions.forEach(pos => {
      points.push({
        x: pos.x,
        y: pos.y,
        background: '#898989',
        targetColor: 'white',
        sequence: sequenceNum--
      });
    });

    // Phase 3: Light grey background
    basePositions.forEach(pos => {
      points.push({
        x: pos.x,
        y: pos.y,
        background: '#CECECE',
        targetColor: 'black',
        sequence: sequenceNum--
      });
    });

    return points;
  };

  const generate13PointGrid = (w, h, margin) => {
    const positions = [];

    // Top row (5 points)
    const y1 = margin.y;
    for (let i = 0; i < 5; i++) {
      const x = margin.x + (w - 2 * margin.x) * i / 4;
      positions.push({ x, y: y1 });
    }

    // Middle row (5 points)
    const y2 = h / 2;
    for (let i = 0; i < 5; i++) {
      const x = margin.x + (w - 2 * margin.x) * i / 4;
      positions.push({ x, y: y2 });
    }

    // Bottom row (3 points)
    const y3 = h - margin.y;
    [0, 2, 4].forEach(i => {
      const x = margin.x + (w - 2 * margin.x) * i / 4;
      positions.push({ x, y: y3 });
    });

    return positions;
  };

  const handleTargetClick = () => {
    // Capture eye data at this moment
    const eyeData = captureEyeData();

    const sample = {
      target: calibrationPoints[currentPoint],
      eyeData,
      timestamp: Date.now()
    };

    setCollectedData([...collectedData, sample]);

    // Move to next point
    if (currentPoint < calibrationPoints.length - 1) {
      setCurrentPoint(currentPoint + 1);
    } else {
      // Calibration complete
      onComplete({
        samples: [...collectedData, sample],
        screenWidth: window.innerWidth,
        screenHeight: window.innerHeight
      });
    }
  };

  const captureEyeData = () => {
    // TODO: Implement actual eye feature extraction
    // For now, return mock data
    return {
      leftPupil: { x: 0, y: 0 },
      rightPupil: { x: 0, y: 0 },
      features: new Array(23).fill(0)
    };
  };

  if (calibrationPoints.length === 0) {
    return <div className="calibration-screen">Loading...</div>;
  }

  const currentCalPoint = calibrationPoints[currentPoint];

  return (
    <div
      className="calibration-screen"
      style={{ background: currentCalPoint.background }}
    >
      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted
        style={{ display: 'none' }}
      />
      <canvas ref={canvasRef} style={{ display: 'none' }} />

      <div className="calibration-progress">
        Point {currentPoint + 1} of {calibrationPoints.length}
      </div>

      <BullseyeTarget
        x={currentCalPoint.x}
        y={currentCalPoint.y}
        color={currentCalPoint.targetColor}
        backgroundColor={currentCalPoint.background}
        sequence={currentCalPoint.sequence}
        onClick={handleTargetClick}
        pulsate={true}
      />

      <div className="calibration-instructions">
        Click each target when it appears
      </div>
    </div>
  );
}

export default CalibrationScreen;
