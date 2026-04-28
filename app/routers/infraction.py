from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, get_infractions_service, get_vehicle_service
from app.models.user import User
from app.schemas.infraction import InfractionQueryResponse, InfractionResponse
from app.schemas.response import APIResponse, success_response
from app.services.infraction_service import InfractionService
from app.services.vehicle_service import VehicleService

infractions_router = APIRouter(prefix="/infractions", tags=["Infractions"])

@infractions_router.get("/queries/{user_id}", status_code=200,
                        response_model=APIResponse[list[InfractionQueryResponse]],
                        summary="Retorna queries pelo user_id",
                        description="Retorna uma query realizada por um usuário que consultou infrações",
                        operation_id="getQueryByUserId",
                        responses={
                            200: {"description": "Queries retornadas com sucesso"},
                            404: {"description": "ID do usuário informado não existe"}
                        })
def get_queries_by_user_id(user_id: int, 
                           service: InfractionService = Depends(get_infractions_service), 
                           get_current_user: User = Depends(get_current_user)) -> APIResponse[list[InfractionQueryResponse]]:
    queries = service.get_queries_by_user_id_service(user_id)
    return success_response(queries, "Queries retornadas com sucesso")

@infractions_router.get("/queries/{query_id}/infractions", status_code=200,
                        response_model=APIResponse[list[InfractionResponse]],
                        summary="Retorna infrações por uma query id",
                        description="Retorna todas as infrações que foram consultadas em uma query específica, pelo seu respectivo id",
                        operation_id="getInfractionsByQueryId",
                        responses={
                            200: {"description": "Infrações retornadas com sucesso"},
                            404: {"description": "O ID da query informado não existe"}
                        })
def get_infractions_by_query_id(query_id: int,
                                service: InfractionService = Depends(get_infractions_service),
                                get_current_user: User = Depends(get_current_user)) -> APIResponse[list[InfractionResponse]]:
    infractions = service.get_infractions_by_query_service(query_id)
    return success_response(infractions, "Infrações retornadas com sucesso")

@infractions_router.get("/{plate}", status_code=200,
                        response_model=APIResponse[list[InfractionResponse]],
                        summary="Retorna infrações por placa",
                        description="Consulta e retorna infrações já registradas no sistema, baseado na placa do veículo",
                        operation_id="getInfractionsByPlate",
                        responses={
                            200: {"description": "Infrações retornadas com sucesso"},
                            404: {"description": "Placa informada não registrada no sistema"}
                        })
def get_infractions_by_plate(plate: str, 
                                   service: InfractionService = Depends(get_infractions_service),
                                   vehicle_service: VehicleService = Depends(get_vehicle_service), 
                                   get_current_user: User = Depends(get_current_user)) -> APIResponse[list[InfractionResponse]]:
    plate = plate.upper() 
    vehicle_service.get_vehicle_by_plate_service(plate)
    infractions = service.get_infractions_by_plate_service(plate)
    return success_response(infractions, "Infrações retornadas com sucesso")

