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

    def list_by_cpf_motorista(self, cpf):
        cursor = self.connection.cursor()

        sql = "select * from veiculo where cpf_motorista = %s"
        cursor.execute(sql, (cpf,))

        records = cursor.fetchall()
        if records is None:
            return []

        veiculos= []

        for r in records:
            veiculo = Veiculo()
            veiculo.set_placa(r[0])
            veiculo.set_cpf_motorista(r[1])
            veiculo.set_modelo(r[2])
            veiculo.set_ano(r[3])
            veiculo.set_cor(r[4])
            veiculos.append(veiculo)

        cursor.close()
        return veiculos
