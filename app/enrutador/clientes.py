from fastapi import APIRouter
from app.modelos.clientes import Cliente, ClienteCrear, ClienteEditar
from ..listas_app import lista_clientes

# por explicar la proxima clase
# aca utilizaremos la sesion de bd

# crear manager de las api router, rutas de la api
ruta_clientes = APIRouter()


@ruta_clientes.get("/clientes")
async def listar_clientes():
    # Creacion de sms mas adecuado al usuario
    return {"Clientes": lista_clientes}


@ruta_clientes.get("/clientes/{id}")
async def listar_cliente(id: int):
    # retornar mensajes claros al usuario, si no existe el cliente
    # return [d for d in lista_clientes if d.id ==id]
    for cliente in lista_clientes:
        if cliente.id == id:
            return cliente


@ruta_clientes.post("/clientes", response_model=Cliente)
async def crear_clientes(datos_cliente: ClienteCrear):
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    cliente_val.id = len(lista_clientes) + 1  # id incremento
    lista_clientes.append(cliente_val)
    return cliente_val
    # return {"Cliente": cliente_val}


@ruta_clientes.put("/clientes/{id}")
def editar_clientes(id: int, datos_cliente: ClienteEditar):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == id:
            cliente_val = Cliente.model_validate(datos_cliente.model_dump())
            cliente_val.id = id
            lista_clientes[i] = cliente_val

    return {
        "mensaje": "Se actualizo el cliente satisfactoriamente.",
        "Cliente": cliente_val,
    }


@ruta_clientes.put("/clientes/{id}")
@ruta_clientes.delete("/clientes")
def eliminar_clientes():
    return {"Cliente": "Cliente eliminado"}



    
@app.get("/clientes")
async def listar_cliente():

    if len(listar_clientes) == 0:
        return {"mensaje": "No hay clientes registrados"}

    return listar_clientes


@app.get("/clientes/{id}")
async def listar_cliente_id(id: int):

    for cliente in listar_clientes:

        if cliente.id == id:
            return cliente

    return {"error": "Cliente no encontrado"}


@app.post("/clientes", response_model=Cliente)
async def crear_cliente(datos_cliente: ClienteCrear):

    cliente_validado = Cliente.model_validate(
        datos_cliente.model_dump()
    )

    cliente_validado.id = len(listar_clientes) + 1

    listar_clientes.append(cliente_validado)

    return cliente_validado


@app.put("/clientes/{id}")
async def editar_cliente(
    id: int,
    datos_cliente: ClienteEditar
):

    for i, cliente in enumerate(listar_clientes):

        if cliente.id == id:

            cliente_val = Cliente.model_validate(
                datos_cliente.model_dump()
            )

            cliente_val.id = id

            listar_clientes[i] = cliente_val

            return {
                "mensaje": "Cliente actualizado",
                "cliente": cliente_val
            }

    return {"error": "Cliente no encontrado"}


@app.delete("/clientes/{id}")
async def eliminar_cliente(id: int):

    for i, cliente in enumerate(listar_clientes):

        if cliente.id == id:

            nombre = cliente.nombre

            del listar_clientes[i]

            return {
                "mensaje": f"Cliente {nombre} eliminado"
            }

    return {"error": "Cliente no encontrado"}
