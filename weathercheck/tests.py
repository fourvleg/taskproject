from django.test import TestCase, Client
from django.urls import reverse

class WeatherViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_get(self):
        response = self.client.get(reverse('weather:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')

    def test_index_post_redirect(self):
        response = self.client.post(reverse('weather:index'), {'city': 'Москва'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/show_weather/', response.url)

    def test_show_weather(self):
        response = self.client.get(reverse('weather:show_weather', args=['Москва']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/result.html')
        self.assertIn('city_name', response.context)
        self.assertEqual(response.context['city_name'], 'Москва')

    def test_city_stats_api(self):
        response = self.client.get(reverse('weather:show_stats'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')