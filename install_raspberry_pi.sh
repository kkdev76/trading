#!/bin/bash
# Raspberry Pi Installation Script for Stock Trading Tool

echo "=== Raspberry Pi Stock Trading Tool Installation ==="
echo "This script will install dependencies optimized for Raspberry Pi"
echo ""

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo; then
    echo "⚠ This script is optimized for Raspberry Pi"
    echo "Continue anyway? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update system packages
echo "Updating system packages..."
sudo apt-get update

# Install system Python packages (pre-compiled)
echo "Installing Python packages via system package manager..."
sudo apt-get install -y python3-pip python3-requests

# Try to install numpy via system package manager first
echo "Installing numpy..."
if ! sudo apt-get install -y python3-numpy; then
    echo "⚠ System numpy installation failed, trying pip..."
    pip3 install --user --only-binary=all numpy
fi

# Try to install pandas via system package manager first
echo "Installing pandas..."
if ! sudo apt-get install -y python3-pandas; then
    echo "⚠ System pandas installation failed, trying pip with pre-compiled wheel..."
    pip3 install --user --only-binary=all pandas
fi

# Install alpaca-py
echo "Installing alpaca-py..."
pip3 install --user alpaca-py

# Install Raspberry Pi specific libraries
echo "Installing Raspberry Pi libraries..."
sudo apt-get install -y python3-smbus python3-dev
pip3 install --user RPi.GPIO

# Check installations
echo ""
echo "=== Installation Check ==="
python3 -c "import numpy; print('✓ numpy installed')" 2>/dev/null || echo "✗ numpy not found"
python3 -c "import pandas; print('✓ pandas installed')" 2>/dev/null || echo "✗ pandas not found"
python3 -c "import alpaca; print('✓ alpaca-py installed')" 2>/dev/null || echo "✗ alpaca-py not found"
python3 -c "import smbus; print('✓ smbus installed')" 2>/dev/null || echo "✗ smbus not found"
python3 -c "import RPi.GPIO; print('✓ RPi.GPIO installed')" 2>/dev/null || echo "✗ RPi.GPIO not found"

echo ""
echo "=== Installation Complete ==="
echo ""
echo "If pandas installation failed, you can use the lightweight alternative:"
echo "python3 lightweight_trading.py --symbol AAPL"
echo ""
echo "To run the main script:"
echo "python3 stock_stream_macd.py --symbol AAPL" 