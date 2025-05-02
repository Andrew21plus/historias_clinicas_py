from fpdf import FPDF
from datetime import datetime
import os

class PDF(FPDF):
    def header(self):
        # Configuración del encabezado (opcional)
        pass
    
    def footer(self):
        # Configuración del pie de página
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        # Puedes personalizar este texto con el nombre de tu sistema
        self.cell(0, 10, f'Generado por Sistema Médico - Página {self.page_no()}/{{nb}}', 0, 0, 'C')

def generar_pdf_evoluciones(paciente_info, consultas, output_path="evoluciones.pdf"):
    try:
        pdf = PDF()
        pdf.add_page()
        pdf.alias_nb_pages()  # Para el número total de páginas
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_margins(left=10, top=10, right=10)
        effective_width = pdf.w - 20  # Ancho útil considerando márgenes
        
        # ===== ENCABEZADO PRINCIPAL =====
        pdf.set_font("Arial", 'B', 16)
        pdf.set_text_color(30, 30, 100)
        pdf.cell(effective_width, 10, "REPORTE DE EVOLUCIONES MÉDICAS", 0, 1, 'C')
        
        pdf.set_font("Arial", '', 12)
        pdf.set_text_color(0)
        pdf.cell(effective_width, 6, f"Paciente: {paciente_info.get('nombre', '')} {paciente_info.get('apellido', '')}", 0, 1, 'C')
        pdf.cell(effective_width, 6, f"Historia Clínica: {paciente_info.get('num_historia', '')}", 0, 1, 'C')
        pdf.cell(effective_width, 6, f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1, 'C')
        pdf.ln(10)

        # ===== DATOS DEL PACIENTE =====
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(effective_width, 8, "DATOS DEL PACIENTE", 0, 1)
        
        datos_paciente = [
            ["Edad:", paciente_info.get('edad', 'N/A')],
            ["Sexo:", paciente_info.get('sexo', 'N/A')],
            #["Fecha Nacimiento:", paciente_info.get('fecha_nacimiento', 'N/A')]
        ]
        
        pdf.set_font("Arial", '', 11)
        col_width = effective_width / 2
        for dato in datos_paciente:
            pdf.cell(col_width, 8, dato[0], border=0)
            pdf.cell(col_width, 8, str(dato[1]), border=0)
            pdf.ln()
        pdf.ln(10)

        # ===== SECCIÓN DE CONSULTAS =====
        for consulta in consultas:
            # Encabezado de consulta
            pdf.set_fill_color(200, 220, 255)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(effective_width, 8, f"CONSULTA: {consulta.get('fecha', 'Fecha no disponible')}", 0, 1, 'L', 1)
            pdf.ln(5)

            # ===== TABLA DE SIGNOS VITALES =====
            if consulta.get('signos_vitales'):
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(effective_width, 8, "SIGNOS VITALES", 0, 1)
                
                signos = consulta['signos_vitales'] or {}
                datos_signos = [
                    ["Presión Arterial:", signos.get('presion', 'N/A')],
                    ["Frec. Cardíaca:", signos.get('frec_cardiaca', 'N/A')],
                    ["Frec. Respiratoria:", signos.get('frec_respi', 'N/A')],
                    ["Temperatura:", f"{signos.get('temp', 'N/A')} °C"],
                    ["Peso:", f"{signos.get('peso', 'N/A')} kg"],
                    ["Talla:", f"{signos.get('talla', 'N/A')} cm"]
                ]
                
                pdf.set_font("Arial", '', 10)
                pdf.set_draw_color(200, 200, 200)
                pdf.set_line_width(0.3)
                
                # Cabecera de tabla
                pdf.set_fill_color(230, 230, 230)
                pdf.cell(effective_width/2, 8, "PARÁMETRO", 1, 0, 'C', 1)
                pdf.cell(effective_width/2, 8, "VALOR", 1, 1, 'C', 1)
                
                # Contenido de tabla
                for dato in datos_signos:
                    pdf.cell(effective_width/2, 8, dato[0], 1)
                    pdf.cell(effective_width/2, 8, str(dato[1]), 1)
                    pdf.ln()
                
                pdf.ln(8)

            # ===== TABLA DE DIAGNÓSTICOS =====
            if consulta.get('diagnosticos'):
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(effective_width, 8, "DIAGNÓSTICOS", 0, 1)

                pdf.set_font("Arial", '', 10)
                pdf.set_draw_color(200, 200, 200)

                # Cabecera
                pdf.set_fill_color(230, 230, 230)
                col_cie = effective_width * 0.2
                col_desc = effective_width * 0.6
                col_estado = effective_width * 0.2

                pdf.cell(col_cie, 8, "CIE", 1, 0, 'C', 1)
                pdf.cell(col_desc, 8, "DESCRIPCIÓN", 1, 0, 'C', 1)
                pdf.cell(col_estado, 8, "ESTADO", 1, 1, 'C', 1)

                for diag in consulta['diagnosticos']:
                    y_start = pdf.get_y()
                    x_start = pdf.get_x()

                    # CIE
                    pdf.multi_cell(col_cie, 8, diag.get('cie', ''), 1, 'L')
                    y_end_cie = pdf.get_y()
                    pdf.set_xy(x_start + col_cie, y_start)

                    # Descripción
                    pdf.multi_cell(col_desc, 8, diag.get('descripcion', ''), 1, 'L')
                    y_end_desc = pdf.get_y()
                    pdf.set_xy(x_start + col_cie + col_desc, y_start)

                    # Estado
                    estado = "Definitivo" if diag.get('estado') else "Presuntivo"
                    pdf.multi_cell(col_estado, 8, estado, 1, 'L')
                    y_end_estado = pdf.get_y()

                    # Ajustar Y a la fila más alta
                    pdf.set_y(max(y_end_cie, y_end_desc, y_end_estado))

                pdf.ln(8)

            # ===== TABLA DE PRESCRIPCIONES MEJORADA =====
            if consulta.get('prescripciones'):
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(effective_width, 8, "PRESCRIPCIONES MÉDICAS", 0, 1)
                
                # Configurar tabla
                pdf.set_font("Arial", '', 10)
                pdf.set_draw_color(200, 200, 200)
                
                # Definir anchos de columna
                col_med = effective_width * 0.4  # Medicamento
                col_dos = effective_width * 0.2  # Dosis
                col_ind = effective_width * 0.4  # Indicaciones
                
                # Cabecera
                pdf.set_fill_color(230, 230, 230)
                pdf.cell(col_med, 8, "MEDICAMENTO", 1, 0, 'C', 1)
                pdf.cell(col_dos, 8, "DOSIS", 1, 0, 'C', 1)
                pdf.cell(col_ind, 8, "INDICACIONES", 1, 1, 'C', 1)
                
                for presc in consulta['prescripciones']:
                    y_start = pdf.get_y()
                    x_start = pdf.get_x()

                    # Calcular alturas
                    pdf.set_xy(x_start, y_start)
                    h_med = pdf.get_string_width(presc.get('medicamento', '')) / (col_med - 1) * 8
                    h_dos = pdf.get_string_width(presc.get('dosis', '')) / (col_dos - 1) * 8
                    h_ind = pdf.get_string_width(presc.get('indicaciones', '')) / (col_ind - 1) * 8

                    # Estimar la altura máxima de la fila
                    max_height = max(
                        pdf.get_string_width(presc.get('medicamento', '')) // (col_med - 2) * 8 + 8,
                        pdf.get_string_width(presc.get('dosis', '')) // (col_dos - 2) * 8 + 8,
                        pdf.get_string_width(presc.get('indicaciones', '')) // (col_ind - 2) * 8 + 8,
                        8
                    )

                    # Celdas sincronizadas
                    pdf.multi_cell(col_med, 8, presc.get('medicamento', ''), 1, 'L')
                    y1 = pdf.get_y()
                    pdf.set_xy(x_start + col_med, y_start)

                    pdf.multi_cell(col_dos, 8, presc.get('dosis', ''), 1, 'L')
                    y2 = pdf.get_y()
                    pdf.set_xy(x_start + col_med + col_dos, y_start)

                    pdf.multi_cell(col_ind, 8, presc.get('indicaciones', ''), 1, 'L')
                    y3 = pdf.get_y()

                    pdf.set_y(max(y1, y2, y3))

                pdf.ln(8)

            # ===== TRATAMIENTO =====
            if consulta.get('tratamiento'):
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(effective_width, 8, "TRATAMIENTO", 0, 1)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(effective_width, 8, consulta.get('tratamiento', ''))
                pdf.ln(5)

            # ===== NOTAS DE EVOLUCIÓN =====
            if consulta.get('notas'):
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(effective_width, 8, "NOTAS DE EVOLUCIÓN", 0, 1)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(effective_width, 8, consulta.get('notas', ''))
                pdf.ln(5)

            # Línea separadora entre consultas
            pdf.set_draw_color(150, 150, 150)
            pdf.line(10, pdf.get_y(), pdf.w - 10, pdf.get_y())
            pdf.ln(10)

        # ===== GUARDAR ARCHIVO =====
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        pdf.output(output_path)
        return output_path

    except Exception as e:
        error_msg = f"Error al generar PDF: {str(e)}"
        print(error_msg)
        raise RuntimeError(error_msg) from e