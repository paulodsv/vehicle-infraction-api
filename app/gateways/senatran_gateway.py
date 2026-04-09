from app.core.config import settings
import httpx
from app.schemas.senatran import SenatranInfractionDetailsQuery, SenatranInfractionQuery

class SenatranGateway():
    def __init__(self):
        self.token = settings.INFOSIMPLES_TOKEN
        self.gov_cpf = settings.GOV_CPF
        self.gov_senha = settings.GOV_SENHA
        self.base_infractions_url = "https://api.infosimples.com/api/v2/consultas/senatran/infracoes"
        self.base_infractions_details_url = "https://api.infosimples.com/api/v2/consultas/senatran/download-infracao"

    def get_infraction_by_plate(self, query: SenatranInfractionQuery):
        infractions = httpx.post(self.base_infractions_url, data={"token": self.token, 
                                                      "placa": query.plate, 
                                                      "cnpj": query.cnpj, 
                                                      "login_cpf": self.gov_cpf, 
                                                      "login_senha": self.gov_senha})
        response = infractions.json()
        return response
    
    def get_infraction_details(self, query: SenatranInfractionDetailsQuery):
        details = httpx.post(self.base_infractions_details_url, data={"token": self.token, 
                                                                      "chave_infracao": query.infraction_key, 
                                                                      "placa": query.plate,
                                                                      "cnpj": query.cnpj})
        response = details.json()
        return response