class Agente:

    def __init__(self):
        self.cpf = None
        self.bairro = None

    def get_cpf(self):
        return self.cpf

    def set_cpf(self, novo):
        self.cpf = novo

    def get_bairro(self):
        return self.bairro
    
    def set_bairro(self, novo):
        self.bairro = novo
