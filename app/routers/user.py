from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, get_user_service
from app.models.user import User
from app.schemas.response import APIResponse, success_response
from app.schemas.user import UserResponse
from app.services.user_service import UserService

user_router = APIRouter(prefix="/Users", tags=["Users"])

@user_router.get("/", status_code=200,
                 response_model=APIResponse[list[UserResponse]], 
                 summary="Lista todos os usuários do sistema", 
                 description="Retorna uma lista de todos os usuários cadastrados no sistema", 
                 operation_id="getAllUsers")
def get_all_users(get_current_user: User = Depends(get_current_user), service: UserService = Depends(get_user_service)) -> APIResponse[list[UserResponse]]:
    users_list = service.get_all_users_service()
    return success_response(users_list, "Usuários listados com sucesso")

@user_router.get("/{user_email}", status_code=200,
                 response_model=APIResponse[UserResponse], 
                 summary="Retorna um usuário pelo email", 
                 description="Busca e retorna um usuário cadastrado no sistema pelo seu email", 
                 operation_id="getUserByEmail", 
                 responses={
                     200: {"description": "Usuário retornado com sucesso"},
                     404: {"description": "Não existe um usuário com o email informado"}
                 })
def get_user_by_email(user_email: str, get_current_user: User = Depends(get_current_user), service: UserService = Depends(get_user_service)) -> APIResponse[UserResponse]:
    user = service.get_user_by_email_service(user_email)
    return success_response(user, "Usuário retornado com sucesso")