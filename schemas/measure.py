"""
Clases para mapear las definiciones de los JSON que llegan en las petciones POST
de usuarios
"""

import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel

class Measure(BaseModel):
    id: Optional[int]
    measurement: Decimal
    measure_date: datetime.datetime
    user_id: int


class MeasureUserSearch(BaseModel):
    userId: int
    date: datetime.date

class MeasureUserList(BaseModel):
    userId: int
    count: int