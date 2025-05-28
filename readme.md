Этот проект представляет собой веб-приложение на Django для отображения прогноза погоды по введённому городу с автодополнением названий. Данные о погоде получаются с помощью [Open-Meteo API](https://open-meteo.com/), геокодинг — через [OpenStreetMap Nominatim](https://nominatim.openstreetmap.org/).

Реализованные функции - все из технического задания за исключением возможности сохранять историю поиска для каждого пользователя, и будет API, показывающего сколько раз вводили какой город

Используемые технологии

- Backend: Django 5.2, Python 3.12
- Frontend: HTML, Bootstrap 5, JavaScript (AJAX)
- API: Open-Meteo, Nominatim
- База данных: PostgreSQL
- Контейнеризация: Docker, Docker Compose

Как запустить проект(2 способа):

1. Клонировать репозиторий
```bash
git clone https://github.com/yourusername/weather-django-app.git
cd weather-django-app
2. установить reuirements.txt
3. поменять настройки базы данных в settings.py с db на localhost
4. запустить сервис погоды

второй способ:
1.Убедитесь, что у вас установлен Docker и Docker Compose.
2️. В терминале выполните:
bashdocker pull your-dockerhub-username/weather-app
docker run -d -p 8000:8000 your-dockerhub-username/weather-app
3️. Откройте сайт в браузере:
http://localhost:8000/

