"""
Clases para mapear las definiciones de los JSON que llegan en las petciones POST
del sensor nir
"""

from typing import Optional
from pydantic import BaseModel

class NirMeasure(BaseModel):
    R: float
    S: float
    T: float
    U: float
    V: float
    W: float