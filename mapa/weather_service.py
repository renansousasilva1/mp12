import requests
from django.utils.timezone import now
from .models import WeatherData, City

API_KEY = "e9365f0cc300d0fc10188ee2394f2e6c"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

CITIES = [
    "Niterói", "Rio de Janeiro", "Itaguaí", "Mangaratiba", "Angra dos Reis",
    "Cabo Frio", "Arraial do Cabo", "Volta Redonda", "Paraty", "Nova Iguaçu",
    "Duque de Caxias", "São Gonçalo", "Campos dos Goytacazes", "São João de Meriti",
    "Macaé", "Petrópolis", "Teresópolis", "Magé", "Itaboraí", "Resende",
    "Queimados", "Maricá", "Barra Mansa", "Seropédica"
]

def fetch_weather_data(city_name):
    """Faz a requisição à API OpenWeather e retorna os dados formatados."""
    params = {"q": city_name, "appid": API_KEY, "units": "metric", "lang": "pt"}
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "wind_direction": data["wind"]["deg"],
            "weather_main": data["weather"][0]["main"],
            "weather_description": data["weather"][0]["description"],
            "weather_icon": data["weather"][0]["icon"],
            "timestamp": now()
        }
    return None

def update_weather_data():
    """Atualiza os dados meteorológicos no banco de dados."""
    for city_name in CITIES:
        city, created = City.objects.get_or_create(name=city_name)
        weather_data = fetch_weather_data(city_name)

        if weather_data:
            WeatherData.objects.update_or_create(
                city=city,
                defaults=weather_data
            )
