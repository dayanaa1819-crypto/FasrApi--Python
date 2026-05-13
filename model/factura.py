from pydantic import BaseModel
from datetime import datetime

class Factura(BaseModel):
    id : int
    fecha : datetime
    total : float
    cliente : str