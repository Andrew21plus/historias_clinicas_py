from fpdf import FPDF
from datetime import datetime
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'CERTIFICADO MÉDICO', 0, 1, 'C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'GENERADO EL {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 0, 'C')

def generar_pdf_certificado(data, output_path="certificados"):
    try:
        pdf = PDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Configurar márgenes y ancho efectivo
        pdf.set_margins(left=15, top=15, right=15)
        effective_width = pdf.w - 30
        
        # Función para convertir texto a mayúsculas
        def to_upper(text):
            return text.upper() if text else ""
        
        # ===== DATOS DEL PACIENTE =====
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(40, 10, to_upper('Paciente:'), 0, 0)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, to_upper(f"{data['paciente'].nombre} {data['paciente'].apellido}"), 0, 1)
        
        # ===== FECHAS =====
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(40, 10, to_upper('Fecha consulta:'), 0, 0)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, to_upper(data['fecha_consulta']), 0, 1)
        
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(40, 10, to_upper('Fecha emisión:'), 0, 0)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, to_upper(data['fecha_emision']), 0, 1)
        pdf.ln(10)
        
        # ===== TEXTO DE CERTIFICACIÓN =====
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(effective_width, 8, to_upper(data['texto_certificacion']), 0, 'J')
        pdf.ln(10)
        
        # ===== DIAGNÓSTICOS CON TABLA =====
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, to_upper('Diagnósticos:'), 0, 1)
        
        if data['diagnosticos']:
            pdf.set_font('Arial', '', 11)
            pdf.set_draw_color(200, 200, 200)
            
            col_cie = effective_width * 0.2
            col_desc = effective_width * 0.8
            
            pdf.set_fill_color(230, 230, 230)
            pdf.cell(col_cie, 8, to_upper("CIE-10"), 1, 0, 'C', 1)
            pdf.cell(col_desc, 8, to_upper("Descripción"), 1, 1, 'C', 1)
            
            for diag in data['diagnosticos']:
                y_start = pdf.get_y()
                x_start = pdf.get_x()
                
                # Extraer código CIE (última parte entre paréntesis)
                cie_code = diag.split('(')[-1].replace(')', '').strip()
                pdf.multi_cell(col_cie, 8, to_upper(cie_code), 1, 'C')
                y_end_cie = pdf.get_y()
                pdf.set_xy(x_start + col_cie, y_start)
                
                # Extraer descripción (todo antes del paréntesis)
                descripcion = diag.split('(')[0].strip()
                pdf.multi_cell(col_desc, 8, to_upper(descripcion), 1, 'L')
                y_end_desc = pdf.get_y()
                
                pdf.set_y(max(y_end_cie, y_end_desc))
            
            pdf.ln(10)
        
        # ===== CONTINGENCIA =====
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(40, 10, to_upper('Contingencia:'), 0, 0)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, to_upper(data['contingencia']), 0, 1)
        pdf.ln(5)
        
        # ===== INDICACIONES MÉDICAS =====
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, to_upper('Indicaciones médicas:'), 0, 1)
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(effective_width, 8, to_upper(data['indicaciones']), 0, 'L')
        pdf.ln(5)
        
        # ===== REPOSO (si aplica) =====
        if data['dias_reposo']:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, to_upper(f"Reposo médico por {data['dias_reposo']} días"), 0, 1, 'L')
            pdf.ln(5)
        
        # ===== FIRMA =====
        pdf.ln(15)
        pdf.cell(0, 10, '_________________________', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, to_upper('Firma del profesional'), 0, 1, 'C')
        pdf.cell(0, 5, to_upper(f"Dr. {data['medico']}"), 0, 1, 'C')
        
        # ===== GUARDAR ARCHIVO =====
        os.makedirs(output_path, exist_ok=True)
        filename = f"{output_path}/certificado_{data['paciente'].id_paciente}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(filename)
        return filename

    except Exception as e:
        error_msg = f"Error al generar PDF: {str(e)}"
        print(error_msg)
        raise RuntimeError(error_msg) from e