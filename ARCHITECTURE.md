# 🏛 Arquitectura y Estructura del Proyecto

## Filosofía de Diseño

Este proyecto fue concebido bajo la premisa de **"Scripts Primero, API Después"**. La lógica de negocio reside en scripts puros que deben poder ejecutarse en cualquier entorno (CI/CD, local, servidor) sin necesidad de levantar un servidor web.

### Desacoplamiento (SRP)
- **Lógica de Automatización**: No conoce la existencia de FastAPI. Recibe diccionarios o modelos de Pydantic y devuelve objetos de datos. Utiliza una estrategia **Local-First** (spaCy) y recurre a **OpenRouter (Free Models)** solo si la complejidad lo requiere, manteniendo un costo de operación de $0.
- **Lógica de Interfaz (API)**: Se encarga de la autenticación, validación de request HTTP, persistencia ligera y disparar los scripts mediante procesos o llamadas a funciones asíncronas.

## 📂 Estructura de Carpetas Propuesta

```text
.
├── .venv/                # Entorno virtual gestionado por uv
├── pyproject.toml        # Configuración de dependencias (uv)
├── README.md
├── ARCHITECTURE.md
├── TASK.md
│
├── api/                  # Capa de FastAPI
│   ├── main.py           # Punto de entrada
│   ├── routes/           # Endpoints organizados por dominio
│   └── dependencies.py   # Inyección de dependencias
│
├── core/                 # Código compartido
│   ├── config.py         # Variables de entorno y constantes
│   ├── models/           # Esquemas Pydantic comunes
│   └── utils/            # Helpers de logging, procesamiento, etc.
│
├── scripts/              # "Cerebro" de automatización
│   ├── base_script.py    # Clase base o utilidades para scripts
│   ├── scraper_leads.py  # Ejemplo de script de scraping
│   └── reporter.py       # Lógica de generación de Docs y PDFs
│
├── data/                 # Almacenamiento local temporal
│   ├── raw/              # JSONs/CSVs crudos
│   └── processed/        # Outputs finales listos para descarga
│
└── tests/                # Testing unitario y de integración
```

## 🛠 Convenciones Técnicas

### 1. Manejo de Datos (Polars)
Se prefiere la `Lazy API` para todas las transformaciones:
```python
import polars as pl

def process_data(path: str):
    return (
        pl.scan_csv(path)
        .filter(pl.col("leads") > 10)
        .collect() # Solo al final se ejecuta
    )
```

### 2. Evasión de Bots
Todo script de Playwright debe inicializarse con el plugin de `stealth` para maximizar la tasa de éxito en navegaciones complejas.

### 3. Logging Estructurado
No se utiliza `print()`. Se utiliza un logger configurado para emitir JSON en producción, permitiendo que FastAPI capture y exponga los logs del script si es necesario.
