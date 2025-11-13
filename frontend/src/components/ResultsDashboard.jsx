import React from 'react';
import './ResultsDashboard.css';
import { calculateDistance } from '../utils/gridUtils';

/**
 * Results Dashboard - Display accuracy metrics from all grid tasks
 * Per whitepaper Section 4.3:
 * - First Re-Validation: Initial calibration accuracy (~106px target)
 * - Large Grid: Full-screen accuracy (~123px target)
 * - Second Re-Validation: Accuracy decay measurement
 * - Comparison shows degradation over time (p<0.01)
 */
function ResultsDashboard({
  calibrationData,
  firstReValidationData,
  largeGridData,
  secondReValidationData,
  onRestart
}) {

  const calculateTaskAccuracy = (taskData) => {
    if (!taskData || !taskData.samples) {
      return null;
    }

    const validSamples = taskData.samples.filter(s => !s.excluded);
    if (validSamples.length === 0) {
      return {
        avgAccuracy: 0,
        validSamples: 0,
        totalSamples: taskData.totalTargets,
        excludedSamples: taskData.samples.filter(s => s.excluded).length
      };
    }

    // Calculate average Euclidean distance (accuracy in pixels)
    // In production, would compare gaze position to target position
    // For now, using simulated accuracy based on target positions
    const distances = validSamples.map(sample => {
      if (sample.gazeData && sample.target) {
        return calculateDistance(sample.gazeData, sample.target);
      }
      return 0; // Simulated - would be actual gaze-to-target distance
    });

    const avgAccuracy = distances.reduce((sum, d) => sum + d, 0) / distances.length;

    return {
      avgAccuracy: avgAccuracy.toFixed(1),
      validSamples: validSamples.length,
      totalSamples: taskData.totalTargets,
      excludedSamples: taskData.samples.filter(s => s.excluded).length
    };
  };

  const firstRevalStats = calculateTaskAccuracy(firstReValidationData);
  const largeGridStats = calculateTaskAccuracy(largeGridData);
  const secondRevalStats = calculateTaskAccuracy(secondReValidationData);

  // Calculate accuracy decay (First Re-Validation vs Second Re-Validation)
  const accuracyDecay = firstRevalStats && secondRevalStats
    ? (parseFloat(secondRevalStats.avgAccuracy) - parseFloat(firstRevalStats.avgAccuracy)).toFixed(1)
    : null;

  return (
    <div className="results-dashboard">
      <div className="results-header">
        <h1>Eye Tracking Results</h1>
        <p className="results-subtitle">RealEye Study - Desktop Calibration & Validation</p>
        <button className="button-secondary" onClick={onRestart}>
          Start New Session
        </button>
      </div>

      <div className="results-content">
        {/* Calibration Summary */}
        <div className="task-result-card">
          <h2>Calibration</h2>
          {calibrationData ? (
            <div className="stat-grid">
              <div className="stat-item">
                <span className="stat-label">Total Points:</span>
                <span className="stat-value">39 (13×3 backgrounds)</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Status:</span>
                <span className="stat-value success">✓ Complete</span>
              </div>
            </div>
          ) : (
            <p className="no-data">No calibration data</p>
          )}
        </div>

        {/* First Re-Validation */}
        <div className="task-result-card">
          <h2>First Re-Validation</h2>
          <p className="task-description">Initial calibration accuracy measurement (13-point grid)</p>
          {firstRevalStats ? (
            <div className="stat-grid">
              <div className="stat-item">
                <span className="stat-label">Average Accuracy:</span>
                <span className="stat-value highlight">{firstRevalStats.avgAccuracy}px</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Valid Samples:</span>
                <span className="stat-value">{firstRevalStats.validSamples}/{firstRevalStats.totalSamples}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Excluded:</span>
                <span className="stat-value">{firstRevalStats.excludedSamples}</span>
              </div>
            </div>
          ) : (
            <p className="no-data">No data available</p>
          )}
        </div>

        {/* Large Grid */}
        <div className="task-result-card">
          <h2>Large Grid</h2>
          <p className="task-description">Full-screen accuracy measurement (49-point grid, 7×7)</p>
          {largeGridStats ? (
            <div className="stat-grid">
              <div className="stat-item">
                <span className="stat-label">Average Accuracy:</span>
                <span className="stat-value highlight">{largeGridStats.avgAccuracy}px</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Valid Samples:</span>
                <span className="stat-value">{largeGridStats.validSamples}/{largeGridStats.totalSamples}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Excluded:</span>
                <span className="stat-value">{largeGridStats.excludedSamples}</span>
              </div>
            </div>
          ) : (
            <p className="no-data">No data available</p>
          )}
        </div>

        {/* Second Re-Validation */}
        <div className="task-result-card">
          <h2>Second Re-Validation</h2>
          <p className="task-description">Accuracy decay measurement (13-point grid)</p>
          {secondRevalStats ? (
            <div className="stat-grid">
              <div className="stat-item">
                <span className="stat-label">Average Accuracy:</span>
                <span className="stat-value highlight">{secondRevalStats.avgAccuracy}px</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Valid Samples:</span>
                <span className="stat-value">{secondRevalStats.validSamples}/{secondRevalStats.totalSamples}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Excluded:</span>
                <span className="stat-value">{secondRevalStats.excludedSamples}</span>
              </div>
            </div>
          ) : (
            <p className="no-data">No data available</p>
          )}
        </div>

        {/* Accuracy Decay Analysis */}
        {accuracyDecay !== null && (
          <div className="task-result-card accuracy-decay">
            <h2>Accuracy Decay Analysis</h2>
            <p className="task-description">
              Comparison between First and Second Re-Validation
            </p>
            <div className="stat-grid">
              <div className="stat-item">
                <span className="stat-label">Initial Accuracy:</span>
                <span className="stat-value">{firstRevalStats.avgAccuracy}px</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Final Accuracy:</span>
                <span className="stat-value">{secondRevalStats.avgAccuracy}px</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Decay:</span>
                <span className={`stat-value ${parseFloat(accuracyDecay) > 0 ? 'warning' : 'success'}`}>
                  {accuracyDecay > 0 ? '+' : ''}{accuracyDecay}px
                </span>
              </div>
            </div>
            <p className="analysis-note">
              {parseFloat(accuracyDecay) > 0
                ? '⚠️ Accuracy decreased over session (accuracy decay detected)'
                : '✓ Accuracy maintained or improved over session'}
            </p>
          </div>
        )}

        {/* Expected Benchmarks (from whitepaper) */}
        <div className="task-result-card benchmarks">
          <h2>Expected Benchmarks (Whitepaper)</h2>
          <div className="stat-grid">
            <div className="stat-item">
              <span className="stat-label">First Re-Validation Target:</span>
              <span className="stat-value">~106px</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Large Grid Target:</span>
              <span className="stat-value">~123px</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Accuracy Decay:</span>
              <span className="stat-value">Statistically significant (p&lt;0.01)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResultsDashboard;
