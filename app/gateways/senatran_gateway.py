from app.core.config import settings
import httpx
from app.schemas.senatran import SenatranInfractionDetailsQuery, SenatranInfractionQuery
from app.dtos.senatran.infraction_dto import SenatranInfractionDTO, SenatranResponseDTO
from app.dtos.senatran.details_dto import SenatranDetailsDTO
from app.gateways.exceptions import ExternalServiceError

class SenatranGateway():
    def __init__(self):
        self.token = settings.INFOSIMPLES_TOKEN
        self.gov_cpf = settings.GOV_CPF
        self.gov_senha = settings.GOV_SENHA
        self.base_infractions_url = settings.INFOSIMPLES_INFRACTIONS_URL
        self.base_infractions_details_url = settings.INFOSIMPLES_DETAILS_URL

    def get_infraction_by_plate(self, query: SenatranInfractionQuery):
        response = httpx.post(self.base_infractions_url, data={"token": self.token, 
                                                      "placa": query.plate, 
                                                      "cnpj": query.cnpj, 
                                                      "login_cpf": self.gov_cpf, 
                                                      "login_senha": self.gov_senha}, 
                                                      timeout=45.0)
        data = response.json()

        if data.get("errors"):
            raise ExternalServiceError(data["errors"][0])
        
        raw = data["data"][0]

        infractions = [
            SenatranInfractionDTO(item)
            for item in raw["infracoes"]
        ]

        total = raw["total_infracoes"]

        return SenatranResponseDTO(infractions, total)
    
    def get_infraction_details(self, query: SenatranInfractionDetailsQuery):
        details = httpx.post(self.base_infractions_details_url, data={"token": self.token, 
                                                                      "chave_infracao": query.infraction_key, 
                                                                      "placa": query.plate,
                                                                      "cnpj": query.cnpj, 
                                                                      "login_cpf": self.gov_cpf,
                                                                      "login_senha": self.gov_senha},
                                                                      timeout=45.0)
        response = details.json()
        raw = response["data"][0]
        details_dto = SenatranDetailsDTO(raw)
        
        return details_dto