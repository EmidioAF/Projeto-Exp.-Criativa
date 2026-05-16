import sys

try:
    import bcrypt
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "bcrypt"])
    import bcrypt

try:
    import pymysql
    from dotenv import load_dotenv
    import os
    load_dotenv()
except ImportError:
    print("Execute: pip install -r requirements.txt primeiro.")
    sys.exit(1)

print("=== The Keep — Criar Admin ===")
email = input("Email do admin: ").strip()
senha = input("Senha do admin: ").strip()

if not senha:
    print("Senha não pode ser vazia.")
    sys.exit(1)

hash_ = bcrypt.hashpw(senha.encode(), bcrypt.gensalt(rounds=12)).decode()

conn = pymysql.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "the_keep"),
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True,
)

with conn.cursor() as cur:
    existe = cur.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
    if existe:
        cur.execute("UPDATE usuarios SET senha_hash=%s, is_admin=TRUE WHERE email=%s", (hash_, email))
        print(f"✔ Admin '{email}' atualizado!")
    else:
        username = email.split("@")[0]
        cur.execute(
            "INSERT INTO usuarios (username, email, senha_hash, is_admin) VALUES (%s,%s,%s,TRUE)",
            (username, email, hash_)
        )
        print(f"✔ Admin '{email}' criado!")

conn.close()
print("Acesse: http://localhost:8000/login")