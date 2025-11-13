import React, { useState, useEffect } from 'react';
import './GridTask.css';
import BullseyeTarget from './BullseyeTarget';
import { generate13PointGrid, randomizeFromCenter } from '../utils/gridUtils';

/**
 * Re-Validation Task - 13-point grid
 * Per whitepaper Section 5.1:
 * - 13 white targets on mid-grey background
 * - Random order, starting from center
 * - Desktop: Click target WHILE fixating
 * - 10-second timeout per target
 * - If participant doesn't click/fixate → exclude sample
 *
 * This task is performed TWICE:
 * 1. First Re-Validation: Right after calibration (measures initial accuracy)
 * 2. Second Re-Validation: After Large Grid (measures accuracy decay)
 */
function ReValidation({ onComplete, isFirstValidation = true }) {
  const [gridPoints] = useState(() => {
    const points = generate13PointGrid(window.innerWidth, window.innerHeight);
    return randomizeFromCenter(points);
  });

  const [currentPointIndex, setCurrentPointIndex] = useState(0);
  const [collectedData, setCollectedData] = useState([]);
  const [isFixating, setIsFixating] = useState(false);
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
    // Mark sample as excluded and move to next
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

  const handleTargetClick = () => {
    // Simulate checking if user is fixating
    // In production, this would check actual gaze data
    const simulatedFixating = true; // Would check real gaze position

    if (!simulatedFixating) {
      // Didn't fixate while clicking - exclude sample
      const excludedSample = {
        targetIndex: currentPointIndex,
        target: gridPoints[currentPointIndex],
        timestamp: Date.now(),
        excluded: true,
        reason: 'no_fixation'
      };
      setCollectedData([...collectedData, excludedSample]);
    } else {
      // Valid sample - clicked while fixating
      const validSample = {
        targetIndex: currentPointIndex,
        target: gridPoints[currentPointIndex],
        timestamp: Date.now(),
        excluded: false,
        gazeData: {
          // In production, would capture actual gaze position
          x: gridPoints[currentPointIndex].x,
          y: gridPoints[currentPointIndex].y
        }
      };
      setCollectedData([...collectedData, validSample]);
    }

    setTimeoutWarning(false);

    // Move to next target
    if (currentPointIndex < gridPoints.length - 1) {
      setCurrentPointIndex(currentPointIndex + 1);
    } else {
      completeTask();
    }
  };

  const completeTask = () => {
    onComplete({
      taskType: isFirstValidation ? 'first_revalidation' : 'second_revalidation',
      samples: collectedData,
      totalTargets: gridPoints.length,
      validSamples: collectedData.filter(s => !s.excluded).length
    });
  };

  if (currentPointIndex >= gridPoints.length) {
    return null; // Task completed, waiting for onComplete callback
  }

  const currentPoint = gridPoints[currentPointIndex];

  return (
    <div className="grid-task" style={{ background: '#898989' }}>
      <div className="task-header">
        <h2>{isFirstValidation ? 'First Re-Validation' : 'Second Re-Validation'}</h2>
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
        Click the target • 10 seconds per target
      </div>
    </div>
  );
}

export default ReValidation;
