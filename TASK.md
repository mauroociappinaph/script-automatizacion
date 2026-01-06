# 📝 Roadmap de Implementación

Checklist para la construcción del sistema de automatización.

## Fase 1: Setup del Entorno 🟢
- [ ] Inicializar proyecto con `uv init`.
- [ ] Configurar `pyproject.toml` con las dependencias core (playwright, polars, spacy, fastapi, pydantic).
- [ ] Configurar el sistema de logging estructurado en `./core/utils/logger.py`.
- [ ] Crear estructura de carpetas inicial (`api/`, `scripts/`, `core/`, `data/`).

## Fase 2: Core de Automatización 🟠
- [ ] Implementar `BaseScript` en `./scripts/` para manejo de errores y logs.
- [ ] Implementar el primer Scraper usando Playwright + Stealth.
- [ ] Configurar cliente para **OpenRouter** (Filtrar solo por modelos `:free`).
- [ ] Configurar procesamiento de lenguaje natural con spaCy (Modelos NER de intención).
- [ ] Crear el motor de procesamiento de datos con Polars (Lazy API).

## Fase 3: Generación de Entregables 🔵
- [ ] Crear el módulo de generador de Word (`python-docx`).
- [ ] Crear el módulo de generador de PDF (`reportlab`).
- [ ] Implementar lógica de almacenamiento y nomenclatura de archivos en `data/processed/`.

## Fase 4: Capa de Servicio (API) 🟣
- [ ] Configurar `main.py` de FastAPI.
- [ ] Crear endpoint para disparar procesos de forma asíncrona.
- [ ] Crear endpoint para descarga de archivos generados.
- [ ] Implementar validación de API Key o seguridad básica.

## Fase 5: Optimización y Deploy 🚀
- [ ] Crear `Dockerfile` optimizado para Python 3.13.
- [ ] Implementar rotación de proxies en el scraper.
- [ ] Configurar tareas programadas (`schedule` o CRON externo).
