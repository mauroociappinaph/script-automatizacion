from abc import ABC, abstractmethod
from core.utils.logger import log
import time
import functools

def handle_errors(func):
    """
    Decorador para capturar errores en los scripts y loguearlos estandarizadamente.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log.exception(f"Error crítico en la ejecución de {func.__name__}: {str(e)}")
            raise e
    return wrapper

class BaseScript(ABC):
    """
    Clase base para todos los scripts de automatización.
    Provee logging, medición de tiempo y estructura estándar.
    """
    def __init__(self, name: str):
        self.name = name
        self.start_time = None

    def start(self, **kwargs):
        """
        Punto de entrada estandarizado.
        """
        self.start_time = time.time()
        log.info(f"🚀 Iniciando script: {self.name}")

        try:
            result = self.run(**kwargs)
            duration = time.time() - self.start_time
            log.success(f"✅ Script {self.name} completado con éxito en {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - self.start_time
            log.error(f"❌ Script {self.name} falló después de {duration:.2f}s")
            raise e

    @abstractmethod
    def run(self, **kwargs):
        """
        Lógica principal a ser implementada por cada script.
        """
        pass
