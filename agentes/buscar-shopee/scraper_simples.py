#!/usr/bin/env python3
"""
Scraper simplificado da Shopee usando API interna (sem Selenium)
"""
import requests
import json
import sys

def buscar_shopee(termo, max_resultados=5):
    """
    Busca produtos na Shopee via API interna
    Retorna: lista de dicts com {titulo, preco, vendedor, url}
    """
    
    # API interna do Shopee retorna JSON com preços reais
    url = "https://shopee.com.br/api/v2/search_items"
    
    params = {
        "by": "relevancy",
        "keyword": termo,
        "limit": max_resultados,
        "newest": 0,
        "order": "asc",
        "page_type": "search"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    }
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        
        data = resp.json()
        
        resultados = []
        for item in data.get('items', [])[:max_resultados]:
            preco = item.get('price_min') / 100000  # Shopee usa centavos
            
            resultado = {
                'titulo': item.get('name'),
                'preco': f"R$ {preco:.2f}",
                'preco_original': f"R$ {item.get('price_max') / 100000:.2f}" if item.get('price_max') else None,
                'vendedor': item.get('shop', {}).get('name'),
                'rating': item.get('rating_star'),
                'url': f"https://shopee.com.br/{item.get('name').replace(' ', '-').lower()}-i.{item.get('itemid')}.{item.get('shopid')}"
            }
            resultados.append(resultado)
        
        return resultados
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Uso: python3 scraper_simples.py 'termo'"}))
        sys.exit(1)
    
    termo = sys.argv[1]
    resultados = buscar_shopee(termo)
    print(json.dumps(resultados, ensure_ascii=False, indent=2))
