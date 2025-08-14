# 📌 CRUD de Estoque com SQLite

> **Atenção**: Projeto desenvolvido para fins educacionais.

Este projeto implementa um sistema de gerenciamento de estoque simples, utilizando **SQLite** e operações **CRUD** (*Create, Read, Update, Delete*) em Python, sem interface gráfica (apenas terminal).

---

## 🎯 Objetivo
Aplicar os conceitos de **SQLite** e operações **CRUD** no desenvolvimento de um sistema que permita gerenciar produtos, controlar movimentações e gerar relatórios.

---

## 🚀 Funcionalidades Principais
- **Criar Produto** – Adiciona um novo produto ao banco de dados.
- **Listar Produtos** – Exibe todos os produtos cadastrados.
- **Atualizar Produto** – Modifica quantidade, preço e outras informações.
- **Deletar Produto** – Remove um produto do banco de dados.
- **Movimentar Estoque** – Entrada ou saída de produtos.
- **Duplicar Produto** – Clona um produto existente com novo nome.
- **Ver Histórico** – Mostra todas as operações realizadas.
- **Relatório Rápido** – Apresenta estatísticas do estoque.
- **Opção de Sair** – Encerra o programa e fecha a conexão.

---

## 📝 Exemplos de Uso

### 🆕 Criando um Produto
```bash
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
```bash
========== MENU DE ESTOQUE ==========
2) Listar produtos
Escolha uma opção: 2

=== Lista de Produtos ===
ID: 1 | Nome: Teclado Mecânico | Qtd: 10 | Preço: R$199.90
Total de produtos: 1
```

### ✏️ Atualizando um Produto
```bash
========== MENU DE ESTOQUE ==========
3) Atualizar produto
Escolha uma opção: 3

ID do produto a atualizar: 1
Nova quantidade [Enter p/ não mudar]: 15
Novo preço (R$) [Enter p/ não mudar]: 189.90

Produto 'Teclado Mecânico' atualizado com sucesso!
```

### ❌ Deletando um Produto
```bash
========== MENU DE ESTOQUE ==========
4) Deletar produto
Escolha uma opção: 4

ID do produto a deletar: 1
Tem certeza que deseja excluir o produto ID=1? (S/N): S

Produto 'Teclado Mecânico' removido do estoque!
```

### 📊 Relatório Rápido
```bash
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

### 🔹 Estoque Negativo
O sistema permitia movimentações que poderiam deixar o estoque negativo.  
✅ **Solução:** Implementada verificação para impedir que a quantidade seja inferior a zero.

### 🔹 Tratamento de Erros no SQLite
Inserções com nomes duplicados geravam falhas no banco de dados.  
✅ **Solução:** Adicionada captura de exceções (`try/except`) para exibir mensagens amigáveis ao usuário.

---
