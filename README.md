# RealEye Eye-Tracking System

A webcam-based eye-tracking system reverse-engineered from the RealEye whitepaper.

## Architecture

- **Backend (Python)**: Core eye-tracking algorithms, face detection, gaze estimation
- **Frontend (React)**: Web interface, calibration UI, real-time visualization

## Features

### Phase 1: Core Infrastructure
- ✅ WebRTC video capture (30+ FPS)
- ✅ Face & eye detection using MediaPipe
- ✅ Real-time landmark extraction

### Phase 2: Calibration System
- 39-point desktop calibration (13 positions × 3 backgrounds)
- 27-point mobile calibration
- Validation step with interactive targets

### Phase 3: Gaze Estimation
- Feature extraction from eye landmarks
- Linear regression model (Ridge)
- Real-time gaze prediction

### Phase 4: Fixation Detection
- I-VT (Velocity-Threshold) filter algorithm
- Moving median noise reduction
- Configurable parameters (min/max duration, velocity threshold)

### Phase 5: Virtual Chinrest
- Head movement detection
- Automatic recalibration alerts
- Gaze position compensation

### Phase 6: Accuracy Measurement
- Grid-based validation tasks
- Multiple accuracy metrics
- Performance benchmarking

### Phase 7: Web Application
- React-based UI
- Real-time gaze overlay
- Heatmap visualization
- Data export

### Phase 8: Advanced Features
- Deep learning models (optional)
- Personal calibration profiles
- Adaptive recalibration

## Target Metrics

| Metric | Desktop | Mobile |
|--------|---------|--------|
| Calibration Accuracy | ~106px | ~56px |
| Full-screen Accuracy | ~123px | ~70px |
| Success Rate | >90% | >90% |
| Processing Latency | <33ms | <33ms |
| Frame Rate | 30 FPS | 30 FPS |

## Installation

### Quick Install (Automated)
```bash
./install.sh
```

### Manual Install

**Backend:**
```bash
pip install -r requirements.txt
cd backend
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

**See also:**
- `DEPENDENCIES.md` - Complete dependency guide
- `requirements.txt` - Python dependencies
- `frontend/package.json` - Frontend dependencies

## Project Structure

```
seebeam/
├── backend/
│   ├── core/
│   │   ├── video_capture.py      # WebRTC video handling
│   │   ├── face_detection.py     # MediaPipe face mesh
│   │   └── feature_extraction.py # Eye feature engineering
│   ├── models/
│   │   ├── gaze_estimator.py     # Linear regression model
│   │   └── fixation_detector.py  # I-VT filter
│   ├── calibration/
│   │   ├── calibrator.py         # Calibration logic
│   │   └── virtual_chinrest.py   # Head movement compensation
│   ├── utils/
│   │   ├── accuracy.py           # Accuracy measurement
│   │   └── data_export.py        # Data formatting
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CameraPermission.jsx
│   │   │   ├── CalibrationScreen.jsx
│   │   │   ├── ValidationScreen.jsx
│   │   │   └── StudyInterface.jsx
│   │   ├── utils/
│   │   │   └── gazeTracking.js
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   └── README.md
└── docs/
    └── whitepaper_notes.md
```

## Technology Stack

### Backend
- **mediapipe**: Face & eye detection
- **opencv-python**: Video processing
- **scikit-learn**: Linear regression models
- **numpy/scipy**: Numerical computations
- **Flask/FastAPI**: Web server (optional)

### Frontend
- **React**: UI framework
- **TensorFlow.js**: Client-side ML inference
- **face-api.js**: Browser-based face tracking
- **Three.js**: 3D animations for calibration
- **Chart.js**: Data visualization

## Calibration Process

### Desktop (39 points)
1. 13 targets on dark grey (#393939) - white targets
2. 13 targets on medium grey (#898989) - white targets
3. 13 targets on light grey (#CECECE) - black targets

### Target Specifications
- Total diameter: 72 CSS pixels
- Inner circle: 24 CSS pixels (clickable area)
- Animation: pulse from 100% → 70% → 100%
- Countdown display: 39→1

### Validation
- 3 validation targets (desktop) or 4 (smartphone)
- Targets "swirl and explode" when gazed at
- Gaze must be within 150px (desktop) or 100px (smartphone)
- Auto-retry if threshold not met for 5 seconds

## Data Format

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

## License

MIT
