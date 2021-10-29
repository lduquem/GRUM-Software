import sqlite3
from sqlite3 import Error
from flask import current_app, g


def get_db():
    try:
        if 'db' not in g:
            print('conexion exitosa')
            g.db = sqlite3.connect('gestionempleados.db')
        return g.db
    except Error:
        print(Error)


def close_db(): # Definir la función.
    db = g.pop( 'db', None ) # Obtener el objeto de base de datos de g si existe, sino retorna None.

    if db is not None: # Si el objeto db existe
        db.close() # Cierra la conexión a la db    


