from typing import List
from app.database import get_supabase
from app.schemas.lessons import LessonOut, LessonWithExercises
from app.utils.exceptions import NotFoundException

class LessonService:
    def __init__(self):
        self.supabase = get_supabase()

    async def create_lesson(self, lesson_data, author_id: str) -> LessonOut:
        lesson = lesson_data.dict()
        lesson["author_id"] = author_id
        
        response = self.supabase.table("lessons").insert(lesson).execute()
        
        if not response.data:
            raise Exception("Error al crear lección")
            
        return response.data[0]

    async def get_public_lessons(self) -> List[LessonOut]:
        response = self.supabase.table("lessons")\
            .select("*")\
            .eq("is_published", True)\
            .order("created_at", desc=True)\
            .execute()
            
        return response.data

    async def get_lesson_with_exercises(self, lesson_id: str) -> LessonWithExercises:
        # Obtener la lección
        lesson_response = self.supabase.table("lessons")\
            .select("*")\
            .eq("id", lesson_id)\
            .single()\
            .execute()
            
        if not lesson_response.data:
            raise NotFoundException("Lección no encontrada")
        
        exercises_response = self.supabase.table("lesson_exercises")\
            .select("exercises(*)")\
            .eq("lesson_id", lesson_id)\
            .execute()
            
        return {
            **lesson_response.data,
            "exercises": [e["exercises"] for e in exercises_response.data]
        }
    
    async def get_all_lessons(self) -> list[LessonOut]:
        response = self.supabase.table("lessons").select("*").order("created_at", desc=True).execute()  # <-- aquí
        return response.data

    async def update_lesson(self, lesson_id: str, lesson_data) -> LessonOut:
        data = lesson_data.dict(exclude_unset=True)
        response = self.supabase.table("lessons").update(data).eq("id", lesson_id).execute()
        if not response.data:
            raise NotFoundException("Lección no encontrada o sin cambios")
        return response.data[0]

    async def delete_lesson(self, lesson_id: str):
        response = self.supabase.table("lessons").delete().eq("id", lesson_id).execute()
        if not response.data:
            raise NotFoundException("Lección no encontrada")