"""
Este archvio contiene los modelos que son las representaciones que usa fastAPI
de las tablas para el manejo de los datos.
"""

from sqlalchemy import Table, Column, engine
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, TIMESTAMP, DECIMAL
from config.db import meta, engine

users = Table("usuarios", meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
    Column("lastname", String(100)),
    Column("email", String(100)),
    Column("password", String(100)),
    Column("phone", String(100)),
    Column("key", String(100))
)

measures = Table("medidas", meta, 
    Column("id", Integer, primary_key=True),
    Column("measurement", DECIMAL(10,2)),
    Column("measure_date", TIMESTAMP),
    Column("user_id", Integer, ForeignKey("usuarios.id"))
)

inferences = Table("inferencias", meta, 
    Column("id", Integer, primary_key=True),
    Column("R", DECIMAL(10,5)),
    Column("S", DECIMAL(10,5)),
    Column("T", DECIMAL(10,5)),
    Column("U", DECIMAL(10,5)),
    Column("V", DECIMAL(10,5)),
    Column("W", DECIMAL(10,5)),
    Column("measurement", DECIMAL(10,2))
)

meta.create_all(engine)