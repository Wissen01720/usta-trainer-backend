from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Any

class LessonBase(BaseModel):
    title: str
    slug: str
    content: str
    difficulty_level: Optional[str] = None
    thumbnail_url: Optional[str] = None
    video_url: Optional[str] = None
    estimated_duration: Optional[int] = None
    prerequisites: Optional[Any] = None

class LessonCreate(LessonBase):
    is_published: bool = False

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    difficulty_level: Optional[str] = None
    thumbnail_url: Optional[str] = None
    video_url: Optional[str] = None
    estimated_duration: Optional[int] = None
    is_published: Optional[bool] = None
    prerequisites: Optional[Any] = None

class LessonOut(LessonBase):
    id: str
    author_id: str
    is_published: bool
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True