class Veiculo:

    def __init__(self):
        self.cpf_motorista = None
        self.modelo = None
        self.ano = None
        self.cor = None
        self.placa = None

    def get_cpf_motorista(self):
        return self.cpf_motorista

    def set_cpf_motorista(self, novo):
        self.cpf_motorista = novo

    def get_modelo(self):
        return self.modelo
    
    def set_modelo(self, novo):
        self.modelo = novo
    
    def get_ano(self):
        return self.ano
    
    def set_ano(self, novo):
        self.ano = novo

    def get_cor(self):
        return self.cor
    
    def set_cor(self, novo):
        self.cor = novo
    
    def get_placa(self):
        return self.placa
    
    def set_placa(self, novo):
        self.placa = novo
    