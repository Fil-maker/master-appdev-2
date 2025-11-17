import pytest
from unittest.mock import AsyncMock, MagicMock

from litestar.di import Provide
from litestar.testing import create_test_client
from litestar.status_codes import HTTP_200_OK, HTTP_404_NOT_FOUND

from app.models.user_model import UserResponse, UserCreate, UserUpdate
from app.services.user_service import UserService


def test_get_user_by_id_success():
    """Тест успешного получения пользователя по ID"""
    # Arrange
    mock_user_service = AsyncMock(spec=UserService)
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.first_name = "John"
    mock_user.second_name = "Doe"
    mock_user.username = "johndoe"
    mock_user.email = "john@example.com"

    mock_user_service.get_by_id.return_value = mock_user

    from app.controllers.user_controller import UserController

    # Act
    with create_test_client(
            route_handlers=[UserController],
            dependencies={"user_service": Provide(lambda: mock_user_service)}
    ) as client:
        response = client.get("/users/1")

    # Assert
    assert response.status_code == HTTP_200_OK
    response_data = response.json()
    assert response_data["id"] == 1
    assert response_data["first_name"] == "John"
    assert response_data["second_name"] == "Doe"
    assert response_data["username"] == "johndoe"
    assert response_data["email"] == "john@example.com"

    mock_user_service.get_by_id.assert_called_once_with(1)


def test_get_user_by_id_not_found():
    """Тест случая, когда пользователь не найден"""
    # Arrange
    mock_user_service = AsyncMock(spec=UserService)
    mock_user_service.get_by_id.return_value = None

    from app.controllers.user_controller import UserController

    # Act
    with create_test_client(
            route_handlers=[UserController],
            dependencies={"user_service": Provide(lambda: mock_user_service)}
    ) as client:
        response = client.get("/users/999")

    # Assert
    assert response.status_code == HTTP_200_OK  # Так как возвращается строка, а не исключение
    assert response.text == "User with ID 999 not found"
    mock_user_service.get_by_id.assert_called_once_with(999)


def test_get_user_by_id_invalid_id():
    """Тест с невалидным ID (меньше или равно 0)"""
    from app.controllers.user_controller import UserController

    with create_test_client(
            route_handlers=[UserController],
            dependencies={"user_service": Provide(lambda: AsyncMock(spec=UserService))}
    ) as client:
        # ID должен быть > 0 согласно параметру gt=0
        response = client.get("/users/0")

    # Должна быть ошибка валидации
    assert response.status_code == 400  # Bad Request


@pytest.mark.asyncio
async def test_get_user_by_id_direct_call():
    """Тест прямого вызова метода контроллера"""
    # Arrange
    mock_user_service = AsyncMock(spec=UserService)
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.first_name = "John"
    mock_user.second_name = "Doe"
    mock_user.username = "johndoe"
    mock_user.email = "john@example.com"

    mock_user_service.get_by_id.return_value = mock_user

    from app.controllers.user_controller import UserController
    controller = UserController()

    # Act
    result = await controller.get_user_by_id(
        user_service=mock_user_service,
        user_id=1
    )

    # Assert
    assert isinstance(result, UserResponse)
    assert result.id == 1
    assert result.first_name == "John"
    assert result.second_name == "Doe"
    assert result.username == "johndoe"
    assert result.email == "john@example.com"
    mock_user_service.get_by_id.assert_called_once_with(1)


def test_get_all_users():
    """Тест получения всех пользователей"""
    # Arrange
    mock_user_service = AsyncMock(spec=UserService)

    # Создаем мок-пользователей
    mock_user1 = MagicMock()
    mock_user1.id = 1
    mock_user1.first_name = "John"
    mock_user1.second_name = "Doe"
    mock_user1.username = "johndoe"
    mock_user1.email = "john@example.com"

    mock_user2 = MagicMock()
    mock_user2.id = 2
    mock_user2.first_name = "Jane"
    mock_user2.second_name = "Smith"
    mock_user2.username = "janesmith"
    mock_user2.email = "jane@example.com"

    mock_user_service.get_by_filter.return_value = [mock_user1, mock_user2]

    from app.controllers.user_controller import UserController

    # Act
    with create_test_client(
            route_handlers=[UserController],
            dependencies={"user_service": Provide(lambda: mock_user_service)}
    ) as client:
        response = client.get("/users")

    # Assert
    assert response.status_code == HTTP_200_OK
    response_data = response.json()
    assert len(response_data) == 2

    assert response_data[0]["id"] == 1
    assert response_data[0]["first_name"] == "John"
    assert response_data[1]["id"] == 2
    assert response_data[1]["first_name"] == "Jane"

    mock_user_service.get_by_filter.assert_called_once_with(2, 1)