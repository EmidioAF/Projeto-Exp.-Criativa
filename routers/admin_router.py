"""
routers/admin_router.py — Painel administrativo.
TODO: Paginação na listagem de usuários/jogos.
"""
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import query_one, query_all, execute
from deps import get_usuario_atual, requer_admin

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="templates")


def _check_admin(request: Request):
    u = get_usuario_atual(request)
    if not u or not u["is_admin"]:
        return None
    return u


@router.get("", response_class=HTMLResponse)
def painel(request: Request):
    admin = _check_admin(request)
    if not admin:
        return RedirectResponse("/", status_code=302)
    jogos = query_all("SELECT * FROM jogos ORDER BY nome")
    usuarios = query_all("SELECT id, username, email, is_admin, criado_em FROM usuarios ORDER BY criado_em DESC")
    total_reviews = query_one("SELECT COUNT(*) as c FROM reviews")
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "usuario": admin,
        "jogos": jogos,
        "usuarios": usuarios,
        "total_reviews": total_reviews["c"] if total_reviews else 0,
    })


# ---- CRUD Jogos ----

@router.get("/jogo/novo", response_class=HTMLResponse)
def novo_jogo_form(request: Request):
    admin = _check_admin(request)
    if not admin:
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse("admin_jogo_form.html", {
        "request": request, "usuario": admin, "jogo": None
    })


@router.post("/jogo/novo")
def novo_jogo(
    request: Request,
    nome: str = Form(...),
    desenvolvedora: str = Form(""),
    data_lancamento: str = Form(""),
    descricao: str = Form(""),
    lore: str = Form(""),
    genero: str = Form(""),
    capa_url: str = Form(""),
):
    admin = _check_admin(request)
    if not admin:
        return RedirectResponse("/", status_code=302)
    dt = data_lancamento if data_lancamento else None
    execute(
        """INSERT INTO jogos (nome, desenvolvedora, data_lancamento, descricao, lore, genero, capa_url)
           VALUES (%s,%s,%s,%s,%s,%s,%s)""",
        (nome, desenvolvedora, dt, descricao, lore, genero, capa_url)
    )
    return RedirectResponse("/admin", status_code=302)


@router.get("/jogo/{jogo_id}/editar", response_class=HTMLResponse)
def editar_jogo_form(request: Request, jogo_id: int):
    admin = _check_admin(request)
    if not admin:
        return RedirectResponse("/", status_code=302)
    jogo = query_one("SELECT * FROM jogos WHERE id=%s", (jogo_id,))
    return templates.TemplateResponse("admin_jogo_form.html", {
        "request": request, "usuario": admin, "jogo": jogo
    })


@router.post("/jogo/{jogo_id}/editar")
def editar_jogo(
    request: Request,
    jogo_id: int,
    nome: str = Form(...),
    desenvolvedora: str = Form(""),
    data_lancamento: str = Form(""),
    descricao: str = Form(""),
    lore: str = Form(""),
    genero: str = Form(""),
    capa_url: str = Form(""),
):
    admin = _check_admin(request)
    if not admin:
        return RedirectResponse("/", status_code=302)
    dt = data_lancamento if data_lancamento else None
    execute(
        """UPDATE jogos SET nome=%s, desenvolvedora=%s, data_lancamento=%s,
           descricao=%s, lore=%s, genero=%s, capa_url=%s WHERE id=%s""",
        (nome, desenvolvedora, dt, descricao, lore, genero, capa_url, jogo_id)
    )
    return RedirectResponse("/admin", status_code=302)


@router.post("/jogo/{jogo_id}/excluir")
def excluir_jogo(request: Request, jogo_id: int):
    admin = _check_admin(request)
    if not admin:
        return RedirectResponse("/", status_code=302)
    execute("DELETE FROM jogos WHERE id=%s", (jogo_id,))
    return RedirectResponse("/admin", status_code=302)


# ---- Gerenciar Usuários ----

@router.post("/usuario/{uid}/toggle-admin")
def toggle_admin(request: Request, uid: int):
    admin = _check_admin(request)
    if not admin:
        return RedirectResponse("/", status_code=302)
    usuario = query_one("SELECT * FROM usuarios WHERE id=%s", (uid,))
    if usuario and usuario["id"] != admin["id"]:  # não alterar a si mesmo
        novo = not usuario["is_admin"]
        execute("UPDATE usuarios SET is_admin=%s WHERE id=%s", (novo, uid))
    return RedirectResponse("/admin", status_code=302)


@router.post("/usuario/{uid}/excluir")
def excluir_usuario(request: Request, uid: int):
    admin = _check_admin(request)
    if not admin:
        return RedirectResponse("/", status_code=302)
    if uid != admin["id"]:
        execute("DELETE FROM usuarios WHERE id=%s", (uid,))
    return RedirectResponse("/admin", status_code=302)
