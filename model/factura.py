from pydantic import BaseModel, computed_field
from datetime import datetime
from model.transacciones import Transaccion
from model.cliente import Cliente

class FacturaBase(BaseModel):
    fecha: datetime
    cliente: Cliente
    transacciones: list[Transaccion] = []
    
    @computed_field
    @property
    def valor_total(self)-> float:
        factura_id_actual = getattr

class CrearFactura(FacturaBase):
    pass

class EditarFactura(FacturaBase):
    pass

class Factura(FacturaBase):
        id: int | None = None

