import datetime as dt
import sqlalchemy.orm as orm
from src import database as db, models as _model, schemas as schema

# 3
def create_database():
    return db.Base.metadata.create_all(bind=db.engine)

# 6
def get_db():
    data = db.SessionLocal()
    try:
        yield data
    finally:
        data.close()

def get_user_by_email(db: orm.Session, email: str):
    return db.query(_model.User).filter(_model.User.email == email).first()

# 7
def create_user(db: orm.Session, user: schema.UserCreate):
    fake_hashed_password = user.password + "thisisnotsecure"
    db_user = _model.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 11
def get_users(db: orm.Session, skip: int, limit: int):
    return db.query(_model.User).offset(skip).limit(limit).all()

def get_user(db: orm.Session, user_id: int):
    return db.query(_model.User).filter(_model.User.id == user_id).first()

def create_post(db: orm.Session, post: schema.PostCreate, user_id: int):
    post = _model.Post(**post.dict(), owner_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_posts(db: orm.Session, skip: int, limit: int):
    return db.query(_model.Post).offset(skip).limit(limit).all()

def get_post(db: orm.Session, post: int):
    return db.query(_model.Post).filter(_model.Post.id == post_id).first() 

def delete_post(db: orm.Session, post_id: int):
    db.query(_model.Post).filter(_model.Post.id == post_id).delete()
    db.commit()

def update_post(db: orm.Session, post= schema.PostCreate,post_id: int):
    db_post = get_post(db=db, post_id=post_id)
    db_post.title = post.title
    db_post.content = post.content
    db_post.date_last_modified = dt.datetime.now()
    db.commit()
    db.refresh(db_post)
    return db_post
