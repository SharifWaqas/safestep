from backend.app.database import engine
from sqlalchemy.orm import sessionmaker

db_engine = engine.engine
Sessionfactory = sessionmaker(bind=db_engine)
