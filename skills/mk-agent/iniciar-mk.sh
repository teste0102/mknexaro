#!/bin/bash

echo "🚀 Iniciando MK Agent..."

# Abre servidor web
python3 ~/.claude/skills/mk-agent/mk-web-completo.py &

# Espera 2 segundos e abre Claude Code
sleep 2
claude &

echo "✅ Tudo aberto! Fale na web quando ela abrir!"

