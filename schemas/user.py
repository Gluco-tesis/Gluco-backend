"""
Clases para mapear las definiciones de los JSON que llegan en las petcione de usuarios
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

class UserDelete(BaseModel):
    password: str

class UserForgotPassword(BaseModel):
    email: str

class UserChangePassword(BaseModel):
    email: str
    reset_code: int
    new_password: str 

class UserLoginResponse(BaseModel):
    id: int
    name : str
    lastname : str
    email: str
    phone: str
    token: str