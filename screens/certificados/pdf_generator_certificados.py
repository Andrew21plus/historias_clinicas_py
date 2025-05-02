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
        self.cell(0, 10, f'Generado el {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 0, 'C')

def generar_pdf_certificado(data, output_path="certificados"):
    try:
        pdf = PDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Configurar márgenes y ancho efectivo
        pdf.set_margins(left=15, top=15, right=15)
        effective_width = pdf.w - 30  # Ancho útil considerando márgenes
        
        # ===== DATOS DEL PACIENTE =====
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(40, 10, 'Paciente:', 0, 0)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f"{data['paciente'].nombre} {data['paciente'].apellido}", 0, 1)
        
        # ===== FECHAS =====
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(40, 10, 'Fecha consulta:', 0, 0)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, data['fecha_consulta'], 0, 1)
        
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(40, 10, 'Fecha emisión:', 0, 0)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, data['fecha_emision'], 0, 1)
        pdf.ln(5)
        
        # ===== DIAGNÓSTICOS CON TABLA =====
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'DIAGNÓSTICOS:', 0, 1)
        
        if data['diagnosticos']:
            # Configurar tabla
            pdf.set_font('Arial', '', 11)
            pdf.set_draw_color(200, 200, 200)
            
            # Definir anchos de columna
            col_cie = effective_width * 0.2
            col_desc = effective_width * 0.8
            
            # Cabecera
            pdf.set_fill_color(230, 230, 230)
            pdf.cell(col_cie, 8, "CIE-10", 1, 0, 'C', 1)
            pdf.cell(col_desc, 8, "DESCRIPCIÓN", 1, 1, 'C', 1)
            
            # Contenido
            for diag in data['diagnosticos']:
                y_start = pdf.get_y()
                x_start = pdf.get_x()
                
                # CIE (primera columna)
                pdf.multi_cell(col_cie, 8, diag.split('(')[-1].replace(')', ''), 1, 'C')
                y_end_cie = pdf.get_y()
                pdf.set_xy(x_start + col_cie, y_start)
                
                # Descripción (segunda columna)
                descripcion = diag.split('(')[0].strip()
                pdf.multi_cell(col_desc, 8, descripcion, 1, 'L')
                y_end_desc = pdf.get_y()
                
                # Ajustar Y a la fila más alta
                pdf.set_y(max(y_end_cie, y_end_desc))
            
            pdf.ln(5)
        
        # ===== CONTINGENCIA =====
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(40, 10, 'Contingencia:', 0, 0)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, data['contingencia'].capitalize(), 0, 1)
        pdf.ln(5)
        
        # ===== INDICACIONES MÉDICAS =====
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Indicaciones médicas:', 0, 1)
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(effective_width, 8, data['indicaciones'], 0, 'L')
        pdf.ln(5)
        
        # ===== REPOSO (si aplica) =====
        if data['dias_reposo']:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, f"Reposo médico por {data['dias_reposo']} días", 0, 1, 'L')
            pdf.ln(5)
        
        # ===== FIRMA =====
        pdf.ln(15)
        pdf.cell(0, 10, '_________________________', 0, 1, 'C')
        pdf.cell(0, 10, 'Firma del profesional', 0, 1, 'C')
        pdf.cell(0, 5, f"Dr. {data.get('medico', 'Nombre del médico')}", 0, 1, 'C')
        
        # ===== GUARDAR ARCHIVO =====
        os.makedirs(output_path, exist_ok=True)
        filename = f"{output_path}/certificado_{data['paciente'].id_paciente}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(filename)
        return filename

    except Exception as e:
        error_msg = f"Error al generar PDF: {str(e)}"
        print(error_msg)
        raise RuntimeError(error_msg) from e