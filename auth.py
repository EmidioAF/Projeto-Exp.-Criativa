"""
auth.py — Helpers de autenticação: hash de senha, sessão.
Sessão simples via cookie assinado com itsdangerous.
TODO: Implementar logout automático por inatividade no middleware.
"""
import os
import bcrypt
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "chave_dev_insegura_troque")
SESSION_MAX_AGE = int(os.getenv("SESSION_MAX_AGE", 1800))  # segundos

_signer = URLSafeTimedSerializer(SECRET_KEY)


# ---------- Senha ----------

def hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()


def verificar_senha(senha: str, hash_: str) -> bool:
    return bcrypt.checkpw(senha.encode(), hash_.encode())


# ---------- Sessão ----------

def criar_sessao(usuario_id: int) -> str:
    """Retorna token assinado com o ID do usuário."""
    return _signer.dumps({"id": usuario_id})


def ler_sessao(token: str) -> int | None:
    """Retorna o ID do usuário ou None se inválido/expirado."""
    try:
        data = _signer.loads(token, max_age=SESSION_MAX_AGE)
        return data["id"]
    except (BadSignature, SignatureExpired, Exception):
        return None
