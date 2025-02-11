from app.utils.db import db

#creacion de la tabla de la base de datos para los personajes
class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    marvel_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    #comics = db.relationship("Comic", back_populates="character")
    #movies = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "marvel_id": self.marvel_id,
            "name": self.name,
            "description": self.description,
            #"comics": self.comics,
            #"movies": self.movies
        }
    def save(self):
        # this method verify if the object exist using the marvel_id, if not, create a new object
        existing_character = Character.query.filter_by(marvel_id=self.marvel_id).first()
        if not existing_character:
            db.session.add(self)
            db.session.commit()
            return self
        else:
            existing_character.name = self.name
            existing_character.description = self.description
            db.session.commit()
            return existing_character
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

