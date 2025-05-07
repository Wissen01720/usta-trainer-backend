from typing import Optional, List
from app.database import get_supabase
from app.schemas.exercise import ExerciseCreate, ExerciseOut, ExerciseWithTests
from app.utils.exceptions import NotFoundException


class ExerciseService:
    def __init__(self):
        self.supabase = get_supabase()
    
    async def create_exercise(self, exercise: ExerciseCreate, author_id: str) -> ExerciseOut:
        exercise_data = exercise.dict()
        exercise_data["author_id"] = author_id
        
        response = self.supabase.table("exercises").insert(exercise_data).execute()
        
        if not response.data:
            raise Exception("Error al crear ejercicio")
        
        return response.data[0]
    
    async def get_exercise(self, difficulty: Optional[str], language: Optional[str]) -> List[ExerciseOut]:
        query = self.supabase.table("exercises").select("*").eq("is_public", True)
        
        if difficulty:
            query = query.eq("difficulty", difficulty)
        if language:
            query = query.eq("language", language)
            
        response = query.execute()
        return response.data 
    
    async def get_exercise_with_tests(self, exercise_id: str) -> ExerciseWithTests:
        response = self.supabase.table("exercises").select("*").eq("id", exercise_id).execute()
        
        if not response.data:
            raise NotFoundException("Ejercicio no encontrado")
        
        tests_response = self.supabase.table("tests_cases").select("*").eq("exercise_id", exercise_id).execute()
        
        return {
            **response.data[0],
            "tests_cases": tests_response.data
        }