class Usuario:

    def __init__(self):
        self.cpf = None
        self.acordos = None

    def get_cpf(self):
        return self.cpf

    def set_cpf(self, novo):
        self.cpf = novo

    def get_acordos(self):
        return self.acordos

    def set_acordos(self, novo):
        self.acordos = novo
        