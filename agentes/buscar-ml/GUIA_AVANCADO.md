# Guia Avançado - Buscar ML

## 🚀 Extractores de Preço Melhorados

Agora temos 3 formas de extrair preços do Mercado Livre:

### 1️⃣ WebSearch + Parsing Manual (Atual)
- **Vantagem**: Rápido, sem bloqueios
- **Desvantagem**: Preços podem não estar visíveis no resultado
- **Uso**: `/buscar-ml <termo>`

### 2️⃣ API Pública do Mercado Livre
```bash
# Use o scraper.sh
bash scraper.sh "tela A15 4g"

# Retorna JSON com: title, price, permalink
```

**Vantagem**: Acesso direto aos dados estruturados  
**Desvantagem**: Limitado a informações básicas

### 3️⃣ Parser JavaScript (parser.js)
Para quando você conseguir acessar o HTML da página:

```javascript
const MercadoLivreParser = require('./parser.js');

// Extrair preço de um elemento
const preco = MercadoLivreParser.extrairPreco(document);
// { moeda: "R$", inteiro: "969", centavos: "03", preco: "R$ 969,03" }

// Extrair todos os produtos
const produtos = MercadoLivreParser.extrairTodosProdutos();

// Ordenar por preço
const ordenados = MercadoLivreParser.ordenarPorPreco(produtos, 'asc');
```

## 📋 Estrutura HTML Referência

### Preço (R$ 969,03)
```html
<span class="andes-money-amount__currency" data-andes-money-amount-currency="true">
  <span class="andes-money-amount__currency-symbol">R$</span>
</span>
<span class="andes-money-amount__fraction" data-andes-money-amount-fraction="true">969</span>
<span class="andes-money-amount__cents" data-andes-money-amount-cents="true">03</span>
```

**Atributos importantes**:
- `data-andes-money-amount-currency="true"` ← Moeda
- `data-andes-money-amount-fraction="true"` ← Parte inteira
- `data-andes-money-amount-cents="true"` ← Centavos

### Outros Elementos
```html
<h1 class="ui-pdp-title">Título do Produto</h1>
<span class="ui-seller-title__label">Loja ABC</span>
<span data-andes-rating="true">4.8</span>
<span data-item-id="MLB1234567">Item ID</span>
```

## 🔧 Como Usar com Puppeteer/Selenium

### Node.js + Puppeteer
```javascript
const puppeteer = require('puppeteer');
const MercadoLivreParser = require('./parser.js');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  await page.goto('https://lista.mercadolivre.com.br/tela-a15-4g');
  
  // Injetar parser
  const produtos = await page.evaluate(() => {
    // Aqui o parser roda no contexto do navegador
    return document.querySelectorAll('.item').map(item => ({
      titulo: item.querySelector('h2')?.textContent,
      preco: item.querySelector('[data-andes-money-amount-fraction]')?.textContent,
      link: item.querySelector('a')?.href
    }));
  });
  
  console.table(produtos);
  await browser.close();
})();
```

## 🎯 Por que o WebFetch é bloqueado?

O Mercado Livre retorna **HTTP 403 Forbidden** porque:
1. Detecta bots/scrapers automáticos
2. Proteção contra abuso de recursos
3. Políticas de ToS (Terms of Service)

**Soluções**:
- ✅ Usar API pública (sem bloqueios)
- ✅ Usar User-Agent realista com Puppeteer/Selenium
- ✅ Adicionar delays entre requisições
- ❌ Não fazer scraping massivo/spam

## 📊 Próximas Implementações

- [ ] Integrar com Puppeteer para bypass do 403
- [ ] Cache de preços com versionamento
- [ ] Alertas de queda de preço
- [ ] Comparação com Shopee/Amazon
- [ ] Exportar para CSV/JSON
