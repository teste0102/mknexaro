#!/usr/bin/env python3
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

try:
    from scraper import run_scraper
    
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Uso: python3 run_shopee.py 'termo'"}))
        sys.exit(1)
    
    termo = sys.argv[1]
    pasta_destino, driver, caminhos_html = run_scraper('product', termo, max_pages=1)
    
    print(json.dumps({
        "status": "success",
        "termo": termo,
        "pasta": str(pasta_destino),
        "htmls": caminhos_html if isinstance(caminhos_html, list) else [caminhos_html]
    }))
    
    if driver:
        driver.quit()

except Exception as e:
    print(json.dumps({"error": str(e)}))
