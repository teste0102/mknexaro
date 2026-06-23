# 📖 Guia: Coleta Manual de Dados da Shopee

## Como Funciona

1. ✅ Você acessa a Shopee normalmente no navegador
2. 📋 Copia os dados dos produtos (usando console do navegador)
3. 💾 Salva em um arquivo Excel
4. ⚙️ Usa o `comparador.py` para consolidar e comparar

---

## Passo a Passo

### 1️⃣ Abra a Shopee e Pesquise

```
https://shopee.com.br/search?keyword=tela+A15+4g
```

### 2️⃣ Abra o DevTools (F12)

![DevTools](https://img.shields.io/badge/F12-DevTools-blue)

- Clique em **F12** ou **Ctrl+Shift+I** (ou Cmd+Option+I no Mac)
- Vá para a aba **Console**

### 3️⃣ Cole Este Script no Console

```javascript
// Script para coletar produtos da Shopee
const produtos = [];

// Obter todos os links de produtos visíveis
document.querySelectorAll('a[href*="/p/"]').forEach((link, idx) => {
    const href = link.href;
    const container = link.closest('div');
    
    let titulo = link.getAttribute('title') || link.innerText;
    titulo = titulo.trim();
    
    // Pular se muito curto ou se é publicidade
    if (titulo.length < 5 || titulo.includes('Publicidade')) return;
    
    let preco = 'N/A';
    let avaliacao = 'N/A';
    let vendas = 'N/A';
    let desconto = '';
    
    // Procurar preço
    if (container) {
        const preco_elem = container.querySelector('[class*="price"]') ||
                          container.querySelector('[class*="Cost"]');
        if (preco_elem) {
            preco = preco_elem.innerText.trim();
        }
        
        const avaliacao_elem = container.querySelector('[class*="rating"]');
        if (avaliacao_elem) {
            avaliacao = avaliacao_elem.innerText.trim();
        }
        
        const vendas_elem = container.querySelector('[class*="sold"]');
        if (vendas_elem) {
            vendas = vendas_elem.innerText.trim();
        }
        
        const desconto_elem = container.querySelector('[class*="percent"]') ||
                             container.querySelector('[class*="discount"]');
        if (desconto_elem) {
            desconto = desconto_elem.innerText.trim();
        }
    }
    
    produtos.push({
        titulo: titulo,
        preco: preco,
        desconto: desconto,
        avaliacao: avaliacao,
        vendas: vendas,
        url: href,
        fonte: 'Shopee',
        imagem: link.querySelector('img')?.src || ''
    });
});

// Mostrar resultado
console.log('Produtos coletados:', produtos.length);
console.table(produtos);

// Copiar para clipboard (JSON)
copy(JSON.stringify(produtos, null, 2));
console.log('✅ Dados copiados para clipboard! Cole em um arquivo .json');
```

### 4️⃣ Executar e Copiar

- Cole o script acima no Console
- Pressione **Enter**
- Você verá uma tabela com os produtos
- Os dados já foram copiados para **Clipboard** (Ctrl+V)

### 5️⃣ Salvar em Excel

**Opção A: Usar o script Python**
```bash
python3 criar_excel_coleta.py "tela A15 4g"
```

**Opção B: Manual no Excel**
- Crie um Excel com as colunas: Título, Preço, Desconto, Avaliação, Vendas, URL, Fonte, Pasta, Imagem
- Cole os dados que copiou
- Salve em `~/Downloads/dados_shopee.xlsx`

---

## Usar o Comparador

Após coletar dados em múltiplas fontes (Shopee, Mercado Livre, etc):

```bash
python3 comparar_precos.py "tela A15 4g"
```

Isso vai:
✅ Ler todos os Excels das pastas  
✅ Filtrar pelo termo procurado  
✅ Comparar preços  
✅ Gerar um Excel consolidado com cores  
✅ Destacar o melhor preço em verde  

---

## Estrutura de Pastas Esperada

```
~/dados_produtos/
├── shopee/
│   ├── tela_A15_20260621_123456.xlsx
│   └── ...
├── mercado_livre/
│   ├── tela_A15_20260621_123456.xlsx
│   └── ...
└── saida_comparacao/
    └── (aqui são gerados os resultados)
```

---

## Dicas

💡 **Scroll para carregar mais**: Role a página para baixo para carregar mais produtos antes de coletar

💡 **Múltiplas buscas**: Faça a coleta várias vezes com diferentes termos

💡 **Nomes consistentes**: Use títulos sem caracteres especiais nos nomes de arquivo

💡 **URLs com hiperlinks**: O comparador converte automaticamente em hyperlinks clicáveis

---

## Suporte

Se tiver dúvidas, rode:
```bash
python3 comparador.py --help
```
