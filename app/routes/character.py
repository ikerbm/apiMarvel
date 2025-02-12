from flask import Blueprint,abort,jsonify
from app.models.character import Character
from app.models.comic import Comic
from app.utils.db import db
from app.services.marvel_service import MarvelService

#el blueprint ayuda a evitar conflictos con el codigo de los route
character_bp = Blueprint("character_bp", __name__)
#Hacemos la comunicacion con la api de marvel, el parametro name es que usaremos para buscar
#/<name> es un parametro que entra a la url
@character_bp.route("/<name>",methods=["GET"])
def get_character(name):
    #obtenemos el personaje de marvel y se almacena en la BD
    data = MarvelService.get_character_from_marvel(name)

    if "status_code" in data:
        return jsonify(data),data["status_code"]

    if data["data"]["results"]:
        marvel_data = data["data"]["results"][0]

        #verificar si el personaje ya existe en la BD
        character = Character.query.filter_by(marvel_id=marvel_data["id"]).first()
        if not character:
            character = Character(
                name=marvel_data["name"],
                marvel_id=marvel_data["id"],
                description=marvel_data["description"]
            )
            db.session.add(character)
            db.session.commit()

            #guardar comics del personaje
            comics = marvel_data["comics"]["items"]
            for comic in comics:
                new_comic = Comic(name=comic["name"],character_id=character.id)
                db.session.add(new_comic)

            db.session.commit()
        return jsonify(character.to_dict()),200
    else:
        return jsonify({"error":"no character"}),404
