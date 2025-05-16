from enum import Enum
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    
    # Configuración moderna para Pydantic v2
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.STUDENT

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    avatar_url: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=500)

class UserOut(BaseModel):
    id: str
    role: UserRole
    avatar_url: Optional[str] = None
    is_active: bool
    created_at: str
    updated_at: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None