from .ConnectionFactory import ConnectionFactory
from modelo.documentos import Usuario

class UsuarioDAO:

    def __init__(self):
        self.collection = ConnectionFactory.get_instance().get_collection("usuarios")

    def insert(self, usuario):
        self.collection.insert_one({
            "cpf": usuario.get_cpf(),
            "acordos": []
        })
