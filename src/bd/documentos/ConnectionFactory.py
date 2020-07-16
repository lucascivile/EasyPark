from pymongo import MongoClient

class ConnectionFactory:

    HOST = "localhost"
    PORT = 27017
    DB = "easypark"
    USERNAME = "ep3_documento"
    PASSWORD = "ep3_documento"

    connection_factory = None

    def __init__(self):
        self.database = MongoClient(ConnectionFactory.HOST, ConnectionFactory.PORT, username=ConnectionFactory.USERNAME, password=ConnectionFactory.PASSWORD)[ConnectionFactory.DB]

    def get_collection(self, name):
        return self.database[name]
    
    @staticmethod
    def get_instance():
        if ConnectionFactory.connection_factory is None:
            ConnectionFactory.connection_factory = ConnectionFactory()
        return ConnectionFactory.connection_factory
