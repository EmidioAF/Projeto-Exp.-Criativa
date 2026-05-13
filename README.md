# The Keep 🏰
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

## Como Rodar

### 1. Clone / copie o projeto
### 2. Crie o banco de dados
```sql
mysql -u root -p < schema.sql
```
### 3. Configure o .env
```bash
cp .env.example .env
# Edite .env com suas credenciais MySQL e uma SECRET_KEY segura
```
### 4. Instale as dependências
```bash
pip install -r requirements.txt
```
### 5. Rode o servidor
```bash
uvicorn main:app --reload
```
Acesse: http://localhost:8000

### Login admin padrão
- Email: `admin@thekeep.com`
- Senha: `admin123`
- **IMPORTANTE**: Gere um novo hash bcrypt e atualize o banco antes de usar em produção!

## O que ainda precisa ser ajustado
Veja a seção de TODOs no código e o arquivo de pendências.
