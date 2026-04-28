from typing import Literal, Optional

from pydantic import BaseModel, field_validator

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
    
    @field_validator("company_cnpj")
    @classmethod
    def validate_cnpj(cls, v: str) -> str:
        v = v.strip().replace(".", "").replace("/", "").replace("-", "")
        if len(v) != 14:
            raise ValueError("CNPJ deve ter 14 dígitos")
        return v
    
    @field_validator("type", mode="before")
    @classmethod
    def validate_type(cls, v: str) -> str:
        return v.lower().strip()

class VehicleUpdate(BaseModel):
    type: Optional[TipoVeiculo] = None
    company_cnpj: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("company_cnpj")
    @classmethod
    def validate_cnpj(cls, v: str) -> str:
        if v is None:
            return v
        v = v.strip().replace(".", "").replace("/", "").replace("-", "")
        if len(v) != 14:
            raise ValueError("CNPJ deve ter 14 dígitos")
        return v
    
    @field_validator("type", mode="before")
    @classmethod
    def validate_type(cls, v: str) -> str:
        if v is None:
            return v
        return v.lower().strip()

class VehicleResponse(VehicleCreate):
    id: int
    is_active: bool

    model_config = {"from_attributes": True}