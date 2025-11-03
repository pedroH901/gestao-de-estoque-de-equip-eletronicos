from flask import Flask, request, render_template, session, redirect, url_for, flash
from datetime import date
from sql_connection import get_db_connection
import sqlite3 # Importado para capturar o erro de 'IntegrityError'

app = Flask(__name__)

# Chave secreta para a 'session'
app.secret_key = '123'


# --- Função Helper de Login ---
def check_login():
    """Função helper para verificar se o usuário está logado"""
    if 'user_id' not in session:
        return False
    return True

# --- Rota de Registro (Com Validação) ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validação para campos vazios
        if not username or not password:
            return render_template('register.html', error="Usuário e Senha são obrigatórios.")
    
        connection = get_db_connection() 
        
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO Usuario (Nome, Login, Senha) VALUES (?, ?, ?)",
                    (username, username, password)
                )
                connection.commit()
                # Após registrar, redireciona para o login
                return redirect(url_for('login'))
            
            except sqlite3.IntegrityError:
                return render_template('register.html', error="Erro: Esse nome de usuário já existe.")
            except Exception as e:
                print(f"Erro ao inserir dados no SQLite: {e}")
                return f"Ocorreu um erro: {e}"
            finally:
                connection.close()
        else:
            return "Falha na conexão com o banco de dados."

    # Se for GET, apenas mostra a página de registro
    return render_template('register.html', error=None)


# --- ENTREGA 4: Rota de Login ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['username']
        senha = request.form['password']
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM Usuario WHERE Login = ? AND Senha = ?", 
                (login, senha)
            )
            usuario = cursor.fetchone() 
            connection.close()

            if usuario:
                # Se encontrou, salva na 'session'
                session['user_id'] = usuario['ID_usuario']
                session['user_name'] = usuario['Nome']
                return redirect(url_for('principal'))
            else:
                # Se não encontrou, mostra erro
                return render_template('login.html', error="Usuário ou senha inválidos.")
        
    return render_template('login.html')


# --- ENTREGA 5: Rota Principal ---
@app.route('/') 
@app.route('/principal')
def principal():
    if not check_login():
        return redirect(url_for('login'))
        
    # Se estiver logado, mostra a página principal
    nome_usuario = session['user_name']
    return render_template('principal.html', nome_usuario=nome_usuario)


# --- Rota de Logout (Corrigida) ---
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('login'))


# --- ENTREGA 6: Rotas de Cadastro de Produto (CRUD) ---

@app.route('/cadastro_produto')
def cadastro_produto():
    if not check_login():
        return redirect(url_for('login'))
    
    query_busca = request.args.get('busca', '') 
    
    conn = get_db_connection()
    if query_busca:
        produtos = conn.execute(
            "SELECT * FROM Produto WHERE Nome LIKE ?", 
            ('%' + query_busca + '%',)
        ).fetchall()
    else:
        produtos = conn.execute("SELECT * FROM Produto ORDER BY Nome ASC").fetchall()
    
    conn.close()
    
    return render_template(
        'cadastro_produto.html', 
        produtos=produtos, 
        nome_usuario=session['user_name'],
        query_busca=query_busca
    )

@app.route('/produto/add', methods=['POST'])
def add_produto():
    if not check_login():
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        quantidade = request.form['quantidade']
        estoque_minimo = request.form['estoque_minimo']

        if not nome or not quantidade or not estoque_minimo:
            return "Erro: Campos obrigatórios não preenchidos."

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO Produto (Nome, Descricao, Quantidade, Estoque_Minimo) VALUES (?, ?, ?, ?)",
            (nome, descricao, quantidade, estoque_minimo)
        )
        conn.commit()
        conn.close()
        
    return redirect(url_for('cadastro_produto'))

