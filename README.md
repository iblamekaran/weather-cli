# WeatherCLI 🌤️

A command-line weather lookup tool with caching and retry logic, built in Python.

## Features
- **Geocoding:** Converts city names to latitude/longitude automatically.
- **Live Weather:** Fetches real-time temperature, wind speed, and conditions via Open-Meteo APIs.
- **Smart Caching:** Caches API responses locally for 10 minutes to reduce network calls and speed up repeated lookups.
- **Resilience:** Implements a retry decorator to automatically handle temporary API failures seamlessly.
- **Clean UI:** Displays colorized, readable output in the terminal with user-friendly error messages (no stack traces!).

## Installation

1. Clone this repository or download the files.
2. It's recommended to set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool by passing the name of a city:
```bash
python weather.py Ludhiana
python weather.py "New York"
```

### Example Output
```text
Weather in Ludhiana, India
----------------------------
Temperature: 31.0°C
Wind Speed:  12.5 km/h
Condition:   Partly cloudy
(fetched fresh)
```

## What I Learned Building This
- **API Integration:** Consuming multiple free endpoints (Open-Meteo Geocoding & Weather APIs) and mapping nested JSON data.
- **Decorators (`@retry_once`):** Wrote a custom wrapper to catch HTTP exceptions, introduce a delay, and retry the request once before failing gracefully. 
- **Caching (`json`):** Built a lightweight local JSON cache store to check timestamps and serve cached data if it's less than 10 minutes old.
- **Command Line Parsing (`argparse`):** Handled positional arguments gracefully, even for multi-word cities.
