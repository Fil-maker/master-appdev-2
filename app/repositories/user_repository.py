from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import UserCreate, UserUpdate
from app.orm_db import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_filter(self, count: int, page: int, **kwargs) -> list[User]:
        """page: в человеческом формате начиная с 1"""
        offset_val = (page - 1) * count
        result = await self.session.execute(
            select(User).limit(count).offset(offset_val)
        )
        return list(result.scalars().all())

    async def get_by_email(self, email: str) -> User:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, user_data: UserCreate) -> User:
        user = User(**user_data.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user_id: int, user_data: UserUpdate) -> User:
        user = await self.get_by_id(user_id)
        if user:
            for key, value in user_data.model_dump().items():
                setattr(user, key, value)
            await self.session.commit()
            await self.session.refresh(user)
        return user

    async def delete(self, user_id: int) -> None:
        user = await self.get_by_id(user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()
