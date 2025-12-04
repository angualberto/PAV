#!/usr/bin/env bash
set -e

# ir para o diretório do projeto
cd "$(dirname "$0")"

# criar/ativar venv
python3 -m venv venv
source venv/bin/activate

# atualizar pip e criar requirements
pip install --upgrade pip
cat > requirements.txt <<'REQ'
flask
flask-restful
flask-sqlalchemy
requests
sqlalchemy
REQ

pip install -r requirements.txt

# parar processo que possa estar usando a porta 5000
if lsof -ti:5000 >/dev/null 2>&1; then
  echo 'Matando processo que usa porta 5000...'
  fuser -k 5000/tcp || true
fi

# iniciar API em background e coletar logs
echo 'Iniciando API...'
nohup venv/bin/python app.py > flask.log 2>&1 &

# esperar um pouco e mostrar primeiros logs
sleep 2
echo '=== flask.log (últimas 200 linhas) ==='
tail -n 200 flask.log || true

# iniciar GUI se existir
if [ -f gui/padaria_gui.py ]; then
  echo 'Iniciando GUI (se disponível)...'
  nohup venv/bin/python gui/padaria_gui.py > gui.log 2>&1 &
  sleep 1
  echo '=== gui.log (últimas 100 linhas) ==='
  tail -n 100 gui.log || true
fi

echo "Pronto. API: http://127.0.0.1:5000 (ver flask.log para detalhes)"
