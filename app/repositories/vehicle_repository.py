from sqlalchemy.orm import Session
from app.schemas.vehicle import VehicleCreate, VehicleUpdate
from app.models.vehicle import Vehicle

class VehicleRepository():
    def __init__(self, db: Session):
        self.db = db

    def save_vehicle(self, vehicle_data: VehicleCreate) -> Vehicle:
        vehicle = Vehicle(plate = vehicle_data.plate, 
                          type = vehicle_data.type, 
                          company_cnpj = vehicle_data.company_cnpj)
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle
    
    def get_vehicle_by_plate(self, plate: str) -> Vehicle:
        return self.db.query(Vehicle).filter(Vehicle.plate == plate).first()
    
    def get_vehicle_by_id(self, id: int) -> Vehicle:
        return self.db.query(Vehicle).filter(Vehicle.id == id).first()
    
    def update_vehicle(self, id: int, vehicle_data: VehicleUpdate) -> Vehicle:
        vehicle = self.get_vehicle_by_id(id)

        if vehicle_data.type is not None:
            vehicle.type = vehicle_data.type
        
        if vehicle_data.company_cnpj is not None:
            vehicle.company_cnpj = vehicle_data.company_cnpj

        if vehicle_data.is_active is not None:
            vehicle.is_active = vehicle_data.is_active
            
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle
    
    def get_all_vehicles(self, 
                         type: str | None = None, 
                         is_active: bool | None = None) -> list[Vehicle]:
        query = self.db.query(Vehicle)
        if type:
            query = query.filter(Vehicle.type == type)
        if is_active:
            query = query.filter(Vehicle.is_active == is_active)
        return query.all()
    
    def get_cnpj_by_plate(self, plate: str) -> str | None:
        vehicle = self.db.query(Vehicle).filter(Vehicle.plate == plate).first()
        if vehicle:
            return vehicle.company_cnpj
        return None