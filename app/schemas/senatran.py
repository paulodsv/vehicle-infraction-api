class SenatranInfractionQuery(BaseModel):
    plate: str
    cnpj: str

class SenatranInfractionDetailsQuery(BaseModel):
    plate: str
    cnpj: str
    infraction_key: str