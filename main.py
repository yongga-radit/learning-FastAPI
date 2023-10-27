from typing import Optional, Union
from fastapi import Depends, FastAPI, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId
import random
import string

from datetime import datetime, timedelta
# from jose import JWTError, jwt
from passlib.context import CryptContext
from typing_extensions import Annotated

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# -----------------
# # database config
# URL = "mongodb://localhost:27017" #mongo
# CLIENT = AsyncIOMotorClient(URL)
# DATABASE = CLIENT["auth_example"]

# # model
# class User(BaseModel):
#     username: str
#     password: str

# # collection
# user_collection = DATABASE["users"]

# # method
# def generate_activation_code():
#     return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# # endpoint method
# @app.post("/sign-up", response_model=User)
# async def sign_up(user: User):
#     # check if the username already taken
#     exisitng_user = await user_collection.find_one({"username": user.username})
#     if exisitng_user:
#         raise HTTPException(status_code=400, detail="Username is already taken")

#     # generate activation code
#     activation_code = generate_activation_code()

#     # insert user with an activation code into database
#     user_dict = user.dict()
#     user_dict["activation_code"] = activation_code
#     await user_collection.insert_one(user_dict)

#     return user

# # activation endpoint
# @app.get("/activate/{activation_code}")
# async def activate(activation_code: str):
#     # find user with activation code
#     user = await user_collection.find_one({"activation_code": activation_code})
#     if not user:
#         raise HTTPException(status_code=404, detail="Activation code not found")
    
#     # remove activation_code and activate the user
#     await user_collection.update_one({"_id": user["_id"]},
#                                      {"$unset": {"activation_code": 1}})
#     return {"message": "Activation successful"}

# # sign-in endpoint
# @app.post("sign-in", response_model=User)
# async def sign_in(user: User):
#     # find user by username and password
#     user_doc = await user_collection.find_one({"username": user.username, 
#                                                "password": user.password})
#     if not user_doc:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
    
#     return user

# ------------------


# SECRET_KEY = ""
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRED_MINUTES = 30

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
