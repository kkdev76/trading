#!/usr/bin/env python3
"""
Setup script for Stock Stream MACD Trading Tool
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages with fallback alternatives"""
    # Core requirements with alternatives
    requirements = [
        ("alpaca-py", None),  # No alternative for alpaca-py
        ("pandas", "pandas-lite"),  # Lightweight alternative
        ("numpy", "numpy-lite")  # Lightweight alternative
    ]
    
    print("Installing required packages...")
    
    # Try different installation methods for externally-managed environments
    install_methods = [
        [sys.executable, "-m", "pip", "install", "--user"],
        [sys.executable, "-m", "pip", "install", "--break-system-packages"],
        [sys.executable, "-m", "pip", "install"]
    ]
    
    for package, alternative in requirements:
        installed = False
        
        # Try main package first
        for method in install_methods:
            try:
                cmd = method + [package]
                print(f"Trying to install {package}...")
                subprocess.check_call(cmd, timeout=300)  # 5 minute timeout
                print(f"✓ {package} installed successfully using {' '.join(method)}")
                installed = True
                break
            except subprocess.CalledProcessError as e:
                print(f"⚠ Failed to install {package} using {' '.join(method)}: {e}")
                continue
            except subprocess.TimeoutExpired:
                print(f"⚠ Installation of {package} timed out (5 minutes)")
                continue
        
        # If main package failed and alternative exists, try alternative
        if not installed and alternative:
            print(f"Trying alternative package: {alternative}")
            for method in install_methods:
                try:
                    cmd = method + [alternative]
                    subprocess.check_call(cmd, timeout=300)
                    print(f"✓ {alternative} installed successfully as alternative to {package}")
                    installed = True
                    break
                except subprocess.CalledProcessError as e:
                    print(f"⚠ Failed to install {alternative}: {e}")
                    continue
                except subprocess.TimeoutExpired:
                    print(f"⚠ Installation of {alternative} timed out")
                    continue
        
        if not installed:
            print(f"✗ Failed to install {package} and its alternatives")
            print("\nManual installation options:")
            print("1. Install system packages: sudo apt-get install python3-pandas python3-numpy")
            print("2. Use virtual environment: python3 -m venv trading_env && source trading_env/bin/activate")
            print("3. Install with timeout: pip install --user --timeout 600 pandas numpy")
            print("4. Use lightweight alternatives: pip install --user pandas-lite numpy-lite")
            return False
    
    return True
    
    # Handle Raspberry Pi specific libraries
    print("\nChecking for Raspberry Pi specific libraries...")
    
    # Try to install RPi.GPIO if on Raspberry Pi
    try:
        import platform
        if platform.machine().startswith('arm'):
            print("Raspberry Pi detected, attempting to install RPi.GPIO...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "RPi.GPIO"])
                print("✓ RPi.GPIO installed successfully")
            except subprocess.CalledProcessError:
                print("⚠ RPi.GPIO installation failed - this is normal on non-Raspberry Pi systems")
        else:
            print("Not on Raspberry Pi - RPi.GPIO not needed")
    except Exception as e:
        print(f"⚠ Could not determine platform: {e}")
    
    # Note about smbus
    print("Note: smbus is typically pre-installed on Raspberry Pi systems")
    print("If you need I2C functionality, ensure I2C is enabled in raspi-config")
    
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