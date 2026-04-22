from fastapi import APIRouter, Depends
from app.models.user import User
from app.core.dependencies import get_current_user
from app.services.user_service import UserService
from app.core.dependencies import get_user_service
from app.schemas.user import UserResponse

user_router = APIRouter(prefix="/Users", tags=["Users"])

@user_router.get("/", status_code=200,
                 response_model=list[UserResponse])
def get_all_users(get_current_user: User = Depends(get_current_user), service: UserService = Depends(get_user_service)) -> list[UserResponse]:
    return service.get_all_users_service()

@user_router.get("/{user_email}", status_code=200,
                 response_model=UserResponse)
def get_user_by_email(user_email: str, get_current_user: User = Depends(get_current_user), service: UserService = Depends(get_user_service)) -> UserResponse:
    return service.get_user_by_email_service(user_email)