import React, { useEffect, useRef } from 'react';
import './ResultsDashboard.css';

function ResultsDashboard({ gazeData, onRestart }) {
  const heatmapCanvasRef = useRef(null);

  useEffect(() => {
    if (heatmapCanvasRef.current && gazeData.length > 0) {
      drawHeatmap();
    }
  }, [gazeData]);

  const drawHeatmap = () => {
    const canvas = heatmapCanvasRef.current;
    const ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth * 0.8;
    canvas.height = window.innerHeight * 0.6;

    // Clear canvas
    ctx.fillStyle = '#ecf0f1';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw gaze points
    gazeData.forEach(point => {
      const x = (point.gazePointX / 100) * canvas.width;
      const y = (point.gazePointY / 100) * canvas.height;

      // Draw gradient circle
      const gradient = ctx.createRadialGradient(x, y, 0, x, y, 30);
      gradient.addColorStop(0, 'rgba(255, 0, 0, 0.3)');
      gradient.addColorStop(1, 'rgba(255, 0, 0, 0)');

      ctx.fillStyle = gradient;
      ctx.fillRect(x - 30, y - 30, 60, 60);
    });
  };

  const calculateStatistics = () => {
    if (gazeData.length === 0) {
      return { totalPoints: 0, duration: 0, fixations: 0 };
    }

    const timestamps = gazeData.map(p => p.timestamp);
    const duration = Math.max(...timestamps) - Math.min(...timestamps);
    const fixations = gazeData.filter(p => p.fixation).length;

    return {
      totalPoints: gazeData.length,
      duration: (duration / 1000).toFixed(1),
      fixations: fixations
    };
  };

  const stats = calculateStatistics();

  return (
    <div className="results-dashboard">
      <div className="results-header">
        <h1>Eye Tracking Results</h1>
        <button className="button-secondary" onClick={onRestart}>
          Start New Session
        </button>
      </div>

      <div className="results-content">
        <div className="stats-panel">
          <h2>Statistics</h2>
          <div className="stat-item">
            <span className="stat-label">Total Gaze Points:</span>
            <span className="stat-value">{stats.totalPoints}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Duration:</span>
            <span className="stat-value">{stats.duration}s</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Fixations:</span>
            <span className="stat-value">{stats.fixations}</span>
          </div>
        </div>

        <div className="heatmap-panel">
          <h2>Gaze Heatmap</h2>
          <canvas ref={heatmapCanvasRef} className="heatmap-canvas" />
        </div>
      </div>
    </div>
  );
}

export default ResultsDashboard;
