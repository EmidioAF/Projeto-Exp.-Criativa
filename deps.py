"""
deps.py — Dependências compartilhadas (usuário logado, admin check).
"""
from fastapi import Request, HTTPException
from database import query_one
from auth import ler_sessao


def get_usuario_atual(request: Request):
    """Retorna dict do usuário logado ou None."""
    token = request.cookies.get("session")
    if not token:
        return None
    uid = ler_sessao(token)
    if not uid:
        return None
    return query_one("SELECT * FROM usuarios WHERE id = %s", (uid,))


def requer_login(request: Request):
    usuario = get_usuario_atual(request)
    if not usuario:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    return usuario


def requer_admin(request: Request):
    usuario = requer_login(request)
    if not usuario.get("is_admin"):
        raise HTTPException(status_code=403, detail="Acesso negado.")
    return usuario
