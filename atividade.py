import sqlite3
import re
from datetime import datetime



class DatabaseManager:
    def __init__(self, db_name="estoque.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()  

    def connect(self):
        try:
            if not self.conn:
                self.conn = sqlite3.connect(self.db_name)
                self.cursor = self.conn.cursor()
                self.create_tables()
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao conectar ao banco de dados: {e}")

    def create_tables(self):
        try:
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT UNIQUE NOT NULL,
                    quantidade INTEGER NOT NULL CHECK (quantidade >= 0),
                    preco REAL NOT NULL CHECK (preco >= 0),
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    categoria TEXT DEFAULT 'Sem categoria',
                    descricao TEXT,
                    fornecedor TEXT DEFAULT 'Desconhecido'
                )
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS historico (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    acao TEXT NOT NULL,
                    produto_id INTEGER,
                    detalhes TEXT,
                    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao criar tabelas: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

#                         Funções de validação

def validar_nome(nome):
    if not nome or not isinstance(nome, str) or len(nome.strip()) < 2:
        raise ValueError("O nome deve ter pelo menos 2 caracteres.")
    if not re.match(r'^[a-zA-Z0-9\s\-\_]+$', nome):
        raise ValueError("O nome deve conter apenas letras, números, espaços, hífens ou sublinhados.")
    if len(nome.strip()) > 50:
        raise ValueError("O nome não pode exceder 50 caracteres.")
    return nome.strip()

def validar_quantidade(quantidade):
    try:
        qtd = int(quantidade)
        if qtd < 0 or qtd > 99999:
            raise ValueError("A quantidade deve estar entre 0 e 99999.")
        return qtd
    except ValueError:
        raise ValueError("A quantidade deve ser um número inteiro válido.")

def validar_preco(preco):
    try:
        valor = float(preco)
        if valor < 0 or valor > 999999.99:
            raise ValueError("O preço deve estar entre 0 e 999999.99.")
        return round(valor, 2)
    except ValueError:
        raise ValueError("O preço deve ser um número real válido.")

def validar_categoria(categoria):
    if not categoria or len(categoria.strip()) < 1:
        return "Sem categoria"
    if len(categoria.strip()) > 30:
        raise ValueError("A categoria não pode exceder 30 caracteres.")
    return categoria.strip()

def validar_descricao(descricao):
    if not descricao:
        return ""
    if len(descricao) > 200:
        raise ValueError("A descrição não pode exceder 200 caracteres.")
    return descricao.strip()

def validar_fornecedor(fornecedor):
    if not fornecedor:
        return "Desconhecido"
    if len(fornecedor.strip()) > 50:
        raise ValueError("O nome do fornecedor não pode exceder 50 caracteres.")
    return fornecedor.strip()


#                     Classe EstoqueManager (CRUD)

class EstoqueManager:
    def __init__(self, db_manager):
        self.db = db_manager

    def criar_produto(self, nome, quantidade, preco, categoria="Sem categoria",
                      descricao="", fornecedor="Desconhecido"):
        try:
            nome = validar_nome(nome)
            quantidade = validar_quantidade(quantidade)
            preco = validar_preco(preco)
            categoria = validar_categoria(categoria)
            descricao = validar_descricao(descricao)
            fornecedor = validar_fornecedor(fornecedor)

            self.db.cursor.execute("""
                INSERT INTO produtos (nome, quantidade, preco, categoria, descricao, fornecedor)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nome, quantidade, preco, categoria, descricao, fornecedor))
            self.db.conn.commit()
            produto_id = self.db.cursor.lastrowid

           
            self.db.cursor.execute("""
                INSERT INTO historico (acao, produto_id, detalhes)
                VALUES (?, ?, ?)
            """, ("Criação", produto_id, f"Produto '{nome}' criado (Qtd: {quantidade}, Preço: {preco})"))
            self.db.conn.commit()

            return True, f"Produto '{nome}' adicionado ao estoque!"
        except sqlite3.IntegrityError:
            return False, f"Erro: O produto '{nome}' já existe no estoque."
        except ValueError as e:
            return False, f"Erro de validação: {e}"
        except sqlite3.Error as e:
            return False, f"Erro ao adicionar o produto: {e}"

    def listar_produtos(self):
        try:
            self.db.cursor.execute("""
                SELECT id, nome, quantidade, preco, data_criacao, ultima_atualizacao,
                       categoria, descricao, fornecedor
                FROM produtos
                ORDER BY id
            """)
            produtos = self.db.cursor.fetchall()
            return produtos
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao listar produtos: {e}")
            return []

    def atualizar_produto(self, id_produto, quantidade=None, preco=None,
                          categoria=None, descricao=None, fornecedor=None):
        try:
            
            self.db.cursor.execute("SELECT nome FROM produtos WHERE id = ?", (id_produto,))
            resultado = self.db.cursor.fetchone()
            if not resultado:
                return False, f"Produto com ID {id_produto} não encontrado."

            nome_produto = resultado[0]
            updates = ["ultima_atualizacao = CURRENT_TIMESTAMP"]
            params = []
            detalhes = []

            if quantidade is not None:
                qtd = validar_quantidade(quantidade)
                updates.append("quantidade = ?")
                params.append(qtd)
                detalhes.append(f"Qtd={qtd}")
            if preco is not None:
                valor = validar_preco(preco)
                updates.append("preco = ?")
                params.append(valor)
                detalhes.append(f"Preço={valor}")
            if categoria is not None:
                cat = validar_categoria(categoria)
                updates.append("categoria = ?")
                params.append(cat)
                detalhes.append(f"Categoria='{cat}'")
            if descricao is not None:
                desc = validar_descricao(descricao)
                updates.append("descricao = ?")
                params.append(desc)
                detalhes.append(f"Desc='{desc}'")
            if fornecedor is not None:
                forn = validar_fornecedor(fornecedor)
                updates.append("fornecedor = ?")
                params.append(forn)
                detalhes.append(f"Forn='{forn}'")

            if len(updates) == 1:
                return False, "Nenhum campo para atualizar."

            params.append(id_produto)
            query = f"UPDATE produtos SET {', '.join(updates)} WHERE id = ?"
            self.db.cursor.execute(query, params)

            
            self.db.cursor.execute("""
                INSERT INTO historico (acao, produto_id, detalhes)
                VALUES (?, ?, ?)
            """, ("Atualização", id_produto, "; ".join(detalhes)))
            self.db.conn.commit()

            return True, f"Produto '{nome_produto}' atualizado com sucesso!"
        except ValueError as e:
            return False, f"Erro de validação: {e}"
        except sqlite3.Error as e:
            return False, f"Erro ao atualizar o produto: {e}"

    def deletar_produto(self, id_produto):
        try:
            
            self.db.cursor.execute("SELECT nome FROM produtos WHERE id = ?", (id_produto,))
            resultado = self.db.cursor.fetchone()
            if not resultado:
                return False, f"Produto com ID {id_produto} não encontrado."

            nome_produto = resultado[0]

            self.db.cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
            
            self.db.cursor.execute("""
                INSERT INTO historico (acao, produto_id, detalhes)
                VALUES (?, ?, ?)
            """, ("Deleção", id_produto, f"Produto '{nome_produto}' removido"))
            self.db.conn.commit()

            return True, f"Produto '{nome_produto}' removido do estoque!"
        except sqlite3.Error as e:
            return False, f"Erro ao deletar o produto: {e}"

    def obter_historico(self):
        try:
            self.db.cursor.execute("""
                SELECT id, acao, produto_id, detalhes, data
                FROM historico
                ORDER BY data DESC
            """)
            return self.db.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao obter histórico: {e}")
            return []

    def movimentar_estoque(self, id_produto, quantidade_alterar):
        """
        Exemplo: se quantidade_alterar=10 => entrada de 10,
                 se quantidade_alterar=-5 => saída de 5.
        """
        try:
            self.db.cursor.execute("SELECT nome, quantidade FROM produtos WHERE id = ?", (id_produto,))
            resultado = self.db.cursor.fetchone()
            if not resultado:
                return False, f"Produto com ID {id_produto} não encontrado."

            nome_produto, qtd_atual = resultado
            qtd_atualizada = qtd_atual + quantidade_alterar

            if qtd_atualizada < 0:
                return False, "Não é possível ficar com estoque negativo."

            
            self.db.cursor.execute("""
                UPDATE produtos
                SET quantidade = ?, ultima_atualizacao = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (qtd_atualizada, id_produto))

            acao_desc = "Entrada" if quantidade_alterar >= 0 else "Saída"
            detalhes = f"{acao_desc} de {abs(quantidade_alterar)} unidades. Estoque final: {qtd_atualizada}"

           
            self.db.cursor.execute("""
                INSERT INTO historico (acao, produto_id, detalhes)
                VALUES (?, ?, ?)
            """, ("Movimentação", id_produto, detalhes))
            self.db.conn.commit()

            return True, f"{acao_desc} realizada com sucesso no produto '{nome_produto}'."
        except sqlite3.Error as e:
            return False, f"Erro na movimentação de estoque: {e}"

    def duplicar_produto(self, id_produto, novo_nome):
        try:
            self.db.cursor.execute("""
                SELECT nome, quantidade, preco, categoria, descricao, fornecedor
                FROM produtos
                WHERE id = ?
            """, (id_produto,))
            resultado = self.db.cursor.fetchone()
            if not resultado:
                return False, f"Produto com ID {id_produto} não encontrado."

            nome_orig, qtd_orig, preco_orig, cat_orig, desc_orig, forn_orig = resultado
            nome_valido = validar_nome(novo_nome)

            self.db.cursor.execute("""
                INSERT INTO produtos (nome, quantidade, preco, categoria, descricao, fornecedor)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nome_valido, qtd_orig, preco_orig, cat_orig, desc_orig, forn_orig))
            self.db.conn.commit()
            new_id = self.db.cursor.lastrowid

            # Registrar no histórico
            self.db.cursor.execute("""
                INSERT INTO historico (acao, produto_id, detalhes)
                VALUES (?, ?, ?)
            """, ("Duplicação", new_id,
                  f"Cópia de '{nome_orig}' para novo produto '{nome_valido}'"))
            self.db.conn.commit()

            return True, f"Produto duplicado com sucesso: '{novo_nome}'!"
        except sqlite3.IntegrityError:
            return False, f"Erro: O nome '{novo_nome}' já existe no estoque."
        except ValueError as e:
            return False, f"Erro de validação: {e}"
        except sqlite3.Error as e:
            return False, f"Erro na duplicação: {e}"


#                           Funções do Menu

def exibir_menu():
    print("\n========== MENU DE ESTOQUE ==========")
    print("1) Criar novo produto")
    print("2) Listar produtos")
    print("3) Atualizar produto")
    print("4) Deletar produto")
    print("5) Movimentar estoque (entrada/saída)")
    print("6) Duplicar produto")
    print("7) Ver histórico")
    print("8) Relatório rápido (quantidade / valor total)")
    print("9) Sair")
    print("=====================================")

def opcao_criar_produto(estoque_manager):
    print("\n=== Criar Novo Produto ===")
    nome = input("Nome: ")
    quantidade = input("Quantidade: ")
    preco = input("Preço (R$): ")
    categoria = input("[Opcional] Categoria: ")
    fornecedor = input("[Opcional] Fornecedor: ")
    descricao = input("[Opcional] Descrição: ")

    sucesso, mensagem = estoque_manager.criar_produto(
        nome, quantidade, preco,
        categoria=categoria if categoria.strip() else "Sem categoria",
        descricao=descricao,
        fornecedor=fornecedor if fornecedor.strip() else "Desconhecido"
    )
    print(mensagem)

def opcao_listar_produtos(estoque_manager):
    print("\n=== Lista de Produtos ===")
    produtos = estoque_manager.listar_produtos()
    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    for p in produtos:
        (idp, nome, qtd, preco, criado, att, cat, desc, forn) = p
        print(f"ID: {idp} | Nome: {nome} | Qtd: {qtd} | Preço: R${preco:.2f}")
    print(f"Total de produtos: {len(produtos)}")

def opcao_atualizar_produto(estoque_manager):
    print("\n=== Atualizar Produto ===")
    id_produto = input("ID do produto a atualizar: ")
    if not id_produto.isdigit():
        print("ID inválido.")
        return

    
    qtd = input("Nova quantidade [Enter p/ não mudar]: ")
    preco = input("Novo preço (R$) [Enter p/ não mudar]: ")
    cat = input("Nova categoria [Enter p/ não mudar]: ")
    forn = input("Novo fornecedor [Enter p/ não mudar]: ")
    desc = input("Nova descrição [Enter p/ não mudar]: ")

    
    qtd = qtd if qtd.strip() else None
    preco = preco if preco.strip() else None
    cat = cat if cat.strip() else None
    forn = forn if forn.strip() else None
    desc = desc if desc.strip() else None

    sucesso, msg = estoque_manager.atualizar_produto(id_produto, qtd, preco, cat, desc, forn)
    print(msg)

def opcao_deletar_produto(estoque_manager):
    print("\n=== Deletar Produto ===")
    id_produto = input("ID do produto a deletar: ")
    if not id_produto.isdigit():
        print("ID inválido.")
        return

    confirma = input(f"Tem certeza que deseja excluir o produto ID={id_produto}? (S/N): ").strip().lower()
    if confirma == 's':
        sucesso, msg = estoque_manager.deletar_produto(id_produto)
        print(msg)
    else:
        print("Exclusão cancelada.")

def opcao_movimentar_estoque(estoque_manager):
    print("\n=== Movimentar Estoque ===")
    id_produto = input("ID do produto: ")
    if not id_produto.isdigit():
        print("ID inválido.")
        return

    quantidade_str = input("Quantidade a adicionar (valor positivo) ou retirar (valor negativo): ")
    try:
        quantidade_alterar = int(quantidade_str)
    except ValueError:
        print("Valor inválido. Digite um inteiro.")
        return

    sucesso, msg = estoque_manager.movimentar_estoque(id_produto, quantidade_alterar)
    print(msg)

def opcao_duplicar_produto(estoque_manager):
    print("\n=== Duplicar Produto ===")
    id_produto = input("ID do produto a duplicar: ")
    if not id_produto.isdigit():
        print("ID inválido.")
        return

    novo_nome = input("Novo nome para o produto duplicado: ")
    sucesso, msg = estoque_manager.duplicar_produto(id_produto, novo_nome)
    print(msg)

def opcao_ver_historico(estoque_manager):
    print("\n=== Histórico de Ações ===")
    historico = estoque_manager.obter_historico()
    if not historico:
        print("Nenhum registro no histórico.")
        return
    for h in historico:
        (id_h, acao, prod_id, detalhes, data_h) = h
        print(f"ID={id_h} | Ação={acao} | ProdID={prod_id} | Detalhes={detalhes} | Data={data_h}")

def opcao_relatorio_rapido(estoque_manager):
    print("\n=== Relatório Rápido do Estoque ===")
    produtos = estoque_manager.listar_produtos()
    if not produtos:
        print("Nenhum produto encontrado.")
        return

    total_produtos = len(produtos)
    total_quantidade = sum(int(p[2]) for p in produtos)  
    total_valor = sum(float(p[3]) * int(p[2]) for p in produtos)  

    print(f"Total de Produtos: {total_produtos}")
    print(f"Quantidade Total: {total_quantidade}")
    print(f"Valor Total do Estoque: R${total_valor:.2f}")


#                      Função Principal


def main():
    db_manager = DatabaseManager()        
    estoque_manager = EstoqueManager(db_manager)

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            opcao_criar_produto(estoque_manager)
        elif opcao == "2":
            opcao_listar_produtos(estoque_manager)
        elif opcao == "3":
            opcao_atualizar_produto(estoque_manager)
        elif opcao == "4":
            opcao_deletar_produto(estoque_manager)
        elif opcao == "5":
            opcao_movimentar_estoque(estoque_manager)
        elif opcao == "6":
            opcao_duplicar_produto(estoque_manager)
        elif opcao == "7":
            opcao_ver_historico(estoque_manager)
        elif opcao == "8":
            opcao_relatorio_rapido(estoque_manager)
        elif opcao == "9":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

    db_manager.close()

if __name__ == "__main__":
    main()
