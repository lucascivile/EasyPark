from .ConnectionFactory import ConnectionFactory
from modelo.relacional import Usuario

class UsuarioDAO:

    def __init__(self):
        self.connection = ConnectionFactory.get_instance().get_connection()

    def insert(self, usuario):
        cursor = self.connection.cursor()

        sql = "insert into usuario (cpf,nome,email,senha,data_nascimento) values (%s,%s,%s,%s,%s)"
        cursor.execute(sql, (usuario.get_cpf(), usuario.get_nome(), usuario.get_email(),
                             usuario.get_senha(), usuario.get_nascimento()))

        self.connection.commit()
        cursor.close()

    def get(self, email, senha):
        cursor = self.connection.cursor()
        
        sql = "select * from usuario where email=%s and senha=%s"
        cursor.execute(sql, (email, senha))

        record = cursor.fetchone()
        if record is None:
            return None
            
        usuario = Usuario()
        usuario.set_cpf(record[0])
        usuario.set_nome(record[1])
        usuario.set_email(record[2])
        usuario.set_senha(record[3])
        usuario.set_nascimento(record[4])

        cursor.close()
        return usuario

    def remove(self, cpf):
        cursor = self.connection.cursor()

        sql = "delete from usuario where cpf=%s"
        cursor.execute(sql, (cpf,))

        self.connection.commit()
        cursor.close()
