from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from sqlmodel import select

from app.model.factura import Factura, FacturaCrear, FacturaEditar
from app.model.cliente import Cliente  # Importante para validar el cliente en la BD
from app.conexion_bd import Sesion_dependencia

router = APIRouter(
    prefix="/facturas",
    tags=["Facturas"]
)

# ///////////////////////
#        CRUD FACTURAS
# ///////////////////////

# --- VER QUE FACTURAS SE ENCUENTRAN ---
@router.get("/")
async def listar_facturas(sesion: Sesion_dependencia):
    # Trae todas las facturas de la base de datos SQLite
    facturas = sesion.exec(select(Factura)).all()

    if len(facturas) == 0:
        return {"mensaje": "No hay facturas registradas"}

    return facturas


# --- CREAR FACTURAS SI EL CLIENTE SE ENCUENTRA ---
@router.post("/{cliente_id}", response_model=Factura)
async def crear_facturas(cliente_id: int, datos_factura: FacturaCrear, sesion: Sesion_dependencia):
    # Buscamos al cliente directamente en la base de datos por su ID
    cliente_encontrado = sesion.get(Cliente, cliente_id)

    # Si no existe cliente
    if not cliente_encontrado:
        raise HTTPException(
            status_code=400,
            detail=f"Cliente con id {cliente_id} no existe, debes crearlo primero.",
        )

    # Crear la factura en la BD mapeando los datos de la petición
    factura_val = Factura.model_validate(datos_factura.model_dump())
    factura_val.fecha = str(datetime.now()) # Adaptamos la fecha a string o al formato de tu modelo
    factura_val.cliente = cliente_encontrado # Si manejas la relación de objetos u objetos anidados

    # Guardamos en la base de datos (SQLite se encarga del ID autoincremental de forma automática)
    sesion.add(factura_val)
    sesion.commit()
    sesion.refresh(factura_val)
    
    return factura_val


# --- PARA BUSCAR UNA FACTURA POR ID ---
@router.get("/{id}", response_model=Factura)
async def obtener_factura(id: int, sesion: Sesion_dependencia):
    # Buscamos la factura directamente por su ID único
    factura = sesion.get(Factura, id)

    if factura:
        return factura

    raise HTTPException(
        status_code=404,
        detail="Factura no encontrada"
    )


# --- BUSCAR UNA FACTURA DE UN CLIENTE POR SU ID ---
@router.get("/clientes/{cliente_id}/facturas")
async def facturas_cliente(cliente_id: int, sesion: Sesion_dependencia):
    # Filtramos en la base de datos las facturas cuyo cliente_id coincida
    # Nota: Si tu modelo Factura usa "cliente_id" como clave foránea, cambia f.cliente.id por f.cliente_id
    statement = select(Factura).where(Factura.cliente_id == cliente_id)
    facturas_cliente = sesion.exec(statement).all()

    return facturas_cliente


# --- EDITAR LA FACTURA ---
@router.put("/{id}", response_model=Factura)
async def editar_factura(id: int, datos_factura: FacturaEditar, sesion: Sesion_dependencia):
    # Buscamos la factura existente en la BD
    factura_db = sesion.get(Factura, id)

    if not factura_db:
        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )

    # Extraemos los datos que nos envían y actualizamos los campos en el objeto de la BD
    datos_nuevos = datos_factura.model_dump(exclude_unset=True)
    for key, value in datos_nuevos.items():
        setattr(factura_db, key, value)

    # Guardamos los cambios en SQLite
    sesion.add(factura_db)
    sesion.commit()
    sesion.refresh(factura_db)

    return factura_db


# --- ELIMINAR LA FACTURA ---
@router.delete("/{id}")
async def eliminar_factura(id: int, sesion: Sesion_dependencia):
    # Buscamos la factura en la BD
    factura = sesion.get(Factura, id)

    if not factura:
        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )

    # Eliminamos el registro de la BD
    sesion.delete(factura)
    sesion.commit()

    return {
        "mensaje": f"Factura {id} eliminada correctamente"
    }