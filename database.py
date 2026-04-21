import mysql.connector
import bcrypt

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="SUA_SENHA_AQUI",
        database="thekeep_db"
    )

def criar_usuario(nome, email, senha):
    conn = get_connection()
    cursor = conn.cursor()

    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

    sql = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
    valores = (nome, email, senha_hash.decode('utf-8'))

    cursor.execute(sql, valores)
    conn.commit()

    usuario_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return usuario_id

def autenticar_usuario(email, senha):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT * FROM usuarios WHERE email = %s"
    cursor.execute(sql, (email,))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario["senha"].encode('utf-8')):
        return True

    return False
