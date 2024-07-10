import sqlite3

def initialize_db():
    conn = sqlite3.connect('controle_pacientes.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_nascimento TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER,
        produto TEXT NOT NULL,
        quantidade TEXT NOT NULL,
        data TEXT NOT NULL,
        FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
    )
    ''')
    
    conn.commit()
    conn.close()

def add_paciente(nome, data_nascimento):
    conn = sqlite3.connect('controle_pacientes.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO pacientes (nome, data_nascimento) VALUES (?, ?)', (nome, data_nascimento))
    conn.commit()
    conn.close()

def get_pacientes():
    conn = sqlite3.connect('controle_pacientes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pacientes')
    pacientes = cursor.fetchall()
    conn.close()
    return pacientes

def add_produto(paciente_id, produto, quantidade, data):
    conn = sqlite3.connect('controle_pacientes.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO produtos (paciente_id, produto, quantidade, data) VALUES (?, ?, ?, ?)', (paciente_id, produto, quantidade, data))
    conn.commit()
    conn.close()

def get_produtos(paciente_id):
    conn = sqlite3.connect('controle_pacientes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos WHERE paciente_id = ?', (paciente_id,))
    produtos = cursor.fetchall()
    conn.close()
    return produtos

def delete_paciente(paciente_id):
    conn = sqlite3.connect('controle_pacientes.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pacientes WHERE id = ?', (paciente_id,))
    cursor.execute('DELETE FROM produtos WHERE paciente_id = ?', (paciente_id,))
    conn.commit()
    conn.close()
