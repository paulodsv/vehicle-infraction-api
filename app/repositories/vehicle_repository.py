from sqlalchemy.orm import Session
from app.schemas.vehicle import VehicleCreate, VehicleUpdate
from app.models.vehicle import Vehicle

class VehicleRepository():
    def __init__(self, db: Session):
        self.db = db

    def save_vehicle(self, vehicle_data: VehicleCreate):
        vehicle = Vehicle(plate = vehicle_data.plate, type = vehicle_data.type, company_cnpj = vehicle_data.company_cnpj)
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle
    
    def get_vehicle_by_plate(self, plate: str):
        return self.db.query(Vehicle).filter(Vehicle.plate == plate).first()
    
    def get_vehicles_by_type(self, type: str):
        return self.db.query(Vehicle).filter(Vehicle.type == type).all()
    
    def get_vehicle_by_id(self, id: int):
        return self.db.query(Vehicle).filter(Vehicle.id == id).first()
    
    def update_vehicle(self, id: int, vehicle_data: VehicleUpdate):
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

    def get_all_active_vehicles(self):
        return self.db.query(Vehicle).filter(Vehicle.is_active == True).all()
    
    def get_all_vehicles(self):
        return self.db.query(Vehicle).all()