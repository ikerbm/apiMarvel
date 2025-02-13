from app.utils.db import db
from app.models.base_model import BaseModel

#python maneja un sistema de prioridad en el cual las clases hijas tienen prioridad a la hora de buscar metodos
#es decir, el exits que existe en comic tiene prioridad sobre el exist en base

class Comic(BaseModel):
    __tablename__ = 'comic'
    #enlazamos el id del personaje que sale en este comic
    character_id = db.Column(db.Integer, db.ForeignKey('character.id', ondelete = 'CASCADE'),nullable=False)

    #modificamos el to_dict que esta en base agregandole mas informacion
    def to_dict(self):
        base_dict = super(Comic, self).to_dict()
        base_dict.update({
            'character_id':self.character_id
        })
        return base_dict

    def exists(self):
        return Comic.query.filter_by(name=self.name).first()





