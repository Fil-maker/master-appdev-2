import os

from faststream import FastStream
from faststream.rabbit import RabbitBroker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = os.getenv("DATABASE_URL",
                              "postgresql+asyncpg://safe_postgres_user:postgres!kio9@217.76.176.93/test_db")
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
broker = RabbitBroker("amqp://guest:guest@217.76.176.93:5672/local")
app = FastStream(broker)

from app.main import (provide_order_repository, provide_order_service,
                      provide_product_repository, provide_product_service)
from app.models.order_model import OrderCreate
from app.models.product_model import ProductCreate


@broker.subscriber("order_create")
async def subscribe_order(
        order: OrderCreate
):
    async with async_session_factory() as session:
        repository = await provide_order_repository(session)
        service = await provide_order_service(repository)
        await service.create(order)
        print(order)


@broker.subscriber("product_create")
async def subscribe_product_create(
        product: ProductCreate
):
    async with async_session_factory() as session:
        repository = await provide_product_repository(session)
        service = await provide_product_service(repository)
        await service.create(product)
        print(product)
