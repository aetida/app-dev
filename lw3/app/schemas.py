from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(...)
    description: Optional[str] = Field(None, max_length=500)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    description: Optional[str] = Field(None, max_length=500)


# Упрощенный UserResponse - БЕЗ addresses для начала
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    description: Optional[str]

    # Убираем addresses или делаем Optional с дефолтным значением
    # addresses: Optional[List[dict]] = Field(default_factory=list)

    class Config:
        from_attributes = True


# Отдельная схема для полного пользователя с адресами
class UserWithAddressesResponse(UserResponse):
    addresses: List[dict] = Field(default_factory=list)
