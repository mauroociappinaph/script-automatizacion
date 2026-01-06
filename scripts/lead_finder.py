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

        Responde en formato de lista corta:
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
        log.info(f"Iniciando búsqueda de agencias de marketing en: {location}")

        leads_processed = []

        with Scraper(headless=True) as motor:
            page = motor.get_page()
            search_url = f"https://www.google.com/search?q=mejores+agencias+marketing+digital+{location}"

            if motor.safe_navigate(page, search_url):
                motor.human_wait(2, 4)

                # Extraemos nombres de agencias (basado en resultados de búsqueda)
                elements = page.query_selector_all("h3")

                for el in elements[:5]: # Procesamos el TOP 5 para el demo comercial
                    agency_name = el.inner_text()
                    if agency_name and len(agency_name) > 3:
                        log.info(f"Analizando agencia: {agency_name}")

                        # Análisis de IA (Costo $0 con OpenRouter Free)
                        analysis = self.analyze_agency(agency_name, f"Agencia de marketing en {location}")

                        leads_processed.append({
                            "AGENCIA": agency_name,
                            "UBICACIÓN": location,
                            "OPORTUNIDADES_IA": analysis.replace("\n", " ").strip()[:200] + "..."
                        })

        if leads_processed:
            # 1. Almacenamos en Motor de Datos (CSV)
            df = DataEngine.create_dataframe(leads_processed)
            csv_path = DataEngine.save_output(df, f"leads_mkt_{location.lower()}", format="csv")

            # 2. Generamos Reporte PDF Profesional
            pdf_path = os.path.abspath(f"data/processed/REPORTE_LEADS_MKT_{location.upper()}.pdf")
            ReportGenerator.to_pdf(leads_processed, f"Análisis de Oportunidades: Agencias MKT {location}", pdf_path)

            return {
                "status": "success",
                "leads_found": len(leads_processed),
                "report": pdf_path
            }

        return {"status": "no_leads_found"}

if __name__ == "__main__":
    # Prueba real en Argentina
    finder = MarketingLeadFinder()
    finder.start(location="Argentina")
