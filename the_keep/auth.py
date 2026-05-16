import os
import bcrypt
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "chave_dev_insegura_troque")
SESSION_MAX_AGE = int(os.getenv("SESSION_MAX_AGE", 1800))

_signer = URLSafeTimedSerializer(SECRET_KEY)


def hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()


def verificar_senha(senha: str, hash_: str) -> bool:
    return bcrypt.checkpw(senha.encode(), hash_.encode())


def criar_sessao(usuario_id: int) -> str:
    return _signer.dumps({"id": usuario_id})


def ler_sessao(token: str):
    try:
        data = _signer.loads(token, max_age=SESSION_MAX_AGE)
        return data["id"]
    except (BadSignature, SignatureExpired, Exception):
        return None