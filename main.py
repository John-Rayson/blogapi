from typing import Union, List
from fastapi import FastAPI, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from enum import Enum
from datetime import datetime, timedelta

app = FastAPI()
auth = AuthJWT(secret_key="my-secret-key", algorithms=["HS256"])

TOKEN_EXPIRATION = timedelta(hours=1)

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class UserName(str, Enum):
    robert = "robert"
    lance = "lance"
    eugine = "eugine"


@auth.verify_token
def verify_token(token):
    try:
        payload = auth.decode_token(token)
        return payload["sub"]
    except:
        return None


@app.post("/login")
def login(user_name: str, password: str, auth: AuthJWT = Depends()):
    # check user credentials here
    if user_name == "admin" and password == "password":
        access_token = auth.create_access_token(subject=user_name, expires_time=TOKEN_EXPIRATION)
        return {"access_token": access_token}

    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/protected")
def protected(user_name=Depends(verify_token)):
    if not user_name:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"user_name": user_name, "message": "This is a protected endpoint"}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users/{user_name}")
async def get_username(user_name: UserName):
    if user_name is UserName.robert:
        return {"user_name": user_name, "message": "HELLO MY NAME IS ROBERT"}

    if user_name.value == "lance":
        return {"user_name": user_name, "message": "YOOO! AKO SI LANCE"}

    return {"user_name": user_name, "message": "Kon'nichiwa, watashinonamaeha yujindesu"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}