class Motorista:

    def __init__(self):
        self.cpf_usuario = None
        self.cnh = None

    def get_cpf_usuario(self):
        return self.cpf_usuario

    def set_cpf_usuario(self, novo):
        self.cpf_usuario = novo

    def get_cnh(self):
        return self.cnh
    
    def set_cnh(self, novo):
        self.cnh = novo
    