import datetime as dt
import sqlalchemy as sql
# from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
import sqlalchemy.orm as orm

from src import database as db

# 2
class User(db.Base):
    __tablename__ = "users"

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    email = sql.Column(sql.String, unique=True, index=True)
    username = sql.Column(sql.String, unique=True, index=True)
    full_name = sql.Column(sql.String, unique=False, index=True)
    hashed_password = sql.Column(sql.String)
    is_active = sql.Column(sql.Boolean, default=True)

    posts = orm.relationship("Post", back_populates="owner")

class Post(db.Base):
    __tablename__ = "posts"

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    title = sql.Column(sql.String, index=True)
    content = sql.Column(sql.String, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))
    date_created = sql.Column(sql.DateTime, default=dt.datetime.utcnow)
    date_last_modified = sql.Column(sql.DateTime, default=dt.datetime.utcnow)

    owner = orm.relationship("User", back_populates="posts")