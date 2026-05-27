from pydantic import BaseModel


class TransaccionBase(BaseModel):
    cantidad: int
    vr_unitario: float
    descripcion: str
    
class TransaccionCrear(BaseModel):
    pass
    
class TransaccionEditar(BaseModel):
    pass

class Transaccion(TransaccionBase):
    id: int | None = None
    factura_id: int | None = None
    