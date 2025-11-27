from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product_model import ProductCreate, ProductUpdate
from app.orm_db import Product


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, product_id: int) -> Product | None:
        result = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()

    async def get_by_filter(self, count: int, page: int, **kwargs) -> list[Product]:
        """page: в человеческом формате начиная с 1"""
        offset_val = (page - 1) * count

        # Build query with optional filters
        query = select(Product)

        # Apply filters from kwargs if provided
        for key, value in kwargs.items():
            if hasattr(Product, key) and value is not None:
                query = query.where(getattr(Product, key) == value)

        query = query.limit(count).offset(offset_val)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, product_data: ProductCreate) -> Product:
        product = Product(**product_data.model_dump())
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def update(
            self, product_id: int, product_data: ProductUpdate
    ) -> Product | None:
        product = await self.get_by_id(product_id)
        if product:
            update_data = product_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(product, key, value)
            await self.session.commit()
            await self.session.refresh(product)
        return product

    async def delete(self, product_id: int) -> bool:
        product = await self.get_by_id(product_id)
        if product:
            await self.session.delete(product)
            await self.session.commit()
            return True
        return False
