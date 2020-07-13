from .ConnectionFactory import ConnectionFactory
from modelo.relacional import Proprietario

class ProprietarioDAO:

    def __init__(self):
        self.connection = ConnectionFactory.get_instance().get_connection()

    def insert(self, proprietario):
        cursor = self.connection.cursor()

        sql = "insert into proprietario" + \
              "(cpf_usuario,endereco_logradouro,endereco_numero,endereco_complemento,endereco_cep) " + \
              "values (%s,%s,%s,%s,%s)"
        cursor.execute(sql, (proprietario.get_cpf_usuario(), proprietario.get_logradouro(),
                             proprietario.get_numero(), proprietario.get_complemento(),
                             proprietario.get_cep()))

        self.connection.commit()
        cursor.close()

    def get(self, cpf_usuario):
        cursor = self.connection.cursor()

        sql = "select * from proprietario where cpf_usuario=%s"
        cursor.execute(sql, (cpf_usuario,))

        record = cursor.fetchone()
        if record is None:
            return None
            
        proprietario = Proprietario()
        proprietario.set_cpf_usuario(record[0])
        proprietario.set_logradouro(record[1])
        proprietario.set_numero(record[2])
        proprietario.set_complemento(record[3])
        proprietario.set_cep(record[4])

        cursor.close()
        return proprietario

    def update(self, proprietario):
        cursor = self.connection.cursor()

        sql = "update proprietario set endereco_logradouro=%s, endereco_numero=%s, "+ \
              "endereco_complemento=%s, endereco_cep=%s where cpf_usuario=%s"
        cursor.execute(sql, (proprietario.get_logradouro(), proprietario.get_numero(),
                             proprietario.get_complemento(), proprietario.get_cep(),
                             proprietario.get_cpf_usuario()))

        self.connection.commit()
        cursor.close()