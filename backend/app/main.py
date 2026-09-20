from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.auth import router as auth_router
from backend.app.api.upload import router as upload_router
from backend.app.api.analysis import router as analysis_router
from backend.app.core.config import settings
from backend.app.core.exception_handlers import register_exception_handlers


app = FastAPI()

cors_origins = [
    origin.strip()
    for origin in settings.CORS_ORIGINS.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(analysis_router)