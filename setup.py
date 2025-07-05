#!/usr/bin/env python3
"""
Setup script for Stock Stream MACD Trading Tool
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    requirements = [
        "alpaca_trade_api",
        "pandas", 
        "numpy"
    ]
    
    print("Installing required packages...")
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}: {e}")
            return False
    return True

def create_env_file():
    """Create a .env file template"""
    env_content = """# Alpaca API Credentials
# Get your API keys from: https://app.alpaca.markets/paper/dashboard/overview
ALPACA_API_KEY=your_api_key_here
ALPACA_SECRET_KEY=your_secret_key_here
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✓ Created .env file template")
        print("Please edit .env file with your Alpaca API credentials")
    else:
        print("✓ .env file already exists")

def main():
    print("Setting up Stock Stream MACD Trading Tool...")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        sys.exit(1)
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install requirements
    if install_requirements():
        print("✓ All packages installed successfully")
    else:
        print("✗ Some packages failed to install")
        sys.exit(1)
    
    # Create env file
    create_env_file()
    
    print("\nSetup complete!")
    print("\nNext steps:")
    print("1. Get your Alpaca API keys from: https://app.alpaca.markets/paper/dashboard/overview")
    print("2. Edit the .env file with your API credentials")
    print("3. Run the script: python stock_stream_macd.py --help")

if __name__ == "__main__":
    main() 