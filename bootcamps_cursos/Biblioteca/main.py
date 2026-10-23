# =============================================================================
# main.py
# Programa principal com menu interativo
# ============================================================================
from datetime import timedelta
from config.database import DatabaseConfig
from services.database_service import DatabaseService
from services.emprestimo_service import EmprestimoService
from services.reserva_service import ReservaService
from services.comentario_service import ComentarioService
from services.pontuacao_service import PontuacaoService
from services.query_service import QueryService
from services.graphics_service import GraphicsService
from services.ia_service import IAService
from services.livro_service import LivroService
from services.usuario_service import UsuarioService
from services.autor_service import AutorService
from services.funcionario_service import FuncionarioService
from services.restaurador_service import RestauradorService
from services.co_autor_service import CoAutorService


class BibliotecaApp:
    def __init__(self):
        self.db_service = DatabaseService()
        self.conn = None
        self.emprestimo_service = None
        self.reserva_service = None
        self.comentario_service = None
        self.pontuacao_service = None
        self.query_service = None
        self.graphics_service = None
        self.ia_service = None
        self.livro_service = None
        self.usuario_service = None
        self.autor_service = None
        self.funcionario_service = None
        self.restaurador_service = None
        self.co_autor_service = None

    
    def conectar_banco(self):
        self.conn = self.db_service.connect()
        if self.conn:
            self.emprestimo_service = EmprestimoService(self.conn)
            self.reserva_service = ReservaService(self.conn)
            self.comentario_service = ComentarioService(self.conn)
            self.pontuacao_service = PontuacaoService(self.conn)
            self.query_service = QueryService(self.conn)
            self.graphics_service = GraphicsService(self.conn)
            self.livro_service = LivroService(self.conn)
            self.usuario_service = UsuarioService(self.conn)
            self.autor_service = AutorService(self.conn)
            self.funcionario_service = FuncionarioService(self.conn)
            self.restaurador_service = RestauradorService(self.conn)
            self.co_autor_service = CoAutorService(self.conn)

            self.ia_service = IAService()
            return True
        return False
    
    def menu_principal(self):
        while True:
            print("\n" + "="*50)
            print("🏛️  SISTEMA DE GERENCIAMENTO DE BIBLIOTECA")
            print("="*50)
            print("1. 📚 Gerenciar Empréstimos")
            print("2. 📋 Gerenciar Reservas") 
            print("3. 💬 Comentários e Resenhas")
            print("4. 🏆 Sistema de Pontuação")
            print("5. 🔍 Consultas e Relatórios")
            print("6. 📊 Gráficos e Estatísticas")
            print("7. 🤖 Recomendações IA")
            print("8. ⚙️  Configurações do Sistema")
            print("9. 📚 Gerenciar Livros")  
            print("10.👤 Gerenciar Usuários")
            print("11.👥 Gerenciar Funcionários") 
            print("12.📖 Gerenciar Autores")
            print("13.🚪 Sair")
            print("="*50)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == '1':
                self.menu_emprestimos()
            elif opcao == '2':
                self.menu_reservas()
            elif opcao == '3':
                self.menu_comentarios()
            elif opcao == '4':
                self.menu_pontuacao()
            elif opcao == '5':
                self.menu_consultas()
            elif opcao == '6':
                self.menu_graficos()
            elif opcao == '7':
                self.menu_ia()
            elif opcao == '8':
                self.menu_sistema()
            elif opcao == '9':
                self.menu_livros()
            elif opcao == '10':
                self.menu_usuarios()
            elif opcao == '11':
                self.menu_funcionarios()  
            elif opcao == '12':
                self.menu_autores()  
            elif opcao == '13':
                print("👋 Obrigado por usar o Sistema de Biblioteca!")
                break
            else:
                print("❌ Opção inválida! Tente novamente.")
    
    def menu_emprestimos(self):
        while True:
            print("\n📚 GERENCIAR EMPRÉSTIMOS")
            print("1. Realizar empréstimo")
            print("2. Devolver livro")
            print("3. Listar empréstimos ativos")
            print("4. Listar Livros Não Devolvidos")
            print("5. Voltar ao menu principal")
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == '1':
                try:
                    id_usuario = int(input("ID do usuário: "))
                    id_livro = int(input("ID do livro: "))
        
                    if self.emprestimo_service.realizar_emprestimo(id_usuario, id_livro):
                        # Adicionar pontos usando o PontuacaoService
                        self.pontuacao_service.processar_pontos_emprestimo(id_usuario)
                        
                except ValueError:
                    print("❌ Por favor, insira números válidos!")
                except Exception as e:
                    print(f"❌ Erro ao realizar empréstimo: {e}")
                    
            elif opcao == '2':
                try:
                    id_emprestimo = int(input("ID do empréstimo: "))
                    
                    # Primeiro, obter dados do empréstimo para pegar o ID do usuário
                    cursor = self.emprestimo_service.conn.cursor()
                    cursor.execute("""
                        SELECT Id_Usuario, Data_Prevista_Devolucao 
                        FROM Emprestimo 
                        WHERE Id_Emprestimo = %s AND Devolvido = FALSE
                    """, (id_emprestimo,))
                    
                    emprestimo_data = cursor.fetchone()
                    cursor.close()
                    
                    if emprestimo_data:
                        id_usuario = emprestimo_data[0]
                        data_prevista = emprestimo_data[1]
                        
                        # Devolver o livro
                        if self.emprestimo_service.devolver_livro(id_emprestimo):
                            # Verificar se foi devolvido no prazo
                            from datetime import datetime
                            data_devolucao = datetime.now().date()
                            
                            if data_devolucao <= data_prevista:
                                # Só adiciona pontos se devolveu no prazo
                                self.pontuacao_service.processar_pontos_devolucao_prazo(id_usuario)
                            else:
                                print("📅 Livro devolvido com atraso - sem pontos por devolução no prazo")
                    else:
                        print("❌ Empréstimo não encontrado ou já devolvido!")
                        
                except ValueError:
                    print("❌ Por favor, insira um número válido!")
                except Exception as e:
                    print(f"❌ Erro ao devolver livro: {e}")
                    
            elif opcao == '3':
                try:
                    self.query_service.consulta_emprestimos_ativos()
                except Exception as e:
                    print(f"❌ Erro ao listar empréstimos ativos: {e}")
                    
            elif opcao == '4':
                try:
                    self.emprestimo_service.listar_livros_nao_devolvidos()
                except Exception as e:
                    print(f"❌ Erro ao listar livros não devolvidos: {e}")
                    
            elif opcao == '5':
                break
                
            else:
                print("❌ Opção inválida!")

    def menu_reservas(self):
        while True:
            print("\n📋 GERENCIAR RESERVAS")
            print("1. Fazer reserva")
            print("2. Cancelar reserva")
            print("3. Listar minhas reservas")
            print("4. Excluir Reserva")
            print("5. Voltar ao menu principal")
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == '1':
                id_usuario = int(input("ID do usuário: "))
                id_livro = int(input("ID do livro: "))
                self.reserva_service.fazer_reserva(id_usuario, id_livro)
            elif opcao == '2':
                id_reserva = int(input("ID da reserva: "))
                self.reserva_service.cancelar_reserva(id_reserva)
            elif opcao == '3':
                id_usuario = int(input("ID do usuário: "))
                self.reserva_service.listar_reservas_usuario(id_usuario)
            elif opcao == '4':
                id_reserva = int(input("ID da reserva a ser excluída: "))
                self.reserva_service.excluir_reserva(id_reserva)
            elif opcao == '5':
                break
            else:
                print("❌ Opção inválida!")
    
    def menu_comentarios(self):
        while True:
            print("\n💬 COMENTÁRIOS E RESENHAS")
            print("1. Adicionar comentário")
            print("2. Escrever resenha")
            print("3. Ver comentários de um livro")
            print("4. Ver resenhas de um livro")
            print("5. Curtir resenha")
            print("6. Voltar ao menu principal")
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == '1':
                try:
                    id_usuario = int(input("ID do usuário: "))
                    id_livro = int(input("ID do livro: "))
                    texto = input("Comentário: ")
                    
                    # Adicionar comentário e pontos apenas se for bem-sucedido
                    if self.comentario_service.adicionar_comentario(id_usuario, id_livro, texto):
                        self.pontuacao_service.processar_pontos_comentario(id_usuario)
                        
                except ValueError:
                    print("❌ Por favor, insira números válidos!")
                except Exception as e:
                    print(f"❌ Erro ao adicionar comentário: {e}")
                    
            elif opcao == '2':
                try:
                    id_usuario = int(input("ID do usuário: "))
                    id_livro = int(input("ID do livro: "))
                    resenha = input("Resenha: ")
                    
                    # Adicionar resenha
                    resultado = self.comentario_service.adicionar_resenha(id_usuario, id_livro, resenha)
                    
                    # Só dar pontos se for uma resenha nova (não atualização)
                    if resultado.get('sucesso') and resultado.get('nova_resenha'):
                        self.pontuacao_service.processar_pontos_resenha(id_usuario)
                    elif resultado.get('sucesso') and not resultado.get('nova_resenha'):
                        print("ℹ️  Resenha atualizada - sem pontos adicionais")
                        
                except ValueError:
                    print("❌ Por favor, insira números válidos!")
                except Exception as e:
                    print(f"❌ Erro ao escrever resenha: {e}")
                    
            elif opcao == '3':
                try:
                    id_livro = int(input("ID do livro: "))
                    self.comentario_service.listar_comentarios_livro(id_livro)
                except ValueError:
                    print("❌ Por favor, insira um número válido!")
                except Exception as e:
                    print(f"❌ Erro ao listar comentários: {e}")
                    
            elif opcao == '4':
                try:
                    id_livro = int(input("ID do livro: "))
                    self.comentario_service.listar_resenhas_livro(id_livro)
                except ValueError:
                    print("❌ Por favor, insira um número válido!")
                except Exception as e:
                    print(f"❌ Erro ao listar resenhas: {e}")
                    
            elif opcao == '5':
                try:
                    id_usuario = int(input("ID do usuário (autor da resenha): "))
                    id_livro = int(input("ID do livro: "))
                    self.comentario_service.curtir_resenha(id_usuario, id_livro)
                except ValueError:
                    print("❌ Por favor, insira números válidos!")
                except Exception as e:
                    print(f"❌ Erro ao curtir resenha: {e}")
                    
            elif opcao == '6':
                break
                
            else:
                print("❌ Opção inválida!")

    def menu_pontuacao(self):
        while True:
            print("\n🏆 SISTEMA DE PONTUAÇÃO")
            print("1. Ver minha pontuação")
            print("2. Ver histórico de pontos")
            print("3. Atualizar ranking")
            print("4. Adicionar pontos manualmente")
            print("5. Voltar ao menu principal")
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == '1':
                id_usuario = int(input("ID do usuário: "))
                pontos = self.pontuacao_service.obter_pontuacao_usuario(id_usuario)
                print(f"🏆 Sua pontuação total: {pontos} pontos")
            elif opcao == '2':
                id_usuario = int(input("ID do usuário: "))
                self.pontuacao_service.obter_historico_pontuacao(id_usuario)
            elif opcao == '3':
                self.pontuacao_service.atualizar_ranking()
            elif opcao == '4':
                id_usuario = int(input("ID do usuário: "))
                motivo = input("Motivo: ")
                pontos = int(input("Pontos: "))
                self.pontuacao_service.adicionar_pontos(id_usuario, motivo, pontos)
            elif opcao == '5':
                break
            else:
                print("❌ Opção inválida!")
    
    def menu_consultas(self):
        while True:
            print("\n🔍 CONSULTAS E RELATÓRIOS")
            print("1. Livros disponíveis")
            print("2. Empréstimos ativos")
            print("3. Usuários com multa")
            print("4. Livros mais populares")
            print("5. Buscar por palavra-chave")
            print("6. Voltar ao menu principal")
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == '1':
                self.query_service.consulta_livros_disponiveis()
            elif opcao == '2':
                self.query_service.consulta_emprestimos_ativos()
            elif opcao == '3':
                self.query_service.consulta_usuarios_com_multa()
            elif opcao == '4':
                limite = int(input("Quantos livros mostrar (padrão 10): ") or "10")
                self.query_service.consulta_livros_mais_populares(limite)
            elif opcao == '5':
                palavra = input("Digite a palavra-chave: ")
                self.query_service.buscar_livros_por_palavra_chave(palavra)
            elif opcao == '6':
                break
            else:
                print("❌ Opção inválida!")
    
    def menu_graficos(self):
        while True:
            print("\n📊 GRÁFICOS E ESTATÍSTICAS")
            print("1. Livros mais emprestados")
            print("2. Empréstimos por categoria")
            print("3. Ranking de usuários")
            print("4. Evolução da pontuação dos usuários")
            print("5. Voltar ao menu principal")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == '1':
                self.graphics_service.grafico_livros_mais_emprestados()
            elif opcao == '2':
                self.graphics_service.grafico_emprestimos_por_categoria()
            elif opcao == '3':
                self.graphics_service.grafico_ranking_usuarios()
            elif opcao == '4':
                self.graphics_service.grafico_pontuacao_usuarios()
            elif opcao == '5':
                break
            else:
                print("❌ Opção inválida!")
    
    def menu_ia(self):
        print("\n🤖 Bem-vindo ao Assistente IA da Biblioteca!")
        print("Você pode pedir recomendações ou sugestões de resenha a qualquer momento.")

        while True:
            print("\nO que você deseja fazer?")
            print("1. 📚 Recomendar livros")
            print("2. ✍️ Sugerir comentário/resenha")
            print("3. 💡 Perguntar algo sobre livros (prompt personalizado)")
            print("4. 🚪 Sair")

            opcao = input("Escolha uma opção: ").strip()

            if opcao == '1':
                id_usuario = int(input("Digite o ID do usuário: "))
                recomendacao = self.ia_service.recomendar_livros(self.conn, id_usuario)
                print(f"\n🔎 Recomendação:\n{recomendacao}")

            elif opcao == '2':
                id_usuario = int(input("Digite o ID do usuário: "))
                id_livro = int(input("Digite o ID do livro: "))
                sugestao = self.ia_service.sugerir_comentario_resenha(self.conn, id_usuario, id_livro)
                print(f"\n📝 Sugestão de comentário/resenha:\n{sugestao}")

            elif opcao == '3':
                id_usuario = int(input("Digite o ID do usuário: "))
                print("\n💡 Digite sua pergunta ou solicitação sobre livros:")
                print("Exemplos:")
                print("- 'Me recomende livros de ficção científica brasileira'")
                print("- 'Quais são os principais autores da literatura modernista?'")
                print("- 'Explique o simbolismo em Dom Casmurro'")
                prompt = input("\nSua pergunta: ").strip()
                resposta = self.ia_service.gerar_resposta_personalizada(self.conn, id_usuario, prompt)
                print(f"\n🤖 Resposta:\n{resposta}")

            elif opcao == '4':
                print("👋 Encerrando o assistente IA. Até a próxima!")
                break

            else:
                print("❌ Opção inválida! Tente novamente.")

    def menu_sistema(self):
        while True:
            print("\n⚙️ CONFIGURAÇÕES DO SISTEMA")
            print("1. Criar tabelas")
            print("2. Inserir dados de exemplo")
            print("3. Remover tabelas")
            print("4. Consultar tabela")
            print("5. Atualizar valor específico")
            print("6. Voltar ao menu principal")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == '1':
                self.db_service.create_all_tables(self.conn)
            elif opcao == '2':
                self.db_service.insert_sample_data(self.conn)
            elif opcao == '3':
                self.db_service.drop_all_tables(self.conn)
            elif opcao == '4':
                tabela = input("Digite o nome da tabela: ")
                self.db_service.show_table(self.conn, tabela)
            elif opcao == '5':
                tabela = input("Digite o nome da tabela: ")
                atributo = input("Digite o nome do atributo a ser atualizado: ")
                valor = input("Digite o novo valor: ")
                pk_coluna = input("Digite o nome da coluna da chave primária: ")
                pk_valor = input("Digite o valor da chave primária: ")
                self.db_service.update_value(self.conn, tabela, atributo, valor, pk_coluna, pk_valor)
            elif opcao == '6':
                break
            else:
                print("❌ Opção inválida!")
   
    def menu_livros(self):
        while True:
            print("\n📚 GERENCIAR LIVROS")
            print("1. Adicionar Livro")
            print("2. Atualizar Informações do Livro")
            print("3. Atualizar Status do Livro")
            print("4. Atualizar Quantidade de Exemplares")
            print("5. Remover Livro")
            print("6. Listar Livros")
            print("7. Buscar Livro por ID")
            print("8. Voltar ao menu principal")

            opcao = input("Escolha uma opção: ").strip()

            if opcao == '1':
                titulo = input("Título do livro: ")
                status = input("Status do livro (disponível, emprestado, reservado): ")
                ano_publicacao = int(input("Ano de publicação: "))
                id_editora = int(input("ID da editora: "))
                id_categoria = int(input("ID da categoria: "))
                quantidade_exemplares = int(input("Quantidade de exemplares: "))
                self.livro_service.adicionar_livro(titulo, status, ano_publicacao, id_editora, id_categoria, quantidade_exemplares)

            elif opcao == '2':
                id_livro = int(input("ID do livro a ser atualizado: "))
                titulo = input("Novo título (deixe em branco para não alterar): ")
                titulo = titulo if titulo else None
                ano_publicacao = input("Novo ano de publicação (deixe em branco para não alterar): ")
                ano_publicacao = int(ano_publicacao) if ano_publicacao else None
                id_editora = input("Novo ID da editora (deixe em branco para não alterar): ")
                id_editora = int(id_editora) if id_editora else None
                id_categoria = input("Novo ID da categoria (deixe em branco para não alterar): ")
                id_categoria = int(id_categoria) if id_categoria else None
                self.livro_service.atualizar_livro(id_livro, titulo, ano_publicacao, id_editora, id_categoria)

            elif opcao == '3':
                id_livro = int(input("ID do livro a ter o status atualizado: "))
                status = input("Novo status (disponível, emprestado, reservado): ")
                self.livro_service.atualizar_status_livro(id_livro, status)

            elif opcao == '4':
                id_livro = int(input("ID do livro a ter a quantidade de exemplares atualizada: "))
                quantidade_exemplares = int(input("Nova quantidade de exemplares: "))
                self.livro_service.atualizar_quantidade_exemplares(id_livro, quantidade_exemplares)

            elif opcao == '5':
                id_livro = int(input("ID do livro a ser removido: "))
                self.livro_service.remover_livro(id_livro)

            elif opcao == '6':
                livros = self.livro_service.listar_livros()
                if livros:
                    print("\n=== LISTA DE LIVROS ===")
                    for livro in livros:
                        print(f"ID: {livro[0]}, Título: {livro[1]}, Status: {livro[2]}, Ano: {livro[3]}, Editora ID: {livro[4]}, Categoria ID: {livro[5]}, Quantidade de Exemplares: {livro[6]}")

            elif opcao == '7':
                id_livro = int(input("ID do livro: "))
                livro = self.livro_service.buscar_livro_por_id(id_livro)
                if livro:
                    print(f"ID: {livro[0]}, Título: {livro[1]}, Status: {livro[2]}, Ano: {livro[3]}, Editora ID: {livro[4]}, Categoria ID: {livro[5]}, Quantidade de Exemplares: {livro[6]}")

            elif opcao == '8':
                break

            else:
                print("❌ Opção inválida! Por favor, escolha uma opção válida.")

    def menu_usuarios(self):
        while True:
            print("\n👤 GERENCIAR USUÁRIOS")
            print("1. Adicionar Usuário")
            print("2. Atualizar Usuário")
            print("3. Remover Usuário")
            print("4. Listar Usuários")
            print("5. Buscar Usuário por ID")
            print("6. Voltar ao menu principal")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == '1':
                nome = input("Nome do usuário: ")
                cpf = input("CPF do usuário: ")
                telefone = input("Telefone do usuário: ")
                email = input("Email do usuário: ")
                tipo_usuario = input("Tipo de usuário: ")
                id_categoria = int(input("ID da categoria: "))
                self.usuario_service.adicionar_usuario(nome, cpf, telefone, email, tipo_usuario, id_categoria)
            elif opcao == '2':
                id_usuario = int(input("ID do usuário a ser atualizado: "))
                nome = input("Novo nome (deixe em branco para não alterar): ")
                nome = nome if nome else None
                telefone = input("Novo telefone (deixe em branco para não alterar): ")
                telefone = telefone if telefone else None
                email = input("Novo email (deixe em branco para não alterar): ")
                email = email if email else None
                tipo_usuario = input("Novo tipo de usuário (deixe em branco para não alterar): ")
                tipo_usuario = tipo_usuario if tipo_usuario else None
                id_categoria = input("Novo ID da categoria (deixe em branco para não alterar): ")
                id_categoria = int(id_categoria) if id_categoria else None
                self.usuario_service.atualizar_usuario(id_usuario, nome, telefone, email, tipo_usuario, id_categoria)
            elif opcao == '3':
                id_usuario = int(input("ID do usuário a ser removido: "))
                self.usuario_service.remover_usuario(id_usuario)
            elif opcao == '4':
                self.usuario_service.listar_usuarios()
            elif opcao == '5':
                id_usuario = int(input("ID do usuário: "))
                self.usuario_service.buscar_usuario_por_id(id_usuario)
            elif opcao == '6':
                break
            else:
                print("❌ Opção inválida!") 
    def menu_funcionarios(self):
        while True:
            print("\n👥 GERENCIAR FUNCIONÁRIOS")
            print("1. Adicionar Funcionário")
            print("2. Atualizar Funcionário")
            print("3. Remover Funcionário")
            print("4. Listar Funcionários")
            print("5. Voltar ao menu principal")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == '1':
                nome = input("Nome do funcionário: ")
                cargo = input("Cargo do funcionário: ")
                self.funcionario_service.adicionar_funcionario(nome, cargo)
            elif opcao == '2':
                id_funcionario = int(input("ID do funcionário a ser atualizado: "))
                nome = input("Novo nome (deixe em branco para não alterar): ")
                nome = nome if nome else None
                cargo = input("Novo cargo (deixe em branco para não alterar): ")
                cargo = cargo if cargo else None
                self.funcionario_service.atualizar_funcionario(id_funcionario, nome, cargo)
            elif opcao == '3':
                id_funcionario = int(input("ID do funcionário a ser removido: "))
                self.funcionario_service.remover_funcionario(id_funcionario)
            elif opcao == '4':
                self.funcionario_service.listar_funcionarios()
            elif opcao == '5':
                break
            else:
                print("❌ Opção inválida!")
    def menu_autores(self):
        while True:
            print("\n📚 GERENCIAR AUTORES")
            print("1. Adicionar Autor")
            print("2. Atualizar Autor")
            print("3. Remover Autor")
            print("4. Listar Autores")
            print("5. Voltar ao menu principal")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == '1':
                nome = input("Nome do autor: ")
                self.autor_service.adicionar_autor(nome)
            elif opcao == '2':
                id_autor = int(input("ID do autor a ser atualizado: "))
                nome = input("Novo nome (deixe em branco para não alterar): ")
                nome = nome if nome else None
                self.autor_service.atualizar_autor(id_autor, nome)
            elif opcao == '3':
                id_autor = int(input("ID do autor a ser removido: "))
                self.autor_service.remover_autor(id_autor)
            elif opcao == '4':
                self.autor_service.listar_autores()
            elif opcao == '5':
                break
            else:
                print("❌ Opção inválida!")    
                    
if __name__ == "__main__":
    app = BibliotecaApp()
    if app.conectar_banco():
        app.menu_principal()
