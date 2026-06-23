#!/usr/bin/env python3
import sys, json, time
from selenium import webdriver
from selenium.webdriver.common.by import By

def buscar_ml(termo):
    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        
        url = f"https://lista.mercadolivre.com.br/{termo.replace(' ', '-')}"
        print(f"🌐 Acessando...", file=sys.stderr)
        driver.get(url)
        time.sleep(3)
        
        produtos = []
        items = driver.find_elements(By.CSS_SELECTOR, "div[data-component='item']")
        
        for item in items[:5]:
            try:
                titulo = item.find_element(By.CSS_SELECTOR, "h2").text
                preco_int = item.find_element(By.CSS_SELECTOR, "span.andes-money-amount__fraction").text
                preco_cents = item.find_element(By.CSS_SELECTOR, "span.andes-money-amount__cents").text
                link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                
                produtos.append({"titulo": titulo, "preco": f"R$ {preco_int},{preco_cents}", "url": link})
            except:
                pass
        
        driver.quit()
        return {"status": "success" if produtos else "no", "total": len(produtos), "produtos": produtos}
    except Exception as e:
        if driver: driver.quit()
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    resultado = buscar_ml(sys.argv[1] if len(sys.argv) > 1 else "tela")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
