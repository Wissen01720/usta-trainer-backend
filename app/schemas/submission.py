from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from enum import Enum

class SubmissionStatus(str, Enum):
    PENDING = "pending"
    PROCESSED = "processed"

class SubmissionBase(BaseModel):
    exercise_id: str
    code: str
    language: str

class SubmissionCreate(SubmissionBase):
    pass

class SubmissionOut(SubmissionBase):
    id: str
    user_id: str
    status: SubmissionStatus
    feedback: Optional[str]
    execution_time_ms: Optional[int]
    memory_usage_kb: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True