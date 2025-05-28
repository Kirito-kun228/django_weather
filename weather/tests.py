from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch


class WeatherAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('weather:index')
        self.suggest_url = reverse('weather:city_suggestions')

    def test_home_get(self):
        """Страница '/' возвращает 200 и содержит форму"""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")

    def test_suggestions_short_query(self):
        """Короткий запрос (меньше 2 символов) возвращает пустой список"""
        response = self.client.get(self.suggest_url, {'q': 'A'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [])

    @patch("weather.views.retry_session.get")
    def test_suggestions_valid_query(self, mock_get):
        """AJAX-подсказка возвращает список городов"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {'display_name': 'London, UK'},
            {'display_name': 'London, Canada'}
        ]

        response = self.client.get(self.suggest_url, {'q': 'Londo'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, ['London, UK', 'London, Canada'])

    def test_template_used(self):
        """Проверка, что используется правильный шаблон"""
        response = self.client.get(self.home_url)
        self.assertTemplateUsed(response, "weather/index.html")

