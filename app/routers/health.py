from fastapi import APIRouter, Depends
from app.core.dependencies import get_db    
from sqlalchemy.orm import Session
from sqlalchemy import text

health_router = APIRouter(prefix="/health", tags=["Health"])

@health_router.get("/")
def get_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "unavailable"
    
    return {"status": "ok", "database": db_status}