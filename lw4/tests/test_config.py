# tests/test_config.py
import os

# Конфигурация для тестов
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["LITESTAR_DEBUG"] = "True"
