# =============================================================================
# config/database.py
# Configuração de conexão com PostgreSQL
# =============================================================================
import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.database = os.getenv('DB_NAME', 'biblioteca')
        self.user = os.getenv('DB_USER', 'postgres')
        self.password = os.getenv('DB_PASSWORD', 'root')
        self.port = os.getenv('DB_PORT', '5432')
    
    def get_connection(self):
        try:
            connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            return connection
        except Error as e:
            print(f"Erro ao conectar ao PostgreSQL: {e}")
            return None