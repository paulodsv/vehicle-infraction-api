from fastapi import APIRouter, Depends
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.schemas.token import TokenResponse
from app.core.dependencies import get_user_service

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/register", status_code=201, 
                  response_model=UserResponse, 
                  summary="Cadastra um novo usuário", 
                  description="Cria um novo usuário no sistema",
                  operation_id="userRegister",
                  responses={
                      201: {"description": "Usuário cadastrado com sucesso"},
                      409: {"description": "Email já registrado no sistema"}
                  })
def register(user_data: UserCreate, service: UserService = Depends(get_user_service)) -> UserResponse:
    return service.register_user_service(user_data)

@auth_router.post("/login", status_code=200, 
                  response_model=TokenResponse,
                  description="Realiza o Login de um usuário",
                  summary="Login do usuário",
                  operation_id="userLogin",
                  responses={
                      200: {"description": "Login realizado com sucesso"},
                      404: {"description": "Email ou senha inválidos"}
                  })
def login(user_data: UserLogin, service: UserService = Depends(get_user_service)) -> TokenResponse:
    return service.login_service(user_data)