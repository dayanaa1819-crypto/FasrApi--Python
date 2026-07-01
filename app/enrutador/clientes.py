from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select, Session
from app.model.cliente import ClienteCrear, ClienteLeer, ClienteEditar, Cliente
from app.conexion_bd import Sesion_dependencia 

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

# ===========================
# CRUD CLIENTES
# ===========================

@router.get("/", response_model=list[ClienteLeer])
async def listar_clientes(session: Sesion_dependencia): 
    consulta = select(Cliente)
    return session.exec(consulta).all()

# --- AQUÍ SE CORRIGIÓ EL DUPLICADO (DEJANDO SOLO LA LÓGICA DE CREACIÓN) ---
@router.post("/", response_model=ClienteLeer, status_code=status.HTTP_201_CREATED)
async def crear_cliente(datos_cliente: ClienteCrear, session: Sesion_dependencia):
    cliente = Cliente.model_validate(datos_cliente.model_dump())
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente


@router.put("/{id}", response_model=ClienteLeer)
async def editar_cliente(id: int, datos_cliente: ClienteEditar, session: Sesion_dependencia):
    cliente = session.get(Cliente, id)
    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    datos = datos_cliente.model_dump(exclude_unset=True)

    for key, value in datos.items():
        setattr(cliente, key, value)

    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente


@router.delete("/{id}")
async def eliminar_cliente(id: int, session: Sesion_dependencia):
    cliente = session.get(Cliente, id)
    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    session.delete(cliente)
    session.commit()
    return {
        "mensaje": "Cliente eliminado correctamente"
    }