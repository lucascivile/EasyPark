class Proprietario:

    def __init__(self):
        self.cpf_usuario = None
        self.logradouro = None
        self.numero = None
        self.complemento = None
        self.cep = None

    def get_cpf_usuario(self):
        return self.cpf_usuario

    def set_cpf_usuario(self, novo):
        self.cpf_usuario = novo

    def get_logradouro(self):
        return self.logradouro
    
    def set_logradouro(self, novo):
        self.logradouro = novo
    
    def get_numero(self):
        return self.numero
    
    def set_numero(self, novo):
        self.numero = novo

    def get_complemento(self):
        return self.complemento
    
    def set_complemento(self, novo):
        self.complemento = novo
    
    def get_cep(self):
        return self.cep
    
    def set_cep(self, novo):
        self.cep = novo
    