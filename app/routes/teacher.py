from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_supabase
from app.utils.dependencies import get_current_user
from app.schemas.lessons import LessonCreate, LessonUpdate, LessonOut

router = APIRouter(prefix="/teacher", tags=["teacher"])

@router.get("/lessons", response_model=list[LessonOut])
async def get_teacher_lessons(current_user=Depends(get_current_user)):
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los profesores pueden acceder a sus lecciones"
        )
    supabase = get_supabase()
    response = supabase.table("lessons").select("*").eq("author_id", current_user.id).execute()
    return response.data or []

@router.post("/lessons", response_model=LessonOut, status_code=201)
async def create_lesson(
    lesson: LessonCreate,
    current_user=Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los profesores pueden crear lecciones"
        )
    supabase = get_supabase()
    lesson_data = lesson.model_dump()
    lesson_data["author_id"] = current_user.id
    response = supabase.table("lessons").insert(lesson_data).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="No se pudo crear la lección")
    return response.data[0]

@router.put("/lessons/{lesson_id}", response_model=LessonOut)
async def update_lesson(
    lesson_id: str,
    lesson: LessonUpdate,
    current_user=Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los profesores pueden editar lecciones"
        )
    supabase = get_supabase()
    response = supabase.table("lessons").update(lesson.model_dump(exclude_unset=True)).eq("id", lesson_id).eq("author_id", current_user.id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Lección no encontrada o no tienes permiso")
    return response.data[0]

@router.delete("/lessons/{lesson_id}", status_code=204)
async def delete_lesson(
    lesson_id: str,
    current_user=Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los profesores pueden eliminar lecciones"
        )
    supabase = get_supabase()
    response = supabase.table("lessons").delete().eq("id", lesson_id).eq("author_id", current_user.id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Lección no encontrada o no tienes permiso")
    return