import uuid

from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    def deactivate(self) -> None:
        """Regra de negócio: Um usuário desativado perde acessos e validações"""
        if not self.is_active:
            raise ValueError("O usuário já está inativo.")
        self.is_active = False

    def activate(self) -> None:
        """Regra de negócio: Um usuário ativado recupera acessos e validações"""
        if self.is_active:
            raise ValueError("O usuário já está ativo.")
        self.is_active = True