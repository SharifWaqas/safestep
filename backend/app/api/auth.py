from fastapi import APIRouter, Depends


from backend.app.api.dependencies import get_auth_service
from backend.app.services.auth_service import AuthService
from backend.app.schemas.auth import LoginRequest, LoginResponse, RegisterResponse, RegisterRequest



router = APIRouter(prefix="/auth", tags=["Authentication",])

@router.post("/login",response_model=LoginResponse)
async def login(request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.login(email=request.email,password=request.password)


@router.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)) -> RegisterResponse:
    return await auth_service.register(request)