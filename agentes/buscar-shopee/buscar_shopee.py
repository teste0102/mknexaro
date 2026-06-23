#!/usr/bin/env python3
"""
Busca Shopee - Integração com HTML.py ShopeeScraper
Baseado no projeto-shopee-main que funcionava
"""
import sys
import os
import json
import time
import tempfile
from pathlib import Path
from datetime import datetime

try:
    import undetected_chromedriver as uc
    from HTML import ShopeeScraper
    DEPENDENCIES_OK = True
except ImportError as e:
    print(f"Erro: {e}")
    DEPENDENCIES_OK = False

def baixar_html_shopee(termo, headless=True):
    """Baixa HTML da Shopee usando Selenium com undetected_chromedriver"""

    try:
        # Configurar Chrome
        options = uc.ChromeOptions()
        options.binary_location = '/usr/bin/chromium'
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')

        if headless:
            options.add_argument('--headless=new')

        print(f"🌐 Iniciando navegador para buscar: {termo}")
        driver = uc.Chrome(
            options=options,
            version_main=149,
            headless=headless
        )

        # Acessar Shopee
        url = f"https://shopee.com.br/search?keyword={termo.replace(' ', '+')}"
        print(f"📍 Acessando: {url}")
        driver.get(url)

        # Aguardar carregamento - tentar aguardar elementos específicos
        print("⏳ Aguardando carregamento de produtos...")
        time.sleep(8)

        # Múltiplos scrolls para carregar conteúdo dinamicamente
        print("📜 Fazendo scrolls para carregar produtos...")
        for i in range(5):
            driver.execute_script("window.scrollBy(0, 2000)")
            time.sleep(1)

        # Fazer scroll de volta ao topo
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(2)

        # Obter HTML
        html = driver.page_source
        driver.quit()

        print(f"✓ HTML obtido ({len(html)} bytes)")
        return html

    except Exception as e:
        print(f"❌ Erro ao baixar HTML: {e}")
        return None

def buscar_e_extrair(termo, max_produtos=10):
    """Busca na Shopee e extrai produtos usando ShopeeScraper"""

    if not DEPENDENCIES_OK:
        return {
            "status": "erro",
            "mensagem": "Dependências não instaladas (undetected_chromedriver ou HTML.py)"
        }

    try:
        # Baixar HTML
        html = baixar_html_shopee(termo)
        if not html:
            return {"status": "erro", "mensagem": "Não foi possível baixar HTML da Shopee"}

        # Salvar HTML temporário
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html)
            html_path = f.name

        print(f"📄 HTML salvo em: {html_path}")

        # Usar ShopeeScraper para extrair
        scraper = ShopeeScraper(html_path)

        if not scraper.carregar_html():
            return {"status": "erro", "mensagem": "Erro ao carregar HTML"}

        print("🔍 Analisando estrutura...")
        scraper.analisar_estrutura()

        print("📦 Extraindo produtos...")
        produtos = scraper.extrair_produtos_shopee()

        # Limpar arquivo temporário
        os.unlink(html_path)

        if not produtos:
            return {
                "status": "aviso",
                "mensagem": "Nenhum produto encontrado com os seletores conhecidos"
            }

        # Formatar resposta
        produtos_formatados = []
        for i, prod in enumerate(produtos[:max_produtos], 1):
            produtos_formatados.append({
                "id": i,
                "titulo": prod.get('titulo', 'N/A'),
                "preco": prod.get('preco', 'N/A'),
                "avaliacao": prod.get('avaliacao', 'N/A'),
                "url": prod.get('url', 'N/A')
            })

        return {
            "status": "sucesso",
            "total": len(produtos),
            "exibidos": len(produtos_formatados),
            "produtos": produtos_formatados
        }

    except Exception as e:
        import traceback
        return {
            "status": "erro",
            "mensagem": str(e),
            "traceback": traceback.format_exc()
        }

if __name__ == "__main__":
    termo = sys.argv[1] if len(sys.argv) > 1 else "tela A15 4g"
    resultado = buscar_e_extrair(termo)
    print("\n" + "="*60)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
