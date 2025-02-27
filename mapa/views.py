from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
import requests
from .forms import ProfileForm, RespostaForm, SugestaoForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
from .models import Profile, Sugestao, Resposta,  APIUsage
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseForbidden, JsonResponse
from django.http import StreamingHttpResponse
import json
import time
import requests 
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from collections import Counter
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from django.utils.timezone import now
from datetime import timedelta

from django.http import JsonResponse
from django.utils.timezone import now
from .models import WeatherData, City
from .weather_service import fetch_weather_data

from django.shortcuts import render
from django.utils.timezone import now
from .models import WeatherData, City
from .weather_service import fetch_weather_data

def weather_view(request, city_name):
    city_name = city_name.strip().title()
    city = get_object_or_404(City, name=city_name)

    weather = WeatherData.objects.filter(city=city).order_by("-timestamp").first()

    if not weather or weather.timestamp.date() < now().date():
        new_data = fetch_weather_data(city_name)
        if new_data:
            weather = WeatherData.objects.create(city=city, **new_data)
            print("Weather Data:", weather.__dict__)  # Debug no terminal

    return render(request, "html/home.html", {"weather": {
    "city": {"name": weather.city.name},
    "temperature": weather.temperature,
    "feels_like": weather.feels_like,
    "humidity": weather.humidity,
    "pressure": weather.pressure,
    "wind_speed": weather.wind_speed,
    "wind_direction": weather.wind_direction,
    "weather_main": weather.weather_main,
    "weather_description": weather.weather_description,
    "weather_icon": f"https://openweathermap.org/img/wn/{weather.weather_icon}.png",
}})



def get_weather(request, city_name):
    """Retorna os dados da cidade consultada, atualizando se necessário."""
    try:
        city = City.objects.get(name=city_name)
        weather = WeatherData.objects.get(city=city)

        # Se os dados forem antigos, atualiza
        if weather.timestamp.date() < now().date():
            new_data = fetch_weather_data(city_name)
            if new_data:
                for key, value in new_data.items():
                    setattr(weather, key, value)
                weather.save()
        
        return JsonResponse({
            "city": weather.city.name,
            "temperature": weather.temperature,
            "feels_like": weather.feels_like,
            "humidity": weather.humidity,
            "pressure": weather.pressure,
            "wind_speed": weather.wind_speed,
            "wind_direction": weather.wind_direction,
            "weather_main": weather.weather_main,
            "weather_description": weather.weather_description,
            "weather_icon": f"https://openweathermap.org/img/wn/{weather.weather_icon}.png",
            "timestamp": weather.timestamp
        })
    except (City.DoesNotExist, WeatherData.DoesNotExist):
        return JsonResponse({"error": "Cidade não encontrada"}, status=404)






headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def coletar_dados_clima(request):
    # 🔹 Fonte 1: Clima
    fonte1 = 'https://www.climatempo.com.br/previsao-do-tempo/cidade/321/riodejaneiro-rj'
    clima_data = {}

    try:
        # 🔹 Coleta de dados do clima (Fonte 1)
        response = requests.get(fonte1, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')

        temp_min = soup.find(id='min-temp-1')
        temp_max = soup.find(id='max-temp-1')

        clima_data = {
            'cidade': 'Rio de Janeiro - RJ',
            'temperatura_minima': temp_min.text.strip() if temp_min else "Não encontrado",
            'temperatura_maxima': temp_max.text.strip() if temp_max else "Não encontrado",
            'fonte': fonte1
        }

        # 🔹 Fonte 2: Sensação
        fonte2 = 'https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/321/riodejaneiro-rj'
        response = requests.get(fonte2, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')

        sensacao_element = soup.find(class_='no-gutters -gray _flex _justify-center _margin-t-20 _padding-b-20 _border-b-light-1')
        sensacao = sensacao_element.text.strip() if sensacao_element else 'Sensação não encontrada'

        # 🔹 Fonte 3: Coleta de dados de precipitação
        fonte3 = requests.get('https://tempo.clic.com.br/rj/rio-dejaneiro').text
        soup = BeautifulSoup(fonte3, 'html.parser')
                              
        # 🔹 Coleta de dados de chuva
        chuva_element = soup.find(class_='precipitationValue')
        if chuva_element:
            chuva = chuva_element.find('span').text.strip()
        else:
            chuva = 'Precipitação não encontrada'

        # 🔹 Fonte 4: Coleta de dados de previsão do céu
        fonte4 = requests.get('https://www.sistema-alerta-rio.com.br/upload/Previsao.html').text
        soup = BeautifulSoup(fonte4, 'html.parser')
                              
        # 🔹 Coleta de dados de céu
        celulas = soup.find_all('td', class_='head')
        previsao = ''
        for celula in celulas:
            if celula.text.strip() == 'Céu':
                linha_celula = celula.find_next('tr')
                celulas_linha = linha_celula.find_all('td')
                previsao = celulas_linha[1].text.strip()  # Pegando a previsão do céu


    except Exception as e:
        clima_data = {'erro': f'Erro ao acessar dados: {str(e)}'}
        sensacao = 'Erro ao acessar dados de sensação térmica.'
        chuva = 'Erro ao acessar dados de precipitação.'
        previsao = 'Erro ao acessar dados de previsão do tempo.'
        icone_clima = 'fa-cloud-sun'  # Fallback genérico
        icone_maxima = 'fa-cloud-sun'

    # Passando os dados para o contexto do template
    context = {
        'clima': clima_data,
        'sensacao': sensacao,
        'chuva': chuva,
        'icone_clima': icone_clima,  # Ícone do clima geral
        'icone_maxima': icone_maxima,  # Ícone colorido para a máxima
        'previsao': previsao  # Previsão do tempo
    }

    return render(request, 'html/update_plan.html', context)


def infos(request):
    # 🔹 Fonte 1: Clima
    fonte1 = 'https://www.climatempo.com.br/previsao-do-tempo/cidade/321/riodejaneiro-rj'
    clima_data = {}

    try:
        # Coleta de dados do clima
        response = requests.get(fonte1)
        soup = BeautifulSoup(response.text, 'html.parser')

        temp_min = soup.find(id='min-temp-1')
        temp_max = soup.find(id='max-temp-1')

        clima_data = {
            'cidade': 'Rio de Janeiro - RJ',
            'temperatura_minima': temp_min.text.strip() if temp_min else "Não encontrado",
            'temperatura_maxima': temp_max.text.strip() if temp_max else "Não encontrado",
            'fonte': fonte1
        }

        # 🔹 Fonte 2: Sensação
        fonte2 = 'https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/321/riodejaneiro-rj'
        response = requests.get(fonte2)
        soup = BeautifulSoup(response.text, 'html.parser')

        sensacao_element = soup.find(class_='no-gutters -gray _flex _justify-center _margin-t-20 _padding-b-20 _border-b-light-1')
        sensacao = sensacao_element.text.strip() if sensacao_element else 'Sensação não encontrada'  # Define sensacao


        # 🔹 Fonte 3: Coleta de dados de precipitação
        fonte3 = requests.get('https://tempo.clic.com.br/rj/rio-de-janeiro').text

        soup = BeautifulSoup(fonte3, 'html.parser')
                              
        # 🔹 Coleta de dados de chuva
        chuva_element = soup.find(class_='precipitationValue')
        if chuva_element:
            # Extrai o valor da precipitação, como '0.0 mm'
            chuva = chuva_element.find('span').text.strip()
        else:
            chuva = 'Precipitação não encontrada'

    except Exception as e:
        clima_data = {'erro': f'Erro ao acessar dados: {str(e)}'}
        sensacao = 'Erro ao acessar dados de sensação térmica.'
        chuva = 'Erro ao acessar dados de chuva.'

    # 🔹 Montando o dicionário final
    context = {
        'clima': clima_data,
        'sensacao': sensacao,
        'chuva': chuva,  # Aqui estamos passando o valor da precipitação para o contexto
    }

    return render(request, 'html/painel.html', context)


# Função para obter o endereço baseado nas coordenadas (latitude e longitude)
@csrf_exempt
def obter_endereco(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            if not latitude or not longitude:
                return JsonResponse({'error': 'Latitude e longitude são necessários.'}, status=400)

            api_key = 'AIzaSyClZ8Fn3e432e2UZBKSqXCuRHF0AxTgs1I'  # Substitua pela sua chave da API do Google Maps
            url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}'

            response = requests.get(url)
            result = response.json()

            if response.status_code == 200 and result.get('results'):
                address = result['results'][0]['formatted_address']
                neighborhood = None
                city = None
                state = None

                for component in result['results'][0]['address_components']:
                    if 'sublocality_level_1' in component['types']:
                        neighborhood = component['long_name']
                    elif 'administrative_area_level_2' in component['types']:
                        city = component['long_name']
                    elif 'administrative_area_level_1' in component['types']:
                        state = component['long_name']

                if not neighborhood:
                    neighborhood = "Não disponível"
                if not city:
                    city = "Não disponível"
                if not state:
                    state = "Não disponível"

                return JsonResponse({
                    'endereco': address,
                    'bairro': neighborhood,
                    'cidade': city,
                    'estado': state
                })
            
            return JsonResponse({'error': 'Não foi possível obter o endereço'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Erro ao decodificar os dados JSON.'}, status=400)

    return JsonResponse({'error': 'Método de requisição inválido. Use POST.'}, status=405)




def tabela(request):
    try:
        # Requisição para pegar os dados da página
        html = requests.get('https://ondetemtiroteio.com/reportview.php').content
        soup = BeautifulSoup(html, 'html.parser')

        # Encontrar a tabela de ocorrências
        tabela = soup.find(class_='table-container')

        if tabela is None:
            return render(request, 'html/tabela.html', {'erro': 'Tabela não encontrada'})

        # Lista para armazenar os locais com tiroteio
        locais_com_tiroteio = []
        ultima_ocorrencia = {}

        linhas = tabela.find_all('tr')
        for linha in linhas:
            print(linha)  # Verifique o conteúdo da linha da tabela


        for i, linha in enumerate(linhas):
            colunas = linha.find_all('td')

            if len(colunas) >= 5:
                ocorrencia = colunas[1].text.strip()
                if 'tiroteio' in ocorrencia.lower():
                    local = colunas[2].text.strip()
                    locais_com_tiroteio.append(local)
                    ultima_ocorrencia[local] = i  # Armazena o índice da última ocorrência
                    print(locais_com_tiroteio)

        # Contagem de frequência dos locais com tiroteio
        contagem_locais = Counter(locais_com_tiroteio)

        # Organizando a lista: primeiro pela contagem e depois pelo índice da última ocorrência
        locais_ordenados = sorted(contagem_locais.items(), key=lambda x: (-x[1], ultima_ocorrencia[x[0]]), reverse=False)

        # Organize a lista em um formato adequado para o template
        locais_com_tiroteio_ordenados = [local for local, _ in locais_ordenados]

        # Passando a lista organizada para o template
        return render(request, 'html/tabela.html', {'locais_com_tiroteio': locais_com_tiroteio_ordenados})
        

    except Exception as e:
        return render(request, 'html/tabela.html', {'erro': str(e)})




@login_required
def sugestao(request):
    if request.method == 'POST':
        form = SugestaoForm(request.POST)
        if form.is_valid():
            sugestao = form.save(commit=False)
            sugestao.autor = request.user  # Associa a sugestão ao usuário logado
            sugestao.save()
            return redirect('pagina_de_sucesso')  # Redireciona para uma página de confirmação

    else:
        form = SugestaoForm()

    return render(request, 'html/sugestao.html', {'form': form})

@login_required
def listar_sugestoes(request):
    # Obtém todas as sugestões que ainda não foram respondidas
    sugestoes = Sugestao.objects.filter(resposta__isnull=True).select_related('autor__profile').all()

    # Ordena para que sugestões de ADMIN apareçam primeiro
    sugestoes = sorted(sugestoes, key=lambda s: 0 if s.autor.is_superuser else 1)

    return render(request, 'html/responder_sugestao.html', {'sugestoes': sugestoes})


@login_required
def responder_sugestao(request, sugestao_id):
    sugestao = get_object_or_404(Sugestao, id=sugestao_id)

    if request.method == 'POST':
        resposta_texto = request.POST.get('resposta')
        # Criação de uma nova instância de Resposta
        resposta = Resposta.objects.create(
            sugestao=sugestao,
            autor=request.user,  # O autor da resposta é o usuário atual
            resposta=resposta_texto
        )
        return redirect('listar_sugestoes')  # Redireciona de volta após responder

    return render(request, 'html/responder_sugestao_detalhes.html', {'sugestao': sugestao})


def get_google_maps_key(request):
    return JsonResponse({"key": settings.GOOGLE_MAPS_API_KEY})

def get_google_api_key(request):
    return JsonResponse({"key": settings.GOOGLE_API_KEY})

def teste6(request):
    return render(request, 'html/teste6.html')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()  # Acessando o perfil através da relação

def geocode(request):
    # Obtém o endereço enviado pelo front-end
    address = request.GET.get('q')
    if not address:
        return JsonResponse({'error': 'No address provided'}, status=400)

    # Faz a requisição para a API do Nominatim
    url = f"https://nominatim.openstreetmap.org/search?q={address}&countrycodes=BR&format=json&addressdetails=1&limit=5"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Gera uma exceção se o status for diferente de 200
        return JsonResponse(response.json(), safe=False)
    except requests.RequestException as e:
        return JsonResponse({'error': 'Error fetching data from Nominatim', 'details': str(e)}, status=500)

def home(request):
    return render(request, 'html/index.html')

def sucesso(request):
    return render(request, 'html/pagina_de_sucesso.html')

def teste5(request):
    return render(request, 'html/teste5.html')


def stream_updates(request):
    def event_stream():
        while True:
            distance = "12 km"  # Aqui, você pode calcular ou pegar de uma API real
            duration = "20 min"
            yield f"data: {json.dumps({'distance': distance, 'duration': duration})}\n\n"
            time.sleep(5)  # Atualiza a cada 5 segundos

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    return response

def autocomplete(request):
    input_text = request.GET.get('input', '')
    if not input_text:
        return JsonResponse({"error": "Input is required"}, status=400)

    url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
    params = {
        "input": input_text,
        "key": settings.GOOGLE_MAPS_API_KEY,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return JsonResponse(response.json())
    return JsonResponse({"error": "Failed to fetch autocomplete suggestions"}, status=500)


# views.py
def get_route(request):
    origin = request.GET.get('origin', '')
    destination = request.GET.get('destination', '')
    if not origin or not destination:
        return JsonResponse({"error": "Origin and destination are required"}, status=400)

    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": settings.GOOGLE_MAPS_API_KEY,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return JsonResponse(response.json())
    return JsonResponse({"error": "Failed to fetch route"}, status=500)




def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('mapa')
        else:
            login_form =AuthenticationForm()
            error_message = "Usuário ou senha inválidos."
            return render(request, 'html/login.html', {'login_form': login_form, 'error_message': error_message})
    else:
        login_form = AuthenticationForm()
    return render(request, 'html/login.html', {'login_form': login_form})


def index(request):
    return render(request, 'html/home.html')

def logout_view(request):
    auth_logout(request)  # Desloga o usuário
    return redirect('login')


def player(request):
    return render(request, 'html/player.html')
   


def premium(request):
    return render (request, 'html/premium.html')

@login_required
def premium_content(request):
    user_plan = request.user.profile.plan  # Obtém o plano do usuário

    if user_plan == 'free':
        template = 'html/free_plan.html'
    elif user_plan == 'basic':
        template = 'html/basic_plan.html'
    elif user_plan == 'premium':
        template = 'html/premium_plan.html'
    else:
        template = 'html/unknown_plan.html'  # Opcional para lidar com casos inesperados

    return render(request, template)

def testepremium(request):
    return render(request, 'html/teste5.html')


def teste(request):
    return render (request, 'html/teste.html')

def teste2(request):
    return render (request, 'html/teste2.html')

def teste4(request):
    return render (request, 'html/teste4.html')


OSRM_URL = "http://router.project-osrm.org/route/v1/driving"

def get_route(request):
    origin = request.GET.get('origin')  # Ex.: "longitude,latitude"
    destination = request.GET.get('destination')  # Ex.: "longitude,latitude"

    if not origin or not destination:
        return JsonResponse({'error': 'Parâmetros "origin" e "destination" são obrigatórios.'}, status=400)

    osrm_url = f"{OSRM_URL}/{origin};{destination}?overview=full&geometries=geojson"
    response = requests.get(osrm_url)

    if response.status_code != 200:
        return JsonResponse({'error': 'Erro ao obter rota do OSRM.'}, status=500)

    return JsonResponse(response.json())


def legenda(request):
    return render (request, 'html/legenda.html')

@login_required
def mp(request):
    return render (request, 'html/mapa.html')



@login_required
def contato(request):
    if request.user.is_staff or request.user.is_superuser:
        sugestoes = Sugestao.objects.all()
        resposta = None  # Inicializa 'resposta' para o caso de staff/superuser
    else:
        sugestoes = Sugestao.objects.filter(autor=request.user)
        resposta = Resposta.objects.filter(autor=request.user)
        
    return render(request, 'html/contato.html', {'sugestoes': sugestoes, 'resposta': resposta})

def donation(request):
    return render (request, 'html/donation.html')


@login_required
def minha_conta(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('minhaconta')
    else:
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'html/minhaconta.html', {
        'profile_form': profile_form,
    })


@login_required
def premium(request):
    user_plan = request.user.profile.plan  # Acessa o plano do usuário
    
    if user_plan == 'free':
        message = "Você está no plano gratuito. Atualize para acessar mais recursos."
    elif user_plan == 'basic':
        message = "Você está no plano básico. Aproveite nossos recursos adicionais."
    elif user_plan == 'premium':
        message = "Bem-vindo ao plano Premium! Aproveite todas as funcionalidades."
    elif user_plan == 'enterprise':
        message = "Você está no plano Empresarial. Recursos completos disponíveis."
    else:
        message = "Plano não reconhecido. Entre em contato com o suporte."

    return render(request, 'html/premium.html', {'message': message})



@login_required
def update_plan(request):
    try:
        # Requisição para pegar os dados da página
        html = requests.get('https://ondetemtiroteio.com/reportview.php').content
        soup = BeautifulSoup(html, 'html.parser')

        # Encontrar a tabela de ocorrências
        tabela = soup.find(class_='table-container')
        if tabela is None:
            return render(request, 'html/update_plan.html', {'erro': 'Tabela não encontrada'})

        # Lista para armazenar os locais com tiroteio
        locais_com_tiroteio = []
        ultima_ocorrencia = {}

        linhas = tabela.find_all('tr')

        for i, linha in enumerate(linhas):
            colunas = linha.find_all('td')

            if len(colunas) >= 5:
                ocorrencia = colunas[1].text.strip()
                if 'tiroteio' in ocorrencia.lower():
                    local = colunas[2].text.strip()
                    locais_com_tiroteio.append(local)
                    ultima_ocorrencia[local] = i  # Armazena o índice da última ocorrência

        # Contagem de frequência dos locais com tiroteio
        contagem_locais = Counter(locais_com_tiroteio)

        # Organizando a lista: primeiro pela contagem e depois pelo índice da última ocorrência
        locais_ordenados = sorted(contagem_locais.items(), key=lambda x: (-x[1], ultima_ocorrencia[x[0]]), reverse=False)

        # Organize a lista em um formato adequado para o template
        locais_com_tiroteio_ordenados = [local for local, _ in locais_ordenados]

        # Pega os 3 primeiros locais com tiroteio
        locais_com_tiroteio_ordenados = locais_com_tiroteio_ordenados[:3]

        
        return render(request, 'html/update_plan.html', {
            'locais_com_tiroteio_ordenados': locais_com_tiroteio_ordenados,
                })

    except Exception as e:
        return render(request, 'html/update_plan.html', {'erro': str(e)})


def teste3(request):
    return render (request, 'html/teste3.html')

def register(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('mapa')
    else:
        user_form =UserCreationForm()
    return render (request, 'html/register.html', { 'user_form': user_form})


def nominatim_proxy(request):
    query = request.GET.get('q', '')
    countrycodes = request.GET.get('countrycodes', 'BR')
    format_ = request.GET.get('format', 'json')
    addressdetails = request.GET.get('addressdetails', '1')
    limit = request.GET.get('limit', '5')
    viewbox = request.GET.get('viewbox', '')
    bounded = request.GET.get('bounded', '1')

    url = f"https://nominatim.openstreetmap.org/search"
    params = {
        'q': query,
        'countrycodes': countrycodes,
        'format': format_,
        'addressdetails': addressdetails,
        'limit': limit,
        'viewbox': viewbox,
        'bounded': bounded,
    }

    headers = {
        'User-Agent': 'SeuProjetoNome/1.0 (email@example.com)',
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return JsonResponse(response.json(), safe=False)
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)