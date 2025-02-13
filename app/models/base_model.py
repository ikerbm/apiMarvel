from app.utils.db import db

#python maneja un sistema de prioridad en el cual las clases hijas tienen prioridad a la hora de buscar metodos
#es decir, el exits que existe en comic tiene prioridad sobre el exist en base

class BaseModel(db.Model):
    #Modelo base abstracto que define campos y metodos comunes
    #Esto hace que la clase sea abstracta (no crea una tabla en la bd)
    __abstract__ = True
    #campos comunes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    #metodos comunes
    def to_dict(self):
        #para convertir a diccionario
        return {
            'id': self.id,
            'name': self.name,
        }

    def exists(self):
        #Verifica si el objeto ya existe en la base de datos.
        return self.query.filter_by(id=self.id).first()

    def update_or_create(self):
       #Actualiza el objeto existente o crea uno nuevo si no existe.
        existing = self.exists()
        if not existing:
            db.session.add(self)
            db.session.commit()
            return self
        else:
            existing.name = self.name
            db.session.commit()
            return existing

    def update(self):
        #Metodo principal que llama a update_or_create.
        return self.update_or_create()

    def delete(self):
        #Elimina el objeto de la base de datos.
        db.session.delete(self)
        db.session.commit()
        return self