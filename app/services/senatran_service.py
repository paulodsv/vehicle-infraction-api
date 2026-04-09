from app.gateways.senatran_gateway import SenatranGateway
from app.schemas.infraction import InfractionQueryCreate, InfractionCreate
from app.schemas.senatran import SenatranInfractionQuery
from app.repositories.infraction_repository import InfractionRepository
from app.repositories.vehicle_repository import VehicleRepository

class SenatranService():
    def __init__(self, senatran_gateway: SenatranGateway, infraction_repo: InfractionRepository, vehicles_repo: VehicleRepository):
        self.senatran_gateway = senatran_gateway
        self.infraction_repo = infraction_repo
        self.vehicles_repo = vehicles_repo

    def consult_infractions_service(self, query: SenatranInfractionQuery, current_user_id: int):

        # ------------------------- QUERY CREATE -----------------------------
        infractions = self.senatran_gateway.get_infraction_by_plate(query)
        infraction_query = InfractionQueryCreate(total_infractions = infractions["data"][0]["total_infracoes"], plate=query.plate, user_id=current_user_id)
        saved_query = self.infraction_repo.save_query(infraction_query)

        # ------------------------ SAVE INFRACTION ---------------------------
        for infraction in infractions["data"][0]["infracoes"]:
            infraction_create = InfractionCreate(plate = query.plate, 
                                                infraction_notice_number = infraction["auto_infracao"], 
                                                infraction_code = infraction["codigo_infracao"],
                                                description = infraction["descricao"],
                                                total_amount = infraction["valor_total"],
                                                due_date = infraction["data_vencimento"],
                                                infraction_key = infraction["chave_infracao"],
                                                status = infraction["situacao"],
                                                query_id = saved_query.id)
            
            self.infraction_repo.save_infraction(infraction_create)
        
        return self.infraction_repo.get_infractions_by_query(saved_query.id)
    
    def consult_fleet_service(self, current_user_id: int):
        all_active_vehicles = self.vehicles_repo.get_all_active_vehicles()

        results = []
        for vehicle in all_active_vehicles:
            query = SenatranInfractionQuery(plate=vehicle.plate, cnpj=vehicle.company_cnpj)
            infractions = self.consult_infractions_service(query, current_user_id)
            results.extend(infractions)
        return results