from fastapi import APIRouter, Depends
from app.schemas.vehicle import VehicleCreate, TipoVeiculo, VehicleUpdate, VehicleResponse
from app.core.dependencies import get_vehicle_service, get_current_user
from app.services.vehicle_service import VehicleService
from app.models.user import User
from app.schemas.response import APIResponse, success_response

vehicle_router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@vehicle_router.post("/", status_code=201, 
                     response_model=APIResponse[VehicleResponse],
                     summary="Cadastra um veículo",
                     description="Registra um novo veículo no sistema",
                     operation_id="saveVehicle",
                     responses={
                         201: {"description": "Veículo registrado com sucesso"},
                         409: {"description": "Veículo com essa placa já registrado no sistema"}
                     })
def save_vehicle(vehicle_data: VehicleCreate, 
                 service: VehicleService = Depends(get_vehicle_service), 
                 current_user: User = Depends(get_current_user)) -> APIResponse[VehicleResponse]:
    vehicle = service.save_vehicle_service(vehicle_data)
    return success_response(vehicle, "Veículo registrado com sucesso")

@vehicle_router.get("/{plate}", status_code=200, 
                    response_model=APIResponse[VehicleResponse],
                    summary="Busca um veículo por placa",
                    description="Retorna um veículo cadastrado no sistema pela sua placa",
                    operation_id="getVehicleByPlate",
                    responses={
                        200: {"description": "Veículo retornado com sucesso"},
                        404: {"description": "Placa informada não encontrada no sistema"}
                    })
def get_vehicle_by_plate(plate: str, 
                         service: VehicleService = Depends(get_vehicle_service), 
                         current_user: User = Depends(get_current_user)) -> APIResponse[VehicleResponse]:
    vehicle = service.get_vehicle_by_plate_service(plate)
    return success_response(vehicle, "Veículo retornado com sucesso")

@vehicle_router.patch("/", status_code=200, 
                     response_model=APIResponse[VehicleResponse],
                     summary="Atualiza um veículo",
                     description="Atualiza informações de um veículo já cadastrado no sistema",
                     operation_id="updateVehicle",
                     responses={
                         201: {"description": "Veículo atualizado com sucesso"},
                         404: {"description": "Veículo com o ID informado não existe"}
                     })
def update_vehicle(id: int, updated_vehicle_data: VehicleUpdate, 
                   service: VehicleService = Depends(get_vehicle_service), 
                   current_user: User = Depends(get_current_user)) -> APIResponse[VehicleResponse]:
    updated_vehicle = service.update_vehicle_service(id, updated_vehicle_data)
    return success_response(updated_vehicle, "Veículo atualizado com sucesso")

@vehicle_router.get("/", status_code=200, 
                    response_model=APIResponse[list[VehicleResponse]],
                    summary="Lista todos os veículos com filtros opcionais",
                    description="Retorna uma lista de todos os veículos já registrados no sistema, com opção de filtros pra veículos ativos e tipo",
                    operation_id="getAllVehicles",
                    responses={
                        200: {"description": "Veículos retornados com sucesso"}
                    })
def get_all_vehicles(type: TipoVeiculo | None = None, 
                           is_active: bool | None = None, 
                           service: VehicleService = Depends(get_vehicle_service),
                           current_user: User = Depends(get_current_user)) -> APIResponse[list[VehicleResponse]]:
    vehicle_list = service.get_all_vehicles_service(type, is_active)
    return success_response(vehicle_list, "Veículos retornados com sucesso")