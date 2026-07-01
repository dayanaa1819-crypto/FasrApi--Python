from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from datetime import datetime

# Modelos necesarios para las consultas e inserciones
from app.model.transacciones import Transacciones 
from app.model.cliente import Cliente
from app.model.factura import Factura
from app.conexion_bd import Sesion_dependencia

router = APIRouter(       
    prefix="/transacciones",  
    tags=["Transacciones"]    
)

# ///////////////////////
#    CRUD TRANSACCIONES
# ///////////////////////

# ///////////////////////
#   VER TRANSACCIONES
# ///////////////////////
@router.get("/")
def listar_transacciones(sesion: Sesion_dependencia):
    # Buscamos todas las transacciones en la base de datos
    transacciones = sesion.exec(select(Transacciones)).all()

    if len(transacciones) == 0:
        return {"mensaje": "No hay transacciones"}

    return {"transacciones": transacciones}


# ///////////////////////
#   CREAR TRANSACCIONES 
# ///////////////////////
@router.post("/{factura_id}")
async def crear_transaccion(
    factura_id: int, 
    datos_transaccion: Transacciones, # Puedes usar TransaccionesCrear si lo tienes
    cliente_id: int,
    sesion: Sesion_dependencia
):
    # 1. Confirmar que el cliente está registrado en la base de datos.
    cliente_encontrado = sesion.get(Cliente, cliente_id)

    if not cliente_encontrado:
        raise HTTPException(
            status_code=400,
            detail=f"Error 400: No existe un cliente con ese id: {cliente_id}, debes crear el cliente.",
        )

    # 2. Buscar si ya existe una factura con el id recibido.
    factura_encontrada = sesion.get(Factura, factura_id)

    # Si encontramos la factura continuamos con el proceso.
    if factura_encontrada:
        # Verificamos que la factura realmente pertenezca al cliente indicado.
        # Ajusta "cliente_id" según el nombre de la clave foránea en tu modelo Factura
        if factura_encontrada.cliente_id == cliente_id:
            
            # Validamos y preparamos la transacción con los datos recibidos
            nueva_transaccion = Transacciones.model_validate(datos_transaccion.model_dump())
            nueva_transaccion.factura_id = factura_id

            # Guardamos la transacción en la base de datos
            sesion.add(nueva_transaccion)
            sesion.commit()
            sesion.refresh(nueva_transaccion)

            # Refrescamos la factura para que incluya la nueva relación
            sesion.refresh(factura_encontrada)

            return {
                "mensaje": f"Transaccion agregada a factura {factura_encontrada.id}",
                "factura": factura_encontrada
            }
        else:
            return {
                "mensaje": f"Se encontro la factura de id: {factura_id}, pero es de otro cliente id: {cliente_id}",
                "factura encontrada": factura_encontrada
            }

    # Si no existe la factura, lanzamos un error o puedes descomentar tu código anterior adaptado.
    raise HTTPException(
        status_code=404,
        detail=f"La factura con id {factura_id} no existe."
    )
    

# ///////////////////////
# BUSCAR UNA TRANSACCIÓN ESPECÍFICA POR ID
# ///////////////////////
@router.get("/{id}", response_model=Transacciones)
async def obtener_transaccion(id: int, sesion: Sesion_dependencia):
    transaccion = sesion.get(Transacciones, id)

    if transaccion:
        return transaccion

    raise HTTPException(
        status_code=404,
        detail="Transacción no encontrada"
    )


# ///////////////////////
# ACTUALIZAR DATOS DE UNA TRANSACCIÓN
# ///////////////////////
@router.put("/{id}", response_model=Transacciones)
async def editar_transaccion(
    id: int,
    datos_transaccion: Transacciones, # Cambiar por TransaccionesEditar si manejas ese esquema
    sesion: Sesion_dependencia
):
    transaccion_db = sesion.get(Transacciones, id)

    if not transaccion_db:
        raise HTTPException(
            status_code=404,
            detail="Transacción no encontrada"
        )

    # Actualizamos los campos recibidos de manera dinámica
    campos_nuevos = datos_transaccion.model_dump(exclude_unset=True)
    for llave, valor in campos_nuevos.items():
        setattr(transaccion_db, llave, valor)

    sesion.add(transaccion_db)
    sesion.commit()
    sesion.refresh(transaccion_db)

    return transaccion_db


# ///////////////////////
# ELIMINAR UNA TRANSACCIÓN
# ///////////////////////
@router.delete("/{id}")
async def eliminar_transaccion(id: int, sesion: Sesion_dependencia):
    transaccion = sesion.get(Transacciones, id)

    if not transaccion:
        raise HTTPException(
            status_code=404,
            detail="Transacción no encontrada"
        )

    sesion.delete(transaccion)
    sesion.commit()

    return {
        "mensaje": f"Transacción {id} eliminada correctamente"
    }