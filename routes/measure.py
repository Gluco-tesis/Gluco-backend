from unittest import result
from fastapi import APIRouter, Response, responses, status
from starlette.responses import Response
from config.db import conn
from models.user import measures
from schemas.measure import Measure, MeasureUserSearch, MeasureUserList
import datetime
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

@measure.post("/measure/search", response_model=list[Measure], tags=["measures"])
def search_measures(measure_user_search: MeasureUserSearch):
    result = conn.execute(measures.select()).fetchall()
    dateFormat = "%Y-%m-%d"

    measure_users = list(
        filter(
            lambda measure: 
            int(measure[3]) == int(measure_user_search.userId)  and
            str(measure[2].strftime(dateFormat)) == str(measure_user_search.date), 
            result
        )
    )

    return measure_users


@measure.post("/measure/list", response_model=list[Measure], tags=["measures"])
def list_measure(measure_list: MeasureUserList):
    result = conn.execute(measures.select()).fetchall()
    n = measure_list.count
    measure_users = list(
        filter(
            lambda measure: 
            int(measure[3]) == int(measure_list.userId),
            result
        )
    )

    # obtengo los n ultimos
    measure_users = measure_users[-n:]
    return measure_users



