"""
Simple Flask web server for eye-tracking demo
Access via browser at http://localhost:5000
"""
from flask import Flask, render_template, Response, jsonify
from flask_cors import CORS
import cv2
import json
import numpy as np
from core.face_detection import FaceDetector

app = Flask(__name__)
CORS(app)

# Initialize components
face_detector = FaceDetector()
camera = None

def get_camera():
    """Get or initialize camera"""
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    return camera

def generate_frames():
    """Generate video frames with face detection"""
    while True:
        cam = get_camera()
        success, frame = cam.read()

        if not success:
            break

        # Detect face
        face_data = face_detector.detect(frame)

        # Draw landmarks
        if face_data is not None:
            frame = face_detector.draw_landmarks(frame, face_data)

        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    """Main page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>RealEye Eye Tracking Demo</title>
        <style>
            body {
                margin: 0;
                padding: 20px;
                background: #1a1a1a;
                color: white;
                font-family: Arial, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            h1 {
                color: #4CAF50;
            }
            .container {
                max-width: 1280px;
                background: #2a2a2a;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }
            #videoFeed {
                width: 100%;
                max-width: 1280px;
                border: 3px solid #4CAF50;
                border-radius: 8px;
            }
            .info {
                margin-top: 20px;
                padding: 15px;
                background: rgba(76, 175, 80, 0.1);
                border-left: 4px solid #4CAF50;
                border-radius: 4px;
            }
            .status {
                margin-top: 10px;
                padding: 10px;
                background: #333;
                border-radius: 4px;
                font-family: monospace;
            }
            .instructions {
                margin-top: 20px;
                line-height: 1.6;
            }
            .instructions li {
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>👁️ RealEye Eye-Tracking Demo</h1>

            <img id="videoFeed" src="/video_feed" alt="Video Feed">

            <div class="info">
                <strong>Status:</strong> Live eye tracking active
                <div class="status" id="status">
                    Detecting face and eyes...
                </div>
            </div>

            <div class="instructions">
                <h3>What you're seeing:</h3>
                <ul>
                    <li><strong>Green circles</strong> on your pupils - pupil tracking</li>
                    <li><strong>Blue outlines</strong> around eyes - eye region detection</li>
                    <li><strong>Yellow outlines</strong> on iris - iris tracking</li>
                </ul>

                <h3>Next steps:</h3>
                <ul>
                    <li>For full calibration, open <code>frontend/</code> in browser</li>
                    <li>For Python integration, see <code>backend/main.py</code></li>
                    <li>Check <code>QUICKSTART.md</code> for detailed instructions</li>
                </ul>
            </div>
        </div>

        <script>
            // Update status periodically
            setInterval(() => {
                const status = document.getElementById('status');
                const time = new Date().toLocaleTimeString();
                status.innerHTML = `Running at ${time}<br>FPS: ~30 | Resolution: 1280×720`;
            }, 1000);
        </script>
    </body>
    </html>
    """

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status')
def status():
    """Get current status"""
    return jsonify({
        'status': 'running',
        'camera': 'active' if camera is not None else 'inactive'
    })

@app.route('/api/face-position')
def face_position():
    """Get current face position and bounding box"""
    cam = get_camera()
    success, frame = cam.read()

    if not success:
        return jsonify({
            'detected': False,
            'error': 'Failed to read camera frame'
        }), 500

    # Detect face
    face_data = face_detector.detect(frame)

    if face_data is None:
        return jsonify({
            'detected': False
        })

    # Return face bounding box and other position data
    return jsonify({
        'detected': True,
        'bbox': face_data['face_bbox'],
        'frame_width': face_data['frame_width'],
        'frame_height': face_data['frame_height'],
        'left_pupil': {
            'x': face_data['left_pupil'][0],
            'y': face_data['left_pupil'][1]
        },
        'right_pupil': {
            'x': face_data['right_pupil'][0],
            'y': face_data['right_pupil'][1]
        },
        'interpupillary_distance': face_data['interpupillary_distance']
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 RealEye Eye-Tracking Web Demo")
    print("=" * 60)
    print()
    print("📡 Starting server at http://localhost:5000")
    print()
    print("👁️  Open your browser and navigate to:")
    print("   http://localhost:5000")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60)

    app.run(host='0.0.0.0', port=5000, debug=False)
