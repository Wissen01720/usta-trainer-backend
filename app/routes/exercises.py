from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.schemas.exercise import ExerciseCreate, ExerciseUpdate, ExerciseOut, ExerciseWithTests
from app.utils.dependencies import get_current_user
from app.utils.exceptions import NotFoundException
from app.services.exercise_service import ExerciseService  # ← IMPORTACIÓN DIRECTA

from loguru import logger

router = APIRouter(
    prefix="/api/v1/exercises",
    tags=["exercises"],
    responses={
        404: {"description": "Resource not found"},
        500: {"description": "Internal server error"}
    }
)

@router.post(
    "/",
    response_model=ExerciseOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        403: {"description": "Forbidden operation"},
        400: {"description": "Invalid input data"}
    }
)
async def create_exercise(
    exercise: ExerciseCreate,
    service: ExerciseService = Depends(ExerciseService),
    current_user=Depends(get_current_user)
):
    """Create a new exercise (requires teacher or admin role)"""
    if current_user.role not in ["teacher", "admin"]:
        logger.warning(f"Unauthorized attempt to create exercise by user {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers and admins can create exercises"
        )

    try:
        return await service.create_exercise(exercise, current_user.id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating exercise: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/",
    response_model=List[ExerciseOut],
    responses={
        200: {"description": "List of public exercises"}
    }
)
async def get_exercises(
    difficulty: str = None,
    language: str = None,
    service: ExerciseService = Depends(ExerciseService)
):
    """Get all public exercises with optional filters"""
    try:
        return await service.get_exercises(difficulty, language)
    except Exception as e:
        logger.error(f"Error fetching exercises: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving exercises"
        )

@router.get(
    "/{exercise_id}",
    response_model=ExerciseWithTests,
    responses={
        404: {"description": "Exercise not found"}
    }
)
async def get_exercise_detail(
    exercise_id: str,
    service: ExerciseService = Depends(ExerciseService)
):
    """Get exercise details with test cases"""
    try:
        return await service.get_exercise_with_tests(exercise_id)
    except NotFoundException as e:
        logger.warning(f"Exercise not found: {exercise_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error fetching exercise {exercise_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving exercise details"
        )
