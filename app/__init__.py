
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from app.api.config.config import BaseConfig

SQLALCHEMY_DATABASE_URL = f"postgresql://{BaseConfig.DB_USERNAME}:{BaseConfig.DB_PASSWORD}@{BaseConfig.DB_HOST}:{BaseConfig.DB_PORT}/{BaseConfig.DB_DATABASE}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    try:
        db = Session(bind=engine)
        yield db
    finally:
        db.close()
