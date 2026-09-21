import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from pydantic import EmailStr

from mcp.server.fastmcp import FastMCP
from modules.users.repositories import SqlAlchemyUserRepository
from modules.users.schemas import UserCreate
from modules.users.services import UserService
from shared.database import AsyncSessionLocal
from shared.uow import SQLAlchemyUnitOfWork

# Instancia o servidor MCP usando FastMCP
mcp = FastMCP("FromDotNetToPython-Users")


async def _get_user_service_context(session):
    repository = SqlAlchemyUserRepository(session)
    uow = SQLAlchemyUnitOfWork(session)
    return UserService(user_repository=repository, uow=uow)


# =====================================================================
# MCP TOOLS
# =====================================================================

@mcp.tool()
async def list_users(page: int = 1, size: int = 10) -> str:
    """Consulta a lista paginada de usuários cadastrados no sistema.
    
    Args:
        page: Número da página (inicia em 1)
        size: Quantidade de itens por página
    """
    async with AsyncSessionLocal() as session:
        service = await _get_user_service_context(session)
        result = await service.get_paginated_users(page=page, size=size)
        return result.model_dump_json(indent=2)


@mcp.tool()
async def find_user_by_email(email: str) -> str:
    """Busca um usuário específico no banco de dados utilizando o e-mail cadastrado.
    
    Args:
        email: Endereço de e-mail exato do usuário
    """
    async with AsyncSessionLocal() as session:
        service = await _get_user_service_context(session)
        try:
            user = await service.get_user_by_email(email)
            return f"Usuário Encontrado: ID={user.id}, Nome={user.name}, Email={user.email}, Ativo={user.is_active}"
        except ValueError as e:
            return f"Erro na busca: {str(e)}"


@mcp.tool()
async def register_new_user(name: str, email: str) -> str:
    """Cadastra um novo usuário no sistema aplicando todas as validações de domínio.
    
    Args:
        name: Nome completo do novo usuário
        email: E-mail único e válido do usuário
    """
    async with AsyncSessionLocal() as session:
        service = await _get_user_service_context(session)
        try:
            dto = UserCreate(name=name, email=email)
            new_user = await service.register_user(dto)
            return f"Usuário cadastrado com sucesso! ID: {new_user.id}"
        except ValueError as e:
            return f"Falha no cadastro (Regra de Negócio): {str(e)}"
        except Exception as e:
            return f"Erro ao registrar usuário: {str(e)}"


if __name__ == "__main__":
    mcp.run()