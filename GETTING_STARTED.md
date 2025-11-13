# Getting Started with RealEye Eye-Tracking System

## Quick Start

### Prerequisites
- Python 3.8+ (for backend)
- Node.js 16+ and npm (for frontend)
- Webcam (1920×1080 recommended)
- Modern browser (Chrome, Firefox, or Safari)

### Backend Setup

1. **Create a virtual environment** (recommended):
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the backend**:
```bash
python main.py
```

This will start the OpenCV-based eye tracking demo. Press 'c' to calibrate and 'q' to quit.

### Frontend Setup

1. **Install dependencies**:
```bash
cd frontend
npm install
```

2. **Start development server**:
```bash
npm start
```

The app will open at http://localhost:3000

## Usage Flow

### 1. Camera Permission
- Click "Grant Camera Access"
- Allow browser to access your webcam

### 2. Calibration (39 points)
- Follow the pulsating targets
- Click each target when it appears
- Targets will cycle through 3 background colors
- Takes about 2-3 minutes

### 3. Validation
- Look at each validation target
- Targets will "explode" when your gaze is detected
- If validation fails, calibration restarts

### 4. Eye Tracking
- Your gaze is now being tracked in real-time
- A small red dot shows your current gaze position
- Move your eyes around to test

### 5. Results
- View statistics (total points, duration, fixations)
- See gaze heatmap
- Export data for analysis

## Project Structure

```
seebeam/
├── backend/               # Python backend
│   ├── core/             # Video capture, face detection
│   ├── models/           # Gaze estimation, fixation detection
│   ├── calibration/      # Calibration logic
│   ├── utils/            # Accuracy testing, data export
│   └── main.py           # Entry point
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/  # UI components
│   │   └── App.js       # Main app
│   └── package.json
└── docs/                 # Documentation
```

## Calibration Tips

### For Best Results:
1. **Sit at a comfortable distance** from the screen (50-70cm)
2. **Ensure good lighting** - avoid backlighting or glare
3. **Keep your head still** during calibration
4. **Look directly at each target** - not near it, but at the center
5. **Click when ready** - don't rush

### Common Issues:
- **"No face detected"**: Check lighting and camera angle
- **"Recalibrate" warning**: You moved your head too much
- **Low accuracy**: Try recalibrating with better lighting
- **Validation fails**: Ensure you're looking directly at targets

## Backend-Only Testing

If you want to test just the backend without the React frontend:

```bash
cd backend
python main.py
```

This opens an OpenCV window showing:
- Real-time face/eye landmark detection
- Pupil positions highlighted
- Current tracking status

Press 'c' to calibrate (note: calibration in this mode is simplified).

## Advanced Usage

### Custom Calibration Points
Edit `backend/calibration/calibrator.py` to change the number or position of calibration points.

### Adjust Fixation Parameters
Edit `backend/models/fixation_detector.py`:
```python
fixation_detector = FixationDetector(
    min_duration=100,        # Minimum fixation duration (ms)
    velocity_threshold=150,  # Velocity threshold (%/s)
    noise_window=200        # Noise reduction window (ms)
)
```

### Export Calibration Model
```python
from models.gaze_estimator import GazeEstimator

estimator = GazeEstimator()
# ... after training ...
estimator.save_model('my_calibration.pkl')
```

### Load Saved Model
```python
estimator.load_model('my_calibration.pkl')
```

## Data Export

The system exports gaze data in RealEye-compatible format:

```json
{
  "timestamp": 10,
  "gazePointX": 45.5,
  "gazePointY": 32.1,
  "fixation": true,
  "fixationId": "fix_001",
  "confidence": 0.87
}
```

## Troubleshooting

### Python Issues
- **ModuleNotFoundError**: Make sure you activated the virtual environment
- **Camera access error**: Check that no other app is using the webcam
- **MediaPipe import error**: Try `pip install --upgrade mediapipe`

### React Issues
- **Port 3000 in use**: Change port with `PORT=3001 npm start`
- **Build errors**: Delete `node_modules` and `package-lock.json`, then `npm install`
- **Camera not working**: Check browser permissions (chrome://settings/content/camera)

### Performance Issues
- Lower resolution in `backend/main.py`: `WebcamCapture(resolution=(1280, 720))`
- Reduce FPS: `WebcamCapture(fps=15)`
- Close other applications using the webcam

## Next Steps

1. **Test Accuracy**: Run validation tests to measure accuracy
2. **Collect Data**: Use for eye-tracking studies
3. **Customize**: Modify calibration or UI for your needs
4. **Contribute**: Help improve the system!

## Support

For issues or questions:
1. Check the documentation in `docs/`
2. Review the whitepaper notes
3. Look at code comments for implementation details

## Performance Benchmarks

Target metrics from RealEye whitepaper:
- Calibration accuracy: ~106px (desktop), ~56px (mobile)
- Full-screen accuracy: ~123px (desktop), ~70px (mobile)
- Success rate: >90%
- Latency: <33ms per frame (30 FPS)

Your results may vary based on:
- Camera quality
- Lighting conditions
- Individual eye characteristics
- Calibration quality
