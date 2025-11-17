from litestar.exceptions import NotFoundException
from app.models.order_model import OrderCreate, OrderUpdate
from app.repositories.order_repository import OrderRepository
from app.orm_db import Order


class OrderService:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def get_by_id(self, order_id: int) -> Order | None:
        """Get order by ID"""
        order = await self.order_repository.get_by_id(order_id)
        if order:
            return order
        return None

    async def get_by_filter(self, count: int, page: int, **kwargs) -> list[Order]:
        orders = await self.order_repository.get_by_filter(count, page)
        return orders

    async def create(self, order_data: OrderCreate) -> Order:
        order = await self.order_repository.create(order_data)
        return order

    async def update(self, order_id: int, order_data: OrderUpdate) -> Order:
        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise NotFoundException(detail=f"Order with ID {order_id} not found")

        updated_order = await self.order_repository.update(order_id, order_data)
        return updated_order

    async def delete(self, order_id: int) -> None:
        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise NotFoundException(detail=f"Order with ID {order_id} not found")
        await self.order_repository.delete(order_id)
