from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.lessons import LessonCreate, LessonOut, LessonWithExercises
from app.services.lesson_service import LessonService
from app.utils.dependencies import get_current_user, get_current_teacher

router = APIRouter(prefix="/api/v1/lessons", tags=["lessons"])

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
    service: LessonService = Depends(LessonService)
):
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