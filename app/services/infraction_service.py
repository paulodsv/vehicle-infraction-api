from app.repositories.infraction_repository import InfractionRepository
from app.models.infractions import Infractions
from app.models.infraction_queries import InfractionQueries

class InfractionService():
    def __init__(self, infraction_repo: InfractionRepository):
        self.infraction_repo = infraction_repo

    def get_infractions_by_plate_service(self, plate: str) -> Infractions:
        return self.infraction_repo.get_infractions_by_plate(plate)

    def get_queries_by_user_id_service(self, user_id: int) -> InfractionQueries:
        return self.infraction_repo.get_queries_by_user(user_id)
    
    def get_infractions_by_query_service(self, query_id: int) -> Infractions:
        return self.infraction_repo.get_infractions_by_query(query_id)