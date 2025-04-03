import matplotlib
matplotlib.use('Agg')  # Configuración ANTES de importar pyplot
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
import io
from matplotlib.dates import DateFormatter

def generar_pdf_signos_vitales(paciente, signos_vitales, output_path="output.pdf"):
    """
    Genera un PDF profesional con la evolución de todos los signos vitales del paciente
    
    Args:
        paciente: Objeto Paciente con los datos del paciente
        signos_vitales: Lista de objetos SignoVital
        output_path: Ruta donde se guardará el PDF (opcional)
    
    Returns:
        str: Ruta del archivo PDF generado
    """
    try:
        # Ordenar signos vitales por fecha
        signos_ordenados = sorted(signos_vitales, key=lambda x: datetime.strptime(x.fecha, "%d-%m-%Y"))
        
        # Crear PDF con primera página vertical
        pdf = FPDF(orientation='P')  # Primera página en portrait (vertical)
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        
        # Encabezado profesional
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, txt="Reporte de Evolución de Signos Vitales", ln=1, align='C')
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, txt=f"Paciente: {paciente.nombre} {paciente.apellido}", ln=1)
        pdf.cell(0, 8, txt=f"Fecha de generación: {datetime.now().strftime('%d-%m-%Y %H:%M')}", ln=1)
        pdf.ln(10)
        
        # Tabla de signos vitales con mejor formato
        col_widths = [25, 25, 25, 25, 20, 20, 20]  # Anchos personalizados
        headers = ["Fecha", "Presión", "Cardíaca", "Respiración", "Temp. (°C)", "Peso (kg)", "Talla (cm)"]
        
        # Encabezados de tabla
        pdf.set_font("Arial", 'B', 10)
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, border=1, align='C')
        pdf.ln()
        
        # Datos de la tabla
        pdf.set_font("Arial", size=9)
        for signo in signos_ordenados:
            pdf.cell(col_widths[0], 8, signo.fecha, border=1)
            pdf.cell(col_widths[1], 8, signo.presion_arterial, border=1)
            pdf.cell(col_widths[2], 8, str(signo.frecuencia_cardiaca), border=1, align='C')
            pdf.cell(col_widths[3], 8, str(signo.frecuencia_respiratoria), border=1, align='C')
            pdf.cell(col_widths[4], 8, str(signo.temperatura), border=1, align='C')
            pdf.cell(col_widths[5], 8, str(signo.peso), border=1, align='C')
            pdf.cell(col_widths[6], 8, str(signo.talla), border=1, align='C')
            pdf.ln()
        
        # Gráficos de evolución
        fechas = [datetime.strptime(s.fecha, "%d-%m-%Y") for s in signos_ordenados]
        fecha_str = [s.fecha for s in signos_ordenados]  # Para usar en las etiquetas
        
        # Función auxiliar para crear gráficos con mejor formato de fechas
        def _agregar_grafico(fechas, valores, titulo, ylabel, color='b'):
            plt.figure(figsize=(10, 4))
            plt.plot(fechas, valores, marker='o', linestyle='-', color=color)
            plt.title(titulo, pad=20)
            plt.xlabel('Fecha', labelpad=10)
            plt.ylabel(ylabel, labelpad=10)
            
            # Formatear eje X para mostrar fechas correctamente
            ax = plt.gca()
            ax.xaxis.set_major_formatter(DateFormatter("%d-%m-%Y"))
            plt.xticks(fechas, rotation=45, ha='right')
            
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            
            img_bytes = io.BytesIO()
            plt.savefig(img_bytes, format='png', dpi=100, bbox_inches='tight')
            plt.close()
            return img_bytes
        
        # 1. Gráfico de Presión Arterial
        try:
            sistolica = [float(s.presion_arterial.split('/')[0]) for s in signos_ordenados]
            diastolica = [float(s.presion_arterial.split('/')[1]) for s in signos_ordenados]
            
            plt.figure(figsize=(10, 4))
            plt.plot(fechas, sistolica, marker='o', label='Sistólica (mmHg)')
            plt.plot(fechas, diastolica, marker='o', label='Diastólica (mmHg)')
            plt.title("Evolución de la Presión Arterial", pad=20)
            plt.xlabel('Fecha', labelpad=10)
            plt.ylabel('Presión (mmHg)', labelpad=10)
            
            # Formatear eje X
            ax = plt.gca()
            ax.xaxis.set_major_formatter(DateFormatter("%d-%m-%Y"))
            plt.xticks(fechas, rotation=45, ha='right')
            
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.legend()
            plt.tight_layout()
            
            img_bytes = io.BytesIO()
            plt.savefig(img_bytes, format='png', dpi=100, bbox_inches='tight')
            plt.close()
            
            # Agregar página horizontal para el gráfico
            pdf.add_page(orientation='L')
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, "Evolución de la Presión Arterial", ln=1)
            pdf.image(img_bytes, x=10, w=pdf.w - 20)
        except Exception as e:
            print(f"Error en gráfico de presión: {str(e)}")
        
        # Gráficos para otros signos vitales
        graficos = [
            ([int(s.frecuencia_cardiaca) for s in signos_ordenados], 
             "Evolución de la Frecuencia Cardíaca", 
             "Latidos por minuto", 
             'green'),
             
            ([int(s.frecuencia_respiratoria) for s in signos_ordenados], 
             "Evolución de la Frecuencia Respiratoria", 
             "Respiraciones por minuto", 
             'purple'),
             
            ([float(s.temperatura) for s in signos_ordenados], 
             "Evolución de la Temperatura", 
             "Temperatura (°C)", 
             'red'),
             
            ([float(s.peso) for s in signos_ordenados], 
             "Evolución del Peso", 
             "Peso (kg)", 
             'orange'),
             
            ([float(s.talla) for s in signos_ordenados], 
             "Evolución de la Talla", 
             "Talla (cm)", 
             'brown')
        ]
        
        for valores, titulo, ylabel, color in graficos:
            try:
                img_bytes = _agregar_grafico(fechas, valores, titulo, ylabel, color)
                # Agregar página horizontal para cada gráfico
                pdf.add_page(orientation='L')
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, titulo, ln=1)
                pdf.image(img_bytes, x=10, w=pdf.w - 20)
            except Exception as e:
                print(f"Error en gráfico {titulo}: {str(e)}")
        
        # Guardar PDF
        pdf.output(output_path)
        return output_path
        
    except Exception as e:
        print(f"Error general al generar PDF: {str(e)}")
        raise
    finally:
        plt.close('all')  # Limpieza garantizada