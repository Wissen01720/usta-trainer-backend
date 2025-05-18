from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class ProgressCreate(BaseModel):
    date: date
    activity: str = Field(..., max_length=255)
    details: Optional[str] = None

class ProgressOut(BaseModel):
    id: str
    user_id: str
    date: date
    activity: str
    details: Optional[str] = None
    created_at: str