import React, { useState } from 'react';
import './CameraPermission.css';

function CameraPermission({ onPermissionGranted }) {
  const [error, setError] = useState(null);
  const [isRequesting, setIsRequesting] = useState(false);

  const requestPermission = async () => {
    setIsRequesting(true);
    setError(null);

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 1920 },
          height: { ideal: 1080 },
          frameRate: { ideal: 30 }
        }
      });

      // Store stream for later use
      window.eyeTrackingStream = stream;

      // Permission granted
      onPermissionGranted();
    } catch (err) {
      console.error('Camera permission error:', err);
      setError(
        'Camera access denied. Please grant camera permission to use eye tracking.'
      );
      setIsRequesting(false);
    }
  };

  return (
    <div className="camera-permission">
      <div className="permission-content">
        <h1>RealEye Eye Tracking</h1>
        <p className="info-text">
          This application uses your webcam to track eye movements.
          We need your permission to access the camera.
        </p>
        <p className="info-text privacy-note">
          <strong>Privacy:</strong> All processing happens locally in your browser.
          No video data is sent to any server.
        </p>

        <button
          className="button-primary"
          onClick={requestPermission}
          disabled={isRequesting}
        >
          {isRequesting ? 'Requesting...' : 'Grant Camera Access'}
        </button>

        {error && <div className="error-message">{error}</div>}

        <div className="requirements">
          <h3>Requirements:</h3>
          <ul>
            <li>Webcam (1920×1080 recommended)</li>
            <li>Good lighting conditions</li>
            <li>Stable head position</li>
            <li>Chrome, Firefox, or Safari browser</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default CameraPermission;
