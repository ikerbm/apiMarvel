from flask import Blueprint,abort
from app.models.character import Character
import hashlib
import requests
import os


from app.models.comic import Comic

#el contador formara parte del ts
contador = 1
#la url de la pagina donde se hacen las consultas, y las llaves necesarias para construir el hash que se solicita

MARVEL_API_URL = "http://gateway.marvel.com/v1/public/characters"
PUBLIC_KEY = os.getenv("MARVEL_PUBLIC_KEY", "21e747281799536f07f2088ee1596574")
PRIVATE_KEY = os.getenv("MARVEL_PRIVATE_KEY", "ebda728eb54e983a20493b770db9de0f01fcd6de")

#el blueprint ayuda a evitar conflictos con el codigo de los route
character_bp = Blueprint("character_bp", __name__)
#Hacemos la comunicacion con la api de marvel, el parametro name es que usaremos para buscar
#/<name> es un parametro que entra a la url
@character_bp.route("/<name>")
def get_character_from_marvel(name):
    global contador
    ts = contador
    prehash= f"{str(ts)}{PRIVATE_KEY}{PUBLIC_KEY}"
    #son los parametros que solicita la api marvel para poder hacer comunicacion con ella
    params = {
        "name": name,
        "apikey": PUBLIC_KEY,
        "ts": ts,
        "hash": hashlib.md5(prehash.encode()).hexdigest()
    }

    response = requests.get(MARVEL_API_URL, params=params)
    if response.status_code == 404:
        abort(404)
    elif response.status_code == 200:
        #almacenamos los datos de la api marvel como un json en la variable data para sacar los datos mas adelante
        data = response.json()
        character = Character()
        if len(data["data"]["results"]) > 0:
            character.name = data["data"]["results"][0]["name"]
            character.marvel_id = data["data"]["results"][0]["id"]
            character.description = data["data"]["results"][0]["description"]
            current_character=character.save()
            comics = data["data"]["results"][0]["comics"]["items"]
            #dado que un personaje puede estar en varios comics, creamos los comics en una tabla aparte
            for comic in comics:
                new_comic = Comic()
                new_comic.name = comic["name"]
                new_comic.character_id = current_character.id
                new_comic.save()
            #el contador forma parte del hash
            contador += 1
            return data
        else:
            return {"status_code": 404, "message": "No se encontrado ningun personaje"}
    else:
        return {"status_code": response.status_code, "message": "error, contacte a su administrador"}

