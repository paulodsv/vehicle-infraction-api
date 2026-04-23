from pydantic import BaseModel, field_validator
from typing import Optional

class SenatranInfractionQuery(BaseModel):
    plate: str
    cnpj: Optional[str] = None

    @field_validator("plate")
    @classmethod
    def validate_plate(cls, v: str) -> str:
        v = v.upper().replace("-", "").strip()
        if len(v) not in (7, 8):
            raise ValueError("Placa deve ter 7 ou 8 caracteres (ex: ABC1234 ou ABC1D23)")
        return v
    
    @field_validator("cnpj")
    @classmethod
    def validate_cnpj(cls, v: str) -> str:
        if v is None:
            return v
        v = v.strip().replace(".", "").replace("/", "").replace("-", "")
        if len(v) != 14:
            raise ValueError("CNPJ deve ter 14 dígitos")
        return v

class SenatranInfractionDetailsQuery(BaseModel):
    plate: str
    cnpj: str
    infraction_key: str