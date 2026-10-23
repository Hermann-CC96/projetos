class AutorService:
    def __init__(self, conn):
        self.conn = conn

    def adicionar_autor(self, nome):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Autor (Nome)
                VALUES (%s)
            """, (nome,))
            self.conn.commit()
            print("Autor adicionado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao adicionar autor: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def atualizar_autor(self, id_autor, nome=None):
        cursor = self.conn.cursor()
        try:
            if nome is None:
                print("Nenhum campo para atualizar foi fornecido.")
                return False

            cursor.execute("""
                UPDATE Autor
                SET Nome = %s
                WHERE Id_Autor = %s
            """, (nome, id_autor))
            self.conn.commit()
            print("Autor atualizado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar autor: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def remover_autor(self, id_autor):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM Autor WHERE Id_Autor = %s", (id_autor,))
            self.conn.commit()
            print("Autor removido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao remover autor: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def listar_autores(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM Autor")
            autores = cursor.fetchall()
            if not autores:
                print("Nenhum autor encontrado.")
                return []
            print("\n=== LISTA DE AUTORES ===")
            for autor in autores:
                print(f"ID: {autor[0]}, Nome: {autor[1]}")
            return autores
        except Exception as e:
            print(f"Erro ao listar autores: {e}")
            return []
        finally:
            cursor.close()
