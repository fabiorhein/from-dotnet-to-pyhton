import uuid

from src.shared.uow import IUnitOfWork

from .models import User
from .repositories import IUserRepository
from .schemas import UserCreate, UserUpdate


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
