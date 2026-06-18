import requests
from django.conf import settings


class WeatherService:
    """Сервис для работы с API Яндекс Погоды"""

    BASE_URL = 'https://api.weather.yandex.ru/v2/forecast'

    @staticmethod
    def get_coordinates(city):
        """Получение координат (словарь + OpenStreetMap)"""

        # Словарь популярных городов
        CITIES = {
            'москва': (55.7558, 37.6173),
            'moscow': (55.7558, 37.6173),
            'санкт-петербург': (59.9343, 30.3351),
            'екатеринбург': (56.8389, 60.6057),
            'ekaterinburg': (56.8389, 60.6057),
            'yekaterinburg': (56.8389, 60.6057),
            'новосибирск': (55.0084, 82.9357),
            'казань': (55.7887, 49.1221),
            'краснодар': (45.0355, 38.9753),
            'нижний новгород': (56.2965, 43.9361),
        }

        city_lower = city.lower().strip()
        if city_lower in CITIES:
            return CITIES[city_lower]

        # Пробуем OpenStreetMap
        url = 'https://nominatim.openstreetmap.org/search'
        params = {'q': city, 'format': 'json', 'limit': 1}

        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
        except Exception:
            pass

        return None, None

    @staticmethod
    def get_weather(city):
        """Получение погоды по городу"""
        if not settings.YANDEX_API_KEY:
            return None

        lat, lon = WeatherService.get_coordinates(city)
        if lat is None or lon is None:
            return None

        headers = {'X-Yandex-API-Key': settings.YANDEX_API_KEY}
        params = {'lat': lat, 'lon': lon, 'limit': 1}

        try:
            response = requests.get(
                WeatherService.BASE_URL,
                headers=headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            fact = data.get('fact', {})
            forecast = data.get('forecasts', [{}])[0]

            return {
                'temperature': fact.get('temp'),
                'pressure': fact.get('pressure_mm'),
                'humidity': fact.get('humidity'),
                'condition': WeatherService._translate_condition(fact.get('condition')),
                'moon_phase': WeatherService._translate_moon_phase(
                    forecast.get('moon_code', 0)
                ),
            }
        except Exception as e:
            print(f"Ошибка получения погоды: {e}")
            return None

    @staticmethod
    def _translate_condition(condition):
        conditions = {
            'clear': 'Ясно',
            'partly-cloudy': 'Малооблачно',
            'cloudy': 'Облачно',
            'overcast': 'Пасмурно',
            'drizzle': 'Морось',
            'light-rain': 'Небольшой дождь',
            'rain': 'Дождь',
            'moderate-rain': 'Умеренный дождь',
            'heavy-rain': 'Сильный дождь',
            'showers': 'Ливень',
            'snow': 'Снег',
            'light-snow': 'Небольшой снег',
            'thunderstorm': 'Гроза',
        }
        return conditions.get(condition, condition)

    @staticmethod
    def _translate_moon_phase(moon_code):
        phases = {
            0: '🌑 Новолуние',
            3: '🌓 Первая четверть',
            7: '🌕 Полнолуние',
            10: '🌗 Последняя четверть',
        }
        return phases.get(moon_code, f'🌙 Фаза {moon_code}')
