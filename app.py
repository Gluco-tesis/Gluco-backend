from fastapi import FastAPI
from routes.user import user
from schemas.nirMeasure import NirMeasure
import httpx

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

URL = "http://192.168.100.44/medir"

async def request():
    async with httpx.AsyncClient(timeout=None) as client:
        result = await client.get(URL)
        result = result.json()
        return result

@app.get("/medir")
async def medir_nir():
    jsonNir = await request()
    R=0
    S=0
    T=0
    U=0
    V=0
    W=0
    
    for i in jsonNir:
        print(i)
        R += i['R']
        S += i['S']
        T += i['T']
        U += i['U']
        V += i['V']
        W += i['W']
    
    promR=R/7
    promS=S/7
    promT=T/7
    promU=U/7
    promV=V/7
    promW=W/7

    return { "promR": promR, "promS":promS, "promT": promT, "promU": promU, "promV": promV, "promW": promW }
