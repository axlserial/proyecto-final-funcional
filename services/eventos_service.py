from typing import Callable
from .payload import generate_payload
import requests

def get_events(pagination: dict[str, int] = {'limit': 10, 'offset': 0}):
    def get_data():
        payload = generate_payload()

        # Hace la petición
        response = requests.get(
            'https://gateway.marvel.com:443/v1/public/events', params=payload)

        result: dict = {}
        

        # Si la petición es correcta
        if response.status_code == 200:
            result = response.json()['data']

        return result

    return get_data