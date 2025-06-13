from pydantic import BaseModel
from typing import List

class UserInput(BaseModel):
    nome: str
    email: str