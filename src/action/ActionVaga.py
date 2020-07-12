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
        vagasAsString = []
            
        try:
            vagas = vagaDAO.list_free_by_location_and_time(user_cpf, latitude, longitude, inicio, fim)
            
            for v in vagas:
                vagaAsString = "id_vaga: " + str(v.get_id_vaga()) + "\n" + \
                               "latitude: " + str(v.get_latitude()) + "\n" + \
                               "longitude: " + str(v.get_longitude()) + "\n" + \
                               "largura: " + str(v.get_largura()) + "\n" + \
                               "comprimento: " + str(v.get_comprimento())
                
                vagasAsString.append(vagaAsString)
        except:
            return None

        if len(vagaAsString):
            return vagasAsString
        else:
            estacionamentoDAOGrafos = EstacionamentoDAOGrafos()
            estacionamentos = estacionamentoDAOGrafos.list_by_coordinates(latitude, longitude)
            estacionamentosAsString = []

            for e in estacionamentos:
                estacionamentoAsString = "nome: " + str(e.get_nome()) + "\n" + \
                                         "latitude: " + str(v.get_latitude()) + "\n" + \
                                         "longitude: " + str(v.get_longitude())
                
                estacionamentosAsString.append(estacionamentoAsString)

            return estacionamentosAsString

    @staticmethod
    def list_by_agente_bairro(cpf):
        vagaDAOGrafos = VagaDAOGrafos()
        vagasAsString = []

        try:
            vagas = vagaDAOGrafos.list_by_agente_bairro(cpf)

            for v in vagas:
                vagaAsString = "id_vaga: " + str(v.get_id_vaga()) + "\n" + \
                               "latitude: " + str(v.get_latitude()) + "\n" + \
                               "longitude: " + str(v.get_longitude())
                
                vagasAsString.append(vagaAsString)
        except:
            return None
        else:
            return vagasAsString

    @staticmethod  
    def insert_avaliacao(id_vaga, cpf_agente, avaliacao, comentario):
        vagaDAOdoc = VagaDAO()

        try:
            vagaDoc = vagaDAOdoc.get(id_vaga)
            avaliacoes = vagaDoc.getAvaliacoes()

            novaAvaliacao = AvaliacaoDoc()
            novaAvaliacao.set_cpf_agente(cpf_agente)
            novaAvaliacao.set_comentario(comentario)
            novaAvaliacao.set_resultado(avaliacao)

            avaliacoes.append(novaAvaliacao)
            vagaDoc.set_avaliacoes(avaliacoes)

            vagaDAOdoc.update(vagaDoc)
        except:
            return False
        else:
            return True
