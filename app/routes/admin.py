from fastapi import APIRouter, Depends
from app.database import get_supabase
from app.utils.dependencies import get_current_admin

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/")
async def admin_dashboard(current_user=Depends(get_current_admin)):
    return {"message": f"Admin dashboard for {current_user['email']}"}

@router.get("/user-stats")
async def user_stats(current_user = Depends(get_current_admin)):
    supabase = get_supabase()
    response = supabase.table("users").select("role").execute()
    if not response.data:
        return {"total": 0, "teachers": 0, "students": 0}
    teachers = sum(1 for u in response.data if u ["role"] == "teacher")
    students = sum(1 for u in response.data if u ["role"] == "student")
    total = len(response.data)
    return {
        "total": total,
        "teachers": teachers,
        "students": students
    }