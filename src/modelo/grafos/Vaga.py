class Vaga:

    def __init__(self):
        self.id_vaga = None
        self.bairro = None
        self.latitude = None
        self.longitude = None

    def get_id_vaga(self):
        return self.id_vaga

    def set_id_vaga(self, novo):
        self.id_vaga = novo

    def get_bairro(self):
        return self.bairro

    def set_bairro(self, novo):
        self.bairro = novo

    def get_latitude(self):
        return self.latitude
    
    def set_latitude(self, novo):
        self.latitude = novo
    
    def get_longitude(self):
        return self.longitude
    
    def set_longitude(self, novo):
        self.longitude = novo
    