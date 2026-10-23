# =============================================================================
# services/graphics_service.py
# Serviço para gerar gráficos
# =============================================================================

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from datetime import datetime

class GraphicsService:
    def __init__(self, conn):
        self.conn = conn
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['font.size'] = 10
    
    def grafico_livros_mais_emprestados(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                SELECT l.Titulo, COUNT(e.Id_Emprestimo) as Total_Emprestimos, STRING_AGG(u.Nome, ', ') as Usuarios
                FROM Livro l
                LEFT JOIN Emprestimo e ON l.Id_Livro = e.Id_Livro
                LEFT JOIN Usuario u ON e.Id_Usuario = u.Id_Usuario
                GROUP BY l.Id_Livro, l.Titulo
                ORDER BY Total_Emprestimos DESC
                LIMIT 10
            """)

            data = cursor.fetchall()

            if not data:
                print("Nenhum dado de empréstimos encontrado")
                return

            # Extrair dados para o gráfico
            titulos = [row[0][:30] + '...' if len(row[0]) > 30 else row[0] for row in data]
            emprestimos = [row[1] for row in data]
            usuarios = [row[2] for row in data]

            # Criar gráfico
            plt.figure(figsize=(12, 8))
            bars = plt.bar(range(len(titulos)), emprestimos, color='skyblue', edgecolor='navy', linewidth=1.2)
            plt.title('Top 10 Livros Mais Emprestados', fontsize=16, fontweight='bold', pad=20)
            plt.xlabel('Livros', fontsize=12)
            plt.ylabel('Número de Empréstimos', fontsize=12)
            plt.xticks(range(len(titulos)), titulos, rotation=45, ha='right')

            # Adicionar valores nas barras
            for bar, value, usuario in zip(bars, emprestimos, usuarios):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height + max(emprestimos) * 0.02, str(value),
                        ha='center', va='bottom', fontweight='bold')
                plt.text(bar.get_x() + bar.get_width() / 2, -max(emprestimos) * 0.05, usuario[:30] + '...' if len(usuario) > 30 else usuario,
                        ha='center', va='top', rotation=45, fontweight='normal', fontsize=8)

            plt.tight_layout()
            plt.grid(axis='y', alpha=0.3)
            plt.show()

        except Exception as e:
            print(f"Erro ao gerar gráfico de livros mais emprestados: {e}")

        finally:
            cursor.close()
    def grafico_emprestimos_por_categoria(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT c.Nome, COUNT(e.Id_Emprestimo) as Total_Emprestimos , STRING_AGG(u.Nome, ', ') as Usuarios
            FROM Categoria c
            LEFT JOIN Usuario u ON c.Id_Categoria = u.Id_Categoria
            LEFT JOIN Emprestimo e ON u.Id_Usuario = e.Id_Usuario
            GROUP BY c.Id_Categoria, c.Nome
            ORDER BY Total_Emprestimos DESC
        """)
        data = cursor.fetchall()
        cursor.close()

        if not data:
            print("Nenhum dado encontrado")
            return

        # Filtrar dados inválidos
        categorias = []
        emprestimos = []

        for row in data:
            nome, total, usuarios = row
            if total is not None:
                categorias.append(nome)
                emprestimos.append(total)

        if not emprestimos:
            print("Nenhum dado válido encontrado para criar o gráfico")
            return

        # Criar gráfico de pizza
        plt.figure(figsize=(10, 8))
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
        wedges, texts, autotexts = plt.pie(
            emprestimos,
            labels=categorias,
            autopct='%1.1f%%',
            colors=colors[:len(categorias)],
            startangle=90,
            explode=[0.05] * len(categorias)
        )
        plt.title('Distribuição de Empréstimos por Categoria de Usuário', fontsize=14, fontweight='bold', pad=20)

        # Melhorar legenda
        plt.legend(
            wedges,
            [f'{cat}: {emp} empréstimos' for cat, emp in zip(categorias, emprestimos)],
            title="Categorias",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    
    def grafico_ranking_usuarios(self):
        cursor = self.conn.cursor()
        
        cursor.execute("""
            
            SELECT u.Nome, COUNT(e.Id_Emprestimo) as Total_Emprestimos,
                   COALESCE(SUM(p.Pontos), 0) as Total_Pontos
            FROM Usuario u
            LEFT JOIN Emprestimo e ON u.Id_Usuario = e.Id_Usuario
            LEFT JOIN Pontuacao p ON u.Id_Usuario = p.Id_Usuario
            GROUP BY u.Id_Usuario, u.Nome
            ORDER BY Total_Emprestimos DESC, Total_Pontos DESC
            LIMIT 10
        """)
        
        data = cursor.fetchall()
        cursor.close()
        
        if not data:
            print("Nenhum dado de ranking encontrado")
            return
        
        nomes = [row[0] for row in data]
        emprestimos = [row[1] for row in data]
        pontos = [row[2] for row in data]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Gráfico de empréstimos
        bars1 = ax1.bar(range(len(nomes)), emprestimos, color='lightcoral', alpha=0.8)
        ax1.set_title('Ranking - Empréstimos por Usuário', fontweight='bold')
        ax1.set_xlabel('Usuários')
        ax1.set_ylabel('Número de Empréstimos')
        ax1.set_xticks(range(len(nomes)))
        ax1.set_xticklabels(nomes, rotation=45, ha='right')
       
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2, height + max(emprestimos) * 0.05, str(int(height)),
                     ha='center', va='bottom', fontweight='bold')
        # Gráfico de pontos
        bars2 = ax2.bar(range(len(nomes)), pontos, color='lightgreen', alpha=0.8)
        ax2.set_title('Ranking - Pontuação por Usuário', fontweight='bold')
        ax2.set_xlabel('Usuários')
        ax2.set_ylabel('Pontos')
        ax2.set_xticks(range(len(nomes)))
        ax2.set_xticklabels(nomes, rotation=45, ha='right')
        
        for bar, value in zip(bars2, pontos):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(value), ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()

    def grafico_pontuacao_usuarios(self):
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                SELECT u.Nome, p.Data_Pontuacao, SUM(p.Pontos) as Pontos_Dia, l.Titulo
                FROM Usuario u
                JOIN Pontuacao p ON u.Id_Usuario = p.Id_Usuario
                LEFT JOIN Emprestimo e ON u.Id_Usuario = e.Id_Usuario
                LEFT JOIN Livro l ON e.Id_Livro = l.Id_Livro
                GROUP BY u.Id_Usuario, u.Nome, p.Data_Pontuacao, l.Titulo
                ORDER BY p.Data_Pontuacao
            """)

            data = cursor.fetchall()

            if not data:
                print("Nenhum dado de pontuação encontrado")
                return

            # Agrupar dados por usuário
            usuarios = {}
            for nome, data_pont, pontos, titulo in data:
                if nome not in usuarios:
                    usuarios[nome] = {'datas': [], 'pontos': [], 'titulos': []}
                usuarios[nome]['datas'].append(data_pont)
                usuarios[nome]['pontos'].append(pontos)
                usuarios[nome]['titulos'].append(titulo)

            # Preparar dados para barras empilhadas
            nomes_usuarios = list(usuarios.keys())
            datas_unicas = sorted(set([data_pont for dados in usuarios.values() for data_pont in dados['datas']]))

            # Montar matriz de pontos
            matriz_pontos = []
            for nome in nomes_usuarios:
                pontos_por_data = []
                for data in datas_unicas:
                    if data in usuarios[nome]['datas']:
                        idx = usuarios[nome]['datas'].index(data)
                        pontos_por_data.append(usuarios[nome]['pontos'][idx])
                    else:
                        pontos_por_data.append(0)
                matriz_pontos.append(pontos_por_data)

            matriz_pontos = np.array(matriz_pontos)

            # Calcular o total de pontos por usuário
            total_por_usuario = np.sum(matriz_pontos, axis=1)

            plt.figure(figsize=(14, 8))
            bottom = np.zeros(len(nomes_usuarios))
            colors = ['b', 'r', 'g', 'orange', 'purple', 'brown', 'pink', 'gray']

            # Barras empilhadas
            for i, data in enumerate(datas_unicas):
                plt.bar(nomes_usuarios, matriz_pontos[:, i], bottom=bottom, color=colors[i % len(colors)], label=data.strftime('%d/%m'))
                bottom += matriz_pontos[:, i]

            # Linha de total
            plt.plot(nomes_usuarios, total_por_usuario, color='green', marker='o', linewidth=2, label='Total')

            # Rótulos de total
            for x, y in zip(nomes_usuarios, total_por_usuario):
                plt.text(x, y + 2, f'{y:.0f}', ha='center', fontsize=9, fontweight='bold', color='green')

            plt.title('Pontuação Total por Usuário', fontsize=16, fontweight='bold', pad=20)
            plt.xlabel('Usuários', fontsize=12)
            plt.ylabel('Pontos', fontsize=12)
            plt.xticks(rotation=45)
            plt.legend(title='Datas', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Erro ao gerar gráfico de pontuação por usuário: {e}")

        finally:
            cursor.close()