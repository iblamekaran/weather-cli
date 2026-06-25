from flask import Flask, render_template, request, jsonify
from api import geocode_city, fetch_weather
from cache import get_cached, set_cache

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather', methods=['GET'])
def get_weather():
    city_name = request.args.get('city')
    unit = request.args.get('unit', 'celsius')
    forecast = request.args.get('forecast', 'false').lower() == 'true'

    if not city_name:
        return jsonify({"error": "City name is required"}), 400

    cache_key = f"{city_name.lower()}_{unit}_{forecast}"
    
    # 1. Check Cache
    cached_data = get_cached(cache_key)
    if cached_data:
        cached_data['is_cached'] = True
        return jsonify(cached_data)

    # 2. Geocode City
    location = geocode_city(city_name)
    if not location:
        return jsonify({"error": f"Couldn't find a city called '{city_name}'."}), 404

    flag = location.get('flag', '')
    display_name = f"{location['name']}, {location['country']} {flag}".strip()

    # 3. Fetch Weather
    weather_data = fetch_weather(location['lat'], location['lon'], unit=unit, include_forecast=forecast)
    if not weather_data:
        return jsonify({"error": "Received malformed data from the weather service."}), 502

    # 4. Save to Cache
    full_data = {
        'display_name': display_name,
        'weather': weather_data
    }
    set_cache(cache_key, full_data)

    full_data['is_cached'] = False
    return jsonify(full_data)

if __name__ == '__main__':
    app.run(debug=True)
