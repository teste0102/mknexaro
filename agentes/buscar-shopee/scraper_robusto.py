#!/usr/bin/env python3
import sys
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

def buscar_shopee(termo, max_products=5):
    """Busca produtos na Shopee com múltiplos seletores"""

    try:
        # Configurar Chrome
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        options.binary_location = '/usr/bin/chromium'

        driver = uc.Chrome(
            options=options,
            version_main=149,
            headless=True
        )

        url = f"https://shopee.com.br/search?keyword={termo.replace(' ', '+')}"
        driver.get(url)

        # Aguardar mais tempo
        time.sleep(5)

        # Tentar scroll para carregar mais itens
        driver.execute_script("window.scrollBy(0, 1000)")
        time.sleep(2)

        # Extrair com BeautifulSoup para melhor parsing
        from bs4 import BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        produtos = []

        # Tentar múltiplos seletores comuns na Shopee
        items = soup.find_all('div', {'data-sqe': 'item'})

        if not items:
            # Alternativa: procurar por classes genéricas
            items = soup.find_all('div', class_=['shopee-product-card', 'product-item', 'shopee-search-item-result'])

        if not items:
            # Last resort: procurar por links de produtos
            items = soup.find_all('a', href=lambda x: x and '/p/' in str(x))[:max_products]

        for idx, item in enumerate(items[:max_products], 1):
            try:
                # Tentar extrair título
                titulo = None
                for selector in ['span[data-sqe="name"]', 'span.shopee-product-card__name', '.product-name']:
                    elem = item.find(string=lambda x: x and len(str(x).strip()) > 10)
                    if elem:
                        titulo = str(elem).strip()[:100]
                        break

                if not titulo:
                    titulo_elem = item.find('span') or item.find('div')
                    titulo = titulo_elem.get_text(strip=True) if titulo_elem else "Produto"

                # Extrair preço
                preco = "N/A"
                price_elem = item.find('span', class_=['shopee-price-display__main-price', 'product-price'])
                if price_elem:
                    preco = price_elem.get_text(strip=True)
                else:
                    # Procurar por "R$"
                    text = item.get_text()
                    import re
                    match = re.search(r'R\$\s*[\d.,]+', text)
                    if match:
                        preco = match.group()

                # Avaliação
                rating = "N/A"
                rating_elem = item.find('span', class_=['shopee-rating'])
                if rating_elem:
                    rating = rating_elem.get_text(strip=True)

                if titulo and preco != "N/A":
                    produtos.append({
                        "id": idx,
                        "titulo": titulo,
                        "preco": preco,
                        "avaliacao": rating
                    })
            except Exception as e:
                continue

        driver.quit()

        if produtos:
            return {"status": "sucesso", "total": len(produtos), "produtos": produtos}
        else:
            return {"status": "aviso", "mensagem": f"Nenhum produto encontrado. HTML obtido: {len(html)} bytes"}

    except Exception as e:
        import traceback
        return {
            "status": "erro",
            "mensagem": str(e),
            "traceback": traceback.format_exc()
        }

if __name__ == "__main__":
    termo = sys.argv[1] if len(sys.argv) > 1 else "tela A15 4g"
    resultado = buscar_shopee(termo)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
