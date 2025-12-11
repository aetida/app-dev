from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime


# Схемы для создания
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(...)
    description: Optional[str] = Field(None, max_length=500)


# Схемы для обновления (ИСПРАВЛЕННЫЙ)
class UserUpdate(BaseModel):
    # ВСЕ поля должны быть Optional с значениями по умолчанию
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    description: Optional[str] = Field(None, max_length=500)


# Схемы для ответов
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    description: Optional[str]
    created_at: Optional[datetime] = None


class AddressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    street: str
    city: str
    postal_code: str
    user_id: int


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float
    description: Optional[str]
    stock_quantity: int
    created_at: Optional[datetime] = None


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    address_id: int
    total_amount: float
    status: str
    created_at: Optional[datetime] = None
