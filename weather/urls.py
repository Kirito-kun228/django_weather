from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('search/', views.index, name='search_weather'),  # Обработка формы поиска
    path('suggest/', views.city_suggestions, name='city_suggestions')
]
