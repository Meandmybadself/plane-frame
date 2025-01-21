# Plane Frame

A Python application that tracks nearby aircraft using ADS-B data and displays flight information on an e-ink display.

## Project Structure
```
planeframe/
├── src/                    # Source code
│   ├── planeframe/        # Main package
│   │   ├── __init__.py
│   │   ├── display/       # Display-related modules
│   │   ├── tracking/      # Aircraft tracking modules
│   │   ├── utils/         # Utility functions
│   │   └── config.py      # Configuration management
├── data/                  # Data files (airports, etc.)
├── images/                # Image assets
├── tests/                 # Test files
├── scripts/              # Utility scripts
├── requirements.txt      # Production dependencies
└── requirements.dev.txt  # Development dependencies
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements.dev.txt  # For development
```

3. Copy `.env.example` to `.env` and configure your settings:
```bash
cp .env.example .env
```

4. Run the application:
```bash
python -m planeframe
```

## Development

### Processing of data.

#### Airports
Airport data is processed using the following script:
```bash
node data-processing/airports/airports.js
```

#### Airlines
Airline data is processed using the following script:
```bash
node data-processing/airlines/index.js
```

- Format code: `black src/`
- Check types: `mypy src/`

## APIs
- [ADSB.lol](https://adsb.lol/)

## Data
* Uses airport data from https://github.com/davidmegginson/ourairports-data
* Uses airline data from https://github.com/elmoallistair/datasets/blob/main/airlines.csv 

### Install
```
pip install -r requirements.dev.txt
```

### Run
```
watch_test_image_gen.sh
```

