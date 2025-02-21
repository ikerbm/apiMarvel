from flask import redirect,Blueprint,jsonify,render_template,request,url_for,flash
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
@character_bp.route("/characters/<name>",methods=["GET"])
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

        else:
            character.name = marvel_data["name"],
            character.description = marvel_data["description"]
            character.image_url = create_img_url(marvel_data)
            db.session.commit()
            #devolver el codigo 200 (ok) cuando el personaje ya existe
        return render_template("character_details.html", character=character)
    except Exception as e:
        #manejar errores inesperados
        return jsonify({"error" : "Ocurrio un error interno en el servidor","details":str(e)}),500

#ruta para mostrar la lista de personajes
@character_bp.route("/characters",methods=["GET"])
def list_characters():
    #sacamos la info de los personajes en la BD
    characters = Character.query.all()
    #se los mandamos al template
    return render_template("characters_list.html", characters=characters,title="Personajes")

#ruta para manejar el envio de formulario
@character_bp.route("/add_character",methods=["GET","POST"])
def add_character():
    if request.method == "POST":
        #obtener los datos del formulario
        name = request.form.get("name")
        marvel_id = request.form.get("marvel_id", type=int)
        description = request.form.get("description")

        #validar que nombre no este vacio
        if not name or not marvel_id:
            flash("faltan campos obligatorios","error")
            return jsonify({"error" : "el parametros faltantes"}),400
        #verificar que el marvel_id este disponible
        existent_character = Character.query.filter_by(marvel_id=marvel_id).first()
        if existent_character:
            flash("El Marvel ID ya está en uso. Por favor, elige otro.", "error")
            return redirect(url_for("character_bp.add_character"))
        #crear un nuevo personaje en la BD
        new_character = Character(
            name=name,
            marvel_id=marvel_id,
            description=description,
        )
        db.session.add(new_character)
        db.session.commit()
        flash("Personaje agregado correctamente.", "success")
        return redirect(url_for("character_bp.list_characters"))
    return render_template("add_character.html")

@character_bp.route("/characters/<int:marvel_id>",methods=["DELETE"])
def delete_character(marvel_id):
    try:
        #buscar el personaje en la BD
        character = Character.query.filter_by(marvel_id=marvel_id).first()
        if not character:
            print(f"personaje no encontrado en la BD")
            return jsonify({"error" : "el personaje no se ha encontrado es invalido"}),400

        #eliminar el personaje de la BD
        db.session.delete(character)
        db.session.commit()
        # Devolver una respuesta de éxito
        return jsonify({"message": "Personaje eliminado correctamente"}), 200
    except Exception as e:
        # Manejar errores inesperados
        db.session.rollback()
        return jsonify({"error": "Ocurrió un error al eliminar el personaje", "details": str(e)}), 500

@character_bp.route("/characters/<int:marvel_id>/edit",methods=["GET","POST"])
def edit_character(marvel_id):
    #obtener el personaje de la BD
    character = Character.query.filter_by(marvel_id=marvel_id).first()
    if request.method == "POST":
        #procesar formulario de edicion
        character.name = request.form.get("name")
        character.description = request.form.get("description")

        #Guardar los cambios en la BD
        db.session.commit()

        #redirigir a la lista de personajes
        return redirect(url_for("character_bp.list_characters"))

    #mostrar el formulario de edicion(Get)
    return render_template("edit_character.html", character=character)

