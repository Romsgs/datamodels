# gethubs.py

import requests
import pandas as pd
from auth import get_access_token

def get_hubs():
    """
    Obtém a lista de hubs usando o token de acesso e retorna um DataFrame do pandas.
    """
    access_token = get_access_token()
    if not access_token:
        return None

    url = 'https://developer.api.autodesk.com/project/v1/hubs'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/vnd.api+json'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        hubs_data = response.json().get('data', [])
        hubs_list = []
        for hub in hubs_data:
            attributes = hub.get('attributes', {})
            hub_info = {
                'id': hub.get('id'),
                'name': attributes.get('name'),
                'type': hub.get('type'),
                'hub_type': attributes.get('extension', {}).get('type'),
                'create_time': attributes.get('createTime'),
                'last_modified_time': attributes.get('lastModifiedTime'),
            }
            hubs_list.append(hub_info)
        hubs_df = pd.DataFrame(hubs_list)
        return hubs_df
    else:
        print(f'Falha ao obter os hubs (Status {response.status_code}):', response.text)
        return None
