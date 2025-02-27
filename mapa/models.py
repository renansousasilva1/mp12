from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import datetime

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class WeatherData(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.FloatField()
    feels_like = models.FloatField()
    humidity = models.IntegerField()
    pressure = models.IntegerField()
    wind_speed = models.FloatField()
    wind_direction = models.IntegerField()
    weather_main = models.CharField(max_length=100)  # Clear, Clouds, Rain, etc.
    weather_description = models.CharField(max_length=200)
    weather_icon = models.CharField(max_length=20)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.city.name} - {self.temperature}°C"


# Create your models here.
class Profile(models.Model):
    PLAN_CHOICES = [
        ('free', 'Grátis'),
        ('basic', 'Básico'),
        ('premium', 'Premium'),
        ('enterprise', 'Empresarial'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')  # Novo campo


    def __str__(self):
        return f'{self.user.username} Profile'
    

class APIUsage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    requests_made = models.IntegerField(default=0)  # Total de requisições
    last_reset = models.DateTimeField(auto_now_add=True)  # Última vez que foi reiniciado

    def __str__(self):
        return f"API Usage for {self.user.username}"
    

class Sugestao(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return self.titulo
   
   
class Resposta(models.Model):
    sugestao = models.ForeignKey(Sugestao, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    resposta = models.TextField()
    data_resposta = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return f"Resposta à Sugestão: {self.sugestao.titulo} (Autor: {self.autor.username}) (Resposta: {self.resposta})"
    

