import os
import requests

from django.shortcuts import render, redirect
from collections import defaultdict
from . import controllers
from django.http import JsonResponse

STATS_FILE = os.path.join(os.path.dirname(__file__), 'stats/city_stats.json')

city_stats = controllers.load_city_stats(STATS_FILE)

def index(request):
	last_city = request.session.get("last_city")
	
	if request.method == 'POST':
		city = request.POST.get('city')
		if city:
			request.session['last_city'] = city
			return redirect('weather:show_weather', city_name=city)
			
	
	return render(request, 'main/index.html',{'last_city': last_city})

def show_weather(request, city_name):
	geo_url = "https://geocoding-api.open-meteo.com/v1/search"
	geo_params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
	geo_response = requests.get(geo_url, params=geo_params)
	geo_data = geo_response.json()

	forecast = []
	if geo_data.get("results"):
		city_stats[city_name.lower()] += 1
		controllers.save_city_stats(city_stats, STATS_FILE)
		lat = geo_data["results"][0]["latitude"]
		lon = geo_data["results"][0]["longitude"]
		
		weather_url = "https://api.open-meteo.com/v1/forecast"
		weather_params = {
			"latitude": lat,
			"longitude": lon,
			"daily": "temperature_2m_max,temperature_2m_min,weathercode",
			"timezone": "auto"
		}
		weather_response = requests.get(weather_url, params=weather_params)
		weather_data = weather_response.json()

		if "daily" in weather_data:
			daily = weather_data["daily"]
			for i in range(len(daily["time"])):
				forecast.append({
					"date": daily["time"][i],
					"temp": f"{daily['temperature_2m_min'][i]}…{daily['temperature_2m_max'][i]}°C",
					"description": controllers.weather_code_to_text(daily["weathercode"][i])
				})

	return render(request, "main/result.html", {
			"city_name": city_name,
			"forecast": forecast
		})

def city_stats_api(request):
	return JsonResponse(dict(city_stats))