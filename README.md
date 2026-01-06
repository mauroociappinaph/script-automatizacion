# 🚀 Script Automation Stack 2026

Este proyecto implementa un ecosistema de automatización de alto rendimiento diseñado para ser modular, eficiente y fácil de escalar. Basado en el **Stack 2026**, prioriza el procesamiento local rápido y el desacoplamiento de componentes.

## 🛠 Tech Stack

- **Runtime**: [Python 3.13](https://docs.python.org/3.13/) (Performance & Async)
- **Package Manager**: [uv](https://github.com/astral-sh/uv) (Extremadamente rápido)
- **Scraping**: [Playwright](https://playwright.dev/python/) + `stealth`
- **Data Engine**: [Polars](https://pola.rs/) (Lazy API & SIMD)
- **NLP/AI**: [spaCy](https://spacy.io/) + [OpenRouter](https://openrouter.ai/) (Utilizando exclusivamente **modelos gratuitos**)
- **API/Orquestación**: [FastAPI](https://fastapi.tiangolo.com/) (Opcional, desacoplada)
- **Validation**: [Pydantic V2](https://docs.pydantic.dev/latest/)
- **Reports**: `python-docx` & `reportlab`

## 🏗 Arquitectura

El proyecto sigue el **Principio de Responsabilidad Única (SRP)**:

1.  **`/scripts`**: Contiene la lógica core de automatización. Cada script es independiente, ejecutable por CLI y utiliza Pydantic para validar sus entradas/salidas.
2.  **`/api`**: Una capa delgada de FastAPI que actúa como interfaz de usuario/sistema externo. Recibe parámetros, dispara los scripts y devuelve los resultados (JSON, Word o PDF).
3.  **`/core`**: Lógica compartida, tipos de Pydantic y utilidades de procesamiento.

## 🚀 Inicio Rápido

### Requisitos
- [uv](https://github.com/astral-sh/uv) instalado.

### Instalación
```bash
# Sincronizar entorno y dependencias
uv sync

# Instalar navegadores de Playwright
uv run playwright install chromium
```

### Ejecutar un Script
```bash
uv run python -m scripts.mi_automatizacion --parametro valor
```

### Levantar API
```bash
uv run fastapi dev api/main.py
```

### Ejecutar con Docker (Recomendado)
```bash
# Construir y levantar todo el ecosistema
docker-compose up --build -d

# Ver logs en tiempo real
docker-compose logs -f
```
La API estará disponible en `http://localhost:8000`.

## 📈 Roadmap & Tareas
Consulta el archivo [TASK.md](./TASK.md) para ver el progreso del desarrollo.
