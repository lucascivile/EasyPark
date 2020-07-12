from neo4j import GraphDatabase

class ConnectionFactory:

    URI = "bolt://localhost:7687"
    USER = "neo4j"
    PASSWORD = "easypark"
    
    connection_factory = None

    def __init__(self):
        self.driver = GraphDatabase.driver(ConnectionFactory.URI,
                            auth=(ConnectionFactory.USER, ConnectionFactory.PASSWORD))

    def get_session(self):
        return self.driver.session()

    @staticmethod
    def get_instance():
        if ConnectionFactory.connection_factory is None:
            ConnectionFactory.connection_factory = ConnectionFactory()
        return ConnectionFactory.connection_factory
