# =============================================================================
# services/reserva_service.py
# Serviço para gerenciar reservas
# =============================================================================
from datetime import datetime

class ReservaService:
    def __init__(self, conn):
        self.conn = conn
    
    def fazer_reserva(self, id_usuario, id_livro):
        cursor = self.conn.cursor()
        
        try:
            # Verificar se o livro existe e obter informações sobre exemplares
            cursor.execute("""
                SELECT Status, Quantidade_Exemplares 
                FROM Livro 
                WHERE Id_Livro = %s
            """, (id_livro,))
            livro_info = cursor.fetchone()
            
            if not livro_info:
                print("Livro não encontrado.")
                return False
            
            status_atual, quantidade_total = livro_info
            
            # Contar quantos exemplares estão emprestados
            cursor.execute("""
                SELECT COUNT(*) FROM Emprestimo 
                WHERE Id_Livro = %s AND Status = 'ativo'
            """, (id_livro,))
            exemplares_emprestados = cursor.fetchone()[0]
            
            # Calcular exemplares disponíveis
            exemplares_disponiveis = quantidade_total - exemplares_emprestados
            
            # Se ainda há exemplares disponíveis, não pode fazer reserva
            if exemplares_disponiveis > 0:
                print(f"Livro possui {exemplares_disponiveis} exemplar(es) disponível(is). Realize um empréstimo direto.")
                return False
            
            # Verificar se usuário já tem reserva ativa para este livro
            cursor.execute("""
                SELECT Id_Reserva FROM Reserva 
                WHERE Id_Usuario = %s AND Id_Livro = %s AND Status = 'ativo'
            """, (id_usuario, id_livro))
            
            if cursor.fetchone():
                print("Você já possui uma reserva ativa para este livro.")
                return False
            
            # Criar reserva
            data_reserva = datetime.now().date()
            cursor.execute("""
                INSERT INTO Reserva (Id_Usuario, Id_Livro, Data, Status)
                VALUES (%s, %s, %s, 'ativo')
            """, (id_usuario, id_livro, data_reserva))
            
            # Atualizar status do livro para 'reservado' quando criar a primeira reserva
            # e não há exemplares disponíveis
            if exemplares_disponiveis == 0:
                cursor.execute("""
                    UPDATE Livro SET Status = 'reservado' 
                    WHERE Id_Livro = %s
                """, (id_livro,))
            
            self.conn.commit()
            print("Reserva realizada com sucesso! Você será notificado quando o livro estiver disponível.")
            return True
            
        except Exception as e:
            print(f"Erro ao fazer reserva: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()
    
    def cancelar_reserva(self, id_reserva):
        cursor = self.conn.cursor()
        
        try:
            # Obter informações da reserva antes de cancelar
            cursor.execute("""
                SELECT Id_Livro FROM Reserva 
                WHERE Id_Reserva = %s AND Status = 'ativo'
            """, (id_reserva,))
            reserva_info = cursor.fetchone()
            
            if not reserva_info:
                print("Reserva não encontrada ou já cancelada.")
                return False
            
            id_livro = reserva_info[0]
            
            # Cancelar a reserva
            cursor.execute("""
                UPDATE Reserva SET Status = 'cancelado' 
                WHERE Id_Reserva = %s AND Status = 'ativo'
            """, (id_reserva,))
            
            # Verificar se ainda há outras reservas ativas para este livro
            cursor.execute("""
                SELECT COUNT(*) FROM Reserva 
                WHERE Id_Livro = %s AND Status = 'ativo'
            """, (id_livro,))
            reservas_restantes = cursor.fetchone()[0]
            
            # Verificar exemplares disponíveis
            cursor.execute("""
                SELECT Quantidade_Exemplares FROM Livro 
                WHERE Id_Livro = %s
            """, (id_livro,))
            quantidade_total = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT COUNT(*) FROM Emprestimo 
                WHERE Id_Livro = %s AND Status = 'ativo'
            """, (id_livro,))
            exemplares_emprestados = cursor.fetchone()[0]
            
            exemplares_disponiveis = quantidade_total - exemplares_emprestados
            
            # Atualizar status do livro baseado na situação atual
            if exemplares_disponiveis > 0:
                novo_status = 'disponível'
            elif reservas_restantes > 0:
                novo_status = 'reservado'
            else:
                novo_status = 'emprestado'
            
            cursor.execute("""
                UPDATE Livro SET Status = %s 
                WHERE Id_Livro = %s
            """, (novo_status, id_livro))
            
            self.conn.commit()
            print(f"Reserva cancelada com sucesso. Status do livro atualizado para: {novo_status}")
            return True
            
        except Exception as e:
            print(f"Erro ao cancelar reserva: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def excluir_reserva(self, id_reserva):
        cursor = self.conn.cursor()
        try:
            # Verificar se a reserva existe e obter informações
            cursor.execute("""
                SELECT Id_Livro, Status FROM Reserva 
                WHERE Id_Reserva = %s
            """, (id_reserva,))
            reserva_info = cursor.fetchone()

            if not reserva_info:
                print("Reserva não encontrada.")
                return False

            id_livro, status_reserva = reserva_info

            # Excluir a reserva
            cursor.execute("DELETE FROM Reserva WHERE Id_Reserva = %s", (id_reserva,))
            
            # Se a reserva excluída estava ativa, atualizar status do livro
            if status_reserva == 'ativo':
                # Verificar se ainda há outras reservas ativas
                cursor.execute("""
                    SELECT COUNT(*) FROM Reserva 
                    WHERE Id_Livro = %s AND Status = 'ativo'
                """, (id_livro,))
                reservas_restantes = cursor.fetchone()[0]
                
                # Verificar exemplares disponíveis
                cursor.execute("""
                    SELECT Quantidade_Exemplares FROM Livro 
                    WHERE Id_Livro = %s
                """, (id_livro,))
                quantidade_total = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT COUNT(*) FROM Emprestimo 
                    WHERE Id_Livro = %s AND Status = 'ativo'
                """, (id_livro,))
                exemplares_emprestados = cursor.fetchone()[0]
                
                exemplares_disponiveis = quantidade_total - exemplares_emprestados
                
                # Definir novo status
                if exemplares_disponiveis > 0:
                    novo_status = 'disponível'
                elif reservas_restantes > 0:
                    novo_status = 'reservado'
                else:
                    novo_status = 'emprestado'
                
                cursor.execute("""
                    UPDATE Livro SET Status = %s 
                    WHERE Id_Livro = %s
                """, (novo_status, id_livro))
                
                print(f"Reserva excluída com sucesso! Status do livro atualizado para: {novo_status}")
            else:
                print("Reserva excluída com sucesso!")
            
            self.conn.commit()
            return True

        except Exception as e:
            print(f"Erro ao excluir reserva: {e}")
            self.conn.rollback()
            return False
        finally:
            cursor.close()
            
    def listar_reservas_usuario(self, id_usuario):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT r.Id_Reserva, l.Titulo, a.Nome as Autor, r.Data, r.Status
            FROM Reserva r
            JOIN Livro l ON r.Id_Livro = l.Id_Livro
            JOIN Co_Autor ca ON l.Id_Livro = ca.Id_Livro
            JOIN Autor a ON ca.Id_Autor = a.Id_Autor
            WHERE r.Id_Usuario = %s
            ORDER BY r.Data DESC
        """, (id_usuario,))
        
        reservas = cursor.fetchall()
        cursor.close()
        
        if not reservas:
            print("Nenhuma reserva encontrada.")
            return []
        
        print("\n=== SUAS RESERVAS ===")
        for reserva in reservas:
            status_emoji = "🟢" if reserva[4] == 'ativo' else "🔴"
            print(f"{status_emoji} {reserva[1]} - {reserva[2]} (Data: {reserva[3]}) - {reserva[4]}")
        
        return reservas
   