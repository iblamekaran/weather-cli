# Weather Dashboard 🌤️

A sleek, modern weather web application built with Python (Flask) and vanilla HTML/CSS/JS. It features a custom API layer with caching and retry logic.

## Features
- **Clean Web UI:** A premium frosted-glass aesthetic (glassmorphism) built with vanilla CSS.
- **Geocoding:** Converts city names to latitude/longitude automatically.
- **Live Weather & Forecasts:** Fetches real-time temperature, wind speed, conditions, and tomorrow's forecast via Open-Meteo APIs.
- **Smart Caching:** Caches API responses locally for 10 minutes to reduce network calls and speed up repeated lookups.
- **Resilience:** Implements a retry decorator to automatically handle temporary API failures seamlessly.

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

Start the Flask web server:
```bash
python app.py
```
Then, open your web browser and navigate to `http://127.0.0.1:5000`.

## What I Learned Building This
- **Web Frameworks (Flask):** Migrated a CLI Python script into a full web application by exposing API endpoints (`/api/weather`) and serving HTML templates.
- **Frontend Integration:** Used the JavaScript `fetch` API to asynchronously call the backend Python server and dynamically update the DOM without reloading the page.
- **API Integration:** Consumed multiple free endpoints (Open-Meteo Geocoding & Weather APIs) and mapped nested JSON data.
- **Decorators (`@retry_once`):** Wrote a custom Python wrapper to catch HTTP exceptions, introduce a delay, and retry the request once before failing gracefully. 
- **Caching (`json`):** Built a lightweight local JSON cache store to check timestamps and serve cached data if it's less than 10 minutes old.
