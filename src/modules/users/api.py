import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.database import get_db
from src.shared.schemas import PageParams, PageResponse
from src.shared.uow import SQLAlchemyUnitOfWork

from .repositories import SqlAlchemyUserRepository
from .schemas import UserCreate, UserResponse, UserResponseEntire, UserUpdate
from .services import UserService

router = APIRouter(prefix="/api/users", tags=["Users"])


# A função está definida logo abaixo no próprio arquivo:
async def get_user_service(session: AsyncSession = Depends(get_db)) -> UserService:
    repository = SqlAlchemyUserRepository(session)
    uow = SQLAlchemyUnitOfWork(session)
    return UserService(user_repository=repository, uow=uow)

@router.post("", response_model=UserResponse, status_code=201)
async def create_user_endpoint(
    request: UserCreate, 
    service: UserService = Depends(get_user_service)
) -> UserResponse:
    try:
        user = await service.register_user(request)
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/by-email", response_model=UserResponse)
async def get_user_by_email_endpoint(
    email: str, service: UserService = Depends(get_user_service)
) -> UserResponse:
    try:
        user = await service.get_user_by_email(email)
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# GET /api/users?page=1&size=10
@router.get("", response_model=PageResponse[UserResponse])
async def list_users_paginated(
    page: int = Query(default=1, ge=1, description="Número da página"),
    size: int = Query(default=10, ge=1, le=100, description="Tamanho da página"),
    service: UserService = Depends(get_user_service),
) -> PageResponse[UserResponse]:
    return await service.get_paginated_users(page=page, size=size)

@router.get("/all", response_model=list[UserResponseEntire])
async def get_all_users_endpoint(
    service: UserService = Depends(get_user_service)
) -> list[UserResponseEntire]:
    users = await service.get_all_users()
    return [UserResponseEntire.model_validate(user) for user in users]

@router.get("/all/without-inactive", response_model=list[UserResponse])
async def get_all_users_without_inactive_endpoint(
    service: UserService = Depends(get_user_service)
) -> list[UserResponse]:
    users = await service.get_all_users_without_inactive()
    return [UserResponse.model_validate(user) for user in users]

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id_endpoint(
    user_id: uuid.UUID,
    service: UserService = Depends(get_user_service)
) -> UserResponse:
    # AQUI: Adicionado o tratamento de erro para retornar 404 em vez de 500
    try:
        user = await service.get_user_by_id(user_id)
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("", response_model=UserResponse)
async def update_user_endpoint(
    request: UserUpdate,
    service: UserService = Depends(get_user_service)
) -> UserResponse:
    try:
        user = await service.update_user(request)
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{user_id}", response_model=UserResponse)
async def deactivate_user_endpoint(
    user_id: uuid.UUID,
    service: UserService = Depends(get_user_service)
) -> UserResponse:
    try:
        user = await service.deactivate_user(user_id)
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{user_id}", response_model=UserResponse)
async def activate_user_endpoint(
    user_id: uuid.UUID,
    service: UserService = Depends(get_user_service)
) -> UserResponse:
    try:
        user = await service.activate_user(user_id)
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))