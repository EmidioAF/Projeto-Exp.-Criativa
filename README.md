# The Keep 
Plataforma de biblioteca e reviews de jogos — Projeto Acadêmico (Experiência Criativa)

## Stack
- **Backend**: Python 3.11+ + FastAPI + Jinja2
- **Banco**: MySQL 8+ (adaptável para SQLite)
- **Auth**: bcrypt + cookie assinado (itsdangerous)
- **Frontend**: HTML5 + CSS3 + JS puro

## Estrutura de Pastas
```
the_keep/
├── main.py              # Entrada da aplicação
├── database.py          # Helpers de conexão SQL
├── auth.py              # Hash de senha + sessão
├── deps.py              # Dependências FastAPI (get_usuario, etc.)
├── schema.sql           # SQL inicial do banco
├── requirements.txt
├── .env.example         # Copie para .env e configure
├── routers/
│   ├── auth_router.py   # Login, Cadastro, Logout
│   ├── jogos_router.py  # Biblioteca, detalhes, reviews, favoritos
│   ├── perfil_router.py # Perfil, edição, exclusão
│   └── admin_router.py  # Painel administrativo
├── templates/           # Templates Jinja2
└── static/              # CSS, JS, imagens
```
