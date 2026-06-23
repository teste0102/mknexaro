---
name: "buscar-shopee"
description: "Busca Shopee com preços REAIS: scraper.py (baixa) + h.py (extrai) + JSON (retorna)"
---

# Buscar Shopee - Pipeline Completo

Quando o usuário pedir para buscar na Shopee, execute:

```bash
cd ~/.claude/skills/buscar-shopee
python3 busca_shopee_completa.py "TERMO"
```

## Retorna JSON com:
- **id**: número do produto
- **titulo**: nome do produto  
- **preco**: preço REAL em R$
- **avaliacao**: rating do vendedor
- **url**: link direto

## Apresente em tabela:

| # | Produto | Preço | Avaliação |
|---|---------|-------|-----------|
| 1 | Tela A15 4G | R$ 120,50 | ⭐ 4.8 |
| 2 | Tela A15 | R$ 110,00 | ⭐ 4.5 |

**Máximo 5 produtos. Ordene por menor preço.**
