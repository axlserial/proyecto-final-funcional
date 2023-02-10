from typing import Callable
from .payload import generate_payload
import requests

def get_series(pagination: dict[str, int]):
    def get_data():
        payload = generate_payload()
        
		# Añade los parámetros de paginación
        payload.update(pagination)

        # Hace la petición
        response = requests.get(
            'https://gateway.marvel.com:443/v1/public/series', params=payload)

        
		# Impresión de la petición
        print(f"Request: {response.url}\n")

        result: dict = {}
        

        # Si la petición es correcta
        if response.status_code == 200:
            result = response.json()['data']

        return result

    return get_data