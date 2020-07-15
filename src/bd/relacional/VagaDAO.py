from .ConnectionFactory import ConnectionFactory
from modelo.relacional import Vaga

class VagaDAO:

    def __init__(self):
        self.connection = ConnectionFactory.get_instance().get_connection()

    def insert(self, vaga):
        cursor = self.connection.cursor()

        sql = "insert into vaga " + \
              "(cpf_proprietario,latitude,longitude,largura,comprimento,preco_hora) " +\
              "values (%s,%s,%s,%s,%s,%s) returning id_vaga"
        cursor.execute(sql, (vaga.get_cpf_proprietario(),
                             vaga.get_latitude(), vaga.get_longitude(), vaga.get_largura(),
                             vaga.get_comprimento(), vaga.get_preco()))

        id_vaga = cursor.fetchone()[0]

        self.connection.commit()
        cursor.close()
        return id_vaga

    def get(self, id_vaga):
        cursor = self.connection.cursor()

        sql = "select * from vaga where id_vaga=%s"
        cursor.execute(sql, (id_vaga,))

        record = cursor.fetchone()
        if record is None:
            return None

        vaga = Vaga()
        vaga.set_id_vaga(record[0])
        vaga.set_cpf_proprietario(record[1])
        vaga.set_preco(record[2])
        vaga.set_latitude(record[3])
        vaga.set_longitude(record[4])
        vaga.set_largura(record[5])
        vaga.set_comprimento(record[6])
        vaga.set_liberada(record[7])

        cursor.close()
        return vaga

    def update(self, vaga):
        cursor = self.connection.cursor()

        sql = "update vaga set liberada=%s where id_vaga=%s"
        cursor.execute(sql, (vaga.get_liberada(), vaga.get_id_vaga()))

        self.connection.commit()
        cursor.close()

    def list_free_by_location_and_time(self, user_cpf, latitude, longitude, inicio, fim):
        cursor = self.connection.cursor()

        sql = "select * " + \
              "from vaga " + \
              "where cpf_proprietario != %s and ABS(latitude - %s) < 1 and ABS(longitude - %s) < 1 " + \
              "and not exists ( " + \
              " select * from acordo as a join solicitacao as s " + \
              " on a.id_solicitacao = s.id_solicitacao " + \
              " where s.id_vaga = vaga.id_vaga and " + \
              " ((inicio <= %s and inicio >= %s) or (fim <= %s and fim  >= %s)))"
        cursor.execute(sql, (user_cpf, latitude, longitude, fim, inicio, fim, inicio))

        records = cursor.fetchall()
        if records is None:
            return []

        vagas = []

        for r in records:
            vaga = Vaga()
            vaga.set_id_vaga(r[0])
            vaga.set_cpf_proprietario(r[1])
            vaga.set_preco(r[2])
            vaga.set_latitude(r[3])
            vaga.set_longitude(r[4])
            vaga.set_largura(r[5])
            vaga.set_comprimento(r[6])
            vaga.set_liberada(r[7])
            vagas.append(vaga)


        cursor.close()
        return vagas
        