from app.core.security import hash_password
from app.schemas.user import UserCreate
from app.repositories.user_repository import UserRepository

class UserService():
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user_service(self, user_data: UserCreate):
        verify_user_existence_by_email = self.user_repo.get_user_by_email(user_data.email)
        if verify_user_existence_by_email:
            raise