from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional

app = FastAPI()

SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRED_MINUTES = 30

# class Data(BaseModel):
#     name: str


# @app.post("/create/")
# async def create(data: Data):
#     return {"data": data}

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}
