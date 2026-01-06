from core.base_script import BaseScript, handle_errors
from core.utils.scraper_engine import Scraper
from core.utils.ai_client import OpenRouterClient
from core.utils.data_engine import DataEngine
from core.utils.report_generator import ReportGenerator
from core.utils.logger import log
import os
import time

class MarketingLeadFinder(BaseScript):
    """
    Script comercial para encontrar agencias de marketing de ALTA CALIDAD.
    Usa Playwright como motor de navegación y IA para el análisis.
    """

    def __init__(self):
        super().__init__(name="MarketingLeadFinder_Intelligence")
        self.ai = OpenRouterClient()

    def analyze_agency(self, name: str, snippet: str):
        """
        Usa IA para validar si es una agencia y sugerir automatizaciones.
        Pausa de 10s para evitar 429 en OpenRouter Free.
        """
        prompt = f"""
        OBJETIVO: Validar agencias de marketing para servicios de automatización.
        NOMBRE: {name}
        DATOS DEL BUSCADOR: {snippet}

        REGLAS:
        1. Si el sitio NO es una agencia de marketing (ej: Amazon, Google, una noticia, Mercado Libre), responde: RECHAZAR.
        2. Si ES una agencia, devuelve 3 oportunidades de automatización técnica.

        Respuesta:
        """
        try:
            time.sleep(12) # Pausa segura para cuotas gratuitas
            return self.ai.complete(prompt, system_prompt="Consultor experto en agencias B2B.")
        except Exception as e:
            log.warning(f"Error IA: {e}")
            return None

    @handle_errors
    def run(self, location: str = "Argentina"):
        log.info(f"Iniciando búsqueda de agencias reales en: {location}")

        leads_processed = []
        # Lista negra para evitar anuncios corporativos típicos
        forbidden = ["amazon", "google", "mercadolibre", "ebay", "noticia", "wikipedia", "youtube"]

        with Scraper(headless=True) as motor:
            page = motor.get_page()
            # Usamos Bing con un query más profesional para evitar basura
            search_url = f"https://www.bing.com/search?q=agencia+marketing+digital+{location}+official+website"

            if motor.safe_navigate(page, search_url):
                motor.human_wait(5, 8)

                # Capturamos bloques de resultados orgánicos
                results = page.query_selector_all("li.b_algo")
                log.info(f"Anatizando {len(results)} resultados potenciales...")

                for res in results:
                    if len(leads_processed) >= 5: break

                    try:
                        title_el = res.query_selector("h2 a")
                        snippet_el = res.query_selector(".b_caption p")

                        if not title_el: continue

                        name = title_el.text_content().strip()
                        snippet = snippet_el.text_content().strip() if snippet_el else ""

                        # Pre-filtro veloz
                        if any(f in name.lower() for f in forbidden):
                            log.debug(f"Saltando ruido: {name}")
                            continue

                        log.info(f"🔍 Validando lead: {name}")

                        # Validación inteligente
                        analysis = self.analyze_agency(name, snippet)

                        if not analysis or "RECHAZAR" in analysis.upper():
                            log.debug(f"IA rechazó el lead: {name}")
                            continue

                        log.success(f"🌟 Lead de calidad confirmado: {name}")

                        leads_processed.append({
                            "AGENCIA": name,
                            "UBICACIÓN": location,
                            "OPORTUNIDADES_IA": analysis.replace("\n", " ").strip()[:250] + "..."
                        })

                    except Exception as e:
                        log.warning(f"Error procesando resultado: {e}")

                log.info(f"Procesamiento finalizado. {len(leads_processed)} leads de calidad obtenidos.")

        if leads_processed:
            # Almacenamiento
            df = DataEngine.create_dataframe(leads_processed)
            DataEngine.save_output(df, f"leads_mkt_{location.lower()}", format="csv")

            # PDF
            pdf_path = os.path.abspath(f"data/processed/REPORTE_LEADS_MKT_{location.upper()}.pdf")
            ReportGenerator.to_pdf(leads_processed, f"Leads de Alta Calidad: Agencias MKT {location}", pdf_path)
            log.success(f"Reporte generado exitosamente.")

            return {"status": "success", "leads_found": len(leads_processed), "report": pdf_path}

        return {"status": "no_leads_found"}

if __name__ == "__main__":
    finder = MarketingLeadFinder()
    finder.start(location="Argentina")
