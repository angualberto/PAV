# PAV — Padaria Bom Pão

Projeto de exemplo que implementa uma API REST simples para uma padaria,
com modelos SQLAlchemy, validações, uma GUI Tkinter opcional e um notebook
com exemplos de chamadas à API.

**Resumo rápido**
- API Flask em `/api` com recursos para `products`, `customers` e `orders`.
- Banco SQLite local: `padaria.db` (ignorado no repositório via `.gitignore`).

## Requisitos
- Python 3.8+
- `git` (para versionamento)
- (opcional) Vagrant + VirtualBox para provisionamento automático

## Setup rápido (local)
Abra um terminal na pasta do projeto (`~/Documentos/Pav`) e execute:

```bash
# criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# atualizar pip e instalar dependências
pip install --upgrade pip
pip install -r requirements.txt
```

Se não existir `requirements.txt`, instale manualmente:

```bash
pip install flask flask-restful flask-sqlalchemy requests sqlalchemy
```

## Rodando a API
Com o `venv` ativado, execute:

```bash
python app.py
```

Isso cria as tabelas (via `Base.metadata.create_all`) e inicia o servidor de
desenvolvimento em `http://127.0.0.1:5000`.

Para rodar em background e salvar logs:

```bash
nohup venv/bin/python app.py > flask.log 2>&1 &
tail -f flask.log
```

Se a porta `5000` já estiver em uso, mate o processo ou altere a porta:

```bash
# matar processo na porta 5000
fuser -k 5000/tcp

# ou alterar porta diretamente em app.py: app.run(port=5001)
```

## GUI (opcional)
Se quiser usar a interface Tkinter (arquivo `gui/padaria_gui.py`):

```bash
source venv/bin/activate
python gui/padaria_gui.py > gui.log 2>&1 &
tail -f gui.log
```

Obs.: a GUI usa display gráfico. Em Vagrant a provision script já configura VNC.

## Notebook de demonstração
O notebook com exemplos de requisições está em `notebooks/demo_api.ipynb`.
Abra com:

```bash
source venv/bin/activate
jupyter notebook notebooks/demo_api.ipynb
```

## Endpoints principais
- `GET /api/products` — lista produtos
- `POST /api/products` — cria produto (veja cabeçalho `X-API-KEY` no notebook)
- `GET /api/products/<id>` — obter produto
- `PUT /api/products/<id>` — atualizar produto
- `DELETE /api/products/<id>` — remover (soft-delete)
- `GET/POST /api/customers` — gerenciar clientes
- `GET/POST /api/orders` — criar/consultar pedidos

## Boas práticas e observações
- `padaria.db` está no .gitignore para não subir o banco ao Git.
- Atualmente o projeto retorna instâncias ORM em alguns controllers — é
	recomendado serializar (transformar em dict/JSON) antes de fechar a sessão.
- Ajustei `db.py` para `expire_on_commit=False` para evitar erros de instância
	desanexada; para produção use um WSGI server (gunicorn/uvicorn) e revise a
	gestão de sessão/serialização.

## Rodando com Vagrant (opcional)
Existe um `Vagrantfile` e `provision.sh` que instalam dependências, criam o
venv e iniciam a API + GUI automaticamente. Para usar:

```bash
vagrant up
```

Após provisionamento, a API deve ficar disponível em `http://127.0.0.1:5000`.

## Git & deploy rápido
- Já há um `.gitignore` preparado. Para subir ao GitHub:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPO.git
git push -u origin main
```

## Problemas comuns
- Erro: porta 5000 ocupada — mate o processo ou altere a porta.
- Erro: permissão ao criar arquivos — verifique permissões da pasta e venv.

---
Se quiser, eu posso:
- gerar/atualizar `requirements.txt` e commitar aqui, ou
- adicionar exemplos de serialização nos controllers (`resources/`), ou
- abrir um PR com melhorias (por exemplo usar marshmallow/pydantic para
	schemas).



