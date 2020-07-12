from pymongo import MongoClient

class ConnectionFactory:

    HOST = "localhost"
    PORT = 27017
    DB = "easypark"

    connection_factory = None

    def __init__(self):
        self.database = MongoClient(ConnectionFactory.HOST, ConnectionFactory.PORT)[ConnectionFactory.DB]

    def get_collection(self, name):
        return self.database[name]
    
    @staticmethod
    def get_instance():
        if ConnectionFactory.connection_factory is None:
            ConnectionFactory.connection_factory = ConnectionFactory()
        return ConnectionFactory.connection_factory
