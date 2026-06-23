#!/bin/bash

echo "🛑 Fechando portas antigas..."
sudo fuser -k 8100/tcp 8101/tcp 8102/tcp 8110/tcp 9000/tcp 2>/dev/null

sleep 2

echo "🚀 Iniciando todos os serviços..."

# Terminal 1 - Email
nohup python3 ~/projetos/mknexaro/apis/api-email.py > ~/.mk-email.log 2>&1 &
echo "✅ API Email (port 8100)"

# Terminal 2 - Loja
nohup python3 ~/projetos/mknexaro/apis/api-loja.py > ~/.mk-loja.log 2>&1 &
echo "✅ API Loja (port 8101)"

# Terminal 3 - GitHub
nohup python3 ~/projetos/mknexaro/apis/api-github.py > ~/.mk-github.log 2>&1 &
echo "✅ API GitHub (port 8102)"

# Terminal 4 - Integrador
nohup python3 ~/projetos/mknexaro/apis/integrador.py > ~/.mk-integrador.log 2>&1 &
echo "✅ Integrador (port 8110)"

sleep 2

# Terminal 5 - Interface
nohup python3 ~/projetos/mknexaro/apis/interface.py > ~/.mk-interface.log 2>&1 &
echo "✅ Interface Web (port 9000)"

sleep 2

echo ""
echo "🎉 TODOS OS SERVIÇOS INICIADOS!"
echo ""
echo "Acesse: http://localhost:9000"
echo ""
echo "Para ver logs:"
echo "  tail -f ~/.mk-email.log"
echo "  tail -f ~/.mk-loja.log"
echo "  tail -f ~/.mk-github.log"
echo "  tail -f ~/.mk-integrador.log"
echo "  tail -f ~/.mk-interface.log"

