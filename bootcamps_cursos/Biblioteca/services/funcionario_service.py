class FuncionarioService:
    def __init__(self, conn):
        self.conn = conn

    def adicionar_funcionario(self, nome, cargo):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Funcionario (Nome, Cargo)
                VALUES (%s, %s)
            """, (nome, cargo))
            self.conn.commit()
            print("Funcionário adicionado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao adicionar funcionário: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def atualizar_funcionario(self, id_funcionario, nome=None, cargo=None):
        cursor = self.conn.cursor()
        try:
            updates = []
            params = []
            if nome is not None:
                updates.append("Nome = %s")
                params.append(nome)
            if cargo is not None:
                updates.append("Cargo = %s")
                params.append(cargo)

            if not updates:
                print("Nenhum campo para atualizar foi fornecido.")
                return False

            params.append(id_funcionario)
            update_query = f"UPDATE Funcionario SET {', '.join(updates)} WHERE Id_Funcionario = %s"
            cursor.execute(update_query, params)
            self.conn.commit()
            print("Funcionário atualizado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar funcionário: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def remover_funcionario(self, id_funcionario):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM Funcionario WHERE Id_Funcionario = %s", (id_funcionario,))
            self.conn.commit()
            print("Funcionário removido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao remover funcionário: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def listar_funcionarios(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM Funcionario")
            funcionarios = cursor.fetchall()
            if not funcionarios:
                print("Nenhum funcionário encontrado.")
                return []
            print("\n=== LISTA DE FUNCIONÁRIOS ===")
            for funcionario in funcionarios:
                print(f"ID: {funcionario[0]}, Nome: {funcionario[1]}, Cargo: {funcionario[2]}")
            return funcionarios
        except Exception as e:
            print(f"Erro ao listar funcionários: {e}")
            return []
        finally:
            cursor.close()
