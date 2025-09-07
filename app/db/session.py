import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_NAME = os.getenv("PG_DB")
if SQLALCHEMY_DATABASE_NAME is None:
    os._exit(1)


engine = create_engine(SQLALCHEMY_DATABASE_NAME)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
