from typing import List, Optional

from app.schemas import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService
from litestar import Controller, delete, get, post, put
from litestar.exceptions import NotFoundException
from litestar.params import Parameter


class UserController(Controller):
    path = "/users"

    @get("/{user_id:int}")
    async def get_user_by_id(
        self,
        user_service: UserService,
        user_id: int = Parameter(gt=0, description="ID пользователя"),
    ) -> UserResponse:
        """Получить пользователя по ID"""
        user = await user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"Пользователь с ID {user_id} не найден")
        return UserResponse.model_validate(user)

    @get()
    async def get_all_users(
        self,
        user_service: UserService,
        count: int = Parameter(
            gt=0, le=100, default=10, description="Количество записей"
        ),
        page: int = Parameter(gt=0, default=1, description="Номер страницы"),
        name: Optional[str] = Parameter(None, description="Фильтр по имени"),
        email: Optional[str] = Parameter(None, description="Фильтр по email"),
    ) -> List[UserResponse]:
        """Получить список пользователей с пагинацией и фильтрацией"""
        filters = {}
        if name:
            filters["name"] = name
        if email:
            filters["email"] = email

        users = await user_service.get_by_filter(count=count, page=page, **filters)
        return [UserResponse.model_validate(user) for user in users]

    @post()
    async def create_user(
        self,
        user_service: UserService,
        data: UserCreate,
    ) -> UserResponse:
        """Создать нового пользователя"""
        user = await user_service.create(data)
        return UserResponse.model_validate(user)

    @delete("/{user_id:int}")
    async def delete_user(
        self,
        user_service: UserService,
        user_id: int = Parameter(gt=0, description="ID пользователя"),
    ) -> None:
        """Удалить пользователя"""
        deleted = await user_service.delete(user_id)
        if not deleted:
            raise NotFoundException(detail=f"Пользователь с ID {user_id} не найден")

    @put("/{user_id:int}")
    async def update_user(
        self,
        user_service: UserService,
        data: UserUpdate,  # ID будет в пути /users/{user_id}
    ) -> UserResponse:
        """Обновить пользователя"""
        # Получаем user_id из пути - Litestar сделает это автоматически
        # Но нам нужно передать его явно. Лучше использовать PATCH
        # Для PUT нужно передать ID в теле или использовать другой подход
        raise NotFoundException(
            detail="Используйте PATCH для обновления или передайте ID в теле"
        )
