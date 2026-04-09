from app.repositories.infraction_repository import InfractionRepository

class InfractionService():
    def __init__(self, infraction_repo: InfractionRepository):
        self.infraction_repo = infraction_repo

    def get_infractions_by_plate_service(self, plate: str):
        return self.infraction_repo.get_infractions_by_plate(plate)

    def get_queries_by_user_id(self, user_id: int):
        return self.infraction_repo.get_queries_by_user(user_id)
    
    def get_infractions_by_query(self, query_id: int):
        return self.infraction_repo.get_infractions_by_query(query_id)