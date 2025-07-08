#!/usr/bin/env python3
"""
Lightweight Stock Trading Tool for Raspberry Pi
Minimal dependencies version that works without pandas
"""

import sys
import os
import time
import json
import requests
from datetime import datetime, timedelta

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

def check_raspberry_pi_libraries():
    """Check for Raspberry Pi specific libraries"""
    try:
        import platform
        raspberry_pi = platform.machine().startswith('arm')
        if raspberry_pi:
            print("✓ Running on Raspberry Pi")
        else:
            print("⚠ Not running on Raspberry Pi")
    except:
        print("⚠ Could not determine platform")
    
    # Check for smbus
    try:
        import smbus
        print("✓ smbus (I2C library) is available")
        return True
    except ImportError:
        print("⚠ smbus not available - I2C functionality will be disabled")
        return False

class LightweightStockTrader:
    def __init__(self, api_key=None, secret_key=None):
        """Initialize the lightweight stock trader"""
        self.api_key = api_key or os.getenv('ALPACA_API_KEY')
        self.secret_key = secret_key or os.getenv('ALPACA_SECRET_KEY')
        self.base_url = 'https://paper-api.alpaca.markets'
        
        if not self.api_key or not self.secret_key:
            print("Error: Alpaca API credentials not found!")
            print("Please set ALPACA_API_KEY and ALPACA_SECRET_KEY environment variables")
            sys.exit(1)
        
        self.headers = {
            'APCA-API-KEY-ID': self.api_key,
            'APCA-API-SECRET-KEY': self.secret_key
        }
        print("✓ Connected to Alpaca API successfully")

    def get_stock_data(self, symbol, lookback_minutes=60):
        """Get stock data using Alpaca API directly"""
        try:
            end = datetime.utcnow()
            start = end - timedelta(minutes=lookback_minutes)
            
            url = f"{self.base_url}/v2/stocks/{symbol}/bars"
            params = {
                'timeframe': '1Min',
                'start': start.isoformat() + 'Z',
                'end': end.isoformat() + 'Z'
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            if 'bars' in data and data['bars']:
                return data['bars']
            else:
                return []
                
        except Exception as e:
            print(f"Error getting stock data: {e}")
            return []

    def calculate_simple_macd(self, prices, fast=12, slow=26):
        """Calculate simple MACD without pandas"""
        if len(prices) < slow:
            return None, None, None
        
        # Simple EMA calculation
        def ema(data, period):
            alpha = 2.0 / (period + 1)
            ema_values = [data[0]]
            for price in data[1:]:
                ema_values.append(alpha * price + (1 - alpha) * ema_values[-1])
            return ema_values
        
        # Calculate EMAs
        fast_ema = ema(prices, fast)
        slow_ema = ema(prices, slow)
        
        # Calculate MACD line
        macd_line = [fast_ema[i] - slow_ema[i] for i in range(len(slow_ema))]
        
        # Calculate signal line (EMA of MACD)
        signal_line = ema(macd_line, 9)
        
        # Calculate histogram
        histogram = [macd_line[i] - signal_line[i] for i in range(len(signal_line))]
        
        return macd_line[-1], signal_line[-1], histogram[-1]

    def write_to_dac(self, address, value):
        """Write to DAC - handles cases where smbus is not available"""
        try:
            import smbus
            bus = smbus.SMBus(1)
            
            if not 0 <= value <= 4095:
                raise ValueError("Value must be between 0 and 4095")

            upper = (int(value) >> 4) & 0xFF
            lower = (int(value) << 4) & 0xFF

            try:
                bus.write_i2c_block_data(address, 0x40, [upper, lower])
                print(f"✓ Wrote value {value:.2f} to DAC at address 0x{address:X}")
            except Exception as e:
                print(f"Error writing to DAC at 0x{address:X}: {e}")
                
        except ImportError:
            print(f"⚠ DAC write skipped - smbus not available (value would be: {value:.2f})")
        except Exception as e:
            print(f"Error in DAC write: {e}")

    def stream_ticker(self, symbol, interval_seconds=60, lookback_minutes=60):
        """Stream real-time ticker data with simple MACD calculation"""
        print(f"Starting lightweight real-time stream for {symbol}")
        print(f"Interval: {interval_seconds} seconds, Lookback: {lookback_minutes} minutes")
        print("Press Ctrl+C to stop")
        print("-" * 80)
        
        try:
            while True:
                try:
                    bars = self.get_stock_data(symbol, lookback_minutes)
                    
                    if not bars:
                        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | No data for {symbol}")
                    else:
                        # Extract closing prices
                        prices = [float(bar['c']) for bar in bars]
                        current_price = prices[-1]
                        
                        # Calculate MACD
                        macd_value, signal_value, histogram = self.calculate_simple_macd(prices)
                        
                        if macd_value is not None:
                            # Write to DAC
                            self.write_to_dac(0x60, signal_value)
                            self.write_to_dac(0x61, macd_value)
                            
                            # Determine signal
                            if macd_value > signal_value and histogram > 0:
                                signal = "BULLISH"
                            elif macd_value < signal_value and histogram < 0:
                                signal = "BEARISH"
                            else:
                                signal = "NEUTRAL"
                            
                            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
                                  f"{symbol} | Price: ${current_price:.2f} | "
                                  f"MACD: {macd_value:.4f} | Signal: {signal_value:.4f} | "
                                  f"Histogram: {histogram:.4f} | {signal}")
                        else:
                            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
                                  f"{symbol} | Price: ${current_price:.2f} | Insufficient data for MACD")
                    
                    time.sleep(interval_seconds)
                    
                except KeyboardInterrupt:
                    print("\nStreaming stopped by user")
                    break
                except Exception as e:
                    print(f"Error getting data: {e}")
                    time.sleep(interval_seconds)
                    
        except Exception as e:
            print(f"Error in stream_ticker: {e}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Lightweight Stock Trading Tool')
    parser.add_argument('--symbol', default='AAPL', help='Stock symbol to stream (default: AAPL)')
    parser.add_argument('--interval', type=int, default=60, help='Streaming interval in seconds (default: 60)')
    parser.add_argument('--lookback', type=int, default=60, help='Lookback period in minutes (default: 60)')
    
    args = parser.parse_args()
    
    # Check Raspberry Pi libraries
    check_raspberry_pi_libraries()
    
    # Initialize trader
    trader = LightweightStockTrader()
    
    # Start streaming
    trader.stream_ticker(args.symbol, args.interval, args.lookback)

if __name__ == "__main__":
    main() 