import json
import os
import time

CACHE_FILE = "cache_store.json"
CACHE_EXPIRY = 600  # 10 minutes in seconds

def _load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def _save_cache(cache_data):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache_data, f, indent=4)

def get_cached(city_name: str) -> dict | None:
    """Returns cached weather data if it exists and is less than 10 minutes old."""
    cache_data = _load_cache()
    city_lower = city_name.lower()
    
    if city_lower in cache_data:
        entry = cache_data[city_lower]
        if time.time() - entry['timestamp'] < CACHE_EXPIRY:
            return entry['data']
    return None

def set_cache(city_name: str, data: dict) -> None:
    """Writes/updates the cache entry for a city with the current timestamp."""
    cache_data = _load_cache()
    city_lower = city_name.lower()
    
    cache_data[city_lower] = {
        'timestamp': time.time(),
        'data': data
    }
    _save_cache(cache_data)
