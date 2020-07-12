class Solicitacao:

    def __init__(self):
        self.id_solicitacao = None
        self.cpf_motorista = None
        self.id_vaga = None
        self.inicio = None
        self.fim = None
        self.resposta = None

    def get_id_solicitacao(self):
        return self.id_solicitacao

    def set_id_solicitacao(self, novo):
        self.id_solicitacao = novo

    def get_cpf_motorista(self):
        return self.cpf_motorista
    
    def set_cpf_motorista(self, novo):
        self.cpf_motorista = novo
    
    def get_id_vaga(self):
        return self.id_vaga
    
    def set_id_vaga(self, novo):
        self.id_vaga = novo

    def get_inicio(self):
        return self.inicio
    
    def set_inicio(self, novo):
        self.inicio = novo
    
    def get_fim(self):
        return self.fim
    
    def set_fim(self, novo):
        self.fim = novo

    def get_resposta(self):
        return self.resposta
    
    def set_resposta(self, novo):
        self.resposta = novo
    