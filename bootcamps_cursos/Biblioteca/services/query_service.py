# =============================================================================
# services/query_service.py 
# Serviço para consultas específicas
# =============================================================================

class QueryService:
    def __init__(self, conn):
        self.conn = conn
    def consulta_livros_disponiveis(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT l.Titulo, a.Nome as Autor, e.Nome as Editora, l.Ano_Publicacao
                FROM Livro l
                JOIN Co_Autor ca ON l.Id_Livro = ca.Id_Livro
                JOIN Autor a ON ca.Id_Autor = a.Id_Autor
                JOIN Editora e ON l.Id_Editora = e.Id_Editora
                WHERE l.Status = 'disponível'
                ORDER BY l.Titulo
            """)
            livros = cursor.fetchall()

            if not livros:
                print("Nenhum livro disponível encontrado.")
                return []

            print("\n=== LIVROS DISPONÍVEIS ===")
            for livro in livros:
                print(f"- {livro[0]} - {livro[1]} ({livro[3]}) - Editora: {livro[2]}")

            return livros
        except Exception as e:
            print(f"Erro ao consultar livros disponíveis: {e}")
            return []
        finally:
            cursor.close()

    def consulta_emprestimos_ativos(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT u.Nome, l.Titulo, e.Data_Emprestimo, e.Data_Prevista_Devolucao,
                   CASE 
                       WHEN e.Data_Prevista_Devolucao < CURRENT_DATE THEN 'Em atraso'
                       ELSE 'No prazo'
                   END as Situacao
            FROM Emprestimo e
            JOIN Usuario u ON e.Id_Usuario = u.Id_Usuario
            JOIN Livro l ON e.Id_Livro = l.Id_Livro
            WHERE e.Devolvido = FALSE
            ORDER BY e.Data_Prevista_Devolucao
        """)
        
        emprestimos = cursor.fetchall()
        cursor.close()
        
        if not emprestimos:
            print("Nenhum empréstimo ativo encontrado.")
            return []
        
        print("\n=== EMPRÉSTIMOS ATIVOS ===")
        for emp in emprestimos:
            print(f"• {emp[0]} - {emp[1]} (Empréstimo: {emp[2]}, Prazo: {emp[3]}) - {emp[4]}")
        
        return emprestimos
    
    def consulta_usuarios_com_multa(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT u.Nome, u.CPF, SUM(e.Multa) as Total_Multa
            FROM Usuario u
            JOIN Emprestimo e ON u.Id_Usuario = e.Id_Usuario
            WHERE e.Multa > 0
            GROUP BY u.Id_Usuario, u.Nome, u.CPF
            ORDER BY Total_Multa DESC
        """)
        
        usuarios_multa = cursor.fetchall()
        cursor.close()
        
        if not usuarios_multa:
            print("Nenhum usuário com multa encontrado.")
            return []
        
        print("\n=== USUÁRIOS COM MULTA ===")
        for usuario in usuarios_multa:
            print(f"• {usuario[0]} (CPF: {usuario[1]}) - Multa Total: R$ {usuario[2]:.2f}")
        
        return usuarios_multa
    
    def consulta_livros_mais_populares(self, limite=10):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT l.Titulo, a.Nome as Autor, COUNT(e.Id_Emprestimo) as Total_Emprestimos,
                   COUNT(c.Id_Comentario) as Total_Comentarios,
                   COUNT(r.Id_Usuario) as Total_Resenhas
            FROM Livro l
            JOIN Co_Autor ca ON l.Id_Livro = ca.Id_Livro
            JOIN Autor a ON ca.Id_Autor = a.Id_Autor
            LEFT JOIN Emprestimo e ON l.Id_Livro = e.Id_Livro
            LEFT JOIN Comentario c ON l.Id_Livro = c.Id_Livro
            LEFT JOIN Resenha r ON l.Id_Livro = r.Id_Livro
            GROUP BY l.Id_Livro, l.Titulo, a.Nome
            ORDER BY Total_Emprestimos DESC, Total_Comentarios DESC
            LIMIT %s
        """, (limite,))
        
        livros_populares = cursor.fetchall()
        cursor.close()
        
        print(f"\n=== TOP {limite} LIVROS MAIS POPULARES ===")
        for i, livro in enumerate(livros_populares, 1):
            print(f"{i}. {livro[0]} - {livro[1]}")
            print(f"   Empréstimos: {livro[2]} | Comentários: {livro[3]} | Resenhas: {livro[4]}")
        
        return livros_populares
    
    def buscar_livros_por_palavra_chave(self, palavra):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT DISTINCT l.Titulo, a.Nome as Autor, pc.Palavra, l.Status
            FROM Livro l
            JOIN Co_Autor ca ON l.Id_Livro = ca.Id_Livro
            JOIN Autor a ON ca.Id_Autor = a.Id_Autor
            JOIN Livro_PalavraChave lpc ON l.Id_Livro = lpc.Id_Livro
            JOIN Palavra_Chave pc ON lpc.Id_Chave = pc.Id_Chave
            WHERE LOWER(pc.Palavra) LIKE LOWER(%s)
            ORDER BY l.Titulo
        """, (f'%{palavra}%',))
        
        resultados = cursor.fetchall()
        cursor.close()
        
        if not resultados:
            print(f"Nenhum livro encontrado com a palavra-chave '{palavra}'.")
            return []
        
        print(f"\n=== LIVROS COM PALAVRA-CHAVE '{palavra.upper()}' ===")
        for livro in resultados:
            status_emoji = "✅" if livro[3] == 'disponivel' else "❌"
            print(f"{status_emoji} {livro[0]} - {livro[1]} (Categoria: {livro[2]})")
        
        return resultados