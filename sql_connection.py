import sqlite3 
import os

DATABASE_FILE = 'saep.db'

def get_db_connection():
    """
    Cria e retorna uma conexão com o banco SQLite.
    """
    connection = None  # Começa como None
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        connection.row_factory = sqlite3.Row 
        
        # Garante que as tabelas existem
        create_tables_if_not_exist(connection)
        
        print(f"Conexão com SQLite ({DATABASE_FILE}) bem-sucedida!")
        return connection
    except Exception as e:
        print(f"Erro ao conectar ou criar tabelas no SQLite: {e}")
        # Se a conexão foi criada mas algo falhou, fecha ela
        if connection:
            connection.close()
        return None

def create_tables_if_not_exist(connection):
    """
    Cria as tabelas 'Usuario' e 'Produto' se elas não existirem.
    """
    # Usar 'with' gerencia o cursor e o commit/rollback automaticamente
    # e evita o 'UnboundLocalError'
    with connection:
        # Tabela Usuario
        connection.execute("""
        CREATE TABLE IF NOT EXISTS Usuario (
            ID_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT,
            Login TEXT UNIQUE NOT NULL, 
            Senha TEXT
        );
        """)
        
        # Tabela Produto (Necessária para a Entrega 6)
        connection.execute("""
        CREATE TABLE IF NOT EXISTS Produto (
            ID_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Descricao TEXT,
            Quantidade INTEGER NOT NULL DEFAULT 0,
            Estoque_Minimo INTEGER NOT NULL DEFAULT 5,
            Tensao TEXT,
            Dimensoes TEXT,
            Resolucao_Tela TEXT,
            Armazenamento TEXT,
            Conectividade TEXT
        );
        """)
        
        # Tabela Movimento (Necessária para a Entrega 7)
        connection.execute("""
        CREATE TABLE IF NOT EXISTS Movimento (
            ID_movimento INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_usuario INTEGER NOT NULL,
            ID_produto INTEGER NOT NULL,
            Data DATE NOT NULL,
            Tipo_operacao TEXT NOT NULL, -- 'Entrada' ou 'Saída'
            Quantidade INTEGER NOT NULL,
            FOREIGN KEY (ID_usuario) REFERENCES Usuario (ID_usuario),
            FOREIGN KEY (ID_produto) REFERENCES Produto (ID_produto)
        );
        """)