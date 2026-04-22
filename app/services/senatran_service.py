from app.gateways.senatran_gateway import SenatranGateway
from app.schemas.infraction import InfractionQueryCreate, InfractionCreate, InfractionDetailedCreate
from app.schemas.senatran import SenatranInfractionQuery, SenatranInfractionDetailsQuery
from app.repositories.infraction_repository import InfractionRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.dtos.senatran.infraction_dto import SenatranInfractionDTO, SenatranInfractionQueryDTO
from app.dtos.senatran.details_dto import SenatranDetailsDTO
from app.models.infractions import Infractions
from app.domain.exceptions import NotRegisteredVehicle

class SenatranService():
    def __init__(self, senatran_gateway: SenatranGateway, infraction_repo: InfractionRepository, vehicles_repo: VehicleRepository):
        self.senatran_gateway = senatran_gateway
        self.infraction_repo = infraction_repo
        self.vehicles_repo = vehicles_repo

    def consult_infractions_service(self, query: SenatranInfractionQuery, current_user_id: int) -> Infractions:

        if not query.cnpj:
            plate_cnpj = self.vehicles_repo.get_cnpj_by_plate(query.plate)
            if not plate_cnpj: 
                raise NotRegisteredVehicle("Veículo não cadastrado no sistema. Favor informar o cnpj correspondente")
            query.cnpj = plate_cnpj

        infractions = self.senatran_gateway.get_infraction_by_plate(query)
        if not infractions["data"]:
            raise Exception(infractions["errors"][0])
        
        #Save da query do respectivo usuário
        query_dto = SenatranInfractionQueryDTO(infractions)
        infraction_query = InfractionQueryCreate(total_infractions = query_dto.total_infractions, 
                                                 plate=query.plate, 
                                                 user_id=current_user_id)
        saved_query = self.infraction_repo.save_query(infraction_query)

        #Save das infrações
        for infraction in infractions["data"][0]["infracoes"]:
            dto = SenatranInfractionDTO(infraction)

            infraction_create = InfractionCreate(plate = query.plate, 
                                                infraction_notice_number = dto.notice_number, 
                                                infraction_code = dto.infraction_code,
                                                description = dto.description,
                                                total_amount = dto.total_amount,
                                                due_date = dto.due_date,
                                                infraction_key = dto.infraction_key,
                                                status = dto.status,
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
    
    
    def fetch_infraction_details(self) -> int | None:
        infractions_with_no_details = self.infraction_repo.get_infractions_with_no_details()

        for infraction in infractions_with_no_details:
            cnpj_infraction = self.vehicles_repo.get_cnpj_by_plate(infraction.plate)
            query_details = SenatranInfractionDetailsQuery(plate=infraction.plate, cnpj=cnpj_infraction, infraction_key=infraction.infraction_key)
            details = self.senatran_gateway.get_infraction_details(query_details)
            dto = SenatranDetailsDTO(details)

            infraction_detailed = InfractionDetailedCreate(issuing_authority=dto.issuing_authority,
                                                           competent_authority=dto.competent_authority,
                                                           ait_number=dto.ait_number,
                                                           notification_date=dto.notification_date,
                                                           defense_deadline=dto.defense_deadline,
                                                           offender_indication_deadline=dto.offender_indication_deadline,
                                                           driver_name=dto.driver_name,
                                                           driver_cnh=dto.driver_cnh,
                                                           driver_document=dto.driver_document,
                                                           fine_amount=dto.fine_amount,
                                                           measurement_taken=dto.measurement_taken,
                                                           considered_value=dto.considered_value,
                                                           regulated_limit=dto.regulated_limit,
                                                           infraction_location=dto.infraction_location,
                                                           infraction_date=dto.infraction_date,
                                                           infraction_time=dto.infraction_time,
                                                           city=dto.city,
                                                           state=dto.state)
            self.infraction_repo.update_infraction_details(infraction_detailed, infraction.infraction_notice_number)
        return len(infractions_with_no_details)

        