from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.repositories import SqlAlchemyUserRepository
from src.shared.database import get_db

from .schemas import Token
from .services import AuthService

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db)
):
    user_repo = SqlAlchemyUserRepository(session)
    auth_service = AuthService(user_repo)
    
    return await auth_service.authenticate_user(form_data.username, form_data.password)