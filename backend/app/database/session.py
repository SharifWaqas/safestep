from backend.app.database import engine
from sqlalchemy.ext.asyncio import async_sessionmaker

db_engine = engine.engine
SessionFactory = async_sessionmaker(bind=db_engine,expire_on_commit=False)
