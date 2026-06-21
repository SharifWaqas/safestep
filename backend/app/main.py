from fastapi import FastAPI
from backend.app.database import engine
from sqlalchemy import text

db_engine = engine.engine
app = FastAPI()

@app.get("/Connection-test")
def Connectiontest():
    with db_engine.connect() as connection: 
        query = text("select 1")
        result = connection.execute(query)
        if result:
            return True
        else:
            return False

