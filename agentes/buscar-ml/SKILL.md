---
name: "buscar-ml"
description: "Busca produtos no Mercado Livre e retorna lista com preços. Use quando o usuário pedir para buscar ou pesquisar produtos no Mercado Livre."
---

# Buscar Produtos no Mercado Livre

Quando o usuário pedir para buscar produtos no Mercado Livre:

## Processo

1. **Use WebSearch** para buscar:
   - Query: `<termo> mercado livre`
   - Filtro: `allowed_domains: ["mercadolivre.com.br"]`

2. **Use WebFetch** nos links do mercadolivre.com.br para extrair:
   - **Preço**: Procure em `<span class="andes-money-amount__fraction">VALOR</span>`
   - **Título**: Tag `<h1>` ou título do produto
   - **Avaliações**: Classe `andes-rating`

3. **Apresente no formato:**

| # | Produto | Preço | Avaliação | Link |
|---|---------|-------|-----------|------|
| 1 | Título | R$ XXX | ⭐ 4.5 | [Ver](url) |

## Seletores HTML do Mercado Livre

### Estrutura Completa do Preço
```html
<span class="andes-money-amount__currency" data-andes-money-amount-currency="true">
  <span class="andes-money-amount__currency-symbol">R$</span>
</span>
<span class="andes-money-amount__fraction" data-andes-money-amount-fraction="true">969</span>
<span class="andes-visually-hidden">,</span>
<span class="andes-money-amount__cents" data-andes-money-amount-cents="true">03</span>
```

### Seletores por Componente
- **Moeda**: `span.andes-money-amount__currency-symbol` → `R$`
- **Inteiro**: `span[data-andes-money-amount-fraction="true"]` → `969`
- **Centavos**: `span[data-andes-money-amount-cents="true"]` → `03`
- **Título**: `<h1 class="ui-pdp-title">`
- **Vendedor**: `<span class="ui-seller-title__label">`
- **Avaliação**: `span.andes-rating`

## Regras
- ✅ Filtre WebSearch apenas para mercadolivre.com.br
- ✅ Use os seletores HTML acima para extrair preços com precisão
- ✅ Máximo 5 resultados
- ✅ Ordene por preço (menor para maior)
- ✅ Apresente em português com R$
- ⚠️ Se WebFetch retornar 403, use Bash com curl + parsing JSON como fallback
