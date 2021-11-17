"""
Clases para mapear las definiciones de los JSON que llegan en las petciones POST
de usuarios
"""

from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[int]
    name: str
    email: str
    password: str
