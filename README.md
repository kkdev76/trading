# Stock Stream MACD Trading Tool

A real-time stock ticker with MACD (Moving Average Convergence Divergence) calculation and trading functions using the Alpaca API. Includes Raspberry Pi support for hardware integration.

## Features

- Real-time stock data streaming
- MACD indicator calculation
- Trading functionality (buy/sell orders)
- Raspberry Pi hardware integration (I2C DAC output)
- Cross-platform compatibility

## Requirements

### Core Requirements
- Python 3.7 or higher
- Alpaca API credentials
- Internet connection

### Raspberry Pi Requirements (Optional)
- Raspberry Pi (any model)
- I2C enabled
- DAC module (e.g., MCP4725) for analog output
- RPi.GPIO library
- smbus library (usually pre-installed)

## Installation

### Quick Setup
```bash
python setup.py
```

### Manual Setup
1. Install required packages:
```bash
pip install -r requirements.txt
```

2. For Raspberry Pi users, install additional libraries:
```bash
pip install RPi.GPIO
```

3. Create a `.env` file with your Alpaca API credentials:
```
ALPACA_API_KEY=your_api_key_here
ALPACA_SECRET_KEY=your_secret_key_here
```

### Lightweight Alternative (for Raspberry Pi)
If pandas installation fails on Raspberry Pi, use the lightweight version:
```bash
# Install minimal dependencies
pip install --user requests

# Run lightweight version
python lightweight_trading.py --symbol AAPL
```

## Raspberry Pi Setup

### Enable I2C
1. Run `sudo raspi-config`
2. Navigate to "Interface Options" → "I2C"
3. Enable I2C
4. Reboot: `sudo reboot`

### Install Raspberry Pi Libraries
```bash
sudo apt-get update
sudo apt-get install python3-smbus python3-dev
pip install RPi.GPIO
```

### Hardware Connection
Connect your DAC module to the Raspberry Pi:
- VCC to 3.3V
- GND to Ground
- SDA to GPIO2 (Pin 3)
- SCL to GPIO3 (Pin 5)

## Usage

### Basic Streaming
```bash
python stock_stream_macd.py --symbol AAPL
```

### With Custom Parameters
```bash
python stock_stream_macd.py --symbol TSLA --interval 30 --lookback 120
```

### Lightweight Version (for Raspberry Pi)
If the main script fails due to pandas installation issues:
```bash
python lightweight_trading.py --symbol AAPL
```

### Trading Functions
```bash
# Check account info
python stock_stream_macd.py --action account

# Buy stock
python stock_stream_macd.py --action buy --symbol AAPL --qty 1

# Sell stock
python stock_stream_macd.py --action sell --symbol AAPL --qty 1
```

## Command Line Options

- `--symbol`: Stock symbol to track (default: AAPL)
- `--interval`: Update interval in seconds (default: 60)
- `--lookback`: Historical data lookback in minutes (default: 60)
- `--action`: Action to perform (stream/buy/sell/account)
- `--qty`: Quantity for buy/sell orders
- `--price`: Limit price for orders
- `--api-key`: Alpaca API key
- `--secret-key`: Alpaca secret key

## Raspberry Pi Features

### DAC Output
The tool can output MACD and signal values to a DAC module:
- DAC1 (address 0x60): Signal line value
- DAC2 (address 0x61): MACD line value

### Cross-Platform Compatibility
- On Raspberry Pi: Full hardware functionality
- On other systems: Hardware features are simulated with console output

## Troubleshooting

### Common Issues

1. **Import Error for smbus/RPi.GPIO**
   - This is normal on non-Raspberry Pi systems
   - Hardware features will be disabled automatically

2. **I2C Connection Issues**
   - Ensure I2C is enabled in raspi-config
   - Check wiring connections
   - Verify DAC module address

3. **Alpaca API Errors**
   - Verify API credentials in .env file
   - Check internet connection
   - Ensure account has sufficient funds

### Getting Help
- Check the console output for detailed error messages
- Verify all dependencies are installed
- Ensure proper API credentials

## License

This project is open source. Feel free to modify and distribute.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests. 