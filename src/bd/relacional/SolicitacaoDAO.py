from .ConnectionFactory import ConnectionFactory
from modelo.relacional import Solicitacao

class SolicitacaoDAO:

    def __init__(self):
        self.connection = ConnectionFactory.get_instance().get_connection()

    def insert(self, solicitacao):
        cursor = self.connection.cursor()

        sql = "insert into solicitacao " + \
              "(cpf_motorista,id_vaga,inicio,fim,resposta) " + \
              "values (%s,%s,%s,%s,%s)"
        cursor.execute(sql, (solicitacao.get_cpf_motorista(), solicitacao.get_id_vaga(),
                             solicitacao.get_inicio(), solicitacao.get_fim(), solicitacao.get_resposta()))

        self.connection.commit()
        cursor.close()

    def get(self, id_solicitacao):
        cursor = self.connection.cursor()

        sql = "select * from solicitacao where id_solicitacao=%s"
        cursor.execute(sql, (id_solicitacao,))

        record = cursor.fetchone()
        if record is None:
            return None

        solicitacao = Solicitacao()
        solicitacao.set_id_solicitacao(record[0])
        solicitacao.set_cpf_motorista(record[1])
        solicitacao.set_id_vaga(record[2])
        solicitacao.set_inicio(record[3])
        solicitacao.set_fim(record[4])
        solicitacao.set_resposta(record[5])

        cursor.close()
        return solicitacao

    def update(self, solicitacao):
        cursor = self.connection.cursor()

        sql = "update solicitacao set resposta=%s where id_solicitacao=%s"
        cursor.execute(sql, (solicitacao.get_resposta(), solicitacao.get_id_solicitacao()))

        self.connection.commit()
        cursor.close()

    def list_by_cpf_motorista(self, cpf):
        cursor = self.connection.cursor()

        sql = "select * from solicitacao where cpf_motorista = %s"
        cursor.execute(sql, (cpf,))

        records = cursor.fetchall()
        if records is None:
            return []

        solicitacoes = []

        for r in records:
            solicitacao = Solicitacao()
            solicitacao.set_id_solicitacao(r[0])
            solicitacao.set_cpf_motorista(r[1])
            solicitacao.set_id_vaga(r[2])
            solicitacao.set_inicio(r[3])
            solicitacao.set_fim(r[4])
            solicitacao.set_resposta(r[5])
            solicitacoes.append(solicitacao)

        cursor.close()
        return solicitacoes

    def list_unanswered_by_cpf_proprietario(self, cpf):
        cursor = self.connection.cursor()

        sql = "select * from solicitacao AS s JOIN vaga AS v on s.id_vaga = v.id_vaga " + \
              "where resposta is null and cpf_proprietario = %s"
        cursor.execute(sql, (cpf,))

        records = cursor.fetchall()
        if records is None:
            return []
            
        solicitacoes = []

        for r in records:
            solicitacao = Solicitacao()
            solicitacao.set_id_solicitacao(r[0])
            solicitacao.set_cpf_motorista(r[1])
            solicitacao.set_id_vaga(r[2])
            solicitacao.set_inicio(r[3])
            solicitacao.set_fim(r[4])
            solicitacao.set_resposta(r[5])
            solicitacoes.append(solicitacao)

        cursor.close()
        return solicitacoes
