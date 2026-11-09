import sqlite3
import os

db_filename = "database.db"  

def create():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()    

    try:
        # Ativa o suporte a chaves estrangeiras no SQLite
        cursor.execute("PRAGMA foreign_keys = ON;")

        # 1. Tabela Cliente
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Cliente (
                idCliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                sobrenome TEXT NOT NULL,
                cpf TEXT NOT NULL DEFAULT '000.000.000-00',
                telefone TEXT NOT NULL DEFAULT '(91)9XXX-XXXX'
            );
        ''')

        # Inserir o dado padrão (Visitante)
        cursor.execute('''
            INSERT OR IGNORE INTO Cliente (idCliente, nome, sobrenome, cpf, telefone) 
            VALUES (1, 'Visitante', 'Visitante', '000.000.000-00', '(91)9XXX-XXXX');
        ''')

        # 2. Tabela Funcionario
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Funcionario (
                idFuncionario INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                funcao TEXT NOT NULL,
                login TEXT NOT NULL,
                senha TEXT NOT NULL
            );
        ''')

        # Inserir o dado padrão (Funcionario Admin)
        cursor.execute('''
            INSERT OR IGNORE INTO Funcionario (idFuncionario, nome, funcao, login, senha) 
            VALUES (1, 'Admin', 'Administrador', 'Admin', '123456');
        ''')        

        # 3. Tabela Carrinho
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Carrinho (
                idCarrinho INTEGER PRIMARY KEY AUTOINCREMENT,
                idCliente INTEGER NOT NULL,
                total REAL NOT NULL DEFAULT 0.00,
                status INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (idCliente) REFERENCES Cliente (idCliente) ON DELETE NO ACTION ON UPDATE NO ACTION
            );
        ''')

        # 4. Tabela Venda
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Venda (
                idVenda INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                idFuncionario INTEGER NOT NULL,
                idCarrinho INTEGER NOT NULL,
                FOREIGN KEY (idFuncionario) REFERENCES Funcionario (idFuncionario) ON DELETE NO ACTION ON UPDATE NO ACTION,
                FOREIGN KEY (idCarrinho) REFERENCES Carrinho (idCarrinho) ON DELETE NO ACTION ON UPDATE NO ACTION
            );
        ''')

        # 5. Tabela Endereco
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Endereco (
                idEndereco INTEGER PRIMARY KEY AUTOINCREMENT,
                endereco TEXT NOT NULL,
                numero TEXT NOT NULL,
                complemento TEXT,
                bairro TEXT NOT NULL,
                cep TEXT NOT NULL,
                idCliente INTEGER NOT NULL,
                FOREIGN KEY (idCliente) REFERENCES Cliente (idCliente) ON DELETE NO ACTION ON UPDATE NO ACTION
            );
        ''')

        # 6. Tabela Servicos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Servicos (
                idServicos INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL
            );
        ''')

        # 7. Tabela Servico_Carrinho (Relacionamento N:M)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Servico_Carrinho (
                idCarrinho INTEGER NOT NULL,
                idServicos INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                PRIMARY KEY (idCarrinho, idServicos),
                FOREIGN KEY (idCarrinho) REFERENCES Carrinho (idCarrinho) ON DELETE NO ACTION ON UPDATE NO ACTION,
                FOREIGN KEY (idServicos) REFERENCES Servicos (idServicos) ON DELETE NO ACTION ON UPDATE NO ACTION
            );
        ''')

        # 8. Tabela Produto
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Produto (
                idProduto INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL
            );
        ''')

        # 9. Tabela Produto_Carrinho (Relacionamento N:M)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Produto_Carrinho (
                idCarrinho INTEGER NOT NULL,
                idProduto INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                PRIMARY KEY (idCarrinho, idProduto),
                FOREIGN KEY (idCarrinho) REFERENCES Carrinho (idCarrinho) ON DELETE NO ACTION ON UPDATE NO ACTION,
                FOREIGN KEY (idProduto) REFERENCES Produto (idProduto) ON DELETE NO ACTION ON UPDATE NO ACTION
            );
        ''')

        # 10. Índices para otimização de buscas (conforme mapeado no dump do MySQL)
        cursor.execute('CREATE INDEX IF NOT EXISTS fk_Carrinho_Cliente1_idx ON Carrinho (idCliente);')
        cursor.execute('CREATE INDEX IF NOT EXISTS fk_Pedido_Funcionario1_idx ON Venda (idFuncionario);')
        cursor.execute('CREATE INDEX IF NOT EXISTS fk_Venda_Carrinho1_idx ON Venda (idCarrinho);')
        cursor.execute('CREATE INDEX IF NOT EXISTS fk_Endereco_Cliente1_idx ON Endereco (idCliente);')
        cursor.execute('CREATE INDEX IF NOT EXISTS fk_Carrinho_has_Servicos_Servicos1_idx ON Servico_Carrinho (idServicos);')
        cursor.execute('CREATE INDEX IF NOT EXISTS fk_Carrinho_has_Servicos_Carrinho1_idx ON Servico_Carrinho (idCarrinho);')
        cursor.execute('CREATE INDEX IF NOT EXISTS fk_Carrinho_has_Produto_Produto1_idx ON Produto_Carrinho (idProduto);')
        cursor.execute('CREATE INDEX IF NOT EXISTS fk_Carrinho_has_Produto_Carrinho1_idx ON Produto_Carrinho (idCarrinho);')

        # 11. Triggers para automação do campo 'total' (Produto + Serviços)
        cursor.executescript('''
            -- ==========================================
            -- TRIGGERS PARA PRODUTO_CARRINHO
            -- ==========================================
            CREATE TRIGGER IF NOT EXISTS trg_produto_total_insert
            AFTER INSERT ON Produto_Carrinho
            BEGIN
                UPDATE Carrinho
                SET total = COALESCE((
                    SELECT SUM(pc.quantidade * p.valor)
                    FROM Produto_Carrinho pc
                    JOIN Produto p ON pc.idProduto = p.idProduto
                    WHERE pc.idCarrinho = NEW.idCarrinho
                ), 0.00) + COALESCE((
                    SELECT SUM(sc.quantidade * s.valor)
                    FROM Servico_Carrinho sc
                    JOIN Servicos s ON sc.idServicos = s.idServicos
                    WHERE sc.idCarrinho = NEW.idCarrinho
                ), 0.00)
                WHERE idCarrinho = NEW.idCarrinho;
            END;

            CREATE TRIGGER IF NOT EXISTS trg_produto_total_update
            AFTER UPDATE OF quantidade, idProduto ON Produto_Carrinho
            BEGIN
                UPDATE Carrinho
                SET total = COALESCE((
                    SELECT SUM(pc.quantidade * p.valor)
                    FROM Produto_Carrinho pc
                    JOIN Produto p ON pc.idProduto = p.idProduto
                    WHERE pc.idCarrinho = NEW.idCarrinho
                ), 0.00) + COALESCE((
                    SELECT SUM(sc.quantidade * s.valor)
                    FROM Servico_Carrinho sc
                    JOIN Servicos s ON sc.idServicos = s.idServicos
                    WHERE sc.idCarrinho = NEW.idCarrinho
                ), 0.00)
                WHERE idCarrinho = NEW.idCarrinho;
            END;

            CREATE TRIGGER IF NOT EXISTS trg_produto_total_delete
            AFTER DELETE ON Produto_Carrinho
            BEGIN
                UPDATE Carrinho
                SET total = COALESCE((
                    SELECT SUM(pc.quantidade * p.valor)
                    FROM Produto_Carrinho pc
                    JOIN Produto p ON pc.idProduto = p.idProduto
                    WHERE pc.idCarrinho = OLD.idCarrinho
                ), 0.00) + COALESCE((
                    SELECT SUM(sc.quantidade * s.valor)
                    FROM Servico_Carrinho sc
                    JOIN Servicos s ON sc.idServicos = s.idServicos
                    WHERE sc.idCarrinho = OLD.idCarrinho
                ), 0.00)
                WHERE idCarrinho = OLD.idCarrinho;
            END;

            -- ==========================================
            -- TRIGGERS PARA SERVICO_CARRINHO
            -- ==========================================
            CREATE TRIGGER IF NOT EXISTS trg_servico_total_insert
            AFTER INSERT ON Servico_Carrinho
            BEGIN
                UPDATE Carrinho
                SET total = COALESCE((
                    SELECT SUM(pc.quantidade * p.valor)
                    FROM Produto_Carrinho pc
                    JOIN Produto p ON pc.idProduto = p.idProduto
                    WHERE pc.idCarrinho = NEW.idCarrinho
                ), 0.00) + COALESCE((
                    SELECT SUM(sc.quantidade * s.valor)
                    FROM Servico_Carrinho sc
                    JOIN Servicos s ON sc.idServicos = s.idServicos
                    WHERE sc.idCarrinho = NEW.idCarrinho
                ), 0.00)
                WHERE idCarrinho = NEW.idCarrinho;
            END;

            CREATE TRIGGER IF NOT EXISTS trg_servico_total_update
            AFTER UPDATE OF quantidade, idServicos ON Servico_Carrinho
            BEGIN
                UPDATE Carrinho
                SET total = COALESCE((
                    SELECT SUM(pc.quantidade * p.valor)
                    FROM Produto_Carrinho pc
                    JOIN Produto p ON pc.idProduto = p.idProduto
                    WHERE pc.idCarrinho = NEW.idCarrinho
                ), 0.00) + COALESCE((
                    SELECT SUM(sc.quantidade * s.valor)
                    FROM Servico_Carrinho sc
                    JOIN Servicos s ON sc.idServicos = s.idServicos
                    WHERE sc.idCarrinho = NEW.idCarrinho
                ), 0.00)
                WHERE idCarrinho = NEW.idCarrinho;
            END;

            CREATE TRIGGER IF NOT EXISTS trg_servico_total_delete
            AFTER DELETE ON Servico_Carrinho
            BEGIN
                UPDATE Carrinho
                SET total = COALESCE((
                    SELECT SUM(pc.quantidade * p.valor)
                    FROM Produto_Carrinho pc
                    JOIN Produto p ON pc.idProduto = p.idProduto
                    WHERE pc.idCarrinho = OLD.idCarrinho
                ), 0.00) + COALESCE((
                    SELECT SUM(sc.quantidade * s.valor)
                    FROM Servico_Carrinho sc
                    JOIN Servicos s ON sc.idServicos = s.idServicos
                    WHERE sc.idCarrinho = OLD.idCarrinho
                ), 0.00)
                WHERE idCarrinho = OLD.idCarrinho;
            END;
        ''')

        conn.commit()
        print("Banco de dados físico 'database.db' criado com sucesso no SQLite!")

    except sqlite3.Error as e:
        print(f"Erro ao criar o banco de dados: {e}")
        conn.rollback()
    finally:
        conn.close()
