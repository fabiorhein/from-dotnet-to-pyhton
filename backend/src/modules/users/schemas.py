# src/modules/users/schemas.py
import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Request
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=6, description="User password (at least 6 characters).")


class UserUpdate(BaseModel):
    id: uuid.UUID
    name: str | None = None
    email: EmailStr | None = None


# Response
class UserResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserResponseEntire(UserResponse):
    pass