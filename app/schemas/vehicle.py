from pydantic import BaseModel
from typing import Optional

class VehicleCreate(BaseModel):
    plate: str
    type: str
    company_cnpj: str

class VehicleUpdate(BaseModel):
    type: Optional[str] = None
    company_cnpj: Optional[str] = None
    is_active: Optional[bool] = None

class VehicleResponse(VehicleCreate):
    id: int
    is_active: bool

    model_config = {"from_attributes": True}