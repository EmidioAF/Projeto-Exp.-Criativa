from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import query_one, query_all, execute
from deps import get_usuario_atual

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/biblioteca", response_class=HTMLResponse)
def biblioteca(request: Request, q: str = "", genero: str = ""):
    usuario = get_usuario_atual(request)
    sql = "SELECT * FROM jogos WHERE 1=1"
    params = []
    if q:
        sql += " AND nome LIKE %s"
        params.append(f"%{q}%")
    if genero:
        sql += " AND genero = %s"
        params.append(genero)
    jogos = query_all(sql, params)
    generos = query_all("SELECT DISTINCT genero FROM jogos WHERE genero IS NOT NULL")
    return templates.TemplateResponse("biblioteca.html", {
        "request": request, "usuario": usuario,
        "jogos": jogos, "generos": generos,
        "q": q, "genero_sel": genero,
    })


@router.get("/jogo/{jogo_id}", response_class=HTMLResponse)
def detalhe_jogo(request: Request, jogo_id: int):
    usuario = get_usuario_atual(request)
    jogo = query_one("SELECT * FROM jogos WHERE id = %s", (jogo_id,))
    if not jogo:
        return templates.TemplateResponse("404.html", {"request": request, "usuario": usuario})

    reviews = query_all(
        """SELECT r.*, u.username, u.foto_url FROM reviews r
           JOIN usuarios u ON r.usuario_id = u.id
           WHERE r.jogo_id = %s ORDER BY r.criado_em DESC""", (jogo_id,)
    )
    minha_review = meu_status = None
    favoritado = False
    if usuario:
        minha_review = query_one(
            "SELECT * FROM reviews WHERE usuario_id=%s AND jogo_id=%s",
            (usuario["id"], jogo_id)
        )
        meu_status = query_one(
            "SELECT status FROM status_jogo WHERE usuario_id=%s AND jogo_id=%s",
            (usuario["id"], jogo_id)
        )
        favoritado = bool(query_one(
            "SELECT id FROM favoritos WHERE usuario_id=%s AND jogo_id=%s",
            (usuario["id"], jogo_id)
        ))

    return templates.TemplateResponse("jogo_detalhe.html", {
        "request": request, "usuario": usuario, "jogo": jogo,
        "reviews": reviews, "minha_review": minha_review,
        "meu_status": meu_status["status"] if meu_status else None,
        "favoritado": favoritado,
    })


@router.post("/jogo/{jogo_id}/review")
def salvar_review(request: Request, jogo_id: int, nota: int = Form(...), comentario: str = Form("")):
    usuario = get_usuario_atual(request)
    if not usuario:
        return RedirectResponse("/login", status_code=302)
    existente = query_one(
        "SELECT id FROM reviews WHERE usuario_id=%s AND jogo_id=%s",
        (usuario["id"], jogo_id)
    )
    if existente:
        execute("UPDATE reviews SET nota=%s, comentario=%s WHERE id=%s",
                (nota, comentario, existente["id"]))
    else:
        execute("INSERT INTO reviews (usuario_id, jogo_id, nota, comentario) VALUES (%s,%s,%s,%s)",
                (usuario["id"], jogo_id, nota, comentario))
    media = query_one("SELECT AVG(nota) as m FROM reviews WHERE jogo_id=%s", (jogo_id,))
    execute("UPDATE jogos SET media_reviews=%s WHERE id=%s", (media["m"] or 0, jogo_id))
    return RedirectResponse(f"/jogo/{jogo_id}", status_code=302)


@router.post("/review/{review_id}/excluir")
def excluir_review(request: Request, review_id: int):
    usuario = get_usuario_atual(request)
    if not usuario:
        return RedirectResponse("/login", status_code=302)
    rev = query_one("SELECT * FROM reviews WHERE id=%s", (review_id,))
    if rev and (rev["usuario_id"] == usuario["id"] or usuario["is_admin"]):
        jogo_id = rev["jogo_id"]
        execute("DELETE FROM reviews WHERE id=%s", (review_id,))
        media = query_one("SELECT AVG(nota) as m FROM reviews WHERE jogo_id=%s", (jogo_id,))
        execute("UPDATE jogos SET media_reviews=%s WHERE id=%s", (media["m"] or 0, jogo_id))
        return RedirectResponse(f"/jogo/{jogo_id}", status_code=302)
    return RedirectResponse("/biblioteca", status_code=302)


@router.post("/jogo/{jogo_id}/favoritar")
def favoritar(request: Request, jogo_id: int):
    usuario = get_usuario_atual(request)
    if not usuario:
        return RedirectResponse("/login", status_code=302)
    fav = query_one("SELECT id FROM favoritos WHERE usuario_id=%s AND jogo_id=%s",
                    (usuario["id"], jogo_id))
    if fav:
        execute("DELETE FROM favoritos WHERE id=%s", (fav["id"],))
    else:
        execute("INSERT INTO favoritos (usuario_id, jogo_id) VALUES (%s,%s)",
                (usuario["id"], jogo_id))
    return RedirectResponse(f"/jogo/{jogo_id}", status_code=302)


@router.post("/jogo/{jogo_id}/status")
def atualizar_status(request: Request, jogo_id: int, status: str = Form(...)):
    usuario = get_usuario_atual(request)
    if not usuario:
        return RedirectResponse("/login", status_code=302)
    existente = query_one(
        "SELECT id FROM status_jogo WHERE usuario_id=%s AND jogo_id=%s",
        (usuario["id"], jogo_id)
    )
    if existente:
        execute("UPDATE status_jogo SET status=%s WHERE id=%s", (status, existente["id"]))
    else:
        execute("INSERT INTO status_jogo (usuario_id, jogo_id, status) VALUES (%s,%s,%s)",
                (usuario["id"], jogo_id, status))
    return RedirectResponse(f"/jogo/{jogo_id}", status_code=302)