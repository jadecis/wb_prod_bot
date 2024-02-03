import pymysql

class Database():
    def __init__(self, host, port, password, name, user):
        self.connection= pymysql.Connection(
            
        )