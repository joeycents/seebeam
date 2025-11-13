import React, { useState, useEffect } from 'react';
import './StudyInterface.css';

function StudyInterface({ calibrationData, onComplete }) {
  const [gazeData, setGazeData] = useState([]);
  const [isTracking, setIsTracking] = useState(false);
  const [currentGaze, setCurrentGaze] = useState({ x: 50, y: 50 });

  useEffect(() => {
    if (isTracking) {
      // Start gaze tracking
      const interval = setInterval(() => {
        // TODO: Implement actual gaze tracking
        // For now, simulate with mouse position
        const gazePoint = {
          timestamp: Date.now(),
          gazePointX: currentGaze.x,
          gazePointY: currentGaze.y,
          fixation: false,
          fixationId: null,
          confidence: 0.85
        };

        setGazeData(prev => [...prev, gazePoint]);
      }, 33); // ~30 FPS

      return () => clearInterval(interval);
    }
  }, [isTracking, currentGaze]);

  const handleStartTracking = () => {
    setIsTracking(true);
  };

  const handleStopTracking = () => {
    setIsTracking(false);
    onComplete(gazeData);
  };

  const handleMouseMove = (e) => {
    const x = (e.clientX / window.innerWidth) * 100;
    const y = (e.clientY / window.innerHeight) * 100;
    setCurrentGaze({ x, y });
  };

  return (
    <div className="study-interface" onMouseMove={handleMouseMove}>
      <div className="study-header">
        <h2>Eye Tracking Active</h2>
        <div className="tracking-stats">
          <span>Data points: {gazeData.length}</span>
          <span>FPS: ~30</span>
        </div>
      </div>

      {!isTracking ? (
        <div className="study-controls">
          <button className="button-primary" onClick={handleStartTracking}>
            Start Tracking
          </button>
        </div>
      ) : (
        <div className="study-controls">
          <button className="button-secondary" onClick={handleStopTracking}>
            Stop & View Results
          </button>
        </div>
      )}

      {/* Gaze overlay (for debugging) */}
      {isTracking && (
        <div
          className="gaze-overlay"
          style={{
            left: `${currentGaze.x}%`,
            top: `${currentGaze.y}%`
          }}
        />
      )}

      <div className="study-content">
        <h1>Sample Content</h1>
        <p>
          This is a demo interface showing eye tracking in action.
          Look around the screen to track your gaze.
        </p>
        <div className="sample-grid">
          <div className="sample-box">Box 1</div>
          <div className="sample-box">Box 2</div>
          <div className="sample-box">Box 3</div>
          <div className="sample-box">Box 4</div>
        </div>
      </div>
    </div>
  );
}

export default StudyInterface;
