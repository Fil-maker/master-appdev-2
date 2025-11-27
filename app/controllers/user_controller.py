from typing import List

from litestar import Controller, delete, get, post, put
from litestar.di import Provide
from litestar.params import Parameter

from app.models.user_model import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService


class UserController(Controller):
    path = "/users"
    dependencies = {"user_service": Provide(UserService)}

    @get("/{user_id:int}")
    async def get_user_by_id(
            self,
            user_service: UserService,
            user_id: int = Parameter(gt=0),
    ) -> UserResponse:
        """Получить пользователя по ID"""
        user = await user_service.get_by_id(user_id)
        if not user:
            return f"User with ID {user_id} not found"
            # raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(
            UserResponse(
                id=user.id,
                first_name=user.first_name,
                second_name=user.second_name,
                username=user.username,
                email=user.email,
            )
        )

    @get()
    async def get_all_users(
            self,
            user_service: UserService,
    ) -> List[UserResponse]:
        """Задавать параметры пагинации"""
        result = await user_service.get_by_filter(2, 1)
        users = [
            UserResponse.model_validate(
                UserResponse(
                    id=user.id,
                    first_name=user.first_name,
                    second_name=user.second_name,
                    username=user.username,
                    email=user.email,
                )
            )
            for user in result
        ]
        return users

    @post()
    async def create_user(
            self,
            user_service: UserService,
            user_data: UserCreate,
    ) -> UserResponse:
        try:
            user = await user_service.create(user_data)
        except ValueError as e:
            return e.args
        return UserResponse(
            id=user.id,
            first_name=user.first_name,
            second_name=user.second_name,
            username=user.username,
            email=user.email,
        )

    @delete("/{user_id:int}")
    async def delete_user(
            self,
            user_service: UserService,
            user_id: int,
    ) -> None:
        await user_service.delete(user_id)

    @put("/{user_id:int}")
    async def update_user(
            self,
            user_service: UserService,
            user_id: int,
            user_data: UserUpdate,
    ) -> UserResponse:
        try:
            user = await user_service.update(user_id, user_data)
        except Exception as e:
            return e.args
        return UserResponse(
            id=user.id,
            first_name=user.first_name,
            second_name=user.second_name,
            username=user.username,
            email=user.email,
        )
