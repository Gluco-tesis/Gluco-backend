"""
Clases para mapear las definiciones de los JSON que llegan en las petciones POST
de usuarios
"""

from typing import Optional
from pydantic import BaseModel

class Measure(BaseModel):
    id: Optional[int]
    measurement: float
    date: str
    user_id: int
