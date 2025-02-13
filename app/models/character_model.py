from app.utils.db import db
from app.models.base_model import BaseModel
#creacion de la tabla de la base de datos para los personajes
class Character(BaseModel):
    __tablename__ = 'character'
    marvel_id = db.Column(db.Integer, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    comics = db.relationship("Comic", backref="character", lazy=True, cascade="all, delete-orphan")
    image_url = db.Column(db.Text, nullable=True)

    # modificamos el to_dict que esta en base agregandole mas informacion
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'marvel_id': self.marvel_id,
            'description': self.description,
            "comics": [comic.name for comic in self.comics], # Agrega los cómics en formato de lista
            "image_url": self.image_url
        })
        return base_dict
