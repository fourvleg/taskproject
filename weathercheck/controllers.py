import json
import os
from collections import defaultdict
import requests

def load_city_stats(STATS_FILE):
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            return defaultdict(int, json.load(f))
    return defaultdict(int)

def save_city_stats(stats, STATS_FILE):
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False)
        
def get_wather_data(city_name, city_stats, STATS_FILE):
	geo_url = "https://geocoding-api.open-meteo.com/v1/search"
	geo_params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
	geo_response = requests.get(geo_url, params=geo_params)
	geo_data = geo_response.json()

	forecast = []
	if geo_data.get("results"):
		city_stats[city_name.lower()] += 1
		save_city_stats(city_stats, STATS_FILE)
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
					"description": weather_code_to_text(daily["weathercode"][i])
				})
	return forecast
  
def weather_code_to_text(code):
    return {
        0: "Ясно",
        1: "Преимущественно ясно",
        2: "Переменная облачность",
        3: "Пасмурно",
        45: "Туман",
        61: "Небольшой дождь",
        63: "Умеренный дождь",
        65: "Сильный дождь",
    }.get(code, "Неизвестно")