from fastapi import FastAPI, BackgroundTasks, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from core.utils.logger import log
from dotenv import load_dotenv

load_dotenv()

API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key == os.getenv("API_KEY"):
        return api_key
    raise HTTPException(status_code=403, detail="Acceso denegado: API Key inválida.")

app = FastAPI(
    title="Ecosistema de Automatización 2026",
    description="API para orquestar scripts de scraping y generación de reportes profesionales.",
    version="1.0.0"
)

# Configuración básica de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "API de Automatización lista.",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Endpoint para descarga de reportes procesados
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join("data", "processed", filename)

    if not os.path.exists(file_path):
        log.error(f"Intento de descarga fallido: {filename} no existe.")
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )

# Importamos rutas de scripts aquí para evitar circulares
# En un proyecto más grande usaríamos APIRouter de forma separada
@app.post("/run-test", dependencies=[Depends(get_api_key)])
async def run_test_automated(background_tasks: BackgroundTasks):
    """
    Dispara el script de prueba de reportes en segundo plano.
    """
    from scripts.test_reports import test_reporting

    log.info("API: Recibida petición para ejecutar test_reports")
    background_tasks.add_task(test_reporting)

    return {"message": "Script de prueba iniciado en segundo plano. Revisa los logs para el progreso."}
