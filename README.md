# app-dev

## установка и запуск

Установить зависимости: pip install -r requirements.txt
Запустить PostgreSQL в контейнере: docker compose up -d
Применить миграции: alembic upgrade head
Запустить приложение командой python -m app.main

## Тестирование

Запуск всех тестов: pytest
Запуск только unit-тестов: pytest tests/test_models/ tests/test_repositories/ tests/test_services/
Запуск только API-тестов: pytest tests/test_routes/
Запуск тестов с покрытием кода: pytest --cov=app --cov-report=html
Параллельный запуск тестов: pytest -n auto
