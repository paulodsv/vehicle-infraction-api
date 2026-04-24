from app.gateways.senatran_gateway import SenatranGateway
from app.schemas.infraction import InfractionQueryCreate, InfractionCreate, InfractionDetailedCreate
from app.schemas.senatran import SenatranInfractionQuery, SenatranInfractionDetailsQuery
from app.repositories.infraction_repository import InfractionRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.dtos.senatran.infraction_dto import SenatranResponseDTO
from app.dtos.senatran.details_dto import SenatranDetailsDTO
from app.models.infractions import Infractions
from app.domain.exceptions import NotRegisteredVehicle

class SenatranService():
    def __init__(self, senatran_gateway: SenatranGateway, infraction_repo: InfractionRepository, vehicles_repo: VehicleRepository):
        self.senatran_gateway = senatran_gateway
        self.infraction_repo = infraction_repo
        self.vehicles_repo = vehicles_repo

    def consult_infractions_service(self, query: SenatranInfractionQuery, current_user_id: int) -> list[Infractions]:

        if not query.cnpj:
            plate_cnpj = self.vehicles_repo.get_cnpj_by_plate(query.plate)
            if not plate_cnpj: 
                raise NotRegisteredVehicle("Veículo não cadastrado no sistema. Favor cadastrar antes de realizar qualquer requisição")
            query.cnpj = plate_cnpj

        response: SenatranResponseDTO = self.senatran_gateway.get_infraction_by_plate(query)
        
        #Save da query do respectivo usuário
        infraction_query = InfractionQueryCreate(total_infractions = response.total, 
                                                 plate=query.plate, 
                                                 user_id=current_user_id)
        saved_query = self.infraction_repo.save_query(infraction_query)

        #Save das infrações
        for infraction in response.infractions:
            infraction_create = InfractionCreate(plate = query.plate, 
                                                infraction_notice_number = infraction.notice_number, 
                                                infraction_code = infraction.infraction_code,
                                                description = infraction.description,
                                                total_amount = infraction.total_amount,
                                                due_date = infraction.due_date,
                                                infraction_key = infraction.infraction_key,
                                                status = infraction.status,
                                                query_id = saved_query.id)
            
            self.infraction_repo.save_infraction(infraction_create)
        return self.infraction_repo.get_infractions_by_query(saved_query.id)
    

    def consult_fleet_service(self, current_user_id: int) -> list[Infractions]:
        all_active_vehicles = self.vehicles_repo.get_all_vehicles(is_active=True)

        results = []
        for vehicle in all_active_vehicles:
            query = SenatranInfractionQuery(plate=vehicle.plate, cnpj=vehicle.company_cnpj)
            infractions = self.consult_infractions_service(query, current_user_id)
            results.extend(infractions)
        return results
    
    
    def fetch_infraction_details_service(self) -> int:
        infractions_with_no_details = self.infraction_repo.get_infractions_with_no_details()
        if not infractions_with_no_details:
            return 0
        
        for infraction in infractions_with_no_details:
            cnpj_infraction = self.vehicles_repo.get_cnpj_by_plate(infraction.plate)
            query_details = SenatranInfractionDetailsQuery(plate=infraction.plate, cnpj=cnpj_infraction, infraction_key=infraction.infraction_key)
            details: SenatranDetailsDTO = self.senatran_gateway.get_infraction_details(query_details)

            infraction_detailed = InfractionDetailedCreate(issuing_authority=details.issuing_authority,
                                                           competent_authority=details.competent_authority,
                                                           ait_number=details.ait_number,
                                                           notification_date=details.notification_date,
                                                           defense_deadline=details.defense_deadline,
                                                           offender_indication_deadline=details.offender_indication_deadline,
                                                           driver_name=details.driver_name,
                                                           driver_cnh=details.driver_cnh,
                                                           driver_document=details.driver_document,
                                                           fine_amount=details.fine_amount,
                                                           measurement_taken=details.measurement_taken,
                                                           considered_value=details.considered_value,
                                                           regulated_limit=details.regulated_limit,
                                                           infraction_location=details.infraction_location,
                                                           infraction_date=details.infraction_date,
                                                           infraction_time=details.infraction_time,
                                                           city=details.city,
                                                           state=details.state)
            self.infraction_repo.update_infraction_details(infraction_detailed, infraction.infraction_notice_number)
        return len(infractions_with_no_details)

        