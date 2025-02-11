from app.utils.db import db

class Comic(db.Model):
    __tablename__ = 'comic'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    #enlazamos el id del personaje que sale en este comic
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'),nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
    def save(self):
        # this method verify if the object exist using the name, if not, create a new object
        existing_comic = Comic.query.filter_by(name=self.name).first()
        if not existing_comic:
            db.session.add(self)
        else:
            existing_comic.name = self.name
        db.session.commit()
        return existing_comic

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self