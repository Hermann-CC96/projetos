class LivroService:
    def __init__(self, conn):
        self.conn = conn
    def adicionar_livro(self, titulo, ano_publicacao, id_editora, id_categoria, quantidade_exemplares):
        cursor = self.conn.cursor()
        try:
           
            status_inicial = 'disponível' if quantidade_exemplares > 0 else 'indisponível'
            
            cursor.execute("""
                INSERT INTO Livro (Titulo, Status, Ano_Publicacao, Id_Editora, Id_Categoria, Quantidade_Exemplares)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (titulo, status_inicial, ano_publicacao, id_editora, id_categoria, quantidade_exemplares))
            
            self.conn.commit()
            print(f"Livro adicionado com sucesso! Status: {status_inicial}")
            return True
            
        except Exception as e:
            print(f"Erro ao adicionar livro: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def atualizar_livro(self, id_livro, titulo=None, status=None, ano_publicacao=None, id_editora=None, id_categoria=None, quantidade_exemplares=None):
        cursor = self.conn.cursor()
        try:
           
            updates = []
            params = []

            if titulo is not None:
                updates.append("Titulo = %s")
                params.append(titulo)
            if status is not None:
                updates.append("Status = %s")
                params.append(status)
            if ano_publicacao is not None:
                updates.append("Ano_Publicacao = %s")
                params.append(ano_publicacao)
            if id_editora is not None:
                updates.append("Id_Editora = %s")
                params.append(id_editora)
            if id_categoria is not None:
                updates.append("Id_Categoria = %s")
                params.append(id_categoria)
            if quantidade_exemplares is not None:
                updates.append("Quantidade_Exemplares = %s")
                params.append(quantidade_exemplares)

            if not updates:
                print("Nenhum campo para atualizar foi fornecido.")
                return False

            params.append(id_livro)
            update_query = f"UPDATE Livro SET {', '.join(updates)} WHERE Id_Livro = %s"

            cursor.execute(update_query, params)
            self.conn.commit()
            print("Livro atualizado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar livro: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def atualizar_status_livro(self, id_livro, status):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                UPDATE Livro SET Status = %s WHERE Id_Livro = %s
            """, (status, id_livro))
            self.conn.commit()
            print("Status do livro atualizado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar status do livro: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def remover_livro(self, id_livro):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM Livro WHERE Id_Livro = %s", (id_livro,))
            self.conn.commit()
            print("Livro removido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao remover livro: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def atualizar_quantidade_exemplares(self, id_livro, quantidade_exemplares):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                UPDATE Livro SET Quantidade_Exemplares = %s WHERE Id_Livro = %s
            """, (quantidade_exemplares, id_livro))
            self.conn.commit()
            print("Quantidade de exemplares atualizada com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar quantidade de exemplares: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()
   
    def listar_livros(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT Id_Livro, Titulo, Status, Ano_Publicacao, Id_Editora, Id_Categoria, Quantidade_Exemplares
                FROM Livro
                ORDER BY Id_Livro ASC
            """)
            livros = cursor.fetchall()
            return livros
        except Exception as e:
            print(f"Erro ao listar livros: {e}")
            return []
        finally:
            cursor.close()
   
    def buscar_livro_por_id(self, id_livro):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM Livro WHERE Id_Livro = %s", (id_livro,))
            livro = cursor.fetchone()
            return livro
        except Exception as e:
            print(f"Erro ao buscar livro: {e}")
            return None
        finally:
            cursor.close()