#!/usr/bin/env python3
"""
Real-time Stock Ticker with MACD Calculator and Trading Functions
Uses Alpaca API for data and trading
"""

import sys
import subprocess
import importlib
import os
import smbus
import time

def load_env_file():
    """Load environment variables from .env file"""
    env_file = '.env'
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print("✓ Loaded environment variables from .env file")
    else:
        print("⚠ .env file not found")

# Load environment variables first
load_env_file()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        sys.exit(1)

def install_and_import(package):
    """Install and import a package if not already installed with alternatives"""
    # Special handling for alpaca-py package
    import_name = "alpaca" if package == "alpaca-py" else package
    
    # Package alternatives for Raspberry Pi compatibility
    alternatives = {
        "pandas": ["pandas-lite", "pandas"],
        "numpy": ["numpy-lite", "numpy"]
    }
    
    # Try to import the main package first
    try:
        module = importlib.import_module(import_name)
        print(f"✓ {package} is already installed")
        return module
    except ImportError:
        print(f"Installing {package}...")
        
        # Try different installation methods for externally-managed environments
        install_methods = [
            [sys.executable, "-m", "pip", "install", "--user"],
            [sys.executable, "-m", "pip", "install", "--break-system-packages"],
            [sys.executable, "-m", "pip", "install"]
        ]
        
        # Get list of packages to try (main package + alternatives)
        packages_to_try = [package]
        if package in alternatives:
            packages_to_try.extend(alternatives[package])
        
        installed = False
        for pkg in packages_to_try:
            for method in install_methods:
                try:
                    cmd = method + [pkg]
                    print(f"Trying to install {pkg}...")
                    subprocess.check_call(cmd, timeout=300)  # 5 minute timeout
                    print(f"✓ {pkg} installed successfully using {' '.join(method)}")
                    installed = True
                    break
                except subprocess.CalledProcessError as e:
                    print(f"⚠ Failed to install {pkg} using {' '.join(method)}: {e}")
                    continue
                except subprocess.TimeoutExpired:
                    print(f"⚠ Installation of {pkg} timed out (5 minutes)")
                    continue
            
            if installed:
                # Try to import the installed package
                try:
                    if pkg == "pandas-lite":
                        return importlib.import_module("pandas")
                    elif pkg == "numpy-lite":
                        return importlib.import_module("numpy")
                    else:
                        return importlib.import_module(import_name)
                except ImportError:
                    print(f"⚠ Package {pkg} installed but import failed")
                    continue
        
        if not installed:
            print(f"Error installing {package} and alternatives")
            print("\nManual installation options:")
            print("1. Install system packages: sudo apt-get install python3-pandas python3-numpy")
            print("2. Use virtual environment: python3 -m venv trading_env && source trading_env/bin/activate")
            print("3. Install with timeout: pip install --user --timeout 600 pandas numpy")
            print("4. Use lightweight alternatives: pip install --user pandas-lite numpy-lite")
            sys.exit(1)

# Global flags for Raspberry Pi functionality
RASPBERRY_PI_AVAILABLE = False
SMBUS_AVAILABLE = False
GPIO_AVAILABLE = False

def check_raspberry_pi_libraries():
    """Check for Raspberry Pi specific libraries and set global flags"""
    global RASPBERRY_PI_AVAILABLE, SMBUS_AVAILABLE, GPIO_AVAILABLE
    
    # Check if we're on a Raspberry Pi
    try:
        import platform
        RASPBERRY_PI_AVAILABLE = platform.machine().startswith('arm')
    except:
        RASPBERRY_PI_AVAILABLE = False
    
    # Check for smbus
    try:
        import smbus
        SMBUS_AVAILABLE = True
        print("✓ smbus (I2C library) is available")
    except ImportError:
        SMBUS_AVAILABLE = False
        print("⚠ smbus not available - I2C functionality will be disabled")
    
    # Check for RPi.GPIO
    try:
        import RPi.GPIO as GPIO
        GPIO_AVAILABLE = True
        print("✓ RPi.GPIO is available")
    except ImportError:
        GPIO_AVAILABLE = False
        print("⚠ RPi.GPIO not available - GPIO functionality will be disabled")
    
    if RASPBERRY_PI_AVAILABLE:
        print("✓ Running on Raspberry Pi")
    else:
        print("⚠ Not running on Raspberry Pi - hardware features will be simulated")

