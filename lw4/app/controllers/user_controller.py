from typing import List, Optional
from litestar import Controller, get, post, patch, delete
from litestar.params import Parameter
from litestar.exceptions import NotFoundException, ValidationException
from litestar.status_codes import HTTP_200_OK
from app.services.user_service import UserService
from app.schemas import UserCreate, UserUpdate, UserResponse


class UserController(Controller):
    path = "/users"

    @get("/{user_id:int}")
    async def get_user_by_id(
        self,
        user_service: UserService,
        user_id: int = Parameter(gt=0, description="User ID"),
    ) -> UserResponse:
        """Get user by ID"""
        user = await user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)

    @get()
    async def get_all_users(
        self,
        user_service: UserService,
        count: int = Parameter(
            gt=0, le=100, default=10, description="Number of records"
        ),
        page: int = Parameter(gt=0, default=1, description="Page number"),
    ) -> List[UserResponse]:
        """Get list of users with pagination"""
        users = await user_service.get_by_filter(count=count, page=page)
        return [UserResponse.model_validate(user) for user in users]

    @post()
    async def create_user(
        self,
        user_service: UserService,
        data: UserCreate,
    ) -> UserResponse:
        """Create new user"""
        try:
            user = await user_service.create(data)
            return UserResponse.model_validate(user)
        except Exception as e:
            if "unique constraint" in str(e).lower() or "duplicate" in str(e).lower():
                raise ValidationException(
                    detail=f"User with email {data.email} already exists"
                )
            raise

    @delete("/{user_id:int}", status_code=HTTP_200_OK)  # Явно указываем статус код 200
    async def delete_user(
        self,
        user_service: UserService,
        user_id: int = Parameter(gt=0, description="User ID"),
    ) -> dict:
        """Delete user"""
        deleted = await user_service.delete(user_id)
        if not deleted:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return {"message": f"User with ID {user_id} deleted successfully"}

    @patch("/{user_id:int}")
    async def update_user(
        self,
        user_service: UserService,
        user_id: int,  # Без Parameter() - получается из пути
        data: UserUpdate,  # Из тела запроса
    ) -> UserResponse:
        """Update user (partial update)"""
        user = await user_service.update(user_id, data)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)
