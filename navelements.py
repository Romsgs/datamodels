# navelements.py

import requests
import pandas as pd
from auth import get_access_token

def make_api_request(url):
    """
    Realiza uma requisição à API Autodesk com o token de acesso e retorna os dados JSON.

    Parâmetros:
    - url (str): O endpoint da API para a requisição.

    Retorna:
    - dict: Dados JSON da resposta da API, ou None em caso de falha.
    """
    access_token = get_access_token()
    if not access_token:
        return None

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/vnd.api+json'
    }

    response = requests.get(url, headers=headers)
    print(response)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print(f'Falha na requisição (Status {response.status_code}):', response.text)
        return None

def extract_attributes(items):
    """
    Extrai atributos relevantes de uma lista de itens e retorna uma lista de dicionários.

    Parâmetros:
    - items (list): Lista de itens JSON obtidos da API.

    Retorna:
    - list: Lista de dicionários com os atributos extraídos.
    """
    return [
        {
            'id': item.get('id'),
            'name': item.get('attributes', {}).get('name'),
            'type': item.get('type'),
            'create_time': item.get('attributes', {}).get('createTime'),
            'last_modified_time': item.get('attributes', {}).get('lastModifiedTime'),
        }
        for item in items
    ]

def get_top_folders(project_id):
    """
    Obtém as pastas de nível superior de um projeto e retorna um DataFrame do pandas.

    Parâmetros:
    - project_id (str): O ID do projeto do qual obter as pastas.

    Retorna:
    - pandas.DataFrame: DataFrame contendo as pastas de nível superior.
    """
    print("preparando o get top folders")
    url = f'https://developer.api.autodesk.com/project/v1/projects/{project_id}/topFolders'
    folders_data = make_api_request(url)
    folders_data_df = pd.DataFrame(folders_data)
    print("isso eh folders data:")
    print(folders_data_df.head())
    if folders_data is not None:
        folders_list = extract_attributes(folders_data)
        
        return pd.DataFrame(folders_list)
    else:
        return None

def get_folder_contents(project_id, folder_id):
    """
    Obtém o conteúdo de uma pasta específica dentro de um projeto e retorna um DataFrame do pandas.

    Parâmetros:
    - project_id (str): O ID do projeto.
    - folder_id (str): O ID da pasta da qual obter o conteúdo.

    Retorna:
    - pandas.DataFrame: DataFrame contendo os itens e subpastas da pasta.
    """
    url = f'https://developer.api.autodesk.com/data/v1/projects/{project_id}/folders/{folder_id}/contents'
    contents_data = make_api_request(url)
    if contents_data is not None:
        contents_list = extract_attributes(contents_data)
        return pd.DataFrame(contents_list)
    else:
        return None
