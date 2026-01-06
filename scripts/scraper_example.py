from core.base_script import BaseScript, handle_errors
from core.utils.scraper_engine import Scraper
from core.utils.logger import log
from core.utils.data_engine import DataEngine

class ExampleScraper(BaseScript):
    """
    Script de ejemplo que demuestra el flujo completo:
    Scraping -> Procesamiento -> Almacenamiento.
    """

    def __init__(self):
        super().__init__(name="ExampleScraper_Google")

    @handle_errors
    def run(self, query: str = "programación python"):
        log.info(f"Buscando información sobre: {query}")

        scraped_data = []

        # Uso del motor de scraping con context manager
        with Scraper(headless=True) as motor:
            page = motor.get_page()

            # Ejemplo: Navegar a Google (pestaña de noticias o similar)
            url = f"https://www.google.com/search?q={query}"
            if motor.safe_navigate(page, url):
                motor.human_wait(2, 4)

                # Extraer títulos de resultados (selectores de ejemplo para Google)
                # Nota: Los selectores de Google cambian frecuentemente, esto es ilustrativo.
                elements = page.query_selector_all("h3")

                for el in elements[:5]: # Solo los primeros 5
                    title = el.inner_text()
                    if title:
                        scraped_data.append({
                            "titulo": title,
                            "fuente": "Google Search",
                            "categoria": "Tech"
                        })

                log.info(f"Se extrajeron {len(scraped_data)} resultados.")

        # Procesar con el motor de datos si hay resultados
        if scraped_data:
            df = DataEngine.create_dataframe(scraped_data)
            path = DataEngine.save_output(df, "google_search_results", format="csv")
            return {"status": "success", "results_count": len(scraped_data), "file": path}

        return {"status": "no_data"}

if __name__ == "__main__":
    scraper = ExampleScraper()
    scraper.start(query="Inteligencia Artificial 2026")
