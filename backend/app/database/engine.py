from sqlalchemy.ext.asyncio import create_async_engine
from backend.app.core.config import settings

db_url = (
    f"postgresql+asyncpg://"
    f"{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}"
    f"/{settings.DB_NAME}"
)

engine = create_async_engine(db_url)