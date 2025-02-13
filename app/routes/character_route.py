from flask import Blueprint,jsonify,render_template
from app.models.character_model import Character
from app.models.comic_model import Comic
from app.utils.db import db
from app.services.marvel_service import MarvelService

def create_img_url(marvel_data):
    # creacion del url de la imagen del heroe
    img_extension = marvel_data["thumbnail"]["extension"]
    img_path = marvel_data["thumbnail"]["path"]
    img_url = f"{img_path}.{img_extension}"
    return img_url
#el blueprint ayuda a evitar conflictos con el codigo de los route
character_bp = Blueprint("character_bp", __name__)
#Hacemos la comunicacion con la api de marvel, el parametro name es que usaremos para buscar
#/<name> es un parametro que entra a la url
@character_bp.route("/<name>",methods=["GET"])
def get_character(name):
    #validamos que el nombre no este vacio
    if not name or not isinstance(name,str):
        return jsonify({"error" : "el parametro 'name' es invalido o esta vacio"}),400

    try:
        #obtenemos el personaje de marvel y se almacena en la BD
        data = MarvelService.get_character_from_marvel(name)
        #si la api de marvel devuelve un error, manejarlo
        if "status_code" in data:
            return jsonify(data),data["status_code"]
        #verificamos si hay resultados
        if not data["data"]["results"]:
            return jsonify({"error" : "personaje no encontrado en la API de marvel"}),404

        marvel_data = data["data"]["results"][0]
        #verificar si el personaje ya existe en la BD
        character = Character.query.filter_by(marvel_id=marvel_data["id"]).first()

        if not character:
            #creamos un nuevo personaje en la BD
            character = Character(
                name=marvel_data["name"],
                marvel_id=marvel_data["id"],
                description=marvel_data["description"],
                image_url=create_img_url(marvel_data)

            )
            db.session.add(character)
            db.session.commit()

            #guardar comics del personaje
            comics = marvel_data["comics"]["items"]
            for comic in comics:
                new_comic = Comic(name=comic["name"],character_id=character.id)
                db.session.add(new_comic)

            db.session.commit()

            #devolver el codigo 201 (created) cuando se crea un nuevo recurso
            return jsonify(character.to_dict()),201
        else:
            character.name = marvel_data["name"],
            character.description = marvel_data["description"]
            character.image_url = create_img_url(marvel_data)
            db.session.commit()
            #devolver el codigo 200 (ok) cuando el personaje ya existe
            return jsonify(character.to_dict()),200
    except Exception as e:
        #manejar errores inesperados
        return jsonify({"error" : "Ocurrio un erro inetrno en el servidor","details":str(e)}),500

#ruta para mostrar la lista de personajes
@character_bp.route("/characters",methods=["GET"])
def list_characters():
    #sacamos la info de los personajes en la BD
    characters = Character.query.all()
    #se los mandamos al template
    return render_template("characters_list.html", characters=characters)