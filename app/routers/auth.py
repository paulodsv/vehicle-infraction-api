from fastapi import APIRouter, Depends

from app.core.dependencies import get_user_service
from app.schemas.response import APIResponse, success_response
from app.schemas.token import TokenResponse
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.user_service import UserService

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/register", status_code=201, 
                  response_model=APIResponse[UserResponse], 
                  summary="Cadastra um novo usuário", 
                  description="Cria um novo usuário no sistema",
                  operation_id="userRegister",
                  responses={
                      201: {"description": "Usuário cadastrado com sucesso"},
                      409: {"description": "Email já registrado no sistema"}
                  })
def register(user_data: UserCreate, service: UserService = Depends(get_user_service)) -> APIResponse[UserResponse]:
    user = service.register_user_service(user_data)
    return success_response(user, "Usuário cadastrado com sucesso")

@auth_router.post("/login", status_code=200, 
                  response_model=TokenResponse,
                  description="Realiza o Login de um usuário",
                  summary="Login do usuário",
                  operation_id="userLogin",
                  responses={
                      200: {"description": "Login realizado com sucesso"},
                      401: {"description": "Email ou senha inválidos"}
                  })
def login(user_data: UserLogin, service: UserService = Depends(get_user_service)) -> TokenResponse:
    return service.login_service(user_data)