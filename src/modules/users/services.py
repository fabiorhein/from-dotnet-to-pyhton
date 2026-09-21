import math
import uuid

from src.shared.schemas import PageResponse

from src.shared.uow import IUnitOfWork

from .models import User
from .repositories import IUserRepository
from .schemas import UserCreate, UserResponse, UserUpdate


class UserService:
    def __init__(self, user_repository: IUserRepository, uow: IUnitOfWork):
        self._user_repository = user_repository
        self._uow = uow

    async def register_user(self, dto: UserCreate) -> User:
        existing_user = await self._user_repository.get_by_email(dto.email)
        if existing_user:
            raise ValueError("E-mail já cadastrado no sistema.")

        new_user = User(name=dto.name, email=dto.email)
        await self._user_repository.add(new_user)
        
        try:
            await self._uow.commit()
            return new_user
        except Exception:
            await self._uow.rollback()
            raise

    # ---------------------------------------------------------
    #                   Read methods
    # ---------------------------------------------------------

    async def get_user_by_email(self, email: str) -> User:
        user = await self._user_repository.get_by_email(email)
        if not user:
            raise ValueError("Usuário não encontrado.")
        return user

    async def get_user_by_id(self, user_id: uuid.UUID) -> User:
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado.")
        return user

    async def get_all_users(self) -> list[User]:
        return await self._user_repository.get_all()

    async def get_all_users_without_inactive(self) -> list[User]:
        return await self._user_repository.get_all_without_inactive()

    async def get_paginated_users(self, page: int, size: int) -> PageResponse[UserResponse]:
        items, total_items = await self._user_repository.get_paginated(page=page, size=size)

        total_pages = math.ceil(total_items / size) if total_items > 0 else 0

        # Mapeia as entidades de domínio/ORM para os DTOs de resposta do Pydantic
        user_responses = [UserResponse.model_validate(user) for user in items]

        return PageResponse[UserResponse](
            items=user_responses,
            page=page,
            size=size,
            total_items=total_items,
            total_pages=total_pages,
        )

    # ---------------------------------------------------------
    #                   Write methods
    # ---------------------------------------------------------

    async def update_user(self, dto: UserUpdate) -> User:
        user = await self._user_repository.get_by_id(dto.id)
        if not user:
            raise ValueError("Usuário não encontrado.")

        if dto.name is not None:
            user.name = dto.name
        if dto.email is not None:
            user.email = dto.email
            
        updated_user = await self._user_repository.update(user)
        
        try:
            await self._uow.commit()
            return updated_user
        except Exception:
            await self._uow.rollback()
            raise

    async def deactivate_user(self, user_id: uuid.UUID) -> User:
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado.")

        user.deactivate()
        updated_user = await self._user_repository.update(user)
        
        try:
            await self._uow.commit()
            return updated_user
        except Exception:
            await self._uow.rollback()
            raise

    async def activate_user(self, user_id: uuid.UUID) -> User:
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado.")

        user.activate()
        updated_user = await self._user_repository.update(user)

        try:
            await self._uow.commit()
            return updated_user
        except Exception:
            await self._uow.rollback()
            raise
