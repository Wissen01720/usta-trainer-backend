from fastapi import APIRouter, Depends, HTTPException
from app.services.progress_service import ProgressService
from app.schemas.progress import ProgressCreate, ProgressOut
from app.utils.dependencies import get_current_user
from app.schemas.user import UserOut

router = APIRouter(prefix="/progress", tags=["progress"])

@router.post("/", response_model=ProgressOut)
async def add_progress(
    progress_data: ProgressCreate,
    service: ProgressService = Depends(ProgressService),
    current_user: UserOut = Depends(get_current_user)
):
    try:
        return await service.add_progress(current_user.id, progress_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ProgressOut])
async def get_my_progress(
    service: ProgressService = Depends(ProgressService),
    current_user: UserOut = Depends(get_current_user)
):
    return await service.get_progress(current_user.id)