import schedule
import time
from core.utils.logger import log
from scripts.test_reports import test_reporting
from scripts.scraper_example import ExampleScraper

def job_scraper():
    log.info("⏰ Ejecutando tarea programada: Scraper de búsqueda...")
    try:
        scraper = ExampleScraper()
        scraper.start(query="Mercado Libre Argentina")
    except Exception as e:
        log.error(f"Fallo en la tarea programada del Scraper: {e}")

# Programación de ejemplo:
# Ejecutar el scraper cada hora
schedule.every().hour.do(job_scraper)

# Ejecutar reportes de prueba cada 10 minutos
# schedule.every(10).minutes.do(test_reporting)

# Ejecutar todos los días a las 10:30
# schedule.every().day.at("10:30").do(job)

if __name__ == "__main__":
    log.info("🚀 Scheduler iniciado. Esperando tareas programadas...")
    while True:
        schedule.run_pending()
        time.sleep(1)
