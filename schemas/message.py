"""
Clases para mapear las definiciones de los JSON de menssages
"""

from pydantic import BaseModel

class MessageResponse(BaseModel):
    message: str