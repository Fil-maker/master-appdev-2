from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.address_model import AddressCreate
from app.orm_db import Address


class AddressRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, address_id: int) -> Address | None:
        result = await self.session.execute(
            select(Address).where(Address.id == address_id)
        )
        return result.scalar_one_or_none()

    async def get_by_filter(self, count: int, page: int, **kwargs) -> list[Address]:
        """page: в человеческом формате начиная с 1"""
        offset_val = (page - 1) * count

        query = select(Address)

        # Apply filters from kwargs if provided
        for key, value in kwargs.items():
            if hasattr(Address, key) and value is not None:
                query = query.where(getattr(Address, key) == value)

        query = query.limit(count).offset(offset_val)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, address_data: AddressCreate) -> Address:
        address = Address(**address_data.model_dump())
        self.session.add(address)
        await self.session.commit()
        await self.session.refresh(address)
        return address
