# Análisis del Sistema de Automatización de Leads (Gemini CLI)

Este documento resume el análisis de la arquitectura, el stack tecnológico y las estrategias de despliegue para el sistema de generación de leads automatizado.

## 1. Resumen del Proyecto
El objetivo es construir un sistema inteligente para detectar oportunidades de venta de alta calidad mediante dos enfoques principales:
*   **Escucha Social (Leads Calientes):** Identificar usuarios expresando necesidades activas en redes sociales.
*   **Análisis Técnico (Intención de Compra):** Detectar empresas con deficiencias técnicas que señalan una necesidad de servicios.

## 2. Arquitectura de las Automatizaciones

### 🔍 Automatización 1: Leads Calientes (Social Listening)
*   **Objetivo:** Capturar la intención de compra explícita.
*   **Fuentes:** LinkedIn (posts/comentarios), Twitter/X, Reddit, Grupos públicos.
*   **Keywords Clave:** "alguien recomienda", "estoy buscando", "problemas con", "necesito proveedor".
*   **Flujo:**
    1.  **Playwright:** Navegación y extracción de texto + métricas de engagement.
    2.  **Polars:** Limpieza de datos y filtrado rápido.
    3.  **spaCy:** Análisis de NLP para confirmar la intención (descartar falsos positivos).

### 🏢 Automatización 2: Intención de Compra (Empresas)
*   **Objetivo:** Identificar clientes potenciales B2B basados en señales técnicas.
*   **Señales:**
    *   Búsquedas laborales activas (indica presupuesto/crecimiento).
    *   Webs lentas o con errores de carga.
    *   Ausencia de píxeles de seguimiento (Meta/GA).
*   **Lógica de Scoring:** `No pixel` + `Web lenta` + `Formulario roto` = 🔥 Lead prioritario.

### ⏱️ Automatización 3: Timing Perfecto
*   **Estrategia:** Scheduler que ejecuta las búsquedas cada X horas.
*   **Filtros de Relevancia:** Solo posts con < 48hs de antigüedad y engagement creciente.
*   **Resultado:** Contexto fresco para contactar al prospecto en el momento justo.

## 3. Stack Tecnológico (Definido en IDEA_GENERAL.md)
Una selección moderna priorizando performance y bajo overhead.

*   **Core:** Python 3.13 (Mejoras en async y performance).
*   **Navegación:** `Playwright` (Estándar actual, mejor manejo de anti-bots que Selenium).
*   **Datos:** `Polars` (Procesamiento de dataframes ultra-rápido y eficiente en RAM).
*   **NLP:** `spaCy` (Detección de entidades y frases de intención, robusto para producción).
*   **Orquestación:** `schedule` (Librería simple para cron jobs en scripts puros).
*   **Reportes:**
    *   `python-docx`: Para entregables editables en Word.
    *   `reportlab`: Para generación de PDFs finales.
*   **API (Opcional):** `FastAPI` (Solo como interfaz/disparador, manteniendo la lógica desacoplada).

## 4. Estrategia de Despliegue (Hosting Gratuito)

Para ejecutar el scheduler sin costos recurrentes, se analizaron tres opciones:

### Opción A: GitHub Actions (Recomendada para Batches)
*   **Funcionamiento:** Cron jobs definidos en archivos `.yml` en el repositorio.
*   **Pros:** 100% Gratis (hasta 2000 min/mes), infraestructura gestionada.
*   **Contras:** Las IPs de Azure (Microsoft) son fáciles de detectar por LinkedIn/Reddit. Requiere uso de proxies residenciales para evitar bloqueos.

### Opción B: Oracle Cloud "Always Free"
*   **Funcionamiento:** VPS (Máquina Virtual) gratuita con arquitectura ARM y 24GB RAM.
*   **Pros:** Potencia suficiente para Playwright, IP fija, control total del servidor (Linux).
*   **Contras:** Curva de aprendizaje de configuración de servidores Linux.

### Opción C: Ejecución Local (Mac) - **MVP Recomendado**
*   **Funcionamiento:** Scripts corriendo en background en tu propia máquina.
*   **Pros:** IP residencial (alta confianza, difícil de bloquear), costo cero, fácil depuración.
*   **Contras:** Requiere que el equipo esté encendido para ejecutar los jobs.

## 5. Visualización y Entrega

Para evitar dashboards complejos en esta etapa, la estrategia de "Push" es la más efectiva:

### 🚀 Integración con Telegram (Opción Ganadora)
*   **Mecanismo:** El script finaliza el análisis y utiliza la API de Telegram para enviar el PDF/Word generado directamente a un chat privado o canal.
*   **Ventaja:** Notificación instantánea en móvil/desktop. Cero costo de infraestructura de frontend.

### Alternativas
*   **Email (SMTP):** Envío de reportes adjuntos por correo.
*   **Servidor FastAPI:** Exponer los archivos en una ruta estática (requiere hosting tipo VPS).

## 6. Consideraciones de Seguridad y "Stealth"
Extraído de `Nota importante.md`:
*   **Rotación de User-Agent:** Imprescindible para simular diferentes navegadores/dispositivos.
*   **Delays Humanos:** Evitar patrones de scraping robóticos (tiempos fijos). Usar `random.sleep()`.
*   **Cuentas:** Uso cuidadoso de cuentas reales; riesgo de suspensión si se abusa de la velocidad de peticiones.

---
**Próximo Paso Sugerido:** Crear la estructura de carpetas e iniciar con el script "Hola Mundo" de Playwright + Telegram.
