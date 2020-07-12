from .ConnectionFactory import ConnectionFactory
from modelo.grafos import Estacionamento

class EstacionamentoDAO:

    def __init__(self):
        self.session = ConnectionFactory.get_instance().get_session()

    def list_by_coordinates(self, latitude, longitude):
        def __list_by_coordinates_tx(tx, latitude, longitude):
            return tx.run(
                "MATCH (e:Estacionamento) " +
                "WHERE abs(e.latitude - $latitude) < 1 AND abs(e.longitude - $longitude) < 1 " +
                "RETURN e.nome, e.latitude, e.longitude",
                latitude=latitude, longitude=longitude
            )

        records = self.session.read_transaction(__list_by_coordinates_tx, latitude, longitude)
        estacionamentos = []

        for r in records:
            estacionamento = Estacionamento()
            estacionamento.set_nome(r["nome"])
            estacionamento.set_latitude(r["latitude"])
            estacionamento.set_longitude(r["longitude"])
            estacionamentos.append(estacionamento)

        return estacionamentos
