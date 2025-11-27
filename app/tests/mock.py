from unittest.mock import AsyncMock, Mock

import pytest

from app.models.order_model import OrderCreate
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.services.order_service import OrderService


class TestOrderService:
    @pytest.mark.asyncio
    async def test_create_order_success(self):
        """Тест успешного создания заказа"""
        # Создаем мок-репозитории
        mock_order_repo = AsyncMock(spec=OrderRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)

        # Настраиваем моки
        mock_user_repo.get_by_id.return_value = Mock(id=1, email="test@example.com")
        mock_product_repo.get_by_id.return_value = Mock(
            id=1, name="Test Product", stock_quantity=5
        )
        mock_order_repo.create.return_value = Mock(id=1, user_id=1)

        order_service = OrderService(order_repository=mock_order_repo)

        order_data = {"user_id": 1, "products_id": [1]}

        result = await order_service.create(OrderCreate(**order_data))

        assert result is not None
        mock_order_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_order_insufficient_stock(self):
        """Тест создания заказа с недостаточным количеством товара"""
        mock_order_repo = AsyncMock(spec=OrderRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)

        mock_user_repo.get_by_id.return_value = Mock(id=1)
        mock_product_repo.get_by_id.return_value = Mock(
            id=1, name="Test Product", stock_quantity=1
        )

        order_service = OrderService(order_repository=mock_order_repo)

        order_data = {"user_id": 1, "products_id": [1]}

        with pytest.raises(ValueError, match="Insufficient stock"):
            await order_service.create(OrderCreate(**order_data))
