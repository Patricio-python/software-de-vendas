import sqlite3

class Cliente:
    def __init__(self,id:int,nome:str,sobrenome:str,cpf:str,telefone:str):
        self.id=id
        self.nome=nome
        self.sobrenome=sobrenome
        self.cpf=cpf
        self.telefone=telefone

    def create(nome:str,sobrenome:str,cpf:str,telefone:str)->str:
        ("Utilizado para adcionar os dados de nome, sobrenome, cpf e telefone de um cliente ao "
        "banco de dados")

        #Abre a conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta inserir os valores no banco de dados e retorna informação que cliente foi cadastrado
        try:
            cursor.execute("INSERT INTO Cliente (nome,sobrenome,cpf,telefone) VALUES (?, ?, ?, ?)", (nome,sobrenome,cpf,telefone))
            conn.commit()
            return f"Cliente {nome} foi cadastrado com sucesso"

        #Se falhar é realizado um rollback para segurança e retorna informação sobre o erro
        except Exception as e:
            conn.rollback()
            return f"Erro ao adicionar\nErro: {e}"

        #Finaliza com o fechamento da conexão com o banco de dados
        finally:
            conn.close()

    def read(id:int)->object:
        ("Usando a ID de um cliente irá retornar os dados desse cliente como Objeto 'clt_dados' ")

        #Conecta ao banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta ler os dados do cliente no banco de dados usando a ID fornecida, e retorna os dados como obejto 'clt_dados'
        try:
            cursor.execute("SELECT idCliente,nome,sobrenome,cpf,telefone FROM Cliente WHERE idCliente=?", (str(id)))
            dados=cursor.fetchone()
            clt_dados=Cliente(dados[0],dados[1],dados[2],dados[3],dados[4])
            return clt_dados

        #Em caso de erro realiza um rollback por segurança e retorna uma frase com erro
        except Exception as e:
                conn.rollback()
                return f"Erro ao selecionar no banco de dados\nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dados
        finally:
            conn.close()

    def update(id:int,nome:str,sobrenome:str,cpf:str,telefone:str):
        ("Usado para atualizar um Cliente no banco de dados.\n\n"
        "Selecione a ID do cliente que será atualizado.\n\n"
        'Utilize "" para os campos que não serão alterados e use string para os campos a serem alterados\n\n'
        'EX: Cliente.update( 4, "" , "" , 969.858.747-31 , (99)98080-6060)\n\n'
        'No exemplo apenas os campos de cpf e de telefone serão alterados no cliente com ID=4')

        #Busca as informações atuais do cliente no banco de dados e salva como objeto temp
        temp=Cliente.read(id)

        #Faz as alterações no Obejto temp se os campos não estiverem vazios na função
        #Se os campos estiverem "" não haverá mudanças e os valores permaneceram o mesmo de quando recuperados
        # pelo banco d dados
        if nome!="":
            temp.nome=nome
        if sobrenome!="":
            temp.sobrenome=sobrenome
        if cpf!="":
            temp.cpf=cpf
        if telefone!="":
            temp.telefone=telefone
        
        #Inicia conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta atualizar o banco de dados com o Objeto temp utlizando a ID fornecida na função,
        # retornando a informação de que foi bem sucedido
        try:
            cursor.execute("UPDATE Cliente SET nome=?, sobrenome=?, cpf=?, telefone=? WHERE idCliente=?", (temp.nome,temp.sobrenome,temp.cpf,temp.telefone,id))
            conn.commit()
            return f"Cliente {temp.nome} Atualizado com sucesso"
        # Se houver algum erro será realizado um rollback e informado o erro que orcorreu
        except Exception as e:
            conn.rollback()
            return f"Erro ao Atualizar no banco de dados\nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dados
        finally:
            conn.close()

    def delete(id: int) -> str:
        """Utilizado para deletar do banco de dados os dados do cliente com a ID selecionada"""

        #Inicia conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta deletar as informação do cliente com a ID fornecida e retornando str de sucesso
        try:
            cursor.execute("DELETE FROM Cliente WHERE idCliente=?", (str(id)))
            conn.commit()
            return f"Cliente com o ID: {id} deletado com sucesso"

        #Em caso de falha um rollback será realizado e uma str informa que ocorreu um erro e qual o erro                
        except Exception as e:
                conn.rollback()
                return f"Erro ao Deletar\nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dadosa
        finally:
            conn.close()

