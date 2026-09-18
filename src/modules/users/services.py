import uuid

from .models import User
from .repositories import IUserRepository
from .schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    async def register_user(self, dto: UserCreate) -> User:
        existing_user = await self._user_repository.get_by_email(dto.email)
        if existing_user:
            raise ValueError("E-mail já cadastrado no sistema.")

        new_user = User(name=dto.name, email=dto.email)
        await self._user_repository.add(new_user)
        
        return new_user

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
        users = await self._user_repository.get_all()
        return users

    async def get_all_users_without_inactive(self) -> list[User]:
        users = await self._user_repository.get_all_without_inactive()
        return users

    async def update_user(self, dto: UserUpdate) -> User:
        user = await self._user_repository.get_by_id(dto.id)
        if not user:
            raise ValueError("Usuário não encontrado.")

        if dto.name is not None:
            user.name = dto.name
        if dto.email is not None:
            user.email = dto.email
        updated_user = await self._user_repository.update(user)
        
        return updated_user

    async def deactivate_user(self, user_id: uuid.UUID) -> User:
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado.")

        user.deactivate()
        updated_user = await self._user_repository.update(user)
        
        return updated_user

    async def activate_user(self, user_id: uuid.UUID) -> User:
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado.")

        user.activate()
        updated_user = await self._user_repository.update(user)

        return updated_user
