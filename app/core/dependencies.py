from app.core.database import SessionLocal
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.config import settings
from app.repositories.user_repository import UserRepository
from app.services.auth_service import UserService
from app.repositories.vehicle_repository import VehicleRepository
from app.services.vehicle_service import VehicleService

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    return user

def get_user_service(db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    service = UserService(user_repo)
    return service

def get_vehicle_service(db: Session = Depends(get_db)):
    vehicle_repo = VehicleRepository(db)
    service = VehicleService(vehicle_repo)