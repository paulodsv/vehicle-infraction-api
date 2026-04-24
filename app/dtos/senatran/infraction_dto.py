class SenatranInfractionDTO:
    def __init__(self, data: dict):
        self.notice_number = data.get("auto_infracao")
        self.infraction_code = data.get("codigo_infracao")
        self.description = data.get("descricao")
        self.total_amount = data.get("valor_total")
        self.due_date = data.get("data_vencimento")
        self.infraction_key = data.get("chave_infracao")
        self.status = data.get("situacao")

class SenatranResponseDTO:
    def __init__(self, infractions: list[SenatranInfractionDTO], total: int):
        self.infractions = infractions
        self.total = total