import pytest

from app.models.address_model import AddressCreate
from app.models.order_model import OrderCreate, OrderUpdate
from app.models.product_model import ProductCreate
from app.models.user_model import UserCreate
from app.repositories.address_repository import AddressRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository


class TestOrderRepository:
    @pytest.mark.asyncio
    async def test_create_order(
            self,
            address_repository: AddressRepository,
            user_repository: UserRepository,
            product_repository: ProductRepository,
            order_repository: OrderRepository,
    ):
        """Test создания order в репозитории"""
        user = await user_repository.create(
            UserCreate(
                email="unique@example.com",
                username="user_test",
                first_name="Test",
                last_name="User",
            )
        )

        product1 = await product_repository.create(ProductCreate(name="laptop"))
        product2 = await product_repository.create(ProductCreate(name="table"))
        products = [product1, product2]

        order = await order_repository.create(
            OrderCreate(
                user_id=user.id,
                address_id=address_repository.create(
                    AddressCreate(country="America", city="NY", street="Washington")
                ),
                products_id=[p.id for p in products],
            )
        )

        assert order.id is not None
        assert order.user.username == "user_test"

    @pytest.mark.asyncio
    async def test_edit_order(
            self,
            address_repository: AddressRepository,
            user_repository: UserRepository,
            product_repository: ProductRepository,
            order_repository: OrderRepository,
    ):
        """Test edit order в репозитории"""
        user = await user_repository.create(
            UserCreate(
                email="unique@example.com",
                username="user_test",
                first_name="Test",
                last_name="User",
            )
        )

        product1 = await product_repository.create(ProductCreate(name="laptop"))
        product2 = await product_repository.create(ProductCreate(name="table"))
        products = [product1, product2]

        order = await order_repository.create(
            OrderCreate(
                user_id=user.id,
                address_id=address_repository.create(
                    AddressCreate(country="America", city="NY", street="Washington")
                ),
                products_id=[p.id for p in products],
            )
        )

        update_address = await address_repository.create(
            AddressCreate(country="Russia", city="Moscow", street="Lenina")
        )
        updated_order = await order_repository.update(
            order.id, OrderUpdate(address=update_address.id)
        )

        assert updated_order.address.country == "Russia"

    @pytest.mark.asyncio
    async def test_delete_order(
            self,
            address_repository: AddressRepository,
            user_repository: UserRepository,
            product_repository: ProductRepository,
            order_repository: OrderRepository,
    ):
        """Test delete order в репозитории"""
        user = await user_repository.create(
            UserCreate(
                email="unique@example.com",
                username="user_test",
                first_name="Test",
                last_name="User",
            )
        )

        product1 = await product_repository.create(ProductCreate(name="laptop"))
        product2 = await product_repository.create(ProductCreate(name="table"))
        products = [product1, product2]

        order = await order_repository.create(
            OrderCreate(
                user_id=user.id,
                address_id=address_repository.create(
                    AddressCreate(country="America", city="NY", street="Washington")
                ),
                products_id=[p.id for p in products],
            )
        )

        await order_repository.delete(order_id=order.id)
        deleted_order = order_repository.get_by_id(order_id=order.id)

        assert deleted_order is None
