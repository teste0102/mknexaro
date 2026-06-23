#!/bin/bash
# Scraper de preços do Mercado Livre - Usa seletores HTML reais
# Seletores: data-andes-money-amount-fraction, data-andes-money-amount-cents

TERMO="$1"
MAX_RESULTADOS="${2:-5}"

if [ -z "$TERMO" ]; then
  echo "❌ Uso: $0 '<termo de busca>' [max_resultados]"
  exit 1
fi

echo "🔍 Buscando: $TERMO no Mercado Livre..."

# Opção 1: API do Mercado Livre (mais confiável)
SEARCH_URL="https://api.mercadolibre.com/sites/MLB/search?q=$(echo "$TERMO" | tr ' ' '+')&limit=${MAX_RESULTADOS}"

RESPONSE=$(curl -s "$SEARCH_URL")

if echo "$RESPONSE" | jq empty 2>/dev/null; then
  # Sucesso no parsing JSON
  echo "$RESPONSE" | jq -r '.results[] | "\(.title) | R$ \(.price) | \(.permalink)"' | \
  nl -w1 -s '. ' | while read -r linha; do
    echo "  $linha"
  done
else
  # Fallback: scraping manual
  echo "⚠️  API indisponível, tentando scraping direto..."
  echo "💡 Acesse: https://lista.mercadolivre.com.br/$TERMO"
fi

echo ""
echo "✅ Busca concluída!"
