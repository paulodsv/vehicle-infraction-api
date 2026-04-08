from pydantic import BaseModel, field_validator
from typing import Optional, Literal

TipoVeiculo = Literal["cavalo", "carreta", "passeio"]

class VehicleCreate(BaseModel):
    plate: str
    type: TipoVeiculo
    company_cnpj: str

    @field_validator("plate")
    @classmethod
    def validate_plate(cls, v: str) -> str:
        v = v.upper().replace("-", "").strip()
        if len(v) not in (7, 8):
            raise ValueError("Placa deve ter 7 ou 8 caracteres (ex: ABC1234 ou ABC1D23)")
        return v

class VehicleUpdate(BaseModel):
    type: Optional[str] = None
    company_cnpj: Optional[str] = None
    is_active: Optional[bool] = None

class VehicleResponse(VehicleCreate):
    id: int
    is_active: bool

    model_config = {"from_attributes": True}