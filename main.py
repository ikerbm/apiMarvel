from flask import Flask
from flask_migrate import Migrate
from app.routes.character import character_bp  # Importar Blueprint de personajes
from app.utils.db import db

#creamos la base de datos con sqlalchemy

#creamos app con flask y decimos que su configuracon vendra del archivo config.py

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    #inicializamos la base de datos de la app y hacemos las migraciones
    db.init_app(app)
    migrate = Migrate(app, db)
    #decimos cuales seran los prefijos de la url de los route
    app.register_blueprint(character_bp) #, url_prefix="/" solo se usa cuando se va a utilizar
    return app