@app.route('/produto/edit/<int:id>', methods=['GET', 'POST'])
def edit_produto(id):
    if not check_login():
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        quantidade = request.form['quantidade']
        estoque_minimo = request.form['estoque_minimo']
        
        if not nome or not quantidade or not estoque_minimo:
            return "Erro: Campos obrigatórios não preenchidos."
            
        conn.execute(
            """UPDATE Produto 
               SET Nome = ?, Descricao = ?, Quantidade = ?, Estoque_Minimo = ?
               WHERE ID_produto = ?""",
            (nome, descricao, quantidade, estoque_minimo, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('cadastro_produto'))

    # Se for GET, mostra o formulário de edição
    produto = conn.execute(
        "SELECT * FROM Produto WHERE ID_produto = ?", (id,)
    ).fetchone()
    conn.close()
    
    if not produto:
        return "Produto não encontrado.", 404
        
    return render_template('edit_produto.html', produto=produto, nome_usuario=session['user_name'])

@app.route('/produto/delete/<int:id>', methods=['POST'])
def delete_produto(id):
    if not check_login():
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    conn.execute("DELETE FROM Produto WHERE ID_produto = ?", (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('cadastro_produto'))


# --- ENTREGA 7: GESTÃO DE ESTOQUE (Movido para o lugar certo) ---

@app.route('/gestao_estoque')
def gestao_estoque():
    if not check_login():
        return redirect(url_for('login'))

    conn = get_db_connection()
    
    produtos = conn.execute("SELECT * FROM Produto ORDER BY Nome ASC").fetchall()
    
    movimentos = conn.execute("""
        SELECT m.*, p.Nome as NomeProduto, u.Nome as NomeUsuario
        FROM Movimento m
        JOIN Produto p ON m.ID_produto = p.ID_produto
        JOIN Usuario u ON m.ID_usuario = u.ID_usuario
        ORDER BY m.Data DESC
    """).fetchall()
    
    conn.close()
    
    return render_template(
        'gestao_estoque.html', 
        nome_usuario=session['user_name'],
        produtos=produtos,
        movimentos=movimentos
    )

@app.route('/registrar_movimento', methods=['POST'])
def registrar_movimento():
    if not check_login():
        return redirect(url_for('login'))

    id_produto = request.form['id_produto']
    tipo_operacao = request.form['tipo_operacao']
    try:
        quantidade = int(request.form['quantidade'])
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva.")
    except ValueError as e:
        flash(f"Erro: Quantidade inválida. {e}", 'error')
        return redirect(url_for('gestao_estoque'))

    id_usuario = session['user_id']
    data_hoje = date.today()

    conn = get_db_connection()
    try:
        with conn: 
            produto = conn.execute(
                "SELECT * FROM Produto WHERE ID_produto = ?", (id_produto,)
            ).fetchone()

            if not produto:
                flash("Erro: Produto não encontrado.", 'error')
                return redirect(url_for('gestao_estoque'))

            quantidade_atual = produto['Quantidade']
            estoque_minimo = produto['Estoque_Minimo']
            nova_quantidade = 0

            if tipo_operacao == 'Entrada':
                nova_quantidade = quantidade_atual + quantidade
            elif tipo_operacao == 'Saída':
                nova_quantidade = quantidade_atual - quantidade
                if nova_quantidade < 0:
                    flash(f"Erro: Estoque não pode ficar negativo. (Atual: {quantidade_atual})", 'error')
                    return redirect(url_for('gestao_estoque'))
            
            conn.execute(
                "UPDATE Produto SET Quantidade = ? WHERE ID_produto = ?",
                (nova_quantidade, id_produto)
            )

            conn.execute(
                """INSERT INTO Movimento 
                   (ID_usuario, ID_produto, Data, Tipo_operacao, Quantidade) 
                   VALUES (?, ?, ?, ?, ?)""",
                (id_usuario, id_produto, data_hoje, tipo_operacao, quantidade)
            )
            
            if nova_quantidade < estoque_minimo:
                flash(f"ALERTA: Estoque do produto '{produto['Nome']}' está abaixo do mínimo ({estoque_minimo})!", 'warning')
            else:
                flash(f"Movimentação registrada com sucesso!", 'success')

    except Exception as e:
        flash(f"Erro inesperado no banco de dados: {e}", 'error')
    finally:
        if conn:
            conn.close()
            
    return redirect(url_for('gestao_estoque'))


# --- INICIA O SERVIDOR (Sempre no final do arquivo) ---
if __name__ == '__main__':
    app.run(debug=True)