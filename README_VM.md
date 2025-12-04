Instruções rápidas para levantar VM, API e GUI

Requisitos no host:
- VirtualBox instalado
- Vagrant instalado

Passos:
1) Abra terminal no diretório /home/andre/Documentos/Pav
2) Inicie a VM:
   vagrant up
   (o provision.sh fará install e iniciará o Flask e o VNC)
3) A API ficará disponível em: http://127.0.0.1:5000
4) Para ver a interface gráfica (Tkinter) conecte um cliente VNC ao endereço:
   localhost:5901
   senha: vagrant
5) Logs no host (pasta do projeto):
   - flask.log
   - gui.log

Parar a VM:
   vagrant halt

Destruir VM:
   vagrant destroy -f
