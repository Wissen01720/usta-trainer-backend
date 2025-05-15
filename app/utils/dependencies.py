from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.schemas.user import UserOut, TokenData
from app.utils.security import decode_token
from app.database import get_supabase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token_data = decode_token(token)
        if token_data is None or token_data.id is None:
            raise credentials_exception
            
        supabase = get_supabase()
        response = supabase.table("users").select("*").eq("id", token_data.id).single().execute()
        
        if not response.data:
            raise credentials_exception
            
        return response.data
    except Exception:
        raise credentials_exception