from .ActionAcordo import ActionAcordo
from modelo.relacional import Solicitacao
from bd.relacional import SolicitacaoDAO

class ActionSolicitacao:

    @staticmethod
    def insert(id_vaga, cpf_motorista, inicio, fim):
        solicitacaoDAO = SolicitacaoDAO()
        solicitacao = Solicitacao()

        solicitacao.set_cpf_motorista(cpf_motorista)
        solicitacao.set_id_vaga(id_vaga)
        solicitacao.set_inicio(inicio)
        solicitacao.set_fim(fim)

        try:
            solicitacaoDAO.insert(solicitacao)
        except:
            return False
        else:
            return True

    @staticmethod
    def list_by_motorista(cpf):
        solicitacaoDAO = SolicitacaoDAO()
        solicitacoesAsString = []
            
        try:
            solicitacoes = solicitacaoDAO.listByCpfMotorista(cpf)

            for s in solicitacoes:
                solicitacaoAsString = "id_solicitacao" + str(s.get_id_solicitacao()) + "\n" + \
                                      "id_vaga" + str(s.get_id_vaga()) + "\n" + \
                                      "inicio" + str(s.get_inicio()) + "\n" + \
                                      "fim" + str(s.get_fim())

                resposta = s.get_resposta()
                if resposta is not None:
                    solicitacaoAsString += "\nresposta: " + ("aceita" if resposta else "recusada")
                
                solicitacoesAsString.append(solicitacaoAsString)
        except:
            return None
        else:
            return solicitacoesAsString

    @staticmethod
    def list_unanswered_by_proprietario(cpf):
        solicitacaoDAO = SolicitacaoDAO()
        solicitacoesAsString = []

        try:
            solicitacoes = solicitacaoDAO.list_unanswered_by_cpf_proprietario(cpf)

            for s in solicitacoes:
                solicitacaoAsString = "id_solicitacao" + str(s.get_id_solicitacao()) + "\n" + \
                                      "id_vaga" + str(s.get_id_vaga()) + "\n" + \
                                      "inicio" + str(s.get_inicio()) + "\n" + \
                                      "fim" + str(s.get_fim())

                solicitacoesAsString.append(solicitacaoAsString)
        except:
            return None
        else:
            return solicitacoesAsString

    @staticmethod
    def update_resposta(id_solicitacao, cpf_proprietario, resposta):
        solicitacaoDAO = SolicitacaoDAO()

        try:
            solicitacao = solicitacaoDAO.get(id_solicitacao)
            solicitacao.set_resposta(resposta)
            solicitacaoDAO.update(solicitacao)

            if resposta:
                ActionAcordo.insert(id_solicitacao, cpf_proprietario, solicitacao.get_cpf_motorista())
        except:
            return False
        else:
            return True
