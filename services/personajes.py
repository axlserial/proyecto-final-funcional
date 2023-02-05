from typing import Callable
from payload import generate_payload
import requests

# Clousure que devuelve una función según lo que se quiere obtener
def get_data(type: str) -> Callable:
    def get_personajes() -> dict:
        payload = generate_payload()
        # Hace la petición
        response = requests.get('https://gateway.marvel.com:443/v1/public/personajes',params=payload)

        # Si la petición es correcta
        if response.status_code == 200:
            # Devuelve los comics
            return response.json()['data']['results']

        # Si la petición no es correcta
        else:
            # Devuelve un diccionario vacío
            return {}
    
    if type == 'personajes':
        return get_personajes
    else:
        return None

print(get_data("personajes"))