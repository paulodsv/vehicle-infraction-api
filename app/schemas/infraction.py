from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class InfractionResponse(BaseModel):
    id: int
    details_fetched: bool
    plate: str
    infraction_notice_number: str
    infraction_code: str
    description: str
    infraction_key: str
    status: str
    total_amount: float
    due_date: str
    issuing_authority: Optional[str] = None
    competent_authority: Optional[str] = None
    ait_number: Optional[str] = None
    notification_date: Optional[str] = None
    defense_deadline: Optional[str] = None
    offender_indication_deadline: Optional[str] = None
    fine_amount: Optional[str] = None
    measurement_taken: Optional[str] = None
    considered_value: Optional[str] = None
    regulated_limit: Optional[str] = None
    infraction_location: Optional[str] = None
    infraction_date: Optional[str] = None
    infraction_time: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None

    model_config = {"from_attributes": True}

class InfractionQueryResponse(BaseModel):
    id: int
    plate: str
    queried_at: datetime
    total_infractions: int
    user_id: int

    model_config = {"from_attributes": True}

class InfractionCreate(BaseModel):
    plate: str
    infraction_notice_number: str
    infraction_code: str
    description: str
    total_amount: float
    due_date: str
    infraction_key: str
    status: str
    query_id: int

class InfractionQueryCreate(BaseModel):
    user_id: int
    plate: str
    total_infractions: int

class InfractionDetailedCreate(BaseModel):
    issuing_authority: Optional[str] = None
    competent_authority: Optional[str] = None
    ait_number: str
    notification_date: str
    defense_deadline: Optional[str] = None
    offender_indication_deadline: Optional[str] = None
    fine_amount: str
    measurement_taken: Optional[str] = None
    considered_value: Optional[str] = None
    regulated_limit: Optional[str] = None
    infraction_location: str
    infraction_date: str
    infraction_time: str
    city: str
    state: str