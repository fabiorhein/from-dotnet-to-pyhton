import contextlib
from collections.abc import AsyncGenerator

from fastapi import FastAPI

from src.modules.users.api import router as users_router
from src.shared.database import Base, engine


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title="Agentic Core API", 
    lifespan=lifespan,
    description="Modular Monolith Backend"
)

app.include_router(users_router)