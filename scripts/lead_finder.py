from core.base_script import BaseScript, handle_errors
from core.utils.scraper_engine import Scraper
from core.utils.ai_client import OpenRouterClient
from core.utils.data_engine import DataEngine
from core.utils.report_generator import ReportGenerator
from core.utils.logger import log
import os

class MarketingLeadFinder(BaseScript):
    """
    Script comercial para encontrar agencias de marketing y analizar
    sus oportunidades de automatización usando IA.
    """

    def __init__(self):
        super().__init__(name="MarketingLeadFinder_Intelligence")
        self.ai = OpenRouterClient()

    def analyze_agency(self, name: str, description: str):
        """
        Usa IA para identificar 'puntos de dolor' y oportunidades de venta.
        """
        prompt = f"""
        Analiza esta Agencia de Marketing y dime 3 oportunidades de AUTOMATIZACIÓN DE PROCESOS
        que les ayudarían a ahorrar dinero. Sé específico y profesional.

        Agencia: {name}
        Descripción/Contexto: {description}

        Si el nombre NO parece ser una agencia de marketing (ej: Amazon, Mercado Libre, un anuncio genérico),
        responde únicamente con la palabra: RECHAZAR.

        Si es válida, responde en formato de lista corta:
        1. [Oportunidad 1]
        2. [Oportunidad 2]
        3. [Oportunidad 3]
        """
        try:
            return self.ai.complete(prompt, system_prompt="Eres un experto en consultoría de automatización B2B.")
        except Exception:
            return "No se pudo realizar el análisis de IA para esta agencia."

    @handle_errors
    def run(self, location: str = "Argentina"):
        log.info(f"Iniciando búsqueda de leads profesionales en: {location}")

        leads_processed = []

        with Scraper(headless=True) as motor:
            page = motor.get_page()
            # Bing suele ser más amigable con scrapers básicos
            search_url = f"https://www.bing.com/search?q=agencias+marketing+digital+{location}"

            if motor.safe_navigate(page, search_url):
                motor.human_wait(3, 5)

                log.info(f"Página cargada: '{page.title()}'")

                # Buscamos los bloques de resultados orgánicos (li.b_algo)
                results = page.query_selector_all("li.b_algo")
                log.info(f"Bloques de resultados encontrados: {len(results)}")

                for res in results:
                    if len(leads_processed) >= 5:
                        break

                    try:
                        title_el = res.query_selector("h2 a")
                        if not title_el:
                            continue

                        agency_name = title_el.text_content().strip()
                        log.debug(f"Candidato detectado: '{agency_name}'")

                        # Análisis y Filtrado por IA (Más inteligente que keywords)
                        analysis = self.analyze_agency(agency_name, f"Agencia de marketing digital en {location}")

                        if "RECHAZAR" in analysis.upper():
                            log.debug(f"Lead rechazado por la IA (No es agencia): {agency_name}")
                            continue

                        log.info(f"✅ Lead VALIDADO por IA: {agency_name}")

                        leads_processed.append({
                            "AGENCIA": agency_name,
                            "UBICACIÓN": location,
                            "OPORTUNIDADES_IA": analysis.replace("\n", " ").strip()[:200] + "..."
                        })
                    except Exception as e:
                        log.warning(f"Error procesando lead: {e}")

                log.info(f"Procesamiento finalizado. Total leads validados: {len(leads_processed)}")

        if leads_processed:
            # 1. Guardar CSV
            df = DataEngine.create_dataframe(leads_processed)
            csv_path = DataEngine.save_output(df, f"leads_mkt_{location.lower()}", format="csv")

            # 2. Generar PDF
            pdf_path = os.path.abspath(f"data/processed/REPORTE_LEADS_MKT_{location.upper()}.pdf")
            ReportGenerator.to_pdf(leads_processed, f"Análisis de leads: Agencias MKT {location}", pdf_path)
            log.success(f"Reporte PDF generado: {pdf_path}")

            return {
                "status": "success",
                "leads_found": len(leads_processed),
                "report": pdf_path
            }

        return {"status": "no_leads_found"}

if __name__ == "__main__":
    finder = MarketingLeadFinder()
    finder.start(location="Argentina")
