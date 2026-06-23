// Parser de preços do Mercado Livre
// Extrai dados usando os seletores HTML reais

class MercadoLivreParser {
  /**
   * Extrai o preço completo de um elemento
   * @param {HTMLElement} containerEl - Elemento contendo a estrutura de preço
   * @returns {Object} { moeda: "R$", inteiro: "969", centavos: "03", preco: "R$ 969,03" }
   */
  static extrairPreco(containerEl) {
    const moedaEl = containerEl.querySelector('[data-andes-money-amount-currency-symbol]');
    const inteiroEl = containerEl.querySelector('[data-andes-money-amount-fraction="true"]');
    const centavosEl = containerEl.querySelector('[data-andes-money-amount-cents="true"]');

    const moeda = moedaEl?.textContent?.trim() || "R$";
    const inteiro = inteiroEl?.textContent?.trim() || "0";
    const centavos = centavosEl?.textContent?.trim() || "00";

    return {
      moeda,
      inteiro,
      centavos,
      preco: `${moeda} ${inteiro},${centavos}`,
      numeroGrande: parseFloat(`${inteiro}.${centavos}`)
    };
  }

  /**
   * Extrai todos os dados de um produto
   */
  static extrairProduto(elementoProduto) {
    const titulo = elementoProduto.querySelector('h1, h2, .ui-pdp-title')?.textContent?.trim();
    const preco = this.extrairPreco(elementoProduto);
    const avaliacao = elementoProduto.querySelector('[data-andes-rating], .andes-rating')?.textContent?.trim();
    const vendedor = elementoProduto.querySelector('[data-seller-title], .ui-seller-title__label')?.textContent?.trim();
    const link = elementoProduto.querySelector('a[href*="mercadolivre"]')?.href;

    return {
      titulo,
      preco: preco.preco,
      precoNumerico: preco.numeroGrande,
      avaliacao,
      vendedor,
      link
    };
  }

  /**
   * Extrai todos os produtos de uma página
   */
  static extrairTodosProdutos(container = document) {
    const produtos = [];
    const elementos = container.querySelectorAll('[data-andes-money-amount-fraction]');

    elementos.forEach((el) => {
      const produtoEl = el.closest('[data-item-id], article, .item, .product');
      if (produtoEl) {
        const produto = this.extrairProduto(produtoEl);
        if (produto.titulo) {
          produtos.push(produto);
        }
      }
    });

    return produtos;
  }

  /**
   * Ordena produtos por preço
   */
  static ordenarPorPreco(produtos, ordem = 'asc') {
    return [...produtos].sort((a, b) => {
      const fatorOrdenacao = ordem === 'asc' ? 1 : -1;
      return (a.precoNumerico - b.precoNumerico) * fatorOrdenacao;
    });
  }
}

// Exportar para Node.js ou navegador
if (typeof module !== 'undefined' && module.exports) {
  module.exports = MercadoLivreParser;
}
