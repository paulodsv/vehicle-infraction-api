from sqlalchemy.orm import Session
from app.schemas.infraction import InfractionQueryCreate, InfractionCreate, InfractionDetailedCreate
from app.models.infraction_queries import InfractionQueries
from app.models.infractions import Infractions

class InfractionRepository():
    def __init__(self, db: Session):
        self.db = db

    def save_query(self, query_data: InfractionQueryCreate) -> InfractionQueries:
        query = InfractionQueries(plate = query_data.plate, total_infractions = query_data.total_infractions, user_id = query_data.user_id)
        self.db.add(query)
        self.db.commit()
        self.db.refresh(query)
        return query
    
    def get_queries_by_user(self, user_id: int) -> InfractionQueries:
        return self.db.query(InfractionQueries).filter(InfractionQueries.user_id == user_id).all()
    
    def get_queries_by_id(self, query_id: int) -> InfractionQueries:
        return self.db.query(InfractionQueries).filter(InfractionQueries.id == query_id).first()
    
    def save_infraction(self, infraction_data: InfractionCreate) -> Infractions:
        infraction = Infractions(
            query_id = infraction_data.query_id,
            plate = infraction_data.plate,
            infraction_notice_number = infraction_data.infraction_notice_number,
            infraction_code = infraction_data.infraction_code,
            description = infraction_data.description,
            infraction_key = infraction_data.infraction_key,
            status = infraction_data.status,
            total_amount = infraction_data.total_amount,
            due_date = infraction_data.due_date
        )
        self.db.add(infraction)
        self.db.commit()
        self.db.refresh(infraction)
        return infraction

    def get_infractions_by_query(self, query_id: int) -> Infractions:
        return self.db.query(Infractions).filter(Infractions.query_id == query_id).all()
    
    def get_infractions_by_plate(self, plate: str) -> Infractions:
        return self.db.query(Infractions).filter(Infractions.plate == plate).all()
    
    def update_infraction_details(self, detailed_infraction: InfractionDetailedCreate, infraction_notice_number: str) -> Infractions:
        infraction = self.db.query(Infractions).filter(Infractions.infraction_notice_number == infraction_notice_number).first()
        infraction.issuing_authority = detailed_infraction.issuing_authority
        infraction.competent_authority = detailed_infraction.competent_authority
        infraction.ait_number = detailed_infraction.ait_number
        infraction.notification_date = detailed_infraction.notification_date
        infraction.defense_deadline = detailed_infraction.defense_deadline
        infraction.offender_indication_deadline = detailed_infraction.offender_indication_deadline
        infraction.driver_name = detailed_infraction.driver_name
        infraction.driver_cnh = detailed_infraction.driver_cnh
        infraction.driver_document = detailed_infraction.driver_document
        infraction.fine_amount = detailed_infraction.fine_amount
        infraction.measurement_taken = detailed_infraction.measurement_taken
        infraction.considered_value = detailed_infraction.considered_value
        infraction.regulated_limit = detailed_infraction.regulated_limit
        infraction.infraction_location = detailed_infraction.infraction_location
        infraction.infraction_date = detailed_infraction.infraction_date
        infraction.infraction_time = detailed_infraction.infraction_time
        infraction.city = detailed_infraction.city
        infraction.state = detailed_infraction.state
        infraction.details_fetched = True
        self.db.commit()
        self.db.refresh(infraction)
        return infraction
    
    def get_infractions_with_no_details(self) -> Infractions:
        infractions = self.db.query(Infractions).filter(Infractions.details_fetched == False).all()
        return infractions