from typing import List, Optional

from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID"""
        return await self.user_repository.get_by_id(user_id)

    async def get_by_filter(
        self, count: int = 10, page: int = 1, **kwargs
    ) -> List[User]:
        """Получить пользователей с фильтрацией"""
        return await self.user_repository.get_by_filter(count, page, **kwargs)

    async def create(self, user_data: UserCreate) -> User:
        """Создать пользователя с бизнес-логикой"""
        # Пример бизнес-логики
        if not user_data.description:
            user_data.description = f"Пользователь {user_data.name}"

        return await self.user_repository.create(user_data)

    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Обновить пользователя"""
        return await self.user_repository.update(user_id, user_data)

    async def delete(self, user_id: int) -> bool:
        """Удалить пользователя"""
        return await self.user_repository.delete(user_id)
