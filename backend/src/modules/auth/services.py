from fastapi import HTTPException, status

from src.modules.users.repositories import IUserRepository
from src.shared.security import create_access_token, verify_password


class AuthService:
    def __init__(self, user_repo: IUserRepository):
        self._user_repo = user_repo

    async def authenticate_user(self, email: str, password: str) -> dict:
        user = await self._user_repo.get_by_email(email)
        
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Usuário inativo.")

        access_token = create_access_token(data={"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}