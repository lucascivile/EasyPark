class Agente:

    def __init__(self):
        self.cpf_usuario = None
        self.registro_municipal = None

    def get_cpf_usuario(self):
        return self.cpf_usuario

    def set_cpf_usuario(self, novo):
        self.cpf_usuario = novo

    def get_registro_municipal(self):
        return self.registro_municipal
    
    def set_registro_municipal(self, novo):
        self.registro_municipal = novo
    