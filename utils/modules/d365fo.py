from http import client
import json
import requests


class D365FOConnection():
    def __init__(self):
        self._d365fo_url = None
        self._client_id = None
        self._client_id_secret = None
        self.bearer = None
        self.AUTH_URL = "https://login.windows.net/microsoft.com/oauth2/token"

    @property
    def d365fo_url(self) -> None:
        pass
    
    @d365fo_url.setter
    def d365fo_url(self, d365fo_url):
        
        d365fo_url = d365fo_url.replace("https://", "")
        d365fo_url = f'https://{d365fo_url}'
        self._d365fo_url = d365fo_url

    @property
    def client_id(self) -> None:
        pass
    
    @client_id.setter
    def client_id(self, client_id):
        self._client_id = client_id

    @property
    def client_id_secret(self) -> None:
        pass
    
    @client_id_secret.setter
    def client_id_secret(self, client_id_secret):
        self._client_id_secret = client_id_secret

        """Returns True if connection was succesfull
        """
    def try_connection(self):
        auth_headers = {
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "client_secret": self._client_id_secret,
            "resource": self._d365fo_url
        }
        try:
            r = requests.post(self.AUTH_URL, data=auth_headers)
            self.bearer = r.json()["access_token"]
        except:
            return False
        if self.bearer is None:
            return False
        else:
            return True
        
    def get_d365fo_collection(self, collection_name, query_params="", ):
        url = f"{self._d365fo_url}/data/{collection_name}?{query_params}"
        auth_bearer = { "Authorization": f'Bearer {self.bearer}'}
        r = requests.get(url, headers=auth_bearer)
        return r.json()["value"]
    
    def get_d365fo_from_url(self, url):
    
        auth_bearer = { "Authorization": f'Bearer {self.bearer}'}
        r = requests.get(url, headers=auth_bearer)
        return r.json()["value"]
            