class Endereco:
    def __init__(self,id:int,endereco:str,numero:str,complemento:str,bairro:str,cep:str,idCliente:int):
        self.id=id
        self.endereco=endereco
        self.numero=numero
        self.complemento=complemento
        self.bairro=bairro
        self.cep=cep
        self.idCliente=idCliente

    def create(endereco:str,numero:str,complemento:str,bairro:str,cep:str,idCliente:int)->str:
        ("Utilizado para adcionar os dados do endereço e vincular a um cliente pela ID do cliente")

        #Abre a conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta inserir os valores no banco de dados e retorna informação que o Endereco foi cadastrado
        try:
            cursor.execute("INSERT INTO Endereco (endereco,numero,complemento,bairro,cep,idCliente) VALUES (?, ?, ?, ?, ?, ?)", (endereco,numero,complemento,bairro,cep,idCliente))
            conn.commit()
            return f"Endereco foi cadastrado com sucesso"

        #Se falhar é realizado um rollback para segurança e retorna informação sobre o erro
        except Exception as e:
            conn.rollback()
            return f"Erro ao adicionar Endereco \nErro: {e}"

        #Finaliza com o fechamento da conexão com o banco de dados
        finally:
            conn.close()

    def read(id:str)->object:
        ("Usando a ID de um cliente irá retornar os dados de endereco do cliente como Objeto 'endreco_dados' ")

        #Conecta ao banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta ler os dados do Endereco no banco de dados usando a ID fornecida, e retorna os dados como obejto 'endereco_dados'
        try:
            cursor.execute("SELECT idEndereco,endereco,numero,complemento,bairro,cep FROM endereco WHERE idCliente=?", (str(id)))
            dados=cursor.fetchone()
            endereco_dados=Endereco(dados[0],dados[1],dados[2],dados[3],dados[4],dados[5],id)
            return endereco_dados

        #Em caso de erro realiza um rollback por segurança e retorna uma frase com erro
        except Exception as e:
                conn.rollback()
                return f"Erro ao selecionar no banco de dados\nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dados
        finally:
            conn.close()

    def update(endereco:str,numero:str,complemento:str,bairro:str,cep:str,idCliente:int):
        ("Usado para atualizar um Endereco no banco de dados.\n\n"
        "Selecione a ID do cliente que será atualizado.\n\n"
        'Utilize "" para os campos que não serão alterados e use string para os campos a serem alterados\n\n'
        'EX: Cliente.update( "", "" , "" , "Municipal" , "66.000-000", 4)\n\n'
        'No exemplo apenas os campos de Bairro e de cep serão alterados no endereço do cliente com ID=4')

        #Busca as informações atuais do Endereco no banco de dados e salva como objeto temp
        temp=Endereco.read(idCliente)

        #Faz as alterações no Obejto temp se os campos não estiverem vazios na função
        #Se os campos estiverem "" não haverá mudanças e os valores permaneceram o mesmo de quando recuperados
        # pelo banco d dados
        if endereco!="":
            temp.endereco=endereco
        if numero!="":
            temp.numero=numero
        if complemento!="":
            temp.complemento=complemento
        if bairro!="":
            temp.bairro=bairro
        if cep!="":
            temp.cep=cep

        #Inicia conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta atualizar o banco de dados com o Objeto temp utlizando a ID fornecida na função,
        # retornando a informação se foi bem sucedido
        try:
            cursor.execute("UPDATE Endereco SET endereco=?, numero=?, complemento=?, bairro=?, cep=? WHERE idCliente=?", (temp.endereco,temp.numero,temp.complemento,temp.bairro,temp.cep,idCliente))
            conn.commit()
            return f"Endereco Atualizado com sucesso"
        
        # Se houver algum erro será realizado um rollback e informado o erro que orcorreu
        except Exception as e:
            conn.rollback()
            return f"Erro ao atualizar Endereco no banco de dados\nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dados
        finally:
            conn.close()

    def delete(id: int) -> str:
        """Utilizado para deletar do banco de dados os dados do Endereco usado ID do cliente selecionado"""

        #Inicia conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta deletar as informação do endereco do cliente com a ID fornecida e retornando str de sucesso
        try:
            cursor.execute("DELETE FROM Endereco WHERE idCliente=?", (str(id)))
            conn.commit()
            return f"Endereço do cliente: {id} foi deletado com sucesso"

        #Em caso de falha um rollback será realizado e uma str informa que ocorreu um erro e qual o erro                
        except Exception as e:
                conn.rollback()
                return f"Erro ao Deletar\nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dadosa
        finally:
            conn.close()

