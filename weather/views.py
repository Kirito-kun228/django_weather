import openmeteo_requests
import requests_cache
from retry_requests import retry
from django.shortcuts import render

from .api import get_weather_by_city
from .forms import CitySearchForm
from .models import SearchHistory, CityStats
from geopy.geocoders import Nominatim
from django.http import JsonResponse


cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

geolocator = Nominatim(user_agent="weather_app")


def index(request):
    form = CitySearchForm()
    error = None

    if request.method == 'POST':
        form = CitySearchForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            result, error = get_weather_by_city(city)

            if result:
                request.session['last_city'] = city
                if not request.session.session_key:
                    request.session.save()
                session_id = request.session.session_key
                SearchHistory.objects.create(
                    session_id=session_id,
                    city_name=city,
                    latitude=result['latitude'],
                    longitude=result['longitude'],
                )
                city_obj, created = CityStats.objects.get_or_create(city_name=city)
                city_obj.search_count += 1
                city_obj.save()

                return render(request, 'weather/result.html', {
                    'title': 'Результаты прогноза',
                    'city': city,
                    'weather': result,
                })

    return render(request, 'weather/index.html', {
        'form': form,
        'error': error,
        'last_city': request.session.get('last_city'),
        'title': 'Прогноз погоды',
    })

def city_suggestions(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse([], safe=False)

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "limit": 5,
        "addressdetails": 1,
    }
    headers = {
        "User-Agent": "weather-app"
    }

    response = retry_session.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        suggestions = [item['display_name'] for item in data]
        return JsonResponse(suggestions, safe=False)
    return JsonResponse([], safe=False)

