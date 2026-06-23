#!/bin/bash

echo "🚀 Instalando MKNEXARO..."

# Dependências
pip3 install whisper anthropic flask gtts --break-system-packages

# Estrutura
mkdir -p ~/.mknexaro
cp -r agentes ~/.mknexaro/
cp -r skills ~/.mknexaro/

echo "✅ Instalação concluída!"
echo "Para iniciar: python3 agentes/mk-master.py"

