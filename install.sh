#!/bin/bash

# RealEye Eye-Tracking System - Installation Script
# This script installs all dependencies for both backend and frontend

set -e  # Exit on error

echo "=========================================="
echo "RealEye Eye-Tracking System"
echo "Automated Installation Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    print_error "Error: Please run this script from the seebeam directory"
    exit 1
fi

# Step 1: Check Python
echo "Step 1: Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python 3 found: $PYTHON_VERSION"
else
    print_error "Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Step 2: Check pip
echo ""
echo "Step 2: Checking pip installation..."
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version | cut -d' ' -f2)
    print_success "pip found: $PIP_VERSION"
else
    print_error "pip not found. Installing pip..."
    python3 -m ensurepip --upgrade
fi

# Step 3: Install Python dependencies
echo ""
echo "Step 3: Installing Python dependencies..."
echo "This may take a few minutes..."
echo ""

if pip3 install --user -r requirements.txt; then
    print_success "Python dependencies installed successfully"
else
    print_error "Failed to install Python dependencies"
    exit 1
fi

# Step 4: Verify Python installation
echo ""
echo "Step 4: Verifying Python installation..."
if python3 -c "import cv2, mediapipe, numpy, sklearn; print('OK')" &> /dev/null; then
    print_success "Python dependencies verified"
else
    print_warning "Some Python dependencies may not be installed correctly"
fi

# Step 5: Check if user wants frontend
echo ""
read -p "Do you want to install the React frontend? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Check Node.js
    echo ""
    echo "Step 5: Checking Node.js installation..."
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_success "Node.js found: $NODE_VERSION"
    else
        print_error "Node.js not found. Please install Node.js 16+ from https://nodejs.org/"
        exit 1
    fi

    # Install frontend dependencies
    echo ""
    echo "Step 6: Installing frontend dependencies..."
    echo "This may take several minutes..."
    echo ""

    cd frontend
    if npm install; then
        print_success "Frontend dependencies installed successfully"
    else
        print_error "Failed to install frontend dependencies"
        exit 1
    fi
    cd ..
fi

# Final summary
echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
print_success "Backend (Python) dependencies installed"

if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_success "Frontend (React) dependencies installed"
fi

echo ""
echo "Next steps:"
echo ""
echo "  Backend demo:"
echo "    cd backend"
echo "    python3 main.py"
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "  Frontend app:"
    echo "    cd frontend"
    echo "    npm start"
    echo ""
fi

echo "  For more information, see:"
echo "    - RUN_THIS.md"
echo "    - QUICKSTART.md"
echo "    - DEPENDENCIES.md"
echo ""
echo "Happy eye-tracking! 👁️"
echo ""