class Funcionario:
    def __init__(self,id:int,nome:str,funcao:str,login:str,senha:str):
        self.id=id
        self.nome=nome
        self.funcao=funcao
        self.login=login
        self.senha=senha

    def create(nome:str,funcao:str,login:str,senha:str)->str:
        ("Utilizado para adcionar os dados do Funcionario")

        #Abre a conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta inserir os valores no banco de dados e retorna informação que o Funcionario foi cadastrado
        try:
            cursor.execute("INSERT INTO Funcionario (nome,funcao,login,senha) VALUES (?, ?, ?, ?)", (nome,funcao,login,senha))
            conn.commit()
            return f"Funcionario {nome} foi cadastrado com sucesso"

        #Se falhar é realizado um rollback para segurança e retorna informação sobre o erro
        except Exception as e:
            conn.rollback()
            return f"Erro ao adicionar Funcionario \nErro: {e}"

        #Finaliza com o fechamento da conexão com o banco de dados
        finally:
            conn.close()

    def read(id:str)->object:
        ("Usando a ID de um Funcionario irá retornar os dados do Funcionario")

        #Conecta ao banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta ler os dados do Funcionario no banco de dados usando a ID fornecida, e retorna os dados como obejto 'Funcionario_dados'
        try:
            cursor.execute("SELECT nome,funcao,login,senha FROM Funcionario WHERE idFuncionario=?", (str(id)))
            dados=cursor.fetchone()
            Funcionario_dados=Funcionario(int(id),dados[0],dados[1],dados[2],dados[3])
            return Funcionario_dados

        #Em caso de erro realiza um rollback por segurança e retorna uma frase com erro
        except Exception as e:
                conn.rollback()
                return f"Erro ao selecionar Funcionario no banco de dados\nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dados
        finally:
            conn.close()

    def update(id:int,nome:str,funcao:str,login:str,senha:str):
        ("Usado para atualizar um Funcionario no banco de dados.\n\n"
        "Selecione a ID do Funcionario que será atualizado.\n\n"
        'Utilize "" para os campos que não serão alterados e use string para os campos a serem alterados\n\n'
        'EX: Funcionario.update(4,"","Vendedor","","Senha.123")\n\n'
        'No exemplo apenas os campos de Funcao e Senha serão alterados no funcionario com ID=4')

        #Busca as informações atuais do Funcionario no banco de dados e salva como objeto temp
        temp=Funcionario.read(id)

        #Faz as alterações no Obejto temp se os campos não estiverem vazios na função
        #Se os campos estiverem "" não haverá mudanças e os valores permaneceram o mesmo de quando recuperados
        # pelo banco d dados
        
        if nome!="":
            temp.nome=nome
        if funcao!="":
            temp.funcao=funcao
        if login!="":
            temp.login=login
        if senha!="":
            temp.senha=senha

        #Inicia conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta atualizar o banco de dados com o Objeto temp utlizando a ID fornecida na função,
        # retornando a informação se foi bem sucedido
        try:
            cursor.execute("UPDATE Funcionario SET nome=?, funcao=?, login=?, senha=? WHERE idFuncionario=?", (temp.nome,temp.funcao,temp.login,temp.senha,id))
            conn.commit()
            return f"Funcionario Atualizado com sucesso"
        
        # Se houver algum erro será realizado um rollback e informado o erro que orcorreu
        except Exception as e:
            conn.rollback()
            return f"Erro ao atualizar Funcionario no banco de dados\nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dados
        finally:
            conn.close()

    def delete(id: int) -> str:
        """Utilizado para deletar do banco de dados os dados do Funcionario usado ID selecionada"""

        #Inicia conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta deletar as informação do Funcionario com a ID fornecida e retornando str de sucesso
        try:
            cursor.execute("DELETE FROM Funcionario WHERE idFuncionario=?", (str(id)))
            conn.commit()
            return f"O Funcionario foi deletado com sucesso"

        #Em caso de falha um rollback será realizado e uma str informa que ocorreu um erro e qual o erro                
        except Exception as e:
                conn.rollback()
                return f"Erro ao Deletar\nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dadosa
        finally:
            conn.close()

