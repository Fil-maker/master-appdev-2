from sqlalchemy import select, create_engine
from sqlalchemy.orm import selectinload, sessionmaker

from main import User, Address, Product, Order

connect_url = "postgresql://postgres:postgres@192.168.1.64:5432/test_db"
engine = create_engine(connect_url, echo=False)
session_factory = sessionmaker(engine)


def fill_db_with_data():
    with session_factory() as session:
        user1 = User(username="John Doe", email="jdoe@example.com")
        user2 = User(username="Josh Sber", email="josh@sber.ru",
                     description="best josh in banking")

        # address: street, city, country
        address1 = Address(country="America", city="NY", street="Washington")
        address2 = Address(country="Russia", city="Ekatrinburg", street="Rosa Lux")

        user1.addresses = [address1]
        user2.addresses = [address2]

        product1 = Product(name="Toy")
        product2 = Product(name="Box")
        product3 = Product(name="Barrel")
        product4 = Product(name="Train")
        product5 = Product(name="Car")

        order1 = Order()
        order1.user = user1
        order1.address = address1
        order1.product = product1

        order2 = Order()
        order2.user = user2
        order2.address = address2
        order2.product = product2

        order3 = Order()
        order3.user = user1
        order3.address = address1
        order3.product = product3

        order4 = Order()
        order4.user = user2
        order4.address = address2
        order4.product = product4

        order5 = Order()
        order5.user = user1
        order5.address = address1
        order5.product = product5

        session.add(order1)
        session.add(order2)
        session.add(order3)
        session.add(order4)
        session.add(order5)

        session.commit()


def drop_unit(unit):
    stmt = select(unit)
    with session_factory() as session:
        results = session.execute(stmt).scalars().all()
        for res in results:
            session.delete(res)
        session.commit()


def drop_all():
    drop_unit(User)
    drop_unit(Address)
    drop_unit(Product)
    drop_unit(Order)


def print_all_data():
    print("Users:")
    stmt = select(User).options(selectinload(User.addresses))
    with session_factory() as session:
        users = session.execute(stmt).scalars().all()
        for i in range(len(users)):
            print(i + 1, users[i].username, users[i].addresses[0].city)
    print("\nAddresses")
    stmt = select(Address).options()
    with session_factory() as session:
        addresses = session.execute(stmt).scalars().all()
        for i in range(len(addresses)):
            print(i + 1, addresses[i].city, addresses[i].street)
    print("\nProducts:")
    stmt = select(Product).options()
    with session_factory() as session:
        products = session.execute(stmt).scalars().all()
        for i in range(len(products)):
            print(i + 1, products[i].name)
    print("\nOrders")
    stmt = select(Order).options(selectinload(Order.address), selectinload(Order.user), selectinload(Order.product))
    with session_factory() as session:
        orders = session.execute(stmt).scalars().all()
        for i in range(len(orders)):
            print(i, orders[i].user.username, orders[i].product.name, orders[i].address.city,
                  orders[i].address.street + " street", sep=", ")


if __name__ == '__main__':
    drop_all()
    fill_db_with_data()
    print_all_data()
