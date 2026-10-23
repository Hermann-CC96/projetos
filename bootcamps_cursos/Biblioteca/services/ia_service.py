
# =============================================================================
# services/ia_service.py
# Serviço de IA para recomendações
# =============================================================================
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
import os

class IAService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def recomendar_livros(self, conn, id_usuario):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT l.Titulo, l.Ano_Publicacao, a.Nome as Autor
                FROM Emprestimo e
                JOIN Livro l ON e.Id_Livro = l.Id_Livro
                JOIN Co_Autor ca ON l.Id_Livro = ca.Id_Livro
                JOIN Autor a ON ca.Id_Autor = a.Id_Autor
                WHERE e.Id_Usuario = %s AND e.Devolvido = TRUE
                ORDER BY e.Data_Devolucao DESC
                LIMIT 5
            """, (id_usuario,))
            historico = cursor.fetchall()
            cursor.close()

            if not historico:
                return "📚 Você ainda não tem histórico de empréstimos. Explore nossa biblioteca!"

            livros_lidos = ", ".join([f"{livro[0]} de {livro[2]}" for livro in historico])

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um bibliotecário especialista em recomendações literárias."},
                    {"role": "user", "content": f"Com base nos livros que o usuário já leu: {livros_lidos}, recomende 3 livros similares da literatura brasileira. Responda diretamente as recomendações com breve explicação."}
                ],
                temperature=0.5,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"❌ Erro ao gerar recomendação: {e}"

    def sugerir_comentario_resenha(self, conn, id_usuario, id_livro):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT l.Titulo, a.Nome as Autor
                FROM Livro l
                JOIN Co_Autor ca ON l.Id_Livro = ca.Id_Livro
                JOIN Autor a ON ca.Id_Autor = a.Id_Autor
                WHERE l.Id_Livro = %s
            """, (id_livro,))
            livro_info = cursor.fetchone()
            cursor.close()

            if not livro_info:
                return "❌ Livro não encontrado."

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um assistente que ajuda usuários a escrever comentários e resenhas de livros."},
                    {"role": "user", "content": f"Baseado no livro '{livro_info[0]}' de {livro_info[1]}, sugira um comentário ou resenha completo que o usuário pode escrever para compartilhar sua experiência de leitura. o remumo deve ter no maximo 300 palvras"}
                ],
                temperature=0.5,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"❌ Erro ao gerar sugestão: {e}"
    
    def gerar_resposta_personalizada(self, conn, id_usuario, prompt_usuario):
        try:
            cursor = conn.cursor()

            # Obter livros associados ao usuário
            cursor.execute("""
                SELECT l.Titulo, a.Nome as Autor
                FROM Emprestimo e
                JOIN Livro l ON e.Id_Livro = l.Id_Livro
                JOIN Co_Autor ca ON l.Id_Livro = ca.Id_Livro
                JOIN Autor a ON ca.Id_Autor = a.Id_Autor
                WHERE e.Id_Usuario = %s AND e.Devolvido = TRUE
                ORDER BY e.Data_Devolucao DESC
                LIMIT 5
            """, (id_usuario,))

            livros_lidos = cursor.fetchall()
            cursor.close()

            if not livros_lidos:
                return "📚 Você ainda não tem histórico de empréstimos. Explore nossa biblioteca!"

            # Formatar o contexto para a IA
            contexto_livros = "Livros lidos pelo usuário:\n" + "\n".join(
                [f"- {livro[0]} por {livro[1]}" for livro in livros_lidos]
            )

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um assistente de biblioteca especializado em literatura e livros."},
                    {"role": "system", "content": contexto_livros},
                    {"role": "user", "content": prompt_usuario}
                ],
                temperature=0.5,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"❌ Erro ao gerar resposta: {e}"
