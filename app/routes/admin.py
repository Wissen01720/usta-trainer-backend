from fastapi import APIRouter, Depends
from app.database import get_supabase
from app.utils.dependencies import get_current_admin

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/")
async def admin_dashboard(current_user=Depends(get_current_admin)):
    return {"message": f"Admin dashboard for {current_user['email']}"}