class Servicos:
    def __init__(self,id:int,nome:str,descricao:str,valor:float):
        self.id=id
        self.nome=nome
        self.descricao=descricao
        self.valor=valor

    def create(nome:str,descricao:str,valor:float)->str:
        ("Utilizado para adcionar os dados dos Servicos ao banco de dados")

        #Abre a conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta inserir os valores no banco de dados e retorna informação que o Servico foi cadastrado
        try:
            cursor.execute("INSERT INTO Servicos (nome,descricao,valor) VALUES (?, ?, ?)", (nome,descricao,valor))
            conn.commit()
            return f"Servico {nome} foi cadastrado com sucesso"

        #Se falhar é realizado um rollback para segurança e retorna informação sobre o erro
        except Exception as e:
            conn.rollback()
            return f"Erro ao adicionar Servico \nErro: {e}"

        #Finaliza com o fechamento da conexão com o banco de dados
        finally:
            conn.close()

    def read(id:str)->object:
        ("Usando a ID de um Servico irá retornar os dados do servico como Objeto ")

        #Conecta ao banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta ler os dados do Servico no banco de dados usando a ID fornecida, e retorna os dados como obejto
        try:
            cursor.execute("SELECT nome,descricao,valor FROM Servicos WHERE idServicos=?", (str(id)))
            dados=cursor.fetchone()
            servico_dados=Servicos(id,dados[0],dados[1],dados[2])
            return servico_dados

        #Em caso de erro realiza um rollback por segurança e retorna uma frase com erro
        except Exception as e:
                conn.rollback()
                return f"Erro ao selecionar no banco de dados\nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dados
        finally:
            conn.close()

    def update(id:int,nome:str,descricao:str,valor:str):
        ("Usado para atualizar um Servico no banco de dados.\n\n"
        "Selecione a ID do servico que será atualizado.\n\n"
        'Utilize "" para os campos que não serão alterados e use string para os campos a serem alterados\n\n'
        'EX: Servicos.update( "Reparo", "" , "45.21" , 5)\n\n'
        'No exemplo apenas os campos de Tipo e Valor serão alterados no Servico de ID 5 ')

        #Busca as informações atuais do Servico no banco de dados e salva como objeto temp
        temp=Servicos.read(id)

        #Faz as alterações no Obejto temp se os campos não estiverem vazios na função
        #Se os campos estiverem "" não haverá mudanças e os valores permaneceram o mesmo de quando recuperados
        # pelo banco d dados
        if nome!="":
            temp.nome=nome
        if descricao!="":
            temp.descricao=descricao
        if valor!="":
            temp.valor=valor
        

        #Inicia conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta atualizar o banco de dados com o Objeto temp utlizando a ID fornecida na função,
        # retornando a informação se foi bem sucedido
        try:
            cursor.execute("UPDATE Servicos SET nome=?, descricao=?, valor=? WHERE idServicos=?", (temp.nome,temp.descricao,temp.valor,id))
            conn.commit()
            return f"Servico Atualizado com sucesso"
        
        # Se houver algum erro será realizado um rollback e informado o erro que orcorreu
        except Exception as e:
            conn.rollback()
            return f"Erro ao atualizar Servico no banco de dados\nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dados
        finally:
            conn.close()

    def delete(id: int) -> str:
        """Utilizado para deletar do banco de dados os dados do Servico usando a ID selecionada"""

        #Inicia conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta deletar as informação do Servico com a ID fornecida e retornando str de sucesso
        try:
            cursor.execute("DELETE FROM Servicos WHERE idServicos=?", (str(id)))
            conn.commit()
            return f"Servico {id}: foi deletado com sucesso"

        #Em caso de falha um rollback será realizado e uma str informa que ocorreu um erro e qual o erro                
        except Exception as e:
                conn.rollback()
                return f"Erro ao Deletar\nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dadosa
        finally:
            conn.close()

