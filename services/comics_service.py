from typing import Callable
from .payload import generate_payload
import requests


# Clousure para obtener los comics
def get_comics(pagination: dict[str, int]):

    def get_data():
        payload = generate_payload()

        # Añade la paginación
        payload.update(pagination)

        # Hace la petición
        response = requests.get(
            'https://gateway.marvel.com:443/v1/public/comics', params=payload)

        result: dict = {}

        # Si la petición es correcta
        if response.status_code == 200:
            result = response.json()['data']

        return result

    return get_data