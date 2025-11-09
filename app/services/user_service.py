from litestar.exceptions import NotFoundException
from app.models.user_model import UserCreate, UserUpdate
from app.repositories.user_repository import UserRepository
from orm_db import User


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(self, user_id: int) -> User | None:
        """Get user by ID"""
        user = await self.user_repository.get_by_id(user_id)
        if user:
            return user
        return None

    async def get_by_filter(self, count: int, page: int, **kwargs) -> list[User]:
        users = await self.user_repository.get_by_filter(count, page)
        return users

    async def create(self, user_data: UserCreate) -> User:
        existing_user = await self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        user = await self.user_repository.create(user_data)
        return user

    async def update(self, user_id: int, user_data: UserUpdate) -> User:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")

        if user_data.email != user.email:
            existing_user = await self.user_repository.get_by_email(user_data.email)
            if existing_user:
                raise ValueError("User with this email already exists")

        updated_user = await self.user_repository.update(user_id, user_data)
        return updated_user

    async def delete(self, user_id: int) -> None:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        success = await self.user_repository.delete(user_id)
        return success
