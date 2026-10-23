# =============================================================================
# models/tables.py
# Definições das tabelas e operações CRUD
# =============================================================================
class BibliotecaTables:
    def __init__(self):
        self.tables = {
            # Definições das tabelas 
            'categoria': """CREATE TABLE IF NOT EXISTS Categoria (
                Id_Categoria SERIAL PRIMARY KEY,
                Nome VARCHAR(100) NOT NULL,
                Limite_Emprestimos INTEGER,
                Dias_Prazo INTEGER,
                Valor_Multa_Dia NUMERIC(8,2)
            )""",
            
            'usuario': """CREATE TABLE IF NOT EXISTS Usuario (
                Id_Usuario SERIAL PRIMARY KEY,
                Nome VARCHAR(100) NOT NULL,
                CPF CHAR(11) UNIQUE NOT NULL,
                Telefone VARCHAR(15),
                Email VARCHAR(100),
                Tipo_Usuario VARCHAR(30),
                Status VARCHAR(10) DEFAULT 'ativo',
                Id_Categoria INTEGER REFERENCES Categoria(Id_Categoria)
            )""",
            'pontuacao': """CREATE TABLE IF NOT EXISTS Pontuacao (
                Id_Pontuacao SERIAL PRIMARY KEY,
                Id_Usuario INTEGER REFERENCES Usuario(Id_Usuario) ,
                Motivo TEXT,
                Pontos INTEGER,
                Data_Pontuacao DATE
            )""",
            
            'ranking': """CREATE TABLE IF NOT EXISTS Ranking (
                Id_Ranking SERIAL PRIMARY KEY,
                Id_Usuario INTEGER REFERENCES Usuario(Id_Usuario),
                Categoria VARCHAR(50),
                Pontos INTEGER,
                Periodo VARCHAR(20),
                Data DATE
            )""",
            
            'editora': """CREATE TABLE IF NOT EXISTS Editora (
                Id_Editora SERIAL PRIMARY KEY,
                Nome VARCHAR(100),
                Data_Edicao DATE
            )""",
            
            'livro': """CREATE TABLE IF NOT EXISTS Livro (
                Id_Livro SERIAL PRIMARY KEY,
                Titulo VARCHAR(200),
                Status VARCHAR(20) DEFAULT 'disponivel',
                Ano_Publicacao INTEGER,
                Id_Editora INTEGER REFERENCES Editora(Id_Editora),
                Id_Categoria INTEGER REFERENCES Categoria(Id_Categoria),
                Quantidade_Exemplares INTEGER DEFAULT 1
            )""",
            
            'autor': """CREATE TABLE IF NOT EXISTS Autor (
                Id_Autor SERIAL PRIMARY KEY,
                Nome VARCHAR(100)
            )""",
            
            'co_autor': """CREATE TABLE IF NOT EXISTS Co_Autor (
                Id_Livro INTEGER REFERENCES Livro(Id_Livro),
                Id_Autor INTEGER REFERENCES Autor(Id_Autor),
                Data_Publicacao DATE,
                PRIMARY KEY (Id_Livro, Id_Autor)
            )""",
            
            'funcionario': """CREATE TABLE IF NOT EXISTS Funcionario (
                Id_Funcionario SERIAL PRIMARY KEY,
                Nome VARCHAR(100),
                Cargo VARCHAR(50)
            )""",
            
            'restaurador': """CREATE TABLE IF NOT EXISTS Restaurador (
                Id_Restaurador SERIAL PRIMARY KEY,
                Nome VARCHAR(100),
                Data_Restaurador DATE
            )""",
            
            'livro_restaurado': """CREATE TABLE IF NOT EXISTS Livro_Restaurado (
                Id_Livro INTEGER REFERENCES Livro(Id_Livro),
                Id_Restaurador INTEGER REFERENCES Restaurador(Id_Restaurador),
                Descricao TEXT,
                Data DATE,
                PRIMARY KEY (Id_Livro, Id_Restaurador)
            )""",
            
            'emprestimo': """CREATE TABLE IF NOT EXISTS Emprestimo (
                Id_Emprestimo SERIAL PRIMARY KEY,
                Id_Usuario INTEGER REFERENCES Usuario(Id_Usuario),
                Id_Livro INTEGER REFERENCES Livro(Id_Livro),
                Data_Emprestimo DATE,
                Data_Prevista_Devolucao DATE,
                Data_Devolucao DATE,
                Devolvido BOOLEAN DEFAULT FALSE,
                Multa NUMERIC(8,2),
                Status VARCHAR(20) CHECK (Status IN ('ativa', 'Em atraso', 'Finalizado'))
            )""",
            
            'reserva': """CREATE TABLE IF NOT EXISTS Reserva (
                Id_Reserva SERIAL PRIMARY KEY,
                Id_Usuario INTEGER REFERENCES Usuario(Id_Usuario),
                Id_Livro INTEGER REFERENCES Livro(Id_Livro),
                Data DATE,
                Status VARCHAR(20) DEFAULT 'ativo'
            )""",
            
            'comentario': """CREATE TABLE IF NOT EXISTS Comentario (
                Id_Comentario SERIAL PRIMARY KEY,
                Id_Usuario INTEGER REFERENCES Usuario(Id_Usuario),
                Id_Livro INTEGER REFERENCES Livro(Id_Livro),
                Texto TEXT,
                Data_Comentario DATE DEFAULT CURRENT_DATE
            )""",
            
            'resenha': """CREATE TABLE IF NOT EXISTS Resenha (
                Id_Usuario INTEGER REFERENCES Usuario(Id_Usuario),
                Id_Livro INTEGER REFERENCES Livro(Id_Livro),
                Resenha TEXT,
                Curtidas INTEGER DEFAULT 0,
                PRIMARY KEY (Id_Usuario, Id_Livro)
            )""",
            
            'palavra_chave': """CREATE TABLE IF NOT EXISTS Palavra_Chave (
                Id_Chave SERIAL PRIMARY KEY,
                Palavra VARCHAR(100)
            )""",
            
            'livro_palavrachave': """CREATE TABLE IF NOT EXISTS Livro_PalavraChave (
                Id_Livro INTEGER REFERENCES Livro(Id_Livro),
                Id_Chave INTEGER REFERENCES Palavra_Chave(Id_Chave),
                PRIMARY KEY (Id_Livro, Id_Chave)
            )"""
        }

        self.inserts = {
            'categoria': """INSERT INTO Categoria (Nome, Limite_Emprestimos, Dias_Prazo, Valor_Multa_Dia) VALUES
                ('Estudante', 5, 15, 2.00),
                ('Professor', 10, 30, 1.50),
                ('Funcionário', 7, 21, 2.50),
                ('Pesquisador', 8, 25, 1.80),
                ('Visitante', 2, 7, 3.00),
                ('Graduado', 6, 20, 2.20),
                ('Pós-Graduado', 12, 35, 1.20),
                ('Senior', 15, 45, 1.00),
                ('Premium', 20, 60, 0.50),
                ('VIP', 25, 90, 0.25);""",

            'usuario': """INSERT INTO Usuario (Nome, CPF, Telefone, Email, Tipo_Usuario, Status, Id_Categoria) VALUES
                ('Maria Silva', '12345678901', '48999887766', 'maria.silva@email.com', 'Estudante', 'ativo', 1),
                ('João Santos', '23456789012', '48988776655', 'joao.santos@email.com', 'Professor', 'ativo', 2),
                ('Ana Costa', '34567890123', '48977665544', 'ana.costa@email.com', 'Funcionário', 'ativo', 3),
                ('Pedro Lima', '45678901234', '48966554433', 'pedro.lima@email.com', 'Estudante', 'ativo', 1),
                ('Carla Nunes', '56789012345', '48955443322', 'carla.nunes@email.com', 'Pesquisador', 'ativo', 4),
                ('Lucas Oliveira', '67890123456', '48944332211', 'lucas.oliveira@email.com', 'Graduado', 'ativo', 6),
                ('Sofia Pereira', '78901234567', '48933221100', 'sofia.pereira@email.com', 'Pós-Graduado', 'ativo', 7),
                ('Diego Martins', '89012345678', '48922110099', 'diego.martins@email.com', 'Senior', 'inativo', 8),
                ('Juliana Rocha', '90123456789', '48911009988', 'juliana.rocha@email.com', 'Premium', 'ativo', 9),
                ('Roberto Alves', '01234567890', '48900998877', 'roberto.alves@email.com', 'VIP', 'ativo', 10),
                ('João Pinto Ferreira', '11432153115', '48988085262', 'jocifer@gmail.com', 'Visitante', 'ativo', 5);""",
            
            'pontuacao': """INSERT INTO Pontuacao (Id_Usuario, Motivo, Pontos, Data_Pontuacao) VALUES
                (1, 'Empréstimo realizado', 10, '2024-01-15'),
                (2, 'Devolução antecipada', 15, '2024-01-20'),
                (3, 'Primeira utilização', 5, '2024-01-25'),
                (4, 'Empréstimo de livro raro', 20, '2024-02-01'),
                (5, 'Participação em evento', 25, '2024-02-05'),
                (6, 'Resenha publicada', 12, '2024-02-10'),
                (7, 'Comentário útil', 8, '2024-02-15'),
                (8, 'Indicação de novo usuário', 30, '2024-02-20'),
                (9, 'Uso frequente', 18, '2024-02-25'),
                (10, 'Feedback positivo', 22, '2024-03-01'),
                (11, 'Recomendação de livro', 10, '2024-03-05');""",
            

            'ranking': """INSERT INTO Ranking (Id_Usuario, Categoria, Pontos, Periodo, Data) VALUES
                (1, 'Estudante', 45, 'Janeiro 2025', '2025-01-31'),
                (2, 'Professor', 52, 'Janeiro 2025', '2025-01-31'),
                (3, 'Funcionário', 38, 'Janeiro 2024', '2024-01-31'),
                (4, 'Estudante', 25, 'Fevereiro 2025', '2025-02-28'),
                (5, 'Pesquisador', 30, 'Fevereiro 2024', '2024-02-28'),
                (6, 'Graduado', 95, 'Marco 2024', '2024-03-31'),
                (7, 'Pós-Graduado', 88, 'Marco 2024', '2024-03-31'),
                (8, 'Senior', 180, 'Dezembro 2023', '2023-12-31'),
                (9, 'Premium', 220, 'Dezembro 2023', '2023-12-31'),
                (10, 'VIP', 90, 'Fevereiro 2024', '2024-02-29'),
                (11, 'Visitante', 15, 'Janeiro 2024', '2024-01-31');""",

            'editora': """INSERT INTO Editora (Nome, Data_Edicao) VALUES
                ('Companhia das Letras', '1986-03-15'),
                ('Record', '1942-05-20'),
                ('Globo Livros', '2000-08-10'),
                ('Saraiva', '1906-01-01'),
                ('Abril', '1950-04-18'),
                ('Rocco', '1975-09-12'),
                ('Objetiva', '1987-11-25'),
                ('Sextante', '2001-07-08'),
                ('Intrínseca', '2007-03-22'),
                ('Suma de Letras', '2003-06-30');""",

            'autor': """INSERT INTO Autor (Nome) VALUES
                ('Machado de Assis'),
                ('Clarice Lispector'),
                ('Jorge Amado'),
                ('Graciliano Ramos'),
                ('José Saramago'),
                ('Gabriel García Márquez'),
                ('Isabel Allende'),
                ('Mario Vargas Llosa'),
                ('Paulo Coelho'),
                ('Lygia Fagundes Telles');""",

            'livro': """INSERT INTO Livro (Titulo, Status, Ano_Publicacao, Id_Editora, Id_Categoria,Quantidade_Exemplares) VALUES
                ('Dom Casmurro', 'disponível', 1899, 1, 1, 5),
                ('A Hora da Estrela', 'emprestado', 1977, 2, 10, 5),
                ('Gabriela, Cravo e Canela', 'disponível', 1958, 3, 2, 10),
                ('Vidas Secas', 'disponível', 1938, 4, 1, 3),
                ('O Evangelho Segundo Jesus Cristo', 'reservado', 1991, 5, 2, 4),
                ('Cem Anos de Solidão', 'disponível', 1967, 6, 3, 6),
                ('A Casa dos Espíritos', 'emprestado', 1982, 7, 3, 7),
                ('A Festa do Bode', 'disponível', 2000, 8, 4, 8),
                ('O Alquimista', 'disponível', 1988, 9, 5, 10),
                ('As Meninas', 'disponível', 1973, 10, 1, 9);""",   

            'co_autor': """INSERT INTO Co_Autor (Id_Livro, Id_Autor, Data_Publicacao) VALUES
                (1, 1, '1899-12-01'),
                (2, 2, '1977-10-15'),
                (3, 3, '1958-08-20'),
                (4, 4, '1938-07-12'),
                (5, 5, '1991-11-08'),
                (6, 6, '1967-05-30'),
                (7, 7, '1982-03-28'),
                (8, 8, '2000-09-15'),
                (9, 9, '1988-04-11'),
                (10, 10, '1973-06-25');""",

            'funcionario': """INSERT INTO Funcionario (Nome, Cargo) VALUES
                ('Carlos Mendes', 'Bibliotecário'),
                ('Fernanda Cruz', 'Assistente de Biblioteca'),
                ('Ricardo Souza', 'Coordenador de Acervo'),
                ('Patrícia Gomes', 'Atendente'),
                ('Marcos Vieira', 'Técnico em Biblioteconomia'),
                ('Luana Barbosa', 'Catalogadora'),
                ('André Ferreira', 'Supervisor'),
                ('Cristina Dias', 'Auxiliar Administrativa'),
                ('Paulo Cardoso', 'Gerente de Biblioteca'),
                ('Vanessa Ramos', 'Especialista em Informação');""",

            'restaurador': """INSERT INTO Restaurador (Nome, Data_Restaurador) VALUES
                ('Alberto Restaurações', '2020-01-15'),
                ('Maria Conservação', '2021-03-22'),
                ('José Preservação', '2019-08-10'),
                ('Atelier do Livro', '2022-05-18'),
                ('Oficina Literária', '2020-11-30'),
                ('Workshop da Restauração', '2021-07-25'),
                ('Estúdio do Papel', '2023-02-14'),
                ('Casa da Encadernação', '2019-12-08'),
                ('Laboratório Textual', '2022-09-12'),
                ('Centro de Conservação', '2020-06-05');""",

            'livro_restaurado': """INSERT INTO Livro_Restaurado (Id_Livro, Id_Restaurador, Descricao, Data) VALUES
                (1, 1, 'Restauração da capa', '2023-01-15'),
                (2, 2, 'Reparo na lombada', '2023-02-20'),
                (3, 3, 'Limpeza e conservação', '2023-03-10'),
                (4, 4, 'Substituição de páginas', '2023-04-05'),
                (5, 5, 'Restauração completa', '2023-05-12'),
                (6, 6, 'Tratamento contra fungos', '2023-06-18'),
                (7, 7, 'Consolidação das folhas', '2023-07-22'),
                (8, 8, 'Restauração da contracapa', '2023-08-30'),
                (9, 9, 'Limpeza e desacidificação', '2023-09-15'),
                (10, 10, 'Reparo em rasgos', '2023-10-25');""",

            'emprestimo': """INSERT INTO Emprestimo (Id_Usuario, Id_Livro, Data_Emprestimo, Data_Prevista_Devolucao, Data_Devolucao, Devolvido, Multa, Status) VALUES
                (1, 2, '2024-01-10', '2024-01-25', '2024-01-24', TRUE, 0.00, 'Finalizado'),
                (2, 7, '2024-01-15', '2024-02-14', NULL, FALSE, 0.00, 'ativa'),
                (3, 1, '2024-01-20', '2024-02-10', '2024-02-12', TRUE, 4.00, 'Finalizado'),
                (4, 3, '2024-01-25', '2024-02-09', NULL, FALSE, 0.00, 'ativa'),
                (5, 4, '2024-02-01', '2024-02-26', NULL, FALSE, 0.00, 'ativa'),
                (6, 6, '2024-02-05', '2024-02-25', '2024-02-23', TRUE, 0.00, 'Finalizado'),
                (7, 8, '2024-02-10', '2024-03-12', NULL, FALSE, 0.00, 'ativa'),
                (8, 9, '2024-02-15', '2024-03-30', '2024-04-05', TRUE, 12.00, 'Finalizado'),
                (9, 10, '2024-02-20', '2024-04-20', NULL, FALSE, 0.00, 'ativa'),
                (10, 1, '2024-02-25', '2024-03-11', NULL, FALSE, 15.00, 'Em atraso'),
                (11, 5, '2024-03-01', '2024-03-15', NULL, FALSE, 0.00, 'ativa');""",

            'reserva': """INSERT INTO Reserva (Id_Usuario, Id_Livro, Data, Status) VALUES
                (1, 5, '2024-01-12', 'ativo'),
                (2, 2, '2024-01-18', 'cancelado'),
                (3, 7, '2024-01-22', 'atendido'),
                (4, 1, '2024-01-28', 'ativo'),
                (5, 3, '2024-02-03', 'ativo'),
                (6, 8, '2024-02-08', 'atendido'),
                (7, 9, '2024-02-12', 'ativo'),
                (8, 4, '2024-02-18', 'cancelado'),
                (9, 6, '2024-02-22', 'ativo'),
                (10, 10, '2024-02-28', 'ativo'),
                (11, 1, '2024-03-05', 'ativo');""",

            'comentario': """INSERT INTO Comentario (Id_Usuario, Id_Livro, Texto, Data_Comentario) VALUES
                (1, 1, 'Ótimo livro!', '2024-01-26'),
                (2, 2, 'Muito interessante.', '2024-02-01'),
                (3, 3, 'Excelente leitura.', '2024-02-05'),
                (4, 4, 'Muito tocante.', '2024-02-10'),
                (5, 5, 'Livro fascinante.', '2024-02-15'),
                (6, 6, 'Recomendo a todos.', '2024-02-20'),
                (7, 7, 'Excelente narrativa.', '2024-02-25'),
                (8, 8, 'Livro envolvente.', '2024-03-01'),
                (9, 9, 'Leitura inspiradora.', '2024-03-05'),
                (10, 10, 'Muito bom!', '2024-03-10'),
                (11, 1, 'Muito interessante.', '2024-03-15');""",

            'resenha': """INSERT INTO Resenha (Id_Usuario, Id_Livro, Resenha, Curtidas) VALUES
                (1, 1, 'Dom Casmurro é um clássico da literatura brasileira.', 25),
                (2, 2, 'A Hora da Estrela é uma obra-prima de Clarice Lispector.', 18),
                (3, 3, 'Gabriela, Cravo e Canela é uma celebração da cultura baiana.', 32),
                (4, 4, 'Vidas Secas é um retrato brutal da seca no nordeste.', 22),
                (5, 5, 'O Evangelho Segundo Jesus Cristo é uma releitura ousada.', 15),
                (6, 6, 'Cem Anos de Solidão é o épico do realismo mágico.', 45),
                (7, 7, 'A Casa dos Espíritos mistura política e magia de forma magistral.', 28),
                (8, 8, 'A Festa do Bode é um thriller político fascinante.', 19),
                (9, 9, 'O Alquimista é uma fábula moderna sobre seguir os sonhos.', 67),
                (10, 10, 'As Meninas é um retrato fino da juventude burguesa.', 31),
                (11, 1, 'Dom Casmurro é uma obra que explora a dúvida e a traição de forma magistral.', 20);""",

            'palavra_chave': """INSERT INTO Palavra_Chave (Palavra) VALUES
                ('Romance'),
                ('Literatura Brasileira'),
                ('Realismo'),
                ('Drama'),
                ('Ficção'),
                ('Clássico'),
                ('Modernismo'),
                ('Regionalismo'),
                ('Psicológico'),
                ('Social');""",

            'livro_palavrachave': """INSERT INTO Livro_PalavraChave (Id_Livro, Id_Chave) VALUES
                (1, 1), (1, 2), (1, 3),
                (2, 2), (2, 7), (2, 9),
                (3, 1), (3, 2), (3, 8),
                (4, 2), (4, 8), (4, 10),
                (5, 5), (5, 9), (5, 4),
                (6, 1), (6, 5), (6, 10),
                (7, 1), (7, 4), (7, 10),
                (8, 1), (8, 4), (8, 9),
                (9, 5), (9, 9), (9, 1),
                (10, 2), (10, 9), (10, 6);"""
        }
        
        self.drop_order = [
            'livro_palavrachave', 'palavra_chave', 'resenha', 'comentario',
            'reserva', 'emprestimo', 'livro_restaurado', 'restaurador',
            'funcionario', 'co_autor', 'autor', 'livro', 'editora',
            'ranking','pontuacao', 'usuario', 'categoria'
        ]