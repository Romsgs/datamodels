# auth.py
import requests
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def get_access_token():
    """
    Obtém o token de acesso usando o fluxo de credenciais do cliente OAuth 2.0.
    """
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("CLIENT_ID e CLIENT_SECRET devem ser definidos no arquivo .env")

    url = 'https://developer.api.autodesk.com/authentication/v2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials',
        'scope': 'account:read data:read'
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        access_token = response.json()['access_token']
        return access_token
    else:
        print('Falha ao obter o token de acesso:', response.text)
        return None
