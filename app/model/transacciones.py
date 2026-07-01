from pydantic import BaseModel


class TransaccionesBase(BaseModel):
    # atributos
    cantidad: int
    vr_unitario: float
    descripcion: str


class TransaccionesCrear(TransaccionesBase):
    pass


class TransaccionesEditar(TransaccionesBase):
    pass


class Transacciones(TransaccionesBase):
    id: int | None = None
    factura_id: int | None = None