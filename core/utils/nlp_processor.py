import spacy
from core.utils.logger import log

class NLPProcessor:
    """
    Procesador de lenguaje natural local usando spaCy.
    Realiza NER (Reconocimiento de Entidades) y análisis de intención.
    """

    def __init__(self, model_name: str = "es_core_news_sm"):
        self.model_name = model_name
        self.nlp = None
        try:
            self.nlp = spacy.load(model_name)
            log.info(f"Modelo spaCy '{model_name}' cargado correctamente.")
        except Exception:
            log.warning(f"Modelo '{model_name}' no encontrado. Se requiere descarga manual.")

    def extract_entities(self, text: str):
        """
        Extrae entidades (Org, Loc, Per, etc.) del texto.
        """
        if not self.nlp:
            return []

        doc = self.nlp(text)
        entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
        return entities

    def analyze_intent(self, text: str, keywords: list):
        """
        Analiza si el texto contiene verbos de intención o frases clave.
        """
        if not self.nlp:
            return False

        doc = self.nlp(text.lower())
        # Ejemplo simple: buscar verbos específicos o lemas
        found = any(k.lower() in doc.text for k in keywords)
        return found
