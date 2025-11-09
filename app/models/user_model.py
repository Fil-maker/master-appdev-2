from pydantic import BaseModel

from orm_db import User


class UserCreate(BaseModel):
    username: str
    email: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class UserUpdate(BaseModel):
    username: str
