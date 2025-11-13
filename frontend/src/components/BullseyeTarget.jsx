import React from 'react';
import './BullseyeTarget.css';

/**
 * Bullseye target as per RealEye whitepaper specifications:
 * - Total diameter: 72 CSS pixels
 * - Inner circle: 24 CSS pixels (clickable area)
 * - Cross: 14x14 CSS pixels in center
 * - Concentric circles (bullseye pattern)
 */
function BullseyeTarget({
  x,
  y,
  color = 'white',
  backgroundColor = '#898989',
  sequence = null,
  onClick = null,
  pulsate = false,
  scale = 1.0
}) {

  return (
    <div
      className="bullseye-target"
      style={{
        left: `${x}px`,
        top: `${y}px`,
        transform: `translate(-50%, -50%) scale(${scale})`
      }}
    >
      {/* Outer circle - 72px diameter */}
      <div
        className={`bullseye-outer ${pulsate ? 'pulsate' : ''}`}
        style={{
          width: '72px',
          height: '72px',
          border: `2px solid ${color}`,
          backgroundColor: backgroundColor
        }}
      >
        {/* Middle ring */}
        <div
          className="bullseye-middle"
          style={{
            width: '48px',
            height: '48px',
            border: `2px solid ${color}`,
            backgroundColor: backgroundColor
          }}
        >
          {/* Inner circle - 24px diameter (clickable) */}
          <div
            className="bullseye-inner"
            style={{
              width: '24px',
              height: '24px',
              backgroundColor: color,
              cursor: onClick ? 'pointer' : 'default'
            }}
            onClick={onClick}
          >
            {/* Cross - 14x14px */}
            <div
              className="bullseye-cross"
              style={{
                color: color === 'white' ? 'black' : 'white'
              }}
            >
              <div className="cross-horizontal"></div>
              <div className="cross-vertical"></div>
            </div>

            {/* Countdown number (for calibration) */}
            {sequence !== null && (
              <span
                className="bullseye-number"
                style={{ color: color === 'white' ? 'black' : 'white' }}
              >
                {sequence}
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default BullseyeTarget;
