from modelo.relacional import Vaga
from modelo.documentos import Vaga as VagaDoc
from modelo.documentos import Avaliacao as AvaliacaoDoc
from modelo.grafos import Vaga as VagaGrafos
from bd.documentos import VagaDAO as VagaDAODoc
from bd.grafos import VagaDAO as VagaDAOGrafos
from bd.grafos import EstacionamentoDAO as EstacionamentoDAOGrafos
from bd.relacional import VagaDAO

class ActionVaga:

    @staticmethod
    def insert(cpf, bairro, latitude, longitude, largura, comprimento, preco):
        vagaDAO = VagaDAO()   
        vaga = Vaga()

        vaga.set_cpf_proprietario(cpf)
        vaga.set_latitude(latitude)
        vaga.set_longitude(longitude)
        vaga.set_largura(largura)
        vaga.set_comprimento(comprimento)
        vaga.set_preco(preco)

        vagaDAODoc = VagaDAODoc()        
        vagaDoc = VagaDoc()

        vagaDAOGrafos = VagaDAOGrafos()
        vagaGrafos = VagaGrafos()
        vagaGrafos.set_bairro(bairro)
        vagaGrafos.set_latitude(latitude)
        vagaGrafos.set_longitude(longitude)

        try:
            id_vaga = vagaDAO.insert(vaga)

            vagaDoc.set_id_vaga(id_vaga)
            vagaDAODoc.insert(vagaDoc)

            vagaGrafos.set_id_vaga(id_vaga)
            vagaDAOGrafos.insert(vagaGrafos)
        except:
            return False
        else:
            return True

    @staticmethod
    def list_by_location_and_time(user_cpf, inicio, fim, latitude, longitude):
        vagaDAO = VagaDAO()
        vagas_output = []
            
        try:
            vagas = vagaDAO.list_free_by_location_and_time(user_cpf, latitude, longitude, inicio, fim)
            
            for v in vagas:
                vaga = {"id_vaga": v.get_id_vaga(), "latitude": v.get_latitude(),
                                      "longitude": v.get_longitude(), "largura": v.get_largura(),
                                      "comprimento": v.get_comprimento(), "preco": v.get_preco()}
                
                vagas_output.append(vaga)
        except:
            return None, None

        if len(vagas_output):
            return vagas_output, True
        else:
            estacionamentoDAOGrafos = EstacionamentoDAOGrafos()
            estacionamentos = estacionamentoDAOGrafos.list_by_coordinates(latitude, longitude)
            estacionamentos_output = []

            for e in estacionamentos:
                estacionamento = {"nome": e.get_nome(), "latitude": e.get_latitude(),
                                                "longitude": e.get_longitude()}
                
                estacionamentos_output.append(estacionamento)

            return estacionamentos_output, False

    @staticmethod
    def list_by_agente_bairro(cpf):
        vagaDAOGrafos = VagaDAOGrafos()
        vagas_output = []

        try:
            vagas = vagaDAOGrafos.list_by_agente_bairro(cpf)

            for v in vagas:
                vaga = {"id_vaga": v.get_id_vaga(), "latitude": v.get_latitude(),
                                      "longitude": v.get_longitude()}
                
                vagas_output.append(vaga)
        except:
            return None
        else:
            return vagas_output

    @staticmethod  
    def insert_avaliacao(id_vaga, cpf_agente, avaliacao, comentario):
        vagaDAO = VagaDAO()
        vagaDAOdoc = VagaDAODoc()

        try:
            if avaliacao:
                vaga = vagaDAO.get(id_vaga)
                vaga.set_liberada(avaliacao)
                vagaDAO.update(vaga)

            vagaDoc = vagaDAOdoc.get(id_vaga)
            avaliacoes = vagaDoc.get_avaliacoes()

            novaAvaliacao = AvaliacaoDoc()
            novaAvaliacao.set_cpf_agente(cpf_agente)
            novaAvaliacao.set_comentario(comentario)
            novaAvaliacao.set_resultado(avaliacao)
            
            avaliacoes.append(novaAvaliacao)
            vagaDoc.set_avaliacoes(avaliacoes)
            vagaDAOdoc.update(vagaDoc)
        except Exception:
            return False
        else:
            return True