class Produto:
    def __init__(self,id:int,nome:str,descricao:str,valor:float):
        self.id=id
        self.nome=nome
        self.descricao=descricao
        self.valor=valor

    def create(nome:str,descricao:str,valor:float):
        ("Utilizado para adcionar os dados dos Produto ao banco de dados")

        #Abre a conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta inserir os valores no banco de dados e retorna informação que o Produto foi cadastrado
        try:
            cursor.execute("INSERT INTO Produto (nome,descricao,valor) VALUES (?, ?, ?)", (nome,descricao,valor))
            conn.commit()
            return f"Produto {nome} foi cadastrado com sucesso"

        #Se falhar é realizado um rollback para segurança e retorna informação sobre o erro
        except Exception as e:
            conn.rollback()
            return f"Erro ao adicionar Produto \nErro: {e}"

        #Finaliza com o fechamento da conexão com o banco de dados
        finally:
            conn.close()

    def read(id:str)->object:
        ("Usando a ID de um Produto irá retornar os dados do Produto como Objeto ")

        #Conecta ao banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta ler os dados do Produto no banco de dados usando a ID fornecida, e retorna os dados como obejto
        try:
            cursor.execute("SELECT nome,descricao,valor FROM Produto WHERE idProduto=?", (str(id)))
            dados=cursor.fetchone()
            produto_dados=Produto(id,dados[0],dados[1],dados[2])
            return produto_dados

        #Em caso de erro realiza um rollback por segurança e retorna uma frase com erro
        except Exception as e:
                conn.rollback()
                return f"Erro ao selecionar Produto no banco de dados\nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dados
        finally:
            conn.close()

    def update(id:int,nome:str,descricao:str,valor:str):
        ("Usado para atualizar um Produto no banco de dados.\n\n"
        "Selecione a ID do Produto que será atualizado.\n\n"
        'Utilize "" para os campos que não serão alterados e use string para os campos a serem alterados\n\n'
        'EX: Produto.update( "Cadeira", "" , "15.00" , 3)\n\n'
        'No exemplo apenas os campos de Nome e Valor serão alterados no Produto de ID 3 ')

        #Busca as informações atuais do Servico no banco de dados e salva como objeto temp
        temp=Produto.read(id)

        #Faz as alterações no Obejto temp se os campos não estiverem vazios na função
        #Se os campos estiverem "" não haverá mudanças e os valores permaneceram o mesmo de quando recuperados
        # pelo banco d dados
        if nome!="":
            temp.nome=nome
        if descricao!="":
            temp.descricao=descricao
        if valor!="":
            temp.valor=valor
        

        #Inicia conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta atualizar o banco de dados com o Objeto temp utlizando a ID fornecida na função,
        # retornando a informação se foi bem sucedido
        try:
            cursor.execute("UPDATE Produto SET nome=?, descricao=?, valor=? WHERE idProduto=?", (temp.nome,temp.descricao,temp.valor,id))
            conn.commit()
            return f"Produto Atualizado com sucesso"
        
        # Se houver algum erro será realizado um rollback e informado o erro que orcorreu
        except Exception as e:
            conn.rollback()
            return f"Erro ao atualizar Produto no banco de dados\nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dados
        finally:
            conn.close()

    def delete(id: int) -> str:
        """Utilizado para deletar do banco de dados os dados do Produto usando ID selecionada"""

        #Inicia conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta deletar as informação do Produto com a ID fornecida e retornando str de sucesso
        try:
            cursor.execute("DELETE FROM Produto WHERE idProduto=?", (str(id)))
            conn.commit()
            return f"Produto {id}: foi deletado com sucesso"

        #Em caso de falha um rollback será realizado e uma str informa que ocorreu um erro e qual o erro                
        except Exception as e:
                conn.rollback()
                return f"Erro ao Deletar Produto \nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dadosa
        finally:
            conn.close()
        
