from fastapi import APIRouter, Depends


from backend.app.api.dependencies import get_auth_service
from backend.app.services.auth_service import AuthService
from backend.app.schemas.auth import LoginRequest, LoginResponse, RegisterResponse, RegisterRequest, RefreshResponse, RefreshRequest, LogoutRequest, LogoutResponse



router = APIRouter(prefix="/auth", tags=["Authentication",])

"Register"
@router.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)) -> RegisterResponse:
    return await auth_service.register(request)

"Login"
@router.post("/login",response_model=LoginResponse)
async def login(request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.login(email=request.email,password=request.password)

"Refresh"
@router.post("/refresh", response_model=RefreshResponse)
async def refresh(request: RefreshRequest, auth_service: AuthService = Depends(get_auth_service)) -> RefreshResponse:
    return await auth_service.refresh(request.refresh_token)

"Logout"
@router.post("/logout", response_model=LogoutResponse)
async def logout(request: LogoutRequest, auth_service: AuthService = Depends(get_auth_service)) -> LogoutResponse:
    return await auth_service.logout(request.refresh_token)