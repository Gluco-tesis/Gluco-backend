from fastapi import FastAPI
from routes.user import user
from routes.measure import measure


app = FastAPI(
    title="Gluco Backend API",
    description="Backend para Gluco, aplicacion desarrollada para el proyecto de grado",
    version="1.0.1",
    openapi_tags=[{
        "name": "users",
        "description": "Rutas de usuarios"
    }]
)


app.include_router(user)
app.include_router(measure)
