from pydantic import BaseModel
from typing import List

class PedidoInput(BaseModel):
    cliente: str
    itens: List[str]
    mesa: int