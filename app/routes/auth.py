from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.schemas.user import UserCreate, UserOut
from app.services.auth_service import AuthService
from app.utils.exceptions import AuthException

router = APIRouter(prefix="/auth", tags=["auth"])

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, service: AuthService = Depends(AuthService)):
    try:
        return await service.register_user(user_data)
    except AuthException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        # Para ver errores de validación y evitar error 500 sin CORS
        print("ERROR EN REGISTRO:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno en el registro")

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(AuthService)):
    try:
        user = await service.authenticate_user(form_data.username, form_data.password)
        from app.utils.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
        from datetime import timedelta
        access_token = create_access_token(
            data={"sub": user.id, "email": user.email, "role": user.role},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
    except AuthException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        print("ERROR EN LOGIN:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno en el login")