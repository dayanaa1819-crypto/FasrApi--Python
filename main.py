from fastapi import FastAPI
from model.cliente import ClienteBase, ClienteCrear, Cliente, ClienteEditar

app = FastAPI()

#Listado de clientes en BD
listar_clientes: list[Cliente] = []


@app.get("/clientes")
async def listar_cliente():
    if len(listar_clientes) == 0:
        return {"Clientes" : "No se han registrado usuarios aun"}
    else:
        return {"Clientes" : listar_clientes}

@app.get("/clientes/{id}")
async def listar_cliente_id(id : int):
    for cliente in listar_clientes:
        if cliente.id == id:
            return cliente
        else:
            return  {"Clientes" : "No se encuentra"}
    
    
@app.post("/clientes", response_model = Cliente)
async def crear_cliente(datos_cliente : ClienteCrear):

    clienteValidado = Cliente.model_validate(datos_cliente.model_dump())
    
    clienteValidado.id = len(listar_clientes) + 1
    
    listar_clientes.append(clienteValidado)
    return clienteValidado


@app.put("/clientes/{id}")
def editar_cliente(id : int, datosCliente : ClienteEditar):
    for i, obj_cliente in enumerate(listar_clientes):
        if obj_cliente.id == id:
            cliente_val = Cliente.model_validate(datosCliente.model_dump())
            cliente_val.id = id
            listar_clientes[i] = cliente_val
    return {"Mensaje" : "Se actualizo satisfactoriamente.", "Cliente": cliente_val}

@app.delete("/clientes/{id}")
def eliminar_cliente(id: int):
    for i, object_cli in enumerate(listar_clientes):
        if object_cli.id == id:
            nombre_cliente = object_cli.nombre 
            del listar_clientes[i]  
            return {"message": f"Cliente {nombre_cliente} eliminado exitosamente"}
            
    return {"error": "Cliente no encontrado"}
#235711