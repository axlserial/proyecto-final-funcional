from typing import Callable
from .payload import generate_payload
import requests

# Clousure que devuelve una función según lo que se quiere obtener
def get_data(type: str) -> Callable:
    def get_stories():
        payload = generate_payload()
        # Hace la petición
        payload['limit'] = 81
        response = requests.get('https://gateway.marvel.com:443/v1/public/stories',params=payload)
        # Si la petición es correcta
        if response.status_code == 200:
            # Devuelve los comics
            #return response.json()['data']['results']
            return [{"id":data['id'],"nombre":data['title'],"comics":list(map(lambda x : x['name'],data['comics']['items'])), "Creadores": list(map(lambda x : x['name'],data['creators']['items'])), "Series" : list(map(lambda x : x['name'],data['series']['items']))} for data in response.json()['data']['results']]

        # Si la petición no es correcta
        else:
            # Devuelve un diccionario vacío
            return {}
    
    if type == 'stories':
        return get_stories
    else:
        return None

#for i in get_data("stories")():
#    print(i)
#    print("-----------")