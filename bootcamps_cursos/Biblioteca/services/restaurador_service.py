class RestauradorService:
    def __init__(self, conn):
        self.conn = conn

    def adicionar_restaurador(self, nome, data_restaurador):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Restaurador (Nome, Data_Restaurador)
                VALUES (%s, %s)
            """, (nome, data_restaurador))
            self.conn.commit()
            print("Restaurador adicionado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao adicionar restaurador: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def remover_restaurador(self, id_restaurador):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM Restaurador WHERE Id_Restaurador = %s", (id_restaurador,))
            self.conn.commit()
            print("Restaurador removido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao remover restaurador: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def atualizar_restaurador(self, id_restaurador, nome=None, data_restaurador=None):
        cursor = self.conn.cursor()
        try:
            updates = []
            params = []
            if nome is not None:
                updates.append("Nome = %s")
                params.append(nome)
            if data_restaurador is not None:
                updates.append("Data_Restaurador = %s")
                params.append(data_restaurador)

            if not updates:
                print("Nenhum campo para atualizar foi fornecido.")
                return False

            params.append(id_restaurador)
            update_query = f"UPDATE Restaurador SET {', '.join(updates)} WHERE Id_Restaurador = %s"
            cursor.execute(update_query, params)
            self.conn.commit()
            print("Restaurador atualizado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar restaurador: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def listar_restauradores(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM Restaurador")
            restauradores = cursor.fetchall()
            if not restauradores:
                print("Nenhum restaurador encontrado.")
                return []
            print("\n=== LISTA DE RESTAURADORES ===")
            for restaurador in restauradores:
                print(f"ID: {restaurador[0]}, Nome: {restaurador[1]}, Data: {restaurador[2]}")
            return restauradores
        except Exception as e:
            print(f"Erro ao listar restauradores: {e}")
            return []
        finally:
            cursor.close()
