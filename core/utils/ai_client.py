import os
import requests
from core.utils.logger import log
from dotenv import load_dotenv

load_dotenv()

class OpenRouterClient:
    """
    Cliente para interactuar con la API de OpenRouter.
    Diseñado para filtrar y utilizar exclusivamente modelos gratuitos (:free).
    """

    API_URL = "https://openrouter.ai/api/v1/chat/completions"

    # Lista de modelos gratuitos recomendados (pueden variar, se prefiere detectarlos dinámicamente o por sufijo)
    # Ejemplo: "google/gemini-pro-1.5-exp:free", "meta-llama/llama-3-8b-instruct:free"
    DEFAULT_MODEL = "google/gemini-2.0-flash-exp:free"

    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            log.warning("OPENROUTER_API_KEY no encontrada en el archivo .env. La IA externa no funcionará.")

    def complete(self, prompt: str, system_prompt: str = "Eres un asistente útil.", model: str = None):
        """
        Envía una petición a OpenRouter asegurando que el modelo sea gratuito.
        """
        if not self.api_key:
            return "Error: No API Key configurada."

        target_model = model or self.DEFAULT_MODEL

        # Validación forzada: El modelo DEBE terminar en :free para ser gratuito
        if not target_model.endswith(":free"):
            log.warning(f"El modelo {target_model} podría no ser gratuito. Forzando fallback a {self.DEFAULT_MODEL}")
            target_model = self.DEFAULT_MODEL

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/mauroociappinaph/script-automatizacion", # Requerido por OpenRouter
            "X-Title": "Script Automatizacion 2026",
            "Content-Type": "application/json"
        }

        payload = {
            "model": target_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3 # Baja temperatura para análisis más deterministas
        }

        try:
            log.info(f"Consultando IA (OpenRouter - {target_model})...")
            response = requests.post(self.API_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            data = response.json()
            answer = data["choices"][0]["message"]["content"]

            log.success("Respuesta de IA recibida correctamente.")
            return answer

        except Exception as e:
            log.error(f"Error consultando OpenRouter: {str(e)}")
            return None
