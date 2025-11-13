# 🚀 HOW TO RUN - Choose Your Option

## ⚠️ Important Note
This eye-tracking system **requires a webcam**. Run this on your **local computer** (not a remote server).

---

## Option 1: Quick Python Demo (Recommended for Testing)

### What You Need
- Python 3.8 or higher
- A webcam
- 5 minutes

### Steps

**1. Clone or download this repository to your local computer**

**2. Install Python dependencies:**
```bash
cd seebeam/backend
pip install numpy scipy opencv-python mediapipe scikit-learn pandas pillow
```

**3. Run the demo:**
```bash
python main.py
```

**4. You'll see:**
- A window with your webcam feed
- Green circles on your pupils
- Eye landmarks highlighted in blue

**5. Controls:**
- Press **'c'** to calibrate (simplified version)
- Press **'q'** to quit

### Expected Output
```
=== RealEye Eye-Tracking System ===
Initializing components...
Camera initialized:
  Resolution: 1920x1080 (requested: 1920x1080)
  FPS: 30 (requested: 30)
✓ Components initialized

Starting video capture...
Press 'q' to quit, 'c' to calibrate
```

---

## Option 2: Full Web Application (Complete Experience)

### What You Need
- Everything from Option 1, plus:
- Node.js 16+ and npm
- 15 minutes

### Steps

**1. Install Node.js** (if you don't have it)
- Download from: https://nodejs.org/
- Choose LTS version

**2. Install frontend dependencies:**
```bash
cd seebeam/frontend
npm install
```

**3. Start the React app:**
```bash
npm start
```

**4. Open browser:**
- The app will automatically open at `http://localhost:3000`
- If not, manually navigate to that URL

**5. Follow the on-screen flow:**
1. **Camera Permission** → Click "Grant Camera Access"
2. **Calibration** → Click each of 39 pulsating targets
3. **Validation** → Look at 3 targets until they explode
4. **Tracking** → Your gaze is now being tracked!
5. **Results** → See heatmap and statistics

### Expected Output
```
Compiled successfully!

You can now view realeye-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.x:3000
```

---

## Option 3: Web-Based Python Demo (Browser UI)

**If you want to see face detection in your browser:**

**1. Install Flask:**
```bash
pip install flask flask-cors
```

**2. Run the web demo:**
```bash
cd seebeam/backend
python web_demo.py
```

**3. Open browser:**
- Navigate to `http://localhost:5000`
- You'll see live face/eye detection with landmarks

---

## 🎯 Which Option Should I Choose?

| Option | Best For | Time | Features |
|--------|----------|------|----------|
| **Option 1: Python Demo** | Quick testing | 5 min | Basic detection, simple UI |
| **Option 2: React Web App** | Full experience | 15 min | 39-point calibration, heatmaps |
| **Option 3: Flask Demo** | Browser testing | 10 min | Face detection in browser |

### Recommendation:
- **Just want to test?** → Option 1
- **Want the full RealEye experience?** → Option 2
- **Want browser-based detection?** → Option 3

---

## 📋 Troubleshooting

### "No webcam found" or "Camera failed to initialize"
```bash
# On Linux, check available cameras:
ls /dev/video*

# On Mac, check Privacy settings:
System Preferences → Security & Privacy → Camera

# On Windows, check Camera app works first
```

### "ModuleNotFoundError: No module named 'cv2'"
```bash
pip install opencv-python
```

### "Permission denied" on Linux
```bash
sudo usermod -a -G video $USER
# Then log out and log back in
```

### React app shows blank page
```bash
# Clear cache and reinstall:
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Port already in use
```bash
# For Python demo, edit main.py and change port
# For React app:
PORT=3001 npm start
```

---

## 💡 Pro Tips

1. **Good Lighting**: Face the light source, avoid backlighting
2. **Camera Position**: Eye level, 50-70cm from screen
3. **Head Stability**: Keep your head still during calibration
4. **Look Directly**: Stare at center of targets, not just near them
5. **First Time**: Do calibration twice for better accuracy

---

## 🔍 Verify Installation

**Test if dependencies are installed:**
```python
python3 -c "import cv2, mediapipe, numpy, sklearn; print('✅ All dependencies OK!')"
```

**Expected output:**
```
✅ All dependencies OK!
```

---

## 📊 What To Expect

### Calibration Accuracy
- Desktop: ~106 pixels
- Mobile: ~56 pixels

### Processing Speed
- 30 FPS real-time tracking
- <33ms latency per frame

### Data Output
- JSON format compatible with RealEye
- CSV export available
- Heatmap visualization

---

## 🎬 Quick Demo Flow

```
Start
  ↓
[Camera Permission] ← Grant access
  ↓
[Calibration] ← Click 39 targets (2-3 minutes)
  ↓
[Validation] ← Look at 3 targets (30 seconds)
  ↓
[Live Tracking] ← Your gaze is tracked!
  ↓
[Results] ← View heatmap & stats
```

---

## 📞 Still Need Help?

1. Check **GETTING_STARTED.md** for detailed setup
2. Check **QUICKSTART.md** for troubleshooting
3. Check **README.md** for architecture overview
4. Look at code comments in `backend/main.py`

---

## 🚀 Ready to Start?

**Absolute quickest path:**
```bash
cd seebeam/backend
pip install opencv-python mediapipe numpy scikit-learn
python main.py
```

That's it! Your webcam should activate and show face tracking.

---

## ✅ Checklist

Before running, make sure you have:
- [ ] Python 3.8+ installed
- [ ] Webcam connected and working
- [ ] Good lighting on your face
- [ ] Downloaded/cloned the repository
- [ ] Installed dependencies

**Now run:** `python backend/main.py` and you're good to go! 👁️
