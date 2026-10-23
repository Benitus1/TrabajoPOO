import os
import pymysql

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


class Conexion:
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'ecotech_db'),
            'port': int(os.getenv('DB_PORT', '3306')),
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }

    def conectar(self):
        return pymysql.connect(**self.config)