class Carrinho:
    def __init__(self,id:int,idCliente:int,total:float,status:bool):
        self.id=id
        self.idCliente=idCliente
        self.total=total
        self.status=status

    def create(idCliente:int)->str:
        ("Utilizado para criar um carro e vincular a um cliente pela ID do cliente")

        #Abre a conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta inserir a ID no banco de dados e retorna informação que o Carrinho foi cadastrado
        try:
            cursor.execute("INSERT INTO Carrinho (idCliente) VALUES (?)", (idCliente,))
            conn.commit()
            return f"Carrinho Criado com sucesso"

        #Se falhar é realizado um rollback para segurança e retorna informação sobre o erro
        except Exception as e:
            conn.rollback()
            return f"Erro ao Criar Carrinho \nErro: {e}"

        #Finaliza com o fechamento da conexão com o banco de dados
        finally:
            conn.close()

    def read(id:str)->object:
        ("Usando a ID irá retornar os dados de Carrinho como Objeto 'carrinho_dados' ")

        #Conecta ao banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta ler os dados do Carrinho no banco de dados usando a ID fornecida, e retorna os dados como obejto
        try:
            cursor.execute("SELECT idCarrinho,idCliente,total,status FROM carrinho WHERE idCarrinho=?", (str(id)))
            dados=cursor.fetchone()
            carrinho_dados=Carrinho(dados[0],dados[1],dados[2],dados[3])
            return carrinho_dados

        #Em caso de erro realiza um rollback por segurança e retorna uma frase com erro
        except Exception as e:
                conn.rollback()
                return f"Erro ao selecionar no banco de dados\nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dados
        finally:
            conn.close()

    def update(id:int,idCliente:int,status:bool):
        ("Usado para atualizar um Carrinho no banco de dados.\n\n"
        "Selecione a ID do carrinho que será atualizado.\n\n"
        'Utilize "" para os campos que não serão alterados e use string para os campos a serem alterados\n\n'
        'EX: Carrinho.update(2, "", 1)\n\n'
        'No exemplo apenas o campo de Status será alterado para TRUE no Carrinho com ID=2'
        "Atributo 'Total' Não é modificado pq ele possui gatilhos de alteração")

        #Busca as informações atuais do Carrinho no banco de dados e salva como objeto temp
        temp=Carrinho.read(id)

        #Faz as alterações no Obejto temp se os campos não estiverem vazios na função
        #Se os campos estiverem "" não haverá mudanças e os valores permaneceram o mesmo de quando recuperados
        # pelo banco d dados
        if idCliente!="":
            temp.idCliente=idCliente
        if status!="":
            temp.status=status

        #Inicia conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta atualizar o banco de dados com o Objeto temp utlizando a ID fornecida na função,
        # retornando a informação se foi bem sucedido
        try:
            cursor.execute("UPDATE Carrinho SET idCliente=?, status=? WHERE idCarrinho=?", (temp.idCliente,temp.status,id))
            conn.commit()
            return f"Carrinho atualizado com sucesso"
        
        # Se houver algum erro será realizado um rollback e informado o erro que orcorreu
        except Exception as e:
            conn.rollback()
            return f"Erro ao atualizar o Carrinho no banco de dados\nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dados
        finally:
            conn.close()

    def delete(id: int) -> str:
        """Utilizado para deletar do banco de dados os dados do Carrinho usando ID selecionada"""

        #Inicia conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta deletar as informação do carrinho com a ID fornecida e retornando str de sucesso
        try:
            cursor.execute("DELETE FROM Carrinho WHERE idCarrinho=?", (str(id)))
            conn.commit()
            return f"Carrinho {id} : foi deletado com sucesso"

        #Em caso de falha um rollback será realizado e uma str informa que ocorreu um erro e qual o erro                
        except Exception as e:
                conn.rollback()
                return f"Erro ao Deletar Carrinho {id} \nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dadosa
        finally:
            conn.close()

