from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user import UserCreate, UserLogin
from app.repositories.user_repository import UserRepository
from app.domain.exceptions import AlreadyRegisteredUser, InvalidUserEmail, InvalidUserPassword
from app.schemas.token import TokenResponse
from app.models.user import User
from app.domain.exceptions import UserEmailNotFound, UserIdNotFound

class UserService():
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user_service(self, user_data: UserCreate) -> User:
        verify_user_existence_by_email = self.user_repo.get_user_by_email(user_data.email)

        if verify_user_existence_by_email:
            raise AlreadyRegisteredUser("Já existe um usuário cadastrado com o email informado")
        
        user_hash_pass = hash_password(user_data.password)
        user_data.password = user_hash_pass
        return self.user_repo.save_user(user_data)
    
    def login_service(self, user_data: UserLogin) -> TokenResponse:
        searched_user = self.user_repo.get_user_by_email(user_data.email)

        if not searched_user:
            raise InvalidUserEmail("Email não cadastrado")
        
        is_pass_valid = verify_password(user_data.password, searched_user.hashed_password)

        if not is_pass_valid:
            raise InvalidUserPassword("Senha incorreta")
        
        access_token = create_access_token({"email": searched_user.email})
        return TokenResponse(access_token=access_token, token_type="bearer")

    def get_all_users_service(self) -> list[User]:
        return self.user_repo.get_all_users()
    
    def get_user_by_email_service(self, user_email: str) -> User:
        user = self.user_repo.get_user_by_email(user_email)
        if not user:
            raise UserEmailNotFound("Não existe um usuário com o email informado")
        return user
    
    def get_user_by_id_service(self, user_id: int) -> User:
        user =  self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserIdNotFound("Não existe um usuário com o ID informado")
        return user