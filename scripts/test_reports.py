from core.utils.report_generator import ReportGenerator
from core.utils.logger import log
import os

def test_reporting():
    log.info("Iniciando prueba de generación de reportes...")

    # Datos ficticios para el reporte
    data = [
        {"nombre": "Empresa A", "leads": 45, "status": "Interesado"},
        {"nombre": "Empresa B", "leads": 12, "status": "No contactado"},
        {"nombre": "Empresa C", "leads": 89, "status": "Venta cerrada"}
    ]

    title = "Reporte de Prueba de Automatización 2026"

    # Rutas de salida
    word_path = os.path.abspath("data/processed/test_report.docx")
    pdf_path = os.path.abspath("data/processed/test_report.pdf")

    # Generar Word
    log.info("Generando Word...")
    ReportGenerator.to_word(data, title, word_path)

    # Generar PDF
    log.info("Generando PDF...")
    ReportGenerator.to_pdf(data, title, pdf_path)

    # Verificar existencia
    if os.path.exists(word_path) and os.path.exists(pdf_path):
        log.success("✅ Prueba de reportes exitosa. Archivos generados correctamente.")
    else:
        log.error("❌ Falló la prueba de reportes. Algunos archivos no se encontraron.")

if __name__ == "__main__":
    test_reporting()
