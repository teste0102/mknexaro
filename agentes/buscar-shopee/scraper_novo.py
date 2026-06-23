#!/usr/bin/env python3
import sys
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def buscar_shopee(termo, max_products=5):
    """Busca produtos na Shopee e retorna JSON com preços"""

    try:
        # Inicializar Chrome com chromium local, ignorando versioncheck
        options = uc.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless=new')
        options.binary_location = '/usr/bin/chromium'

        driver = uc.Chrome(
            options=options,
            version_main=149,  # Forçar versão
            headless=True
        )

        url = f"https://shopee.com.br/search?keyword={termo.replace(' ', '+')}"
        driver.get(url)

        # Aguardar carregamento dos produtos
        time.sleep(3)

        # Coletar produtos
        produtos = []
        items = driver.find_elements(By.CSS_SELECTOR, 'div[data-sqe="item"]')[:max_products]

        for idx, item in enumerate(items, 1):
            try:
                titulo = item.find_element(By.CSS_SELECTOR, 'div[data-sqe="name"]').text
                preco_elem = item.find_element(By.CSS_SELECTOR, 'span.shopee-price-display__main-price')
                preco = preco_elem.text

                # Tentar pegar avaliação
                try:
                    rating = item.find_element(By.CSS_SELECTOR, 'span[data-sqe="rating"]').text
                except:
                    rating = "N/A"

                produtos.append({
                    "id": idx,
                    "titulo": titulo,
                    "preco": preco,
                    "avaliacao": rating
                })
            except Exception as e:
                continue

        driver.quit()
        return {"status": "sucesso", "produtos": produtos}

    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

if __name__ == "__main__":
    termo = sys.argv[1] if len(sys.argv) > 1 else "tela A15 4g"
    resultado = buscar_shopee(termo)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
