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
    Intelligence V5: Buscador basado en Yahoo para eludir bloqueos.
    Extrae leads de LinkedIn y Reddit y los valida con IA.
    """

    def __init__(self):
        super().__init__(name="MarketingLeadFinder_Intelligence_V5")
        self.ai = OpenRouterClient()

    def analyze_source(self, name: str, snippet: str, source: str):
        """
        Valida si el lead es una agencia real y propone automatizaciones.
        Pausa de 15s para evitar Rate Limit de OpenRouter Free.
        """
        prompt = f"""
        OBJETIVO: Identificar leads de agencias de marketing para servicios de automatización.
        FUENTE: {source}
        TÍTULO/NOMBRE: {name}
        DESCRIPCIÓN: {snippet}

        REGLAS:
        1. Si NO es una agencia de marketing clara o no está en Argentina, responde: RECHAZAR.
        2. Si ES un lead válido, genera 3 oportunidades de automatización técnica que les ahorren dinero.

        Respuesta:
        """
        try:
            log.info(f"Aguardando 15s para validar lead: {name[:30]}...")
            time.sleep(15)
            resp = self.ai.complete(prompt, system_prompt="Consultor B2B experto en automatización.")
            return resp
        except Exception as e:
            log.warning(f"Error en IA: {e}")
            return None

    @handle_errors
    def run(self, location: str = "Argentina"):
        log.info(f"🚀 Iniciando Intelligence V5 (Yahoo Source) en: {location}")

        leads_processed = []
        # Yahoo es más permisivo con dorks simples
        search_queries = [
            f"site:linkedin.com/company \"marketing digital\" {location}",
            f"site:reddit.com \"agencia de marketing\" {location}"
        ]

        with Scraper(headless=True) as motor:
            page = motor.get_page()

            for query in search_queries:
                source_name = "LinkedIn" if "linkedin" in query else "Reddit"
                # Usamos Yahoo Search
                search_url = f"https://search.yahoo.com/search?p={query}"

                if motor.safe_navigate(page, search_url):
                    motor.human_wait(5, 8)
                    log.info(f"Buscando en {source_name} vía Yahoo...")

                    # Selector de Yahoo: div.algo (contenedores de resultados)
                    results = page.query_selector_all("div.algo")
                    log.info(f"Resultados potenciales encontrados: {len(results)}")

                    if not results:
                        log.warning("No se detectaron bloques 'div.algo'. Probando fallback 'h3 a'...")
                        results = page.query_selector_all("h3 a")
                        log.info(f"Fallback: {len(results)} enlaces directos encontrados.")

                    for res in results:
                        if len(leads_processed) >= 5: break # Límite para el demo

                        try:
                            # Si res es el enlace directamente (fallback), lo usamos.
                            # Si es un div (bloque), buscamos el enlace dentro.
                            tag_name = res.evaluate("node => node.tagName").lower()
                            title_el = res.query_selector("h3 a") if tag_name == "div" else res

                            if not title_el: continue

                            title = title_el.text_content().strip()

                            snippet_el = None
                            if tag_name == "div":
                                snippet_el = res.query_selector("div.compText") or res.query_selector("p")

                            snippet = snippet_el.text_content().strip() if snippet_el else ""

                            # Filtro rápido de ruido (Amazon, Anuncios genéricos)
                            forbidden = ["amazon", "mercado libre", "shopee", "movie", "news"]
                            if any(f in title.lower() for f in forbidden):
                                continue

                            log.info(f"🔍 Validando lead potencial: {title[:50]}...")
                            analysis = self.analyze_source(title, snippet, source_name)

                            if not analysis or "RECHAZAR" in analysis.upper():
                                log.debug("Lead rechazado por irrelevancia.")
                                continue

                            log.success(f"🌟 LEAD VALIDADO ({source_name}): {title[:40]}")

                            leads_processed.append({
                                "AGENCIA/PERFIL": title[:100],
                                "FUENTE": source_name,
                                "UBICACIÓN": location,
                                "OPORTUNIDADES_IA": analysis.replace("\n", " ").strip()[:240] + "..."
                            })

                        except Exception as e:
                            log.warning(f"Error procesando resultado: {e}")

        if leads_processed:
            df = DataEngine.create_dataframe(leads_processed)
            csv_path = DataEngine.save_output(df, f"leads_yahoo_{location.lower()}", format="csv")

            pdf_path = os.path.abspath(f"data/processed/REPORTE_LEADS_YAHOO_{location.upper()}.pdf")
            ReportGenerator.to_pdf(leads_processed, f"Leads de Alta Calidad: Redes Sociales {location}", pdf_path)
            log.success(f"Reporte generado exitosamente: {pdf_path}")

            return {"status": "success", "leads_found": len(leads_processed), "report": pdf_path}

        return {"status": "no_leads_found"}

if __name__ == "__main__":
    finder = MarketingLeadFinder()
    finder.start(location="Argentina")
