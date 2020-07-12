class Avaliacao:

    def __init__(self):
        self.cpf_agente = None
        self.resultado = None
        self.comentario = None

    def get_cpf_agente(self):
        return self.cpf_agente

    def set_cpf_agente(self, novo):
        self.cpf_agente = novo

    def get_resultado(self):
        return self.resultado

    def set_resultado(self, novo):
        self.resultado = novo

    def get_comentario(self):
        return self.comentario

    def set_comentario(self, novo):
        self.comentario = novo
        