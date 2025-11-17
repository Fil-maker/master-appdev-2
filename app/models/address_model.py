from typing import Optional

from pydantic import BaseModel


class AddressCreate(BaseModel):
    street: str
    city: str
    state: Optional[str]
    zip_code: Optional[str]
    country: str
    is_primary: Optional[str] = False


class AddressResponse(BaseModel):
    id: int
    street: str
    city: str
    state: Optional[str]
    zip_code: Optional[str]
    country: str
    is_primary: Optional[str] = False
