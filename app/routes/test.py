# app/routes/test.py
from fastapi import APIRouter
from app.database import get_supabase

router = APIRouter()

@router.get("/test-connection")
async def test_connection():
    supabase = get_supabase()
    try:
        result = supabase.table('users').select('*').limit(1).execute()
        return {
            "status": "CONEXIÓN EXITOSA A SUPABASE",
            "data": result.data,
            "count": len(result.data)
        }
    except Exception as e:
        return {
            "status": "ERROR DE CONEXIÓN",
            "error": str(e)
        }