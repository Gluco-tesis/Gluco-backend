"""
Clases para mapear las definiciones de los JSON que llegan en las petciones POST
de usuarios
"""

from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    id: Optional[int]
    name: str
    lastname: str
    email: str
    password: str
    phone: str

class UserEdit(BaseModel):
    name: str
    lastname: str
    password: str
    phone: str

class UserLogin(BaseModel):
    email: str
    password: str
