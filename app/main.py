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


@app.put("/facturas/{id}")
async def editar_factura(
    id: int,
    datos_factura: EditarFactura
):

    for i, factura in enumerate(listas_facturas):

        if factura.id == id:

            factura_val = Factura.model_validate(
                datos_factura.model_dump()
            )

            factura_val.id = id

            listas_facturas[i] = factura_val

            return {
                "mensaje": "Factura actualizada",
                "factura": factura_val
            }

    return {"error": "Factura no encontrada"}


@app.delete("/facturas/{id}")
async def eliminar_factura(id: int):

    for i, factura in enumerate(listas_facturas):

        if factura.id == id:

            del listas_facturas[i]

            return {
                "mensaje": "Factura eliminada"
            }

    return {"error": "Factura no encontrada"}


# ===================================
# CRUD TRANSACCIONES
# ===================================

@app.get("/transacciones")
async def listar_transacciones():

    return lista_transacciones


@app.get("/transacciones/{id}")
async def obtener_transaccion(id: int):

    for transaccion in lista_transacciones:

        if transaccion.id == id:
            return transaccion

    return {"error": "Transacción no encontrada"}


@app.post("/transacciones/{factura_id}")
async def crear_transaccion(
    factura_id: int,
    datos_transaccion: TransaccionCrear
):

    factura_encontrada = None

    for factura in listas_facturas:

        if factura.id == factura_id:
            factura_encontrada = factura
            break

    if not factura_encontrada:

        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )

    transaccion_val = Transaccion.model_validate(
        datos_transaccion.model_dump()
    )

    transaccion_val.id = len(lista_transacciones) + 1
    transaccion_val.factura_id = factura_id

    lista_transacciones.append(transaccion_val)

    factura_encontrada.transacciones.append(
        transaccion_val
    )

    return {
        "mensaje": "Transacción creada",
        "transaccion": transaccion_val
    }


@app.put("/transacciones/{id}")
async def editar_transaccion(
    id: int,
    datos_transaccion: TransaccionEditar
):

    for i, transaccion in enumerate(
        lista_transacciones
    ):

        if transaccion.id == id:

            transaccion_val = Transaccion.model_validate(
                datos_transaccion.model_dump()
            )

            transaccion_val.id = id
            transaccion_val.factura_id = (
                transaccion.factura_id
            )

            lista_transacciones[i] = transaccion_val

            return {
                "mensaje": "Transacción actualizada",
                "transaccion": transaccion_val
            }

    return {"error": "Transacción no encontrada"}


@app.delete("/transacciones/{id}")
async def eliminar_transaccion(id: int):

    for i, transaccion in enumerate(
        lista_transacciones
    ):

        if transaccion.id == id:

            del lista_transacciones[i]

            return {
                "mensaje": "Transacción eliminada"
            }

    return {"error": "Transacción no encontrada"}