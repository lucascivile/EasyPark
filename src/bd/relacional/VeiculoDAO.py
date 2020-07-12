from .ConnectionFactory import ConnectionFactory
from modelo.relacional import Veiculo

class VeiculoDAO:

    def __init__(self):
        self.connection = ConnectionFactory.get_instance().get_connection()

    def insert(self, veiculo):
        cursor = self.connection.cursor()

        sql = "insert into veiculo (cpf_motorista,modelo,ano,cor,placa) values (%s,%s,%s,%s,%s)"
        cursor.execute(sql, (veiculo.get_cpf_motorista(), veiculo.get_modelo(), veiculo.get_ano(),
                             veiculo.get_cor(), veiculo.get_placa()))

        self.connection.commit()
        cursor.close()
