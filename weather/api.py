import requests
import openmeteo_requests
import requests_cache
from retry_requests import retry
from datetime import datetime

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

def geocode_city(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1,
    }
    headers = {"User-Agent": "weather_django_app/1.0"}
    response = requests.get(url, params=params, headers=headers)
    print(f"Geo Response for {city_name}: {response.status_code} {response.text}")
    if response.ok and response.json():
        data = response.json()[0]
        return float(data['lat']), float(data['lon'])
    return None, None

def get_weather_by_city(city_name):
    lat, lon = geocode_city(city_name)
    if lat is None:
        return None, "Город не найден"

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation_probability",
        "forecast_days": 1,
        "timezone": "auto"
    }
    try:
        responses = openmeteo.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
        response = responses[0]
        hourly = response.Hourly()


        start_time = hourly.Time()
        end_time = hourly.TimeEnd()
        interval = hourly.Interval()
        times = [start_time + i * interval for i in range((end_time - start_time) // interval)]
        temperatures = hourly.Variables(0).ValuesAsNumpy()
        precip_probs = hourly.Variables(1).ValuesAsNumpy()

        forecast = []
        for t, temp, precip_probs in zip(times, temperatures, precip_probs):
            readable_time = datetime.utcfromtimestamp(t).strftime("%Y-%m-%d %H:%M")
            forecast.append({
                'time': readable_time,
                'temperature': round(temp,1),
                'precip_probs': round(precip_probs)
            })
        data = {
            'latitude': response.Latitude(),
            'longitude': response.Longitude(),
            'timezone': response.Timezone(),
            'forecast': forecast
        }
        return data, None

    except Exception as e:
        return None, f"Ошибка при получении данных: {str(e)}"