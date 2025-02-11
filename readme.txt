el proyecto consta de una comunicacion entre una base de datos propio y una api para desarrolladores de marvel 
el url de la api de marvel es https://developer.marvel.com 
el objetivo de la prueba es hacer consultas a la api y que los datos que la api arroje como resultado se almacenen en la base de datos
al editar los campos en la base de datos, estos deben de quedar guardados, pero al volver a hacer la consulta del mismo personaje, estos deben de editarse con la informacion en la api marvel

para el desarrollo se creo un contenedor en docker para la creacion de la base de datos marvelDB con mysql
la base de datos se sincronizo con el projecto por medio de flask y sqlalchemy, al realizar las migraciones las tablas programadas como modelos se crearon en la BD

por medio de la api marvel se recibieron las llaves de acceso neccesarias para la comunicacion de los datos, y de esta manera se pudieron almacenar los datos en la BD

para la realizacion de este ejercicio se opto por crear la tabla character en la cual recibiriamos informacion del personaje que se buscara
y se creo ademas la tabla comic para almacenar los comics donde este personaje aparecia, ambas tablas quedaron enlazadas

teniendo en cuenta que el ejerccio se realizo como una prueba para backend, no se realizo ningun tipo de trabajo para mostrar los datos

