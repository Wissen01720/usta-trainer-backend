import os
from supabase import create_client, Client
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

class SupabaseClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            # Verificar que las variables de entorno estén configuradas
            if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"):
                raise HTTPException(
                    status_code=500,
                    detail="Configuración de Supabase no encontrada"
                )
                
            cls._instance = super().__new__(cls)
            cls._instance.url = os.getenv("SUPABASE_URL")
            cls._instance.key = os.getenv("SUPABASE_KEY")
            cls._instance.client = create_client(cls._instance.url, cls._instance.key)
            
            # Verificar conexión
            try:
                cls._instance.client.table('users').select('*').limit(1).execute()
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error conectando a Supabase: {str(e)}"
                )
        return cls._instance

def get_supabase() -> Client:
    return SupabaseClient().client