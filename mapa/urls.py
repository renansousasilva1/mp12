from django.conf import settings
from django.urls import path
from .views import nominatim_proxy, stream_updates
from . import views  # Importa as views do app
from django.conf.urls.static import static


urlpatterns = [
    # Exemplo de configuração de uma view chamada `home`
    path('', views.home, name='home'),
    path('tabela', views.tabela, name='tabela'),
    path('teste', views.teste, name='teste'),
    path('teste2', views.teste2, name='teste2'),
    path('teste3', views.teste3, name='teste3'),
    path('teste4', views.teste4, name='teste4'),
    path('teste5', views.teste5, name='teste5'),
    path('update_plan/', views.coletar_dados_clima, name='api-clima'),  # Defina a rota
    path('bairro/', views.obter_endereco, name='bairro_do_usuario'),
    path('register/', views.register, name='register'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path("sugestao", views.sugestao, name="sugestao"), 
    path("stream-updates/", stream_updates, name="stream_updates"),
    path('responder_sugestao/', views.listar_sugestoes, name='listar_sugestoes'),
    path('responder_sugestao/<int:sugestao_id>/', views.responder_sugestao, name="responder_sugestao"),   
    path('get-route/', views.get_route, name='get_route'),
    path('api/get-google-maps-key/', views.get_google_maps_key, name='get_google_maps_key'),
    path('api/get-google-api-key/', views.get_google_api_key, name='get_google_api_key'),path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('play', views.player, name='player'),
    path('update_plan/', views.update_plan, name='update_plan'),
    path('premium-content/', views.premium_content, name='premium_content'),
    path('testepremium/', views.testepremium, name='testepremium'),
    path('nominatim-proxy/', nominatim_proxy, name='nominatim_proxy'),
    path('route/', views.get_route, name='get_route'),
    path('mapa', views.mp, name="mapa"),
    path('sucesso', views.sucesso, name="pagina_de_sucesso"),
    path('legenda', views.legenda, name="legenda"),
    path('donation', views.donation, name="donation"),
    path('contato', views.contato, name="contato"),
    path('premium', views.premium, name="premium"),
    path('geocode/', views.geocode, name='geocode'),
    path('index', views.index, name="index"),
    path('minhaconta', views.minha_conta, name="minhaconta"),
    path('painel', views.infos, name="painel"),
    path('teste6', views.teste6, name="teste6"),
    path("weather/<str:city_name>/", views.get_weather, name="get_weather"),
   

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