def setup_environment():
    """Setup the environment and install required packages"""
    print("Setting up environment...")
    check_python_version()
    
    # Install required packages
    packages = ["alpaca-py", "pandas", "numpy"]
    for pkg in packages:
        install_and_import(pkg)
    
    # Check for Raspberry Pi specific libraries
    check_raspberry_pi_libraries()
    
    print("Environment setup complete!")

# Setup environment first
setup_environment()

# Now import the packages
import time
import pandas as pd
import numpy as np
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import argparse

# Global flags for Raspberry Pi functionality
RASPBERRY_PI_AVAILABLE = False
SMBUS_AVAILABLE = False
GPIO_AVAILABLE = False

class StockTrader:
    def __init__(self, api_key=None, secret_key=None, base_url='https://paper-api.alpaca.markets'):
        """Initialize the stock trader with Alpaca API credentials"""
        self.api_key = api_key or os.getenv('ALPACA_API_KEY')
        self.secret_key = secret_key or os.getenv('ALPACA_SECRET_KEY')
        self.base_url = base_url
        
        if not self.api_key or not self.secret_key:
            print("Error: Alpaca API credentials not found!")
            print("Please set ALPACA_API_KEY and ALPACA_SECRET_KEY environment variables")
            print("Or provide them as arguments when initializing StockTrader")
            sys.exit(1)
        
        try:
            self.trading_client = TradingClient(self.api_key, self.secret_key, paper=True)
            self.data_client = StockHistoricalDataClient(self.api_key, self.secret_key)
            print("✓ Connected to Alpaca API successfully")
        except Exception as e:
            print(f"Error connecting to Alpaca API: {e}")
            sys.exit(1)

    def get_macd(self, df, fast=12, slow=26, signal=9):
        """Calculate MACD indicator"""
        df = df.copy()
        df['EMA_fast'] = df['close'].ewm(span=fast, adjust=False).mean()
        df['EMA_slow'] = df['close'].ewm(span=slow, adjust=False).mean()
        df['MACD'] = df['EMA_fast'] - df['EMA_slow']
        df['Signal'] = df['MACD'].ewm(span=signal, adjust=False).mean()
        df['MACD_Histogram'] = df['MACD'] - df['Signal']
        return df[['MACD', 'Signal', 'MACD_Histogram']]

    def write_to_dac(self, address, value):
        """Write to DAC - handles cases where smbus is not available"""
        DAC1_ADDR = 0x60  # A0 pin to GND
        DAC2_ADDR = 0x61  # A0 pin to VCC
        
        # Check if smbus is available using global flag
        if SMBUS_AVAILABLE:
            try:
                import smbus
                bus = smbus.SMBus(1)
                
                if not 0 <= value <= 4095:
                    raise ValueError("Value must be between 0 and 4095")

                upper = (value >> 4) & 0xFF
                lower = (value << 4) & 0xFF

                try:
                    bus.write_i2c_block_data(address, 0x40, [upper, lower])  # 0x40 = write DAC register
                    #print(f"Wrote value {value} to DAC at address 0x{address:X}")
                except Exception as e:
                    print(f"Error writing to DAC at 0x{address:X}: {e}")
                    
            except Exception as e:
                print(f"Error in DAC write: {e}")
        else:
            # smbus not available (not on Raspberry Pi)
            print(f"⚠ DAC write skipped - smbus not available (value would be: {value:.2f})")


    def stream_ticker(self, symbol, interval_seconds=60, lookback_minutes=60):
        """Stream real-time ticker data with MACD calculation"""
        print(f"Starting real-time stream for {symbol}")
        print(f"Interval: {interval_seconds} seconds, Lookback: {lookback_minutes} minutes")
        print("Press Ctrl+C to stop")
        print("-" * 80)
        
        try:
            while True:
                try:
                    end = pd.Timestamp.utcnow()
                    start = end - pd.Timedelta(minutes=lookback_minutes)
                    
                    request_params = StockBarsRequest(
                        symbol_or_symbols=symbol,
                        timeframe=TimeFrame.Minute,
                        start=start,
                        end=end
                    )
                    bars = self.data_client.get_stock_bars(request_params)
                    
                    if bars.df.empty:
                        print(f"{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')} | No data for {symbol}")
                    else:
                        bars_df = bars.df
                        if symbol in bars_df.index.get_level_values(0):
                            bars_df = bars_df.loc[symbol]
                        macd_data = self.get_macd(bars_df)
                        current_price = bars_df['close'].iloc[-1]
                        macd_value = macd_data['MACD'].iloc[-1]
                        signal_value = macd_data['Signal'].iloc[-1]
                        histogram = macd_data['MACD_Histogram'].iloc[-1]
                        
                        #code to write to DAC goes here. only fcn call. 
                        self.write_to_dac(0x60, signal_value)
                        self.write_to_dac(0x61, macd_value)


                        # Determine MACD signal
                        if macd_value > signal_value and histogram > 0:
                            signal = "BULLISH"
                        elif macd_value < signal_value and histogram < 0:
                            signal = "BEARISH"
                        else:
                            signal = "NEUTRAL"
                        
                        print(f"{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')} | "
                              f"{symbol} | Price: ${current_price:.2f} | "
                              f"MACD: {macd_value:.4f} | Signal: {signal_value:.4f} | "
                              f"Histogram: {histogram:.4f} | {signal}")
                    
                    time.sleep(interval_seconds)
                    
                except KeyboardInterrupt:
                    print("\nStreaming stopped by user")
                    break
                except Exception as e:
                    print(f"Error getting data: {e}")
                    time.sleep(interval_seconds)
                    
        except Exception as e:
            print(f"Error in stream_ticker: {e}")

    def buy_stock(self, symbol, qty, limit_price=None):
        """Buy stock with limit or market order"""
        try:
            from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
            
            if limit_price:
                order_data = LimitOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side='buy',
                    time_in_force='gtc',
                    limit_price=limit_price
                )
                order = self.trading_client.submit_order(order_data)
                print(f"✓ Limit buy order submitted for {qty} shares of {symbol} at ${limit_price}")
            else:
                order_data = MarketOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side='buy',
                    time_in_force='day'
                )
                order = self.trading_client.submit_order(order_data)
                print(f"✓ Market buy order submitted for {qty} shares of {symbol}")
            
            return order
        except Exception as e:
            print(f"Error placing buy order: {e}")
            return None

    def sell_stock(self, symbol, qty, limit_price=None):
        """Sell stock with limit or market order"""
        try:
            from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
            
            if limit_price:
                order_data = LimitOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side='sell',
                    time_in_force='gtc',
                    limit_price=limit_price
                )
                order = self.trading_client.submit_order(order_data)
                print(f"✓ Limit sell order submitted for {qty} shares of {symbol} at ${limit_price}")
            else:
                order_data = MarketOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side='sell',
                    time_in_force='day'
                )
                order = self.trading_client.submit_order(order_data)
                print(f"✓ Market sell order submitted for {qty} shares of {symbol}")
            
            return order
        except Exception as e:
            print(f"Error placing sell order: {e}")
            return None

    def get_account_info(self):
        """Get account information"""
        try:
            account = self.trading_client.get_account()
            print(f"Account Status: {account.status}")
            print(f"Buying Power: ${float(account.buying_power):.2f}")
            print(f"Cash: ${float(account.cash):.2f}")
            print(f"Portfolio Value: ${float(account.portfolio_value):.2f}")
            return account
        except Exception as e:
            print(f"Error getting account info: {e}")
            return None

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='Real-time Stock Ticker with MACD and Trading')
    parser.add_argument('--api-key', help='Alpaca API Key')
    parser.add_argument('--secret-key', help='Alpaca Secret Key')
    parser.add_argument('--symbol', default='AAPL', help='Stock symbol to stream (default: AAPL)')
    parser.add_argument('--interval', type=int, default=60, help='Streaming interval in seconds (default: 60)')
    parser.add_argument('--lookback', type=int, default=60, help='Lookback period in minutes (default: 60)')
    parser.add_argument('--action', choices=['stream', 'buy', 'sell', 'account'], default='stream',
                       help='Action to perform (default: stream)')
    parser.add_argument('--qty', type=float, help='Quantity for buy/sell orders')
    parser.add_argument('--price', type=float, help='Limit price for buy/sell orders')
    
    args = parser.parse_args()
    
    # Initialize trader
    trader = StockTrader(api_key=args.api_key, secret_key=args.secret_key)
    
    if args.action == 'stream':
        trader.stream_ticker(args.symbol, args.interval, args.lookback)
    elif args.action == 'buy':
        if not args.qty:
            print("Error: Quantity (--qty) is required for buy orders")
            sys.exit(1)
        trader.buy_stock(args.symbol, args.qty, args.price)
    elif args.action == 'sell':
        if not args.qty:
            print("Error: Quantity (--qty) is required for sell orders")
            sys.exit(1)
        trader.sell_stock(args.symbol, args.qty, args.price)
    elif args.action == 'account':
        trader.get_account_info()

if __name__ == "__main__":
    main() 