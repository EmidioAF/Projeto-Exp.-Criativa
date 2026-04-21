import mysql.connector
import bcrypt

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="SUA_SENHA_AQUI",
        database="thekeep_db"
    )

# =========================
# USUÁRIOS
# =========================

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
        return {
            "id": usuario["id"],
            "nome": usuario["nome"],
            "email": usuario["email"]
        }

    return None

def buscar_usuario_por_id(usuario_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT id, nome, email, criado_em FROM usuarios WHERE id = %s"
    cursor.execute(sql, (usuario_id,))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    return usuario

def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT id, nome, email, criado_em FROM usuarios"
    cursor.execute(sql)
    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()

    return usuarios

def atualizar_usuario(usuario_id, nome, email):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "UPDATE usuarios SET nome = %s, email = %s WHERE id = %s"
    cursor.execute(sql, (nome, email, usuario_id))
    conn.commit()

    cursor.close()
    conn.close()

def deletar_usuario(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "DELETE FROM usuarios WHERE id = %s"
    cursor.execute(sql, (usuario_id,))
    conn.commit()

    cursor.close()
    conn.close()

# =========================
# JOGOS
# =========================

def listar_jogos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT * FROM jogos"
    cursor.execute(sql)
    jogos = cursor.fetchall()

    cursor.close()
    conn.close()

    return jogos

def buscar_jogo_por_id(jogo_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT * FROM jogos WHERE id = %s"
    cursor.execute(sql, (jogo_id,))
    jogo = cursor.fetchone()

    cursor.close()
    conn.close()

    return jogo

# =========================
# REVIEWS
# =========================

def criar_review(usuario_id, jogo_id, nota, comentario):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO reviews (usuario_id, jogo_id, nota, comentario)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (usuario_id, jogo_id, nota, comentario))
    conn.commit()

    review_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return review_id

def listar_reviews_por_jogo(jogo_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT r.id, u.nome AS usuario, r.nota, r.comentario, r.criado_em
        FROM reviews r
        JOIN usuarios u ON r.usuario_id = u.id
        WHERE r.jogo_id = %s
        ORDER BY r.criado_em DESC
    """
    cursor.execute(sql, (jogo_id,))
    reviews = cursor.fetchall()

    cursor.close()
    conn.close()

    return reviews

def atualizar_review(review_id, nota, comentario):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "UPDATE reviews SET nota = %s, comentario = %s WHERE id = %s"
    cursor.execute(sql, (nota, comentario, review_id))
    conn.commit()

    cursor.close()
    conn.close()

def deletar_review(review_id):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "DELETE FROM reviews WHERE id = %s"
    cursor.execute(sql, (review_id,))
    conn.commit()

    cursor.close()
    conn.close()

# =========================
# LISTA DE JOGOS
# =========================

def adicionar_ou_atualizar_lista(usuario_id, jogo_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    sql_verifica = "SELECT id FROM lista_jogos WHERE usuario_id = %s AND jogo_id = %s"
    cursor.execute(sql_verifica, (usuario_id, jogo_id))
    existente = cursor.fetchone()

    if existente:
        sql_update = "UPDATE lista_jogos SET status = %s WHERE usuario_id = %s AND jogo_id = %s"
        cursor.execute(sql_update, (status, usuario_id, jogo_id))
    else:
        sql_insert = """
            INSERT INTO lista_jogos (usuario_id, jogo_id, status)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql_insert, (usuario_id, jogo_id, status))

    conn.commit()
    cursor.close()
    conn.close()

def listar_lista_usuario(usuario_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT j.titulo, l.status
        FROM lista_jogos l
        JOIN jogos j ON l.jogo_id = j.id
        WHERE l.usuario_id = %s
    """
    cursor.execute(sql, (usuario_id,))
    lista = cursor.fetchall()

    cursor.close()
    conn.close()

    return lista

def remover_da_lista(usuario_id, jogo_id):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "DELETE FROM lista_jogos WHERE usuario_id = %s AND jogo_id = %s"
    cursor.execute(sql, (usuario_id, jogo_id))
    conn.commit()

    cursor.close()
    conn.close()
