from pydantic import BaseModel, computed_field
from datetime import datetime

from model.cliente import Cliente
from model.transacciones import Transaccion


class FacturaBase(BaseModel):
    fecha: datetime
    cliente: Cliente
    transacciones: list[Transaccion] = []

    @computed_field
    @property
    def valor_total(self) -> float:
        return sum(
            t.cantidad * t.vr_unitario
            for t in self.transacciones
        )


class CrearFactura(FacturaBase):
    pass


class EditarFactura(FacturaBase):
    pass


class Factura(FacturaBase):
    id: int | None = None