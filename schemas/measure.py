"""
Clases para mapear las definiciones de los JSON que llegan en las petciones de medidas
"""

import datetime
from decimal import Decimal
from pydantic import BaseModel

class Measure(BaseModel):
    glucoseCal: Decimal

class MeasureUserSearch(BaseModel):
    userId: int
    date: datetime.date

class MeasureUserList(BaseModel):
    userId: int
    count: int