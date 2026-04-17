from fastapi import APIRouter, Depends
from app.schemas.vehicle import VehicleCreate, TipoVeiculo, VehicleUpdate, VehicleResponse
from app.core.dependencies import get_vehicle_service
from app.services.vehicle_service import VehicleService
from typing import List

vehicle_router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@vehicle_router.post("/", response_model=VehicleResponse,
                     summary="Cadastra um veículo",
                     description="Registra um novo veículo no sistema",
                     operation_id="saveVehicle",
                     responses={
                         201: {"description": "Veículo registrado com sucesso"},
                         409: {"description": "Veículo com essa placa já registrado no sistema"}
                     })
def save_vehicle(vehicle_data: VehicleCreate, service: VehicleService = Depends(get_vehicle_service)):
    return service.save_vehicle_service(vehicle_data)

@vehicle_router.get("/{plate}", response_model=VehicleResponse,
                    summary="Busca um veículo por placa",
                    description="Retorna um veículo cadastrado no sistema pela sua placa",
                    operation_id="getVehicleByPlate",
                    responses={
                        200: {"description": "Veículo retornado com sucesso"},
                        404: {"description": "Placa informada não encontrada no sistema"}
                    })
def get_vehicle_by_plate(plate: str, service: VehicleService = Depends(get_vehicle_service)):
    return service.get_vehicle_by_plate_service(plate)


@vehicle_router.get("/{id}", response_model=VehicleResponse,
                    summary="Busca um veículo por id",
                    description="Retorna um veículo cadastrado no sistema pelo id",
                    operation_id="getVehicleById",
                    responses={
                        200: {"description": "Veículo retornado com sucesso"},
                        404: {"description": "ID informado não encontrado no sistema"}
                    })
def get_vehicle_by_id(id: int, service: VehicleService = Depends(get_vehicle_service)):
    return service.get_vehicle_by_id_service(id)

@vehicle_router.patch("/", response_model=VehicleResponse,
                     summary="Atualiza um veículo",
                     description="Atualiza informações de um veículo já cadastrado no sistema",
                     operation_id="updateVehicle",
                     responses={
                         201: {"description": "Veículo atualizado com sucesso"},
                         404: {"description": "Veículo com o ID informado não existe"}
                     })
def update_vehicle(id: int, updated_vehicle_data: VehicleUpdate, service: VehicleService = Depends(get_vehicle_service)):
    return service.update_vehicle_service(id, updated_vehicle_data)

@vehicle_router.get("/", response_model=List[VehicleResponse],
                    summary="Lista todos os veículos com filtros opcionais",
                    description="Retorna uma lista de todos os veículos já registrados no sistema, com opção de filtros pra veículos ativos e tipo",
                    operation_id="getAllVehicles",
                    responses={
                        200: {"description": "Veículos retornados com sucesso"}
                    })
def get_all_vehicles(type: TipoVeiculo | None = None, 
                           is_active: bool | None = None, 
                           service: VehicleService = Depends(get_vehicle_service)):
    return service.get_all_vehicles_service(type, is_active)