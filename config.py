import os

class Config:
    #hacemos la comunicacion del api propio con la base de datos marvelDB almacenada en el local
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://root:admin@localhost:3306/marvelDB")
    SQLALCHEMY_TRACK_MODIFICATIONS = False