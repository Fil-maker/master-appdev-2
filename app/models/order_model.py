from pydantic import BaseModel, ConfigDict
from app.models.user_model import UserResponse
from app.models.address_model import AddressResponse
from app.models.product_model import ProductResponse
from datetime import datetime
from typing import Optional


class OrderCreate(BaseModel):
    user_id: int
    address_id: int
    products_id: list[int]


class OrderUpdate(BaseModel):
    user_id: Optional[int]
    address_id: Optional[int]
    products_id: Optional[list[int]]


class OrderResponse(BaseModel):
    id: int
    user: UserResponse
    address: AddressResponse
    products: list[ProductResponse]
