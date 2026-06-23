#!/usr/bin/env python3
"""
Scraper Mercado Livre CORRIGIDO 2026
- Delay 1-5s entre requisições
- User-Agent dinâmico
- Seletores CSS atualizados
- Retorna JSON com preços REAIS
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random
import sys
from datetime import datetime

class ScraperML:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36"
        ]
        self.produtos = []
    
    def get_headers(self):
        """User-Agent dinâmico"""
        return {
            "User-Agent": random.choice(self.user_agents),
            "Accept-Language": "pt-BR,pt;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive"
        }
    
    def buscar(self, termo, paginas=1):
        """Busca no ML com delay entre requisições"""
        
        print(f"🔍 Buscando '{termo}' no Mercado Livre...", file=sys.stderr)
        
        for pagina in range(paginas):
            try:
                # URL de busca
                url = f"https://lista.mercadolivre.com.br/{termo.replace(' ', '-')}"
                if pagina > 0:
                    url += f"_Desde_{pagina * 50 + 1}"
                
                print(f"  📄 Página {pagina + 1}... delay {1}-{5}s", file=sys.stderr)
                
                # Delay 1-5s
                delay = random.uniform(1, 5)
                time.sleep(delay)
                
                # Request com headers dinâmicos
                response = requests.get(
                    url,
                    headers=self.get_headers(),
                    timeout=10
                )
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Seletores ATUALIZADOS (2026)
                seletores = [
                    # Novo seletor (2024+)
                    ('div[data-component="item"]', 'h2', 'span.price-tag-fraction'),
                    # Seletor alternativo
                    ('li.ui-search-layout__item', 'h2.ui-search-item__title', 'span.andes-money-amount__fraction'),
                    # Genérico
                    ('article', 'h2', 'span')
                ]
                
                encontrados = False
                
                for item_sel, titulo_sel, preco_sel in seletores:
                    items = soup.select(item_sel)
                    
                    if items:
                        print(f"    ✅ {len(items)} produtos encontrados", file=sys.stderr)
                        encontrados = True
                        
                        for item in items[:5]:
                            try:
                                # Extrai título
                                titulo_elem = item.select_one(titulo_sel)
                                titulo = titulo_elem.text.strip() if titulo_elem else "N/A"
                                
                                # Extrai preço
                                preco_elem = item.select_one(preco_sel)
                                preco = preco_elem.text.strip() if preco_elem else "N/A"
                                
                                # Extrai URL
                                link_elem = item.find('a', href=True)
                                url_prod = link_elem['href'] if link_elem else "N/A"
                                
                                self.produtos.append({
                                    "titulo": titulo,
                                    "preco": f"R$ {preco}" if preco != "N/A" else preco,
                                    "url": url_prod,
                                    "marketplace": "MERCADO LIVRE"
                                })
                            except Exception as e:
                                print(f"    ⚠️  Erro ao extrair produto: {e}", file=sys.stderr)
                                continue
                        
                        break
                
                if not encontrados:
                    print(f"    ⚠️  Nenhum produto encontrado nesta página", file=sys.stderr)
            
            except Exception as e:
                print(f"  ❌ Erro na página {pagina + 1}: {e}", file=sys.stderr)
                continue
        
        return self.produtos[:5]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Uso: python3 scraper_ml_completo.py 'termo'"}))
        sys.exit(1)
    
    termo = sys.argv[1]
    
    scraper = ScraperML()
    produtos = scraper.buscar(termo, paginas=1)
    
    resultado = {
        "status": "success" if produtos else "no_results",
        "termo": termo,
        "marketplace": "MERCADO LIVRE",
        "total": len(produtos),
        "produtos": produtos,
        "timestamp": datetime.now().isoformat()
    }
    
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
