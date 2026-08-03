from fastapi import FastAPI
from backend.app.api.auth import router as auth_router
from backend.app.api.upload import router as upload_router
from backend.app.api.analysis import router as analysis_router
from backend.app.core.exception_handlers import register_exception_handlers

app = FastAPI()

register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(analysis_router)


