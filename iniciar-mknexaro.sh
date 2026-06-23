#!/bin/bash

echo "🛑 Fechando portas..."
sudo fuser -k 8100/tcp 8101/tcp 8102/tcp 8110/tcp 9000/tcp 2>/dev/null
sleep 2

echo "🚀 Iniciando MKNEXARO..."

# Inicia cada API
python3 ~/projetos/mknexaro/apis/api-email.py &
sleep 1

python3 ~/projetos/mknexaro/apis/api-loja.py &
sleep 1

python3 ~/projetos/mknexaro/apis/api-github.py &
sleep 1

python3 ~/projetos/mknexaro/apis/integrador.py &
sleep 1

python3 ~/projetos/mknexaro/apis/interface.py &

sleep 2
echo "✅ TUDO ONLINE!"
echo "Acesse: http://localhost:9000"

