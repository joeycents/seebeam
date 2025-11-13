# RealEye Whitepaper - Implementation Notes

## Overview
This document contains implementation notes from the RealEye whitepaper reverse engineering.

## Key Specifications

### Calibration
- **Desktop**: 39 points (13 positions × 3 backgrounds)
- **Mobile**: 27 points (9 positions × 3 backgrounds)
- **Target Size**: 72px total diameter, 24px clickable inner circle
- **Animation**: Pulsating from 100% → 70% → 100%
- **Backgrounds**:
  - Dark grey (#393939) with white targets
  - Medium grey (#898989) with white targets
  - Light grey (#CECECE) with black targets

### Validation
- **Desktop**: 3 validation points
- **Mobile**: 4 validation points
- **Threshold**: 150px (desktop), 100px (mobile)
- **Timeout**: 5 seconds
- **Animation**: Targets "swirl and explode" when gazed at

### Gaze Estimation
- **Algorithm**: Linear Regression (Ridge)
- **Features**: 23-dimensional feature vector
  - Normalized pupil positions
  - Eye corner positions
  - Inter-pupillary distance (IPD)
  - Eye aspect ratios
  - Iris diameters
  - Relative pupil positions
- **Models**: Separate models for X and Y coordinates

### Fixation Detection (I-VT Filter)
- **Min Duration**: 100ms
- **Max Duration**: 3000ms
- **Noise Window**: 200ms (moving median)
- **Velocity Threshold**: 150%/s
- **Max Saccade Duration**: 150ms

### Virtual Chinrest
- **Position Threshold**: 30 pixels
- **Size Threshold**: 20 pixels
- **Alert**: Show recalibration prompt when thresholds exceeded

### Target Accuracy
| Metric | Desktop | Mobile |
|--------|---------|--------|
| Calibration Accuracy | ~106px | ~56px |
| Full-screen Accuracy | ~123px | ~70px |
| Success Rate | >90% | >90% |

## Implementation Status

### ✅ Completed
1. **Core Infrastructure**
   - WebRTC video capture (backend/core/video_capture.py)
   - Face & eye detection with MediaPipe (backend/core/face_detection.py)
   - Feature extraction (backend/core/feature_extraction.py)

2. **Calibration System**
   - 39-point desktop calibration
   - 27-point mobile calibration
   - React calibration UI with pulsating targets
   - Background color cycling

3. **Gaze Estimation**
   - Ridge regression models
   - Feature engineering
   - Model save/load functionality

4. **Fixation Detection**
   - I-VT algorithm implementation
   - Moving median noise reduction
   - Configurable parameters

5. **Virtual Chinrest**
   - Head movement detection
   - Position compensation
   - Recalibration alerts

6. **Accuracy Measurement**
   - Grid-based validation (13-point, 49-point)
   - Multiple accuracy calculation methods
   - Comparison to benchmarks

7. **Web Application**
   - React frontend
   - Camera permission flow
   - Calibration interface
   - Validation screen
   - Study interface
   - Results dashboard with heatmap

### 🚧 TODO (Phase 8: Advanced Features)
1. **Deep Learning Models**
   - CNN-based gaze estimation
   - Transfer learning from pre-trained models
   - ONNX export for browser inference

2. **Optimizations**
   - WebWorker for processing
   - WASM acceleration
   - Reduce latency (<33ms target)

3. **Personal Profiles**
   - Store user calibration data
   - Quick recalibration for returning users
   - Adaptive learning

4. **Advanced UI**
   - Real-time gaze visualization
   - Better heatmap rendering (WebGL)
   - Export data in multiple formats

5. **Browser Integration**
   - Integrate TensorFlow.js for client-side inference
   - Use face-api.js for browser-based face detection
   - Eliminate need for backend

## Technical Decisions

### Why Linear Regression?
Per the whitepaper, linear regression (Ridge) provides good accuracy with low computational cost. More complex models may overfit on limited calibration data.

### Why MediaPipe?
- Real-time performance (30+ FPS)
- Built-in iris tracking
- Cross-platform support
- Free and open-source

### Why React?
- Component-based architecture fits calibration flow
- Large ecosystem for visualization
- Easy to deploy as static site

## Testing Strategy

### Unit Tests
- Test feature extraction with known face data
- Verify calibration point generation
- Test fixation detection algorithm

### Integration Tests
- End-to-end calibration flow
- Gaze prediction accuracy
- Data export formats

### User Studies
- Replicate whitepaper methodology
- Test with diverse participants
- Measure accuracy across conditions

## References
- RealEye Whitepaper (provided by user)
- MediaPipe Face Mesh: https://google.github.io/mediapipe/solutions/face_mesh
- I-VT Algorithm: Salvucci & Goldberg (2000)
