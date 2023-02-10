from typing import Callable
from .payload import generate_payload
import requests

# Clousure que devuelve una función según lo que se quiere obtener
def get_data(type: str) -> Callable:
    def get_personajes():
        payload = generate_payload()
        # Hace la petición
        payload['limit'] = 81
        response = requests.get('https://gateway.marvel.com:443/v1/public/characters',params=payload)
        # Si la petición es correcta
        if response.status_code == 200:
            # Devuelve los comics
            #return response.json()['data']['results']
            return [{"id":data['id'],"nombre":data['name'],"descripcion":data['description'],
            "imagen":data['thumbnail']['path']+"."+data['thumbnail']['extension'],
            "comics":list(map(lambda x : x['name'],data['comics']['items']))} 
            for data in response.json()['data']['results']]

        # Si la petición no es correcta
        else:
            # Devuelve un diccionario vacío
            return {}
    
    if type == 'personajes':
        return get_personajes
    else:
        return None


#a = get_data("personajes")
#for i in a():
#    print(i['storiesTypes'])
#    print("---------------------")