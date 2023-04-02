# Busca distancia entre CEPS  

Utilizando python 3.9.10, não testado em demais versões

## Como executar  
    pip install geopy
    pip install pandas
    python exemplo.py


## Utilização
Consulte o arquivo exemplo.py para o uso em um dataframe

    from bycep import distancia_metros_entre_ceps
    distancia = distancia_metros_entre_ceps('cep_origem', 'cep_destino')
    print(distancia)

# Notas
- Caso a brasilAPI não responda diretamente a geolocalização do CEP, a busca é executada no geopy
- Caso o geopy também não encontre, busca pelo bairro ao invés do logradouro específico
- Usa o OSRM para buscar rotas até o destino viajando de **carro**, trazendo apenas a distância entre os dois pontos
- O tempo que leva entre um ponto e outro também é retornado pela API do OSRM mas não abordado nas funções, basta capturar a informação e retornar


## APis usadas
- Utilizando BrasilAPI para consulta de CEPs em endereços (https://brasilapi.com.br/)
- Uitlizando geopy  para consulta de geolocalização quando não providenciada pela BrasilAPI (https://geopy.readthedocs.io/en/stable/) que utiliza o open-street-map
- Utilizando OSRM para descobrir rotas entre geolocalizações (https://project-osrm.org/)