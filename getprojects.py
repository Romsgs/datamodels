# getprojects.py

import requests
import pandas as pd
from auth import get_access_token

def get_projects(hub_id):
    """
    Retrieves the list of projects from a specific hub and returns a pandas DataFrame.

    Parameters:
    - hub_id (str): The ID of the hub to get projects from.

    Returns:
    - pandas.DataFrame: DataFrame containing the projects.
    """
    access_token = get_access_token()
    if not access_token:
        print("Access token not found.")
        return None

    url = f'https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/vnd.api+json'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f'Failed to get projects (Status {response.status_code}): {response.text}')
        return None

    projects_data = response.json().get('data', [])
    if not projects_data:
        print('No projects found.')
        return None

    # Use pandas.json_normalize for efficient DataFrame creation
    projects_df = pd.json_normalize(projects_data)

    # Renomear colunas para facilitar o acesso
    projects_df.rename(columns=lambda x: x.replace('attributes.', ''), inplace=True)
    projects_df.rename(columns=lambda x: x.replace('relationships.', ''), inplace=True)
    projects_df.rename(columns=lambda x: x.replace('extension.', ''), inplace=True)

    if projects_df.empty:
        print('No projects found after processing data.')
        return None
    return projects_df
