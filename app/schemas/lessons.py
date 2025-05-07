from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schemas.exercise import ExerciseOut

class LessonBase(BaseModel):
    title: str
    content: str
    difficulty_level: Optional[str]
    thumbnail_url: Optional[str]

class LessonCreate(LessonBase):
    is_published: bool = False
    prerequisites: Optional[List[str]]

class LessonOut(LessonBase):
    id: str
    author_id: str
    is_published: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class LessonWithExercises(LessonOut):
    exercises: List[ExerciseOut]