import re
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import query_one, execute
from auth import hash_senha, verificar_senha, criar_sessao, SESSION_MAX_AGE
from deps import get_usuario_atual

router = APIRouter()
templates = Jinja2Templates(directory="templates")

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def email_valido(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email.strip().lower()))


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    if get_usuario_atual(request):
        return RedirectResponse("/biblioteca", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "erro": None})


@router.post("/login")
def login_action(request: Request, email: str = Form(...), senha: str = Form(...)):
    usuario = query_one("SELECT * FROM usuarios WHERE email = %s", (email,))
    if not usuario or not verificar_senha(senha, usuario["senha_hash"]):
        return templates.TemplateResponse("login.html", {
            "request": request, "erro": "Email ou senha incorretos."
        })
    token = criar_sessao(usuario["id"])
    resp = RedirectResponse("/biblioteca", status_code=302)
    resp.set_cookie("session", token, httponly=True, max_age=SESSION_MAX_AGE, samesite="lax")
    return resp


@router.get("/cadastro", response_class=HTMLResponse)
def cadastro_page(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request, "erro": None})


@router.post("/cadastro")
def cadastro_action(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
):
    if len(username.strip()) < 3:
        return templates.TemplateResponse("cadastro.html", {
            "request": request,
            "erro": "Username deve ter pelo menos 3 caracteres."
        })
    if not email_valido(email):
        return templates.TemplateResponse("cadastro.html", {
            "request": request,
            "erro": "Email inválido. Use um formato como usuario@dominio.com."
        })
    if query_one("SELECT id FROM usuarios WHERE email = %s", (email,)):
        return templates.TemplateResponse("cadastro.html", {
            "request": request, "erro": "Email já cadastrado."
        })
    if query_one("SELECT id FROM usuarios WHERE username = %s", (username,)):
        return templates.TemplateResponse("cadastro.html", {
            "request": request, "erro": "Username já em uso."
        })
    execute(
        "INSERT INTO usuarios (username, email, senha_hash) VALUES (%s, %s, %s)",
        (username.strip(), email.strip().lower(), hash_senha(senha))
    )
    return RedirectResponse("/login?cadastro=ok", status_code=302)


@router.get("/logout")
def logout():
    resp = RedirectResponse("/", status_code=302)
    resp.delete_cookie("session")
    return resp
