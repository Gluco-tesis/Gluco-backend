from fastapi import APIRouter, Response, responses, status
from starlette.responses import Response
from config.db import conn
from models.user import users
from schemas.user import User, UserLogin
from starlette.status import HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from cryptography.fernet import Fernet
import jwt

key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()

@user.get("/users", response_model=list[User], tags=["users"])
def get_users():
    return conn.execute(users.select()).fetchall()

@user.post("/users", response_model=User, tags=["users"])
def create_user(user: User):
    new_user = {"name": user.name, "email":user.email}
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    new_user["key"] = key.decode()
    result = conn.execute(users.insert().values(new_user))
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()

@user.get("/users/{id}", response_model=User, tags=["users"])
def get_user(id:int):
    result = conn.execute(users.select().where(users.c.id == id)).first()
    return result

@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id:int):
    # TODO: check password
    conn.execute(users.delete().where(users.c.id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)

@user.put("/users/{id}", response_model=User, tags=["users"])
def uptade_user(id:int, user: User):
    result = conn.execute(users.select().where(users.c.id == id)).first()
    user_key = result.key.encode()
    # TODO: check password
    f_user = Fernet(user_key)
    conn.execute(users.update().values(
        name=user.name, 
        email=user.email,
        password=f_user.encrypt(user.password.encode("utf-8"))
    ).where(users.c.id == id))
    return conn.execute(users.select().where(users.c.id == id)).first()

@user.post("/users/login", tags=["users"])
def login(user_login: UserLogin):
    result = conn.execute(users.select()).fetchall()
    for row in result:
        user_key = row.key.encode()
        f_user = Fernet(user_key)
        passwd = f_user.decrypt(row.password.encode("utf-8")).decode()
        if(row.email == user_login.email and passwd == user_login.password):
            payload_data = {
                "id": row.id,
                "username" : row.name,
                "email": row.email,
            }

            token = jwt.encode(
                payload = payload_data,
                key = "hola123"
            )

            return {
                "username" : row.name,
                "email": row.email,
                "token": token
            }
    
    return Response(status_code=HTTP_401_UNAUTHORIZED)
