from .ConnectionFactory import ConnectionFactory
from modelo.grafos import Vaga

class VagaDAO:

    def __init__(self):
        self.session = ConnectionFactory.get_instance().get_session()

    def insert(self, vaga):
        def __insert_bairro_if_not_exists(tx, bairro):
            tx.run("MERGE (:Bairro {nome:$bairro});")

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

        self.session.write_transaction(__insert_bairro_if_not_exists, vaga.get_bairro())
        self.session.write_transaction(__insert_vaga_tx, vaga.get_id_vaga(), vaga.get_latitude(),
                vaga.get_longitude())
        self.session.write_transaction(__insert_esta_em_tx, vaga.get_id_vaga(), vaga.get_bairro())

    def list_by_agente_bairro(self, agente_cpf):
        def __list_by_agente_cpf_tx(tx, cpf):
            result = tx.run(
                "MATCH (:Agente {cpf:$cpf})-[:FISCALIZA]->(:Bairro)<-[:ESTA_EM]-(v:Vaga) " +
                "RETURN v.id_vaga as id_vaga, v.latitude as latitude, v.longitude as longitude;",
                cpf=cpf
            )
            return [r for r in result]

        records = self.session.read_transaction(__list_by_agente_cpf_tx, agente_cpf)
        vagas = []

        for r in records:
            vaga = Vaga()
            vaga.set_id_vaga(r["id_vaga"])
            vaga.set_latitude(r["latitude"])
            vaga.set_longitude(r["longitude"])
            vagas.append(vaga)

        return vagas
