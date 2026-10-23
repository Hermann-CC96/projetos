# =============================================================================
# services/comentario_service.py
# Serviço para gerenciar comentários e resenhas
# =============================================================================
from datetime import datetime
class ComentarioService:
    def __init__(self, conn):
        self.conn = conn
    def adicionar_comentario(self, id_usuario, id_livro, texto):
        cursor = self.conn.cursor()
        try:
            # Verificar se o usuário já leu o livro
            cursor.execute("""
                SELECT 1 FROM Emprestimo
                WHERE Id_Usuario = %s AND Id_Livro = %s AND Devolvido = TRUE
            """, (id_usuario, id_livro))
            
            if not cursor.fetchone():
                print("Você precisa ter lido o livro para comentar.")
                return False
            
            # Adicionar comentário
            cursor.execute("""
                INSERT INTO Comentario (Id_Usuario, Id_Livro, Texto)
                VALUES (%s, %s, %s)
            """, (id_usuario, id_livro, texto))
            
            # Deixe apenas o PontuacaoService cuidar dos pontos
            
            self.conn.commit()
            print("Comentário adicionado com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao adicionar comentário: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()
    
    def listar_comentarios_livro(self, id_livro):
        """Lista todos os comentários de um livro específico."""
        cursor = self.conn.cursor()
        try:
            # Consulta SQL ajustada para usar o nome correto da tabela
            cursor.execute("""
                SELECT c.Id_Comentario, u.Nome, c.Texto, c.Data_Comentario
                FROM Comentario c
                JOIN Usuario u ON c.Id_Usuario = u.Id_Usuario
                WHERE c.Id_Livro = %s
                ORDER BY c.Data_Comentario DESC
            """, (id_livro,))

            comentarios = cursor.fetchall()

            if not comentarios:
                print("Nenhum comentário encontrado para este livro.")
                return

            print(f"\nComentários para o Livro ID {id_livro}:")
            for comentario in comentarios:
                print(f"ID Comentário: {comentario[0]}, Usuário: {comentario[1]}, Data: {comentario[3]}")
                print(f"Comentário: {comentario[2]}\n")

        except Exception as e:
            print(f"Erro ao listar comentários: {e}")
        finally:
            cursor.close()

    def adicionar_resenha(self, id_usuario, id_livro, resenha):
        cursor = self.conn.cursor()
        try:
            # Verificar se o usuário já leu o livro
            cursor.execute("""
                SELECT 1 FROM Emprestimo
                WHERE Id_Usuario = %s AND Id_Livro = %s AND Devolvido = TRUE
            """, (id_usuario, id_livro))
            
            if not cursor.fetchone():
                print("Você precisa ter lido o livro para escrever uma resenha.")
                return False
            
            # Verificar se já existe resenha (para não duplicar pontos)
            cursor.execute("""
                SELECT 1 FROM Resenha
                WHERE Id_Usuario = %s AND Id_Livro = %s
            """, (id_usuario, id_livro))
            
            ja_existe_resenha = cursor.fetchone() is not None
            
            # Adicionar ou atualizar resenha
            cursor.execute("""
                INSERT INTO Resenha (Id_Usuario, Id_Livro, Resenha)
                VALUES (%s, %s, %s)
                ON CONFLICT (Id_Usuario, Id_Livro)
                DO UPDATE SET Resenha = EXCLUDED.Resenha
            """, (id_usuario, id_livro, resenha))
            # Deixe apenas o PontuacaoService cuidar dos pontos
            
            self.conn.commit()
            print("Resenha salva com sucesso!")
            
            # Retornar se é uma resenha nova (para saber se deve dar pontos)
            return {'sucesso': True, 'nova_resenha': not ja_existe_resenha}
            
        except Exception as e:
            print(f"Erro ao salvar resenha: {e}")
            self.conn.rollback()
            return {'sucesso': False, 'nova_resenha': False}
        finally:
            cursor.close()
            
    def listar_resenhas_livro(self, id_livro):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT u.Nome, r.Resenha, r.Curtidas
                FROM Resenha r
                JOIN Usuario u ON r.Id_Usuario = u.Id_Usuario
                WHERE r.Id_Livro = %s
                ORDER BY r.Curtidas DESC
            """, (id_livro,))
            resenhas = cursor.fetchall()
            if not resenhas:
                print("Nenhuma resenha encontrada para este livro.")
                return []

            # Obter título do livro
            cursor.execute("SELECT Titulo FROM Livro WHERE Id_Livro = %s", (id_livro,))
            titulo = cursor.fetchone()[0]

            print(f"\n=== RESENHAS - {titulo.upper()} ===")
            for resenha in resenhas:
                print(f"\n📝 {resenha[0]}")
                print(f"⭐ {resenha[2]} Curtidas")
                print(f"📄 {resenha[1]}\n")
            return resenhas
        except Exception as e:
            print(f"Erro ao listar resenhas: {e}")
            return []
        finally:
            cursor.close()

    def curtir_resenha(self, id_usuario, id_livro):
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE Resenha 
                SET Curtidas = Curtidas + 1
                WHERE Id_Usuario = %s AND Id_Livro = %s
            """, (id_usuario, id_livro))
            
            if cursor.rowcount == 0:
                print("Resenha não encontrada.")
                return False
            
            self.conn.commit()
            print("Resenha curtida!")
            return True
            
        except Exception as e:
            print(f"Erro ao curtir resenha: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()