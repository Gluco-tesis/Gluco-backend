"""
Este archivo contine los datos de conneccion a la base de datos local.
"""
from sqlalchemy import create_engine, MetaData, engine

engine = create_engine("mariadb+pymysql://root:123456@localhost:3306/glucometro")

meta = MetaData()

conn = engine.connect()

