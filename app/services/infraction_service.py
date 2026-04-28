from app.repositories.infraction_repository import InfractionRepository
from app.models.infractions import Infractions
from app.models.infraction_queries import InfractionQueries
from app.domain.exceptions import UserIdNotFound, QueryIdNotFound, NotRegisteredVehicle
from app.repositories.user_repository import UserRepository 
from app.repositories.vehicle_repository import VehicleRepository

class InfractionService():
    def __init__(self, infraction_repo: InfractionRepository, user_repo: UserRepository, vehicle_repo = VehicleRepository):
        self.infraction_repo = infraction_repo
        self.user_repo = user_repo
        self.vehicle_repo = vehicle_repo

    def get_infractions_by_plate_service(self, plate: str) -> Infractions:
        try_plate = self.vehicle_repo.get_vehicle_by_plate(plate)
        if not try_plate:
            raise NotRegisteredVehicle("Placa informada não cadastrada no sistema")
        return self.infraction_repo.get_infractions_by_plate(plate)

    def get_queries_by_user_id_service(self, user_id: int) -> InfractionQueries:
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise UserIdNotFound("Não existe um usuário com o ID informado")
        return self.infraction_repo.get_queries_by_user(user_id)
    
    def get_infractions_by_query_service(self, query_id: int) -> Infractions:
        infractions = self.infraction_repo.get_infractions_by_query(query_id)
        if not infractions:
            raise QueryIdNotFound("Não existe uma consulta com o ID informado")
        return infractions