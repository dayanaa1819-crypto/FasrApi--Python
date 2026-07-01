from fastapi import FastAPI
from app.enrutador import clientes, facturas, transacciones
from app.enrutador.facturas import *
from app.enrutador.transacciones import *
from app.conexion_bd import crear_tablas




app = FastAPI(lifespan= crear_tablas)


app.include_router(clientes.router)
app.include_router(facturas.router)
app.include_router(transacciones.router)