from fastapi import APIRouter, Depends, HTTPException, status
from app.services.user_service import UserService
from app.utils.dependencies import get_current_user
from app.utils.exceptions import NotFoundException
from app.schemas.user import UserOut, UserUpdate, UserCreate

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
async def get_current_user_profile(
    current_user: UserOut = Depends(get_current_user)
):
    """
    Obtener el perfil del usuario autenticado.
    """
    return current_user

@router.put("/me", response_model=UserOut)
async def update_current_user(
    user_data: UserUpdate,
    service: UserService = Depends(UserService),
    current_user: UserOut = Depends(get_current_user)
):
    """
    Actualizar el perfil del usuario autenticado.
    """
    try:
        return await service.update_user(current_user.id, user_data)
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

@router.get("/{user_id}", response_model=UserOut)
async def get_user_profile(
    user_id: str,
    service: UserService = Depends(UserService),
    current_user: UserOut = Depends(get_current_user)
):
    """
    Obtener el perfil de un usuario por su ID.
    Los usuarios normales solo pueden acceder a su propio perfil.
    """
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este recurso"
        )
    try:
        return await service.get_user_by_id(user_id)
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

@router.get("/", response_model=list[UserOut])
async def list_users(
    service: UserService = Depends(UserService),
    current_user: UserOut = Depends(get_current_user)
):
    """
    Listar todos los usuarios.
    Solo accesible para administradores.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este recurso"
        )
    return await service.list_users()

@router.put("/{user_id}", response_model=UserOut)
async def update_user_by_admin(
    user_id: str,
    user_data: UserUpdate,
    service: UserService = Depends(UserService),
    current_user: UserOut = Depends(get_current_user)
):
    """
    Editar usuario por ID (solo admin).
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este recurso"
        )
    try:
        return await service.update_user(user_id, user_data)
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

@router.delete("/{user_id}", status_code=204)
async def delete_user_by_admin(
    user_id: str,
    service: UserService = Depends(UserService),
    current_user: UserOut = Depends(get_current_user)
):
    """
    Eliminar usuario por ID (solo admin).
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este recurso"
        )
    try:
        await service.delete_user(user_id)
    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

@router.post("/", response_model=UserOut, status_code=201)
async def create_user_by_admin(
    user_data: UserCreate,
    service: UserService = Depends(UserService),
    current_user: UserOut = Depends(get_current_user)
):
    """
    Crear un nuevo usuario (solo admin).
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este recurso"
        )
    try:
        return await service.create_user(user_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )