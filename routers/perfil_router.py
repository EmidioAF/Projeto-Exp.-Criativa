"""
routers/perfil_router.py — Perfil do usuário, edição, exclusão de conta.
TODO: Upload real de imagem (hoje aceita só URL).
"""
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import query_one, query_all, execute
from auth import hash_senha, verificar_senha
from deps import get_usuario_atual

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/perfil", response_class=HTMLResponse)
def perfil(request: Request):
    usuario = get_usuario_atual(request)
    if not usuario:
        return RedirectResponse("/login", status_code=302)

    favoritos = query_all(
        """SELECT j.* FROM jogos j
           JOIN favoritos f ON j.id = f.jogo_id
           WHERE f.usuario_id = %s""",
        (usuario["id"],)
    )
    jogando = query_all(
        """SELECT j.*, sj.status FROM jogos j
           JOIN status_jogo sj ON j.id = sj.jogo_id
           WHERE sj.usuario_id = %s AND sj.status = 'jogando'""",
        (usuario["id"],)
    )
    jogados = query_all(
        """SELECT j.*, sj.status FROM jogos j
           JOIN status_jogo sj ON j.id = sj.jogo_id
           WHERE sj.usuario_id = %s AND sj.status = 'jogado'""",
        (usuario["id"],)
    )
    minhas_reviews = query_all(
        """SELECT r.*, j.nome as jogo_nome FROM reviews r
           JOIN jogos j ON r.jogo_id = j.id
           WHERE r.usuario_id = %s ORDER BY r.criado_em DESC""",
        (usuario["id"],)
    )
    return templates.TemplateResponse("perfil.html", {
        "request": request,
        "usuario": usuario,
        "favoritos": favoritos,
        "jogando": jogando,
        "jogados": jogados,
        "minhas_reviews": minhas_reviews,
        "erro": None,
        "sucesso": None,
    })


@router.post("/perfil/editar")
def editar_perfil(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    foto_url: str = Form(""),
):
    usuario = get_usuario_atual(request)
    if not usuario:
        return RedirectResponse("/login", status_code=302)

    # Verifica duplicatas (excluindo o próprio usuário)
    dup_email = query_one(
        "SELECT id FROM usuarios WHERE email=%s AND id != %s", (email, usuario["id"])
    )
    dup_user = query_one(
        "SELECT id FROM usuarios WHERE username=%s AND id != %s", (username, usuario["id"])
    )
    if dup_email:
        return RedirectResponse("/perfil?erro=email_em_uso", status_code=302)
    if dup_user:
        return RedirectResponse("/perfil?erro=username_em_uso", status_code=302)

    foto = foto_url if foto_url else usuario["foto_url"]
    execute(
        "UPDATE usuarios SET username=%s, email=%s, foto_url=%s WHERE id=%s",
        (username, email, foto, usuario["id"])
    )
    return RedirectResponse("/perfil?sucesso=1", status_code=302)


@router.post("/perfil/senha")
def alterar_senha(
    request: Request,
    senha_atual: str = Form(...),
    nova_senha: str = Form(...),
):
    usuario = get_usuario_atual(request)
    if not usuario:
        return RedirectResponse("/login", status_code=302)
    if not verificar_senha(senha_atual, usuario["senha_hash"]):
        return RedirectResponse("/perfil?erro=senha_incorreta", status_code=302)
    execute(
        "UPDATE usuarios SET senha_hash=%s WHERE id=%s",
        (hash_senha(nova_senha), usuario["id"])
    )
    return RedirectResponse("/perfil?sucesso=senha", status_code=302)


@router.post("/perfil/excluir")
def excluir_conta(request: Request, senha: str = Form(...)):
    usuario = get_usuario_atual(request)
    if not usuario:
        return RedirectResponse("/login", status_code=302)
    if not verificar_senha(senha, usuario["senha_hash"]):
        return RedirectResponse("/perfil?erro=senha_incorreta", status_code=302)
    execute("DELETE FROM usuarios WHERE id=%s", (usuario["id"],))
    resp = RedirectResponse("/", status_code=302)
    resp.delete_cookie("session")
    return resp
