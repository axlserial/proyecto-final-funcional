from .payload import generate_payload
import requests


# Clousure para obtener a los creators
def get_creators(extra_params: dict[str, int]):

    def get_data():
        payload = generate_payload()

        # Añade los parámetros extra
        payload.update(extra_params)

        # Hace la petición
        response = requests.get(
            'https://gateway.marvel.com:443/v1/public/creators', params=payload)

        # Impresión de la petición
        print(f"Request: {response.url}\n")

        result: dict = {}

        # Si la petición es correcta
        if response.status_code == 200:
            result = response.json()['data']

        return result

    return get_data