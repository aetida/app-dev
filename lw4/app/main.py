import logging
import os
from contextlib import asynccontextmanager

from app.controllers.user_controller import UserController
from app.models import Base
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from dotenv import load_dotenv
from litestar import Litestar, Request, Response
from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

# Настройка логирования
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

# Настройка базы данных
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

# Создаем асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=False)
async_session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


@asynccontextmanager
async def lifespan(app: Litestar):
    """Контекст жизненного цикла приложения"""
    # Создаем таблицы при запуске
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


async def provide_db_session() -> AsyncSession:
    """Провайдер сессии базы данных - БЕЗ автоматического коммита"""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()  # Просто закрываем сессию, коммит делается в обработчиках


async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    """Провайдер репозитория пользователей"""
    return UserRepository(db_session)


async def provide_user_service(user_repository: UserRepository) -> UserService:
    """Провайдер сервиса пользователей"""
    return UserService(user_repository)


def handle_exception(request: Request, exc: Exception) -> Response:
    """Глобальный обработчик исключений"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    if isinstance(exc, HTTPException):
        return Response(
            content={"detail": exc.detail},
            status_code=exc.status_code,
        )

    return Response(
        content={
            "detail": "Internal Server Error",
            "error": str(exc),
            "type": exc.__class__.__name__,
        },
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )


app = Litestar(
    route_handlers=[UserController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_repository": Provide(provide_user_repository),
        "user_service": Provide(provide_user_service),
    },
    lifespan=[lifespan],
    exception_handlers={
        Exception: handle_exception,
    },
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
