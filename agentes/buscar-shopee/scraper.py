# Definindo exceções personalizadas
class LoginRequired(Exception):
    """Exceção para quando o login é necessário."""
    pass

class CaptchaRequired(Exception):
    """Exceção para quando o captcha é necessário."""
    pass

import os
import re
import random
import time
from datetime import datetime
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from unidecode import unidecode
from bs4 import BeautifulSoup

# ---------- helpers ----------

def is_parar(parar_execucao):
    """Helper para checagem de parada flexível (bool ou função)."""
    if parar_execucao is None:
        return False
    if callable(parar_execucao):
        return parar_execucao()
    return bool(parar_execucao)

def pause(a=0.6, b=1.4, parar_execucao=None):
    """Pausa em intervalos pequenos, checando por parada."""
    total_sleep = random.uniform(a, b)
    elapsed = 0
    check_int = 0.2
    while elapsed < total_sleep:
        if is_parar(parar_execucao):
            raise Exception("[PARADO] Execução interrompida pelo usuário durante pausa!")
        time.sleep(min(check_int, total_sleep - elapsed))
        elapsed += check_int

def slugify(text):
    return re.sub(r"[^\w]", "", unidecode(text)).lower()

def url_com_page(base, idx):
    if "page=" in base:
        return re.sub(r"page=\d+", f"page={idx}", base)
    sep = "&" if "?" in base else "?"
    return f"{base}{sep}page={idx}"

def pagina_erro(html):
    soup = BeautifulSoup(html, "html.parser")
    if soup.select_one('div[class*="page-not-found"], div[class*="not-found-page"]'):
        return True
    if soup.select_one('img[src*="404"]'):
        return True
    h2 = soup.find('h2')
    return h2 and "faltando" in h2.get_text(strip=True).lower()

def pagina_captcha(html):
    soup = BeautifulSoup(html, "html.parser")
    if soup.find('div', {'class': re.compile(r'(captcha|g-recaptcha|cf-challenge)', re.I)}):
        return True
    if "Desculpe, precisamos ter certeza de que você não é um robô" in html:
        return True
    if soup.find('iframe', src=re.compile(r'captcha', re.I)):
        return True
    return False

# Espera por um elemento com checagem constante de parada
def wait_element(driver, by, value, timeout=15, interval=0.4, parar_execucao=None):
    end = time.time() + timeout
    last_exc = None
    while time.time() < end:
        if is_parar(parar_execucao):
            raise Exception("[PARADO] Execução interrompida pelo usuário durante espera de elemento!")
        try:
            elem = driver.find_element(by, value)
            return elem
        except Exception as exc:
            last_exc = exc
            time.sleep(interval)
    raise TimeoutException(f"Elemento não encontrado: {value}. Última exceção: {last_exc}")

# Espera por uma condição customizada, também checando por parada
def wait_condition(driver, condition, timeout=15, interval=0.4, parar_execucao=None):
    end = time.time() + timeout
    while time.time() < end:
        if is_parar(parar_execucao):
            raise Exception("[PARADO] Execução interrompida pelo usuário durante espera de condição!")
        try:
            if condition(driver):
                return True
        except Exception:
            pass
        time.sleep(interval)
    raise TimeoutException("Timeout esperando condição.")

# Função para contar o total de páginas (usando waits curtos)
def total_paginas(driver, parar_execucao=None):
    try:
        span = wait_element(driver, By.CSS_SELECTOR, 'span.shopee-mini-page-controller__total', timeout=7, parar_execucao=parar_execucao)
        return int(span.text.split('/')[-1])
    except TimeoutException:
        nums = driver.find_elements(By.CSS_SELECTOR, 'button.shopee-mini-page-controller__num , a.shopee-button-no-outline')
        if nums:
            return int(nums[-1].text)
        return 1

"""
IMPORTANTE:
- O argumento parar_execucao pode ser uma função (recomendado!) que retorna True para interromper,
  ou uma variável booleana.
- Checagem de parada é feita ANTES e DURANTE scraping, exceto enquanto estiver travado em driver.get().
"""

