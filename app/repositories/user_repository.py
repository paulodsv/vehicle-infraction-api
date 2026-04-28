from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository():
    def __init__(self, db: Session):
        self.db = db

    def save_user(self, user_data: UserCreate) -> User:
        user = User(email = user_data.email, hashed_password = user_data.password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, id: int) -> User:
        return self.db.query(User).filter(User.id == id).first()
    
    def get_all_users(self) -> list[User]:
        return self.db.query(User).all()