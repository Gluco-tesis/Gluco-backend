from fastapi import APIRouter, Response, status
from starlette.responses import Response
from config.db import conn
from models.user import users, codes
from schemas.user import UserCreate, UserEdit, UserLogin, UserForgotPassword, UserChangePassword
from starlette.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
from utils import emaillUtil
from sqlalchemy import and_
import jwt, random

key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()

@user.get("/users", response_model=list[UserCreate], tags=["users"])
def get_users():
    """Lista todos los usuarios de la BD"""
    return conn.execute(users.select()).fetchall()

@user.post("/users", response_model=UserCreate, tags=["users"])
def create_user(user: UserCreate):
    """ Crea Un nuevo Usuario en la base de datos pide como modelo:
        name: str
        lastname: str
        email: str
        password: str
        phone: str
    """
    new_user = {"name": user.name, "lastname": user.lastname, "email":user.email, "phone": user.phone}
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    new_user["key"] = key.decode()
    result = conn.execute(users.insert().values(new_user))
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()

@user.get("/users/{id}", response_model=UserCreate, tags=["users"])
def get_user(id:int):
    """ Devuelve los datos de un usuario en particular pasandole su id"""
    result = conn.execute(users.select().where(users.c.id == id)).first()
    return result

@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id:int):
    """ Elimina los datos de un usuario en particular pasandole su id"""
    # TODO: check password
    conn.execute(users.delete().where(users.c.id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)

@user.put("/users/{id}", response_model=UserEdit, tags=["users"])
def uptade_user(id:int, user: UserEdit):
    """ Edita los datos de un usuario en particular es necesario pasarle 
    la id en la url y enviar el modelo: 
        name: str
        lastname: str
        password: str
        phone: str
    """
    result = conn.execute(users.select().where(users.c.id == id)).first()
    user_key = result.key.encode()
    f_user = Fernet(user_key)
    conn.execute(users.update().values(
        name=user.name,
        lastname=user.lastname,
        password=f_user.encrypt(user.password.encode("utf-8")),
        phone=user.phone
    ).where(users.c.id == id))
    return conn.execute(users.select().where(users.c.id == id)).first()

@user.post("/users/login", tags=["users"])
def login(user_login: UserLogin):
    """Permite a un usuario logearse a la aplicacion devolviendo sus datos
    Pide el moelo:
        email: str
        password: str
    """
    print(user_login)
    result = conn.execute(users.select()).fetchall()
    for row in result:
        user_key = row.key.encode()
        f_user = Fernet(user_key)
        passwd = f_user.decrypt(row.password.encode("utf-8")).decode()
        if(row.email == user_login.email and passwd == user_login.password):
            payload_data = {
                "id": row.id,
                "name" : row.name,
                "lastname" : row.lastname,
                "email": row.email,
                "phone": row.phone,
            }

            token = jwt.encode(
                payload = payload_data,
                key = "hola123"
            )

            return {
                "id": row.id,
                "name" : row.name,
                "lastname" : row.lastname,
                "email": row.email,
                "phone": row.phone,
                "token": token
            }
    return Response(status_code=HTTP_401_UNAUTHORIZED)

@user.post("/user/forgot-password/", tags=["users"])
async def forgot_password(request: UserForgotPassword):
    # Check user existed
    result = conn.execute(users.select().where(users.c.email == request.email)).first()
    if not result:
        return Response(status_code=HTTP_404_NOT_FOUND)

    # Create rest code and save in DB
    reset_code = random.randint(10000,99999)
    now = datetime.now() + timedelta(days=1)
    new_code = {
        "user_id" : result.id,
        "rest_code" : reset_code,
        "status" : "1",
        "expired_in" : now
    }

    conn.execute(codes.insert().values(new_code))

    # Sending Email
    subject = "GLUCO - Cambio de contraseña"
    recipient = [request.email]
    message = {} 
    message["email"] = request.email
    message["reset_code"] = reset_code

    await emaillUtil.send_email(subject, recipient, message)

    return {
        "code" : 200,
        "message": "Le enviamos un mail con las instrucciones para cambiar su contraseña."
    }

@user.post("/user/change-password/", tags=["users"])
def change_password(request: UserChangePassword):
    # Busco al usuario por su mail
    find_user = conn.execute(users.select().where(users.c.email == request.email)).first()
    if not find_user:
        return Response(status_code=HTTP_404_NOT_FOUND)

    # Busco el codigo por user_id, por reset_code, por estado = 1 y por fecha de expiracion

    find_code = conn.execute(
        codes.select().where(
            and_(
                codes.c.user_id == find_user.id,
                codes.c.rest_code == request.reset_code,
                codes.c.status == 1,
                codes.c.expired_in > datetime.now()
            )
        )
    ).first()

    if not find_code:
        return Response(status_code=HTTP_404_NOT_FOUND)
    
    # Cambiar la password
    user_key = find_user.key.encode()
    f_user = Fernet(user_key)
    conn.execute(users.update().values(
        password=f_user.encrypt(request.new_password.encode("utf-8"))
    ).where(users.c.id == find_user.id))

    # Cambiar estado del codigo
    conn.execute(codes.update().values(
        status = 0
    ).where(codes.c.id == find_code.id ))

    return {
        "code" : 200,
        "message": "La contraseña se cambio con éxito"
    }