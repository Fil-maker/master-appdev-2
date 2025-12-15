from typing import List

from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from litestar.params import Parameter

from app.models.product_model import (ProductCreate, ProductResponse,
                                      ProductUpdate)
from app.redisCache import RedisCache
from app.services.product_service import ProductService


class ProductController(Controller):
    path = "/products"
    dependencies = {"product_service": Provide(ProductService)}

    @get("/{product_id:int}")
    async def get_product_by_id(
            self,
            product_service: ProductService,
            product_id: int = Parameter(gt=0),
    ) -> str:
        """Получить продукт по ID"""
        cache = RedisCache()
        await cache.connect()
        product = await cache.get(f"product_{product_id}")
        if product is None:
            product = await product_service.get_by_id(product_id)
            if product is not None:
                await cache.set(f"product_{product_id}", ProductResponse(
                    id=product.id,
                    name=product.name,
                    stock_quantity=product.stock_quantity
                ).model_dump(), ttl=60 * 10)
                product = ProductResponse(
                    id=product.id,
                    name=product.name,
                    stock_quantity=product.stock_quantity
                )
        await cache.connect()
        if not product:
            return f"Product with ID {product_id} not found"
        return product

    @get()
    async def get_all_products(
            self,
            product_service: ProductService,
    ) -> List[ProductResponse]:
        """Задавать параметры пагинации"""
        result = await product_service.get_by_filter(2, 1)
        products = [
            ProductResponse.model_validate(
                ProductResponse(
                    id=product.id,
                    name=product.name,
                    stock_quantity=product.stock_quantity
                )
            )
            for product in result
        ]
        return products

    @post()
    async def create_product(
            self,
            product_service: ProductService,
            product_data: ProductCreate,
    ) -> ProductResponse:
        try:
            product = await product_service.create(product_data)
        except ValueError as e:
            return e.args
        return ProductResponse(
            id=product.id,
            name=product.name,
            stock_quantity=product.stock_quantity
        )

    @delete("/{product_id:int}")
    async def delete_product(
            self,
            product_service: ProductService,
            product_id: int,
    ) -> None:
        await product_service.delete(product_id)
        cache = RedisCache()
        await cache.connect()
        await cache.delete(f"product_{product_id}")

    @put("/{product_id:int}")
    async def update_product(
            self,
            product_service: ProductService,
            product_id: int,
            product_data: ProductUpdate,
    ) -> ProductResponse:
        try:
            product = await product_service.update(product_id, product_data)
            cache = RedisCache()
            await cache.connect()
            await cache.delete(f"product_{product_id}")
            await cache.set(f"product_{product_id}", ProductResponse(
                id=product.id,
                name=product.name,
                stock_quantity=product.stock_quantity
            ).model_dump(), ttl=60 * 10)
            await cache.disconnect()
        except Exception as e:
            return e.args
        return ProductResponse(
            id=product.id,
            name=product.name,
            stock_quantity=product.stock_quantity
        )
