import pytest
from app.models.user_model import UserCreate, UserUpdate
from app.repositories.user_repository import UserRepository


class TestUserRepository:
    @pytest.mark.asyncio
    async def test_create_user(self, user_repository: UserRepository):
        """Test создания пользователя в репозитории"""
        user_data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
        }

        user = await user_repository.create(UserCreate(**user_data))

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"

    @pytest.mark.asyncio
    async def test_get_user_by_email(self, user_repository: UserRepository):
        """Test получения пользователя по email"""
        # Сначала создаем пользователя
        user = await user_repository.create(UserCreate(
            email="unique@example.com",
            username="user_test",
            first_name="Test",
            last_name="User")
        )

        # Затем ищем по email
        found_user = await user_repository.get_by_email("unique@example.com")
        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.email == "unique@example.com"

    @pytest.mark.asyncio
    async def test_update_user(self, user_repository: UserRepository):
        """Test обновления пользователя"""
        user = await user_repository.create(UserCreate(
            email="update@example.com",
            username="test",
            first_name="Original",
            last_name="Name")
        )

        updated_user = await user_repository.update(user.id, UserUpdate(
            first_name="Updated"
        ))

        assert updated_user.username == "test"
        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Name"  # НЕ ИЗМЕНИЛОСЬ

    @pytest.mark.asyncio
    async def test_delete_user(self, user_repository: UserRepository):
        """Test удаления пользователя"""
        user = await user_repository.create(UserCreate(
            email="update@example.com",
            username="test",
            first_name="Original",
            last_name="Name")
        )

        await user_repository.delete(user_id=user.id)
        found_user = await user_repository.get_by_id(user_id=user.id)
        assert found_user is None

    @pytest.mark.asyncio
    async def test_get_list_user(self, user_repository: UserRepository):
        """Test получения списка пользователей"""
        user1 = await user_repository.create(UserCreate(
            email="update@example.com",
            username="test1",
            first_name="Original1",
            last_name="Name1")
        )
        user2 = await user_repository.create(UserCreate(
            email="update2@example.com",
            username="test2",
            first_name="Original2",
            last_name="Name2")
        )

        users = await user_repository.get_by_filter(2, 1)

        assert len(users) == 2
