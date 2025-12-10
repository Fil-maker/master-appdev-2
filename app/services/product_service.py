from litestar.exceptions import NotFoundException

from app.models.product_model import ProductCreate, ProductUpdate
from app.orm_db import Product
from app.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def get_by_id(self, product_id: int) -> Product | None:
        """Get order by ID"""
        product = await self.product_repository.get_by_id(product_id)
        if product:
            return product
        return None

    async def get_by_filter(self, count: int, page: int, **kwargs) -> list[Product]:
        products = await self.product_repository.get_by_filter(count, page, **kwargs)
        return products

    async def create(self, product_data: ProductCreate) -> Product:
        product = await self.product_repository.create(product_data)
        return product

    async def update(self, product_id: int, product_data: ProductUpdate) -> Product:
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise NotFoundException(detail=f"Product with ID {product_id} not found")

        updated_product = await self.product_repository.update(product_id, product_data)
        return updated_product

    async def delete(self, product_id: int) -> None:
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise NotFoundException(detail=f"Product with ID {product_id} not found")
        await self.product_repository.delete(product_id)
