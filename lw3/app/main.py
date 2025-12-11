import os
from contextlib import asynccontextmanager

from app.controllers.user_controller import UserController
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from dotenv import load_dotenv
from litestar import Litestar
from litestar.di import Provide
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

# Загрузка переменных окружения
load_dotenv()

# Настройка базы данных
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost/postgres?client_encoding=utf8",
)

# Создаем асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True)
async_session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


@asynccontextmanager
async def lifespan(app: Litestar):
    """Контекст жизненного цикла приложения"""
    yield
    await engine.dispose()


async def provide_db_session() -> AsyncSession:
    """Провайдер сессии базы данных (асинхронный)"""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    """Провайдер репозитория пользователей"""
    return UserRepository(db_session)


async def provide_user_service(user_repository: UserRepository) -> UserService:
    """Провайдер сервиса пользователей"""
    return UserService(user_repository)


app = Litestar(
    route_handlers=[UserController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_repository": Provide(provide_user_repository),
        "user_service": Provide(provide_user_service),
    },
    lifespan=[lifespan],  # lifespan должен быть списком
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
