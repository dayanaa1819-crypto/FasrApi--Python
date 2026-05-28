from fastapi import FastAPI, HTTPException

from model.cliente import (
    Cliente,
    ClienteCrear,
    ClienteEditar
)

from model.factura import (
    Factura,
    CrearFactura,
    EditarFactura
)

from model.transacciones import (
    Transaccion,
    TransaccionCrear,
    TransaccionEditar
)

app = FastAPI()

# ===================================
# LISTAS SIMULANDO BASE DE DATOS
# ===================================

listar_clientes: list[Cliente] = []
listas_facturas: list[Factura] = []
lista_transacciones: list[Transaccion] = []


# ===================================
# CRUD CLIENTES
# ===================================

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


# ===================================
# CRUD FACTURAS
# ===================================

@app.get("/facturas", response_model=list[Factura])
async def listar_facturas():

    return listas_facturas


@app.get("/facturas/{id}")
async def obtener_factura(id: int):

    for factura in listas_facturas:

        if factura.id == id:
            return factura

    return {"error": "Factura no encontrada"}


@app.post("/facturas/{cliente_id}")
async def crear_factura(
    cliente_id: int,
    datos_factura: CrearFactura
):

    cliente_encontrado = None

    for cliente in listar_clientes:

        if cliente.id == cliente_id:
            cliente_encontrado = cliente
            break

    if not cliente_encontrado:

        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    factura_val = Factura.model_validate(
        datos_factura.model_dump()
    )

    factura_val.id = len(listas_facturas) + 1
    factura_val.cliente = cliente_encontrado

    listas_facturas.append(factura_val)

    return factura_val


