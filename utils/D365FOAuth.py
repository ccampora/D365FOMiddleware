import json
import requests
import logging

# REPLACE HERE
D365FOENV_URL = "<D365FO URL without trailing slash>"
CLIENT_APP_ID = "Client App Id"
SECRET = "Client App Secret"

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

AUTH_URL = "https://login.windows.net/microsoft.com/oauth2/token"
URLS = {
    "MetadataEntities": f'{D365FOENV_URL}/Metadata/DataEntities',
    "CustomersV2": f'{D365FOENV_URL}/data/CustomersV2?$format=json&cross-company=true'
}

def pretty_json(ugly_json):
    return json.dumps(ugly_json, indent=2)

def query_d365fo(url, bearer):
    auth_bearer = { "Authorization": f'Bearer {bearer}'}
    r = requests.get(url, headers=auth_bearer)
    jsonResponse = r.json()
    print(pretty_json(jsonResponse))

auth_headers = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_APP_ID,
    "client_secret": SECRET,
    "resource": D365FOENV_URL
}

r = requests.post(AUTH_URL, data=auth_headers)
bearer = r.json()["access_token"]

# Print Collection

for entity, url in URLS.items():
    query_d365fo(url, bearer=bearer)