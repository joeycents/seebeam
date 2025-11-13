# Dependencies Guide

This document explains all dependencies needed to run the RealEye eye-tracking system.

## 📦 Quick Install

### Option 1: Install Everything (One Command)
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies (if using React app)
cd frontend && npm install
```

### Option 2: Minimal Install (Backend Only)
```bash
# Just the essentials for eye tracking
pip install numpy scipy opencv-python mediapipe scikit-learn
```

---

## 🐍 Python Dependencies

### Required (Core Eye-Tracking)

Located in: `requirements.txt` and `backend/requirements.txt`

| Package | Version | Purpose |
|---------|---------|---------|
| **numpy** | ≥1.24.0 | Numerical computations, array operations |
| **scipy** | ≥1.10.0 | Scientific computing, median filters |
| **opencv-python** | ≥4.8.0 | Video capture, image processing |
| **mediapipe** | ≥0.10.0 | Face/eye detection, iris tracking |
| **scikit-learn** | ≥1.3.0 | Ridge regression for gaze estimation |
| **pandas** | ≥2.0.0 | Data export and manipulation |
| **pillow** | ≥10.0.0 | Image handling |

### Optional (Web Demo)

| Package | Version | Purpose |
|---------|---------|---------|
| **flask** | ≥2.3.0 | Web server for browser demo |
| **flask-cors** | ≥4.0.0 | CORS support for web API |

### Optional (Advanced ML)

| Package | Version | Purpose |
|---------|---------|---------|
| tensorflow | ≥2.13.0 | Deep learning models (future) |
| torch | ≥2.0.0 | PyTorch models (future) |
| onnxruntime | ≥1.15.0 | ONNX model inference (future) |

---

## 📱 Frontend Dependencies (React)

Located in: `frontend/package.json`

### Required

| Package | Version | Purpose |
|---------|---------|---------|
| **react** | ^18.2.0 | UI framework |
| **react-dom** | ^18.2.0 | React DOM rendering |
| **react-scripts** | 5.0.1 | Build tooling |

### Eye-Tracking & ML

| Package | Version | Purpose |
|---------|---------|---------|
| **@tensorflow/tfjs** | ^4.11.0 | Browser ML inference |
| **face-api.js** | ^0.22.2 | Browser face detection |

### Visualization

| Package | Version | Purpose |
|---------|---------|---------|
| **chart.js** | ^4.4.0 | Data visualization |
| **react-chartjs-2** | ^5.2.0 | React wrapper for Chart.js |
| **simpleheat** | ^0.4.0 | Heatmap generation |
| **three** | ^0.157.0 | 3D graphics (animations) |
| **@react-three/fiber** | ^8.15.0 | React Three.js integration |
| **@react-three/drei** | ^9.88.0 | Three.js helpers |

---

## 🔧 System Requirements

### Python
- **Version**: Python 3.8 or higher
- **Check**: `python --version` or `python3 --version`
- **Install**: https://www.python.org/downloads/

### Node.js (for frontend only)
- **Version**: Node.js 16 or higher
- **Check**: `node --version`
- **Install**: https://nodejs.org/

### Hardware
- **Webcam**: Any USB or built-in webcam
- **Recommended**: 1920×1080 resolution
- **Minimum**: 1280×720 resolution

---

## 📥 Installation Methods

### Method 1: Using pip (Python)

**Root directory:**
```bash
pip install -r requirements.txt
```

**Backend directory:**
```bash
cd backend
pip install -r requirements.txt
```

**With virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Method 2: Using npm (Frontend)

```bash
cd frontend
npm install
```

**Alternative package managers:**
```bash
# Using yarn
yarn install

# Using pnpm
pnpm install
```

---

## 🧪 Verify Installation

### Test Python Dependencies
```bash
python -c "
import numpy
import scipy
import cv2
import mediapipe
import sklearn
print('✅ All Python dependencies installed correctly!')
"
```

### Test Frontend Dependencies
```bash
cd frontend
npm list --depth=0
```

---

## 🐛 Troubleshooting

### "No module named 'cv2'"
```bash
pip install opencv-python
# Or try:
pip install opencv-python-headless
```

### "No module named 'mediapipe'"
```bash
# Make sure pip is up to date
pip install --upgrade pip
pip install mediapipe
```

### "command not found: pip"
```bash
# Use pip3 instead
pip3 install -r requirements.txt

# Or install pip
python -m ensurepip --upgrade
```

### npm install fails
```bash
# Clear cache and try again
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Permission errors on Linux
```bash
# Install for current user only
pip install --user -r requirements.txt
```

### MacOS: "clang: error" during pip install
```bash
# Install Xcode Command Line Tools
xcode-select --install
```

---

## 📊 Dependency Sizes

### Python (approximate)
- Minimal install: ~500 MB
- With Flask: ~520 MB
- With TensorFlow: ~2 GB

### Frontend (approximate)
- node_modules: ~300 MB
- Build output: ~2 MB

---

## 🔄 Updating Dependencies

### Python
```bash
pip install --upgrade -r requirements.txt
```

### Frontend
```bash
cd frontend
npm update
```

---

## 📝 Dependency Files Location

```
seebeam/
├── requirements.txt           ← ROOT: Python dependencies (all)
├── backend/
│   └── requirements.txt       ← Backend-specific Python deps
└── frontend/
    ├── package.json           ← Frontend dependencies (npm)
    └── package-lock.json      ← Locked versions (auto-generated)
```

---

## 🎯 Minimal Setup for Quick Testing

If you just want to test the eye tracking without the full web app:

```bash
# Install only these 5 packages
pip install numpy opencv-python mediapipe scikit-learn scipy

# Run the demo
cd backend
python main.py
```

---

## 🚀 Production Deployment

For production deployments, consider:

### Python
```bash
# Generate exact versions
pip freeze > requirements-lock.txt

# Install exact versions
pip install -r requirements-lock.txt
```

### Frontend
```bash
# Build optimized production bundle
cd frontend
npm run build

# Output will be in frontend/build/
```

---

## 📞 Still Having Issues?

1. Check Python version: `python --version` (need 3.8+)
2. Check pip version: `pip --version`
3. Try updating pip: `pip install --upgrade pip`
4. Check Node version: `node --version` (need 16+)
5. Try with virtual environment (see Method 1 above)

---

## ✅ Installation Checklist

- [ ] Python 3.8+ installed
- [ ] pip installed and updated
- [ ] Virtual environment created (optional but recommended)
- [ ] `pip install -r requirements.txt` successful
- [ ] Test import successful: `python -c "import cv2, mediapipe"`
- [ ] Node.js 16+ installed (if using frontend)
- [ ] `npm install` in frontend/ successful (if using frontend)
- [ ] Webcam connected and working

Once all checked, you're ready to run!
