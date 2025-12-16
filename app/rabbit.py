import os

from aio_pika import ExchangeType
from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue
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

exch = RabbitExchange("report", type=ExchangeType.TOPIC)

from app.main import (provide_order_repository, provide_order_service,
                      provide_product_repository, provide_product_service,
                      provide_report_repository)
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


queue_1 = RabbitQueue("cmd_order", routing_key="*.info",
                      arguments={"x-dead-letter-exchange": "", "x-dead-letter-routing-key": "cmd_order.dead_letter"})
queue_2 = RabbitQueue("cmd_order.dead_letter", routing_key="*.info")


@broker.subscriber(queue_1, exch)
async def get_order_report(msg):
    async with async_session_factory() as session:
        order_repository = await provide_order_repository(session)
        orders = await order_repository.get_by_filter(10, 1)
    async with async_session_factory() as session:
        report_repository = await provide_report_repository(session)
        for order in orders:
            await report_repository.create(order.id)


@broker.subscriber(queue_2, exch)
async def get_order_report_dead(msg):
    # print(smth)
    return "Hello world"
