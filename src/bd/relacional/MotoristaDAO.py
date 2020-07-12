from .ConnectionFactory import ConnectionFactory
from modelo.relacional import Motorista

class MotoristaDAO:

    def __init__(self):
        self.connection = ConnectionFactory.get_instance().get_connection()

    def insert(self, motorista):
        cursor = self.connection.cursor()

        sql = "insert into motorista(cnh,cpf_usuario) values (%s,%s)"
        cursor.execute(sql, (motorista.get_cnh(), motorista.get_cpf_usuario()))

        self.connection.commit()
        cursor.close()

    def get(self, cpf_usuario):
        cursor = self.connection.cursor()

        sql = "select * from motorista where cpf_usuario=%s"
        cursor.execute(sql, (cpf_usuario,))

        record = cursor.fetchone()
        motorista = Motorista()

        motorista.set_cpf_usuario(record[0])
        motorista.set_cnh(record[1])

        cursor.close()
        return motorista

    def remove(self, cpf_usuario):
        cursor = self.connection.cursor()

        sql = "delete from motorista where cpf_usuario=%s"
        cursor.execute(sql, (cpf_usuario,))

        self.connection.commit()
        cursor.close()
