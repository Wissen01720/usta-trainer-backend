from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

class ExerciseBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    difficulty: str = Field(..., pattern="^(beginner|intermediate|advanced|expert)$")
    language: str = Field(..., min_length=2, max_length=20)
    
    # Configuración moderna para Pydantic v2
    model_config = ConfigDict(from_attributes=True)

class ExerciseCreate(ExerciseBase):
    starter_code: str = Field(..., min_length=10)
    solution_code: Optional[str] = None
    is_public: bool = False

class ExerciseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=100)
    description: Optional[str] = Field(None, min_length=10, max_length=500)
    is_public: Optional[bool] = None

class ExerciseOut(ExerciseBase):
    id: str
    author_id: str
    created_at: datetime
    updated_at: datetime
    is_public: bool

class ExerciseWithTests(ExerciseOut):
    test_cases: List[dict]