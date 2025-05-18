from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schemas.exercise import ExerciseOut

class LessonBase(BaseModel):
    title: str
    content: str
    difficulty_level: Optional[str] = None
    thumbnail_url: Optional[str] = None

class LessonCreate(LessonBase):
    is_published: bool = False
    prerequisites: Optional[List[str]] = None

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    difficulty_level: Optional[str] = None
    thumbnail_url: Optional[str] = None
    is_published: Optional[bool] = None
    prerequisites: Optional[List[str]] = None

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