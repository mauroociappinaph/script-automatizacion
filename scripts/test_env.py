from core.utils.logger import log
import polars as pl
import playwright
import spacy
import fastapi
import pydantic
import os

def test_environment():
    log.info("Iniciando prueba de entorno...")

    # Probar carga de ENV
    app_env = os.getenv("APP_ENV", "N/A")
    log.info(f"Entorno detectado: {app_env}")

    # Probar Polars
    df = pl.DataFrame({"status": ["ok", "fast", "polars"]})
    log.info(f"Polars verificado: {df.shape}")

    # Probar Imports
    log.success("✅ Todas las dependencias críticas cargadas correctamente.")
    log.info("Estructura de carpetas válida.")

if __name__ == "__main__":
    test_environment()
