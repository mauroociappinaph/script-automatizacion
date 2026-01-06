# Usar la imagen oficial de Python 3.13 (slim para menor peso)
FROM python:3.13-slim-bookworm

# Instalar dependencias del sistema necesarias para Playwright y spaCy
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    asound2 \
    && rm -rf /var/lib/apt/lists/*

# Instalar uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Configurar directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias primero para cachear capas
COPY pyproject.toml uv.lock ./

# Instalar dependencias sin crear entorno virtual (usar el sistema del contenedor)
# Y descargar el modelo de spaCy
RUN uv sync --frozen \
    && uv pip install es_core_news_sm

# Instalar navegadores de Playwright
RUN uv run playwright install chromium --with-deps

# Copiar el resto del código
COPY . .

# Exponer el puerto de FastAPI
EXPOSE 8000

# Comando para arrancar la API con Uvicorn
CMD ["uv", "run", "fastapi", "run", "api/main.py", "--host", "0.0.0.0", "--port", "8000"]
