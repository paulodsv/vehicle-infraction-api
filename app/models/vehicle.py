from app.core.database import Base
from sqlalchemy import String, Integer, Boolean, Column

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    plate = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)
    company_cnpj = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)