
# 📌 CRUD de Estoque com SQLite  

## 🎯 Objetivo  
Este projeto tem como objetivo aplicar os conceitos de **SQLite** e operações **CRUD** (*Create, Read, Update, Delete*) em Python,  
desenvolvendo um sistema simples de gerenciamento de estoque **sem interface gráfica** (usando apenas terminal).

---

## 🚀 Funcionalidades  

**Criar Produto** – Adiciona um novo produto ao banco de dados.  
**Listar Produtos** – Exibe todos os produtos cadastrados.  
**Atualizar Produto** – Permite modificar a quantidade, preço e outras informações de um produto.  
**Deletar Produto** – Remove um produto do banco de dados.  
**Movimentar Estoque** – Entrada ou saída de produtos no estoque.  
**Duplicar Produto** – Clona um produto existente com um novo nome.  
**Ver Histórico** – Exibe todas as operações realizadas no estoque.  
**Relatório Rápido** – Mostra estatísticas sobre os produtos no estoque.  
**Opção de Sair** – Encerra o programa e fecha a conexão com o banco.  

---

## 🔧 Tecnologias Utilizadas  

- 🐍 **Python 3.x**  
- 🗄️ **SQLite** para armazenamento de dados  

---

## 📝 Exemplos de Uso  

### 🆕 Criando um Produto  
```md
========== MENU DE ESTOQUE ==========
1) Criar novo produto
Escolha uma opção: 1

Nome: Teclado Mecânico
Quantidade: 10
Preço (R$): 199.90
Categoria: Periféricos
Fornecedor: Logitech
Descrição: Teclado mecânico RGB switch Red

Produto 'Teclado Mecânico' adicionado ao estoque!
```

### 📋 Listando Produtos  
```md
========== MENU DE ESTOQUE ==========
2) Listar produtos
Escolha uma opção: 2

=== Lista de Produtos ===
ID: 1 | Nome: Teclado Mecânico | Qtd: 10 | Preço: R$199.90
Total de produtos: 1
```

### ✏️ Atualizando um Produto  
```md
========== MENU DE ESTOQUE ==========
3) Atualizar produto
Escolha uma opção: 3

ID do produto a atualizar: 1
Nova quantidade [Enter p/ não mudar]: 15
Novo preço (R$) [Enter p/ não mudar]: 189.90

Produto 'Teclado Mecânico' atualizado com sucesso!
```

### ❌ Deletando um Produto  
```md
========== MENU DE ESTOQUE ==========
4) Deletar produto
Escolha uma opção: 4

ID do produto a deletar: 1
Tem certeza que deseja excluir o produto ID=1? (S/N): S

Produto 'Teclado Mecânico' removido do estoque!
```

### 📊 Relatório Rápido  
```md
========== MENU DE ESTOQUE ==========
8) Relatório rápido (quantidade / valor total)
Escolha uma opção: 8

=== Relatório Rápido do Estoque ===
Total de Produtos: 5
Quantidade Total: 150
Valor Total do Estoque: R$ 7,500.00
```

---

## ⚠️ Dificuldades Encontradas e Soluções  


### 🔹 **Evitando Estoque Negativo**  
O sistema permitia a movimentação do estoque (entrada e saída de produtos), mas poderia aceitar valores negativos incorretamente.  
✅ **Solução:** Adicionada uma verificação para impedir que a quantidade de um produto fique abaixo de zero.  

### 🔹 **Tratamento de Erros no SQLite**  
Tentativas de inserir nomes duplicados causavam erros no banco de dados.  
✅ **Solução:** Adicionada captura de exceção (`try/except`) para evitar falhas e exibir mensagens amigáveis ao usuário.  

### 🔹 **Fechamento Seguro do Banco de Dados**  
O banco de dados poderia permanecer aberto caso o programa fosse fechado abruptamente.  
✅ **Solução:** O `db_manager.close()` foi chamado no final do programa para garantir o fechamento correto da conexão.  

---
