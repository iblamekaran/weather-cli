import time
from functools import wraps
import requests

def retry_once(func):
    """
    A decorator that catches request exceptions, waits 2 seconds, 
    and retries the wrapped function exactly once before letting the error propagate.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException:
            time.sleep(2)
            # If it fails again, we let the exception bubble up
            return func(*args, **kwargs)
    return wrapper

@retry_once
def geocode_city(city_name: str) -> dict | None:
    """
    Calls Open-Meteo geocoding API.
    Returns {"lat": float, "lon": float, "name": str, "country": str} or None if not found.
    """
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    if not data.get("results"):
        return None
        
    result = data["results"][0]
    return {
        "lat": result["latitude"],
        "lon": result["longitude"],
        "name": result["name"],
        "country": result.get("country", "Unknown")
    }

def get_weather_description(code: int) -> str:
    """Maps WMO weather codes to human-readable strings."""
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
    }
    return weather_codes.get(code, "Unknown condition")

@retry_once
def fetch_weather(lat: float, lon: float, unit: str = 'celsius', include_forecast: bool = False) -> dict | None:
    """
    Calls Open-Meteo weather API.
    Returns a parsed weather dict.
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    if unit == 'fahrenheit':
        url += "&temperature_unit=fahrenheit"
        
    if include_forecast:
        url += "&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=auto"
        
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    current = data.get("current_weather", {})
    if not current:
        return None
        
    result = {
        "temperature": current.get("temperature"),
        "wind_speed": current.get("windspeed"),
        "condition": get_weather_description(current.get("weathercode", -1)),
        "unit": "°F" if unit == "fahrenheit" else "°C"
    }

    if include_forecast and "daily" in data:
        daily = data["daily"]
        if len(daily.get("time", [])) > 1:
            result["forecast"] = {
                "date": daily["time"][1],
                "max_temp": daily["temperature_2m_max"][1],
                "min_temp": daily["temperature_2m_min"][1],
                "condition": get_weather_description(daily["weathercode"][1])
            }
            
    return result
