from .ConnectionFactory import ConnectionFactory
from modelo.grafos import Vaga

class VagaDAO:

    def __init__(self):
        self.session = ConnectionFactory.get_instance().get_session()

    def insert(self, vaga):
        def __insert_vaga_tx(tx, id_vaga, latitude, longitude):
            tx.run(
                "CREATE (:Vaga {id_vaga:$id_vaga, latitude:$latitude, longitude:$longitude}); ",
                id_vaga=id_vaga, latitude=latitude, longitude=longitude
            )

        def __insert_esta_em_tx(tx, id_vaga, bairro):
            tx.run(
                "MATCH (v:Vaga {id_vaga:$id_vaga}), (b:Bairro {nome:$bairro}) " +
                "CREATE (v)-[:ESTA_EM]->(b);",
                id_vaga=id_vaga, bairro=bairro
            )

        self.session.write_transaction(__insert_vaga_tx, vaga.get_id_vaga(), vaga.get_latitude(),
                vaga.get_longitude())
        self.session.write_transaction(__insert_esta_em_tx, vaga.get_id_vaga(), vaga.get_bairro())

    def list_by_agente_bairro(self, agente_cpf):
        def __list_by_agente_cpf_tx(tx, cpf):
            return tx.run(
                "MATCH (:Agente {cpf:$cpf})-[:FISCALIZA]->(:Bairro)<-[:ESTA_EM]-(v:Vaga) " +
                "RETURN v.id_vaga, v.latitude, v.longitude;",
                cpf=cpf
            )

        records = self.session.read_transaction(__list_by_agente_cpf_tx, agente_cpf)
        vagas = []

        for r in records:
            vaga = Vaga()
            vaga.set_id_vaga(r["id_vaga"])
            vaga.set_latitude(r["latitude"])
            vaga.set_longitude(r["longitude"])
            vagas.append(vaga)

        return vagas
