#!/bin/bash

echo "=========================================="
echo "RealEye Eye-Tracking System - Quick Demo"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -d "backend" ]; then
    echo "Error: Please run this script from the seebeam directory"
    exit 1
fi

echo "Step 1: Installing Python dependencies..."
echo "This may take a few minutes..."
echo ""

python3 -m pip install --user numpy scipy opencv-python mediapipe scikit-learn pandas pillow

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo ""
echo "Step 2: Starting eye-tracking demo..."
echo ""
echo "INSTRUCTIONS:"
echo "  - Make sure your webcam is connected"
echo "  - Press 'c' to start calibration (simplified)"
echo "  - Press 'q' to quit"
echo ""
echo "Starting in 3 seconds..."
sleep 3

cd backend
python3 main.py
