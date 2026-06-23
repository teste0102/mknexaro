#!/usr/bin/env python3
"""
Busca Shopee com múltiplas estratégias
1. Tenta API interna
2. Fallback: Web scraping com headers
3. Fallback: Retorna instruções de busca manual
"""
import sys
import json
import requests
from urllib.parse import quote

def estrategia_1_api():
    """Tentar API interna da Shopee"""
    try:
        termo = sys.argv[1] if len(sys.argv) > 1 else "tela A15 4g"

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Referer': 'https://shopee.com.br/',
        }

        # Tentar endpoint v4
        url = f"https://shopee.com.br/api/v4/search/search_items?keyword={quote(termo)}&limit=20"
        resp = requests.get(url, headers=headers, timeout=5)

        if resp.status_code == 200:
            data = resp.json()
            if 'items' in data:
                produtos = []
                for i, item in enumerate(data['items'][:5], 1):
                    produtos.append({
                        "id": i,
                        "titulo": item.get('name', 'N/A'),
                        "preco": f"R$ {item.get('price', 0) / 100000:.2f}",
                        "avaliacao": f"{item.get('rating_average', 0):.1f}⭐"
                    })
                return {"status": "sucesso", "fonte": "API", "produtos": produtos}
    except Exception as e:
        pass

    return None

def estrategia_2_selenium():
    """Fallback: Tentar novamente com Selenium"""
    try:
        import undetected_chromedriver as uc
        from bs4 import BeautifulSoup
        import time

        termo = sys.argv[1] if len(sys.argv) > 1 else "tela A15 4g"

        options = uc.ChromeOptions()
        options.binary_location = '/usr/bin/chromium'
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = uc.Chrome(options=options, version_main=149, headless=True)
        driver.get(f"https://shopee.com.br/search?keyword={termo.replace(' ', '+')}")

        time.sleep(8)

        # Extrair com JS
        driver.execute_script("""
            window.produtos = [];
            document.querySelectorAll('a[href*="/p/"]').forEach(link => {
                window.produtos.push({
                    titulo: link.textContent.slice(0, 100),
                    href: link.href
                });
            });
        """)

        produtos = driver.execute_script("return window.produtos")
        driver.quit()

        if produtos and len(produtos) > 0:
            return {
                "status": "sucesso",
                "fonte": "Selenium",
                "produtos": [
                    {
                        "id": i,
                        "titulo": p['titulo'],
                        "url": p['href'],
                        "preco": "Verificar no link",
                        "avaliacao": "Verificar no link"
                    }
                    for i, p in enumerate(produtos[:5], 1)
                ]
            }
    except Exception as e:
        pass

    return None

def estrategia_3_manual():
    """Fallback: Instruções para busca manual"""
    termo = sys.argv[1] if len(sys.argv) > 1 else "tela A15 4g"
    return {
        "status": "info",
        "mensagem": "Shopee está bloqueando requisições automáticas",
        "solucao": "Acesse manualmente",
        "url": f"https://shopee.com.br/search?keyword={termo.replace(' ', '+')}",
        "instrucoes": [
            "1. Clique no link acima",
            "2. Ordene por 'Menor Preço'",
            "3. Compare avaliações dos vendedores",
            "4. Verifique frete grátis"
        ]
    }

if __name__ == "__main__":
    # Tentar estratégias em ordem
    resultado = estrategia_1_api()

    if not resultado:
        resultado = estrategia_2_selenium()

    if not resultado:
        resultado = estrategia_3_manual()

    print(json.dumps(resultado, ensure_ascii=False, indent=2))
