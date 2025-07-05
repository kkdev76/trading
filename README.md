# Real-time Stock Ticker with MACD and Trading

A Python tool that streams real-time stock data, calculates MACD indicators, and allows trading through the Alpaca API.

## Features

- 🔄 Real-time stock data streaming
- 📊 MACD (Moving Average Convergence Divergence) calculation
- 💹 Buy/sell orders with limit or market prices
- 🔧 Auto-installation of required dependencies
- 🛡️ Paper trading support (safe for testing)
- 📱 Command-line interface

## Prerequisites

- Python 3.7 or higher
- Alpaca API account (free paper trading available)

## Quick Start

### 1. Setup

```bash
# Run the setup script
python setup.py
```

### 2. Get Alpaca API Keys

1. Go to [Alpaca Markets](https://app.alpaca.markets/paper/dashboard/overview)
2. Create a free account
3. Get your API key and secret key from the dashboard

### 3. Configure API Keys

Edit the `.env` file created by the setup script:

```bash
ALPACA_API_KEY=your_api_key_here
ALPACA_SECRET_KEY=your_secret_key_here
```

Or set environment variables:

```bash
export ALPACA_API_KEY="your_api_key_here"
export ALPACA_SECRET_KEY="your_secret_key_here"
```

## Usage

### Stream Real-time Data with MACD

```bash
# Stream AAPL data every 60 seconds
python stock_stream_macd.py --symbol AAPL --interval 60

# Stream TSLA data every 30 seconds with 30-minute lookback
python stock_stream_macd.py --symbol TSLA --interval 30 --lookback 30
```

### Buy/Sell Orders

```bash
# Buy 10 shares of AAPL at market price
python stock_stream_macd.py --action buy --symbol AAPL --qty 10

# Buy 5 shares of AAPL at $170 limit price
python stock_stream_macd.py --action buy --symbol AAPL --qty 5 --price 170

# Sell 3 shares of TSLA at $250 limit price
python stock_stream_macd.py --action sell --symbol TSLA --qty 3 --price 250
```

### Check Account Information

```bash
python stock_stream_macd.py --action account
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--symbol` | Stock symbol to trade/stream | AAPL |
| `--interval` | Streaming interval in seconds | 60 |
| `--lookback` | Lookback period in minutes | 60 |
| `--action` | Action: stream, buy, sell, account | stream |
| `--qty` | Quantity for buy/sell orders | Required for buy/sell |
| `--price` | Limit price for buy/sell orders | Market order if not specified |
| `--api-key` | Alpaca API key | From environment |
| `--secret-key` | Alpaca secret key | From environment |

## MACD Indicator

The tool calculates and displays:
- **MACD Line**: Difference between 12-period and 26-period EMAs
- **Signal Line**: 9-period EMA of MACD line
- **Histogram**: MACD line minus Signal line
- **Signal**: BULLISH, BEARISH, or NEUTRAL based on MACD position

## Example Output

```
2024-01-15 14:30:00 | AAPL | Price: $185.50 | MACD: 0.0234 | Signal: 0.0189 | Histogram: 0.0045 | BULLISH
2024-01-15 14:31:00 | AAPL | Price: $185.75 | MACD: 0.0241 | Signal: 0.0192 | Histogram: 0.0049 | BULLISH
```

## Safety Notes

- This tool uses Alpaca's paper trading by default (safe for testing)
- Always test with small amounts before live trading
- MACD is a lagging indicator - use with other analysis
- Past performance doesn't guarantee future results

## Troubleshooting

### Python Interpreter Not Found
Make sure Python 3.7+ is installed and in your PATH:
```bash
python --version
# or
python3 --version
```

### Import Errors
Run the setup script to install dependencies:
```bash
python setup.py
```

### API Connection Issues
- Verify your API keys are correct
- Check your internet connection
- Ensure you're using the correct Alpaca environment (paper/live)

## License

This project is for educational purposes. Use at your own risk.

## Support

For issues with:
- Alpaca API: [Alpaca Support](https://alpaca.markets/support/)
- This tool: Check the troubleshooting section above 