from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
from fastapi import FastAPI, Depends

nombre_bd = "bd_clientes.sqlite3"
url_bd = f"sqlite:///{nombre_bd}"

# motor de base de datos
motor_bd = create_engine(url_bd)

# Definir el metodo para crear las tablas
def crear_tablas(app: FastAPI):
    SQLModel.metadata.create_all(motor_bd)
    yield #no hay nada para retornar o ejecutar

# Definir el metodo para la sesión
def obtener_sesion():
    # CAMBIADO: 'motor' por 'motor_bd'
    with Session(motor_bd) as session:
        yield session

Sesion_dependencia = Annotated[Session, Depends(obtener_sesion)]