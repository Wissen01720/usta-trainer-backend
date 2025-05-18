from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class ExerciseBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=100,
                      examples=["Implement a stack data structure"],
                      description="Title of the exercise")
    description: str = Field(..., min_length=10, max_length=500,
                           examples=["Create a stack class with push, pop and peek methods"],
                           description="Detailed exercise description")
    difficulty: str = Field(..., pattern="^(beginner|intermediate|advanced|expert)$",
                          description="Exercise difficulty level")
    language: str = Field(..., min_length=2, max_length=20,
                         examples=["python", "javascript"],
                         description="Programming language for the exercise")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "title": "Implement a stack",
                "description": "Create stack with basic operations",
                "difficulty": "intermediate",
                "language": "python"
            }
        }
    )

class ExerciseCreate(ExerciseBase):
    starter_code: str = Field(..., min_length=10,
                            description="Initial code provided to students")
    solution_code: Optional[str] = Field(None,
                                       description="Reference solution code")
    is_public: bool = Field(False,
                           description="Visibility of the exercise")

class ExerciseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=100)
    description: Optional[str] = Field(None, min_length=10, max_length=500)
    difficulty: Optional[str] = None
    language: Optional[str] = None
    starter_code: Optional[str] = None
    solution_code: Optional[str] = None
    is_public: Optional[bool] = None

class ExerciseOut(ExerciseBase):
    id: str = Field(..., description="Unique identifier for the exercise")
    author_id: str = Field(..., description="ID of the exercise author")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    is_public: bool = Field(..., description="Visibility status")

class ExerciseWithTests(ExerciseOut):
    test_cases: List[dict] = Field(...,
                                 description="List of test cases for validation",
                                 example=[{"input": "5", "output": "120"}])