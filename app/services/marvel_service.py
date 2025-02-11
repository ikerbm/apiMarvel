import requests
import os
import hashlib

#la url de la pagina donde se hacen las consultas, y las llaves necesarias para construir el hash que se solicita
MARVEL_API_URL = "http://gateway.marvel.com/v1/public/characters"
PUBLIC_KEY = os.getenv("MARVEL_PUBLIC_KEY", "21e747281799536f07f2088ee1596574")
PRIVATE_KEY = os.getenv("MARVEL_PRIVATE_KEY", "ebda728eb54e983a20493b770db9de0f01fcd6de")

#Hacemos la comunicacion con la api de marvel, el parametro name es que usaremos para buscar
def get_character_from_marvel(name):
    params = {
        "name": name,
        "apikey": PUBLIC_KEY,
    }
    response = requests.get(MARVEL_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["data"]["results"]:
            character = data["data"]["results"][0]
            return {
                "marvel_id": character["id"],
                "name": character["name"],
                "description": character.get("description", "No description available"),
                "comics": [comic["name"] for comic in character["comics"]["items"]]
            }
    return None
