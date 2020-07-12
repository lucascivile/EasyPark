from .ConnectionFactory import ConnectionFactory
from modelo.relacional import Acordo

class AcordoDAO:

    def __init__(self):
        self.connection = ConnectionFactory.get_instance().get_connection()

    def insert(self, acordo):
        cursor = self.connection.cursor()

        sql = "insert into acordo(id_solicitacao) values (%s) returning id_acordo"
        cursor.execute(sql, (acordo.get_id_solicitacao()))

        id_acordo = cursor.fetchone()[0]

        self.connection.commit()
        cursor.close()
        return id_acordo

    def get(self, id_acordo):
        cursor = self.connection.cursor()

        sql = "select * from acordo where id_acordo=%s"
        cursor.execute(sql, (id_acordo,))

        record = cursor.fetchone()
        acordo = Acordo()

        acordo.set_id_acordo(record[0])
        acordo.set_id_solicitacao(record[1])

        cursor.close()
        return acordo

    def list(self):
        cursor = self.connection.cursor()

        sql = "select * from acordo"
        cursor.execute(sql)

        records = cursor.fetchall()
        acordos = []

        for r in records:
            acordo = Acordo()
            acordo.set_id_acordo(r[0])
            acordo.set_id_solicitacao(r[1])
            acordos.append(acordo)

        cursor.close()
        return acordos
