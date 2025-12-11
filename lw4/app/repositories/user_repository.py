# app/repositories/user_repository.py
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.models import User
from app.schemas import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID"""
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_filter(
        self, count: int = 10, page: int = 1, **kwargs
    ) -> List[User]:
        """Получить пользователей с фильтрацией и пагинацией"""
        query = select(User)

        # Применяем фильтры
        for key, value in kwargs.items():
            if hasattr(User, key):
                if isinstance(value, (list, tuple)):
                    query = query.where(getattr(User, key).in_(value))
                else:
                    query = query.where(getattr(User, key) == value)

        # Пагинация
        offset = (page - 1) * count
        query = query.offset(offset).limit(count)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, user_data: UserCreate) -> User:
        """Создать нового пользователя"""
        user = User(**user_data.model_dump())
        self.session.add(user)
        await self.session.commit()  # Комитим сразу
        await self.session.refresh(user)  # Обновляем объект
        return user

    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Обновить пользователя"""
        # Получаем пользователя
        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            return None

        # Обновляем только переданные поля
        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        await self.session.commit()  # Комитим
        await self.session.refresh(user)  # Обновляем
        return user

    async def delete(self, user_id: int) -> bool:
        """Удалить пользователя"""
        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if user:
            await self.session.delete(user)
            await self.session.commit()  # Комитим
            return True
        return False
