#!/usr/bin/env python3
"""
Script integrado: Scraper Shopee → Extrai preços → Retorna JSON
Fluxo completo: scraper.py (baixa) + h.py (extrai) = preços reais
"""

import sys
import json
import os
from pathlib import Path

# Adiciona path para imports
sys.path.insert(0, str(Path(__file__).parent))

def buscar_e_extrair(termo):
    """Pipeline completo de busca e extração"""
    
    try:
        print(f"📥 [1/3] Baixando HTML da Shopee para '{termo}'...", file=sys.stderr)
        
        # PASSO 1: Baixar HTML com scraper.py
        from scraper import run_scraper
        
        pasta_destino, driver, caminhos_html = run_scraper('product', termo, max_pages=1)
        
        if not caminhos_html:
            return {"error": "Nenhum HTML baixado", "status": "failed"}
        
        caminho_html = caminhos_html[0] if isinstance(caminhos_html, list) else caminhos_html
        
        if not os.path.exists(caminho_html):
            return {"error": f"Arquivo HTML não existe: {caminho_html}", "status": "failed"}
        
        print(f"✅ HTML baixado: {caminho_html}", file=sys.stderr)
        
        # PASSO 2: Extrair com h.py (ShopeeScraper)
        print(f"🔍 [2/3] Extraindo produtos...", file=sys.stderr)
        
        from h import ShopeeScraper
        
        scraper = ShopeeScraper(caminho_html)
        
        if not scraper.carregar_html():
            return {"error": "Falha ao carregar HTML", "status": "failed"}
        
        scraper.extrair_produtos_shopee()
        
        if not scraper.produtos:
            return {"error": "Nenhum produto encontrado no HTML", "status": "no_results"}
        
        print(f"✅ {len(scraper.produtos)} produtos encontrados", file=sys.stderr)
        
        # PASSO 3: Formatar para JSON
        print(f"📊 [3/3] Formatando resultados...", file=sys.stderr)
        
        resultados = []
        for i, prod in enumerate(scraper.produtos[:5], 1):
            resultado = {
                "id": i,
                "titulo": prod.get('titulo', 'N/A'),
                "preco": prod.get('preco', 'N/A'),
                "avaliacao": prod.get('avaliacao', 'N/A'),
                "url": prod.get('url', 'N/A')
            }
            resultados.append(resultado)
        
        # Fecha driver se existir
        if driver:
            driver.quit()
        
        return {
            "status": "success",
            "termo": termo,
            "total": len(resultados),
            "produtos": resultados
        }
    
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "error": str(e),
            "details": traceback.format_exc()
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Uso: python3 busca_shopee_completa.py 'termo'"}))
        sys.exit(1)
    
    termo = sys.argv[1]
    resultado = buscar_e_extrair(termo)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
