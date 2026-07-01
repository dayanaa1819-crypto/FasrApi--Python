from pydantic import BaseModel

class ClienteBase(BaseModel):
    #atributos
    nombre : str
    edad: int
    descripcion: str | None

# Cambiado SQLModel por ClienteBase para que herede los atributos correctamente
class ClienteLeer(ClienteBase):
    id: int

class ClienteCrear(ClienteBase):
    pass

class ClienteEditar(ClienteBase):
    pass

class Cliente(ClienteBase):
    id : int | None = None