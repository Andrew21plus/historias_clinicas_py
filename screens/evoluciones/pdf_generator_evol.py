# pdf_generator.py
from fpdf import FPDF
from datetime import datetime

def generar_pdf_evoluciones(paciente_info, consultas, output_path="evoluciones.pdf"):
    pdf = FPDF()
    pdf.add_page()
    
    # Configuración inicial
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Historia Clínica - {paciente_info['nombre']}", 0, 1, 'C')
    pdf.ln(10)
    
    # Información del paciente
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Datos del Paciente:", 0, 1)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Nombre: {paciente_info['nombre']} {paciente_info['apellido']}", 0, 1)
    pdf.cell(0, 10, f"Historia Clínica: {paciente_info['num_historia']}", 0, 1)
    pdf.cell(0, 10, f"Edad/Sexo: {paciente_info['edad']} años / {paciente_info['sexo']}", 0, 1)
    pdf.ln(10)
    
    # Consultas
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Evoluciones:", 0, 1)
    pdf.ln(5)
    
    for consulta in consultas:
        # Fecha de consulta
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"Consulta del {consulta['fecha']}", 0, 1)
        pdf.set_font("Arial", '', 10)
        
        # Signos vitales
        if consulta.get('signos_vitales'):
            pdf.cell(0, 10, "Signos Vitales:", 0, 1)
            signos = consulta['signos_vitales']
            pdf.cell(0, 10, f"  - Presión Arterial: {signos.get('presion', 'N/A')} mmHg", 0, 1)
            pdf.cell(0, 10, f"  - Frecuencia Cardíaca: {signos.get('frec_cardiaca', 'N/A')} lpm", 0, 1)
            pdf.cell(0, 10, f"  - Frecuencia Respiratoria: {signos.get('frec_respi', 'N/A')} rpm", 0, 1)
            pdf.cell(0, 10, f"  - Temperatura: {signos.get('temp', 'N/A')} °C", 0, 1)
            pdf.cell(0, 10, f"  - Peso: {signos.get('peso', 'N/A')} kg", 0, 1)
            pdf.cell(0, 10, f"  - Talla: {signos.get('talla', 'N/A')} cm", 0, 1)
            pdf.ln(5)
        
        # Diagnósticos
        if consulta.get('diagnosticos'):
            pdf.cell(0, 10, "Diagnósticos:", 0, 1)
            for diag in consulta['diagnosticos']:
                pdf.cell(0, 10, f"  - {diag.get('cie', 'N/A')}: {diag.get('descripcion', 'N/A')} ({diag.get('estado', 'N/A')})", 0, 1)
            pdf.ln(5)
        
        # Prescripciones
        if consulta.get('prescripciones'):
            pdf.cell(0, 10, "Prescripciones:", 0, 1)
            for presc in consulta['prescripciones']:
                pdf.cell(0, 10, f"  - {presc.get('medicamento', 'N/A')} - {presc.get('dosis', 'N/A')}", 0, 1)
                if presc.get('indicaciones'):
                    pdf.cell(0, 10, f"    Indicaciones: {presc['indicaciones']}", 0, 1)
            pdf.ln(5)
        
        # Tratamientos
        if consulta.get('tratamiento'):
            pdf.cell(0, 10, "Tratamiento:", 0, 1)
            pdf.cell(0, 10, f"  - {consulta['tratamiento']}", 0, 1)
            pdf.ln(5)
        
        # Notas de evolución
        if consulta.get('notas'):
            pdf.cell(0, 10, "Notas de Evolución:", 0, 1)
            pdf.multi_cell(0, 10, f"  {consulta['notas']}")
            pdf.ln(5)
        
        pdf.ln(10)
    
    # Pie de página
    pdf.set_y(-15)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 0, 'C')
    
    pdf.output(output_path)
    return output_path