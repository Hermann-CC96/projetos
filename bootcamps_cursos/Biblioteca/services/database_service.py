# =============================================================================
# services/database_service.py
# Serviço para operações com banco de dados
# =============================================================================

from config.database import DatabaseConfig
from models.tables import BibliotecaTables

class DatabaseService:
    def __init__(self):
        self.config = DatabaseConfig()
        self.tables_model = BibliotecaTables()
    
    def connect(self):
        conn = self.config.get_connection()
        if conn:
            print("Conectado ao PostgreSQL com sucesso!")
            return conn
        return None
    
    def create_all_tables(self, conn):
        print("\n--- CRIANDO TABELAS ---")
        cursor = conn.cursor()
        
        for table_name, table_sql in self.tables_model.tables.items():
            try:
                print(f"Criando tabela {table_name}: ", end='')
                cursor.execute(table_sql)
                print("OK")
            except Exception as e:
                print(f"Erro: {e}")
        
        conn.commit()
        cursor.close()
    
    def drop_all_tables(self, conn):
        print("\n--- REMOVENDO TABELAS ---")
        cursor = conn.cursor()
        
        for table_name in self.tables_model.drop_order:
            try:
                print(f"Removendo tabela {table_name}: ", end='')
                cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE")
                print("OK")
            except Exception as e:
                print(f"Erro: {e}")
        
        conn.commit()
        cursor.close()
    
    def insert_sample_data(self, conn):
        print("\n--- INSERINDO DADOS DE EXEMPLO ---")
        cursor = conn.cursor()
        
        for table_name, insert_sql in self.tables_model.inserts.items():
            try:
                print(f"Inserindo dados em {table_name}: ", end='')
                cursor.execute(insert_sql)
                print("OK")
            except Exception as e:
                print(f"Erro: {e}")
        
        conn.commit()
        cursor.close()

    def show_table(self, conn, table_name):
        """Consulta e exibe os dados de uma tabela específica."""
        cursor = conn.cursor()
        try:
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            results = cursor.fetchall()
            print(f"\nTABELA {table_name}:")
            for row in results:
                print(row)
        except Exception as e:
            print(f"Erro ao consultar tabela {table_name}: {e}")
        finally:
            cursor.close()

    def update_value(self, conn, table_name, attribute, value, primary_key_column, primary_key_value):
        """Atualiza um valor específico em uma tabela."""
        cursor = conn.cursor()
        try:
            query = f"""
                UPDATE {table_name}
                SET {attribute} = '{value}'
                WHERE {primary_key_column} = {primary_key_value}
            """
            cursor.execute(query)
            print("Atributo atualizado com sucesso.")
        except Exception as e:
            print(f"Erro ao atualizar atributo: {e}")
        finally:
            conn.commit()
            cursor.close()
