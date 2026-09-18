import uuid

from pydantic import BaseModel, ConfigDict, EmailStr


# Request
class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserUpdate(BaseModel):
    id: uuid.UUID
    name: str | None = None
    email: EmailStr | None = None

#Response
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    email: EmailStr

class UserResponseEntire(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    email: EmailStr
    is_active: bool
