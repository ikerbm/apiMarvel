from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#creamos la base de datos con sqlalchemy
db = SQLAlchemy()
migrate = Migrate()