class Produto_carrinho:
    def __init__(self,idCarrinho:int,idProduto:int,quantidade:int):
        self.idCarrinho=idCarrinho
        self.idProduto=idProduto
        self.quantidade=quantidade

    def create(idCarrinho:int,idProduto:int,quantidade:int)->str:
        ("Utilizado para adicionar Produtos pela sua ID e a quantidade a ser colocada em um Carrinho")

        #Abre a conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta as indformações no banco de dados e retorna informação que o Produto foi adicionado ao Carrinho
        try:
            cursor.execute("INSERT INTO Produto_Carrinho (idCarrinho,idProduto,quantidade) VALUES (?,?,?)", (idCarrinho,idProduto,quantidade))
            conn.commit()
            return f"Produto Adicionado com sucesso ao Carrinho {idCarrinho}"

        #Se falhar é realizado um rollback para segurança e retorna informação sobre o erro
        except Exception as e:
            conn.rollback()
            return f"Erro ao adicionar Produto ao carrinho\nErro: {e}"

        #Finaliza com o fechamento da conexão com o banco de dados
        finally:
            conn.close()

    def read(idCarrinho:int)->object:
        ("Usando a ID irá retornar os Produtos e quantidade do Carrinho ")

        #Conecta ao banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta ler os dados da tabela Produto_carrinho no banco de dados usando a ID fornecida, e retorna os dados
        try:
            cursor.execute("SELECT * FROM Produto_Carrinho WHERE idCarrinho=?", (str(idCarrinho)))
            dados=cursor.fetchall()
            
            return dados

        #Em caso de erro realiza um rollback por segurança e retorna uma frase com erro
        except Exception as e:
                conn.rollback()
                return f"Erro ao selecionar no banco de dados\nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dados
        finally:
            conn.close()

    def update(idCarrinho:int,idProduto:int,quantidade:int):
        ("Usado para modificar a quantidade de um produto em um carrinho")

        #Inicia conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta atualizar a quantidade de itens no banco de dados utilizando as informações fornecidas,
        # retornando a informação se foi bem sucedido
        try:
            cursor.execute("UPDATE Produto_Carrinho SET quantidade=? WHERE idCarrinho=? AND idProduto=?", (quantidade,idCarrinho,idProduto))
            conn.commit()
            return f"Carrinho atualizado com sucesso"
        
        # Se houver algum erro será realizado um rollback e informado o erro que orcorreu
        except Exception as e:
            conn.rollback()
            return f"Erro ao atualizar Quantidade de produtos no banco de dados\nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dados
        finally:
            conn.close()

    def delete(idCarrinho:int,idProduto:int) -> str:
        """Utilizado para deletar do banco de dados o Produto fornecido pela ID de um Carrinho com a ID Fornecida"""

        #Inicia conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Tenta deletar as informação do carrinho com a ID fornecida e retornando str de sucesso
        try:
            cursor.execute("DELETE FROM Produto_Carrinho WHERE idCarrinho=? AND idProduto=?", (idCarrinho,idProduto))
            conn.commit()
            return f"Produto {idProduto} foi deletado com sucesso do Carrinho {idCarrinho}"

        #Em caso de falha um rollback será realizado e uma str informa que ocorreu um erro e qual o erro                
        except Exception as e:
                conn.rollback()
                return f"Erro ao Deletar Produto {idProduto} do Carrinho {idCarrinho} \nErro: {e}"

        #Finaliza com o encerramento da conexão com o banco de dadosa
        finally:
            conn.close()

