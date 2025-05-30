from datetime import timedelta
from app.database import get_supabase
from app.schemas.user import UserCreate, UserOut
from app.utils.security import (
    verify_password,
    get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.utils.exceptions import AuthException
from pydantic import ValidationError

class AuthService:
    def __init__(self):
        self.supabase = get_supabase()

    async def register_user(self, user_data: UserCreate) -> UserOut:
        # Verificar si el email ya existe
        existing_user = self.supabase.table("users")\
            .select("*")\
            .eq("email", user_data.email)\
            .execute()
        
        if existing_user.data:
            raise AuthException("El email ya está registrado")
        
        # Hashear la contraseña antes de guardar
        hashed_password = get_password_hash(user_data.password)
        
        # Crear perfil en la tabla users
        user_profile = {
            "email": user_data.email,
            "password_hash": hashed_password,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "role": user_data.role.value,
            "status": "active",
        }
        
        response = self.supabase.table("users").insert(user_profile).execute()
        
        if not response.data:
            raise AuthException("Error al crear perfil de usuario")
        
        try:
            return UserOut(**response.data[0])
        except ValidationError as e:
            raise ValueError(f"Error de validación: {str(e)}")
    
    async def authenticate_user(self, email: str, password: str) -> UserOut:
        try:
            # Busca el usuario por email
            user_row = self.supabase.table("users").select("*").eq("email", email).single().execute()
            user = user_row.data
            if not user or not verify_password(password, user["password_hash"]):
                raise AuthException("Credenciales inválidas")
            return UserOut(**user)
        except Exception as e:
            raise AuthException(f"Error en autenticación: {str(e)}")