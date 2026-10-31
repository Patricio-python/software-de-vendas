import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

def create():
    try:
        # 1. Tabela Cliente
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cliente (
                idCliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                sobrenome TEXT NOT NULL,
                cpf TEXT NOT NULL DEFAULT '000.000.000-00',
                telefone TEXT NOT NULL DEFAULT '(91)9XXX-XXXX'
            );
        ''')

        # Inserir o dado padrão (Visitante)
        cursor.execute('''
            INSERT OR IGNORE INTO cliente (idCliente, nome, sobrenome, cpf, telefone) 
            VALUES (1, 'Visitante', 'Visitante', '000.000.000-00', '(91)9XXX-XXXX');
        ''')

        # 2. Tabela Endereco
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS endereco (
                idEndereco INTEGER PRIMARY KEY AUTOINCREMENT,
                endereco TEXT NOT NULL,
                numero TEXT NOT NULL,
                complemento TEXT,
                bairro TEXT NOT NULL,
                cep TEXT NOT NULL,
                idCliente INTEGER NOT NULL,
                FOREIGN KEY (idCliente) REFERENCES cliente (idCliente) ON DELETE CASCADE
            );
        ''')

        # 3. Tabela Funcionario
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS funcionario (
                idFuncionario INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                funcao TEXT NOT NULL,
                login TEXT NOT NULL,
                senha TEXT NOT NULL
            );
        ''')

        # 4. Tabela Servicos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS servicos (
                idServicos INTEGER PRIMARY KEY AUTOINCREMENT,
                Tipo TEXT NOT NULL,
                Descricao TEXT NOT NULL,
                Valor REAL NOT NULL
            );
        ''')

        # 5. Tabela Venda
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS venda (
                idVenda INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                idCliente INTEGER NOT NULL,
                idFuncionario INTEGER NOT NULL,
                FOREIGN KEY (idCliente) REFERENCES cliente (idCliente),
                FOREIGN KEY (idFuncionario) REFERENCES funcionario (idFuncionario)
            );
        ''')

        # 6. Tabela Carrinho (Tabela N:M entre Servicos e Venda)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS carrinho (
                idServicos INTEGER NOT NULL,
                idVenda INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                PRIMARY KEY (idServicos, idVenda),
                FOREIGN KEY (idServicos) REFERENCES servicos (idServicos),
                FOREIGN KEY (idVenda) REFERENCES venda (idVenda) ON DELETE CASCADE
            );
        ''')

        # Índices adicionais para otimização de buscas (conforme mapeado no dump)
        cursor.execute('CREATE INDEX IF NOT EXISTS fk_Endereco_Cliente1_idx ON endereco (idCliente);')
        cursor.execute('CREATE INDEX IF NOT EXISTS fk_Pedido_Cliente1_idx ON venda (idCliente);')
        cursor.execute('CREATE INDEX IF NOT EXISTS fk_Pedido_Funcionario1_idx ON venda (idFuncionario);')
        cursor.execute('CREATE INDEX IF NOT EXISTS fk_Servicos_has_Venda_Venda1_idx ON carrinho (idVenda);')
        cursor.execute('CREATE INDEX IF NOT EXISTS fk_Servicos_has_Venda_Servicos1_idx ON carrinho (idServicos);')

        conn.commit()
        print(f"Banco de dados físico criado com sucesso!")

    except sqlite3.Error as e:
        print(f"Erro ao criar o banco de dados: {e}")
        conn.rollback()
    finally:
        conn.close()
