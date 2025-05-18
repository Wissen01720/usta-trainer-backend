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
        print("Datos a actualizar:", update_data)
        print("User ID:", user_id)
    
        response = self.supabase.table("users")\
            .update(update_data)\
            .eq("id", user_id)\
            .execute()
        print("Respuesta de supabase:", response.data)
    
        if not response.data:
            print("No se encontró el usuario o no hubo cambios.")
            raise NotFoundException("Usuario no encontrado o sin cambios")
        try:
            # Supabase retorna una lista de dicts en data después de update
            return UserOut(**response.data[0])
        except ValidationError as e:
            print("Error de validación:", str(e))
            raise ValueError(f"Error de validación: {str(e)}")
        
    async def list_users(self) -> list[UserOut]:
        response = self.supabase.table("users").select("*").execute()
        return [UserOut(**user) for user in response.data or []]
    
    async def delete_user(self, user_id: str):
        response = self.supabase.table("users").delete().eq("id", user_id).execute()
        if not response.data:
            raise NotFoundException("Usuario no encontrado")