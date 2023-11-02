import datetime as dt
import fastapi.security as secure
import fastapi as fa
import sqlalchemy.orm as orm
import passlib.hash as _hash
import jwt
from src import database as db, models as _model, schemas as schema

outh2schema = secure.OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = "my_secret"
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

async def get_user_by_email(db: orm.Session, email: str):
    return db.query(_model.User).filter(_model.User.email == email).first()

# 7
async def create_user(db: orm.Session, user: schema.UserCreate):
    user_obj = _model.User(email=user.email, 
                           hashed_password=_hash.bcrypt.hash(user.hashed_password)
                )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

    # fake_hashed_password = user.password + "thisisnotsecure"
    # db_user = _model.User(email=user.email, hashed_password=fake_hashed_password)
    # db.add(db_user)
    # db.commit()
    # db.refresh(db_user)
    # return db_user

async def authenticate_user(email: str, password: str, db: orm.Session):
    user = await get_user_by_email(db, email)
    
    if not user:
        return False
    
    if not user.verify_password(password):
        return False
    
    return user

async def create_token(user: _model.User):
    user_obj = schema.User.from_orm(user)

    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return dict(access_token=token, token_type="bearer")

# 11
def get_users(db: orm.Session, skip: int, limit: int):
    return db.query(_model.User).offset(skip).limit(limit).all()

def get_current_user(
        db: orm.Session = fa.Depends(get_db),
        token: str = fa.Depends(outh2schema),
):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_model.User).get(payload["id"])
    except:
        raise fa.HTTPException(401, "Invalid email or Password")
    
    return schema.User.from_orm(user)

# def get_user(db: orm.Session, user_id: int):
#     return db.query(_model.User).filter(_model.User.id == user_id).first()

def create_post(db: orm.Session, post: schema.PostCreate, user_id: int):
    post = _model.Post(**post.dict(), owner_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_posts(db: orm.Session, skip: int, limit: int):
    return db.query(_model.Post).offset(skip).limit(limit).all()

def create_post(db: orm.Session, post: schema.PostCreate, user_id: int):
    post = _model.Post(**post.dict(), owner_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_post(db: orm.Session, post_id: int):
    return db.query(_model.Post).filter(_model.Post.id == post_id).first() 

def delete_post(db: orm.Session, post_id: int):
    db.query(_model.Post).filter(_model.Post.id == post_id).delete()
    db.commit()

def update_post(db: orm.Session, post_id: int, post= schema.PostCreate):
    db_post = get_post(db=db, post_id=post_id)
    db_post.title = post.title
    db_post.content = post.content
    db_post.date_last_modified = dt.datetime.now()
    db.commit()
    db.refresh(db_post)
    return db_post
