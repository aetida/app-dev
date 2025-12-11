import pytest
from unittest.mock import Mock, AsyncMock
import uuid
from app.services.user_service import UserService
from app.schemas import UserCreate, UserUpdate
from app.models import User


class TestUserServiceWithMock:
    """Тесты сервиса пользователей с мок-репозиторием"""

    @pytest.fixture
    def unique_email(self):
        return f"mock-test-{uuid.uuid4().hex[:8]}@example.com"

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, mock_user_repository: Mock, unique_email: str
    ):
        """Тест успешного получения пользователя по ID"""

        expected_user = User(
            id=1, name="Test User", email=unique_email, description="Test description"
        )
        mock_user_repository.get_by_id = AsyncMock(return_value=expected_user)

        service = UserService(mock_user_repository)
        user = await service.get_by_id(1)

        assert user is not None
        assert user.id == 1
        assert user.name == "Test User"
        mock_user_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_create_user_with_business_logic(self, mock_user_repository: Mock):
        """Тест создания пользователя с бизнес-логикой"""
        unique_email = f"create-test-{uuid.uuid4().hex[:8]}@example.com"

        user_create = UserCreate(
            name="Test User",
            email=unique_email,
            description=None,
        )

        created_user = User(
            id=1,
            name="Test User",
            email=unique_email,
            description="Пользователь Test User",
        )

        mock_user_repository.create = AsyncMock(return_value=created_user)

        service = UserService(mock_user_repository)
        user = await service.create(user_create)

        assert user is not None
        assert user.id == 1
        assert user.description == "Пользователь Test User"
        mock_user_repository.create.assert_called_once()


class TestUserServiceWithRealRepository:
    """Тесты сервиса пользователей с реальным репозиторием"""

    @pytest.mark.asyncio
    async def test_create_user_with_default_description(
        self, user_service: UserService
    ):
        """Тест создания пользователя с дефолтным описанием"""
        unique_email = f"default-desc-{uuid.uuid4().hex[:8]}@example.com"

        user_create = UserCreate(
            name="Test User",
            email=unique_email,
        )

        user = await user_service.create(user_create)

        assert user is not None
        assert user.description == "Пользователь Test User"

    @pytest.mark.asyncio
    async def test_create_user_with_custom_description(self, user_service: UserService):
        """Тест создания пользователя с указанным описанием"""
        unique_email = f"custom-desc-{uuid.uuid4().hex[:8]}@example.com"

        user_create = UserCreate(
            name="Test User", email=unique_email, description="Custom description"
        )

        user = await user_service.create(user_create)

        assert user is not None
        assert user.description == "Custom description"
