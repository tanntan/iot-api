from typing import Optional
from pydantic import BaseModel


class UserLogin(BaseModel):
    companyCode: str
    factoryId: int
    password: str
    username: str
    class Config:

        orm_mode = True


class User(BaseModel):
    status: int
    userId: int
    username: str
    factoryId: int
    factory: str
    role: str
    language: str
    mfgLineId: Optional[int] = None
    accessToken: str
    refreshToken: str
    class Config:

        orm_mode = True
