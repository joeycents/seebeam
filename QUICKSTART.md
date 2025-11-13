# Quick Start Guide

## 🚀 Fastest Way to Run (Backend Demo)

### Prerequisites
- Python 3.8+ installed
- Webcam connected
- Linux/Mac (Windows works too with slight modifications)

### Run the Demo

**Option A: One-line command**
```bash
./run_demo.sh
```

**Option B: Manual steps**
```bash
# 1. Install dependencies
pip install numpy scipy opencv-python mediapipe scikit-learn pandas pillow

# 2. Run the demo
cd backend
python main.py
```

### What You'll See

- A window showing your webcam feed
- Green circles on your pupils (if face detected)
- Eye landmarks highlighted
- Status messages at the top

### Controls
- **Press 'c'**: Start calibration (simplified for demo)
- **Press 'q'**: Quit the application

---

## 🌐 Full Web Application (React Frontend)

For the complete calibration experience with the React UI:

### Step 1: Install Node.js
```bash
# Check if Node.js is installed
node --version  # Should be 16+
npm --version
```

### Step 2: Install Frontend Dependencies
```bash
cd frontend
npm install
```

### Step 3: Start the Web App
```bash
npm start
```

The app will open at **http://localhost:3000**

### Web App Features
1. **Camera Permission** - Grant access to your webcam
2. **39-Point Calibration** - Follow pulsating targets through 3 background colors
3. **Validation** - Look at targets until they "explode"
4. **Live Tracking** - See your gaze in real-time
5. **Results** - View heatmap and statistics

---

## 📋 Troubleshooting

### "No webcam found"
- Check webcam is connected
- On Linux: `ls /dev/video*` to see available cameras
- Try closing other apps using the camera (Zoom, Skype, etc.)

### "ModuleNotFoundError: No module named 'cv2'"
```bash
pip install opencv-python
```

### "No module named 'mediapipe'"
```bash
pip install mediapipe
```

### "Port 3000 already in use"
```bash
PORT=3001 npm start
```

### "Camera permission denied" (in browser)
- Click the camera icon in browser address bar
- Allow camera access
- Refresh the page

---

## 🎯 What Each Option Does

### Backend Demo (Python + OpenCV)
- **Pros**: Quick to start, no browser needed, good for testing
- **Cons**: Simplified calibration, no fancy UI
- **Use for**: Testing if eye detection works, debugging

### Web App (React)
- **Pros**: Full calibration system, beautiful UI, data visualization
- **Cons**: Requires Node.js, longer setup
- **Use for**: Actual eye-tracking studies, complete experience

---

## 📊 Testing Accuracy

After calibration, you can test accuracy:

```python
from backend.utils.accuracy import AccuracyTester

tester = AccuracyTester(screen_width=1920, screen_height=1080)
grid_points = tester.generate_13_point_grid()

# Test accuracy at each point
# Expected: ~106px for desktop calibration
```

---

## 💡 Tips for Best Results

1. **Lighting**: Ensure your face is well-lit, avoid backlighting
2. **Distance**: Sit 50-70cm from the screen
3. **Stability**: Keep your head still during calibration
4. **Look Directly**: Stare at the center of each target, not just near it
5. **Camera**: Higher resolution = better accuracy (1920×1080 ideal)

---

## 📦 What's Included

### Backend Modules
- ✅ Video capture (30 FPS)
- ✅ Face/eye detection (MediaPipe)
- ✅ Feature extraction (23 dimensions)
- ✅ Gaze estimation (Ridge regression)
- ✅ Fixation detection (I-VT algorithm)
- ✅ Virtual chinrest
- ✅ Accuracy testing

### Frontend Components
- ✅ Camera permission
- ✅ 39-point calibration
- ✅ Validation screen
- ✅ Live tracking
- ✅ Results dashboard
- ✅ Heatmap visualization

---

## 🔗 Next Steps

1. **Try the Backend Demo** - Run `./run_demo.sh`
2. **Check Face Detection** - Make sure green circles appear on your pupils
3. **Try Web App** - For full calibration experience
4. **Read Documentation** - See GETTING_STARTED.md for details
5. **Customize** - Modify calibration points, thresholds, etc.

---

## 📞 Need Help?

Check these files:
- **GETTING_STARTED.md** - Detailed setup instructions
- **README.md** - Project overview and architecture
- **docs/whitepaper_notes.md** - Implementation details

Happy eye-tracking! 👁️
