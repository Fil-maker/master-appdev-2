import asyncio
import sys

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from app.models.order_model import OrderCreate
from app.models.product_model import ProductCreate

broker = RabbitBroker("amqp://guest:guest@217.76.176.93:5672/local")
app = FastStream(broker)


@app.after_startup
async def test_publish():
    # UserCreate(first_name="Josh", second_name="Sber", username="josh_sber", email="josh@sber.ru"),
    # 6
    await broker.publish(
        ProductCreate(name="stol1", stock_quantity=3), "product_create")
    await broker.publish(
        ProductCreate(name="stol2", stock_quantity=3), "product_create")
    await broker.publish(
        ProductCreate(name="stol3", stock_quantity=3), "product_create")
    await broker.publish(
        ProductCreate(name="stol4", stock_quantity=3), "product_create")
    await broker.publish(
        ProductCreate(name="stol5", stock_quantity=3), "product_create")
    # 7

    await broker.publish(
        OrderCreate(user_id=1, address_id=1, products_id=[1, 2]), "order_create")
    await broker.publish(
        OrderCreate(user_id=2, address_id=1, products_id=[3, 4]), "order_create")
    await broker.publish(
        OrderCreate(user_id=2, address_id=2, products_id=[1, 5, 6]), "order_create")
    sys.exit(0)


async def main():
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
