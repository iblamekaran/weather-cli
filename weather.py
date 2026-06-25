import argparse
import sys
import requests
from api import geocode_city, fetch_weather
from cache import get_cached, set_cache

# Ensure console can print Unicode emojis (especially on Windows)
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Simple ANSI colors for terminal output
class Colors:
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def display_weather(city_display_name: str, weather_data: dict, is_cached: bool):
    """Prints the weather data in a clean, formatted way."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}Weather in {city_display_name}{Colors.RESET}")
    print("-" * 30)
    print(f"{Colors.BOLD}Temperature:{Colors.RESET} {weather_data['temperature']}{weather_data.get('unit', '°C')}")
    print(f"{Colors.BOLD}Wind Speed:{Colors.RESET}  {weather_data['wind_speed']} km/h")
    print(f"{Colors.BOLD}Condition:{Colors.RESET}   {weather_data['condition']}")
    
    if "forecast" in weather_data:
        f_data = weather_data["forecast"]
        print("-" * 30)
        print(f"{Colors.CYAN}{Colors.BOLD}Tomorrow's Forecast ({f_data['date']}):{Colors.RESET}")
        print(f"{Colors.BOLD}High/Low:{Colors.RESET}    {f_data['max_temp']}{weather_data.get('unit', '°C')} / {f_data['min_temp']}{weather_data.get('unit', '°C')}")
        print(f"{Colors.BOLD}Condition:{Colors.RESET}   {f_data['condition']}")
        
    status = "cached" if is_cached else "fetched fresh"
    color = Colors.GREEN if is_cached else Colors.YELLOW
    print(f"({color}{status}{Colors.RESET})\n")

def main():
    parser = argparse.ArgumentParser(description="A command-line weather lookup tool with caching and retry logic.")
    parser.add_argument("city", nargs="+", help="Name of the city to get weather for")
    parser.add_argument("--unit", choices=["celsius", "fahrenheit"], default="celsius", help="Temperature unit (celsius or fahrenheit)")
    parser.add_argument("--forecast", action="store_true", help="Show next-day forecast")
    args = parser.parse_args()
    
    city_name = " ".join(args.city)
    cache_key = f"{city_name}_{args.unit}_{args.forecast}"
    
    try:
        # 1. Check Cache
        cached_data = get_cached(cache_key)
        if cached_data:
            display_weather(cached_data['display_name'], cached_data['weather'], is_cached=True)
            return

        # 2. Geocode City
        location = geocode_city(city_name)
        if not location:
            print(f"{Colors.RED}Error:{Colors.RESET} Couldn't find a city called '{city_name}'. Check spelling and try again.")
            sys.exit(1)

        flag = location.get('flag', '')
        display_name = f"{location['name']}, {location['country']} {flag}".strip()

        # 3. Fetch Weather
        weather_data = fetch_weather(location['lat'], location['lon'], unit=args.unit, include_forecast=args.forecast)
        if not weather_data:
            print(f"{Colors.RED}Error:{Colors.RESET} Received malformed data from the weather service.")
            sys.exit(1)

        # 4. Save to Cache
        full_data = {
            'display_name': display_name,
            'weather': weather_data
        }
        set_cache(cache_key, full_data)

        # 5. Display Result
        display_weather(display_name, weather_data, is_cached=False)

    except requests.exceptions.RequestException:
        # Catches network errors that persisted even after the retry decorator
        print(f"{Colors.RED}Error:{Colors.RESET} Weather service is unreachable right now. Check your internet connection or try again in a bit.")
        sys.exit(1)
    except Exception as e:
        # Catch-all for unexpected errors so we don't show stack traces to users
        print(f"{Colors.RED}Unexpected Error:{Colors.RESET} {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
