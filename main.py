from typing import Union, List
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class UserName(str, Enum):
    robert = "robert"
    lance = "lance"
    eugine = "eugine"


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



###@app.get("/items/{item_id}")
###def read_item(item_id: int, q: Union[str, None] = None):
###    return {"item_id": item_id, "q": q}


###@app.put("/items/{item_id}")
###def update_item(item_id: int, item: Item):
 ###   return {"item_name": item.name, "item_id": item_id}