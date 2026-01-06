import sys
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()

def setup_logger():
    """
    Configura el logger de loguru para el proyecto.
    En producción emite JSON, en desarrollo texto legible.
    """
    # Eliminar el logger por defecto
    logger.remove()

    # Nivel de log desde env o por defecto INFO
    log_level = os.getenv("LOG_LEVEL", "INFO")
    app_env = os.getenv("APP_ENV", "development")

    # Configuración para desarrollo (Colores y formato legible)
    if app_env == "development":
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=log_level,
            colorize=True
        )
    else:
        # Configuración para producción (JSON estructurado)
        logger.add(
            sys.stderr,
            format="{time} {level} {name} {message}",
            level=log_level,
            serialize=True # Esto convierte el output a JSON
        )

    # También guardar en un archivo local para debug persistente (ignorado por git)
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="7 days",
        level="DEBUG",
        compression="zip"
    )

    return logger

# Inicializar al importar
log = setup_logger()
