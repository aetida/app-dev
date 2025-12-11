import pytest
import asyncio
from typing import AsyncGenerator, Generator
from unittest.mock import Mock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import text

from app.models import Base
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
import uuid


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Fixture for test database engine"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest.fixture
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Fixture for test database session with cleanup"""
    async_session = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )

    async with async_session() as session:
        try:
            yield session
        finally:

            for table in reversed(Base.metadata.sorted_tables):
                await session.execute(table.delete())
            await session.commit()
            await session.close()


@pytest.fixture
async def clean_db(test_session: AsyncSession):
    """Clean database - уже встроено в test_session"""
    yield


@pytest.fixture
def user_repository(test_session: AsyncSession) -> UserRepository:
    """Fixture for user repository"""
    return UserRepository(test_session)


@pytest.fixture
def mock_user_repository() -> Mock:
    """Mock fixture for user repository"""
    return Mock(spec=UserRepository)


@pytest.fixture
def user_service(user_repository: UserRepository) -> UserService:
    """Fixture for user service with real repository"""
    return UserService(user_repository)


@pytest.fixture
def mock_user_service(mock_user_repository: Mock) -> UserService:
    """Fixture for user service with mock repository"""
    return UserService(mock_user_repository)


@pytest.fixture
def user_data_factory():
    """Factory for test user data"""

    def _factory(**kwargs):
        base_data = {
            "name": f"Test User {uuid.uuid4().hex[:8]}",
            "email": f"test-{uuid.uuid4().hex[:8]}@example.com",
            "description": "Test description",
        }
        base_data.update(kwargs)
        return base_data

    return _factory


@pytest.fixture
def user_data(user_data_factory):
    """Test user data with unique email"""
    return user_data_factory()
