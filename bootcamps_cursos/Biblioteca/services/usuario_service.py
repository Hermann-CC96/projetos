class UsuarioService:
    def __init__(self, conn):
        self.conn = conn

    def adicionar_usuario(self, nome, cpf, telefone, email, tipo_usuario, id_categoria):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Usuario (Nome, CPF, Telefone, Email, Tipo_Usuario, Id_Categoria)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nome, cpf, telefone, email, tipo_usuario, id_categoria))
            self.conn.commit()
            print("Usuário adicionado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao adicionar usuário: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def atualizar_usuario(self, id_usuario, nome=None, telefone=None, email=None, tipo_usuario=None, id_categoria=None):
        cursor = self.conn.cursor()
        try:
            updates = []
            params = []
            if nome is not None:
                updates.append("Nome = %s")
                params.append(nome)
            if telefone is not None:
                updates.append("Telefone = %s")
                params.append(telefone)
            if email is not None:
                updates.append("Email = %s")
                params.append(email)
            if tipo_usuario is not None:
                updates.append("Tipo_Usuario = %s")
                params.append(tipo_usuario)
            if id_categoria is not None:
                updates.append("Id_Categoria = %s")
                params.append(id_categoria)

            if not updates:
                print("Nenhum campo para atualizar foi fornecido.")
                return False

            params.append(id_usuario)
            update_query = f"UPDATE Usuario SET {', '.join(updates)} WHERE Id_Usuario = %s"
            cursor.execute(update_query, params)
            self.conn.commit()
            print("Usuário atualizado com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao atualizar usuário: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def remover_usuario(self, id_usuario):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM Usuario WHERE Id_Usuario = %s", (id_usuario,))
            self.conn.commit()
            print("Usuário removido com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao remover usuário: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def listar_usuarios(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM Usuario")
            usuarios = cursor.fetchall()
            if not usuarios:
                print("Nenhum usuário encontrado.")
                return []
            print("\n=== LISTA DE USUÁRIOS ===")
            for usuario in usuarios:
                print(f"ID: {usuario[0]}, Nome: {usuario[1]}, CPF: {usuario[2]}, Telefone: {usuario[3]}, Email: {usuario[4]}, Tipo: {usuario[5]}, Categoria ID: {usuario[7]}")
            return usuarios
        except Exception as e:
            print(f"Erro ao listar usuários: {e}")
            return []
        finally:
            cursor.close()

    def buscar_usuario_por_id(self, id_usuario):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM Usuario WHERE Id_Usuario = %s", (id_usuario,))
            usuario = cursor.fetchone()
            if not usuario:
                print("Usuário não encontrado.")
                return None
            print(f"ID: {usuario[0]}, Nome: {usuario[1]}, CPF: {usuario[2]}, Telefone: {usuario[3]}, Email: {usuario[4]}, Tipo: {usuario[5]}, Categoria ID: {usuario[7]}")
            return usuario
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            return None
        finally:
            cursor.close()
