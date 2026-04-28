from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.gateways.senatran_gateway import SenatranGateway
from app.models.user import User
from app.repositories.infraction_repository import InfractionRepository
from app.repositories.user_repository import UserRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.services.infraction_service import InfractionService
from app.services.senatran_service import SenatranService
from app.services.user_service import UserService
from app.services.vehicle_service import VehicleService


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
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
    return service

def get_infractions_service(db: Session = Depends(get_db)):
    infraction_repo = InfractionRepository(db)
    user_repo = UserRepository(db)
    vehicle_repo = VehicleRepository(db)
    service = InfractionService(infraction_repo, user_repo, vehicle_repo)
    return service

def get_senatran_service(db: Session = Depends(get_db)):
    senatran_gateway = SenatranGateway()
    infraction_repo = InfractionRepository(db)
    vehicle_repo = VehicleRepository(db)
    service = SenatranService(senatran_gateway, infraction_repo, vehicle_repo)
    return service