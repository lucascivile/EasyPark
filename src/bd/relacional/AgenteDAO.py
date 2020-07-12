from .ConnectionFactory import ConnectionFactory
from modelo.relacional import Agente

class AgenteDAO:

    def __init__(self):
        self.connection = ConnectionFactory.get_instance().get_connection()

    def insert(self, agente):
        cursor = self.connection.cursor()

        sql = "insert into agente_municipal(cpf_usuario,registro_municipal) values (%s,%s)"
        cursor.execute(sql, (agente.get_cpf_usuario(), agente.get_registro_municipal()))

        self.connection.commit()
        cursor.close()

    def get(self, cpf_usuario):
        cursor = self.connection.cursor()

        sql = "select * from agente_municipal where cpf_usuario=%s"
        cursor.execute(sql, (cpf_usuario,))

        record = cursor.fetchone()
        agente = Agente()

        agente.set_cpf_usuario(record[0])
        agente.set_registro_municipal(record[1])

        cursor.close()
        return agente

    def update(self, agente):
        cursor = self.connection.cursor()

        sql = "update agente_municipal set registro_municipal=%s where cpf_usuario=%s"
        cursor.execute(sql, (agente.get_registro_municipal(), agente.get_cpf_usuario()))

        self.connection.commit()
        cursor.close()
