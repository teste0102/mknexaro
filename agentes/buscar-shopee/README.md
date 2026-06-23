# 🛍️ Buscar Shopee - Sistema de Comparação de Preços

Coleta dados da Shopee **manualmente** (via navegador) e compara preços com outras fontes usando Excel.

## ⚡ Quick Start

### 1. Criar Template para Coleta
```bash
python3 run.py template "tela A15 4g"
```

Isso cria um arquivo Excel em: `~/dados_produtos/shopee/`

### 2. Coletar Dados Manualmente
1. Abra https://shopee.com.br/search?keyword=tela+A15+4g
2. Pressione **F12** (DevTools)
3. Vá para **Console**
4. Cole o script em `GUIA_COLETA.md`
5. Copie os dados gerados
6. Cole no Excel criado

### 3. Comparar Preços
```bash
python3 run.py comparar "tela A15 4g"
```

Gera um Excel consolidado com todos os preços comparados e cores!

---

## 📋 Modo Interativo

```bash
python3 run.py
```

Menu com:
- ✅ Criar template
- ✅ Comparar preços
- ✅ Ver guia detalhado
- ✅ Abrir pasta de dados

---

## 📁 Estrutura de Pastas

```
~/dados_produtos/
├── shopee/
│   ├── 20260621_110000_tela_A15_4g.xlsx
│   └── ...
├── mercado_livre/
│   └── 20260621_110000_tela_A15_4g.xlsx
└── saida_comparacao/
    └── 20260621_110000_tela_A15_4g.xlsx  (resultado final)
```

---

## 🔧 Arquivos da Skill

| Arquivo | Função |
|---------|--------|
| `run.py` | Menu principal interativo |
| `criar_excel_coleta.py` | Cria template Excel vazio |
| `comparador.py` | Processa e compara múltiplos Excels |
| `HTML.py` | Parser para HTML (futuro) |
| `GUIA_COLETA.md` | Guia passo a passo de coleta |

---

## 💡 Dicas Importantes

✅ **Coletar de várias fontes**
- Shopee
- Mercado Livre
- Olist
- Qualquer marketplace

✅ **Organizar em pastas diferentes**
- Cada fonte em uma pasta: `shopee/`, `mercado_livre/`, etc.
- Comparador processa automaticamente

✅ **Nomes de arquivo**
- Use: `YYYYMMDD_HHMMSS_produto.xlsx`
- Evite caracteres especiais

✅ **Rollagem da página**
- Role para baixo antes de coletar
- Alguns produtos só carregam com scroll

---

## 🎯 Fluxo Completo

```
1. COLETA MANUAL
   Abrir Shopee → DevTools → Script → Copiar dados

2. SALVAR EM EXCEL
   Cole em template → Salve na pasta correta

3. COMPARADOR
   Lê todos os Excels → Filtra termo → Compara preços

4. RESULTADO
   Excel com cores, links clicáveis, ordenado por preço
```

---

## ❌ Por Que Não Automático?

A Shopee tem proteção robusta contra bots:
- Detecta Selenium
- Bloqueia requisições HTTP
- Redireciona para verificação

**Solução**: Coleta manual via navegador normal funciona 100%

---

## 📊 Exemplo de Resultado

O comparador gera um Excel com:
- ✅ Preço em **verde**
- ✅ Produtos coloridos por fonte
- ✅ URLs clicáveis
- ✅ Ordenado do mais barato

---

## 🔗 Comandos Úteis

```bash
# Ver guia detalhado
python3 run.py  # Menu → Opção 3

# Criar template diretamente
python3 criar_excel_coleta.py "tela A15 4g"

# Ver pasta de dados
xdg-open ~/dados_produtos

# Usar comparador diretamente (precisa de GUI)
python3 comparador.py
```

---

## 📝 License

Baseado em projeto original que funcionava com sucesso.
Adaptado para contornar proteção da Shopee.
