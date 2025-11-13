import React, { useState, useEffect } from 'react';
import './PulsatingTarget.css';

function PulsatingTarget({ x, y, color, sequence, onClick }) {
  const [scale, setScale] = useState(1.0);
  const [direction, setDirection] = useState(-1); // -1 for shrinking, 1 for growing

  // Pulsating animation: 100% → 70% → 100%
  useEffect(() => {
    const interval = setInterval(() => {
      setScale(prevScale => {
        const newScale = prevScale + direction * 0.02;

        // Reverse direction at boundaries
        if (newScale <= 0.7) {
          setDirection(1);
          return 0.7;
        } else if (newScale >= 1.0) {
          setDirection(-1);
          return 1.0;
        }

        return newScale;
      });
    }, 30); // ~33 FPS

    return () => clearInterval(interval);
  }, [direction]);

  return (
    <div
      className="pulsating-target"
      style={{
        left: `${x}px`,
        top: `${y}px`,
        transform: `translate(-50%, -50%) scale(${scale})`
      }}
    >
      <div
        className="target-outer"
        style={{
          borderColor: color,
          background: `radial-gradient(circle, ${color} 0%, transparent 70%)`
        }}
      >
        <div
          className="target-inner"
          style={{ background: color }}
          onClick={onClick}
        >
          <span className="target-number" style={{ color: color === 'white' ? 'black' : 'white' }}>
            {sequence}
          </span>
        </div>
      </div>
    </div>
  );
}

export default PulsatingTarget;
