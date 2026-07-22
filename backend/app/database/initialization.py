import asyncio

from backend.app.database.base import Base    
from backend.app.database.engine import engine
from backend.app.models.session import Session
from backend.app.models.user import User
from backend.app.models.upload import Upload

async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

asyncio.run(create_tables())
