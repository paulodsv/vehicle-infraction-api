class SenatranInfractionDTO:
    def __init__(self, data: dict):
        self.notice_number = data["auto_infracao"]
        self.infraction_code = data["codigo_infracao"]
        self.description = data["descricao"]
        self.total_amount = data["valor_total"]
        self.due_date = data["data_vencimento"]
        self.infraction_key = data["chave_infracao"]
        self.status = data["situacao"]

class SenatranInfractionQueryDTO:
    def __init__(self, data: dict):
        self.total_infractions = data["data"][0]["total_infracoes"]