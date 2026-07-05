import pytest

from backend.app.services.jwt_service import JWTService
from backend.app.services.exceptions import TokenVerificationError

def test_create_access_token_returns_valid_jwt():

    jwt_service = JWTService()
    user_id = "ABC123"
    token_type = "access"
    
    token = jwt_service.create_access_token(user_id)
    result =  jwt_service.verify_token(token)
    
    assert result["sub"] == user_id  
    assert result["type"] == token_type

def test_create_refresh_token_returns_valid_jwt():
    
    jwt_service = JWTService()
    user_id = "ABC123"
    token_type = "refresh"
    
    token = jwt_service.create_refresh_token(user_id)
    result =  jwt_service.verify_token(token)
    
    assert result["sub"] == user_id  
    assert result["type"] == token_type



def test_verify_token_raises_token_verification_error_for_invalid_token():
    
    jwt_service = JWTService()
    token = "not-a-jwt"
    
    with pytest.raises(TokenVerificationError):
        jwt_service.verify_token(token)
