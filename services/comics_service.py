from typing import Callable
from .payload import generate_payload
import requests


# Clousure que devuelve una función según lo que se quiere obtener
def get_data(type: str) -> Callable:
    if type == 'comics':
        return get_comics
    else:
        return None


# Función para obtener los comics
def get_comics() -> dict:

    payload = generate_payload()
    # Hace la petición
    response = requests.get('https://gateway.marvel.com:443/v1/public/comics',
                            params=payload)

    # Si la petición es correcta
    if response.status_code == 200:
        # Devuelve los comics
        return response.json()['data']['results']

    # Si la petición no es correcta
    else:
        # Devuelve un diccionario vacío
        return {}