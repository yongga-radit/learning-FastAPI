import sqlalchemy as sql
import sqlalchemy.ext.declarative as declare
import sqlalchemy.orm as orm

# 1
# mariadb_uri = f"mariadb+mariadbconnector://root:password@localhost:3306/database_test"
# mariadb_engine = sql.create_engine(mariadb_uri, pool_size=5, pool_recycle=1800)
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = sql.create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base  = declare.declarative_base()

