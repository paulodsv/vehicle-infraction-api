from app.repositories.vehicle_repository import VehicleRepository
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, TipoVeiculo, VehicleUpdate
from app.domain.exceptions import AlreadyRegisteredVehicle, NotRegisteredVehicle

class VehicleService():
    def __init__(self, vehicle_repo: VehicleRepository):
        self.vehicle_repo = vehicle_repo
    
    def save_vehicle_service(self, vehicle_data: VehicleCreate) -> Vehicle:
        vehicle = self.vehicle_repo.get_vehicle_by_plate(vehicle_data.plate)
        if vehicle:
            raise AlreadyRegisteredVehicle("Já existe um veículo cadastrado com a placa informada")
        
        return self.vehicle_repo.save_vehicle(vehicle_data)
    
    def get_vehicle_by_plate_service(self, plate: str) -> Vehicle:
        vehicle = self.vehicle_repo.get_vehicle_by_plate(plate)
        if not vehicle:
            raise NotRegisteredVehicle("Veículo com a placa informada não cadastrado no sistema")
        
        return vehicle           
    
    def get_vehicle_by_id_service(self, id: int) -> Vehicle:
        vehicle = self.vehicle_repo.get_vehicle_by_id(id)
        if not vehicle:
            raise NotRegisteredVehicle("Veículo com o id informado não cadastrado no sistema")
        
        return vehicle
    
    def update_vehicle_service(self, id: int, vehicle_data: VehicleUpdate) -> Vehicle:
        vehicle = self.vehicle_repo.get_vehicle_by_id(id)
        if not vehicle:
            raise NotRegisteredVehicle("Veículo com o id informado não cadastrado no sistema")
        
        return self.vehicle_repo.update_vehicle(id, vehicle_data)
    
    def get_all_vehicles_service(self, type: TipoVeiculo | None = None, is_active: bool | None = None) -> list[Vehicle]:
        return self.vehicle_repo.get_all_vehicles(type, is_active)
    