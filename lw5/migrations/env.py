import asyncio
import os
from logging.config import fileConfig

from alembic import context
# Импорт моделей
from app.models import Base
from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

# Загрузка Alembic-конфигурации
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Мета-данные моделей
target_metadata = Base.metadata

# Загрузка переменных окружения
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def run_migrations_online() -> None:
    """Запуск миграций в асинхронном режиме."""

    connectable = create_async_engine(
        DATABASE_URL,
        echo=False,
        poolclass=pool.NullPool,
    )

    async def do_run_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(run_migrations_sync)

    asyncio.run(do_run_migrations())


def run_migrations_sync(connection):
    """Синхронная функция для Alembic."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    # При необходимости можно добавить offline-режим
    raise NotImplementedError("Offline migrations not implemented")
else:
    run_migrations_online()
