# WeatherCheck

**WeatherCheck** — это Django-приложение для просмотра прогноза погоды по городам с сохранением статистики запросов.

Использовал json для подсчета поиска городов. Посчитал это более уместным. ¯\_(ツ)_/¯
Разделил логику используя controllers.

##Стек
- Django-5.2.1
- Requests

## Возможности

- Ввод города и просмотр прогноза погоды на несколько дней.
- Сохранение статистики запросов по городам в JSON-файл.
- API для получения статистики по городам.
- Docker-окружение для быстрого запуска.

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/fourvleg/taskproject.git
cd taskproject
```

### 2. Запуск через Docker

Соберите образ (если не собран):

```bash
docker build -t weather-check .
```

Запустите контейнер:

```bash
docker-compose up
```
После выполните миграции в отдельном терминале:

```bash
docker-compose exec weather python manage.py migrate
```

Приложение будет доступно по адресу [http://localhost:8000](http://localhost:8000)

### 3. Локальный запуск (без Docker)

Установите зависимости:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Примените миграции:

```bash
python manage.py migrate
```

Запустите сервер:

```bash
python manage.py runserver
```

### 4. Тесты

```bash
python manage.py test
```

## Переменные окружения

- `SECRET_KEY` — секретный ключ Django (см. `docker-compose.yml`)
- `DEBUG` — режим отладки (`True`/`False`)

## API

- `/api/v1/show_stats/` — получить статистику запросов по городам (JSON)

## Пример использования

1. Введите название города на главной странице.
2. Получите прогноз погоды.
3. Посмотрите статистику по городам через API.

---

