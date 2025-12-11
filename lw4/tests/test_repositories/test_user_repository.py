import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate, UserUpdate
from app.models import User
import uuid


class TestUserRepository:
    """Тесты для репозитория пользователей"""

    @pytest.fixture
    def unique_email(self):
        """Генератор уникальных email для тестов"""
        return f"test-{uuid.uuid4().hex[:8]}@example.com"

    @pytest.fixture
    def user_data(self, unique_email):
        """Тестовые данные пользователя с уникальным email"""
        return {
            "name": "Test User",
            "email": unique_email,
            "description": "Test description",
        }

    @pytest.mark.asyncio
    async def test_create_user(self, test_session: AsyncSession, user_data: dict):
        """Тест создания пользователя"""
        repository = UserRepository(test_session)
        user_create = UserCreate(**user_data)

        user = await repository.create(user_create)

        assert user.id is not None
        assert user.name == user_data["name"]
        assert user.email == user_data["email"]
        assert user.description == user_data["description"]

    @pytest.mark.asyncio
    async def test_get_by_id(self, test_session: AsyncSession, user_data: dict):
        """Тест получения пользователя по ID"""
        repository = UserRepository(test_session)
        user_create = UserCreate(**user_data)

        created_user = await repository.create(user_create)

        retrieved_user = await repository.get_by_id(created_user.id)

        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.name == user_data["name"]
        assert retrieved_user.email == user_data["email"]

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, test_session: AsyncSession):
        """Тест получения несуществующего пользователя"""
        repository = UserRepository(test_session)

        user = await repository.get_by_id(999)

        assert user is None

    @pytest.mark.asyncio
    async def test_get_by_filter(self, test_session: AsyncSession):
        """Тест получения пользователей с фильтрацией"""
        repository = UserRepository(test_session)

        users_data = [
            {
                "name": "User 1",
                "email": f"user1-{uuid.uuid4().hex[:8]}@example.com",
                "description": "Desc 1",
            },
            {
                "name": "User 2",
                "email": f"user2-{uuid.uuid4().hex[:8]}@example.com",
                "description": "Desc 2",
            },
            {
                "name": "User 3",
                "email": f"user3-{uuid.uuid4().hex[:8]}@example.com",
                "description": "Desc 3",
            },
        ]

        for data in users_data:
            await repository.create(UserCreate(**data))

        users = await repository.get_by_filter(count=2, page=1)

        assert len(users) == 2

        filtered_users = await repository.get_by_filter(name="User 1")

        assert len(filtered_users) <= 1
        if filtered_users:
            assert filtered_users[0].name == "User 1"

    @pytest.mark.asyncio
    async def test_update_user(self, test_session: AsyncSession):
        """Тест обновления пользователя"""
        repository = UserRepository(test_session)

        unique_email = f"update-test-{uuid.uuid4().hex[:8]}@example.com"
        user_create = UserCreate(
            name="Original Name", email=unique_email, description="Original description"
        )

        created_user = await repository.create(user_create)

        new_email = f"updated-{uuid.uuid4().hex[:8]}@example.com"
        update_data = UserUpdate(
            name="Updated Name", email=new_email, description="Updated description"
        )

        updated_user = await repository.update(created_user.id, update_data)

        assert updated_user is not None
        assert updated_user.name == "Updated Name"
        assert updated_user.email == new_email
        assert updated_user.description == "Updated description"

    @pytest.mark.asyncio
    async def test_update_user_not_found(self, test_session: AsyncSession):
        """Тест обновления несуществующего пользователя"""
        repository = UserRepository(test_session)
        update_data = UserUpdate(name="Updated Name")

        updated_user = await repository.update(999, update_data)

        assert updated_user is None

    @pytest.mark.asyncio
    async def test_delete_user(self, test_session: AsyncSession):
        """Тест удаления пользователя"""
        repository = UserRepository(test_session)

        unique_email = f"delete-test-{uuid.uuid4().hex[:8]}@example.com"
        user_create = UserCreate(
            name="User to Delete", email=unique_email, description="Will be deleted"
        )

        created_user = await repository.create(user_create)

        # Удаляем пользователя
        deleted = await repository.delete(created_user.id)

        assert deleted is True

        # Проверяем, что пользователь удален
        user_after_delete = await repository.get_by_id(created_user.id)
        assert user_after_delete is None

    @pytest.mark.asyncio
    async def test_delete_user_not_found(self, test_session: AsyncSession):
        """Тест удаления несуществующего пользователя"""
        repository = UserRepository(test_session)

        deleted = await repository.delete(999)

        assert deleted is False
