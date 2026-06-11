from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from routers import auth_router, jogos_router, perfil_router, admin_router
from deps import get_usuario_atual
from auth import ler_sessao

app = FastAPI(title="The Keep")

@app.middleware("http")
async def limpar_sessao_expirada(request: Request, call_next):
    token = request.cookies.get("session")
    if token and ler_sessao(token) is None:
        rotas_publicas = ["/login", "/cadastro", "/static", "/"]
        if not any(request.url.path.startswith(r) for r in rotas_publicas):
            response = RedirectResponse("/login", status_code=302)
            response.delete_cookie("session")
            return response
    return await call_next(request)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(auth_router.router)
app.include_router(jogos_router.router)
app.include_router(perfil_router.router)
app.include_router(admin_router.router)


@app.get("/", response_class=HTMLResponse)
def landing(request: Request):
    usuario = get_usuario_atual(request)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "usuario": usuario,
    })
