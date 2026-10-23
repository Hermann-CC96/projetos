# =============================================================================
# services/pontuacao_service.py
# Serviço para gerenciar sistema de pontuação
# =============================================================================
from datetime import datetime
class PontuacaoService:
    def __init__(self, conn):
        self.conn = conn

    def adicionar_pontos(self, id_usuario, motivo, pontos):
        cursor = self.conn.cursor()

        try:
            data_pontuacao = datetime.now().date()
            cursor.execute("""
                INSERT INTO Pontuacao (Id_Usuario, Motivo, Pontos, Data_Pontuacao)
                VALUES (%s, %s, %s, %s)
            """, (id_usuario, motivo, pontos, data_pontuacao))

            self.conn.commit()
            print(f"Pontuação adicionada: +{pontos} pontos por {motivo}")
            return True

        except Exception as e:
            print(f"Erro ao adicionar pontos: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def processar_pontos_emprestimo(self, id_usuario):
        # Pontos por empréstimo realizado
        return self.adicionar_pontos(id_usuario, "Empréstimo realizado", 10)

    def processar_pontos_devolucao_prazo(self, id_usuario):
        # Pontos por devolução no prazo
        return self.adicionar_pontos(id_usuario, "Devolução no prazo", 5)

    def processar_pontos_comentario(self, id_usuario):
        # Pontos por comentário
        return self.adicionar_pontos(id_usuario, "Comentário adicionado", 3)

    def processar_pontos_resenha(self, id_usuario):
        # Pontos por resenha
        return self.adicionar_pontos(id_usuario, "Resenha escrita", 15)

    def obter_pontuacao_usuario(self, id_usuario):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COALESCE(SUM(Pontos), 0) as Total_Pontos
            FROM Pontuacao
            WHERE Id_Usuario = %s
        """, (id_usuario,))

        total_pontos = cursor.fetchone()[0]
        cursor.close()

        return total_pontos
   
    def obter_historico_pontuacao(self, id_usuario):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT Motivo, Pontos, Data_Pontuacao
            FROM Pontuacao 
            WHERE Id_Usuario = %s
            ORDER BY Data_Pontuacao DESC
            LIMIT 20
        """, (id_usuario,))
        
        historico = cursor.fetchall()
        cursor.close()
        
        if not historico:
            print("Nenhum histórico de pontuação encontrado.")
            return []
        
        print("\n=== HISTÓRICO DE PONTUAÇÃO ===\n")

        ano_atual = None

        for registro in historico:
            motivo = registro[0]
            pontos = registro[1]
            data = registro[2]
            ano = data.year
            sinal = "+" if pontos > 0 else ""

            # Emoji por motivo
            if 'Empréstimo' in motivo:
                emoji = "📚"
            elif 'Devolução' in motivo:
                emoji = "✅"
            elif 'Resenha' in motivo:
                emoji = "✍️"
            elif 'Reserva' in motivo:
                emoji = "🔖"
            else:
                emoji = "⭐"

            # Mostra o ano apenas quando mudar
            if ano != ano_atual:
                print(f"\n📅 Ano: {ano}\n" + "-"*20)
                ano_atual = ano

            print(f"{emoji} {data} | {sinal}{pontos} pts - {motivo}")
        
        return historico
    
    def atualizar_ranking(self):
        cursor = self.conn.cursor()
        
        try:
            # Limpar ranking atual
            cursor.execute("DELETE FROM Ranking")
            
            # Calcular ranking mensal
            cursor.execute("""
                INSERT INTO Ranking (Id_Usuario, Categoria, Pontos, Periodo, Data)
                SELECT p.Id_Usuario, 'Mensal', SUM(p.Pontos), 'Mensal', CURRENT_DATE
                FROM Pontuacao p
                WHERE p.Data_Pontuacao >= DATE_TRUNC('month', CURRENT_DATE)
                GROUP BY p.Id_Usuario
                ORDER BY SUM(p.Pontos) DESC
            """)
            
            # Calcular ranking geral
            cursor.execute("""
                INSERT INTO Ranking (Id_Usuario, Categoria, Pontos, Periodo, Data)
                SELECT p.Id_Usuario, 'Geral', SUM(p.Pontos), 'Geral', CURRENT_DATE
                FROM Pontuacao p
                GROUP BY p.Id_Usuario
                ORDER BY SUM(p.Pontos) DESC
            """)
            
            self.conn.commit()
            print("Ranking atualizado com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao atualizar ranking: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()
