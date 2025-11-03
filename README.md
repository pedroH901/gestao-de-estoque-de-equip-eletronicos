# Sistema de Gestão de Estoque de Equipamentos Eletrônicos

Este projeto é uma aplicação web simples em Flask desenvolvida para atender aos requisitos de um simulado de Sistema de Gestão de Estoque. Ele permite o cadastro de usuários, autenticação e o gerenciamento (CRUD) de produtos, além do controle de entrada e saída de itens do estoque.

## 🚀 Tecnologias Utilizadas

* **Backend:** Python
* **Framework Web:** Flask
* **Banco de Dados:** SQLite 3
* **Frontend:** HTML (com templates Jinja2)

## 📋 Funcionalidades Principais

* **Autenticação:** Sistema de registro, login e logout de usuários usando sessões do Flask.
* **Gestão de Produtos (CRUD):** Funcionalidade completa para Criar, Ler (com busca), Atualizar e Deletar produtos.
* **Gestão de Estoque:** Registro de movimentações de entrada e saída, com atualização automática da quantidade de produtos.
* **Alertas:** O sistema exibe alertas (via `flash`) quando uma movimentação de saída deixa o estoque de um produto abaixo do nível mínimo configurado.
* **Histórico:** A tela de gestão de estoque exibe um histórico de todas as movimentações, mostrando o produto, data, tipo e responsável.

---

## ⚙️ Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/pedroh901/gestao-de-estoque-de-equip-eletronicos.git](https://github.com/pedroh901/gestao-de-estoque-de-equip-eletronicos.git)
    cd gestao-de-estoque-de-equip-eletronicos
    ```

2.  **Crie um ambiente virtual (Recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install Flask
    ```

4.  **Execute a aplicação:**
    ```bash
    python app.py
    ```
    O servidor estará rodando em `http://127.0.0.1:5000`.

5.  **Acesse a aplicação:**
    * Abra `http://127.0.0.1:5000/register` para criar um novo usuário.
    * Depois, acesse `http://127.0.0.1:5000/login` para entrar no sistema.

---

## 🛠️ Passo a Passo da Criação

Este projeto foi construído seguindo as entregas do simulado, evoluindo de uma aplicação simples para um sistema funcional.

### Passo 1: Configuração do Ambiente e Banco de Dados

O projeto foi iniciado com **Flask**. Para facilitar o desenvolvimento e os testes sem depender de um servidor externo, foi escolhido o **SQLite**.

Um arquivo `sql_connection.py` foi criado para centralizar a lógica de conexão. Esta função também é responsável por criar as tabelas (`Usuario`, `Produto`, `Movimento`) na primeira execução, se o arquivo `saep.db` não existir.

### Passo 2: Autenticação de Usuário (Entrega 4)

* Foram criadas as rotas `/register` e `/login` no `app.py`.
* A rota `/register` insere um novo usuário na tabela `Usuario`, validando se os campos não estão vazios e se o login já existe (para evitar duplicatas).
* A rota `/login` busca no banco por um usuário que combine `Login` e `Senha`.
* Foram criados os templates `register.html` e `login.html` para renderizar os formulários.

### Passo 3: Interface Principal e Sessão (Entrega 5)

* Uma `app.secret_key` foi adicionada para habilitar o uso de `session` no Flask.
* Ao logar com sucesso, o `ID_usuario` e o `Nome` são salvos na `session`.
* Foi criada a rota `/principal` (e `/`), que só pode ser acessada por usuários logados (verificados pela `session`).
* A rota `/logout` foi criada para limpar a `session` e redirecionar para o login.
* O template `principal.html` foi criado para ser a página inicial e conter os links para as outras funcionalidades.

### Passo 4: Cadastro de Produto (Entrega 6)

* Foram implementadas as rotas de CRUD para produtos:
    * `/cadastro_produto`: Lista todos os produtos e inclui um formulário de busca (GET).
    * `/produto/add`: (POST) Adiciona um novo produto ao banco.
    * `/produto/edit/<id>`: (GET/POST) Busca um produto pelo ID para exibir em um formulário de edição e salva as alterações.
    * `/produto/delete/<id>`: (POST) Remove um produto do banco.
* Templates `cadastro_produto.html` e `edit_produto.html` foram criados para essas funcionalidades.

### Passo 5: Gestão de Estoque (Entrega 7)

* A rota `/gestao_estoque` foi criada para listar produtos (em ordem alfabética) e o histórico de movimentações.
* A rota `/registrar_movimento` (POST) foi implementada para lidar com a lógica de negócio:
    1.  Busca o produto.
    2.  Calcula a nova quantidade com base na "Entrada" ou "Saída".
    3.  Impede que o estoque fique negativo.
    4.  Atualiza a tabela `Produto` com a nova quantidade.
    5.  Insere um registro na tabela `Movimento`, vinculando o `ID_usuario` da sessão e o `ID_produto`.
    6.  Usa `flash()` para enviar um alerta de sucesso ou um aviso de estoque mínimo.
* O template `gestao_estoque.html` foi criado para exibir os alertas, o formulário de movimentação e o histórico.

### Passo 6: Limpeza do Repositório (Boas Práticas)

* Um arquivo `.gitignore` foi adicionado ao projeto para instruir o Git a ignorar arquivos desnecessários, como o banco de dados (`*.db`) e as pastas de cache do Python (`__pycache__`).