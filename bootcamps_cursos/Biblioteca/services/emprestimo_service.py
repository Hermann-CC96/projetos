# =============================================================================
# services/emprestimo_service.py
# Serviço para gerenciar empréstimos
# =============================================================================
from datetime import datetime, timedelta

class EmprestimoService:
    def __init__(self, conn):
        self.conn = conn
    def realizar_emprestimo(self, id_usuario, id_livro):
        cursor = self.conn.cursor()

        try:
            # ⭐ NOVA RESTRIÇÃO: Verificar se o usuário já tem empréstimo ativo do mesmo livro
            cursor.execute("""
                SELECT COUNT(*) FROM Emprestimo 
                WHERE Id_Usuario = %s AND Id_Livro = %s AND Devolvido = FALSE
            """, (id_usuario, id_livro))
            
            emprestimo_mesmo_livro = cursor.fetchone()[0]
            
            if emprestimo_mesmo_livro > 0:
                print("❌ ERRO: Você já possui um empréstimo ativo deste livro!")
                print("💡 Dica: Devolva o livro antes de emprestar novamente.")
                return False

            # Verificar se o usuário tem multas pendentes
            cursor.execute("SELECT Multa FROM Emprestimo WHERE Id_Usuario = %s AND Multa > 0", (id_usuario,))
            if cursor.fetchone():
                print("Usuário possui multas pendentes. Não é possível realizar empréstimo.")
                return False

            # Verificar se o usuário atingiu o limite de empréstimos
            cursor.execute("SELECT COUNT(*) FROM Emprestimo WHERE Id_Usuario = %s AND Devolvido = FALSE", (id_usuario,))
            emprestimos_ativos = cursor.fetchone()[0]

            cursor.execute("""
                SELECT c.Limite_Emprestimos FROM Usuario u
                JOIN Categoria c ON u.Id_Categoria = c.Id_Categoria
                WHERE u.Id_Usuario = %s
            """, (id_usuario,))
            limite_emprestimos = cursor.fetchone()[0]

            if emprestimos_ativos >= limite_emprestimos:
                print("Usuário atingiu o limite de empréstimos.")
                return False

            # Verificar se há exemplares disponíveis do livro
            cursor.execute("SELECT Quantidade_Exemplares FROM Livro WHERE Id_Livro = %s", (id_livro,))
            quantidade_exemplares = cursor.fetchone()[0]

            if quantidade_exemplares <= 0:
                print("Livro não disponível para empréstimo. Você pode fazer uma reserva.")
                return False

            # Obter dados do usuário e categoria
            cursor.execute("""
                SELECT u.Id_Usuario, c.Dias_Prazo
                FROM Usuario u
                JOIN Categoria c ON u.Id_Categoria = c.Id_Categoria
                WHERE u.Id_Usuario = %s
            """, (id_usuario,))

            user_data = cursor.fetchone()
            if not user_data:
                print("Usuário não encontrado")
                return False

            # Calcular datas
            data_emprestimo = datetime.now().date()
            data_prevista = data_emprestimo + timedelta(days=user_data[1])

            # Inserir empréstimo
            cursor.execute("""
                INSERT INTO Emprestimo (Id_Usuario, Id_Livro, Data_Emprestimo, Data_Prevista_Devolucao, Status)
                VALUES (%s, %s, %s, %s, 'ativa')
            """, (id_usuario, id_livro, data_emprestimo, data_prevista))

            # Atualizar quantidade de exemplares do livro
            cursor.execute("""
                UPDATE Livro
                SET Quantidade_Exemplares = Quantidade_Exemplares - 1
                WHERE Id_Livro = %s
            """, (id_livro,))

            self.conn.commit()
            print(f"✅ Empréstimo realizado com sucesso! Data de devolução: {data_prevista}")
            return True

        except Exception as e:
            print(f"Erro ao realizar empréstimo: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()
            
    def devolver_livro(self, id_emprestimo):
        cursor = self.conn.cursor()

        try:
            # Obter dados do empréstimo
            cursor.execute("""
                SELECT e.Id_Livro, e.Data_Prevista_Devolucao, e.Id_Usuario, c.Valor_Multa_Dia
                FROM Emprestimo e
                JOIN Usuario u ON e.Id_Usuario = u.Id_Usuario
                JOIN Categoria c ON u.Id_Categoria = c.Id_Categoria
                WHERE e.Id_Emprestimo = %s AND e.Devolvido = FALSE
            """, (id_emprestimo,))

            emprestimo_data = cursor.fetchone()
            if not emprestimo_data:
                print("Empréstimo não encontrado ou já devolvido")
                return False

            id_livro, data_prevista, id_usuario, valor_multa_dia = emprestimo_data
            data_devolucao = datetime.now().date()

            # Calcular multa se houver atraso
            multa = 0
            if data_devolucao > data_prevista:
                dias_atraso = (data_devolucao - data_prevista).days
                multa = dias_atraso * float(valor_multa_dia)

            # Atualizar empréstimo
            cursor.execute("""
                UPDATE Emprestimo
                SET Data_Devolucao = %s, Devolvido = TRUE, Multa = %s, Status = 'Finalizado'
                WHERE Id_Emprestimo = %s
            """, (data_devolucao, multa, id_emprestimo))

            # Atualizar status do livro
            cursor.execute("UPDATE Livro SET Status = 'disponivel' WHERE Id_Livro = %s", (id_livro,))

            # Atualizar quantidade de exemplares do livro
            cursor.execute("""
                UPDATE Livro
                SET Quantidade_Exemplares = Quantidade_Exemplares + 1
                WHERE Id_Livro = %s
            """, (id_livro,))

            self.conn.commit()

            if multa > 0:
                print(f"Livro devolvido com atraso. Multa: R$ {multa:.2f}")
            else:
                print("Livro devolvido com sucesso!")

            return True

        except Exception as e:
            print(f"Erro ao devolver livro: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def listar_livros_nao_devolvidos(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT e.Id_Emprestimo, l.Titulo, u.Nome as Usuario, e.Data_Emprestimo, e.Data_Prevista_Devolucao
                FROM Emprestimo e
                JOIN Livro l ON e.Id_Livro = l.Id_Livro
                JOIN Usuario u ON e.Id_Usuario = u.Id_Usuario
                WHERE e.Devolvido = FALSE
            """)
            livros_nao_devolvidos = cursor.fetchall()

            if not livros_nao_devolvidos:
                print("Nenhum livro não devolvido encontrado.")
                return []

            print("\n=== LIVROS NÃO DEVOLVIDOS ===")
            for livro in livros_nao_devolvidos:
                print(f"ID Empréstimo: {livro[0]}, Título: {livro[1]}, Usuário: {livro[2]}, Data de Empréstimo: {livro[3]}, Data Prevista de Devolução: {livro[4]}")

            return livros_nao_devolvidos
        except Exception as e:
            print(f"Erro ao listar livros não devolvidos: {e}")
            return []
        finally:
            cursor.close()