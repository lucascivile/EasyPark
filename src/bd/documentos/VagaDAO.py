from .ConnectionFactory import ConnectionFactory
from modelo.documentos import Vaga, Acordo, Avaliacao

class VagaDAO:

    def __init__(self):
        self.collection = ConnectionFactory.get_instance().get_collection("vagas")

    def insert(self, vaga):
        self.collection.insert_one({
            "id_vaga": vaga.get_id_vaga(),
            "avaliacoes": [],
            "acordos": []
        })

    def update(self, vaga):
        acordos_formatted = []
        for a in vaga.get_acordos():
            acordos_formatted.append({
                "id_acordo": a.get_id_acordo(),
                "nota_mp": a.get_nota_MP(),
                "nota_pm": a.get_nota_PM()
            })
        self.collection.update_one({"id_vaga": vaga.get_id_vaga()}, {"$set": {"acordos": acordos_formatted}})

        avaliacoes_formatted = []
        for a in vaga.get_avaliacoes():
            avaliacoes_formatted.append({
                "comentario": a.get_comentario(),
                "cpf_agente": a.get_cpf_agente(),
                "resultado": a.get_resultado()
            })
        self.collection.update_one({"id_vaga": vaga.get_id_vaga()}, {"$set": {"avaliacoes": avaliacoes_formatted}})
        
    def get(self, id_vaga):
        doc = self.collection.find_one({"id_vaga": id_vaga})

        vaga = Vaga()
        vaga.set_id_vaga(doc["id_vaga"])

        acordos = []
        for a in doc["acordos"]:
            acordo = Acordo()
            acordo.set_id_acordo(a["id_acordo"])
            acordo.set_nota_MP(a["nota_mp"])
            acordo.set_nota_PM(a["nota_pm"])
            acordos.append(acordo)

        avaliacoes = []
        for a in doc["avaliacoes"]:
            avaliacao = Avaliacao()
            avaliacao.set_comentario(a["comentario"])
            avaliacao.set_cpf_agente(a["cpf_agente"])
            avaliacao.set_resultado(a["resultado"])
            avaliacoes.append(avaliacao)

        vaga.set_acordos(acordos)
        vaga.set_avaliacoes(avaliacoes)
        return vaga
