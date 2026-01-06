import polars as pl
from core.utils.logger import log
from datetime import datetime
import os

class DataEngine:
    """
    Motor de procesamiento de datos ultra-rápido basado en Polars.
    Especializado en transformaciones Lazy y exportación eficiente.
    """

    @staticmethod
    def create_dataframe(data: list):
        """
        Convierte una lista de diccionarios en un Polars DataFrame.
        """
        try:
            return pl.DataFrame(data)
        except Exception as e:
            log.error(f"Error al crear DataFrame: {str(e)}")
            return pl.DataFrame()

    @staticmethod
    def save_output(df: pl.DataFrame, filename_base: str, format: str = "csv"):
        """
        Guarda el DataFrame en la carpeta data/processed con timestamp.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_base}_{timestamp}.{format}"
        path = os.path.join("data", "processed", filename)

        try:
            if format == "csv":
                df.write_csv(path)
            elif format == "json":
                df.write_json(path)

            log.success(f"Datos exportados exitosamente a: {path}")
            return path
        except Exception as e:
            log.error(f"Falló la exportación de datos: {str(e)}")
            return None

    @staticmethod
    def filter_leads(df: pl.DataFrame, score_column: str, threshold: float):
        """
        Ejemplo de pipeline de filtrado usando Lazy API.
        """
        return (
            df.lazy()
            .filter(pl.col(score_column) >= threshold)
            .sort(score_column, descending=True)
            .collect()
        )
