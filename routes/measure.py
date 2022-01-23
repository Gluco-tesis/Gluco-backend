from fastapi import APIRouter, Response, responses, status
from starlette.responses import Response
from config.db import conn
from models.user import users
from schemas.user import User, UserLogin
from schemas.nirMeasure import NirMeasure
from starlette.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
import httpx

measure = APIRouter()

URL = "http://192.168.100.63/medir"

async def request():
    async with httpx.AsyncClient(timeout=None) as client:
        result = await client.get(URL)
        result = result.json()
        return result

def inferences(json_nir, cantidad_mediciones):
    R = S = T = U = V = W = 0
    for i in json_nir:
        R += i['R']
        S += i['S']
        T += i['T']
        U += i['U']
        V += i['V']
        W += i['W']
    
    promR=R/cantidad_mediciones
    promS=S/cantidad_mediciones
    promT=T/cantidad_mediciones
    promU=U/cantidad_mediciones
    promV=V/cantidad_mediciones
    promW=W/cantidad_mediciones

    return { 
        "promR": promR, 
        "promS":promS, 
        "promT": promT, 
        "promU": promU, 
        "promV": promV, 
        "promW": promW 
    }

    
@measure.get("/measure/medir", tags=["measures"])
async def medir_nir():
    cantidad_mediciones = 7
    json_nir = await request()
    promedios = inferences(json_nir, cantidad_mediciones)
    return promedios