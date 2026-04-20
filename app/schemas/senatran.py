from pydantic import BaseModel
from typing import Optional

class SenatranInfractionQuery(BaseModel):
    plate: str
    cnpj: Optional[str] = None

class SenatranInfractionDetailsQuery(BaseModel):
    plate: str
    cnpj: str
    infraction_key: str