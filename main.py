"""
main.py — Ponto de entrada da aplicação The Keep.
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from routers import auth_router, jogos_router, perfil_router, admin_router
from deps import get_usuario_atual

app = FastAPI(title="The Keep")

# Arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Registrar routers
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
