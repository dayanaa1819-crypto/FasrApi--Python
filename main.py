from fastapi import FastAPI, HTTPException
from model.cliente import ClienteBase, ClienteCrear, Cliente, ClienteEditar
from model.factura import Factura, CrearFactura, EditarFactura, Factura
from model.transacciones import TransaccionCrear, TransaccionEditar ,Transaccion

app = FastAPI()

# =========================
# LISTAS SIMULANDO BD
# =========================

listar_clientes: list[Cliente] = []
listas_facturas: list[Factura] = []
lista_transacciones = list[Transaccion] = []


# ======================================================
# CRUD CLIENTES
# ======================================================

@app.get("/clientes")
async def listar_cliente():

    if len(listar_clientes) == 0:
        return {"Clientes": "No se han registrado usuarios aun"}

    return {"Clientes": listar_clientes}


@app.get("/clientes/{id}")
async def listar_cliente_id(id: int):

    for cliente in listar_clientes:

        if cliente.id == id:
            return cliente

    return {"Clientes": "No se encuentra"}


@app.post("/clientes", response_model=Cliente)
async def crear_cliente(datos_cliente: ClienteCrear):

    cliente_validado = Cliente.model_validate(
        datos_cliente.model_dump()
    )

    cliente_validado.id = len(listar_clientes) + 1

    listar_clientes.append(cliente_validado)

    return cliente_validado


@app.put("/clientes/{id}")
async def editar_cliente(id: int, datos_cliente: ClienteEditar):

    for i, obj_cliente in enumerate(listar_clientes):

        if obj_cliente.id == id:

            cliente_val = Cliente.model_validate(
                datos_cliente.model_dump()
            )

            cliente_val.id = id

            listar_clientes[i] = cliente_val

            return {
                "Mensaje": "Se actualizo satisfactoriamente.",
                "Cliente": cliente_val
            }

    return {"Error": "Cliente no encontrado"}


@app.delete("/clientes/{id}")
async def eliminar_cliente(id: int):

    for i, object_cli in enumerate(listar_clientes):

        if object_cli.id == id:

            nombre_cliente = object_cli.nombre

            del listar_clientes[i]

            return {
                "message": f"Cliente {nombre_cliente} eliminado exitosamente"
            }

    return {"error": "Cliente no encontrado"}


# ======================================================
# CRUD FACTURAS
# ======================================================

@app.get("/facturas", response_model= list[Factura])
async def listar_facturas():
    return listas_facturas

@app.post("/facturas/{cliente_id}", response_model=Factura)
async def crear_facturas(cliente_id: int, datos_factura: CrearFactura):
    cliente_encontrado = None
    for c in listar_clientes:
        if c.id == cliente_id:
            cliente_encontrado = c
            break
        
    if not cliente_encontrado:
        raise HTTPException(status_code=400, detail=f"Cliente con id {cliente_id} no existe, debes crear.")
    
    factura_val= Factura.model_validate(datos_factura.model_dump())
    factura_val.id = len(listas_facturas) + 1
    factura_val.cliente = cliente_encontrado
    listas_facturas.append(factura_val)
    return factura_val
 