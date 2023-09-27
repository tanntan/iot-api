import os
from datetime import timedelta


class BaseConfig(object):
    HOST = 'localhost'
    APP_PORT = 8003
    APP_MODE = 'iot'
    DB_USERNAME = 'postgres'
    DB_PASSWORD ='BSmis2008'
    DB_HOST ='localhost'
    DB_PORT = 5432
    DB_DATABASE = 'iot'
    DATABASE_URL =f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    SQLALCHEMY_DATABASE_URI =f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
