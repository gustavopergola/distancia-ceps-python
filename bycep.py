import requests
from collections import namedtuple
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import random

# Estrutura auxiliar para passar coordenadas tipadas
Coordenadas = namedtuple("Coordenadas", "latitude longitude")

# inicia o geolocator do geopy
geolocator = Nominatim(user_agent="GetDistanceBetweenCeps" + str(random.randint(0,100000)))
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def format_endereco(endereco, sem_logradouro=False):
    logradouro = endereco['street'] + ", "
    if sem_logradouro:
        logradouro = ''

    return logradouro + endereco['neighborhood'] + ", " + endereco['city'] + " - " + endereco['state']

def address_from_cep(cep: str):
    # busca o endereco ou coordenada pelo CEP
    response = requests.get(f'https://brasilapi.com.br/api/cep/v2/{cep}') 
    
    # caso a request não dê certo, puxa a mensagem de erro e mostra. Se não tiver mensagem, mostra "api error"
    if response.status_code != 200:
        err = response.json() 
        raise Exception(f"could not find CEP! Error: {err.get('message', 'api error')}")

    endereco = response.json()
    
    # Pega as informações de coordenadas direto da brasilapi se estiverem presentes. 
    # Muitas vezes não está, então retorna None quando for esse caso
    coordenadas = endereco.get('location', {}).get('coordinates', None)

    # removendo conteúdo dos correios indicando qual é o lado da rua pelo CEP
    endereco['street'] = endereco['street'].split(" lado ")[0] 

    # formata o endereço para ficar apropriado apra o geopy
    return endereco, coordenadas


def lat_long_from_cep(cep: str) -> Coordenadas:
    # busca CEP e faz um catch exception caso a request não tenha funcionado como esperado
    try:
        endereco, coord = address_from_cep(cep)
    except Exception as e:
        print(e)
        return None, None

    # Se as coordenadas estiverem presentes pela BrasilAPI, use-as. Caso contrário, busque no Geopy pelo enderedeço
    if coord and len(coord) > 0:
        location = Coordenadas(**coord)
    else:
        geopy_loc = geocode(format_endereco(endereco))
        
        # tentando novamente só com o bairro ao invés da rua quando não achar
        if not geopy_loc:
            geopy_loc = geocode(format_endereco(endereco, sem_logradouro=True))

        location = geopy_loc.point if geopy_loc else None

    if not location:
        print(f"both brasilAPI and geopy failed to find location for CEP: {cep}")
        return None, None

    return location.latitude, location.longitude


# utilizando o método de ir de CARRO para calcular rotas entre os CEPS
def distancia_metros_entre_ceps(origem: str, destino: str):
    lat1, long1 = lat_long_from_cep(origem)
    lat2, long2 = lat_long_from_cep(destino)

    # se por acaso não achou as coordenadas de um dos dois ceps, retorna nulo
    if not lat1 or not lat2:
        return None

    response = requests.get(f'https://routing.openstreetmap.de/routed-car/route/v1/driving/{long1},{lat1};{long2},{lat2}?overview=false')
    
    # Nem sempre o OSMR responde OK
    if response.status_code != 200:
        print(f"error on request to OSMR {cep1} e {cep2}")
        return None

    # Verifica se achou rotas entre os dois ceps. 
    # Pode não encontrar quando distancia muito curta ou muito longa ou não tem rotas entre os ceps
    rotas = response.json()
    if not len(rotas['routes']) > 0:
        print(f"Nenhuma rota entre os dois ceps {cep1} e {cep2} foi encontrada")
        return None

    return rotas['routes'][0]['distance']
