from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    stock_quantity: Optional[int] = 0


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    stock_quantity: Optional[int] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    stock_quantity: Optional[int] = None
