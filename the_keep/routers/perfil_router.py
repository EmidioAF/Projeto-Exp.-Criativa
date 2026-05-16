import re
import os
import uuid
from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import query_one, query_all, execute
from auth import hash_senha, verificar_senha
from deps import get_usuario_atual

router = APIRouter()
templates = Jinja2Templates(directory="templates")

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
UPLOAD_DIR = "static/img/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
EXTENSOES_PERMITIDAS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

def email_valido(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email.strip().lower()))


@router.get("/perfil", response_class=HTMLResponse)
def perfil(request: Request):
    usuario = get_usuario_atual(request)
    if not usuario:
        return RedirectResponse("/login", status_code=302)

    favoritos = query_all(
        """SELECT j.* FROM jogos j JOIN favoritos f ON j.id = f.jogo_id
           WHERE f.usuario_id = %s""", (usuario["id"],)
    )
    jogando = query_all(
        """SELECT j.* FROM jogos j JOIN status_jogo sj ON j.id = sj.jogo_id
           WHERE sj.usuario_id = %s AND sj.status = 'jogando'""", (usuario["id"],)
    )
    jogados = query_all(
        """SELECT j.* FROM jogos j JOIN status_jogo sj ON j.id = sj.jogo_id
           WHERE sj.usuario_id = %s AND sj.status = 'jogado'""", (usuario["id"],)
    )
    minhas_reviews = query_all(
        """SELECT r.*, j.nome as jogo_nome FROM reviews r
           JOIN jogos j ON r.jogo_id = j.id
           WHERE r.usuario_id = %s ORDER BY r.criado_em DESC""", (usuario["id"],)
    )

    erros = {
        "email_em_uso":    "Este email já está em uso.",
        "username_em_uso": "Este username já está em uso.",
        "senha_incorreta": "Senha incorreta.",
        "email_invalido":  "Email inválido. Use um formato como usuario@dominio.com.",
        "username_curto":  "Username deve ter pelo menos 3 caracteres.",
        "foto_invalida":   "Formato inválido. Use JPG, PNG, GIF ou WEBP.",
        "foto_grande":     "Imagem muito grande. Máximo 2MB.",
    }
    sucesso_msgs = {
        "perfil": "Perfil atualizado com sucesso!",
        "senha":  "Senha alterada com sucesso!",
        "foto":   "Foto atualizada com sucesso!",
    }
    qp = request.query_params

    return templates.TemplateResponse("perfil.html", {
        "request": request,
        "usuario": usuario,
        "favoritos": favoritos,
        "jogando": jogando,
        "jogados": jogados,
        "minhas_reviews": minhas_reviews,
        "erro": erros.get(qp.get("erro", "")),
        "sucesso": sucesso_msgs.get(qp.get("sucesso", "")),
    })


@router.post("/perfil/editar")
def editar_perfil(request: Request, username: str = Form(...), email: str = Form(...)):
    usuario = get_usuario_atual(request)
    if not usuario:
        return RedirectResponse("/login", status_code=302)
    if len(username.strip()) < 3:
        return RedirectResponse("/perfil?erro=username_curto", status_code=302)
    if not email_valido(email):
        return RedirectResponse("/perfil?erro=email_invalido", status_code=302)
    if query_one("SELECT id FROM usuarios WHERE email=%s AND id != %s", (email, usuario["id"])):
        return RedirectResponse("/perfil?erro=email_em_uso", status_code=302)
    if query_one("SELECT id FROM usuarios WHERE username=%s AND id != %s", (username, usuario["id"])):
        return RedirectResponse("/perfil?erro=username_em_uso", status_code=302)
    execute(
        "UPDATE usuarios SET username=%s, email=%s WHERE id=%s",
        (username.strip(), email.strip().lower(), usuario["id"])
    )
    return RedirectResponse("/perfil?sucesso=perfil", status_code=302)


@router.post("/perfil/foto")
async def upload_foto(request: Request, foto: UploadFile = File(...)):
    usuario = get_usuario_atual(request)
    if not usuario:
        return RedirectResponse("/login", status_code=302)
    ext = os.path.splitext(foto.filename or "")[1].lower()
    if ext not in EXTENSOES_PERMITIDAS:
        return RedirectResponse("/perfil?erro=foto_invalida", status_code=302)
    conteudo = await foto.read()
    if len(conteudo) > 2 * 1024 * 1024:
        return RedirectResponse("/perfil?erro=foto_grande", status_code=302)
    nome_arquivo = f"{uuid.uuid4().hex}{ext}"
    with open(os.path.join(UPLOAD_DIR, nome_arquivo), "wb") as f:
        f.write(conteudo)
    foto_antiga = usuario.get("foto_url", "")
    if foto_antiga and "avatar_default" not in foto_antiga and "/uploads/" in foto_antiga:
        try:
            os.remove(foto_antiga.lstrip("/"))
        except OSError:
            pass
    execute("UPDATE usuarios SET foto_url=%s WHERE id=%s",
            (f"/static/img/uploads/{nome_arquivo}", usuario["id"]))
    return RedirectResponse("/perfil?sucesso=foto", status_code=302)


@router.post("/perfil/senha")
def alterar_senha(request: Request, senha_atual: str = Form(...), nova_senha: str = Form(...)):
    usuario = get_usuario_atual(request)
    if not usuario:
        return RedirectResponse("/login", status_code=302)
    if not verificar_senha(senha_atual, usuario["senha_hash"]):
        return RedirectResponse("/perfil?erro=senha_incorreta", status_code=302)
    execute("UPDATE usuarios SET senha_hash=%s WHERE id=%s",
            (hash_senha(nova_senha), usuario["id"]))
    return RedirectResponse("/perfil?sucesso=senha", status_code=302)


@router.post("/perfil/excluir")
def excluir_conta(request: Request, senha: str = Form(...)):
    usuario = get_usuario_atual(request)
    if not usuario:
        return RedirectResponse("/login", status_code=302)
    if not verificar_senha(senha, usuario["senha_hash"]):
        return RedirectResponse("/perfil?erro=senha_incorreta", status_code=302)
    foto = usuario.get("foto_url", "")
    if foto and "/uploads/" in foto:
        try:
            os.remove(foto.lstrip("/"))
        except OSError:
            pass
    execute("DELETE FROM usuarios WHERE id=%s", (usuario["id"],))
    resp = RedirectResponse("/", status_code=302)
    resp.delete_cookie("session")
    return resp