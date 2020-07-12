class Acordo:

    def __init__(self):
        self.id_acordo = None
        self.nota_PM = None
        self.nota_MP = None

    def get_id_acordo(self):
        return self.id_acordo

    def set_id_acordo(self, novo):
        self.id_acordo = novo

    def get_nota_PM(self):
        return self.nota_PM
    
    def set_nota_PM(self, novo):
        self.nota_PM = novo
    
    def get_nota_MP(self):
        return self.nota_MP
    
    def set_nota_MP(self, novo):
        self.nota_MP = novo
    