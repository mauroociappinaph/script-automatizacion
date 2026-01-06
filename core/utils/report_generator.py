from docx import Document
from docx.shared import Inches, Pt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from core.utils.logger import log
import os

class ReportGenerator:
    """
    Generador de reportes profesionales en formatos Word y PDF.
    """

    @staticmethod
    def to_word(data: list, title: str, output_path: str):
        """
        Genera un documento Word (.docx) con una tabla de datos.
        """
        try:
            doc = Document()
            doc.add_heading(title, 0)

            doc.add_paragraph(f"Reporte generado automáticamente el: {os.path.basename(output_path)}")

            if not data:
                doc.add_paragraph("No se encontraron registros para este reporte.")
            else:
                # Crear tabla
                keys = data[0].keys()
                table = doc.add_table(rows=1, cols=len(keys))
                table.style = 'Light Grid Accent 1'

                # Encabezados
                hdr_cells = table.rows[0].cells
                for i, key in enumerate(keys):
                    hdr_cells[i].text = str(key).upper()

                # Datos
                for item in data:
                    row_cells = table.add_row().cells
                    for i, key in enumerate(keys):
                        row_cells[i].text = str(item.get(key, ""))

            doc.save(output_path)
            log.success(f"Reporte Word guardado en: {output_path}")
            return output_path
        except Exception as e:
            log.error(f"Error generando reporte Word: {str(e)}")
            return None

    @staticmethod
    def to_pdf(data: list, title: str, output_path: str):
        """
        Genera un documento PDF profesional usando ReportLab.
        """
        try:
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []

            # Título
            title_style = styles['Title']
            elements.append(Paragraph(title, title_style))
            elements.append(Spacer(1, 12))

            if not data:
                elements.append(Paragraph("No se encontraron registros.", styles['Normal']))
            else:
                # Preparar datos para la tabla
                keys = list(data[0].keys())
                table_data = [keys] # Fila de encabezado

                for item in data:
                    table_data.append([str(item.get(k, "")) for k in keys])

                # Crear y estilar tabla
                t = Table(table_data)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(t)

            doc.build(elements)
            log.success(f"Reporte PDF guardado en: {output_path}")
            return output_path
        except Exception as e:
            log.error(f"Error generando reporte PDF: {str(e)}")
            return None
