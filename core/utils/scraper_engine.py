from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
from core.utils.logger import log
import random
import time

class Scraper:
    """
    Motor de scraping basado en Playwright con capacidades de sigilo (Stealth).
    Gestiona el ciclo de vida del navegador y contextos de forma segura.
    """

    def __init__(self, headless: bool = True, proxy: dict = None):
        self.headless = headless
        self.proxy = proxy # Formato: {"server": "http://ip:port", "username": "user", "password": "pwd"}
        self.pw = None
        self.browser = None
        self.context = None

    def __enter__(self):
        self.pw = sync_playwright().start()
        # Configuración de lanzamiento optimizada
        self.browser = self.pw.chromium.launch(
            headless=self.headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )
        # Contexto con User Agent realista y Proxy opcional
        context_args = {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        if self.proxy:
            context_args["proxy"] = self.proxy

        self.context = self.browser.new_context(**context_args)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.pw:
            self.pw.stop()
        log.debug("Navegador de Playwright cerrado correctamente.")

    def get_page(self):
        """
        Crea una nueva página aplicando el plugin de sigilo.
        """
        page = self.context.new_page()
        Stealth().apply_stealth_sync(page)
        return page

    def human_wait(self, min_sec: float = 1.0, max_sec: float = 3.0):
        """
        Simula una espera humana aleatoria.
        """
        sleep_time = random.uniform(min_sec, max_sec)
        log.debug(f"Esperando {sleep_time:.2f}s (Human Wait)...")
        time.sleep(sleep_time)

    def safe_navigate(self, page, url: str, timeout: int = 30000):
        """
        Navega a una URL con manejo de errores y reintentos básicos.
        """
        try:
            log.info(f"Navegando a: {url}")
            page.goto(url, wait_until="networkidle", timeout=timeout)
            return True
        except Exception as e:
            log.error(f"Error al navegar a {url}: {str(e)}")
            return False
