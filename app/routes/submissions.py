from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.schemas.submission import SubmissionOut, SubmissionCreate
from app.services.submission_service import SubmissionService
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/submissions", tags=["submissions"])

@router.post("/", response_model=SubmissionOut, status_code=status.HTTP_201_CREATED)
async def create_submission(
    submission: SubmissionCreate,
    service: SubmissionService = Depends(SubmissionService),
    current_user=Depends(get_current_user)
):
    try:
        return await service.create_submission(current_user.id, submission)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/me", response_model=List[SubmissionOut])
async def get_my_submissions(
    exercise_id: Optional[str] = None,
    service: SubmissionService = Depends(SubmissionService),
    current_user=Depends(get_current_user)
):
    return await service.get_user_submissions(current_user.id, exercise_id)

@router.get("/exercise/{exercise_id}", response_model=List[SubmissionOut])
async def get_exercise_submissions(
    exercise_id: str,
    service: SubmissionService = Depends(SubmissionService),
    current_user=Depends(get_current_user)
):
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo profesores y administradores pueden ver estos envíos"
        )
    
    return await service.get_exercise_submissions(exercise_id)