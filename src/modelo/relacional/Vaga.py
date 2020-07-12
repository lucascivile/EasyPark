class Vaga:

    def __init__(self):
        self.id_vaga = None
        self.cpf_proprietario = None
        self.liberada = None
        self.latitude = None
        self.longitude = None
        self.largura = None
        self.comprimento = None
        self.preco = None

    def get_id_vaga(self):
        return self.id_vaga

    def set_id_vaga(self, novo):
        self.id_vaga = novo

    def get_cpf_proprietario(self):
        return self.cpf_proprietario
    
    def set_cpf_proprietario(self, novo):
        self.cpf_proprietario = novo
    
    def get_liberada(self):
        return self.liberada
    
    def set_liberada(self, novo):
        self.liberada = novo

    def get_latitude(self):
        return self.latitude
    
    def set_latitude(self, novo):
        self.latitude = novo
    
    def get_longitude(self):
        return self.longitude
    
    def set_longitude(self, novo):
        self.longitude = novo

    def get_largura(self):
        return self.largura
    
    def set_largura(self, novo):
        self.largura = novo

    def get_comprimento(self):
        return self.comprimento

    def set_comprimento(self, novo):
        self.comprimento = novo

    def get_preco(self):
        return self.preco

    def set_preco(self, novo):
        self.preco = novo
    