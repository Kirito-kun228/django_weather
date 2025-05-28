from django.db import models

# Create your models here.

#вообще так как количество запросов к апи ограничено,
#существует смысл кэшировать погоду в бд для каждого города
#и отправлять новый запрос к api погоды, только по истечению некоторого времени

class SearchHistory(models.Model):
    session_id = models.CharField(max_length=255)  #будем обращаться по сессии пользователя
    city_name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city_name} — {self.searched_at.strftime('%Y-%m-%d %H:%M')}"

class CityStats(models.Model):
    city_name = models.CharField(max_length=100, unique=True)
    search_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.city_name} ({self.search_count})"
