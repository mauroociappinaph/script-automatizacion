from core.base_script import BaseScript, handle_errors
from core.utils.ai_client import OpenRouterClient
from core.utils.logger import log
import os
import datetime

class ContentGenerator(BaseScript):
    """
    Script de Automatización de Contenido B2B.
    Genera Artículos de Blog, Posts de LinkedIn y Prompts de Imagen a partir de un tema.
    """

    def __init__(self):
        super().__init__(name="B2B_Content_Machine")
        self.ai = OpenRouterClient()

    def generate_blog_post(self, topic: str, target_audience: str, tone: str):
        log.info("✍️ Redactando Artículo de Blog (SEO optimizado)...")
        prompt = f"""
        Actúa como un Redactor SEO Experto B2B.
        Escribe un artículo de blog completo sobre: "{topic}".

        Público Objetivo: {target_audience}
        Tono: {tone}

        Estructura requerida (en Markdown):
        1. Título H1 (Pegadizo y con Keywords)
        2. Introducción (Problema + Agitación + Solución)
        3. 3 a 5 Subtítulos H2 desarrollados en profundidad.
        4. Conclusión con Call to Action (CTA).
        5. Meta Descripción para Google.

        El contenido debe ser original, valioso y sin relleno.
        """
        return self.ai.complete(prompt, system_prompt="Eres un redactor profesional de tecnología y negocios.")

    def generate_linkedin_post(self, blog_content: str):
        log.info("🚀 Creando Post Viral para LinkedIn...")
        prompt = f"""
        Basado en el siguiente artículo, crea un Post de LinkedIn de alto impacto.

        Artículo:
        {blog_content[:1500]}... (resumen)

        Estructura del Post:
        1. "Hook" (Gancho) controversial o pregunta en la primera línea.
        2. Espacios en blanco para facilitar lectura.
        3. Lista de bullets con los insights clave.
        4. CTA (Call to Action) para comentar.
        5. 3 Hashtags relevantes.

        Usa emojis estratégicos pero sin abusar.
        """
        return self.ai.complete(prompt, system_prompt="Eres un experto en Ghostwriting para LinkedIn.")

    def generate_image_prompt(self, topic: str):
        log.info("🎨 Diseñando Prompt de Imagen (Midjourney)...")
        prompt = f"""
        Crea un prompt detallado para generar una imagen de portada para un artículo sobre "{topic}".
        Estilo: Profesional, Minimalista, Tecnológico, Cinematic Lighting, 8k.
        Formato del prompt: Solo el texto en inglés para copiar y pegar en Midjourney o DALL-E 3.
        """
        return self.ai.complete(prompt, system_prompt="Eres un experto en Ingeniería de Prompts para Arte Digital.")

    @handle_errors
    def run(self, topic: str = "Automatización con IA", audience: str = "Dueños de PYMES", tone: str = "Profesional"):
        log.info(f"Iniciando Generación de Contenido sobre: '{topic}'")

        # 1. Generar Blog Post
        blog_post = self.generate_blog_post(topic, audience, tone)
        if not blog_post:
            log.error("Fallo generando el blog post.")
            return

        # 2. Generar LinkedIn Post
        linkedin_post = self.generate_linkedin_post(blog_post)

        # 3. Generar Image Prompt
        image_prompt = self.generate_image_prompt(topic)

        # 4. Guardar Pack
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"content_{timestamp}.md"
        filepath = os.path.abspath(f"data/content/{filename}")

        final_content = f"""# 📦 Pack de Contenido: {topic}
Fecha: {datetime.datetime.now().strftime("%d/%m/%Y")}

---
## 🖼️ Prompt de Imagen (Copy-Paste)
`{image_prompt}`

---
## 🟦 Post de LinkedIn
{linkedin_post}

---
## 📝 Artículo de Blog (SEO)
{blog_post}
"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_content)

        log.success(f"¡Contenido generado exitosamente! Guardado en: {filepath}")
        return {"status": "success", "file": filepath}

if __name__ == "__main__":
    generator = ContentGenerator()
    # Ejemplo de uso directo
    generator.start(
        topic="Cómo la IA reduce costos en estudios jurídicos",
        audience="Abogados Socios y Gerentes Legales",
        tone="Autoridad y Confianza"
    )
