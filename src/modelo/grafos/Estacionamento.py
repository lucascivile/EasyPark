class Estacionamento:

    def __init__(self):
        self.nome = None
        self.latitude = None
        self.longitude = None

    def get_nome(self):
        return self.nome

    def set_nome(self, novo):
        self.nome = novo

    def get_latitude(self):
        return self.latitude
    
    def set_latitude(self, novo):
        self.latitude = novo
    
    def get_longitude(self):
        return self.longitude
    
    def set_longitude(self, novo):
        self.longitude = novo
    