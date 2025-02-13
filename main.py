from flask import Flask, render_template
from app.routes.character_route import character_bp  # Importar Blueprint de personajes
from app.utils.db import db,migrate
from app.config import Config

#creamos app con flask y decimos que su configuracon vendra del archivo config.py
def create_app():
    application = Flask(__name__, template_folder='templates')
    application.config.from_object(Config)
    #inicializamos la base de datos de la app y hacemos las migraciones
    db.init_app(application)
    migrate.init_app(application, db)
    #decimos cuales seran los prefijos de la url de los route
    with application.app_context():
        application.register_blueprint(character_bp) #, url_prefix="/" solo se usa cuando se va a utilizar
    return application
app = create_app()
    # Ruta principal para la página de inicio

@app.route('/')
def index():
    return render_template('index.html')  # Renderiza la plantilla index.html


