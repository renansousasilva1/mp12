// Inicializa o mapa
const map = L.map('map').setView([-23.000372, -43.365894], 10);
  
    // Adiciona o layer base com fundo preto e texto branco
L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}{r}.png', {
          attribution: '&copy; OpenStreetMap contributors & CartoDB',
          subdomains: 'abcd',
          maxZoom: 19,
          opacity: 1.0 // Garante fundo completamente preto
    }).addTo(map);
  
    // Adiciona um círculo azul para a localização do usuário
var userMarker = L.circleMarker([0.0, -0.09], {
      radius: 10,
      fillColor: "#0f356b",
      color: "#3388ff",
      weight: 1,
      opacity: 1,
      fillOpacity: 0.5
}).addTo(map);
  
    // Função para atualizar a localização do usuário
function updateLocation(position) {
      var lat = position.coords.latitude;
      var lon = position.coords.longitude;
  
      // Atualiza a posição do marcador
    userMarker.setLatLng([lat, lon]);
    map.setView([lat, lon], 13); // Centraliza o mapa na nova posição
    }
  
    // Função para lidar com erros de geolocalização
    function handleError(error) {
      console.warn(`ERRO (${error.code}): ${error.message}`);
    }
  
    // Solicita a localização do usuário
    if (navigator.geolocation) {
      navigator.geolocation.watchPosition(updateLocation, handleError, {
        enableHighAccuracy: true,
        maximumAge: 30000,
        timeout: 10000
      });
    } else {
      alert("Geolocalização não é suportada por este navegador.");
    }
  
    // Função para redirecionar o mapa para a localização do usuário
    function locateUser() {
      // Obtém a última posição conhecida do marcador
      var latLng = userMarker.getLatLng();
  
      // Centraliza o mapa na última localização do usuário
      map.setView(latLng, 16); // Redefine o zoom e a localização
    }
  
    // Posiciona o controle de zoom no canto inferior direito
    map.zoomControl.setPosition('bottomright');

  
  
  
  const kmzUrls = [
      '/static/app/5m.kmz',
      '/static/app/ada.kmz',
      '/static/app/tcp.kmz',
      '/static/app/cv.kmz'
  ];

          // Função para definir o ícone padrão para a camada
      function getDefaultIcon(layerName) {
          let iconUrl;
      
          // Definindo ícones específicos para cada camada
          const iconConfig = {
              'Camada 1': '/static/5m.png',  // Ícone específico para camada 1
              'Camada 2': '/static/ada.png',  // Ícone específico para camada 2
              'Camada 3': '/static/tcp.png',  // Ícone específico para camada 3
              'Camada 4': '/static/cv.png',   // Ícone específico para camada 4
              
          };
  
          // Retorna o ícone da camada ou um ícone padrão
          iconUrl = iconConfig[layerName] || '/static/default-icon.png';  // Ícone padrão se a camada não estiver configurada
  
          return L.icon({
              iconUrl: iconUrl,
              iconSize: [40, 40],  // Tamanho do ícone
              iconAnchor: [12, 41],  // Posição do ícone no marcador
              popupAnchor: [1, -34]  // Posição do popup em relação ao ícone
          });
      }
  
      // Função para carregar o KMZ e adicionar ao mapa
      function loadKmzLayer(kmzUrl, layerName) {
          fetch(kmzUrl)
              .then(response => response.arrayBuffer())  // Carrega o KMZ como um ArrayBuffer
              .then(buffer => {
                  const zip = new JSZip();
                  return zip.loadAsync(buffer);  // Descompacta o arquivo KMZ
              })
              .then(zip => {
                  // Encontra o arquivo KML dentro do KMZ
                  const kmlFile = Object.keys(zip.files).find(fileName => fileName.endsWith('.kml'));
                  if (!kmlFile) throw new Error('Arquivo KML não encontrado no KMZ');
                  return zip.files[kmlFile].async('text');
              })
              .then(kmlText => {
                  const parser = new DOMParser();
                  const kml = parser.parseFromString(kmlText, 'text/xml');  // Converte o KML para XML
                  const geojson = toGeoJSON.kml(kml);  // Converte KML para GeoJSON
  
                  // Cria a camada GeoJSON a partir do GeoJSON
                  const geoJsonLayer = L.geoJSON(geojson, {
                      style: feature => ({
                          color: feature.properties.stroke || 'blue',
                          fillColor: feature.properties.fill || 'blue',
                          fillOpacity: feature.properties['fill-opacity'] || 0.250,
                          weight: feature.properties['stroke-width'] || 2
                      }),
                      pointToLayer: function (feature, latlng) {
                          // Chama a função para obter o ícone padrão para a camada
                          const icon = getDefaultIcon(layerName);
                          
                          // Cria o marcador com o ícone
                          return L.marker(latlng, { icon: icon });
                      },
                      onEachFeature: (feature, layer) => {
                          const props = feature.properties || {};
                          if (props.name || props.description) {
                              layer.bindPopup(`<b>${props.name || 'Sem nome'}</b><br>${props.description || 'Sem descrição'}`);
                          }
                      }
                  });
  
                  // Adiciona a camada GeoJSON ao mapa
                  geoJsonLayer.addTo(map);
  
                  
              })
              .catch(error => console.error('Erro ao processar o KMZ:', error));  // Tratamento de erro
      }
  
      // Objeto para armazenar as camadas de sobreposição
      const overlayMaps = {};
  
      // Carregar todos os arquivos KMZ como camadas separadas
      kmzUrls.forEach((url, index) => {
          loadKmzLayer(url, `Camada ${index + 1}`);
      });
 

  
    
    
      const originInput = document.getElementById('origin');
      const suggestionsBox = document.getElementById('autocomplete-suggestions');
      // Evento para capturar as teclas digitadas
      originInput.addEventListener('input', function () {
          const query = originInput.value.trim();
          if (query.length < 3) {
              suggestionsBox.style.display = 'none';
              return;
          }
      
          // Faz a chamada à API do Nominatim para buscar sugestões
          fetch(`https://nominatim.openstreetmap.org/search?q=Rio de Janeiro&countrycodes=BR&format=json&q=${encodeURIComponent(query)}&addressdetails=1&limit=5`)
              .then(response => response.json())
              .then(data => {
                  if (data.length === 0) {
                      suggestionsBox.style.display = 'none';
                      return;
                  }
      
                  // Limpa sugestões anteriores
                  suggestionsBox.innerHTML = '';
      
                  // Exibe novas sugestões
                  data.forEach(item => {
                      const suggestion = document.createElement('div');
                      suggestion.textContent = item.display_name;
                      suggestion.dataset.lat = item.lat;
                      suggestion.dataset.lon = item.lon;
                      suggestionsBox.appendChild(suggestion);
                  });
      
                  suggestionsBox.style.display = 'block';
              })
              .catch(err => console.error('Erro ao buscar sugestões:', err));
      });
      
      // Evento para selecionar uma sugestão
      suggestionsBox.addEventListener('click', function (e) {
          if (e.target && e.target.dataset.lat && e.target.dataset.lon) {
              const selectedSuggestion = e.target.textContent;
              const lat = e.target.dataset.lat;
              const lon = e.target.dataset.lon;
      
              // Preenche o campo de pesquisa com a sugestão selecionada
              originInput.value = selectedSuggestion;
      
              // Centraliza o mapa na localização selecionada
              map.setView([lat, lon], 14);
      
              // Oculta o box de sugestões
              suggestionsBox.style.display = 'none';
          }
      });
      
      // Oculta as sugestões se clicar fora do campo ou do dropdown
      document.addEventListener('click', function (e) {
          if (!originInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
              suggestionsBox.style.display = 'none';
          }
      });
      
      
      
          const routeIcon = document.getElementById('route-icon');
          const routeBar = document.getElementById('route-bar');
      
          routeIcon.addEventListener('click', () => {
              routeBar.style.display = routeBar.style.display === 'flex' ? 'none' : 'flex';
          });
      
          let currentRouteLayer = null; // Variável global para armazenar a camada atual da rota
      
      document.getElementById('find-route').addEventListener('click', () => {
      const origin = document.getElementById('origin').value;
      const destination = document.getElementById('destination').value;
      
      if (!origin || !destination) {
          alert('Por favor, preencha o ponto de origem e destino.');
          return;
      }
      
      // Usa a API de geocodificação do Nominatim para converter endereços em coordenadas
      const geocodeURL = (address) =>
          `https://nominatim.openstreetmap.org/search?q=Rio de Janeiro&countrycodes=BR&format=json&q=${encodeURIComponent(address)}`;
      
      Promise.all([
          fetch(geocodeURL(origin)).then(res => res.json()),
          fetch(geocodeURL(destination)).then(res => res.json())
      ])
      .then(([originData, destinationData]) => {
          if (originData.length === 0 || destinationData.length === 0) {
              alert('Não foi possível localizar um dos endereços.'); return; }
              const originCoords = [originData[0].lat, originData[0].lon];
              const destinationCoords = [destinationData[0].lat, destinationData[0].lon];
          
              // Chamada à API OSRM para calcular a rota
              const routeURL = `https://router.project-osrm.org/route/v1/driving/${originCoords[1]},${originCoords[0]};${destinationCoords[1]},${destinationCoords[0]}?overview=full&geometries=geojson`;
          
              return fetch(routeURL)
                  .then(res => res.json())
                  .then(routeData => {
                      if (routeData.routes.length === 0) {
                          alert('Nenhuma rota encontrada.');
                          return;
                      }
          
                      // Remove a rota anterior (se existir)
                      if (currentRouteLayer) {
                          map.removeLayer(currentRouteLayer);
                      }
          
                      // Adiciona a nova rota ao mapa
                      const route = routeData.routes[0].geometry;
                      currentRouteLayer = L.geoJSON(route, {
                          style: {
                              color: 'blue',
                              weight: 4
                          }
                      }).addTo(map);
          
                      // Centraliza o mapa na nova rota
                      map.fitBounds(currentRouteLayer.getBounds());
                  });
          })
          .catch(error => console.error('Erro ao traçar a rota:', error));
          
      });
      