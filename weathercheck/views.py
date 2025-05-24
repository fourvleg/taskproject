import os

from django.shortcuts import render, redirect
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
	forecast = controllers.get_wather_data(city_name, city_stats, STATS_FILE)
 
	return render(request, "main/result.html", {
			"city_name": city_name,
			"forecast": forecast
		})

def city_stats_api(request):
	return JsonResponse(dict(city_stats))