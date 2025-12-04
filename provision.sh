#!/usr/bin/env bash
set -e

# Atualiza e instala pacotes necessários (XFCE desktop + VNC + Python)
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y \
  python3 python3-venv python3-pip git \
  xfce4 xfce4-goodies dbus-x11 x11-xserver-utils \
  tigervnc-standalone-server xterm

# Ir para pasta do projeto sincronizado
cd /vagrant

# Criar venv e instalar dependências Python
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
. venv/bin/activate
pip install --upgrade pip
pip install flask flask-restful flask-sqlalchemy requests sqlalchemy

# Garantir permissões
chown -R vagrant:vagrant /vagrant

# Criar DB e iniciar Flask (rodando em background)
if [ ! -f "padaria.db" ]; then
  # criar DB via app.py (app.py chama create_all)
  nohup /vagrant/venv/bin/python /vagrant/app.py > /vagrant/flask.log 2>&1 &
  sleep 2
else
  nohup /vagrant/venv/bin/python /vagrant/app.py > /vagrant/flask.log 2>&1 &
  sleep 2
fi

# Configurar VNC (senha simples: 'vagrant') e iniciar servidor VNC como root (provision run como root)
mkdir -p /root/.vnc
echo "vagrant" | vncpasswd -f > /root/.vnc/passwd
chmod 600 /root/.vnc/passwd
cat >/root/.vnc/xstartup <<'XSTART'
#!/bin/sh
xrdb $HOME/.Xresources
startxfce4 &
XSTART
chmod +x /root/.vnc/xstartup

# Iniciar VNC display :1
vncserver :1 -geometry 1024x768 -depth 24 || true

# Iniciar GUI Tkinter apontando para DISPLAY :1 (em background)
export DISPLAY=":1"
nohup /vagrant/venv/bin/python /vagrant/gui/padaria_gui.py > /vagrant/gui.log 2>&1 &

echo "Provision complete. Flask logs: /vagrant/flask.log, GUI logs: /vagrant/gui.log"
echo "Acesse API: http://127.0.0.1:5000 (no host). Conecte VNC em localhost:5901 com senha 'vagrant'."
