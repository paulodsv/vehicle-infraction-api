from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.core.database import Base


class InfractionQueries(Base):
    __tablename__ = "infraction_queries"
    id = Column(Integer, primary_key=True, index=True)
    plate = Column(String, nullable=False)
    queried_at = Column(DateTime, default=datetime.utcnow)
    total_infractions = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)