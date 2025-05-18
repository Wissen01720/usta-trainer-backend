import re
from typing import Optional, List
from app.database import get_supabase
from app.schemas.exercise import ExerciseCreate, ExerciseOut, ExerciseUpdate, ExerciseWithTests
from app.utils.exceptions import NotFoundException
from fastapi import HTTPException, status
from loguru import logger
from pydantic import ValidationError

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^\w\-]', '', text)
    text = re.sub(r'-+', '-', text)
    return text

class ExerciseService:
    def __init__(self):
        self.supabase = get_supabase()

    async def create_exercise(self, exercise: ExerciseCreate, author_id: str) -> ExerciseOut:
        try:
            exercise_data = exercise.model_dump()
            exercise_data["author_id"] = author_id
            # Generar slug si no viene del frontend
            if not exercise_data.get("slug"):
                exercise_data["slug"] = slugify(exercise_data["title"])
            response = self.supabase.table("exercises").insert(exercise_data).execute()
            if not response.data:
                logger.error("Empty response from Supabase when creating exercise")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to create exercise"
                )
            return ExerciseOut(**response.data[0])
        except ValidationError as e:
            logger.error(f"Validation error while creating exercise: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Invalid data format for exercise"
            )
        except Exception as e:
            logger.error(f"Unexpected error creating exercise: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    async def get_exercises(self, difficulty: Optional[str] = None,
                            language: Optional[str] = None) -> List[ExerciseOut]:
        """Retrieve only public exercises (for students)"""
        try:
            query = self.supabase.table("exercises").select("*").eq("is_public", True)
            if difficulty:
                query = query.eq("difficulty", difficulty)
            if language:
                query = query.eq("language", language)
            response = query.execute()
            exercises = []
            for item in response.data:
                try:
                    exercises.append(ExerciseOut(**item))
                except ValidationError as e:
                    logger.warning(f"Skipping invalid exercise data: {str(e)}")
            return exercises
        except Exception as e:
            logger.error(f"Database error fetching exercises: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )

    async def get_all_exercises(self, difficulty: Optional[str] = None,
                                language: Optional[str] = None) -> List[ExerciseOut]:
        """Retrieve all exercises (for admin/teacher)"""
        try:
            query = self.supabase.table("exercises").select("*")
            if difficulty:
                query = query.eq("difficulty", difficulty)
            if language:
                query = query.eq("language", language)
            response = query.execute()
            exercises = []
            for item in response.data:
                try:
                    exercises.append(ExerciseOut(**item))
                except ValidationError as e:
                    logger.warning(f"Skipping invalid exercise data: {str(e)}")
            return exercises
        except Exception as e:
            logger.error(f"Database error fetching all exercises: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )

    async def get_exercise_with_tests(self, exercise_id: str) -> ExerciseWithTests:
        try:
            exercise_response = self.supabase.table("exercises") \
                .select("*") \
                .eq("id", exercise_id) \
                .execute()
            if not exercise_response.data:
                raise NotFoundException("Exercise not found")
            tests_response = self.supabase.table("test_cases") \
                .select("*") \
                .eq("exercise_id", exercise_id) \
                .execute()
            return ExerciseWithTests(
                **exercise_response.data[0],
                test_cases=tests_response.data or []
            )
        except ValidationError as e:
            logger.error(f"Data validation error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Invalid data format"
            )
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching exercise: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    async def update_exercise(self, exercise_id: str, exercise: ExerciseUpdate) -> ExerciseOut:
        update_data = exercise.model_dump(exclude_unset=True)
        response = self.supabase.table("exercises").update(update_data).eq("id", exercise_id).execute()
        if not response.data:
            raise NotFoundException("Exercise not found or no changes")
        return ExerciseOut(**response.data[0])

    async def delete_exercise(self, exercise_id: str):
        response = self.supabase.table("exercises").delete().eq("id", exercise_id).execute()
        if not response.data:
            raise NotFoundException("Exercise not found")