import sqlite3

class Cliente:
    def __init__(self,id:int,nome:str,sobrenome:str,cpf:str,telefone:str):
        self.id=id
        self.nome=nome
        self.sobrenome=sobrenome
        self.cpf=cpf
        self.telefone=telefone

    def create(nome:str,sobrenome:str,cpf:str,telefone:str)->str:
        "Utilizado para adcionar os dados de nome, sobrenome, cpf e telefone de um cliente ao banco de dados"
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO Cliente (nome,sobrenome,cpf,telefone) VALUES (?, ?, ?, ?)", (nome,sobrenome,cpf,telefone))
            conn.commit()
            return f"Cliente Cadastrado {nome} com sucesso"
        
        except Exception as e:
            conn.rollback()
            return f"Erro ao adicionar\nErro: {e}"

        finally:
            conn.close()

    def read(id:int)->object:
        """Utilize a ID de um cliente para retornar os dados desse cliente"""

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT idCliente,nome,sobrenome,cpf,telefone FROM Cliente WHERE idCliente=?", (str(id)))
            dados=cursor.fetchone()
            dados=Cliente(dados[0],dados[1],dados[2],dados[3],dados[4])
            return dados
                
        except Exception as e:
                conn.rollback()
                return f"Erro ao selecionar no banco de dados\nErro: {e}"
        
        finally:
            conn.close()

    def update(id:int,nome:str,sobrenome:str,cpf:str,telefone:str):
        """Usado para atualizar um Cliente no banco de dados.\n
        Selecione a ID do cliente que será atualizado.\n
        Utilize "" para os campos que não serão alterados e use string para os campos a serem alterados"""

        temp=Cliente.read(id)

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        if nome!="":
            temp.nome=nome
        if sobrenome!="":
            temp.sobrenome=sobrenome
        if cpf!="":
            temp.cpf=cpf
        if telefone!="":
            temp.telefone=telefone
        
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE Cliente SET nome=?, sobrenome=?, cpf=?, telefone=? WHERE idCliente=?", (temp.nome,temp.sobrenome,temp.cpf,temp.telefone,id))
            conn.commit()
            return f"Cliente {temp.nome} Atualizado com sucesso"
                
        except Exception as e:
            conn.rollback()
            return f"Erro ao Atualizar no banco de dados\nErro: {e}"
        
        finally:
            conn.close()

    def delete(id: int) -> str:
        """Utilizado para deletar do banco de dados os dados do cliente com a ID selecionada"""

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM Cliente WHERE idCliente=?", (str(id)))
            conn.commit()
            return f"Cliente com o ID: {id} deletado com sucesso"
                
        except Exception as e:
                conn.rollback()
                return f"Erro ao Deletar\nErro: {e}"
        
        finally:
            conn.close()

class Endereco:
    pass
