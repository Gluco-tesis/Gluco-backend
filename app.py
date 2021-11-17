from fastapi import FastAPI
from routes.user import user
from schemas.nirMeasure import NirMeasure
import httpx

app = FastAPI(
    title="Gluco Backend",
    description="Backend para Gluco, aplicacion desarrollada para el proyecto de grado",
    version="1.0.0",
    openapi_tags=[{
        "name": "users",
        "description": "Rutas de usuarios"
    }]
)


app.include_router(user)

URL = "http://192.168.100.44/medir"

async def request():
    async with httpx.AsyncClient(timeout=None) as client:
        result = await client.get(URL)
        result = result.json()
        return result

@app.get("/medir", response_model=NirMeasure)
async def medir_nir():
  return await request()
