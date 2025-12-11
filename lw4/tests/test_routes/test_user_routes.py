import pytest
import sys
import os

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from litestar.testing import TestClient
from sqlalchemy.ext.asyncio import create_async_engine
from app.models import Base


class TestUserRoutes:
    """Tests for user API endpoints"""

    @pytest.fixture(autouse=True)
    async def setup_database(self):
        """Создание таблиц перед всеми тестами класса"""
        from app.main import engine

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        yield
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @pytest.fixture
    def test_client(self):
        """Fixture for TestClient"""
        from app.main import app

        return TestClient(app=app)

    def test_create_user_success(self, test_client: TestClient):
        """Test successful user creation via API"""
        user_data = {
            "name": "API Test User",
            "email": "api-test@example.com",
            "description": "Created via API test",
        }

        response = test_client.post("/users", json=user_data)

        print(f"\nCREATE USER RESPONSE:")
        print(f"  Status: {response.status_code}")
        print(f"  Body: {response.text}")

        assert response.status_code in [
            200,
            201,
        ], f"Expected 200/201, got {response.status_code}: {response.text}"

        data = response.json()
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]
        assert "id" in data

    def test_get_all_users(self, test_client: TestClient):
        """Test get all users"""
        # Создаем пользователя
        create_response = test_client.post(
            "/users",
            json={"name": "Test User for List", "email": "list-test@example.com"},
        )

        assert create_response.status_code in [
            200,
            201,
        ], f"Create failed: {create_response.text}"

        # Теперь получаем всех пользователей
        response = test_client.get("/users")

        print(f"\nGET ALL USERS RESPONSE:")
        print(f"  Status: {response.status_code}")
        print(f"  Body: {response.text}")

        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text}"

        users = response.json()
        assert isinstance(users, list)
        # Проверяем, что есть хотя бы один пользователь
        assert len(users) >= 1, f"Expected at least 1 user, got {len(users)}"

    def test_get_user_by_id_not_found(self, test_client: TestClient):
        """Test get non-existent user"""
        response = test_client.get("/users/999999")

        print(f"\nGET NON-EXISTENT USER RESPONSE:")
        print(f"  Status: {response.status_code}")

        assert (
            response.status_code == 404
        ), f"Expected 404, got {response.status_code}: {response.text}"

    def test_get_user_by_id_success(self, test_client: TestClient):
        """Test successful get user by ID"""
        # Сначала создаем пользователя и сохраняем его ID
        create_response = test_client.post(
            "/users",
            json={"name": "Get By ID Test", "email": "getbyid-test@example.com"},
        )

        print(f"\nCREATE FOR GET BY ID:")
        print(f"  Status: {create_response.status_code}")
        print(f"  Body: {create_response.text}")

        assert create_response.status_code in [
            200,
            201,
        ], f"Create failed: {create_response.text}"
        user_id = create_response.json()["id"]

        print(f"Created user with ID: {user_id}")

        # Ждем немного (для асинхронных операций)
        import time

        time.sleep(0.1)

        # Теперь получаем пользователя
        response = test_client.get(f"/users/{user_id}")

        print(f"\nGET USER BY ID RESPONSE:")
        print(f"  Status: {response.status_code}")
        print(f"  Body: {response.text}")

        if response.status_code != 200:
            print(f"ERROR: {response.json()}")

        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text}"

        data = response.json()
        assert data["id"] == user_id
        assert data["name"] == "Get By ID Test"
        assert data["email"] == "getbyid-test@example.com"

    def test_update_user_success(self, test_client: TestClient):
        """Test successful user update"""
        # Создаем пользователя
        create_response = test_client.post(
            "/users",
            json={"name": "Update Test User", "email": "update-test@example.com"},
        )

        assert create_response.status_code in [
            200,
            201,
        ], f"Create failed: {create_response.text}"
        user_id = create_response.json()["id"]

        print(f"Created user with ID: {user_id}")

        # Ждем
        import time

        time.sleep(0.1)

        # Обновляем пользователя
        update_data = {"name": "Updated Name", "description": "Updated description"}

        response = test_client.patch(f"/users/{user_id}", json=update_data)

        print(f"\nUPDATE USER RESPONSE:")
        print(f"  Status: {response.status_code}")
        print(f"  Body: {response.text}")

        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text}"

        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["description"] == "Updated description"
        assert data["email"] == "update-test@example.com"  # Email не менялся

    def test_delete_user_success(self, test_client: TestClient):
        """Test successful user deletion"""
        # Создаем пользователя
        create_response = test_client.post(
            "/users",
            json={"name": "Delete Test User", "email": "delete-test@example.com"},
        )

        assert create_response.status_code in [
            200,
            201,
        ], f"Create failed: {create_response.text}"
        user_id = create_response.json()["id"]

        print(f"Created user with ID: {user_id}")

        # Ждем
        import time

        time.sleep(0.1)

        # Удаляем пользователя
        response = test_client.delete(f"/users/{user_id}")

        print(f"\nDELETE USER RESPONSE:")
        print(f"  Status: {response.status_code}")
        print(f"  Body: {response.text}")

        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text}"

        # Проверяем, что пользователь удален
        get_response = test_client.get(f"/users/{user_id}")
        assert (
            get_response.status_code == 404
        ), f"Expected 404 after delete, got {get_response.status_code}: {get_response.text}"
