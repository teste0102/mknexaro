---
name: "buscador"
description: "Busca informações específicas sobre qualquer assunto na internet e retorna um resumo estruturado com fontes."
---

# Buscador - Pesquisa na Internet

Quando `/buscar <termo>` é invocado:

1. Extraia o `<termo>` passado como argumento
2. Use **WebSearch** para pesquisar o termo na internet
3. Filtre os 3 a 5 resultados mais relevantes
4. Retorne um resumo estruturado no formato abaixo:

```
## Resultados para: <termo>

### 1. <Título do resultado>
**Resumo:** <Descrição curta e objetiva do conteúdo>
**Fonte:** <URL>

### 2. <Título do resultado>
**Resumo:** <Descrição curta e objetiva do conteúdo>
**Fonte:** <URL>

...

---
Pesquisa realizada em: <data atual>
```

Regras:
- Sempre use WebSearch para buscar — nunca responda de memória.
- Filtre resultados irrelevantes, duplicados ou de baixa qualidade.
- Priorize fontes confiáveis (sites oficiais, publicações reconhecidas, documentação técnica).
- Limite a resposta a no máximo 5 resultados.
- Se nenhum resultado relevante for encontrado, informe claramente e sugira termos alternativos.
- Apresente os resultados em português, mesmo que as fontes sejam em outro idioma.
