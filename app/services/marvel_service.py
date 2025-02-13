import os
import hashlib
import urllib

import requests
from dotenv import load_dotenv

load_dotenv()
#la url de la pagina donde se hacen las consultas, y las llaves necesarias para construir el hash que se solicita
MARVEL_API_URL = "http://gateway.marvel.com/v1/public"
                  #"/characters"

PUBLIC_KEY = os.getenv("MARVEL_PUBLIC_KEY")
PRIVATE_KEY = os.getenv("MARVEL_PRIVATE_KEY")
class MarvelService:
    contador = 1 #contador para el timestap

    @classmethod
    def get_character_from_marvel(cls,name):
        #consulta un personaje en la api de marvel y devueve los datos como json
        ts = cls.contador
        prehash = f"{ts}{PRIVATE_KEY}{PUBLIC_KEY}"
        params = {
            "name": name,
            "apikey": PUBLIC_KEY,
            "ts":ts,
            "hash": hashlib.md5(prehash.encode()).hexdigest()
        }

        #creamos la url para la consulta de los personajes
        url = f"{MARVEL_API_URL}/characters"
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            cls.contador += 1
            return data
        elif response.status_code == 404:
            return {"status_code": 404, "message": "perosnaje no encontrado"}
        else:
            return {"status_code": response.status_code, "message": "error" }

