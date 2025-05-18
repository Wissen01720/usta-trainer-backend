from typing import Optional
from app.database import get_supabase
from app.schemas.user import UserOut, UserUpdate
from app.utils.exceptions import NotFoundException
from pydantic import ValidationError

class UserService:
    def __init__(self):
        self.supabase = get_supabase()
        
    async def get_user_by_id(self, user_id: str) -> UserOut:
        response = self.supabase.table("users").select("*").eq("id", user_id).single().execute()
        if not response.data:
            raise NotFoundException("Usuario no encontrado")
        try:
            return UserOut(**response.data)
        except ValidationError as e:
            raise ValueError(f"Error de validación: {str(e)}")
    
    async def update_user(self, user_id: str, user_data: UserUpdate) -> UserOut:
        update_data = user_data.model_dump(exclude_unset=True) if hasattr(user_data, "model_dump") else user_data.dict(exclude_unset=True)
        print("Datos a actualizar:", update_data)  # <-- Depuración
    
        response = self.supabase.table("users")\
            .update(update_data)\
            .eq("id", user_id)\
            .select("*")\
            .single()\
            .execute()
        print("Respuesta de supabase:", response.data)  # <-- Depuración
    
        if not response.data:
            raise NotFoundException("Usuario no encontrado o sin cambios")
        try:
            return UserOut(**response.data)
        except ValidationError as e:
            raise ValueError(f"Error de validación: {str(e)}")