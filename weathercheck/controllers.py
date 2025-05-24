import json
import os
from collections import defaultdict

def load_city_stats(STATS_FILE):
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            return defaultdict(int, json.load(f))
    return defaultdict(int)

def save_city_stats(stats, STATS_FILE):
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False)


def weather_code_to_text(code):
    # Упрощённый перевод кодов погоды (можно расширить)
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