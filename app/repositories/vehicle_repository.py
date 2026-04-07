from sqlalchemy.orm import Session
from app.schemas.vehicle import VehicleCreate
from app.models.vehicle import Vehicle

class VehicleRepository():
    def __init__(self, db: Session):
        self.db = db

    def save_vehicle(self, vehicle_data: VehicleCreate):
        vehicle = Vehicle(plate = vehicle_data.plate, type = vehicle_data.type, company_cnpj = vehicle_data.company_cnpj)
        self.db.add(vehicle)
        self.db.commmit()
        self.db.refresh(vehicle)
        return vehicle