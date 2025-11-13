import React, { useState, useEffect } from 'react';
import './GridTask.css';
import BullseyeTarget from './BullseyeTarget';
import { generate49PointGrid, randomizeFromCenter } from '../utils/gridUtils';

/**
 * Large Grid Task - 49-point grid (7×7)
 * Per whitepaper Section 5.1:
 * - 49 white targets on mid-grey background
 * - Random order, starting from center
 * - Desktop: Click target WHILE fixating
 * - 10-second timeout per target
 * - Tests full-screen accuracy across wider areas
 */
function LargeGrid({ onComplete }) {
  const [gridPoints] = useState(() => {
    const points = generate49PointGrid(window.innerWidth, window.innerHeight);
    return randomizeFromCenter(points);
  });

  const [currentPointIndex, setCurrentPointIndex] = useState(0);
  const [collectedData, setCollectedData] = useState([]);
  const [timeoutWarning, setTimeoutWarning] = useState(false);

  const TIMEOUT_DURATION = 10000; // 10 seconds

  useEffect(() => {
    if (currentPointIndex < gridPoints.length) {
      // Start timeout for current target
      const timer = setTimeout(() => {
        setTimeoutWarning(true);
        // Show warning for 2 seconds, then auto-advance
        setTimeout(() => {
          handleTimeout();
        }, 2000);
      }, TIMEOUT_DURATION);

      return () => clearTimeout(timer);
    }
  }, [currentPointIndex]);

  const handleTimeout = () => {
    // Participant didn't click/fixate in time
    const excludedSample = {
      targetIndex: currentPointIndex,
      target: gridPoints[currentPointIndex],
      timestamp: Date.now(),
      excluded: true,
      reason: 'timeout'
    };

    setCollectedData([...collectedData, excludedSample]);
    setTimeoutWarning(false);

    if (currentPointIndex < gridPoints.length - 1) {
      setCurrentPointIndex(currentPointIndex + 1);
    } else {
      completeTask();
    }
  };

  const handleTargetClick = () {
    // Simulate checking if user is fixating
    const simulatedFixating = true; // Would check real gaze position

    if (!simulatedFixating) {
      const excludedSample = {
        targetIndex: currentPointIndex,
        target: gridPoints[currentPointIndex],
        timestamp: Date.now(),
        excluded: true,
        reason: 'no_fixation'
      };
      setCollectedData([...collectedData, excludedSample]);
    } else {
      const validSample = {
        targetIndex: currentPointIndex,
        target: gridPoints[currentPointIndex],
        timestamp: Date.now(),
        excluded: false,
        gazeData: {
          x: gridPoints[currentPointIndex].x,
          y: gridPoints[currentPointIndex].y
        }
      };
      setCollectedData([...collectedData, validSample]);
    }

    setTimeoutWarning(false);

    if (currentPointIndex < gridPoints.length - 1) {
      setCurrentPointIndex(currentPointIndex + 1);
    } else {
      completeTask();
    }
  };

  const completeTask = () => {
    onComplete({
      taskType: 'large_grid',
      samples: collectedData,
      totalTargets: gridPoints.length,
      validSamples: collectedData.filter(s => !s.excluded).length
    });
  };

  if (currentPointIndex >= gridPoints.length) {
    return null;
  }

  const currentPoint = gridPoints[currentPointIndex];

  return (
    <div className="grid-task" style={{ background: '#898989' }}>
      <div className="task-header">
        <h2>Large Grid Task</h2>
        <p>Click each target while looking directly at it</p>
      </div>

      <div className="task-progress">
        Target {currentPointIndex + 1} of {gridPoints.length}
      </div>

      <BullseyeTarget
        x={currentPoint.x}
        y={currentPoint.y}
        color="white"
        backgroundColor="#898989"
        onClick={handleTargetClick}
      />

      {timeoutWarning && (
        <div className="timeout-warning">
          <p>⏱️ Time's up! Moving to next target...</p>
        </div>
      )}

      <div className="task-instructions">
        Click the target • {currentPointIndex + 1}/{gridPoints.length}
      </div>
    </div>
  );
}

export default LargeGrid;
