from backend.app.database.base import Base    
from backend.app.database.engine import engine
from backend.app.models.session import Session
from backend.app.models.user import User
from backend.app.models.upload import Upload

def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()