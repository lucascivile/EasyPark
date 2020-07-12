from .ConnectionFactory import ConnectionFactory
from modelo.documentos import Acordo

class AcordoDAO:

    def __init__(self):
        self.usuarios_collection = ConnectionFactory.get_instance().get_collection("usuarios")
        self.vagas_collection = ConnectionFactory.get_instance().get_collection("vagas")

    def insert(self, acordo, cpf_proprietario, cpf_motorista, id_vaga):
        acordos_proprietario = self.usuarios_collection.find_one({"cpf", cpf_proprietario})["acordos"]
        acordos_proprietario.append({
            "id_acordo": acordo.get_id_acordo(),
            "nota_mp": acordo.get_nota_mp(),
            "nota_pm": acordo.get_nota_pm()
        })
        self.usuarios_collection.update_one({"cpf", cpf_proprietario}, {"$set": {"acordos": acordos_proprietario}})

        acordos_motorista = self.usuarios_collection.find_one({"cpf", cpf_motorista})["acordos"]
        acordos_motorista.append({
            "id_acordo": acordo.get_id_acordo(),
            "nota_mp": acordo.get_nota_mp(),
            "nota_pm": acordo.get_nota_pm()
        })
        self.usuarios_collection.update_one({"cpf", cpf_motorista}, {"$set": {"acordos": acordos_motorista}})

        acordos_vaga = self.vagas_collection.find_one({"id_vaga", id_vaga})["acordos"]
        acordos_vaga.append({
            "id_acordo": acordo.get_id_acordo(),
            "nota_mp": acordo.get_nota_mp(),
            "nota_pm": acordo.get_nota_pm()
        })
        self.vagas_collection.update_one({"id_vaga", id_vaga}, {"$set": {"acordos": acordos_vaga}})

    def update(self, acordo, cpf_proprietario, cpf_motorista, id_vaga):
        acordos_proprietario = self.usuarios_collection.find_one({"cpf", cpf_proprietario})["acordos"]
        acordos_proprietario_novo = [a for a in acordos_proprietario if a["id_acordo"] != acordo.get_id_acordo()]
        acordos_proprietario_novo.append({
            "id_acordo": acordo.get_id_acordo(),
            "nota_mp": acordo.get_nota_mp(),
            "nota_pm": acordo.get_nota_pm()
        })
        self.usuarios_collection.update_one({"cpf", cpf_proprietario}, {"$set": {"acordos": acordos_proprietario_novo}})

        acordos_motorista = self.usuarios_collection.find_one({"cpf", cpf_motorista})["acordos"]
        acordos_motorista_novo = [a for a in acordos_motorista if a["id_acordo"] != acordo.get_id_acordo()]
        acordos_motorista_novo.append({
            "id_acordo": acordo.get_id_acordo(),
            "nota_mp": acordo.get_nota_mp(),
            "nota_pm": acordo.get_nota_pm()
        })
        self.usuarios_collection.update_one({"cpf", cpf_motorista}, {"$set": {"acordos": acordos_motorista_novo}})

        acordos_vaga= self.usuarios_collection.find_one({"id_vaga", id_vaga})["acordos"]
        acordos_vaga_novo = [a for a in acordos_vaga if a["id_acordo"] != acordo.get_id_acordo()]
        acordos_vaga_novo.append({
            "id_acordo": acordo.get_id_acordo(),
            "nota_mp": acordo.get_nota_mp(),
            "nota_pm": acordo.get_nota_pm()
        })
        self.usuarios_collection.update_one({"id_vaga", id_vaga}, {"$set": {"acordos": acordos_vaga_novo}})

    def get(self, id_acordo):
        for u in self.usuarios_collection.find():
            for a in u["acordos"]:
                if a["id_acordo"] == id_acordo:
                    acordo = Acordo()
                    acordo.set_id_acordo(a["id_acordo"])
                    acordo.set_nota_MP(a["nota_mp"])
                    acordo.set_nota_PM(a["nota_pm"])
                    return acordo
        return None
