import contextlib
from collections.abc import AsyncGenerator
from fastapi import FastAPI
from src.shared.database import engine, Base
from src.modules.users.api import router as users_router

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