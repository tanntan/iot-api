from sqlalchemy import Column, Integer, String
from app import Base
from app.api.models import *

class User(Base, Mixin, TrackMixin):
    __tablename__ = "users"

    username = title_column(unique=True)
    password =  text_column()