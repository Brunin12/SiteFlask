import requests

def tom():
    url = "https://api.themoviedb.org/3/discover/movie"

    # Substitua 'SUA_CHAVE_DE_API_DO_TMDB' pela sua chave de API real
    api_key = 'af3279e78076bc5268a9739421acebff'

    # Parâmetros da consulta
    params = {
        'api_key': api_key,
        'with_people': '500',
        'language': 'pt-BR',
        'region': 'BR',
    }

    # Fazendo a requisição para a API
    response = requests.get(url, params=params)

    # Verificando se a resposta foi bem-sucedida
    if response.status_code == 200:
        # Convertendo a resposta para o formato JSON
        data = response.json()

        # Verificando se existem filmes na resposta
        if 'results' in data:
            filmes = data['results']
            print(filmes)
        else:
            return []
    else:
        print('Erro ao fazer a requisição à API do TMDB.')
        return []

tom()
