from typing import List
import datetime as dt
import pydantic as pd

# 4
class _PostBase(pd.BaseModel):
    title: str
    content: str

class PostCreate(_PostBase):
    pass

class Post(_PostBase):
    id: int
    owner_id: int
    date_created: dt.datetime
    date_last_modified: dt.datetime

    class Config:
        orm_mode = True

class _UserBase(pd.BaseModel):
    email: str

class UserCreate(_UserBase):
    password: str

# {
#     "email": "john@gmail.com",
#     "id": 1,
#     "is_active": True,
#     "posts": []
# }

class User(_UserBase):
    id: int
    is_active: int
    posts: List[Post] = []

    class Config:
        orm_mode = True

# from typing import List, Union
# from pydantic import BaseModel
# from sqlalchemy.orm import Session
# import src.models as models


# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     hashed_password: str


# class User(UserBase):
#     id: int
#     username: str
#     full_name: str
#     disabled: bool
#     # is_active: bool
#     # items: List[Item] = []

#     class Config:
#         orm_mode = True



# # def get_user(db: Session, user_id: int):
# #     return db.query(User).filter(User.id == user_id).first()


# # def get_user_by_email(db: Session, email: str):
# #     return db.query(User).filter(User.email == email).first()


# # def get_users(db: Session, skip: int = 0, limit: int = 100):
# #     return db.query(User).offset(skip).limit(limit).all()


# def create_user(db: Session, user: UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, 
#                           hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user