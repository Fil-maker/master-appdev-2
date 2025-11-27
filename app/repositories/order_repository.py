from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order_model import OrderCreate, OrderUpdate
from app.orm_db import Address, Order, Product, User


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, order_id: int) -> Order | None:
        result = await self.session.execute(select(Order).where(Order.id == order_id))
        return result.scalar_one_or_none()

    async def get_by_filter(self, count: int, page: int, **kwargs) -> list[Order]:
        """page: в человеческом формате начиная с 1"""
        offset_val = (page - 1) * count
        result = await self.session.execute(
            select(Order).limit(count).offset(offset_val)
        )
        return list(result.scalars().all())

    async def create(self, order_data: OrderCreate) -> Order:
        order = Order(**order_data.model_dump())
        address = await self.session.execute(
            select(Address).where(Address.id == order_data.address_id)
        )
        products = []
        for i in order_data.products_id:
            result = await self.session.execute(select(Product).where(Product.id == i))
            products.append(result.first())
        user = await self.session.execute(
            select(User).where(User.id == order_data.user_id)
        )
        order.address = address.first()
        order.products = products
        order.user = user
        self.session.add(order)

        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def update(self, order_id: int, order_data: OrderUpdate) -> Order | None:
        order = await self.get_by_id(order_id)
        if not order:
            return None
        update_data = order_data.model_dump(exclude_unset=True)
        if update_data.get("user_id", None):
            user = await self.session.execute(
                select(User).where(User.id == order_data.user_id)
            )
            order.user = user
        if update_data.get("address_id", None):
            address = await self.session.execute(
                select(Address).where(Address.id == order_data.address_id)
            )
            order.address = address
        if update_data.get("products_id", None):
            products = []
            for i in order_data.products_id:
                result = await self.session.execute(
                    select(Product).where(Product.id == i)
                )
                products.append(result.first())
            order.products = products
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def delete(self, order_id: int) -> bool:
        order = await self.get_by_id(order_id)
        if order:
            await self.session.delete(order)
            await self.session.commit()
            return True
        return False
