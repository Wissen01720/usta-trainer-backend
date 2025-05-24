from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.lessons import LessonCreate, LessonOut, LessonWithExercises
from app.services.lesson_service import LessonService
from app.utils.dependencies import get_current_user, get_current_teacher

router = APIRouter(prefix="/lessons", tags=["lessons"])

@router.post("/", response_model=LessonOut, status_code=status.HTTP_201_CREATED)
async def create_lesson(
    lesson: LessonCreate,
    service: LessonService = Depends(LessonService),
    current_user=Depends(get_current_teacher)
):
    try:
        return await service.create_lesson(lesson, current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[LessonOut])
async def get_lessons(
    service: LessonService = Depends(LessonService),
    current_user=Depends(get_current_user)
):
    # Si el usuario es admin o teacher, devuelve todas las lecciones
    if current_user.role in ["admin", "teacher"]:
        return await service.get_all_lessons()
    # Si es estudiante, solo las publicadas
    return await service.get_public_lessons()

@router.get("/{lesson_id}", response_model=LessonWithExercises)
async def get_lesson_detail(
    lesson_id: str,
    service: LessonService = Depends(LessonService)
):
    try:
        return await service.get_lesson_with_exercises(lesson_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e))

@router.put("/{lesson_id}", response_model=LessonOut)
async def update_lesson(
    lesson_id: str,
    lesson: LessonCreate,
    service: LessonService = Depends(LessonService),
    current_user=Depends(get_current_teacher)
):
    try:
        return await service.update_lesson(lesson_id, lesson)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{lesson_id}", status_code=204)
async def delete_lesson(
    lesson_id: str,
    service: LessonService = Depends(LessonService),
    current_user=Depends(get_current_teacher)
):
    try:
        await service.delete_lesson(lesson_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )