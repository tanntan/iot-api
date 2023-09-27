import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

class BaseConfig(object):
    HOST = os.getenv("HOST")
    APP_PORT = os.getenv("APP_PORT")
    APP_MODE = os.getenv('APP_MODE')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD') 
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT') or 5432
    DB_DATABASE = os.getenv('DB_DATABASE') or 'iot'
    DATABASE_URL = os.getenv('DATABASE_URL') or f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
