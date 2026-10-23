class CoAutorService:
    def __init__(self, conn):
        self.conn = conn

    def adicionar_co_autor(self, id_livro, id_autor, data_publicacao):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Co_Autor (Id_Livro, Id_Autor, Data_Publicacao)
                VALUES (%s, %s, %s)
            """, (id_livro, id_autor, data_publicacao))
            self.conn.commit()
            print("Co-autor adicionado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao adicionar co-autor: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def remover_co_autor(self, id_livro, id_autor):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM Co_Autor WHERE Id_Livro = %s AND Id_Autor = %s", (id_livro, id_autor))
            self.conn.commit()
            print("Co-autor removido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao remover co-autor: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def atualizar_co_autor(self, id_livro, id_autor, data_publicacao=None):
        cursor = self.conn.cursor()
        try:
            updates = []
            params = []
            if data_publicacao is not None:
                updates.append("Data_Publicacao = %s")
                params.append(data_publicacao)

            if not updates:
                print("Nenhum campo para atualizar foi fornecido.")
                return False

            params.extend([id_livro, id_autor])
            update_query = f"UPDATE Co_Autor SET {', '.join(updates)} WHERE Id_Livro = %s AND Id_Autor = %s"
            cursor.execute(update_query, params)
            self.conn.commit()
            print("Co-autor atualizado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar co-autor: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def listar_co_autores(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM Co_Autor")
            co_autores = cursor.fetchall()
            if not co_autores:
                print("Nenhum co-autor encontrado.")
                return []
            print("\n=== LISTA DE CO-AUTORES ===")
            for co_autor in co_autores:
                print(f"ID Livro: {co_autor[0]}, ID Autor: {co_autor[1]}, Data Publicação: {co_autor[2]}")
            return co_autores
        except Exception as e:
            print(f"Erro ao listar co-autores: {e}")
            return []
        finally:
            cursor.close()