# Função principal de scraping
def run_scraper(search_type: str, termo: str, driver=None, max_pages=None, parar_execucao=None):
    """
    Baixa HTMLs da Shopee.
    Retorna o caminho da pasta destino, o driver ativo e o caminho do HTML baixado (string).
    Checa de forma constante se foi solicitado parar.
    """
    assert search_type in ("product", "store"), "search_type deve ser 'product' ou 'store'"

    html_paths = []

    # Se o driver não for passado, cria um novo driver
    if driver is None:
        opts = uc.ChromeOptions()
        opts.add_argument("--start-maximized")
        opts.add_argument(r'--user-data-dir=C:\ShopeeBotProfile')  # <- Mantém login/sessão!
        driver = uc.Chrome(options=opts, headless=False)

    # -- Primeira checagem de parada
    if is_parar(parar_execucao):
        print("[INFO] Execução interrompida pelo usuário antes de acessar Shopee!")
        return None, driver, []

    driver.get('https://shopee.com.br/')
    if pagina_captcha(driver.page_source):
        raise CaptchaRequired("Captcha detectado na página.")

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    slug_term = slugify(termo) if search_type == "store" else termo
    base_dir = os.path.join(os.path.expanduser("~/Desktop"), "prospecção", "busca")
    dest_dir = os.path.join(base_dir, f"Shopee_{slug_term}_html_{ts}")
    os.makedirs(dest_dir, exist_ok=True)

    try:
        if search_type == "product":
            driver.get("https://shopee.com.br/")
            pause(2, 3, parar_execucao)
            campo = wait_element(driver, By.CSS_SELECTOR, 'input.shopee-searchbar-input__input', timeout=10, parar_execucao=parar_execucao)
            campo.send_keys(termo, Keys.RETURN)
            wait_condition(driver, lambda d: "/search" in d.current_url or "/list/" in d.current_url, timeout=15, parar_execucao=parar_execucao)
        else:
            slug = slugify(termo)
            def abrir_loja(slug_try):
                driver.get(f"https://shopee.com.br/{slug_try}")
                pause(4, 5, parar_execucao)
                return not pagina_erro(driver.page_source)
            driver.get("https://shopee.com.br/")
            pause(2, 3, parar_execucao)
            campo = wait_element(driver, By.CSS_SELECTOR, 'input.shopee-searchbar-input__input', timeout=10, parar_execucao=parar_execucao)
            campo.send_keys(termo, Keys.RETURN)
            wait_condition(driver, lambda d: "/search" in d.current_url, timeout=12, parar_execucao=parar_execucao)
            pause(3, 3.7, parar_execucao)
            try:
                tab_lojas = driver.find_elements(By.XPATH, '//div[contains(@class,"tab")][contains(translate(., "A","a"), "lojas")]')
                if tab_lojas:
                    tab_lojas[0].click()
                    pause(1, 1.2, parar_execucao)
            except Exception:
                pass
            try:
                links_loja = driver.find_elements(By.XPATH,
                    f'//a[contains(@class,"search-shop") or contains(@class,"search-shop-card")][contains(translate(., "A","a"), "{slug}")]')
                if links_loja:
                    driver.execute_script("arguments[0].click();", links_loja[0])
                    pause(4, 5, parar_execucao)
                else:
                    if not abrir_loja(slug):
                        raise RuntimeError("Loja não encontrada.")
            except TimeoutException:
                if not abrir_loja(slug):
                    raise RuntimeError("Loja não encontrada.")
            if pagina_erro(driver.page_source):
                raise RuntimeError("Página 404 da loja.")

        if not isinstance(driver, uc.Chrome):
            raise TypeError("O objeto driver não é uma instância válida do WebDriver antes de acessar page_source.")

        if pagina_erro(driver.page_source):
            raise RuntimeError("Página 404 detectada; abortando.")

        pause(5, 5.8, parar_execucao)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        pause(0.7, 1.5, parar_execucao)

        total = total_paginas(driver, parar_execucao=parar_execucao)
        if max_pages is not None:
            total = min(total, int(max_pages))  # Limita pelo usuário
        print(f"🔵 Total de páginas: {total}\n")

        base = driver.current_url
        if search_type == "store" and "page=" not in base:
            base = url_com_page(base, 0)

        html_paths = []

        # ===== CHECA PARADA AQUI =====
        if is_parar(parar_execucao):
            print("[INFO] Execução interrompida pelo usuário antes de iniciar download dos HTMLs!")
            return dest_dir, driver, []

        for idx in range(total):
            if is_parar(parar_execucao):
                print("[INFO] Execução interrompida pelo usuário durante scraping!")
                break

            # driver.get pode travar se a página demorar para responder, não tem como interromper antes de terminar.
            driver.get(url_com_page(base, idx))
            pause(5, 6, parar_execucao)
            if not isinstance(driver, uc.Chrome):
                raise TypeError("O objeto driver não é uma instância válida do WebDriver após navegar.")
            if pagina_erro(driver.page_source):
                print("   ⚠️  Página retornou 404; pulando.")
                continue

            file_path = os.path.join(dest_dir, f"{idx + 1}.html")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("   ➔ salvo.")
            html_paths.append(file_path)

        print("\n📅 Raspagem concluída. Pronto para nova busca.")

    except (TimeoutException, WebDriverException) as e:
        print(f"\n❌ Erro Selenium: {getattr(e, 'msg', str(e))}")
    except Exception as e:
        print(f"\n❌ {e}")

    return dest_dir, driver, html_paths
