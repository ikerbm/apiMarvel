import os

class Config:
    #hacemos la comunicacion del api probase de datospio con la base de datos marvelDB almacenada en el local
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://root:admin@localhost:3306/marvelDB")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

#hubo errores de con la conexion a la base de datos cuando el docker se ejecutaba pero no se abria el gestor DBeaver
#se soluciono instalando el paquete cryptography
#no se sabe el como tod0 se arreglo sin necesidad de realizar importaciones