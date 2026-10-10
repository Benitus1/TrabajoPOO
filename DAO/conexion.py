import pymysql

class Conexion:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'ecotech_db',
            'port': 3306,
            'cursorclass': pymysql.cursors.DictCursor
        }

    def conectar(self):
        return pymysql.connect(**self.config)
