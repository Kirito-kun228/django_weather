Этот проект представляет собой веб-приложение на Django для отображения прогноза погоды по введённому городу с автодополнением названий. Данные о погоде получаются с помощью [Open-Meteo API](https://open-meteo.com/), геокодинг — через [OpenStreetMap Nominatim](https://nominatim.openstreetmap.org/).

Реализованные функции - все из технического задания за исключением возможности сохранять историю поиска для каждого пользователя, и будет API, показывающего сколько раз вводили какой город

Используемые технологии

- Backend: Django 5.2, Python 3.12
- Frontend: HTML, Bootstrap 5, JavaScript (AJAX)
- API: Open-Meteo, Nominatim
- База данных: PostgreSQL
- Контейнеризация: Docker, Docker Compose

Как запустить проект:

1. Клонировать репозиторий
   git clone https://github.com/Kirito-kun228/django_weather
2. переходим в папку проекта командой cd django_weather
3. создаем и запускаем наш проект docker-compose up --build

