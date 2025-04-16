from fpdf import FPDF
from datetime import datetime

def generar_pdf_evoluciones(paciente_info, consultas, output_path="evoluciones.pdf"):
    pdf = FPDF()
    pdf.add_page()

    # === Estilo general ===
    pdf.set_auto_page_break(auto=True, margin=15)

    # Encabezado
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(30, 30, 100)
    pdf.cell(0, 10, f"Reporte de Evoluciones Médicas", 0, 1, 'C')
    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(0)
    pdf.cell(0, 10, f"Paciente: {paciente_info['nombre']} {paciente_info['apellido']} | Historia Clínica: {paciente_info['num_historia']}", 0, 1, 'C')
    pdf.cell(0, 10, f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1, 'C')
    pdf.ln(10)

    # Información personal
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 10, "Datos del Paciente", 0, 1)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, f"Edad: {paciente_info['edad']}", 0, 1)
    pdf.cell(0, 8, f"Sexo: {paciente_info['sexo']}", 0, 1)
    pdf.ln(8)

    # Sección de consultas
    for consulta in consultas:
        pdf.set_draw_color(200, 200, 200)
        pdf.set_fill_color(230, 230, 250)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"Consulta del {consulta['fecha']}", 0, 1, '', fill=True)

        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(0)

        # Signos vitales
        if consulta.get('signos_vitales'):
            signos = consulta['signos_vitales']
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 8, "Signos Vitales:", 0, 1)
            pdf.set_font("Arial", '', 10)
            for etiqueta, valor in {
                "Presión Arterial": signos.get('presion', 'N/A'),
                "Frec. Cardíaca": signos.get('frec_cardiaca', 'N/A'),
                "Frec. Respiratoria": signos.get('frec_respi', 'N/A'),
                "Temperatura": f"{signos.get('temp', 'N/A')} °C",
                "Peso": f"{signos.get('peso', 'N/A')} kg",
                "Talla": f"{signos.get('talla', 'N/A')} cm",
            }.items():
                pdf.cell(0, 6, f"  - {etiqueta}: {valor}", 0, 1)
            pdf.ln(2)

        # Diagnósticos
        if consulta.get('diagnosticos'):
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 8, "Diagnósticos:", 0, 1)
            pdf.set_font("Arial", '', 10)
            for diag in consulta['diagnosticos']:
                pdf.cell(0, 6, f"  - {diag.get('cie')}: {diag.get('descripcion')} ({diag.get('estado')})", 0, 1)
            pdf.ln(2)

        # Prescripciones
        if consulta.get('prescripciones'):
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 8, "Prescripciones:", 0, 1)
            pdf.set_font("Arial", '', 10)
            for presc in consulta['prescripciones']:
                pdf.multi_cell(0, 6, f"  - {presc.get('medicamento')} ({presc.get('dosis')}): {presc.get('indicaciones', '')}")
            pdf.ln(2)

        # Tratamiento
        if consulta.get('tratamiento'):
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 8, "Tratamiento:", 0, 1)
            pdf.set_font("Arial", '', 10)
            pdf.multi_cell(0, 6, f"  {consulta['tratamiento']}")
            pdf.ln(2)

        # Notas
        if consulta.get('notas'):
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(0, 8, "Notas de Evolución:", 0, 1)
            pdf.set_font("Arial", '', 10)
            pdf.multi_cell(0, 6, f"{consulta['notas']}")
            pdf.ln(4)

        pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Línea separadora
        pdf.ln(6)

    # Pie de página
    pdf.set_y(-15)
    pdf.set_font("Arial", 'I', 8)
    pdf.set_text_color(120)
    pdf.cell(0, 10, f"Generado por DenverStimuCheck - {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 0, 'C')

    pdf.output(output_path)
    return output_path
