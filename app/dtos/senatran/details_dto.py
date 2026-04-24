class SenatranDetailsDTO:
    def __init__(self, data: dict):
        autuacao = data.get("autuacao") or {}
        self.issuing_authority = autuacao.get("orgao_autuador")
        self.competent_authority = autuacao.get("orgao_competente")
        self.ait_number = autuacao.get("numero_ait")
        self.notification_date = autuacao.get("data_notificacao")
        self.defense_deadline = autuacao.get("data_limite_defesa")
        self.offender_indication_deadline = autuacao.get("data_limite_indicacao_infrator")

        condutor = data.get("condutor") or {}
        self.driver_name = condutor.get("nome")
        self.driver_cnh = condutor.get("cnh")
        self.driver_document = condutor.get("documento")

        infracao = data.get("infracao") or {}
        self.fine_amount = infracao.get("valor_multa")
        self.measurement_taken = infracao.get("medicao_realizada")
        self.considered_value = infracao.get("valor_considerado")
        self.regulated_limit = infracao.get("limite_regulamentado")

        local_data_hora = data.get("local_data_hora")
        self.infraction_location = local_data_hora.get("local_infracao")
        self.infraction_date = local_data_hora.get("data_infracao")
        self.infraction_time = local_data_hora.get("hora_infracao") 
        self.city = local_data_hora.get("municipio")
        self.state = local_data_hora.get("uf")
