from fastapi import APIRouter, Depends
from app.schemas.senatran import SenatranInfractionQuery
from app.schemas.infraction import InfractionResponse
from app.core.dependencies import get_current_user, get_senatran_service
from app.models.user import User
from app.services.senatran_service import SenatranService

senatran_router = APIRouter(prefix="/senatran", tags=["Senatran"])

@senatran_router.post("/infractions", status_code=201, 
                      response_model=list[InfractionResponse],
                      summary="Consulta infrações no Senatran",
                      description="Retorna uma lista de infrações do Senatran pela placa do veículo",
                      operation_id="getSenatranInfractions",
                      responses={
                          201: {"description": "Infrações consultadas e gravadas com sucesso!"},
                          400: {"description": "Placa ou CNPJ informados incorretos"}
                      })
def consult_infractions(data: SenatranInfractionQuery, 
                        current_user: User = Depends(get_current_user), 
                        service: SenatranService = Depends(get_senatran_service)) -> list[InfractionResponse]:
    return service.consult_infractions_service(data, current_user.id)


@senatran_router.post("/fetch-details", status_code=200, 
                      summary="Busca detalhes das infrações pendentes",
                      description="Atualiza infrações do banco de dados que ainda não possuem detalhes registrados",
                      operation_id="fetchDetails",
                      responses={
                          200: {"description": "x infrações atualizadas com sucesso"},
                          500: {"description": "Erro interno ao atualizar infrações pendentes"}
                      })
def fetch_infraction_details(get_current_user: User = Depends(get_current_user), 
                               service: SenatranService = Depends(get_senatran_service)):
    count = service.fetch_infraction_details_service()
    return {"message": f"{count} infrações atualizadas com sucesso"}