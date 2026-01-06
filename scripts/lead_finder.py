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
        log.info(f"Iniciando búsqueda de leads profesionales en: {location}")

        leads_processed = []

        with Scraper(headless=True) as motor:
            page = motor.get_page()
            # Bing suele ser más amigable con scrapers básicos
            search_url = f"https://www.bing.com/search?q=agencias+marketing+digital+{location}"

            if motor.safe_navigate(page, search_url):
                # Esperamos un poco para renderizado
                motor.human_wait(3, 5)

                log.info(f"Página cargada: '{page.title()}'")

                # Selector de títulos en Bing
                elements = page.query_selector_all("li.b_algo h2 a")
                log.info(f"Resultados brutos encontrados: {len(elements)}")

                # Lista negra de palabras y validación de industria
                blacklist = ["amazon", "mercado libre", "shopee", "anuncio", "patrocinado", "sponsored"]
                keywords = ["agencia", "marketing", "digital", "publicidad", "ads", "seo", "branding", "estudio", "comunicación", "estrategia"]

                for el in elements:
                    if len(leads_processed) >= 5: # Límite para el reporte
                        break

                    try:
                        agency_name = el.text_content().strip()
                        lower_name = agency_name.lower()

                        log.debug(f"Evaluando: '{agency_name}'")

                        # 1. Filtro de Blacklist (Evitar Amazon, etc.)
                        if any(word in lower_name for word in blacklist):
                            log.debug(f"Saltando (blacklist/ad): {agency_name}")
                            continue

                        # 2. Validación de industria (Asegurar que sea marketing/agencia)
                        # Si no tiene palabras clave en el título, a veces es una agencia específica (ej: 'Puent7')
                        # Pero para el buscador automático, mejor pedir al menos una Keyword o filtrar menos agresivo
                        if not any(key in lower_name for key in keywords):
                            log.debug(f"Saltando (no parece agencia por nombre): {agency_name}")
                            continue

                        if len(agency_name) > 3:
                            log.info(f"✅ Lead de CALIDAD detectado: {agency_name}")

                            # Análisis de IA con OpenRouter (Gratis)
                            analysis = self.analyze_agency(agency_name, f"Agencia de marketing digital en {location}")

                            leads_processed.append({
                                "AGENCIA": agency_name,
                                "UBICACIÓN": location,
                                "OPORTUNIDADES_IA": analysis.replace("\n", " ").strip()[:200] + "..."
                            })
                    except Exception as e:
                        log.warning(f"Error procesando elemento: {e}")

                log.info(f"Procesamiento finalizado. Total leads reales: {len(leads_processed)}")

        if leads_processed:
            # 1. Guardar CSV
            df = DataEngine.create_dataframe(leads_processed)
            DataEngine.save_output(df, f"leads_mkt_{location.lower()}", format="csv")

            # 2. Generar PDF
            pdf_path = os.path.abspath(f"data/processed/REPORTE_LEADS_MKT_{location.upper()}.pdf")
            ReportGenerator.to_pdf(leads_processed, f"Análisis de leads: Agencias MKT {location}", pdf_path)
            log.success(f"Reporte PDF generado exitosamente: {pdf_path}")

            return {
                "status": "success",
                "leads_found": len(leads_processed),
                "report": pdf_path
            }

        return {"status": "no_leads_found"}

if __name__ == "__main__":
    finder = MarketingLeadFinder()
    finder.start(location="Argentina")
