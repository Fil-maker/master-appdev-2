from typing import Optional

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    stock_quantity: Optional[int] = None


class ProductUpdate(BaseModel):
    name: Optional[str]
    stock_quantity: Optional[int] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    stock_quantity: int
