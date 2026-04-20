from fastapi import APIRouter, Depends
from app.schemas.senatran import SenatranInfractionQuery
from app.core.dependencies import get_current_user, get_senatran_service
from app.models.user import User
from app.services.senatran_service import SenatranService

senatran_router = APIRouter(prefix="/senatran", tags=["Senatran"])

@senatran_router.post("/infractions", status_code=201)
def consult_infractions(data: SenatranInfractionQuery, current_user: User = Depends(get_current_user), service: SenatranService = Depends(get_senatran_service)):
    return service.consult_infractions_service(data, current_user.id)