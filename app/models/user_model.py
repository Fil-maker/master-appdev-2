from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    first_name: str
    second_name: str
    username: str


class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str
    second_name: str
    email: str


class UserUpdate(BaseModel):
    username: str
    first_name: str
    second_name: str
