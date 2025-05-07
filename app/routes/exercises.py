from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate, ExerciseOut, ExerciseWithTests
from app.services.exercise_service import ExerciseService
from app.utils.dependencies import get_current_user
from app.utils.exceptions import NotFoundException

router = APIRouter(prefix="/api/v1/exercises", tags=["exercises"])

@router.post("/", response_model=ExerciseOut, status_code=status.HTTP_201_CREATED)
async def create_exercise(
    exercise: ExerciseCreate,
    service: ExerciseService = Depends(ExerciseService),
    current_user=Depends(get_current_user)
):
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo profesores y administradores pueden crear ejercicios"
        )
    
    try:
        return await service.create_exercise(exercise, current_user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[ExerciseOut])
async def get_exercises(
    difficulty: str = None,
    language: str = None,
    service: ExerciseService = Depends(ExerciseService)
):
    try:
        return await service.get_exercises(difficulty, language)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error obteniendo ejercicios"
        )

@router.get("/{exercise_id}", response_model=ExerciseWithTests)
async def get_exercise_detail(
    exercise_id: str,
    service: ExerciseService = Depends(ExerciseService)
):
    try:
        return await service.get_exercise_with_tests(exercise_id)
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ejercicio no encontrado"
        )