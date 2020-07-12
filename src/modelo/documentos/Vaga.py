class Vaga:

    def __init__(self):
        self.id_vaga = None
        self.acordos = None
        self.avaliacoes = None

    def get_id_vaga(self):
        return self.id_vaga

    def set_id_vaga(self, novo):
        self.id_vaga = novo

    def get_acordos(self):
        return self.acordos

    def set_acordos(self, novo):
        self.acordos = novo

    def get_avaliacoes(self):
        return self.avaliacoes

    def set_avaliacoes(self, novo):
        self.avaliacoes = novo
        