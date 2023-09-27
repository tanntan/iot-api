
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:BSmis2008@localhost/iot"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    try:
        db = Session(bind=engine)
        yield db
    finally:
        db.close()
