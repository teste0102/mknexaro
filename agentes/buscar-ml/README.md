# Buscar ML - Skill Melhorada

Busca produtos no Mercado Livre com preços atualizados e informações completas.

## ✨ Melhorias Implementadas

### 1. Seletores HTML Precisos
- Agora usa os seletores corretos do Mercado Livre
- Extrai preço de: `<span class="andes-money-amount__fraction">`
- Funciona mesmo com bloqueios básicos

### 2. Fallback com API
- Se WebFetch falhar (403), usa a API pública do ML
- Script `scraper.sh` fornece dados em JSON
- Mais confiável e rápido

### 3. Informações Completas
- ✅ Preço (inteiro + centavos)
- ✅ Avaliação do vendedor
- ✅ Link direto
- ✅ Ordenado por preço

## 🚀 Como Usar

```bash
# Básico
/buscar-ml tela A15 4g

# Com mais detalhes
/buscar-ml samsung galaxy a15

# Produto específico
/buscar-ml display lcd a15
```

## 📊 Resultado Esperado

| # | Produto | Preço | Avaliação | Link |
|---|---------|-------|-----------|------|
| 1 | Tela Display A15 4G | R$ 89,90 | ⭐ 4.8 | [Ver](link) |
| 2 | Tela Compatível A15 | R$ 109,00 | ⭐ 4.5 | [Ver](link) |

## 🛠️ Técnicas Usadas

1. **WebSearch** - Busca inicial filtrada por domínio
2. **WebFetch** - Extração com seletores CSS específicos  
3. **Fallback com curl** - API pública do ML como backup
4. **Parsing JSON** - Estruturação dos dados

## 🔍 Seletores HTML - Estrutura Completa

### Preço Completo (Estrutura Real do HTML)
```html
<!-- EXEMPLO: R$ 969,03 -->
<span class="andes-money-amount__currency" data-andes-money-amount-currency="true">
  <span class="andes-money-amount__currency-symbol">R$</span>
</span>
<span class="andes-money-amount__fraction" data-andes-money-amount-fraction="true">969</span>
<span class="andes-visually-hidden">,</span>
<span class="andes-money-amount__cents andes-money-amount__cents--superscript-20" 
      style="font-size: 10px;" data-andes-money-amount-cents="true">03</span>
```

**Parsing em JavaScript:**
```javascript
const moeda = document.querySelector('[data-andes-money-amount-currency-symbol]')?.textContent; // "R$"
const inteiro = document.querySelector('[data-andes-money-amount-fraction="true"]')?.textContent; // "969"
const centavos = document.querySelector('[data-andes-money-amount-cents="true"]')?.textContent; // "03"
const preco = `${moeda} ${inteiro},${centavos}`; // "R$ 969,03"
```

### Outros Elementos
```html
<!-- Título -->
<h1 class="ui-pdp-title">Tela Display Samsung A15 4G...</h1>

<!-- Vendedor -->
<span class="ui-seller-title__label">Loja Oficial</span>

<!-- Avaliação -->
<span class="andes-rating">4.8</span>
```

## 📝 Próximas Melhorias

- [ ] Comparar preços com Shopee
- [ ] Filtrar por frete grátis
- [ ] Alertas de preço
- [ ] Cache de resultados
