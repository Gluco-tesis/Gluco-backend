"""
Clases para mapear las definiciones de los JSON que llegan en las petciones POST
de usuarios
"""

from typing import Optional
from pydantic import BaseModel

class Inference(BaseModel):
    id: Optional[int]
    R: float
    S: float
    T: float
    U: float
    V: float
    W: float
    measurement: float