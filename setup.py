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
        ("numpy", None),  # Try numpy first as pandas depends on it
        ("pandas", None)  # No lightweight alternative for pandas
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
                
                # Special handling for pandas to avoid compilation
                if package == "pandas":
                    # Try to install pre-compiled wheel first
                    try:
                        wheel_cmd = method + ["--only-binary=all", package]
                        subprocess.check_call(wheel_cmd, timeout=600)  # 10 minute timeout
                        print(f"✓ {package} installed successfully using pre-compiled wheel")
                        installed = True
                        break
                    except subprocess.CalledProcessError:
                        print(f"⚠ Pre-compiled wheel not available for {package}, trying system package...")
                        # Try system package installation
                        try:
                            if package == "pandas":
                                subprocess.check_call(["sudo", "apt-get", "install", "-y", "python3-pandas"])
                                print(f"✓ {package} installed via system package manager")
                                installed = True
                                break
                        except subprocess.CalledProcessError:
                            print(f"⚠ System package installation failed for {package}")
                            continue
                else:
                    # For other packages, try normal installation
                    subprocess.check_call(cmd, timeout=300)  # 5 minute timeout
                    print(f"✓ {package} installed successfully using {' '.join(method)}")
                    installed = True
                    break
                    
            except subprocess.CalledProcessError as e:
                print(f"⚠ Failed to install {package} using {' '.join(method)}: {e}")
                continue
            except subprocess.TimeoutExpired:
                print(f"⚠ Installation of {package} timed out")
                continue
        
        if not installed:
            print(f"✗ Failed to install {package}")
            if package == "pandas":
                print("\nPandas installation failed. Try these solutions:")
                print("1. Use the lightweight alternative: python lightweight_trading.py")
                print("2. Install system pandas: sudo apt-get install python3-pandas")
                print("3. Use pre-compiled wheel: pip install --only-binary=all --user pandas")
                print("4. Increase swap space: sudo dphys-swapfile swapoff && sudo dphys-swapfile set 2048 && sudo dphys-swapfile swapon")
                print("5. Use virtual environment with more memory")
            else:
                print("\nManual installation options:")
                print("1. Install system packages: sudo apt-get install python3-pandas python3-numpy")
                print("2. Use virtual environment: python3 -m venv trading_env && source trading_env/bin/activate")
                print("3. Install with timeout: pip install --user --timeout 600 pandas numpy")
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