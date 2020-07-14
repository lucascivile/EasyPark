import psycopg2

class ConnectionFactory:

    HOST = "localhost"
    DB = "ep3"
    USER = "ep3_relacional"
    PORT = 5432
    PASSWORD = "ep3_relacional"
    
    connection_factory = None

    def __init__(self):
        self.connection = psycopg2.connect(host=ConnectionFactory.HOST, database=ConnectionFactory.DB,
                                           user=ConnectionFactory.USER, password=ConnectionFactory.PASSWORD,
                                           port=ConnectionFactory.PORT)

    def get_connection(self):
        return self.connection

    @staticmethod
    def get_instance():
        if ConnectionFactory.connection_factory is None:
            ConnectionFactory.connection_factory = ConnectionFactory()
        return ConnectionFactory.connection_factory
        