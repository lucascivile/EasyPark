class Usuario:

    def __init__(self):
        self.cpf = None
        self.nome = None
        self.email = None
        self.senha = None
        self.nascimento = None

    def get_cpf(self):
        return self.cpf

    def set_cpf(self, novo):
        self.cpf = novo

    def get_nome(self):
        return self.nome
    
    def set_nome(self, novo):
        self.nome = novo
    
    def get_email(self):
        return self.email
    
    def set_email(self, novo):
        self.email = novo

    def get_senha(self):
        return self.senha
    
    def set_senha(self, novo):
        self.senha = novo
    
    def get_nascimento(self):
        return self.nascimento
    
    def set_nascimento(self, novo):
        self.nascimento = novo
    