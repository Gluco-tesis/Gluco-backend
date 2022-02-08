from decimal import Decimal
from fastapi import APIRouter
from config.db import conn
from models.user import measures, inferences
from schemas.measure import MeasureUserSearch, MeasureUserList, Measure
from starlette.responses import JSONResponse
from datetime import datetime
import httpx
import numpy as np
from decimal import Decimal

measure = APIRouter()
time_format = "%H:%M:%S"

URL = "http://192.168.100.42/medir"

async def request():
    # Add 30 seconds to cancelar la solicitud
    timeout = httpx.Timeout(timeout=30.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        result = await client.get(URL)
        result = result.json()
        return result

def calc_inferences(json_nir, cantidad_mediciones):
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

def get_estadistic_values(x,y, prom_canal):
    n = len(x)
    x = np.array(x)
    y = np.array(y)
    sumx = sum(x)
    sumy = sum(y)
    sumx2 = sum(x*x)
    sumy2  = sum(y*y)
    sumxy = sum(x*y)
    promx = sumx/n
    promy = sumy/n

    m  = round((sumx*sumy - n*sumxy)/(sumx**2 - n*sumx2),2)
    b = round(promy - m*promx,2)

    sigmax = np.sqrt(sumx2/n - promx**2)
    sigmay = np.sqrt(sumy2/n - promy**2)
    sigmaxy = sumxy/n - promx*promy
    correlation_coeff= round((sigmaxy/(sigmax*sigmay)),2)

    prom_canal = round(Decimal(prom_canal),2)
    glucose_value  = round((Decimal(prom_canal) - b)/(m),2)

    values = {
        "m" : m,
        "b" : b,
        "glucoseValue" : glucose_value,
        "correlationCoeff": correlation_coeff
    }
    return values

@measure.get("/measure/{user_id}", response_model=Measure, tags=["measures"])
async def nir_measure(user_id:int):
    """Realiza la medicion de glucosa llamando al endpoint en arduino y devulve el nivel de glucosa
    Pide el id del usuario a medir
    """
    cantidad_mediciones = 7
    json_nir = await request()
    sensor_avg = calc_inferences(json_nir, cantidad_mediciones)

    result = conn.execute(inferences.select().order_by(inferences.c.measurement)).fetchall()

    channel_r = [round(x[1],2) for x in result]
    channel_s = [round(x[2],2) for x in result]
    channel_t = [round(x[3],2) for x in result]
    channel_u = [round(x[4],2) for x in result]
    channel_v = [round(x[5],2) for x in result]
    channel_w = [round(x[6],2) for x in result]
    glucose = [round(x[7],2) for x in result]

    glucose_r = round(get_estadistic_values(glucose, channel_r, sensor_avg["promR"])["glucoseValue"],2)
    glucose_s = round(get_estadistic_values(glucose, channel_s, sensor_avg["promS"])["glucoseValue"],2)
    glucose_t = round(get_estadistic_values(glucose, channel_t, sensor_avg["promT"])["glucoseValue"],2)
    glucose_u = round(get_estadistic_values(glucose, channel_u, sensor_avg["promU"])["glucoseValue"],2)
    glucose_v = round(get_estadistic_values(glucose, channel_v, sensor_avg["promV"])["glucoseValue"],2)
    glucose_w = round(get_estadistic_values(glucose, channel_w, sensor_avg["promW"])["glucoseValue"],2)

    print("Glucosa canal R", glucose_r)
    print("Glucosa canal S", glucose_s)
    print("Glucosa canal T", glucose_t)
    print("Glucosa canal U", glucose_u)
    print("Glucosa canal V", glucose_v)
    print("Glucosa canal W", glucose_w)

    glucose_final = (glucose_r + glucose_s + glucose_t + glucose_u + glucose_v + glucose_w) / 6
    print("Glucosa total", round(glucose_final,2))

    coef_r = get_estadistic_values(glucose,channel_r,round(sensor_avg["promR"], 2))["correlationCoeff"] 
    coef_s = get_estadistic_values(glucose,channel_s,round(sensor_avg["promS"], 2))["correlationCoeff"] 
    coef_t = get_estadistic_values(glucose,channel_t,round(sensor_avg["promT"], 2))["correlationCoeff"] 
    coef_u = get_estadistic_values(glucose,channel_u,round(sensor_avg["promU"], 2))["correlationCoeff"] 
    coef_v = get_estadistic_values(glucose,channel_v,round(sensor_avg["promV"], 2))["correlationCoeff"] 
    coef_w = get_estadistic_values(glucose,channel_w,round(sensor_avg["promW"], 2))["correlationCoeff"] 

    weighted_avg = (glucose_r * coef_r + glucose_s * coef_s + glucose_t * coef_t + glucose_u * coef_u + glucose_v * coef_v + glucose_w * coef_w) / (coef_r + coef_s + coef_t +coef_u + coef_v + coef_w)

    weighted_avg = round(weighted_avg, 2)
    print("Promedio ponderado: ", weighted_avg)

    print(get_estadistic_values(glucose,channel_r,round(sensor_avg["promR"], 2)))
    print(get_estadistic_values(glucose,channel_s,round(sensor_avg["promS"], 2)))
    print(get_estadistic_values(glucose,channel_t,round(sensor_avg["promT"], 2)))
    print(get_estadistic_values(glucose,channel_u,round(sensor_avg["promU"], 2)))
    print(get_estadistic_values(glucose,channel_v,round(sensor_avg["promV"], 2)))
    print(get_estadistic_values(glucose,channel_w,round(sensor_avg["promW"], 2)))

    now_date_time = datetime.now() 

    new_measure = { "measurement": weighted_avg, "measure_date": now_date_time, "user_id": user_id}
    result = conn.execute(measures.insert().values(new_measure))

    response = { "glucoseCal" :  weighted_avg }

    return JSONResponse(
        response,
        status_code=200
    )

@measure.post("/measure/search", tags=["measures"])
def search_measures(measure_user_search: MeasureUserSearch):
    """Realiza la busqueda de las mediciones de un usuario enviando los datos del 
    modelo: MeasureUserSearch Devuelve el listado con todas las mediciones para ese usuario
    """
    result = conn.execute(measures.select()).fetchall()
    date_format = "%Y-%m-%d"

    measure_users = list(
        filter(
            lambda measure: 
            int(measure[3]) == int(measure_user_search.userId)  and
            str(measure[2].strftime(date_format)) == str(measure_user_search.date), 
            result
        )
    )

    measure_users = list(
        map(
            lambda measure:
            { 
                "id": measure['id'], 
                "measurement": measure['measurement'], 
                "measure_date": measure['measure_date'].strftime(time_format),
            },
            measure_users
        )
    )

    return JSONResponse(
        measure_users,
        status_code=200
    )

@measure.post("/measure/list", tags=["measures"])
def list_measure(measure_list: MeasureUserList):
    """Realiza la busqueda de las n ultimas mediciones de un usuario 
    enviando los datos del modelo: MeasureUserList  Devuelve un listado con esas mediciones
    """
    result = conn.execute(measures.select()).fetchall()
    n = measure_list.count
    measure_users = list(
        filter(
            lambda measure: 
            int(measure[3]) == int(measure_list.userId),
            result
        )
    )

    measure_users = list(
        map(
            lambda measure:
            { 
                "id": measure['id'], 
                "measurement": measure['measurement'], 
                "measure_date": measure['measure_date'],
                "measure_time": measure['measure_date'].strftime(time_format),
            },
            measure_users
        )
    )

    # obtengo los n ultimos
    measure_users = measure_users[-n:]
    return measure_users



