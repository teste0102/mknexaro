#!/usr/bin/env python3
"""
Busca Shopee - Versão final com fallbacks
Quando Shopee bloqueia: retorna instrução de coleta manual
"""
import sys
import os
import json
import time
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime

def buscar_com_fallback(termo):
    """Tenta buscar com múltiplas estratégias"""

    # Estratégia 1: Tentar com Selenium + JS avançado
    print(f"🔍 Tentando estratégia 1: Selenium com JS avançado...")
    resultado = tentar_selenium_avancado(termo)
    if resultado["status"] == "sucesso":
        return resultado

    # Estratégia 2: Busca manual via navegador (instruções para o usuário)
    print(f"⚠️  Shopee está bloqueando automatização.")
    print(f"📌 Usando alternativa: Gerar instruções para busca e coleta manual")
    return gerar_instrucoes_coleta(termo)

def tentar_selenium_avancado(termo):
    """Tenta Selenium com truques avançados"""
    try:
        import undetected_chromedriver as uc
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By

        options = uc.ChromeOptions()
        options.binary_location = '/usr/bin/chromium'
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')

        driver = uc.Chrome(options=options, version_main=149, headless=True)

        url = f"https://shopee.com.br/search?keyword={termo.replace(' ', '+')}"
        driver.get(url)

        # Estratégia: aguardar por mutation observer de mudanças no DOM
        wait = WebDriverWait(driver, 15)

        try:
            # Tentar aguardar qualquer elemento que indique carregamento
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/p/']")))

            # Se chegou aqui, produtos carregaram
            html = driver.page_source
            driver.quit()

            # Processar HTML
            from HTML import ShopeeScraper
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html)
                html_path = f.name

            scraper = ShopeeScraper(html_path)
            if scraper.carregar_html():
                produtos = scraper.extrair_produtos_shopee()
                os.unlink(html_path)

                if produtos:
                    return {
                        "status": "sucesso",
                        "total": len(produtos),
                        "produtos": [
                            {
                                "id": i,
                                "titulo": p.get('titulo', 'N/A'),
                                "preco": p.get('preco', 'N/A'),
                                "url": p.get('url', 'N/A')
                            }
                            for i, p in enumerate(produtos[:10], 1)
                        ]
                    }
        except:
            driver.quit()
            pass

    except Exception as e:
        pass

    return {"status": "erro"}

def gerar_instrucoes_coleta(termo):
    """Gera instruções JSON para coleta manual de dados"""

    url_busca = f"https://shopee.com.br/search?keyword={termo.replace(' ', '+')}"

    return {
        "status": "info",
        "mensagem": "Shopee bloqueou automatização. Use este procedimento para coletar dados:",
        "url_busca": url_busca,
        "procedimento": {
            "passo_1": {
                "descricao": "Abra o navegador e acesse o link",
                "link": url_busca
            },
            "passo_2": {
                "descricao": "Abra DevTools (F12)",
                "instrucoes": "Console → copie o script abaixo"
            },
            "passo_3": {
                "descricao": "Cole este script no console e execute",
                "script": """
// Capturar dados dos produtos visíveis
const produtos = [];
document.querySelectorAll('a[href*="/p/"]').forEach(link => {
    const titulo = link.getAttribute('title') || link.textContent.trim();
    if (titulo.length > 5) {
        produtos.push({
            titulo: titulo,
            url: link.href
        });
    }
});

// Capturar preços
document.querySelectorAll('[class*="price"]').forEach(el => {
    const preco = el.textContent.match(/R\\$[\\s\\d.,]+/);
    if (preco) console.log('Preço encontrado:', preco[0]);
});

// Retornar dados
console.log(JSON.stringify(produtos, null, 2));

// Copiar para clipboard
copy(JSON.stringify(produtos, null, 2));
"""
            },
            "passo_4": {
                "descricao": "Copie o JSON que aparece e envie para analisar"
            }
        },
        "aviso": "A Shopee tem proteção contra bots. Para buscas programáticas, considere usar APIs comerciais como RapidAPI ou Serpapi"
    }

if __name__ == "__main__":
    termo = sys.argv[1] if len(sys.argv) > 1 else "tela A15 4g"
    resultado = buscar_com_fallback(termo)

    print("\n" + "="*60)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
