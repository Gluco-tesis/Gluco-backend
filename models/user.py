"""
Este archvio contiene los modelos que son las representaciones que usa fastAPI
de las tablas para el manejo de los datos.
"""

from datetime import datetime
from sqlalchemy import Table, Column, engine
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, TIMESTAMP, DECIMAL, FLOAT
from config.db import meta, engine

users = Table("usuarios", meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
    Column("email", String(100)),
    Column("password", String(100))
)

measures = Table("medidas", meta, 
    Column("id", Integer, primary_key=True),
    Column("measurement", DECIMAL(10.0)),
    Column("date", TIMESTAMP),
    Column("user_id", Integer, ForeignKey("usuarios.id"))
)

inferences = Table("inferencias", meta, 
    Column("id", Integer, primary_key=True),
    Column("R", FLOAT),
    Column("S", FLOAT),
    Column("T", FLOAT),
    Column("U", FLOAT),
    Column("V", FLOAT),
    Column("W", FLOAT),
    Column("measurement", DECIMAL(10.0))
)

meta.create_all(engine)