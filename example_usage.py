#!/usr/bin/env python3
"""
Example usage of the StockTrader class
"""

import os
from stock_stream_macd import StockTrader

def main():
    # Example 1: Stream real-time data with MACD
    print("=== Example 1: Streaming Real-time Data ===")
    print("This will stream AAPL data for 5 minutes with 30-second intervals")
    print("Press Ctrl+C to stop early")
    
    # Uncomment the lines below to run the example
    # trader = StockTrader()
    # trader.stream_ticker('AAPL', interval_seconds=30, lookback_minutes=30)
    
    print("\n=== Example 2: Account Information ===")
    # trader = StockTrader()
    # trader.get_account_info()
    
    print("\n=== Example 3: Trading Examples ===")
    print("Note: These are examples - uncomment to run actual trades")
    
    # trader = StockTrader()
    
    # Buy 1 share of AAPL at market price
    # trader.buy_stock('AAPL', 1)
    
    # Buy 2 shares of TSLA at $250 limit price
    # trader.buy_stock('TSLA', 2, 250)
    
    # Sell 1 share of AAPL at $180 limit price
    # trader.sell_stock('AAPL', 1, 180)
    
    print("\nTo run these examples:")
    print("1. Set your Alpaca API credentials in environment variables or .env file")
    print("2. Uncomment the desired lines in this script")
    print("3. Run: python example_usage.py")

if __name__ == "__main__":
    main() 